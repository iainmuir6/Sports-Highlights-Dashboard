"""
Iain Muir, iam9ez

"""

import pandas as pd

LEAGUE_ID = 1080747

INDICES = {
    "NBA": 3,
    "MLB": 4,
    "NHL": 5,
    "Men's College Basketball": 7,
    "Premier League": 8,
    "MLS": 9,
    "La Liga": 10,
    "Bundesliga": 11,
    "Ligue 1": 12,
    "Serie A": 13,
    "Champions League": 14,
    "Europa League": 15,
    "NFL": 16
}

LOGOS = {
    "nba": "https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg",
    "nfl": "https://upload.wikimedia.org/wikipedia/en/a/a2/National_Football_League_logo.svg",
    "mlb": "https://upload.wikimedia.org/wikipedia/en/a/a6/Major_League_Baseball_logo.svg",
    "nhl": "https://upload.wikimedia.org/wikipedia/en/3/3a/05_NHL_Shield.svg",
    "ncaab": "https://upload.wikimedia.org/wikipedia/commons/d/dd/NCAA_logo.svg",
    "epl": "https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg",
    "mls": "https://upload.wikimedia.org/wikipedia/commons/7/76/MLS_crest_logo_RGB_gradient.svg",
    "liga": "https://upload.wikimedia.org/wikipedia/commons/1/13/LaLiga.svg",
    "bund": "https://upload.wikimedia.org/wikipedia/en/d/df/Bundesliga_logo_%282017%29.svg",
    "fran": "https://upload.wikimedia.org/wikipedia/en/b/ba/Ligue_1_Uber_Eats.svg",
    "seri": "https://upload.wikimedia.org/wikipedia/en/e/e1/Serie_A_logo_%282019%29.svg",
    "chlg": "https://upload.wikimedia.org/wikipedia/en/b/bf/UEFA_Champions_League_logo_2.svg",
    "uefa": "https://upload.wikimedia.org/wikipedia/en/0/03/Europa_League.svg"
}

CODES = {
    "NBA": "nba",
    "NFL": "nfl",
    "MLB": "mlb",
    "NHL": "nhl",
    "Men's College Basketball": "ncaab",
    "Premier League": "epl",
    "MLS": "mls",
    "La Liga": "liga",
    "Bundesliga": "bund",
    "Ligue 1": "fran",
    "Serie A": "seri",
    "Champions League": "chlg",
    "Europa League": "uefa"
}

LOGO_CODES = {
    "nba": "basketball",
    "nfl": "football",
    "mlb": "baseball",
    "nhl": "hockey",
    "ncaab": "basketball",
    "epl": "soccer",
    "mls": "soccer",
    "liga": "soccer",
    "bund": "soccer",
    "fran": "soccer",
    "seri": "soccer",
    "chlg": "soccer",
    "uefa": "soccer"
}

RESPONSE = pd.DataFrame(
    {'Timestamp': '7/21/2020 11:08:49',
     'Email Address': 'iam9ez@virginia.edu',
     'Sports League you would like to receive highlights from:': "NBA, NFL, MLB, NHL, Men's College Basketball,"
                                                                 " Premier League, MLS, La Liga, Bundesliga,"
                                                                 " Ligue 1, Serie A, Champions League, Europa League",
     'NBA Teams': 'BOS Celtics, BKN Nets, DAL Mavericks, DEN Nuggets, HOU Rockets, LA Clippers, LA Lakers,'
                  ' MEM Grizzlies, MIA Heat, MIL Bucks, NO Pelicans, PHI 76ers, TOR Raptors, WAS Wizards',
     'MLB Teams': 'BOS Red Sox, CHI Cubs, CLE Indians, COL Rockies, LA Angels, LA Dodgers, MIN Twins, NY Yankees,'
                  ' SF Giants, STL Cardinals, TB Rays, WSH Nationals',
     'NHL Teams': 'BOS Bruins, CHI Blackhawks, NY Rangers, PHI Flyers, PIT Penguins, SJ Sharks,'
                  ' TB Lightning, VGS Golden Knights, WAS Capitals',
     'Would you like condensed or full highlights?': 'Condensed',
     'NCAA Basketball Teams': 'Virginia, Duke, Notre Dame, Virginia Tech, North Carolina, Texas, Maryland,'
                              ' Ohio State, Michigan, Indiana, Arizona, Stanford, Kentucky, Florida, Georgia',
     'EPL Teams': 'Arsenal, Chelsea, Everton, Leicester City, Liverpool, Manchester City,'
                  ' Manchester United, Tottenham Hotspur',
     'MLS Teams': 'Atlanta, Chicago, D.C. United, LA Galaxy, LAFC, Minnesota,'
                  ' NYCFC, NY Red Bulls, Seattle',
     'La Liga Teams': 'Atlético Madrid, Barcelona, Real Madrid, Sevilla, Valencia',
     'Bundesliga Teams': 'Bayer Leverkusen, Bayern Munich, Dortmund, RB Leipzig, Werder Bremen',
     'Ligue 1 Teams': 'Lyon, Marseille, Montpellier, Nice, PSG, Saint-Etienne, Stade Rennes',
     'Serie A Teams': 'Fiorentina, Internazionale, Juventus, Lazio, Milan, Napoli, Roma',
     'Champions League Teams': 'Barcelona, Real Madrid, PSG, Juventus, Napoli, Roma, Bayern Munich,'
                               ' Dortmund, RB Leipzig, Liverpool, Manchester City, Manchester United',
     'Europa League Teams': 'Barcelona, Real Madrid, PSG, Juventus, Napoli, Roma, Bayern Munich, ' 
                            'Dortmund, RB Leipzig, Liverpool, Manchester City, Manchester United',
     'NFL Teams': 'ATL Falcons, BAL Ravens, CAR Panthers, CHI Bears, CLE Browns, DAL Cowboys, GB Packers, KC Chiefs,'
                  ' LA Rams, MIN Vikings, NE Patriots, NO Saints, SF 49ers, SEA Seahawks, WSH Football Team'
     }, index=[0]
)
