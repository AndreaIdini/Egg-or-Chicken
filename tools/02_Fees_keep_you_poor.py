import streamlit as st
import pandas as pd

from utils import calculate_compound_interest

# uncomment if standalone
# st.set_page_config(page_title="Fees keep you poor", layout="centered")

st.title("Fees keep you poor")
st.subheader("...and the banker rich 💸")

st.markdown("""Imagine a business partner who puts up $0 capital, takes 0% of the risk, but demands a massive cut of the business every single year. This is the reality of investment fees. 

> If you want to read more about this, check out my [Substack article on the Ferrari in your Banker's driveway](https://idini.substack.com/publish/post/181027330).
          
## 1. The drag: yearly fees.

This is the most insidious fee because it acts like reverse compounding. It doesn't just reduce your return; it shrinks the capital base that generates future returns.

Once again, the counterintuitive nature of exponentials makes it hard to realise what is really going on. Even if fees are at a relative small percentage of your returns, their compound effect can become huge with time. At an average return of 7% per year, a not unusual 2% fee means that in 30 years you will have given away half of your investment gains, and in 75 years the bank will have earned more than 3 times as you! 
            
With the simulation below you can adjust parameters to see what a huge difference it makes to go with a 0.2% fee index fund instead of a 2% mutual fund.
""")

# We create columns to organize the inputs neatly side-by-side
col1, col2, col3 = st.columns(3)

with col1:
    # Numeric input for the initial amount
    initial_amount = st.number_input("Initial investment (currency)", value=1000.0, step=100.0)

with col2:
    # Slider for the number of years
    years = st.slider("Time Horizon (Years)", min_value=1, max_value=75, value=30)

with col3:
    # Input for inflation rate (default 2%)
    investment_rate = st.number_input("Investment Return (%)", value=7.0, step=0.1)

col4, = st.columns(1)
with col4:
    # Input for fees rate (default 1%)
    fees_rate = st.number_input("Fees (%)", value=2.0, step=0.1)

year_range = list(range(years+1))
invested_values = calculate_compound_interest(initial_amount, investment_rate, year_range)
invested_fees_values = calculate_compound_interest(initial_amount, investment_rate - fees_rate, year_range)

Fees_dataframe = pd.DataFrame({
    "Year": year_range,
    "Investment": invested_values,
    "Investment with fees": invested_fees_values 
    })

st.subheader("Investment value over time")

st.success(f"🎉 You earned {(invested_fees_values[-1]-initial_amount):.1f} in {years} years.")
st.warning(f"😞 Your bank earned {invested_values[-1]-invested_fees_values[-1]:,.1f} thanks to you.")

st.line_chart(Fees_dataframe, x="Year", y=["Investment", "Investment with fees"], x_label="Year", y_label="Investment value", color=["#32CD32", "#FF4B4B"])

st.markdown(""" ### Takeaway message:

High fees are the most effective way to destroy wealth. This is especially deadly for low-yield investments (like bonds), where fees can eat the entire return. Always prefer low-cost index funds.
""")

st.divider()

st.markdown("""
## 2. The cut: Transaction costs

"Courtage," "Spreads," "Conversion Fees"—bankers have infinite names for the same thing: taking a slice every time money moves.
These fees punish activity. If you buy and sell frequently, you pay the toll booth both ways. Even small costs compound negatively because that money is gone forever and can no longer grow.

While they may seem small they can add up over time, especially if you trade frequently. Below you can set your expected trading frequency and the associated costs.
            
The example uses the investment parameters from before.
""")

# We create columns to organize the inputs neatly side-by-side

col4, col5 = st.columns(2)

with col4:
    # Input for fees rate (default 1%)
    trans_fees_rate = st.number_input("Fees (%)", value=0.25, step=0.05)

with col5:
    # Input for inflation rate (default 2%)
    trans_fees_currency = st.number_input("Fees (currency)", value=10.0, step=0.1)

year_range = list(range(years+1))
invested_transfees_values = calculate_compound_interest(initial_amount*(1-trans_fees_rate/100)-trans_fees_currency, investment_rate, year_range)

