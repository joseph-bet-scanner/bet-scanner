import os
import requests

def get_match_odds():
    # ID du match que tu as testé
    match_id = "8897222"
    url = f"https://sofascore.p.rapidapi.com/matches/get-all-odds?matchId={match_id}"
    
    headers = {
        "x-rapidapi-key": os.getenv('API_KEY'),
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # On affiche les cotes pour confirmer la réussite
            print(f"Cotes récupérées pour le match {match_id}:")
            # Exemple : lire le premier marché disponible
            markets = data.get('markets', [])
            for market in markets:
                print(f"Marché: {market.get('marketName')}")
                for choice in market.get('choices', []):
                    print(f" - {choice.get('name')}: {choice.get('fractionalValue')}")
        else:
            print(f"Erreur API {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    get_match_odds()
