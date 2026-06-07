import requests
import os

# Configuration API
API_KEY = os.getenv('API_KEY')
HEADERS = {
    "x-rapidapi-host": "free-football-api-data.p.rapidapi.com",
    "x-rapidapi-key": API_KEY,
    "Content-Type": "application/json"
}

def get_data(endpoint):
    """Fonction générique pour appeler l'API sans erreurs"""
    url = f"https://free-football-api-data.p.rapidapi.com/{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erreur lors de la requête vers {endpoint}: {e}")
        return None

def main():
    print("--- SCAN DE PRODUCTION INITIALISÉ ---")
    
    # 1. Récupération de la liste des pays/ligues
    data = get_data("football-all-countries")
    
    if data:
        print(f"Connexion réussie. Analyse de {len(data)} ligues détectées.")
        print("-" * 40)
        
        # 2. Traitement des résultats (Tri et affichage)
        # On affiche les 10 premières ligues pour valider le flux
        for item in data[:10]:
            name = item.get('name', 'N/A')
            league_id = item.get('id', 'N/A')
            print(f"Ligue identifiée : {name} [ID: {league_id}]")
            
        print("-" * 40)
        print("Scan terminé. Système opérationnel.")
    else:
        print("Erreur : Aucune donnée reçue du serveur.")

if __name__ == "__main__":
    main()