fees_charged = initial_amount*trans_fees_rate/100+trans_fees_currency

st.info(f"You invested {initial_amount:,.1f} and in {years} years you earned {invested_transfees_values[-1]:,.1f}. Your bank charged you {fees_charged:,.1f} at the beginning and you lost {invested_values[-1] - invested_transfees_values[-1]:,.1f} of compound interest.")

daily_trader = calculate_compound_interest(initial_amount-2*fees_charged, investment_rate/252, 1)

if daily_trader < initial_amount:
    st.warning(f"⚠️ If you were to trade this amount daily with these fees, your capital would vanish mathematically. You would go bankrupt simply from friction costs.")

st.markdown("""### Takeaway message:
            
Transaction, currency conversion and all these other fees can be just a few euros/dollars/pounds, but over time the loss of not having invested those few bucks will be much larger. You did not just spend 10$, you killed the 100$ they would have become. The *time value* of a few bucks is significant! Be extra careful if you trade frequently.""")

st.divider()

st.markdown("""
## 3. The house: Performance fees

Heads I win, tails you lose. Performance fees are charged only when the investment does well, typically as a percentage of the profits above a certain benchmark. While this may seem fair, it is an additional drawdown on your returns. This is used mostly by hedge funds and some mutual funds. A common structure is "2 and 20", meaning a 2% management fee plus 20% of the profits above some benchmark.
            
Also in this case, the example uses the investment parameters from before.
""")


col1, col2, col3 = st.columns(3)

with col1:
    # Input for fees rate (default 1%)
    hedge_fees_rate = st.number_input("Yearly fees (%)", value=2.0, step=0.1)

with col2:
    # Input for inflation rate (default 2%)
    performance_fees_rate = st.number_input("Performance Fees (%)", value=20.0, step=0.1)

with col3:
    # Input for inflation rate (default 2%)
    benchmark = st.number_input("Benchmark return (%)", value=4.0, step=0.1)

# investment_rate = investment_rate + 0.5  # from before

if investment_rate - hedge_fees_rate < benchmark:
    hedge_fund_rate = investment_rate - hedge_fees_rate
else:
    hedge_fund_rate = investment_rate - hedge_fees_rate - performance_fees_rate * (investment_rate - hedge_fees_rate - benchmark)/100

invested_hedge = calculate_compound_interest(initial_amount, hedge_fund_rate, year_range)

hedge_dataframe = pd.DataFrame({
    "Year": year_range,
    "Investment": invested_values,
    "Investment with fees": invested_fees_values,
    "Investment with hedge fund fees": invested_hedge
    })

st.subheader("Investment value over time")

st.success(f"🎉 Your earned {(invested_fees_values[-1]-initial_amount):.1f} in {years} years.")
st.warning(f"😞 Your hedge fund earned {invested_values[-1]-invested_hedge[-1]:,.1f} thanks to you.")

st.line_chart(hedge_dataframe, x="Year", y=["Investment", "Investment with fees", "Investment with hedge fund fees"], x_label="Year", y_label="Investment value", color=["#32CD32", "#FF4B4B", "#FFA500"])

st.markdown("""### Final thoughts
In the real world, performance fees are even worse, because the markets and hedge funds in particular tend to have really good years where the fees will be enormous. In order to understand this variation, we need to go into *variance* and *risk*, in the next tab.
""")

st.markdown("""## 4. The cost of doing business
            
If we consider all of the above fees together, it is easy to see how much of your investment returns are eaten up by fees. Let's see a typical case of a worker that saves yearly towards retirement. When considering fees, what is the difference from the ideal cost of the [**Egg or Chicken**](/tvm) example?
            
All the values you can set below are in *Real* terms, i.e. inflation adjusted. You can set other parameters in the settings.
""")


col1, col2, col3 = st.columns(3)

with col1:
    job_savings = st.number_input("Work savings (real value)", value=1000, step=100)

