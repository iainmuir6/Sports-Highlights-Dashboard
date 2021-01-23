"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

streamlit run /Users/iainmuir/PycharmProjects/Desktop/sportsHighlights/fantasy_app.py
"""

import streamlit as st

try:
    from sportsHighlights import sports_home, highlights, schedule, analytics
except ModuleNotFoundError:
    import sports_home
    import highlights
    import schedule
    import analytics


def launch():
    pages = {
        "Home": sports_home,
        "Highlights": highlights,
        "Schedule": schedule,
        "Analytics": analytics,
    }

    st.sidebar.title("Sports Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page.run()


if __name__ == '__main__':
    launch()
