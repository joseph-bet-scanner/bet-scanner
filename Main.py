import os
import requests
import datetime

# Configuration
API_KEY = os.getenv('API_KEY')
API_HOST = "sofascore.p.rapidapi.com"

def get_sofascore_matches():
    # Date du jour au format requis par Sofascore
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # URL de l'API Sofascore pour les matchs de football
    url = f"https://{API_HOST}/v1/sport/football/scheduled-events/{today}"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('events', [])
        else:
            print(f"Erreur API {response.status_code}: {response.text}")
            return []
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return []

# Traitement des données
def run_scanner():
    print("Démarrage du scan Sofascore...")
    matches = get_sofascore_matches()
    
    if not matches:
        print("Aucun match trouvé pour aujourd'hui.")
        return

    with open("resultats_analyse.txt", "w", encoding="utf-8") as f:
        for match in matches:
            home = match.get('homeTeam', {}).get('name', 'Inconnu')
            away = match.get('awayTeam', {}).get('name', 'Inconnu')
            tournament = match.get('tournament', {}).get('name', 'Inconnu')
            
            ligne = f"Match: {home} vs {away} | Compétition: {tournament}\n"
            print(ligne.strip())
            f.write(ligne)
            
    print("Analyse terminée et sauvegardée dans resultats_analyse.txt")

if __name__ == "__main__":
    run_scanner()
