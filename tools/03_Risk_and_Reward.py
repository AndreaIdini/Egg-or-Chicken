import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


from utils import calculate_compound_interest, generate_paths, compounding_frequency_adjusted, generate_deltas

st.title("Nothing ventured, nothing gained")
st.subheader("Nothing in life is without risk")

st.markdown("""
In finance, Risk and Return are two sides of the same coin. You cannot have one without the other.
But we need to distinguish between two very different types of risk:
            
1. *Default Risk:* The company goes bankrupt. The stock goes to zero. You lose everything. Game over.
2. *Volatility Risk:* The price swings up and down. You lose some this month, but might gain more next year. The game continues.

Most people confuse the two. They cannot be more different.

**Volatility is the price of admission for high returns.**

> If you want some more guidance when looking at these simulation results, check out my [Substack article](https://open.substack.com/pub/idini/p/the-price-of-wealth-jitters?r=1rbb68).
            
## 1. The Rollercoaster (Volatility) 🎢

Volatility is a measure of emotional pain. It measures how wildly the price swings.
A bank account has 0% volatility (the number never wiggles and the price is exact). The stock market has high volatility (it wiggles a lot famously unpredictably).

Here is the cruel math of volatility: If an asset drops 50%, you need a 100% gain just to get back to even.
If volatility is too high, this "drag" pulls your long-term returns down, even if the average return looks good on paper. 

For the mathematically inclined, you can look at [the page about volatility](/volatility) for definition and how did I model it in these simulations.
            
Depending of conditions, the market has a typical volatility of 1 to 2% per month. Try to run several simulations and see how different degree of volatility affects the final value at short and long time horizons.
""")

col1, col2 = st.columns(2)

with col1:
    # Numeric input for the initial amount
    initial_amount = st.number_input("Initial investment (currency)", value=1000.0, step=100.0)

with col2:
    # Slider for the number of years
    years = st.slider("Time Horizon (Years)", min_value=1, max_value=75, value=30)

col3, col4 = st.columns(2)

with col3:
    # Input for inflation rate (default 2%)
    investment_rate = st.number_input("Investment Return (%)", value=7.0, step=0.1)

with col4:
    # Input for volatility (default 15%)
    investment_volatility = st.slider("Investment Volatility (%/month)", min_value=0.0, max_value=20.0, value=2.)

buf1, col5, buf2 = st.columns(3)

with col5:
    if st.button("Make another simulation"):
        seed = False

year_range = list(range(12*years+1))
investment_rate = compounding_frequency_adjusted(investment_rate, 12)
invested_values = calculate_compound_interest(initial_amount, investment_rate, year_range)
invested_volatility = generate_paths(12*years+1, investment_volatility/100, investment_rate, start_val=initial_amount)
year_range = [yr/12 for yr in year_range]

Fees_dataframe = pd.DataFrame({
    "Year": year_range,
    "Investment": invested_values,
    "Investment with volatility": invested_volatility 
    })

st.line_chart(Fees_dataframe, x="Year", y=["Investment", "Investment with volatility"], x_label="Year", y_label="Investment value", color=["#32CD32", "#FF4B4B"])

st.markdown("""
###  Takeaway message: 
            
- At least for relatively low volatility of total market 1 or 2% per month, you can expect that over long enough time horizons (30 years or more) the final value of your investment will always be positive and usually close to the average expected return.
- Volatility implies that an investment might lose value for several years before recovering. Being *locked in* is the *risk* of the market in this case.
- As volatility increases, the final value can be significantly different than the average expected return even for long time horizons (drag).
- Very high volatility over long time always leads to default. In this stocastic model, what goes up quickly, can go down just as quickly. The important difference being that doubling your money is nice, but there's no come back from zero.
""")
# note that for high volatility and high time horizon, the final value is always zero.

st.divider()

st.markdown("""
## 2. Rewarding the brave 🦁

Since volatility is a risk that investors have to bear, they expect to be compensated for it. As a rule, the more volatile an investment is, the higher the expected return should be. The following simulation gives all equally valid investments, for different degree of risk (the measure of this is the **Sharpe ratio**, which is explained [here](/volatility)).      
""")

# Sharpe ratio = (Return of the investment - Risk-free rate) / Volatility

