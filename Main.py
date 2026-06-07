import os
import requests
import datetime

# Récupération sécurisée de la clé depuis les Secrets GitHub
API_KEY = os.getenv('API_KEY')
API_HOST = "api-football-v1.p.rapidapi.com"

def get_matches_today():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://{API_HOST}/v3/fixtures"
    querystring = {"date": today}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.json().get('response', [])
        else:
            print(f"Erreur API {response.status_code}: {response.text}")
            return []
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return []

# --- EXÉCUTION ---
print(f"🚀 Démarrage du scan automatique - {datetime.datetime.now()}")
matchs = get_matches_today()

# Ouvre le fichier en mode écriture ('w')
with open("resultats_analyse.txt", "w", encoding="utf-8") as f:
    if matchs:
        print(f"✅ {len(matchs)} matchs trouvés.")
        f.write(f"Rapport du {datetime.datetime.now()}\n")
        f.write("-" * 30 + "\n")
        for match in matchs:
            h = match['teams']['home']['name']
            a = match['teams']['away']['name']
            ligne = f"{h} vs {a}"
            print(f"Analyse : {ligne}")
            f.write(ligne + "\n")
        print("💾 Résultats enregistrés dans 'resultats_analyse.txt'")
    else:
        f.write("Aucun match trouvé pour aujourd'hui.")
        print("⚠️ Aucun match ou échec de l'API.")
