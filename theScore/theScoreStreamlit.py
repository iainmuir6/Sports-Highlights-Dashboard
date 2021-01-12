"""
Iain Muir, iam9ez@virginia.edu

Scrapes personalized sports highlights data from theScore.com and deploys a Streamlit dashboard

STRUCTURE:
    Loop of inputs (no loop for personal use)
        Loop of leagues
            Loop of games
"""

# Modules for scraping
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
# import time

# Other
from constants import LEAGUE_ID
from secrets import SWID, ESPN_S2
import streamlit as st
import pandas as pd
import numpy as np
import sys


def print_exception():
    """
    exc_type --> error class (ex. <class 'ZeroDivisionError'>)
    exc_obj --> error description (ex. division by zero)
    tb --> error traceback (ex. <traceback object at 0x1031e7b08>)
        tb.tb_lineno --> line number of the error
    """
    exc_type, exc_obj, tb = sys.exc_info()
    print(str(exc_obj).capitalize(), "on line", tb.tb_lineno)
    print("     |->  " + str(exc_type))
    print("     |->  " + str(tb))


def get_nfl_week():
    """
    Scrapes the duration of the current NFL regular season from Wikipedia in order to calculate the current week

    :return Current week in the NFL
    """

    # TODO Adjust for playoffs

    # url = "https://en.wikipedia.org/wiki/" + str(date.year) + "_NFL_season"
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, "html.parser")
    # duration = soup.find("table", class_='infobox vevent').tbody.find("td").text
    # start = duration[duration.find("(") + 1: duration.find(")")]
    # return 1 + ((date - datetime.strptime(start, "%Y-%m-%d")).days // 7)

    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(date.year) + "/segments/0/leagues/" + \
          str(LEAGUE_ID)
    response1 = requests.get(url,
                             cookies={
                                 "SWID": SWID,
                                 "espn_s2": ESPN_S2
                             }).json()

    print(response1['scoringPeriodId'])


@st.cache(suppress_st_warning=True)
def loop_data(rows, today_date):
    """
    :argument rows – DataFrame of favorite sports teams/leagues
    :argument today_date

    Initial Loop: loop through each person in inputs (only one call for personal use)

    • Creates list of leagues and teams given the input data

    :return no return value
    """

    global highlights

    if rows[0] != '7/21/2020 11:08:49' and rows[1] != "iam9ez@virginia.edu":
        return None, None

    st.markdown("<center><img src='https://i.postimg.cc/WbYzfHvd/morningscoop.jpg' alt='Image' width='200'></center>",
                unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Morning Scoop</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'> Highlights from: " + str(today_date.date()) + "</h1>",
                unsafe_allow_html=True)

    leagues = np.array(rows[2].split(","))
    indices_arr = np.array(list(map(lambda x: indices[x.strip()], leagues)))
    teams = np.array(list(map(lambda x: rows[x].split(","), indices_arr)))

    highlights = {}

    df = pd.DataFrame(columns=['league', 'tm1', 'score1', 'score2', 'tm2', 'gameLink', 'logo1', 'logo2'])
    league_data = list(map(lambda x, y: loop_leagues(x.strip(), y), leagues, teams))

    for l in league_data:
        if isinstance(l, list):
            temp = pd.DataFrame(l,
                                columns=['league', 'tm1', 'score1', 'score2', 'tm2', 'gameLink', 'logo1', 'logo2'])
        else:
            temp = pd.DataFrame([[l, None, None, None, None, None, None, None]],
                                columns=['league', 'tm1', 'score1', 'score2', 'tm2', 'gameLink', 'logo1', 'logo2'])

        df = df.append(temp)

    return df, highlights


