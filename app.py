# This app is for educational purpose only. Insights gained is not financial advice. Use at your own risk!
import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time
import plotly.express as px
from datetime import datetime
import streamlit.components.v1 as components

# Add this import for API data
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page layout
# Page expands to full width
st.set_page_config(layout="wide")

# Main app tabs
main_tabs = st.tabs(["Original Interface", "Enhanced Interface"])

with main_tabs[0]:
    # Title
    try:
        # Update the path to the logo file
        image = Image.open('logo/CryptoPriceLogo.png')
        st.image(image, width=500)
    except:
        # Fallback if the logo file is not found
        st.warning("Logo image not found. Please check the path: logo/CryptoPriceLogo.png")
    
    st.title('Crypto Price App')
    st.markdown("""
    This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the CoinMarketCap!
    """)

    # About section
    expander_bar = st.expander("About")
    expander_bar.markdown("""
    * **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, plotly, requests, json, time
    * **Data source:** [CoinMarketCap API](http://coinmarketcap.com).
    """)
    
    # Page layout (continued)
    # Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
    col1 = st.sidebar
    col2, col3 = st.columns((2,1))
    
    # Sidebar + Main panel
    col1.header('API Options')
    
    # Sidebar - Currency selection for API
    currency = col1.selectbox('Select currency', ('USD', 'BTC', 'ETH'))
    
    # CoinMarketCap API setup
    API_KEY = os.getenv("COINMARKETCAP_API_KEY")  # Get API key from environment variable
    BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    
    # Cache data fetching from API
    st.subheader("CoinMarketCap API Data")
    
    # Cache data fetching from API
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def fetch_crypto_data(limit=100, currency='USD'):
        params = {
            "start": "1",
            "limit": str(limit),
            "convert": currency
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": API_KEY
        }
        
        try:
            response = requests.get(BASE_URL, headers=headers, params=params)
            data = response.json()
            
            if "data" in data:
                coins = data["data"]
                
                # Create lists to store data
                coin_name = []
                coin_symbol = []
                market_cap = []
                percent_change_1h = []
                percent_change_24h = []
                percent_change_7d = []
                price = []
                volume_24h = []
                
                # Extract data for each coin
                for coin in coins:
                    coin_name.append(coin['slug'])
                    coin_symbol.append(coin['symbol'])
                    price.append(coin['quote'][currency]['price'])
                    percent_change_1h.append(coin['quote'][currency]['percent_change_1h'])
                    percent_change_24h.append(coin['quote'][currency]['percent_change_24h'])
                    percent_change_7d.append(coin['quote'][currency]['percent_change_7d'])
                    market_cap.append(coin['quote'][currency]['market_cap'])
                    volume_24h.append(coin['quote'][currency]['volume_24h'])
                    
                # Create DataFrame
                df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 
                                          'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
                df['coin_name'] = coin_name
                df['coin_symbol'] = coin_symbol
                df['price'] = price
                df['percent_change_1h'] = percent_change_1h
                df['percent_change_24h'] = percent_change_24h
                df['percent_change_7d'] = percent_change_7d
                df['market_cap'] = market_cap
                df['volume_24h'] = volume_24h
                
                return df
            else:
                st.error(f"API Error: {data.get('status', {}).get('error_message', 'Unknown error')}")
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return pd.DataFrame()
    
    # Fetch data using API
    df = fetch_crypto_data(currency=currency)
    
    if not df.empty:
        st.write(f"Data last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Sidebar - Cryptocurrency selections
        sorted_coin = sorted(df['coin_symbol'])
        selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin[:10])
        
        df_selected_coin = df[(df['coin_symbol'].isin(selected_coin))]  # Filtering data
        
        # Sidebar - Number of coins to display
        num_coin = col1.slider('Display Top N Coins', 1, 100, 10)
        df_coins = df_selected_coin[:num_coin]
        
        # Sidebar - Percent change timeframe
        percent_timeframe = col1.selectbox('Percent change time frame', 
                                                    ['7d','24h', '1h'])
        percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
        selected_percent_timeframe = percent_dict[percent_timeframe]
        
        # Sidebar - Sorting values
        sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])
        
        # Display price data
        col2.subheader('Price Data of Selected Cryptocurrency')
        col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + 
                          str(df_selected_coin.shape[1]) + ' columns.')
        col2.dataframe(df_coins)
        
        # Download CSV data
        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="crypto_data.csv">Download CSV File</a>'
            return href
        
        col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)
        
        # Preparing data for Bar plot of % Price change
        col2.subheader('Table of % Price Change')
        df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, 
                                     df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
        df_change = df_change.set_index('coin_symbol')
        df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
        df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
        df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
        col2.dataframe(df_change)
        
        # Conditional creation of Bar plot (time frame)
        col3.subheader('Bar plot of % Price Change')
        
        if percent_timeframe == '7d':
            if df_change.empty:
                col3.warning("No data available for the selected filters.")
            else:
                if sort_values == 'Yes':
                    df_change = df_change.sort_values(by=['percent_change_7d'])
                col3.write('*7 days period*')
                plt.figure(figsize=(5, 10))
                plt.subplots_adjust(top=1, bottom=0)
                df_change['percent_change_7d'].plot(kind='barh', 
                                                     color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
                col3.pyplot(plt)
        elif percent_timeframe == '24h':
            if df_change.empty:
                col3.warning("No data available for the selected filters.")
            else:
                if sort_values == 'Yes':
                    df_change = df_change.sort_values(by=['percent_change_24h'])
                col3.write('24 hour period')
                plt.figure(figsize=(5,25))
                plt.subplots_adjust(top=1, bottom=0)
                df_change['percent_change_24h'].plot(kind='barh', 
                                                          color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
                col3.pyplot(plt)
        else:
            if df_change.empty:
                col3.warning("No data available for the selected filters.")
            else:
                if sort_values == 'Yes':
                    df_change = df_change.sort_values(by=['percent_change_1h'])
                col3.write('1 hour period')
                plt.figure(figsize=(5,25))
                plt.subplots_adjust(top=1, bottom=0)
                df_change['percent_change_1h'].plot(kind='barh', 
                                                         color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
                col3.pyplot(plt)
    else:
        st.warning("Unable to fetch data from CoinMarketCap API. Please check your API key or try again later.")

with main_tabs[1]:
    # Custom CSS for styling
    st.markdown("""
        <style>
        .title { font-size: 2.5em; color: #1f77b4; text-align: center; }
        .metric-positive { color: #00cc00; }
        .metric-negative { color: #ff3333; }
        .footer { text-align: center; font-size: 0.9em; color: #888; }
        </style>
    """, unsafe_allow_html=True)

    # App header
    st.markdown('<p class="title">CryptoPulse: Real-Time Market Tracker</p>', unsafe_allow_html=True)
    
    # Update the logo path here too
    try:
        image = Image.open('logo/CryptoPriceLogo.png')
        st.image(image, width=50)
    except:
        st.image("https://cryptologos.cc/logos/bitcoin-btc-logo.png", width=50)  # Fallback to web image

    # Theme toggle
    if "theme" not in st.session_state:
        st.session_state.theme = "Light"
    theme = st.sidebar.selectbox("Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1)
    st.session_state.theme = theme
    if theme == "Dark":
        st.markdown('<style>body { background-color: #1e1e1e; color: #ffffff; }</style>', unsafe_allow_html=True)

    # Sidebar controls
    st.sidebar.header("Settings")
    num_coins = st.sidebar.slider("Number of Coins", 5, 50, 10)
    refresh = st.sidebar.button("Refresh Data")

    # CoinMarketCap API setup
    API_KEY = "5600d1f6-de5b-4150-8dd9-8541652c49ff"  # Your API key
    BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    HEADERS = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": API_KEY}

    # Cache data fetching
    @st.cache_data(ttl=300)
    def fetch_enhanced_data(limit=10):
        params = {"start": "1", "limit": str(limit), "convert": "USD"}
        try:
            response = requests.get(BASE_URL, headers=HEADERS, params=params)
            data = response.json()
            coins = data["data"]
            df = pd.DataFrame(coins)
            df["price"] = df["quote"].apply(lambda x: x["USD"]["price"])
            df["market_cap"] = df["quote"].apply(lambda x: x["USD"]["market_cap"])
            df["volume_24h"] = df["quote"].apply(lambda x: x["USD"]["volume_24h"])
            df["percent_change_24h"] = df["quote"].apply(lambda x: x["USD"]["percent_change_24h"])
            return df[["name", "symbol", "price", "market_cap", "volume_24h", "percent_change_24h"]]
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return pd.DataFrame()

    # Fetch and display data
    data = fetch_enhanced_data(num_coins)
    
    if not data.empty:
        st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Top Gainers/Losers
        top_gainers = data.nlargest(3, "percent_change_24h")[["symbol", "percent_change_24h"]]
        top_losers = data.nsmallest(3, "percent_change_24h")[["symbol", "percent_change_24h"]]
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Gainers")
            for _, row in top_gainers.iterrows():
                st.markdown(f"{row['symbol']}: <span class='metric-positive'>+{row['percent_change_24h']:.2f}%</span>", unsafe_allow_html=True)
        with col2:
            st.subheader("Top Losers")
            for _, row in top_losers.iterrows():
                st.markdown(f"{row['symbol']}: <span class='metric-negative'>{row['percent_change_24h']:.2f}%</span>", unsafe_allow_html=True)

        # Main data table with sorting
        st.subheader("Cryptocurrency Prices")
        sorted_column = st.selectbox("Sort by", ["price", "market_cap", "volume_24h", "percent_change_24h"])
        sorted_data = data.sort_values(by=sorted_column, ascending=False)
        st.dataframe(sorted_data.style.format({
            "price": "${:.2f}",
            "market_cap": "${:,.0f}",
            "volume_24h": "${:,.0f}",
            "percent_change_24h": "{:.2f}%"
        }).applymap(lambda x: "color: #00cc00" if isinstance(x, float) and x > 0 else "color: #ff3333", subset=["percent_change_24h"]))

        # Interactive chart
        st.subheader("Price Visualization")
        chart_type = st.selectbox("Chart Type", ["Bar", "Scatter", "Line"])
        
        if chart_type == "Bar":
            fig = px.bar(sorted_data, x="symbol", y="price", color="percent_change_24h",
                        color_continuous_scale="RdYlGn", title="Crypto Prices (USD)", log_y=True)
        elif chart_type == "Scatter":
            fig = px.scatter(sorted_data, x="market_cap", y="price", color="percent_change_24h",
                            size="volume_24h", hover_name="name", log_x=True, log_y=True,
                            color_continuous_scale="RdYlGn", title="Price vs Market Cap")
        else:
            fig = px.line(sorted_data.sort_values("market_cap", ascending=False), x="symbol", y="price",
                        title="Crypto Prices (USD)", markers=True)
            
        st.plotly_chart(fig, use_container_width=True)

        # Currency converter
        st.subheader("Currency Converter")
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Enter amount in USD", min_value=0.0, value=100.0)
            selected_coin = st.selectbox("Select cryptocurrency", data["symbol"])
        
        with col2:
            coin_price = data[data["symbol"] == selected_coin]["price"].values[0]
            converted = amount / coin_price
            st.metric("Converted Amount", f"{converted:.8f} {selected_coin}")
            st.write(f"1 {selected_coin} = ${coin_price:.2f}")

        # Footer
        st.markdown('<p class="footer">Built with ❤️ by Naman | Powered by CoinMarketCap</p>', unsafe_allow_html=True)
    else:
        st.error("Unable to fetch data. Please check your API key or try again later.")