import os
import requests
import numpy as np
from scipy.stats import poisson

HEADERS = {"x-rapidapi-key": os.getenv('API_KEY'), "x-rapidapi-host": "sofascore.p.rapidapi.com"}

def get_live_matches():
    # Récupère les matchs du jour (ex: top ligues)
    url = "https://sofascore.p.rapidapi.com/matches/get-by-date?date=2026-06-07"
    response = requests.get(url, headers=HEADERS)
    # Retourne une liste de 10 IDs de matchs
    return [m['id'] for m in response.json().get('events', [])[:10]]

def get_match_stats(match_id):
    # Récupère cotes et stats H2H pour estimer les xG
    odds_res = requests.get(f"https://sofascore.p.rapidapi.com/matches/get-all-odds?matchId={match_id}", headers=HEADERS).json()
    h2h_res = requests.get(f"https://sofascore.p.rapidapi.com/matches/get-h2h?matchId={match_id}", headers=HEADERS).json()
    
    # Extraction cote 1 (simple)
    c1 = 2.0 # Default
    try:
        c1 = float(odds_res['markets'][0]['choices'][0]['fractionalValue'].split('/')[0]) / float(odds_res['markets'][0]['choices'][0]['fractionalValue'].split('/')[1]) + 1
    except: pass
    
    # Estimation xG basée sur l'historique
    h_wins = h2h_res.get('teamDuel', {}).get('homeWins', 1)
    a_wins = h2h_res.get('teamDuel', {}).get('awayWins', 1)
    return (1.5 * (h_wins/(h_wins+a_wins)) + 0.5), (1.5 * (a_wins/(h_wins+a_wins)) + 0.5), c1

def main():
    match_ids = get_live_matches()
    print(f"{'MATCH ID':<10} | {'xG D/E':<8} | {'COTE':<6} | {'PICK':<10}")
    print("-" * 50)
    
    for m_id in match_ids:
        hxG, axG, c1 = get_match_stats(m_id)
        # Loi de Poisson
        p1 = np.sum(np.tril([[poisson.pmf(i, hxG) * poisson.pmf(j, axG) for j in range(3)] for i in range(3)], -1))
        
        # Alerte si EV > 10%
        ev = (p1 * c1) - 1
        pick = "⚠️ Victoire 1" if ev > 0.10 else "Victoire 1"
        
        print(f"{m_id:<10} | {hxG:.1f}/{axG:.1f} | {c1:.2f} | {pick}")

if __name__ == "__main__":
    main()
