import requests
import os

# Configuration de la clé API
API_KEY = os.getenv('API_KEY')
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
}

def get_live_matches():
    # URL exacte fournie par ton Playground
    url = "https://sofascore.p.rapidapi.com/tournaments/get-live-events?sport=football"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        # On extrait les IDs des événements (selon la structure habituelle de l'API)
        return [m['id'] for m in data.get('events', [])[:5]]
    except Exception as e:
        print(f"Erreur get_live_matches: {e}")
        return []

def get_match_stats(match_id):
    try:
        # Endpoints pour stats et h2h
        odds_url = f"https://sofascore.p.rapidapi.com/matches/{match_id}/odds/1/all"
        h2h_url = f"https://sofascore.p.rapidapi.com/matches/{match_id}/h2h"
        
        odds_res = requests.get(odds_url, headers=HEADERS).json()
        h2h_res = requests.get(h2h_url, headers=HEADERS).json()
        
        # Calcul cote
        c1 = 2.0
        try:
            markets = odds_res.get('markets', [])
            if markets:
                choices = markets[0].get('choices', [])
                if choices:
                    val = choices[0].get('fractionalValue', '1/1')
                    num, den = map(int, val.split('/'))
                    c1 = (num / den) + 1
        except: pass
        
        # Estimation xG
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

if __name__ == "__main__":
    print("--- Démarrage du scan Sofascore ---")
    matches = get_live_matches()
    if not matches:
        print("Aucun match trouvé.")
    else:
        print(f"Matchs trouvés : {len(matches)}")
        for m_id in matches:
            stats = get_match_stats(m_id)
            print(f"Match ID {m_id} : xG Home {stats[0]:.2f}, xG Away {stats[1]:.2f}, Cote {stats[2]:.2f}")
    print("--- Scan terminé ---")
