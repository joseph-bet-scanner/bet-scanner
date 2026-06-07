import requests
import os

# Configuration
API_KEY = os.getenv('API_KEY')
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
}
SEUIL_CONFIANCE = 0.05  # 5% de marge
BANKROLL = 1000         # Ton capital de départ pour le calcul

def get_live_matches():
    url = "https://sofascore.p.rapidapi.com/v1/events/live"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return [m['id'] for m in response.json().get('events', [])[:5]]
    except: return []

def calculate_kelly_stake(prob, cote, bankroll):
    if cote <= 1: return 0
    b = cote - 1
    kelly = ((cote * prob) - 1) / b
    return max(0, (kelly * 0.25) * bankroll)

def get_match_stats(match_id):
    try:
        h2h_res = requests.get(f"https://sofascore.p.rapidapi.com/matches/{match_id}/h2h", headers=HEADERS).json()
        odds_res = requests.get(f"https://sofascore.p.rapidapi.com/matches/{match_id}/odds/1/all", headers=HEADERS).json()
        
        # Stats
        duel = h2h_res.get('teamDuel', {})
        h_wins, a_wins, draws = duel.get('homeWins', 0), duel.get('awayWins', 0), duel.get('draws', 0)
        total = h_wins + a_wins + draws
        
        # Moyenne buts
        goals = sum([m.get('homeScore', {}).get('current', 0) + m.get('awayScore', {}).get('current', 0) 
                     for m in h2h_res.get('previousMatches', [])[:5]])
        avg_goals = (goals / len(h2h_res.get('previousMatches', []))) if h2h_res.get('previousMatches') else 0
        
        # Cote
        c1 = 2.0
        markets = odds_res.get('markets', [])
        if markets and 'choices' in markets[0]:
            val = markets[0]['choices'][0].get('fractionalValue', '1/1')
            num, den = map(int, val.split('/'))
            c1 = (num / den) + 1
        
        prob_home = ((h_wins + draws) / total) if total > 0 else 0.5
        is_value = prob_home > (1 / c1) + SEUIL_CONFIANCE
        
        return prob_home, c1, is_value, avg_goals
    except: return None

if __name__ == "__main__":
    print("--- Scan de Production ---")
    matches = get_live_matches()
    for m_id in matches:
        res = get_match_stats(m_id)
        if res:
            prob, cote, value, goals = res
            if value:
                stake = calculate_kelly_stake(prob, cote, BANKROLL)
                print(f"Match {m_id} | !!! VALUE BET !!! | DC: {prob:.2f} | Cote: {cote:.2f} | Buts: {goals:.1f} | Mise: {stake:.2f}€")
            else:
                print(f"Match {m_id} | Standard | DC: {prob:.2f} | Cote: {cote:.2f} | Buts: {goals:.1f}")
    print("--- Scan terminé ---")
