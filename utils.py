import requests

def fetch_odds(api_key, league_code, min_odds):
    """
    Fetches sports odds from The Odds API and filters them based on minimum odds.
    
    Args:
        api_key (str): Your API key from the-odds-api.com.
        league_code (str): The sport/league identifier (e.g., 'soccer_epl').
        min_odds (float): The minimum odds threshold for filtering.
        
    Returns:
        list: A list of dictionaries containing match details, or None if failed.
    """
    url = f"https://api.the-odds-api.com/v4/sports/{league_code}/odds/?apiKey={api_key}&regions=eu&markets=h2h"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return None
    
    matches = []
    
    for m in data:
        home = m['home_team']
        away = m['away_team']
        
        # Check if bookmakers and markets exist to avoid errors
        if not m['bookmakers'] or not m['bookmakers'][0]['markets']:
            continue
            
        # Get odds from the first available bookmaker
        bookmaker = m['bookmakers'][0]
        market = bookmaker['markets'][0]
        
        for outcome in market['outcomes']:
            if outcome['price'] >= min_odds:
                matches.append({
                    "Pertandingan": f"{home} vs {away}",
                    "Pilihan": outcome['name'],
                    "Odds": outcome['price']
                })
                
    return matches
