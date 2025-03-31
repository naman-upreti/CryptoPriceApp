# Crypto Price App

## Overview
Crypto Price App is a real-time cryptocurrency tracking tool built with Streamlit, designed to provide up-to-date market insights, price trends, and analytics for the top 100 cryptocurrencies. The app features interactive visualizations and data filtering tools to help users analyze market movements efficiently.

## Problem Statement
With the rapid fluctuations in cryptocurrency prices, staying informed about market trends is crucial for investors and traders. This application addresses the challenge by:

1. Providing real-time data on the top 100 cryptocurrencies
2. Offering visual representations of price changes
3. Enabling data filtering and sorting for better analysis
4. Including a built-in currency converter for quick calculations

## About Cryptocurrencies
Cryptocurrencies are digital assets secured by cryptography and powered by decentralized blockchain networks. Unlike traditional fiat currencies controlled by governments, cryptocurrencies offer:

- **Decentralization**: No central authority controls them.
- **Blockchain Technology**: Transactions are recorded on a public, distributed ledger.
- **Limited Supply**: Many cryptocurrencies, like Bitcoin, have a fixed supply cap.
- **High Volatility**: Prices can fluctuate significantly over short periods.
- **Diverse Use Cases**: Digital payments, smart contracts, and decentralized applications.

## Features
- **Real-time cryptocurrency data from CoinMarketCap**
- **Two user interfaces:**
  - **Original Interface**: Focused on raw data analysis with customizable filters
  - **Enhanced Interface**: Modern design with interactive charts and a currency converter
- **Filter cryptocurrencies** by symbol
- **Sort data** by price, market cap, volume, and percent change
- **Visualize price changes** with color-coded charts
- **Download cryptocurrency data as a CSV file**
- **Dark/Light theme toggle** in the enhanced interface
- **Built-in currency converter**

## File Structure
```
CryptoPriceApp/
├── app.py              # Main application file
├── .env                # Environment variables file (API keys, not included by default)
├── requirements.txt    # Project dependencies
├── README.md           # Documentation
├── .gitignore          # Git ignore file
└── logo/               # Directory containing the application logo
    └── CryptoPriceLogo.png  # App logo
```

## Technologies Used
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Matplotlib & Plotly** - Data visualization
- **Requests & BeautifulSoup** - API interaction and web scraping
- **Python-dotenv** - Environment variable management

## How to Use
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/CryptoPriceApp.git
   cd CryptoPriceApp
   ```
2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a `.env` file** and add your CoinMarketCap API key:
   ```
   COINMARKETCAP_API_KEY=your_api_key_here
   ```
   **Note:** While the Original Interface uses the API key from the .env file, the Enhanced Interface currently has a hardcoded API key. You may need to update this in the code (around line 258 in app.py) if you want to use your own API key for both interfaces.
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```
5. **Navigate through the UI**:
   - Use the sidebar to filter cryptocurrencies and customize the display
   - Switch between the **Original** and **Enhanced** interfaces using the tabs at the top

## Data Source
The application retrieves real-time cryptocurrency market data from the [CoinMarketCap API](https://coinmarketcap.com/api/).

## Future Enhancements
- **Historical price charts** for trend analysis
- **Price alerts and notifications**
- **Portfolio tracking functionality**
- **Additional technical indicators** (moving averages, RSI, etc.)
- **Support for more currencies**
- **Mobile-friendly UI** for better accessibility
- **Integration with TradingView** for advanced analytics

## Created By
Built with ❤️ by **Naman** | Powered by **CoinMarketCap**