if "roi" not in st.session_state:
    st.session_state.roi = 7.
if "volatility" not in st.session_state:
    st.session_state.volatility = 2.

# 2. DEFINE CALLBACK FUNCTIONS
# These run immediately when a slider is moved, BEFORE the page reloads.
sharpe_ratio = 2.
risk_free_rate = 3.

def update_roi():
    # If Stocks changed, Bonds must become the remainder
    st.session_state.roi =  st.session_state.volatility * sharpe_ratio + risk_free_rate

def update_volatility():
    # If Bonds changed, Stocks must become the remainder
    st.session_state.volatility = (st.session_state.roi - risk_free_rate) / sharpe_ratio

# 3. CREATE THE SLIDERS
col1, col2 = st.columns(2)

with col1:
    # Notice we don't use 'value='. We use 'key='.
    # Streamlit automatically binds the slider to st.session_state['stocks']
    st.slider(
        "Return (%)", 
        min_value=risk_free_rate, 
        max_value=15., 
        key="roi",          # Links to st.session_state.stocks
        on_change=update_volatility # Trigger this function when user moves this slider
    )

with col2:
    st.slider(
        "Volatility (%/month)", 
        min_value=0., 
        max_value=12., 
        key="volatility",           # Links to st.session_state.bonds
        on_change=update_roi # Trigger this function when user moves this slider
    )

buf1, col5, buf2 = st.columns(3)

with col5:
    if st.button("Make another simulation", key="button2"):
        seed = False

investment_rate = compounding_frequency_adjusted(st.session_state.roi, 12)
invested_values = calculate_compound_interest(initial_amount, risk_free_rate, year_range)
invested_volatility = generate_paths(12*years+1, st.session_state.volatility/100, investment_rate, start_val=initial_amount)

Fees_dataframe = pd.DataFrame({
    "Year": year_range,
    "Investment": invested_values,
    "Investment with volatility": invested_volatility 
    })

st.line_chart(Fees_dataframe, x="Year", y=["Investment", "Investment with volatility"], x_label="Year", y_label="Investment value", color=["#32CD32", "#FF4B4B"])

st.markdown("""
###  Takeaway message: 
            
- Short Term: Volatility is gambling. You might gain a lot of money or lose a lot of it, with no predictable pattern.
- Long Term: Volatility is statistics. The higher expected return eventually dominates over the volatility.
- Very high volatility can lead to radical losses even on the long term.
""")

st.divider()

st.markdown("""
## 3. Time is the Great Equalizer ⏳
            
This leads to the most important concept in investing: time is your friend.
Over 1 year, the stock market is almost a casino. You can make money or lose it.
Over 20 years, the stock market has (historically) never lost money. Assuming you invested correctly (i.e. in the [total market](/tvm) with [low fees](/fees))

Run 100 simulations below. Watch how the "Probability of Loss" collapses as you compare short and long term.
""")

@st.cache_data
def run_montecarlo(n_sims, time, volatility, rate, initial_amount):

    paths = []
    for i in range(n_sims):
        paths.append(generate_paths(time, volatility, rate, start_val=initial_amount))
    return paths

with st.form("Risk and Return simulation"):
    col1, col2 = st.columns(2)
    with col1:
        investment_rate = st.number_input("Investment Return (%)", value=7.0, step=0.1, key="mc_rate")
    with col2:
        investment_volatility = st.number_input("Investment Volatility (%/month)", value=2., key="mc_volatility")
        
    # The button that triggers the update
    calculate_btn = st.form_submit_button("Run Simulation")

buf1, col3, buf2 = st.columns(3)
with col3:
    comparison_year = st.slider("Time Horizon (Years)", min_value=1, max_value=10, value=1, key="mc_years")

initial_amount = 1000
years = 50
investment_rate = compounding_frequency_adjusted(investment_rate, 12)

paths = run_montecarlo(100, 12*years+1, investment_volatility/100, investment_rate, initial_amount)

year1 = []
year50 = []
for p in paths:
    year1.append(p[12*comparison_year])
    year50.append(p[-1])

