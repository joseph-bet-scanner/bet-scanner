import os
import requests

def get_sofascore_odds(event_id):
    # Remplace l'URL par celle que le testeur RapidAPI utilise pour les cotes
    url = f"https://sofascore.p.rapidapi.com/v1/event/{event_id}/odds/1/all"
    
    headers = {
        "x-rapidapi-key": os.getenv('API_KEY'),
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # On parcourt les marchés (ex: "Full time")
        for market in data.get('markets', []):
            print(f"Marché : {market.get('marketName')}")
            for choice in market.get('choices', []):
                print(f" - Choix: {choice.get('name')} | Cote: {choice.get('fractionalValue')}")
    else:
        print(f"Erreur {response.status_code}: {response.text}")

if __name__ == "__main__":
    # Remplace par un ID de match réel trouvé dans tes tests
    get_sofascore_odds("8701972")
