import streamlit as st
import pandas as pd
import numpy as np

# --- 1. SETUP THE PAGE ---
# This configures the browser tab title and layout
st.set_page_config(page_title="Chicken or Egg", layout="centered")

# --- 2. ADD TEXT/MARKDOWN ---
# Streamlit allows you to write Markdown directly.
st.title("🐣 Egg today or chicken tomorrow?")
st.markdown("""There is an Italian saying: *"Better an egg today than a chicken tomorrow."* 
It sounds conservative, but in finance, having the "egg" (capital) today is actually powerful.

Why? *Because money has potential.*

An amount held today can be invested to generate returns. Waiting for a larger amount in the future comes at a cost: you lose the years of compounding interest. This is the core principle of the **Time Value of Money**.

## 1. The Power of Compounding 💹
Let's test the proverb. If you invest the price of an "egg" today, how long does it take to grow into the price of a "chicken"? 

Depending on the yield (that can come in many forms, like interest rates on bonds), the results can be surprising. The default value, 3.5%, is a reasonable assumption for a conservative investment but more can be gained at higher volatility suitable to long term investing.

Input your parameters on the left (or top on mobile) to see the projection.
""")

# We create columns to organize the inputs neatly side-by-side
col1, col2, col3 = st.columns(3)

with col1:
    # Numeric input for the initial amount
    initial_amount = st.number_input("Initial Amount (egg)", value=0.4, step=0.1)

with col2:
    # Input for inflation rate (default 3.5%)
    investment_rate = st.number_input("Yearly Yield (%)", value=3.5, step=0.1)

with col3:
    # Slider for the number of years
    chicken_amount = st.number_input("Final Amount (Chicken)", value=10.0, step=1.0)

year_range = list(range(101))
invested_values = [initial_amount * ((1 + investment_rate/100)**i) for i in year_range]

breakeven_year = np.log(chicken_amount / initial_amount) / np.log(1 + investment_rate/100)

if breakeven_year > 100:
    st.warning(f"⚠️ Your egg will pay for the chicken only in {breakeven_year:,.1f} years.")
else:
    st.success(f"🎉 Your egg will grow into a chicken in **{breakeven_year:.1f} years**.")
    
    Egg_dataframe = pd.DataFrame({
    "Year": year_range,
    "Investment egg": invested_values,
    "Original chicken": chicken_amount 
    })

    st.subheader("Investment egg over time")
    st.line_chart(Egg_dataframe, x="Year", y=["Investment egg", "Original chicken"], x_label="Year", y_label="Purchasing Power", color=["#32CD32", "#FF4B4B"])

st.markdown(""" ### Takeaway message:
            
Investing allows to grow your money over time, giving exponentially more money thanks to years of compounding interest. It takes longer than growing a chicken from an egg, but then you don't have to deal with a chicken.
            """)

st.divider()

st.markdown("""
## 2. Inflation, the silent thief 💸 
            
While investing makes money grow, on the other hand **inflation** makes it shrink. 

If you keep your capital in cash (under the mattress or in a current account), its numerical value stays the same, but its **Purchasing Power** drops year by year. 

Central banks aim for inflation to be at 2%, but as we know, real life can be much more expensive.
""")

# --- 3. INPUTS (THE FRONTEND WIDGETS) ---
# We create columns to organize the inputs neatly side-by-side
col1, col2, col3 = st.columns(3)

with col1:
    # Numeric input for the initial amount
    initial_amount = st.number_input("Initial Amount (currency)", value=1000, step=100)

with col2:
    # Input for inflation rate (default 2%)
    inflation_rate = st.number_input("Yearly Inflation (%)", value=2.0, step=0.1)

with col3:
    # Slider for the number of years
    years = st.slider("Time Horizon (Years)", min_value=1, max_value=50, value=10)

# --- 4. CALCULATIONS (THE BACKEND) ---
# We use standard Python/NumPy/Pandas logic here.
# Logic: Adjusted Value = Amount / (1 + rate/100)^year

