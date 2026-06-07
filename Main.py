import requests
import os
from datetime import datetime

API_KEY = os.getenv('API_KEY')
HEADERS = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "sofascore.p.rapidapi.com"}
SEUIL_CONFIANCE = 0.05
BANKROLL = 1000

def get_todays_matches():
    # Récupère la date actuelle
    aujourd_hui = datetime.now().strftime('%Y-%m-%d')
    url = f"https://sofascore.p.rapidapi.com/matches/date/{aujourd_hui}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        # Retourne les IDs des matchs du jour
        return [m['id'] for m in response.json().get('events', [])[:10]]
    except Exception as e:
        print(f"Erreur API (Date): {e}")
        return []

def get_match_stats(match_id):
    try:
        h2h_res = requests.get(f"https://sofascore.p.rapidapi.com/matches/{match_id}/h2h", headers=HEADERS).json()
        odds_res = requests.get(f"https://sofascore.p.rapidapi.com/matches/{match_id}/odds/1/all", headers=HEADERS).json()
        
        duel = h2h_res.get('teamDuel', {})
        total = duel.get('homeWins', 0) + duel.get('awayWins', 0) + duel.get('draws', 0)
        
        c1 = 2.0
        markets = odds_res.get('markets', [])
        if markets and 'choices' in markets[0]:
            val = markets[0]['choices'][0].get('fractionalValue', '1/1')
            num, den = map(int, val.split('/'))
            c1 = (num / den) + 1
        
        prob_home = ((duel.get('homeWins', 0) + duel.get('draws', 0)) / total) if total > 0 else 0
        return {"id": match_id, "prob": prob_home, "cote": c1}
    except: return None

if __name__ == "__main__":
    print(f"--- Scan des matchs du {datetime.now().strftime('%Y-%m-%d')} ---")
    match_ids = get_todays_matches()
    results = []

    for m_id in match_ids:
        stats = get_match_stats(m_id)
        if stats and stats["prob"] > 0:
            results.append(stats)

    # Tri par probabilité décroissante
    results.sort(key=lambda x: x["prob"], reverse=True)

    for res in results:
        is_value = res["prob"] > (1 / res["cote"]) + SEUIL_CONFIANCE
        status = "!!! VALUE BET !!!" if is_value else "Standard"
        print(f"Match {res['id']} | Prob: {res['prob']:.2f} | Cote: {res['cote']:.2f} | {status}")
    
    print("--- Scan terminé ---")