with col2:
    investment_rate = st.number_input("Investment Yield (%).", value=5.0, step=0.1)

with col3:
    retirement_spending = st.number_input("Retirement spending (real value).", value=5000, step=100)

col4, col5 = st.columns(2)
with col4:
    yearly_fees = st.number_input("Yearly Fees (%)", value=1.0, step=0.1)
with col5:
    transaction_fees = st.number_input("Transaction Fees (%)", value=0.25, step=0.05)

with st.expander("⚙️ Settings"):
    opt_col1, opt_col2 = st.columns(2)
    with opt_col1:
        years_work = st.slider("Work life (Years)", min_value=10, max_value=50, value=40)

    with opt_col2:
        years_retirement = st.slider("Retirement (Years)", min_value=0, max_value=70, value=30)

    opt_col3, opt_col4 = st.columns(2)
    with opt_col3:
        wealth_tax = st.number_input("Wealth Tax (%)", value=0.0, step=0.1)
    with opt_col4:
        wealth_tax_threshold = st.number_input("Wealth Tax Threshold (real value)", value=1000000.0, step=100000.0)

    opt_col5, opt_col6 = st.columns(2)
    with opt_col5:
        performance_fees = st.number_input("Perf. Fees (%)", value=0.0, step=1.0)
    with opt_col6:
        # Input for inflation rate (default 2%)
        benchmark = st.number_input("Benchmark (%)", value=4.0, step=0.1)


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

invested_with_fees = [0]
wealth_taxable = (1 if invested_with_fees[-1] > wealth_tax_threshold else 0)

for i in range(1, years):
    contribution = default_data["Contribution"][i-1]
    contribution = contribution *(1-transaction_fees/100 * (1 if contribution > 0 else -1) ) # apply transaction fees with the correct sign when withdrawing
    invested_with_fees.append( (invested_with_fees[-1] + contribution ) * (1 + default_data["Investment Rate (%)"][i-1]/100 - yearly_fees/100 - performance_fees/100 * max(0, default_data["Investment Rate (%)"][i-1]-benchmark)/100 - wealth_tax/100 * wealth_taxable) )


if min(invested_with_fees) < 0:
    st.error("⚠️ Warning: You run out of invested money during retirement!")
    # find the first year where invested < 0
    for i in range(len(invested)):
        if invested[i] < 0:
            years = i+1
            break
else:
    st.success("🎉 Success: Your investments last through retirement!")

st.metric(
    label=f"Wealth at the end of retirement, and how much has been lost to fees", 
    value=f"{invested_with_fees[-1]:,.1f}", 
    delta=f"{invested_with_fees[-1] - invested[-1]:,.2f}",
    delta_color="normal" # Makes the negative change red
)

default_data["Investment with Fees"] = invested_with_fees
default_data["Investment without Fees"] = invested


st.line_chart(default_data[:years], x="Year", y=["Investment without Fees","Investment with Fees"], x_label="Years of investing", y_label="Investment Value Over Life", color=["#FF4B4B", "#32CD32"])

st.markdown("""### 📝  Final thoughts
Yearly fees are the silent killer of your investments. Even seemingly small fees can have a huge impact over time due to the power of compound interest. While in a no-fees scenario you might be able to retire comfortably and even accumulate such wealth to be able to retire early and live off passive income without eroding your wealth, even just 2% yearly fees might make it impossible to retire! Over a lifetime, every fraction of a percent makes up for a Ferrari that your advisor gets instead of you!
            
Transaction fees are less impactful on the long term for a disciplined buy-and-hold investor, but they can add up if you trade frequently. 
            
Always be aware of the fees you are paying and try to minimize them as much as possible. Low-cost index funds are often a better choice than actively managed funds precisely because of the high fees. Over time, the difference can be staggering! 
            
In finance you get what you *don't* pay for. Unless you have a good reason, always go for investment options with lower fees.
""")

st.info("If you want to read more about this, check out my [Substack article on the Ferrari in your Banker's driveway](https://idini.substack.com/publish/post/181027330).")