# Create a list of years from 0 to N
year_range = list(range(years + 1))

# Calculate the value for each year
# We use a list comprehension, but you could use numpy arrays too
adjusted_values = [initial_amount / ((1 + inflation_rate/100)**i) for i in year_range]

# Create a Pandas DataFrame (The standard format for data plotting)
df = pd.DataFrame({
    "Year": year_range,
    "Purchasing Power": adjusted_values
})

# --- 5. DISPLAY RESULTS ---
# Display the final calculated value with big text
final_value = adjusted_values[-1]
st.metric(
    label=f"Value in {years} years", 
    value=f"{final_value:,.2f}", 
    delta=f"{final_value - initial_amount:,.2f}",
    delta_color="normal" # Makes the negative change red
)

# --- 6. PLOTTING ---
# Streamlit has a built-in line chart that takes a dataframe
st.subheader("Purchasing Power Over Time")
st.line_chart(df, x="Year", y="Purchasing Power", x_label="Year", y_label="Purchasing Power")

st.markdown(""" ### Takeaway message:
            
Keeping your money tucked away is also risky. Inflation will silently erode the purchasing value of your money over time. One of the few guarantees of the financial world is that cash will buy you less over time. Investments and inflation are in a tug-of-war. To preserve and grow your wealth, your investments must outpace inflation. In the following examples, we'll talk only about the actual purchasing power of money, adjusting for inflation. This is called the *"real value"* or *"purchasing power parity"* of money.
            """)

st.divider()

st.markdown("""## 3. Should you aim for that hard job? 👷‍♂️👩‍⚕️
            
It's nice to get a high salary, but if it comes later, does it really give more money in the bank? Here we have a common choice between two jobs. 

- Job 1 pays little and can start immediately, 
- Job 2 pays lots, but only after some years without income.

Is Job 2 worth the wait?
            
In this example we assume that in job 2 you save double the amount of money per year and that in both jobs you invest your savings each year at a slightly more aggressive rate than the previous example. Feel free to adjust of course.
            """)

col1, col2, col3, col4 = st.columns(4)

with col1:
    job1_savings = st.number_input("Job 1 savings (currency)", value=1000, step=100)

with col2:
    job2_savings = st.number_input("Job 2 savings (currency)", value=2000, step=100)

with col3:
    investment_rate = st.number_input("Yearly Yield (%).", value=6.0, step=0.1)

with col4:
    years_delay = st.number_input("Years delay", value=10, step=1)

year_range = list(range(41))

invested_job1 = [0]
invested_job2 = [0]
for i in year_range[1:]:
    invested_job1.append( (invested_job1[-1]+job1_savings) * (1 + investment_rate/100))
    if i <= years_delay:
        invested_job2.append(0)
    else:
        invested_job2.append((invested_job2[-1] + job2_savings) * (1 + investment_rate/100))

jobs_comparison = pd.DataFrame({
    "Year": year_range,
    "Investment in Job 1": invested_job1,
    "Investment in Job 2": invested_job2
})

st.subheader("Investment value over time")
st.line_chart(jobs_comparison, x="Year", y=["Investment in Job 1", "Investment in Job 2"], x_label="Years of investing", y_label="Investment Value")

st.markdown(""" ### Takeaway message:

In the financial world, time is money. Delaying income has a cost, as it forfeits years of potential investment growth. This is called the **"Opportunity cost"**. Even with a higher salary later, and much more money invested overall, the lost time can result in a lower overall investment value compared to starting earlier. Note that in many real life cases, training is unpaid, or one might even have to pay for the education, so the opportunity cost is much higher than this example.
            """)


st.divider()

st.markdown(""" ## 4. 🔮 A Life Well Spent
            
Financial life has two main phases:
1.  **Accumulation (Work):** You save money and invest it to make it grow.
2.  **Decumulation (Retirement):** You stop working and withdraw from your investments.

Let's simulate your financial journey through these phases. Adjust the parameters to see how your savings grow during your working years and how long they can sustain your lifestyle in retirement.
            """)

