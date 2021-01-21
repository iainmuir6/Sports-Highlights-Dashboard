"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

streamlit run /Users/iainmuir/PycharmProjects/Desktop/sportsHighlights/app.py
"""

import streamlit as st

import home
import highlights
import schedule
import analytics

# st.set_page_config(layout="wide")

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
