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
matchs = get_matches_today()

# On ouvre toujours le fichier, même si matchs est vide
with open("resultats_analyse.txt", "w", encoding="utf-8") as f:
    f.write(f"Rapport du {datetime.datetime.now()}\n")
    if matchs:
        for match in matchs:
            h = match['teams']['home']['name']
            a = match['teams']['away']['name']
            f.write(f"{h} vs {a}\n")
    else:
        f.write("Aucun match aujourd'hui.")
        f.write("Aucun match trouvé pour aujourd'hui.")
        print("⚠️ Aucun match ou échec de l'API.")
