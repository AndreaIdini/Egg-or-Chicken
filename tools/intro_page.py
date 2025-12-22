import streamlit as st

# uncomment if standalone
# st.set_page_config(page_title="The Financial Sandbox", layout="centered")

st.title("📊 The Financial Sandbox")

st.markdown("""
Welcome! This is the interactive companion to my [**Substack Blog**](https://idini.substack.com).

Here you will find interactive simulations and brief explanations of key financial concepts. 
You can go to [the blog](https://idini.substack.com) for more details and context.

Select a lecture from the sidebar 👈 to get started.

### Latest Tools:
""")
st.page_link("tools/01_Egg_or_Chicken.py", label="Egg or Chicken: Visualize the Time Value of Money", icon="📊")
st.page_link("tools/02_Fees_keep_you_poor.py", label="Fees keep you poor: See how 1% can destroy your retirement.", icon="💸")
st.page_link("tools/03_Risk_and_Reward.py", label="Risk and Reward: Learn to be courageous with your investments", icon="⚖️")

st.info("""If you want to learn more, and you liked this app contact me, follow me on my substack, and ask to make more! :)

Write me at andrea.idini (at) gmail.com if you want to thank me for this project or if you have an idea!""")