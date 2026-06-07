import pandas as pd
import math
import sqlite3
import requests
from io import StringIO

# --- CONFIGURATION ---
DB_PATH = 'historique_analyses.db'
REPORT_FILE = 'rapport_bets.txt'

# Dictionnaire des ligues
championnats = {
    "Premier League": "https://www.football-data.co.uk/mmz4281/2526/E0.csv",
    "La Liga": "https://www.football-data.co.uk/mmz4281/2526/SP1.csv",
    "Serie A": "https://www.football-data.co.uk/mmz4281/2526/I1.csv",
    "Bundesliga": "https://www.football-data.co.uk/mmz4281/2526/D1.csv",
    "Ligue 1": "https://www.football-data.co.uk/mmz4281/2526/F1.csv",
    "Argentine": "https://www.football-data.co.uk/mmz4281/2526/ARG.csv",
    "Brésil": "https://www.football-data.co.uk/mmz4281/2526/BRA.csv",
    "Norvège": "https://www.football-data.co.uk/mmz4281/2526/N1.csv"
}

def get_csv_data(url):
    # La carte d'identité pour passer le 403 Forbidden
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return StringIO(response.text)

def clean_name(name):
    return str(name).lower().replace(" ", "").replace("ü", "u").replace("é", "e")

def get_team_stats(team_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(buts_pour), AVG(buts_contre) FROM historique_matchs WHERE equipe_clean = ?", (clean_name(team_name),))
    row = cursor.fetchone()
    conn.close()
    return (float(row[0]), float(row[1])) if row and row[0] is not None else (1.2, 1.2)

def calculer_poisson(lh, la):
    def p(k, lam): return (lam**k * math.exp(-lam)) / math.factorial(k)
    p1, px, p2 = 0, 0, 0
    for i in range(6):
        for j in range(6):
            prob = p(i, lh) * p(j, la)
            if i > j: p1 += prob
            elif i == j: px += prob
            else: p2 += prob
    return p1, px, p2

# --- SCANNER ---
open(REPORT_FILE, "w").close() 
print("🚀 Scan mondial lancé avec contournement anti-bot...")

for nom_ligue, url in championnats.items():
    print(f"Analyse de {nom_ligue}...")
    try:
        # Utilisation de la nouvelle fonction pour le téléchargement
        df = pd.read_csv(get_csv_data(url))
        matchs_a_venir = df[df['FTHG'].isna()] 
        
        for _, row in matchs_a_venir.iterrows():
            h_team, a_team = row['HomeTeam'], row['AwayTeam']
            att_h, def_h = get_team_stats(h_team)
            att_a, def_a = get_team_stats(a_team)
            
            lh, la = att_h * def_a, att_a * def_h
            p1, px, p2 = calculer_poisson(lh, la)
            
            conf = max(p1, p2, px)
            if conf >= 0.60:
                type_pari = "1" if p1 == conf else ("2" if p2 == conf else "Nul")
                msg = f"🔥 {nom_ligue} | {h_team} vs {a_team} | Pari: {type_pari} | Conf: {conf*100:.1f}%"
                with open(REPORT_FILE, "a") as f: f.write(msg + "\n")
    except Exception as e:
        print(f"Erreur sur {nom_ligue}: {e}")

print("✅ Scan terminé. Vérifie ton fichier rapport_bets.txt.")
