import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Volume Based Industry Scanner", layout="wide")
st.title("🔥 Smart Money Industry Volume Scanner")
st.write("Yeh tool un industries aur stocks ko dhoondta hai jahan pichle averages ke mukable sabse bada Volume Spike aaya hai.")

# 1. Comprehensive Database of Indian Stocks mapped to their exact Industry & Market Cap
@st.cache_data
def get_stock_database():
    stocks_data = [
        # --- RAILWAYS ---
        {"ticker": "IRFC.NS", "name": "IRFC", "industry": "Railways", "cap": "Large Cap"},
        {"ticker": "RVNL.NS", "name": "RVNL", "industry": "Railways", "cap": "Mid Cap"},
        {"ticker": "IRCON.NS", "name": "IRCON", "industry": "Railways", "cap": "Mid Cap"},
        {"ticker": "RAILTEL.NS", "name": "RailTEL", "industry": "Railways", "cap": "Small Cap"},
        {"ticker": "TITAGARH.NS", "name": "Titagarh Rail", "industry": "Railways", "cap": "Small Cap"},
        
        # --- DEFENSE ---
        {"ticker": "HAL.NS", "name": "Hindustan Aeronautics", "industry": "Defense", "cap": "Large Cap"},
        {"ticker": "BEL.NS", "name": "Bharat Electronics", "industry": "Defense", "cap": "Large Cap"},
        {"ticker": "MAZDOCK.NS", "name": "Mazagon Dock", "industry": "Defense", "cap": "Mid Cap"},
        {"ticker": "COCHINSHIP.NS", "name": "Cochin Shipyard", "industry": "Defense", "cap": "Mid Cap"},
        {"ticker": "BDL.NS", "name": "Bharat Dynamics", "industry": "Defense", "cap": "Mid Cap"},
        
        # --- GREEN ENERGY & POWER ---
        {"ticker": "SUZLON.NS", "name": "Suzlon Energy", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "IREDA.NS", "name": "IREDA", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "TATAPOWER.NS", "name": "Tata Power", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "ADANIGREEN.NS", "name": "Adani Green", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "NHPC.NS", "name": "NHPC", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "SJVN.NS", "name": "SJVN", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        
        # --- BANKING & FINANCE ---
        {"ticker": "HDFCBANK.NS", "name": "HDFC Bank", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "ICICIBANK.NS", "name": "ICICI Bank", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "SBIN.NS", "name": "State Bank of India", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "PNB.NS", "name": "Punjab National Bank", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "IDFCFIRSTB.NS", "name": "IDFC First Bank", "industry": "Banking & Finance", "cap": "Mid Cap"},
        {"ticker": "IREDA.NS", "name": "IREDA", "industry": "Banking & Finance", "cap": "Mid Cap"},
        
        # --- IT & TECH ---
        {"ticker": "TCS.NS", "name": "TCS", "industry": "IT & Software", "cap": "Large Cap"},
        {"ticker": "INFY.NS", "name": "Infosys", "industry": "IT & Software", "cap": "Large Cap"},
        {"ticker": "WIPRO.NS", "name": "Wipro", "industry": "IT & Software", "cap": "Large Cap"},
        {"ticker": "KPITTECH.NS", "name": "KPIT Technologies", "industry": "IT & Software", "cap": "Mid Cap"},
        {"ticker": "TATAELXSI.NS", "name": "Tata Elxsi", "industry": "IT & Software", "cap": "Mid Cap"},
        {"ticker": "ZENSARTECH.NS", "name": "Zensar Tech", "industry": "IT & Software", "cap": "Small Cap"},
        
        # --- INFRA & REALTY ---
        {"ticker": "LT.NS", "name": "Larsen & Toubro", "industry": "Infrastructure & Realty", "cap": "Large Cap"},
        {"ticker": "DLF.NS", "name": "DLF", "industry": "Infrastructure & Realty", "cap": "Large Cap"},
        {"ticker": "GMRINFRA.NS", "name": "GMR Infra", "industry": "Infrastructure & Realty", "cap": "Mid Cap"},
        {"ticker": "GODREJPROP.NS", "name": "Godrej Properties", "industry": "Infrastructure & Realty", "cap": "Mid Cap"},
        {"ticker": "NBCC.NS", "name": "NBCC India", "industry": "Infrastructure & Realty", "cap": "Small Cap"},
        
        # --- CHEMICALS & FERTILIZERS ---
        {"ticker": "SRF.NS", "name": "SRF Limited", "industry": "Chemicals", "cap": "Large Cap"},
        {"ticker": "TATACHEM.NS", "name": "Tata Chemicals", "industry": "Chemicals", "cap": "Mid Cap"},
        {"ticker": "DEEPAKNTR.NS", "name": "Deepak Nitrite", "industry": "Chemicals", "cap": "Mid Cap"},
        {"ticker": "FACT.NS", "name": "FACT", "industry": "Chemicals", "cap": "Mid Cap"},
        {"ticker": "RCF.NS", "name": "Rashtriya Chemicals", "industry": "Chemicals", "cap": "Small Cap"},
        
        # --- AUTOMOBILES ---
        {"ticker": "TATAMOTORS.NS", "name": "Tata Motors", "industry": "Automobiles", "cap": "Large Cap"},
        {"ticker": "M&M.NS", "name": "Mahindra & Mahindra", "industry": "Automobiles", "cap": "Large Cap"},
        {"ticker": "MARUTI.NS", "name": "Maruti Suzuki", "industry": "Automobiles", "cap": "Large Cap"},
        {"ticker": "BAJAJ-AUTO.NS", "name": "Bajaj Auto", "industry": "Automobiles", "cap": "Large Cap"},
        {"ticker": "OLECTRA.NS", "name": "Olectra Greentech", "industry": "Automobiles", "cap": "Small Cap"},
        
        # --- PHARMA & HEALTHCARE ---
        {"ticker": "SUNPHARMA.NS", "name": "Sun Pharma", "industry": "Pharma & Healthcare", "cap": "Large Cap"},
        {"ticker": "CIPLA.NS", "name": "Cipla", "industry": "Pharma & Healthcare", "cap": "Large Cap"},
        {"ticker": "DRREDDY.NS", "name": "Dr Reddy's Labs", "industry": "Pharma & Healthcare", "cap": "Large Cap"},
        {"ticker": "LUPIN.NS", "name": "Lupin", "industry": "Pharma & Healthcare", "cap": "Mid Cap"},
        {"ticker": "JUBLPHARMA.NS", "name": "Jubilant Pharma", "industry": "Pharma & Healthcare", "cap": "Small Cap"}
    ]
    return pd.DataFrame(stocks_data)

# 2. Fetch Volume Data from yfinance
def fetch_volume_data(df_db, timeframe):
    tickers = df_db['ticker'].tolist()
    
    # Setting period based on Daily, Weekly, Monthly view
    if timeframe == "Daily":
        period, lookback = "2mo", 1
    elif timeframe == "Weekly":
        period, lookback = "6mo", 5
    else:  # Monthly
        period, lookback = "1y", 20

    # Download data
    data = yf.download(tickers, period=period, progress=False)
    
    if data.empty or 'Volume' not in data.columns or 'Close' not in data.columns:
        st.error("Yahoo Finance se data fetch nahi ho pa rha hai. Kripya thodi der baad try karein.")
        return pd.DataFrame()
        
    volume_df = data['Volume'].ffill().bfill()
    close_df = data['Close'].ffill().bfill()
    
    stock_results = []
    
    for _, row in df_db.iterrows():
        t = row['ticker']
        if t in volume_df.columns and len(volume_df[t]) > 30:
            # Current Volume (Last 'lookback' days total volume)
            current_vol = volume_df[t].iloc[-lookback:].sum()
            
            # Historical Average Volume (Excluding the current lookback period)
            avg_vol = volume_df[t].iloc[:-lookback].tail(20).mean() 
            
            # Price change percentage
            price_start = close_df[t].iloc[-lookback-1]
            price_end = close_df[t].iloc[-1]
            price_chg = ((price_end - price_start) / price_start) * 100
            
            if avg_vol > 0:
                spike_ratio = current_vol / avg_vol
                stock_results.append({
                    "ticker": t,
                    "name": row['name'],
                    "industry": row['industry'],
                    "cap": row['cap'],
                    "current_volume": int(current_vol),
                    "avg_volume": int(avg_vol),
                    "volume_spike": round(spike_ratio, 2),
                    "price_change_%": round(price_chg, 2)
                })
                
    return pd.DataFrame(stock_results)

# --- Sidebar Filters ---
st.sidebar.header("⚙️ Configuration Filters")
timeframe = st.sidebar.radio("Select Timeframe", ["Daily", "Weekly", "Monthly"])
market_cap_filter = st.sidebar.selectbox("Filter by Market Cap", ["All Caps", "Large Cap", "Mid Cap", "Small Cap"])

# Load Data
df_db = get_stock_database()

with st.spinner(f"Fetching and analyzing data for {timeframe} timeframe..."):
    df_stocks = fetch_volume_data(df_db, timeframe)

if not df_stocks.empty:
    # Filter by Market Cap if selected
    if market_cap_filter != "All Caps":
        df_stocks = df_stocks[df_stocks['cap'] == market_cap_filter]
        
    # 3. Calculate Industry-wise Aggregated Data
    industry_grouped = df_stocks.groupby('industry').agg(
        Total_Current_Volume=('current_volume', 'sum'),
        Total_Avg_Volume=('avg_volume', 'sum'),
        Average_Price_Change=('price_change_%', 'mean'),
        Total_Stocks=('ticker', 'count')
    ).reset_index()
    
    # Calculate Industry Spike Ratio
    industry_grouped['Industry_Volume_Spike'] = (industry_grouped['Total_Current_Volume'] / industry_grouped['Total_Avg_Volume']).round(2)
    
    # Sort Industry List from High to Low Volume Spike
    industry_grouped = industry_grouped.sort_values(by='Industry_Volume_Spike', ascending=False).reset_index(drop=True)
    
    # --- Main Screen Display ---
    st.subheader(f"🏆 Industry Leaderboard ({timeframe} Volume Breakout)")
    st.write("Neeche di gayi list high volume spike se low volume spike ke order me sorted hai. Industry par click karke uske andar ke stocks dekhein.")
    
    # Display Industry Cards / Accordions dynamically
    for idx, row in industry_grouped.iterrows():
        # Visual color indicator based on volume spike strength
        spike = row['Industry_Volume_Spike']
        if spike >= 2.0:
            badge = "🚀 HUGE INFLOW"
        elif spike >= 1.2:
            badge = "📈 ACCUMULATION"
        else:
            badge = "💤 NORMAL"
            
        header_text = f"#{idx+1} {row['industry'].upper()}  |  Volume Spike: {spike}x  |  ({badge})  | Avg Price Chg: {row['Average_Price_Change']:.2f}%"
        
        # Creating a Clickable Dropdown Expandable bar for each industry
        with st.expander(header_text):
            st.markdown(f"**Detailed view for {row['industry']} Industry Stocks ({market_cap_filter}):**")
            
            # Extract stocks belonging to this specific industry
            industry_stocks = df_stocks[df_stocks['industry'] == row['industry']].sort_values(by='volume_spike', ascending=False)
            
            # Clean dataframe for front-end presentation
            display_df = industry_stocks[['name', 'ticker', 'cap', 'volume_spike', 'price_change_%']].copy()
            display_df.columns = ['Stock Name', 'Ticker Code', 'Market Cap', 'Volume Spike (x times)', 'Price Change (%)']
            
            # Highlight Rows using Streamlit dataframe features
            st.dataframe(
                display_df.style.background_gradient(subset=['Volume Spike (x times)'], cmap='YlOrRd')
                                .format({'Price Change (%)': '{:.2f}%', 'Volume Spike (x times)': '{:.2f}x'}),
                use_container_width=True,
                hide_index=True
            )
else:
    st.info("Koi valid data load nahi hua. Kripya refresh karein.")
