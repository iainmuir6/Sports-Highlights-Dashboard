"""
Iain Muir, iam9ez@virginia.edu

Scrapes personalized sports highlights data from theScore.com and deploys a Streamlit dashboard

STRUCTURE:
    Loop of inputs (no loop for personal use)
        Loop of leagues
            Loop of games

TODO
    • Generate Data Source Once
    • Unfiltered Highlights
    •

"""

# Modules for scraping
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
# import time

# Other
from constants import INDICES, LOGOS, CODES, RESPONSE
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

    TODO Adjust for playoffs

    :return Current week in the NFL
    """

    url = "https://en.wikipedia.org/wiki/" + str(year) + "_NFL_season"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    duration = soup.find("table", class_='infobox vevent').tbody.find("td").text
    start = datetime.strptime(duration[duration.find("(") + 1: duration.find(")")], "%Y-%m-%d")
    end = datetime.strptime(duration[duration.rfind("(") + 1: duration.rfind(")")], "%Y-%m-%d")

    return 1 + ((date - start).days // 7) if date < end else 17 + ((date - end).days // 7)


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

    print(today_date)
    if rows[0] != '7/21/2020 11:08:49' and rows[1] != "iam9ez@virginia.edu":
        return None, None

    leagues = np.array(rows[2].split(","))
    indices_arr = np.array(list(map(lambda x: INDICES[x.strip()], leagues)))
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

    sport_shortened = CODES[league]
    url = "https://www.thescore.com/" + sport_shortened + "/events/" + \
          ("conference/All%20Conferences/date/" + str(date.date()) if sport_shortened == 'ncaab' else
           "date/" + str(year) + "-" + str(get_nfl_week()) if sport_shortened == 'nfl' else
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
            no_highlights += '<img src="' + LOGOS[CODES[sport]] + '" width="40"/>                               '
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


def run():
    """

    TODO Better Method for Determining Year
    """
    global date, year

    date = datetime.today() - timedelta(days=1)
    year = date.year if date.month > 3 else date.year - 1

    st.markdown("<center><img src='https://i.postimg.cc/WbYzfHvd/morningscoop.jpg' alt='Image' width='200'></center>",
                unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Morning Scoop</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'> Highlights from: " +
                date.date().strftime('%B %d, %Y') + "</h1>", unsafe_allow_html=True)

    col1, col2 = st.beta_columns(2)
    custom = col1.checkbox('Enter Custom Date')
    if custom:
        input_ = col2.date_input("Enter Date:",
                                 min_value=datetime.today() - timedelta(days=365),
                                 max_value=datetime.today() - timedelta(days=1))
        date = datetime.combine(input_, datetime.min.time())

    d, h = loop_data(RESPONSE.values[0], date)

    if d is not None:
        display(d.dropna().set_index('league'), h)
    else:
        print('Data passed incorrectly')
        exit(code=0)


if __name__ == '__main__':
    run()
