import streamlit as st

# --- 1. SETUP PAGE CONFIG ---
st.set_page_config(page_title="The Financial Sandbox", layout="centered")

st.write("Hello World")


# --- 2. DEFINE PAGES ---
# We wrap the python files in st.Page objects
# 'url_path' allows you to set the deep link (e.g. /fees instead of /fees_logic)

intro_page = st.Page("tools/intro_page.py", title="Homepage", icon="🏠", default=True)

# # Section: Basics
# egg_page = st.Page("tools/01_Egg_or_Chicken.py", title="Egg vs Chicken", icon="🐣", url_path="tvm")
# fee_page = st.Page("tools/02_Fees_keep_you_poor.py", title="Fees keep you poor", icon="💸", url_path="fees")

# Section: Advanced
# mc_page  = st.Page("tools/monte_carlo.py", title="Monte Carlo Sim", icon="🎲", url_path="monte-carlo")

# --- 3. CREATE NAVIGATION (SUBSECTIONS) ---
# This dictionary structure creates the "Grouping" in the sidebar
pg = st.navigation({
    "Welcome": [intro_page]#,
    # "The Basics": [egg_page, fee_page] #,
    # "Advanced Modeling": [fee_page, mc_page]
})

# --- 4. SHARED SIDEBAR ELEMENTS ---
# Anything you write here will appear on EVERY page
st.sidebar.text("Made by Andrea Idini")
# st.logo("assets/logo.png") # Adds a nice image at the top left

# Optional: Add a "Subscribe" link for your Substack
st.sidebar.link_button("Subscribe to Substack", "https://idini.substack.com")

# --- 5. RUN THE SELECTED PAGE ---
pg.run()