# make a histogram in streamlit
col1, col2 = st.columns(2)
with col1:
    # counts, bin_edges = np.histogram(year1, bins=5)

    # how many values are below initial amount
    below_initial = sum(1 for v in year1 if v < initial_amount)
    below_risk_free = sum(1 for v in year1 if v < calculate_compound_interest(initial_amount, risk_free_rate, comparison_year))
    st.write(f"""After {comparison_year} years, out of 100 simulations, 
- {below_initial} are below initial amount, {np.min(year1):.2f} being the lowest.
- {below_risk_free} are below 3% risk-free amount.
- {np.max(year1):.2f} is the most successful simulation.""")

    fig = px.histogram(
        year1, 
        nbins=10, 
        title=f"Distribution of values after {comparison_year} year(s)",
        labels={'value': 'value after 1 year', 'count': 'Frequency'},
        opacity=0.8,
        template="simple_white" # Clean look
    )
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,           # 99% from the bottom (top)
            xanchor="right",
            x=0.99,           # 1% from the left
            bgcolor="rgba(255, 255, 255, 0.5)" # Optional: semi-transparent background
        )
    )

    # This forces the bars to have a thin white gap (looks more professional)
    fig.update_traces(marker_line_width=1.5, marker_line_color="white")
    fig.update_xaxes(range=[min(np.min(year1)*0.95, initial_amount), np.max(year1)*1.05])
    # Add a vertical line for the Mean or Median
    # fig.add_vline(x=np.mean(year1), line_width=5, line_dash="dash", line_color="red", opacity=1.0)

    fig.add_vline(x=initial_amount, line_width=4, line_dash="solid", line_color="green", opacity=1.0)

    fig.add_vline(x=calculate_compound_interest(initial_amount, risk_free_rate, comparison_year), line_width=4, line_dash="solid", line_color="red")

    st.plotly_chart(fig, use_container_width=True)

    # st.write("Distribution of Portfolio Values After 1 Year")
    # st.write(f"Mean: {np.mean(year1):.2f}, Std Dev: {np.std(year1):.2f}")
    # # 2. Create a clean DataFrame for the bar chart
    # # We use the bin edges as the index (labels)
    # # st.write(bin_edges)
    # hist_df = pd.DataFrame({'count': counts}, index=bin_edges[:-1])
    # st.write(hist_df)
    # # 3. Plot using the native bar chart
    # st.bar_chart(hist_df)
with col2:
    # st.write("Distribution of Portfolio Values After 50 Years")
    # st.write(f"Mean: {np.mean(year50):.2f}, Std Dev: {np.std(year50):.2f}")
    # counts, bin_edges = np.histogram(year50, bins=5)
    below_initial = sum(1 for v in year50 if v < initial_amount)
    below_risk_free = sum(1 for v in year50 if v < calculate_compound_interest(initial_amount, risk_free_rate, 50))


    st.write(f"""After 50 years, out of 100 simulations, 
- {below_initial} are below initial amount, {np.min(year50):.2f} being the lowest.
- {below_risk_free} are below 3% risk-free amount.
- {np.max(year50):.2f} is the most successful simulation.""")

    fig = px.histogram(
        year50, 
        nbins=20,
        title="Distribution of values after 50 year",
        labels={'value': 'value after 50 year', 'count': 'Frequency'},
        opacity=0.8,
        template="simple_white" # Clean look
    )
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,           # 99% from the bottom (top)
            xanchor="right",
            x=0.99,           # 1% from the left
            bgcolor="rgba(255, 255, 255, 0.5)" # Optional: semi-transparent background
        )
    )

    # This forces the bars to have a thin white gap 
    fig.update_traces(marker_line_width=1.5, marker_line_color="white")
    # fig.update_xaxes(range=[0, np.max(year50)*1.1])
    # Add a vertical line for the Mean or Median
    # fig.add_vline(x=np.mean(year50), line_width=5, line_dash="dash", line_color="red", opacity=1.0)

    fig.add_vline(x=initial_amount, line_width=4, line_dash="solid", line_color="green", opacity=1.0)

    fig.add_vline(x=calculate_compound_interest(initial_amount, risk_free_rate, 50), line_width=4, line_dash="solid", line_color="red")

    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
