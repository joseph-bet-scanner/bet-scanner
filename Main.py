import requests
import os

# 1. Chargement de la clé API depuis GitHub Secrets
API_KEY = os.getenv('API_KEY')
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
}

def get_live_matches():
    # URL mis à jour pour correspondre aux standards actuels de l'API Sofascore
    url = "https://sofascore.p.rapidapi.com/matches/get-by-date?date=2026-06-07"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return [m['id'] for m in data.get('events', [])[:10]]
    except Exception as e:
        print(f"Erreur lors de la récupération des matchs: {e}")
        return []

def get_match_stats(match_id):
    try:
        # Utilisation d'URL simplifiées pour éviter les erreurs de structure
        odds_url = f"https://sofascore.p.rapidapi.com/matches/{match_id}/odds/1/all"
        h2h_url = f"https://sofascore.p.rapidapi.com/matches/{match_id}/h2h"
        
        odds_res = requests.get(odds_url, headers=HEADERS).json()
        h2h_res = requests.get(h2h_url, headers=HEADERS).json()
        
        # Extraction sécurisée de la cote
        c1 = 2.0
        try:
            markets = odds_res.get('markets', [])
            if markets:
                choices = markets[0].get('choices', [])
                if choices:
                    val = choices[0].get('fractionalValue', '1/1')
                    num, den = map(int, val.split('/'))
                    c1 = (num / den) + 1
        except: 
            pass
        
        # Estimation xG avec sécurité (évite la division par zéro)
        duel = h2h_res.get('teamDuel', {})
        h_wins = duel.get('homeWins', 1)
        a_wins = duel.get('awayWins', 1)
        total = h_wins + a_wins
        
        home_xg = (1.5 * (h_wins/total) + 0.5)
        away_xg = (1.5 * (a_wins/total) + 0.5)
        
        return home_xg, away_xg, c1
    except Exception as e:
        print(f"Erreur sur le match {match_id}: {e}")
        return 1.0, 1.0, 2.0

# Point d'entrée pour tester le script
if __name__ == "__main__":
    print("Début du scan...")
    matches = get_live_matches()
    print(f"Matchs trouvés : {len(matches)}")
    for m_id in matches:
        stats = get_match_stats(m_id)
        print(f"Match {m_id} -> xG Home: {stats[0]:.2f}, xG Away: {stats[1]:.2f}, Cote: {stats[2]:.2f}")
    print("Scan terminé.")
