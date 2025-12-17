import streamlit as st

st.markdown("""
Coming soon... Write me at andrea.idini (at) gmail.com if you want to thank me for this project or if you have an idea!
""")

# # 1. INITIALIZE STATE
# # We need to create the variables in memory if they don't exist yet.
# if "stocks" not in st.session_state:
#     st.session_state.stocks = 60
# if "bonds" not in st.session_state:
#     st.session_state.bonds = 40

# # 2. DEFINE CALLBACK FUNCTIONS
# # These run immediately when a slider is moved, BEFORE the page reloads.

# def update_bonds():
#     # If Stocks changed, Bonds must become the remainder
#     st.session_state.bonds = 100 - st.session_state.stocks

# def update_stocks():
#     # If Bonds changed, Stocks must become the remainder
#     st.session_state.stocks = 100 - st.session_state.bonds

# # 3. CREATE THE SLIDERS
# col1, col2 = st.columns(2)

# with col1:
#     # Notice we don't use 'value='. We use 'key='.
#     # Streamlit automatically binds the slider to st.session_state['stocks']
#     st.slider(
#         "Stocks allocation (%)", 
#         min_value=0, 
#         max_value=100, 
#         key="stocks",          # Links to st.session_state.stocks
#         on_change=update_bonds # Trigger this function when user moves this slider
#     )

# with col2:
#     st.slider(
#         "Bonds allocation (%)", 
#         min_value=0, 
#         max_value=100, 
#         key="bonds",           # Links to st.session_state.bonds
#         on_change=update_stocks # Trigger this function when user moves this slider
#     )

# # 4. VERIFICATION
# st.write(f"**Total:** {st.session_state.stocks + st.session_state.bonds}%")
