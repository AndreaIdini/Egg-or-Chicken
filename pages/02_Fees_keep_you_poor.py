import streamlit as st
import pandas as pd

from utils import calculate_compound_interest

# uncomment if standalone
# st.set_page_config(page_title="Fees keep you poor", layout="centered")

st.title("Fees keep you poor")
st.subheader("...and the banker rich 💸")

st.markdown("""Imagine a business partner who puts up $0 capital, takes 0% of the risk, but demands a cut every year that enormously draw down. This is what happens when you pay investment fees. 
            
## 1. Yearly management fees

This is the most important and insidious since it erodes your capital slowing down the snowball effect of compound interest. Yearly management fees are applied yearly as a percentage of investment. A seemingly small difference between two options can have a devastating impact by the time you retire.

Once again, the counterintuitive nature of exponentials makes it hard to realise what is really going on. Even if fees are at a relative small percentage of your returns, their compound effect can become huge with time. At an average return of 7% per year, a not unusual 2% fee means that in 30 years you will have given away half of your investment gains to the bank. And in 75 years the bank will have earned more than 3 times as you! You can see what a huge difference it makes to go with a 0.2% fee index fund instead of a mutual fund.
            
Below you can simulate different scenarios by changing the parameters.
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

st.success(f"🎉 Your earned {(invested_fees_values[-1]-initial_amount):.1f} in {years} years.")
st.warning(f"😞 Your bank earned {invested_values[-1]-invested_fees_values[-1]:,.1f} thanks to you.")

st.line_chart(Fees_dataframe, x="Year", y=["Investment", "Investment with fees"], x_label="Year", y_label="Investment value", color=["#32CD32", "#FF4B4B"])

st.markdown(""" ### Takeaway message:

Slowing down the accumulation of compound interest through fees is the single most effective way to reduce your final wealth. This is extra worse for low yield investments, like bonds where your yield can be annhilated. Always prefer low-cost index funds over actively managed funds with high fees. Over time, the difference will be staggering!""")

st.divider()

st.markdown("""
## 2. Transaction and currency costs

There are also fees a bunch that are applied when you buy or sell an asset. They can be a percentage of the transaction or a fixed cost per trade. When it comes to names, the fantasy of bankers is infinite. Transaction fees, courtage, currency conversion fees, and more names are used for what is substantially just a one-time fee. They work either on a percentage or a fixed amount basis, and all of them follow the more intuitive definition of removing a given fraction of the investment, and thus reducing the wealth down the line of that same fraction.

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
    st.warning(f"⚠️ If you were to buy and sell this quantity in a single day, with this fee, after the first day you would have on average {daily_trader:.1f} which is less than the starting capital, so you would go bust in not so many days.")

st.markdown("""### Takeaway message:
Transaction, currency conversion and all these other fees can be just a few euros/dollars/pounds, but over time the loss of not having invested those few bucks will be much larger (this is also true for that double mocha frappuccino). The *time value* of a few bucks is significant! These costs can add up over time, especially if you trade frequently.""")

st.divider()

st.markdown("""
## 3. Performance fees

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
st.warning(f"😞 Your heddge fund earned {invested_values[-1]-invested_hedge[-1]:,.1f} thanks to you.")

st.line_chart(hedge_dataframe, x="Year", y=["Investment", "Investment with fees", "Investment with hedge fund fees"], x_label="Year", y_label="Investment value", color=["#32CD32", "#FF4B4B", "#FFA500"])

st.markdown("""### Final thoughts
In the real world, performance fees are even worse, because the markets and hedge funds in particular tend to have really good years where the fees will be enormous. In order to understand this variation, we need to go into *variance* and *risk*, in the next tab.
""")

st.markdown("""## 4. The cost of doing business
            
If we consider all of the above fees together, it is easy to see how much of your investment returns are eaten up by fees. Let's see a typical case of a monthly saver and the difference from the ideal cost of the [**Egg or Chicken**](/tvm) example.
""")