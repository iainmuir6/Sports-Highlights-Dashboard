"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

streamlit run /Users/iainmuir/PycharmProjects/Desktop/sportsHighlights/app.py
"""

import streamlit as st

from sportsHighlights import home, highlights, schedule, analytics


def launch():
    PAGES = {
        "Home": home,
        "Highlights": highlights,
        "Schedule": schedule,
        "Analytics": analytics,
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.run()
