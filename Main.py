import requests
import os

# Configuration de la clé API
API_KEY = os.getenv('API_KEY')
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
}

def get_live_matches():
    # Utilisation d'un endpoint plus stable pour la liste des matchs
    url = "https://sofascore.p.rapidapi.com/v1/events/live"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        # On récupère les IDs des événements
        return [m['id'] for m in data.get('events', [])[:5]]
    except Exception as e:
        print(f"Erreur get_live_matches: {e}")
        return []

def get_match_stats(match_id):
    try:
        # URL corrigée selon ton exemple curl
        url = "https://sofascore.p.rapidapi.com/matches/get-h2h-events"
        # Le paramètre matchId est obligatoire pour cet endpoint
        querystring = {"matchId": str(match_id)}
        
        response = requests.get(url, headers=HEADERS, params=querystring)
        response.raise_for_status()
        
        data = response.json()
        # Affichage pour debug dans les logs GitHub
        print(f"Succès pour match {match_id}")
        return True
    except Exception as e:
        print(f"Erreur sur match {match_id}: {e}")
        return False

if __name__ == "__main__":
    print("--- Démarrage du scan ---")
    matches = get_live_matches()
    if not matches:
        print("Aucun match trouvé.")
    else:
        for m_id in matches:
            get_match_stats(m_id)
    print("--- Scan terminé ---")