col1, col2, col3 = st.columns(3)

with col1:
    job_savings = st.number_input("Work savings (currency)", value=1000, step=100)

with col2:
    investment_rate = st.number_input("Yearly Investment Yield (%).", value=5.0, step=0.1)

with col3:
    retirement_spending = st.number_input("Yearly Spending (currency).", value=5000, step=100)

col1, col2 = st.columns(2)
with col1:
    years_work = st.slider("Work life (Years)", min_value=10, max_value=50, value=40)

with col2:
    years_retirement = st.slider("Retirement (Years)", min_value=0, max_value=70, value=20)

years = years_work+years_retirement

st.markdown(""" **👇 Interactive Scenario:**  
Real life isn't linear. What if the market crashes right when you retire? What if you get a promotion or win the lottery?  
**Edit the table below** to change the Yield or Cashflow for specific years and see how the curve reacts.
""")

default_data = pd.DataFrame({
    "Year": range(1, years + 1),
    "Investment Rate (%)": [investment_rate] * years, # [3.0, 3.0, 3.0, 3.0, 3.0]
    "Contribution": [job_savings] * years_work + [-retirement_spending] * years_retirement
})

# if st.checkbox("Edit yearly contributions"):
default_data = st.data_editor(
    default_data,
    # Optional: Lock the 'Year' column so users can't change it
    disabled=["Year"],
    # Optional: Formatting numbers
    column_config={
        "Investment Rate (%)": st.column_config.NumberColumn(
            "Investment Rate (%)",
            format="%.1f%%"
        ),
        "Contribution ($)": st.column_config.NumberColumn(
            "Contribution",
            format="$%d"
        )
    },
    hide_index=True, # Hide the 0,1,2,3... index column
    num_rows="fixed" # Prevents user from adding/deleting rows (optional)
)

invested = [0]
for i in range(1, years):
    invested.append( (invested[-1]+default_data["Contribution"][i-1]) * (1 + default_data["Investment Rate (%)"][i-1]/100))

if min(invested) < 0:
    st.error("⚠️ Warning: You run out of invested money during retirement!")
    # find the first year where invested < 0
    for i in range(len(invested)):
        if invested[i] < 0:
            years = i+1
            break

else:
    st.success("🎉 Success: Your investments last through retirement!")
    
# add column to dataframe
default_data["Investment Value"] = invested

st.line_chart(default_data[:years], x="Year", y="Investment Value", x_label="Years of investing", y_label="Investment Value Over Life")
# limit data_frame to years

st.markdown(""" ### 📝 Final Thoughts

*   **Time is Money:** Starting early or delaying withdrawal often matters more than earning more.
*   **Planning is Key:** Retirement requires a balance of saving discipline and realistic spending.
*   **No Moonshots Needed:** You don't need risky bets to retire comfortably; you need consistency and time.

**Disclaimer:** these models are simplified and do not account for taxes, fees, or changing market conditions. Future performance might be radically different from the past and hence the numbers we are using might not be representative. I have used for the examples typical numbers considered in inflation-adjusted scenarios (otherwise also salary should grow with inflation). But it is easy to play with the numbers to simulate inflation and variability in returns, the effect of promotions, and a draw a lot of interesting conclusions. See what happens if you have a market crash at the beginning or at the end of your investing life.
""")
st.info("If you want to learn more, and you liked this app, contact me and ask to make more! :)")

st.divider()

# --- 6. RAW DATA ---
if st.checkbox("Show raw calculation data"):
    if 'Egg_dataframe' in locals():
        st.markdown("### Egg to Chicken Data")
        st.dataframe(Egg_dataframe)
    
    st.markdown("### Inflation Data")
    st.dataframe(df)
    
    st.markdown("### Job Comparison Data")
    st.dataframe(jobs_comparison)
    
    st.markdown("### Life Cycle Data")
    st.dataframe(default_data)
