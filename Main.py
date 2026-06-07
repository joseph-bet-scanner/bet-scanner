import requests
import os

# Configuration avec ta clé API
API_KEY = os.getenv('API_KEY')
HEADERS = {
    "x-rapidapi-host": "sofascore.p.rapidapi.com",
    "x-rapidapi-key": API_KEY
}

def get_matches_for_today():
    # En utilisant l'endpoint que tu as validé via ton curl
    # Note : teamId=38 est un exemple, assure-toi d'utiliser 
    # l'ID d'une équipe qui joue aujourd'hui
    url = "https://sofascore.p.rapidapi.com/teams/get-tournaments?teamId=38"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        # On extrait les tournois/événements
        # Ajuste 'tournaments' selon la structure du JSON retourné
        return data.get('tournaments', [])
    except Exception as e:
        print(f"Erreur lors de la récupération : {e}")
        return []

if __name__ == "__main__":
    print("--- Scan des matchs ---")
    tournois = get_matches_for_today()
    
    if tournois:
        print(f"Trouvé {len(tournois)} tournois actifs.")
        for t in tournois:
            print(f"Tournoi: {t.get('tournament', {}).get('name', 'N/A')}")
    else:
        print("Aucun tournoi trouvé pour cette équipe aujourd'hui.")
    print("--- Scan terminé ---")
