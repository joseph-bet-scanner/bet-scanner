import requests
import os

# Configuration API
API_KEY = os.getenv('API_KEY')
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
}
SEUIL_CONFIANCE = 0.05
BANKROLL = 1000

def get_live_matches():
    url = "https://sofascore.p.rapidapi.com/v1/events/live"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return [m['id'] for m in response.json().get('events', [])[:5]]
    except Exception as e:
        print(f"Erreur get_live_matches: {e}")
        return []

def calculate_kelly_stake(prob, cote, bankroll):
    if cote <= 1: return 0
    b = cote - 1
    kelly = ((cote * prob) - 1) / b
    return max(0, (kelly * 0.25) * bankroll)

def get_match_stats(match_id):
    try:
        h2h_res = requests.get(f"https://sofascore.p.rapidapi.com/matches/{match_id}/h2h", headers=HEADERS).json()
        odds_res = requests.get(f"https://sofascore.p.rapidapi.com/matches/{match_id}/odds/1/all", headers=HEADERS).json()
        
        # Stats H2H
        duel = h2h_res.get('teamDuel', {})
        h_wins = duel.get('homeWins', 0)
        a_wins = duel.get('awayWins', 0)
        draws = duel.get('draws', 0)
        total = h_wins + a_wins + draws
        
        # Moyenne buts
        prev = h2h_res.get('previousMatches', [])
        goals = sum([m.get('homeScore', {}).get('current', 0) + m.get('awayScore', {}).get('current', 0) for m in prev[:5]])
        avg_goals = (goals / len(prev[:5])) if prev else 0
        
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
    except Exception:
        return None

if __name__ == "__main__":
    print("--- Démarrage complet du scan ---")
    matches = get_live_matches()
    if not matches:
        print("Aucun match live trouvé pour le moment.")
    for m_id in matches:
        res = get_match_stats(m_id)
        if res:
            prob, cote, value, goals = res
            status = "!!! VALUE BET !!!" if value else "Standard"
            print(f"Match {m_id} | Prob: {prob:.2f} | Cote: {cote:.2f} | Buts: {goals:.1f} | {status}")
        else:
            print(f"Match {m_id} | Données insuffisantes pour analyse.")
    print("--- Scan terminé ---")
