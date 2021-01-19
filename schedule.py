# Iain Muir
# iam9ez

from datetime import datetime
from bs4 import BeautifulSoup
from constants import CODES
import streamlit as st
import pandas as pd
import requests
import os


def get_nfl_week():
    """
    Scrapes the duration of the current NFL regular season from Wikipedia in order to calculate the current week

    :return Current week in the NFL
    """

    url = "https://en.wikipedia.org/wiki/" + str(year) + "_NFL_season"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    duration = soup.find("table", class_='infobox vevent').tbody.find("td").text
    start = datetime.strptime(duration[duration.find("(") + 1: duration.find(")")], "%Y-%m-%d")
    end = datetime.strptime(duration[duration.rfind("(") + 1: duration.rfind(")")], "%Y-%m-%d")

    return 1 + ((date - start).days // 7) if date < end else 17 + ((date - end).days // 7)


def loop_games(game, l):
    """

    """
    teams = game.find_all("div", class_="EventCard__teamColumn--17asJ")
    tm1, tm2 = teams[0].text, teams[1].text

    lines = game.find_all("div", class_="EventCard__scoreColumn--2JZbq")
    team_logos = game.find_all("div", class_="EventCard__teamLogo--3D7cf")
    logo1, logo2 = team_logos[0].span.img["src"], team_logos[1].span.img["src"]

    return [
        l,
        "WSH Football" if tm1 == "WSH Football Team" else tm1,
        lines[0].text,
        lines[1].text,
        "WSH Football" if tm2 == "WSH Football Team" else tm2,
        game.find('div', class_='EventCard__clockColumn--3lEPz').text,
        "https://www.thescore.com" + game.span.span.a["href"],
        "https://upload.wikimedia.org/wikipedia/en/8/84/Juventus_IF_logo.svg" if tm1 == "Juventus" else logo1,
        "https://upload.wikimedia.org/wikipedia/en/8/84/Juventus_IF_logo.svg" if tm2 == "Juventus" else logo2
    ]


def get_schedule():
    """

    """

    data = []

    for league_ in list(CODES.values()):
        url = "https://www.thescore.com/" + league_ + "/events/" + \
              ("conference/Top%2025/date/" + str(date.date()) if league_ == 'ncaab' else
               "date/" + str(year) + "-" + str(get_nfl_week() + 1) if league_ == 'nfl' else
               "date/" + str(date.date()))
        page = requests.get(url=url)
        soup = BeautifulSoup(page.content, 'html.parser')
        all_games = soup.find_all("div", class_="col-xs-12 col-md-6")
        schedule = list(map(lambda g: loop_games(g, league_), all_games))
        data += schedule

    df = pd.DataFrame(data, columns=[
        'league', 'team1', 'line1', 'line2', 'team2', 'time', 'link', 'logo1', 'logo2'
    ])

    df.to_csv('schedule_' + str(date.date()) + '.csv')


def reformat(s):
    index = 0
    for i, let in enumerate(s):
        if let.istitle():
            index = i
            break
    return s[index:]


def get_teams():
    """

    """

    data = []

    for league_ in list(CODES.values()):
        url = 'https://www.thescore.com/' + league_ + '/standings' + \
              ('/american-league' if league_ == 'mlb' else '/afc' if league_ == 'nfl' else
               '/AP%20Top%2025' if league_ == 'ncaab' else '')
        page = requests.get(url=url)
        soup = BeautifulSoup(page.content, 'html.parser')
        print(league_)
        table = soup.find_all('div', class_='standings')[0]
        all_teams = [[league_, reformat(a.div.div.text), a['href'][a['href'].rfind('/') + 1:],
                      'https://www.thescore.com' + a['href']] for a in table.find_all('a')]
        data += all_teams

        if league_ == 'mlb' or league_ == 'nfl':
            url = 'https://www.thescore.com/' + league_ + '/standings' + (
                '/national-league' if league_ == 'mlb' else '/nfc' if league_ == 'nfl' else '')
            page = requests.get(url=url)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find_all('div', class_='standings')[0]
            all_teams = [[league_, reformat(a.div.div.text), a['href'][a['href'].rfind('/') + 1:],
                          'https://www.thescore.com' + a['href']] for a in table.find_all('a')]
            data += all_teams

    df = pd.DataFrame(data, columns=['league', 'team', 'id', 'link'])
    df.to_csv('teams.csv')


def display(games):
    """
    :argument

    # TODO Alternating Background Color
    """

    col1, col2 = st.beta_columns(2)
    for i, g in enumerate(games.values):
        col = col1 if i % 2 == 0 else col2

        col.markdown("<p style='font-size:16px;text-align:left;'> <img src='" + g[8] + "' height='60' />" +
                     "<b>" + g[2] + "</b> " + str(g[3]) + " <span style='float:right;'><a href='" + g[7] + "'>" + g[6] +
                     "</a></span></p>", unsafe_allow_html=True)
        col.markdown("<p style='font-size:16px;text-align:left;'> <img src='" + g[9] +
                     "' height='60' /> <b>" + g[5] + "</b> " + str(g[4]) + "</p>",
                     unsafe_allow_html=True)
        col.write('------------------------------')


def run():
    """


    """
    global date, year

    date = datetime.today()
    year = date.year if date.month > 3 else date.year - 1

    st.markdown("<center><img src='https://i.postimg.cc/WbYzfHvd/morningscoop.jpg' alt='Image' width='200'></center>",
                unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Today's Schedule</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'> Date: " +
                date.date().strftime('%B %d, %Y') + "</h3>", unsafe_allow_html=True)

    league = st.selectbox('Choose the League', ['--- Select a League ---'] + list(CODES.keys()),
                          index=0)

    if not os.path.exists('schedule_' + str(date.date()) + '.csv'):
        st.warning("Gathering Data for Today's Games...")
        get_schedule()
    schedule_df = pd.read_csv('schedule_' + str(date.date()) + '.csv')
    if not os.path.exists('teams.csv'):
        st.warning("Gathering Data for Today's Games...")
        get_teams()
        exit(0)
    teams_df = pd.read_csv('teams.csv')

    if league != '--- Select a League ---':
        st.markdown("<h3 style='text-align: center;'>Schedule for the " + league + "</h3>", unsafe_allow_html=True)
        st.write('------------------------------')

        games = schedule_df.query('league == "' + CODES[league] + '"')
        display(games)

        team = st.selectbox('Choose a Team', ['--- Select a Team ---'] +
                            list(teams_df.query('league == "' + CODES[league] + '"')['team']),
                            index=0)

        if team != '--- Select a Team ---':
            st.write(team)


if __name__ == '__main__':
    date = datetime.today()
    year = date.year if date.month > 3 else date.year - 1

    run()
