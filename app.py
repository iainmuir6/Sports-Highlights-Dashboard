"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

streamlit run /Users/iainmuir/PycharmProjects/Desktop/sportsHighlights/app.py
"""

import streamlit as st

try:
    from sportsHighlights import home, highlights, schedule, analytics
except ModuleNotFoundError:
    import home
    import highlights
    import schedule
    import analytics


def launch():
    pages = {
        "Home": home,
        "Highlights": highlights,
        "Schedule": schedule,
        "Analytics": analytics,
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page.run()


if __name__ == '__main__':
    launch()