###  Takeaway message: 
- If you need the money in 2 years, the stock market is dangerous.
- If you need the money in 20 years, cash is lethal (due to [inflation](/tvm)) and the stock market is relatively safe.
Time turns risk into certainty.
""")

st.divider()

st.markdown("""
## 4. Riding the waves
            
Now that we understand volatility better, let's see how it affects the simulation of accumulation and decumulation of wealth during working years and retirement. While volatility can be scary, there's an automatic psychological safety embedded in most people's investment profile: the accumulation is monthly.
            
During working years, you put automatically money in the market every month, buying the corresponding number of shares. This is called dollar-cost averaging and it automatically reduces the effect of volatility. When the market is down, you buy more shares, that will appreciate even more later on.
            
In the following, we run 100 simulations of a financial life cycle with different volatility scenarios, and see how it affects the wealth over time. The blue band shows where 90% of the simulations lie. The default 3% risk free investment (inflation adjusted) is quite optimistic and shown for comparison. As always, you can adjust all the parameters and run your own scenario.
""")

with st.form("Retirement Simulation with volatility"):

    col1, col2, col3 = st.columns(3)
    with col1:
        investment_rate = st.number_input("Investment Yield (after fees) (%).", value=7.0, step=0.1)

    with col2:
        investment_volatility = st.number_input("Investment Volatility (%/month).", value=2.0, step=0.1)

    with col3:
        rf_rate = st.number_input("Risk-free rate (%).", value=3.0, step=0.1)

    with st.expander("⚙️ Settings"):
        opt_col1, opt_col2 = st.columns(2)

        with opt_col1:
            job_savings = st.number_input("Work savings (real value)", value=1000, step=100)

        with opt_col2:
            years_work = st.slider("Work life (Years)", min_value=10, max_value=50, value=40)

        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            retirement_spending = st.number_input("Retirement spending (real value).", value=5000, step=100)

        with opt_col2:
            years_retirement = st.slider("Retirement (Years)", min_value=0, max_value=70, value=30)

                    
    # The button that triggers the update
    calculate_btn = st.form_submit_button("Run Simulation")

years = years_work + years_retirement

year_range = list(range(12*years+1))
investment_rate = compounding_frequency_adjusted(investment_rate, 12)
rf_rate = compounding_frequency_adjusted(rf_rate, 12)

@st.cache_data
def run_montecarlo_delta(n_sims, time, volatility, rate):

    paths = []
    for i in range(n_sims):
        paths.append(generate_deltas(time, volatility, rate))
    return paths

contributions = [job_savings/12] * (years_work*12) + [-retirement_spending/12] * (years_retirement*12)
total_contributions = job_savings*years_work
# total_contributions_value = total_contributions/calculate_compound_interest(1, investment_rate, years_work)/2.

delta_paths = run_montecarlo_delta(100, 12*years+1, investment_volatility/100, investment_rate)

monthly_paths = []
for delta in delta_paths:
    invested = [0]
    for i in range(1,12*years):
        invested.append( (invested[-1]+contributions[i-1]) * (1 + delta[i-1]))
    monthly_paths.append(invested)

monthly_paths = np.asarray(monthly_paths)

# lump_paths =[]
# for delta in delta_paths:
#     invested = [total_contributions_value]
#     for i in range(1,12*years):
#         invested.append( (invested[-1]) * (1 + delta[i-1]))
#     lump_paths.append(invested)

# lump_median = np.median(lump_paths, axis=0)

median_path = np.median(monthly_paths, axis=0)
lower_bound = np.percentile(monthly_paths, 5, axis=0)
upper_bound = np.percentile(monthly_paths, 95, axis=0)

# st.write(risk_free_rate, median_path)

default_data = pd.DataFrame({
    "Year": [yr/12 for yr in range(1, 12*years + 1)],
    "Median Investment Rate (%)": median_path, # [3.0, 3.0, 3.0, 3.0, 3.0]
    "Lower Bound Rate (%)": lower_bound,
    "Upper Bound Rate (%)": upper_bound,
    "Contribution": contributions
})

# add column to dataframe
default_data["Investment Value"] = median_path
default_data["Lower Bound"] = lower_bound
default_data["Upper Bound"] = upper_bound

invested_rf = [0]
for i in range(1, 12*years):
    invested_rf.append( (invested_rf[-1]+default_data["Contribution"][i-1]) * (1 + rf_rate/100))

default_data["Risk-Free Investment"] = invested_rf



# if min(invested) < 0:
#     st.error("⚠️ Warning: You run out of invested money during retirement!")
#     # find the first year where invested < 0
#     for i in range(len(invested)):
#         if invested[i] < 0:
#             years = i+1
#             break

# else:
#     st.success("🎉 Success: Your investments last through retirement!")


# st.line_chart(default_data, x="Year", y=["Investment Value", "Risk-Free Investment"], x_label="Year", y_label="Investment value", color=["#32CD32", "#FF4B4B"])


# Plotly line chart with fill between for volatility
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=default_data["Year"],
    y=default_data["Investment Value"],
    mode='lines',
    name='Median Monthly Investment Outcome',
    line=dict(color='rgb(0, 100, 255)', width=3)
))

fig.add_trace(go.Scatter(
    x=default_data["Year"],
    y=default_data["Upper Bound"],
    mode='lines',
    line=dict(width=0), # No line
    showlegend=False,
    name='Upper 90%'
))

fig.add_trace(go.Scatter(
    x=default_data["Year"],
    y=default_data["Lower Bound"],
    mode='lines',
    line=dict(width=0), # No line
    fill='tonexty',     # <--- Fills area between this trace and the previous one
    fillcolor='rgba(0, 100, 255, 0.2)', # Blue with 20% opacity
    showlegend=False,
    name='Lower 10%'
))

fig.add_trace(go.Scatter(
    x=default_data["Year"],
    y=default_data["Risk-Free Investment"],
    mode='lines',
    line=dict(color='#32CD32'), # Solid Blue
    name='Volatility-Free Outcome'
))

# fig.add_trace(go.Scatter(
#     x=default_data["Year"],
#     y=lump_median,
#     mode='lines',
#     line=dict(color='#32CD32'), # Solid Blue
#     name='Lump Sum Outcome'
# ))

# 3. LAYOUT POLISH
fig.update_layout(
    title="Simulation of retirement with volatility",
    xaxis_title="Years",
    yaxis_title="Portfolio Value",
    template="simple_white",
    hovermode="x unified" # Shows all values when hovering over a specific year
)

fig.update_layout(
    legend=dict(
        yanchor="top",
        y=0.99,           # 99% from the bottom (top)
        xanchor="left",
        x=0.01,           # 1% from the left
        bgcolor="rgba(255, 255, 255, 0.5)" # Optional: semi-transparent background
    )
)


st.write(f"""
### 📊  Simulation Results
- After {years_work} years of work and {years_retirement} years of retirement, you saved {total_contributions/1000.:.0f} thousands and spent {retirement_spending*years_retirement/1000.:.0f} thousands in real currency value (inflation adjusted).""")

if invested_rf[-1] >= 0:
    st.write(f"- Investing only on bonds without volatility gives {invested_rf[-1]:.2f} real currency, lasting through retirment 🎉")
else:
    st.write(f"- Investing only on volatility-free bonds runs out of money after {(next(i for i, v in enumerate(invested_rf) if v < 0)/12)-years_work:.1f} years of retirement ⚠️")

st.write(f"""- Despite the volatility, investing with monthly contributions gives a median outcome of {median_path[-1]/1000.:.0f} thousands real currency after retirement, that means that half scenarios will be above that and half below.
- 90% of scenarios will end up between from {lower_bound[-1]/1000.:.0f} thousands to {upper_bound[-1]/1000.:.0f} thousands real currency.""")

st.plotly_chart(fig, use_container_width=True)


st.markdown("""### 📝  Final thoughts
- Volatility is not the enemy or scary. It is the engine of growth.
- *The "Risk-Free" trap:* Bonds and cash feel safe, but they often fail to accumulate enough for retirement. That is a guaranteed slow death.
- *The solution:* A diversified portfolio (to eliminate Default Risk), held for a long time (to tame Volatility Risk), purchased monthly (to profit from the dips).
""")

st.info("If you want to read more about this, check out my [Substack article](https://open.substack.com/pub/idini/p/the-price-of-wealth-jitters?r=1rbb68).")