def loop_leagues(league, teams_list):
    """
    :argument league – specific sports league (full name, ex. "Champions League)
    :argument teams_list – list of favorite teams within the league

    Secondary Loop: loop through each of their favorite sports leagues

    • Scrapes all games on the given date for the specific league
    • Checks if any favorite teams played on this date

    :return None – breaks "loop" if no favorite teams played (condition == False)
    """
    global highlights

    sport_shortened = codes[league]
    url = "https://www.thescore.com/" + sport_shortened + "/events/" + \
          ("conference/All%20Conferences/date/" + str(date.date()) if sport_shortened == 'ncaab' else
           "date/" + str(date.date())[:4] + "-" + str(get_nfl_week()) if sport_shortened == 'nfl' else
           "date/" + str(date.date()))

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    all_games = soup.find_all("div", class_="col-xs-12 col-md-6")
    teams_list = np.array(list(map(lambda x: x.strip(), teams_list)))

    if sport_shortened == 'ncaab':
        all_teams = [team.text for team in soup.find_all('div', class_='EventCard__teamName--JweK5')]
        lst = [ele in teams_list for ele in all_teams]
        condition = bool(any(lst))
    else:
        lst = [ele in str(soup) for ele in teams_list]
        condition = bool(any(lst))

    if not condition:
        highlights[league] = False
        return league

    games = list(map(lambda x: loop_games(x, teams_list, league), all_games))
    highlights[league] = True
    return games


def loop_games(game_html, team_list, league):
    """
    :argument game_html – HTML / soup of individual games played that day
    :argument team_list – list of favorite teams within the league
    :argument league –

    Third/Final Loop: loop through each game played on that date

    • Scrape the following data for each game and deploy to dashboard in Markdown format
        teams (tm1, tm2)
        scores (scores[0].text, scores[1].text)
        logos (logo1, logo2)

    :return None – breaks "loop" after markdown statements to avoid repeat
    """

    teams = game_html.find_all("div", class_="EventCard__teamColumn--17asJ")
    tm1, tm2 = teams[0].text, teams[1].text

    if tm1 in team_list or tm2 in team_list:
        scores = game_html.find_all("div", class_="EventCard__scoreColumn--2JZbq")
        team_logos = game_html.find_all("div", class_="EventCard__teamLogo--3D7cf")
        logo1, logo2 = team_logos[0].span.img["src"], team_logos[1].span.img["src"]
        score1, score2 = scores[0].text, scores[1].text
        link = "https://www.thescore.com" + game_html.span.span.a["href"]

        if tm1 == "Juventus":
            logo1 = "https://upload.wikimedia.org/wikipedia/en/8/84/Juventus_IF_logo.svg"
        elif tm2 == "Juventus":
            logo2 = "https://upload.wikimedia.org/wikipedia/en/8/84/Juventus_IF_logo.svg"
        if tm1 == "WSH Football Team":
            tm1 = "WSH Football"
        elif tm2 == "WSH Football Team":
            tm2 = "WSH Football"

        game_data = [league, tm1, score1, score2, tm2, link, logo1, logo2]
        return game_data

    else:
        return [None, None, None, None, None, None, None, None]


def display(data, highlights):
    """
    :argument data
    :argument highlights
    """

    no_highlights = "<center> "
    for sport, any_ in highlights.items():
        if not any_:
            no_highlights += '<img src="' + logos[codes[sport]] + '" width="40"/>                               '
        else:
            st.markdown("<h3 style='text-align: center;'> " + sport + "</h1>",
                        unsafe_allow_html=True)
            counter = 0
            col1, col2 = st.beta_columns(2)

            for g in data.query('league == "' + sport + '"').values:
                counter += 1
                col = col1 if counter % 2 != 0 else col2
                tm1, score1, score2, tm2, link, logo1, logo2 = g

                font_size = '14'
                if "T:" in score1 or "-" in score2:
                    score1, score2 = "", ""
                if len(tm1 + tm2 + score1 + score2) > 30:
                    font_size = '13'

                col.markdown("<p style='font-size:" + font_size + "px;text-align:center;'> <img src='" + logo1 +
                             "' height='40' /> <b>" + tm1 + "</b> " + score1 + " <a href='" + link + "'> -</a> "
                             + score2 + " <b>" + tm2 + "</b> <img src='" + logo2 + "' height='40' /> </p>",
                             unsafe_allow_html=True)

    st.subheader("No highlights:")
    st.markdown(no_highlights + "</center>", unsafe_allow_html=True)


indices = {"NBA": 3,
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
logos = {"nba": "https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg",
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
         "uefa": "https://upload.wikimedia.org/wikipedia/en/0/03/Europa_League.svg"}
codes = {"NBA": "nba",
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
         "Europa League": "uefa",
         }
response = pd.DataFrame(
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

date = datetime.today() - timedelta(days=1)
print(get_nfl_week())
exit(0)
d, h = loop_data(response.values[0], date)

if d is not None:
    display(d.dropna().set_index('league'), h)
else:
    print('Data passed incorrectly')
    exit(code=0)
