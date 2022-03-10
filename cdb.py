import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
from datetime import datetime as dt
import quandl 


plt.style.use("ggplot")
st.sidebar.write("""
# Crypto Dashboard (Dollar pairs only)
""")

st.sidebar.header("Coin input")

#Get user input
start = st.sidebar.date_input("From",dt(2017, 1, 1))
end = st.sidebar.date_input("To",dt.now())
ticker = st.sidebar.text_input("Coin ticker","BTC")
#pair = st.sidebar.text_input("USD for Dollar or the coin's ticker for other currencies pairing","USD")

#Coin Data
def coin_data() :
    df = quandl.get("BITFINEX/"+ticker+"USD", authtoken="xTg8PEQnESopgGUhA38H")
    coin = df.loc[start:end]
    return coin

coin = coin_data()
st.header(ticker.upper()+"/USD"+" Data")
st.dataframe(coin)

#Figure
def fig() :
    fig,ax = plt.subplots(figsize = (30,18), constrained_layout=True)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))
    plt.yticks(fontsize = 15)
    plt.xticks(fontsize = 15)
    plt.xlabel("Dates",fontsize = 20)
    return (fig,ax)

#EMA
def ema(data,period) : 
     return data.ewm(period).mean()

#SMA
def sma(data,period) :
    return data.rolling(period).mean()
    
#Price movement chart
st.header(ticker.upper()+"/USD"+" Price Movement")
two_hundred_ema = ema(coin["Last"],200)
fifty_ema = ema(coin["Last"],50)
fig1,ax1 = fig()
ax1.plot(coin.index,coin["Last"], lw = 3, c = "g", label = ticker.upper()+" Price", alpha = 0.6)
ax1.plot(two_hundred_ema, lw = 2, c = "darkorange", label ="200 EMA", alpha = 0.6)
ax1.plot(fifty_ema, lw = 2, c = "deepskyblue", label ="50 EMA", alpha = 0.6)
plt.legend(loc = "center left", bbox_to_anchor=(1.0, 0.5), fontsize = 20)
plt.ylabel("Price",fontsize = 20)
plt.title(ticker.upper()+" Price movement chart", fontsize = 50)
st.pyplot(fig1)

#Volume
st.header(ticker.upper()+"/USD"+" Volume")
fig2,ax2 = fig()
ax2.bar(coin.index, coin["Volume"], color = "g", alpha = 0.6)
plt.ylabel("Volume",fontsize = 20)
plt.title(ticker.upper()+" Volume chart", fontsize = 50)
st.pyplot(fig2)

#Bollinger bands indicator
st.header("Bollinger bands indicator")
twenty_sma = sma(coin["Last"],20)
upper_band = coin["Last"] + 2*(coin["Last"].rolling(20).std())
lower_band = coin["Last"] - 2*(coin["Last"].rolling(20).std())
fig3,ax3 = fig()
ax3.plot(coin["Last"], c = "steelblue", lw = 3, label = "Price", alpha = 0.8)
ax3.plot(twenty_sma, c = "maroon", lw = 1, label = "20 SMA")
ax3.plot(upper_band, c = "g", lw = 1, alpha = 0.5, ls = "--", label = "Upper band")
ax3.plot(lower_band, c = "r", lw = 1, alpha = 0.5, ls = "--", label = "Lower band")
plt.legend(loc = "center left", bbox_to_anchor=(1.0, 0.5), fontsize = 20)
plt.ylabel("Price",fontsize = 20)
plt.title("Bollinger bands indicator", fontsize = 50)
st.pyplot(fig3)

#RSI indicator
st.header("Relative strength index (RSI) indicator")
if len(coin.index) < 14 :
    st.write("Selected range must be over 14 days")
else :
    price_diff = coin["Last"].diff() #the price difference between everyday and it's previous day
    price_diff = price_diff[1:] #since the first day in the selected period has no previous day the first row of the price difference table was neglected because it has no value
    gain = price_diff.copy()
    gain[gain < 0] = 0
    loss = price_diff.copy()
    loss[loss > 0] = 0
    avg_gain = sma(gain,14)
    avg_loss = abs(sma(loss,14))
    rs = avg_gain[13:] / avg_loss[13:]
    rsi = 100.0 - (100.0/(1.0 + rs))
    fig4,ax4 = fig()
    ax4.plot(rsi, lw = 2, color = "dodgerblue", label = "RSI", alpha = 0.8)
    plt.axhline(30, c= "limegreen", label = "30 line", ls = "-.")
    plt.axhline(70, c= "crimson", label = "70 line", ls = "-.")
    plt.legend(loc = "center left", bbox_to_anchor=(1.0, 0.5), fontsize = 20)
    plt.ylabel("Momentum",fontsize = 20)
    plt.title("Relative strength index indicator", fontsize = 50)
    st.pyplot(fig4)

#MACD indicator
st.header("Moving average convergence divergence (MACD) indicator")
macd = ema(coin["Last"],12) - ema(coin["Last"],26)
signal_line = ema(macd,9)
fig5,ax5 = fig()
ax5.plot(macd, lw = 3 , color = "coral", label = "MACD" , alpha = 0.8 )
ax5.plot(signal_line, lw = 3 , color = "deepskyblue", label = "Signal line" , alpha = 0.8 )
plt.legend(loc = "center left", bbox_to_anchor=(1.0, 0.5), fontsize = 20)
plt.title("Moving average convergence divergence indicator", fontsize = 50)
st.pyplot(fig5)

