import os
import requests
import datetime

# Récupération de la clé depuis les secrets GitHub
API_KEY = os.getenv('API_KEY')
API_HOST = "sofascore.p.rapidapi.com"

def get_sofascore_matches():
    # Date du jour
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://{API_HOST}/v1/sport/football/scheduled-events/{today}"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('events', [])
        else:
            print(f"Erreur API {response.status_code}: {response.text}")
            return []
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return []

def run():
    print("--- Scan des matchs Sofascore ---")
    matches = get_sofascore_matches()
    
    if not matches:
        print("Aucun match trouvé ou erreur de connexion.")
        return

    # Affichage direct dans les logs (plus simple que la gestion de fichier)
    for match in matches:
        home = match.get('homeTeam', {}).get('name', 'N/A')
        away = match.get('awayTeam', {}).get('name', 'N/A')
        comp = match.get('tournament', {}).get('name', 'N/A')
        print(f"Match: {home} vs {away} | Compétition: {comp}")

if __name__ == "__main__":
    run()
