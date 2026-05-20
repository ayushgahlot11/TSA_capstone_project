import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE SETUP ---
st.set_page_config(page_title="TSA Capstone 2026 | Portfolio Dashboard", layout="wide")
st.title("📈 TSA Capstone 2026: Live Portfolio Execution Dashboard")
st.markdown("Interactive visualization of forecasting models, capital allocation, and live market execution.")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        allocation_df = pd.read_csv("reports/task5_final_allocation.csv")
        eval_df = pd.read_csv("experiment_live/reports/live_portfolio_evaluation.csv")
        vol_df = pd.read_csv("reports/task4_volatility_and_trend.csv")
        raw_data = pd.read_csv("data/raw/capstone_raw_data.csv", index_col=0, parse_dates=True)
        return allocation_df, eval_df, vol_df, raw_data
    except Exception as e:
        st.error(f"⚠️ Data missing! Ensure paths are correct. Error: {e}")
        return None, None, None, None

allocation_df, eval_df, vol_df, raw_data = load_data()

if allocation_df is not None:
    
    st.divider()

    # --- ROW 1: ALLOCATION & CORRELATION ---
    col1, col2 = st.columns(2)

    with col1:
        # UPDATED: Explicitly linking to Task 5
        st.subheader("1. Final Capital Allocation (Task 5)")
        alloc_col = [col for col in allocation_df.columns if 'Allocated' in col][0]
        pie_data = allocation_df[allocation_df[alloc_col] > 0]
        
        fig_pie = px.pie(
            pie_data, 
            values=alloc_col, 
            names='Stock', 
        )
        
        # Keep labels outside, shrink the font slightly so they fit better
        fig_pie.update_traces(
            textposition='outside', 
            textinfo='percent+label',
            textfont_size=11  
        )
        
        # Massive margins and increased height to force it to center and not cut off
        fig_pie.update_layout(
            showlegend=False,
            height=650,  
            margin=dict(t=100, b=100, l=120, r=120) 
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
        

    with col2:
        # UPDATED: Explicitly explaining Diversification Strategy
        st.subheader("2. Asset Correlation Matrix (Diversification Check)")
        st.markdown("Verifying Task 5 Strategy C: Ensuring low cross-asset correlation to minimize sector-wide risk.")
        corr_matrix = raw_data.tail(125).corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, cmap="coolwarm", annot=False, ax=ax)
        st.pyplot(fig)

    st.divider()

    # --- ROW 2: FORECAST VS ACTUAL (GRAPHS) ---
    # UPDATED: Explicitly naming Task 8 and May 2026 execution
    st.subheader("3. Live Execution (Task 8): Actual vs Predicted Prices")
    st.markdown("Out-of-sample performance during the **May 2026** StockGro trading window.")
    
    col_bar, col_scatter = st.columns(2)
    
    with col_bar:
        # Grouped bar chart showing the comparison for every stock
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=eval_df['Stock'], y=eval_df['Pred Day 2'], name='Predicted', marker_color='#1f77b4'))
        fig_bar.add_trace(go.Bar(x=eval_df['Stock'], y=eval_df['Actual Day 2'], name='Actual', marker_color='#ff7f0e'))
        fig_bar.update_layout(title="All Stocks: Final Day Execution Prices", barmode='group', xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_scatter:
        # Scatter plot mapping Prediction Accuracy
        fig_scatter = px.scatter(
            eval_df, x='Actual Day 2', y='Pred Day 2', hover_name='Stock',
            title="Forecast Accuracy (Closer to dotted line = Better)",
            labels={'Actual Day 2': 'Actual Market Price', 'Pred Day 2': 'Model Predicted Price'}
        )
        # Add the 45-degree perfect prediction line
        min_val = min(eval_df['Actual Day 2'].min(), eval_df['Pred Day 2'].min())
        max_val = max(eval_df['Actual Day 2'].max(), eval_df['Pred Day 2'].max())
        fig_scatter.add_shape(type="line", x0=min_val, y0=min_val, x1=max_val, y1=max_val, line=dict(color="White", dash="dash"))
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # --- ROW 3: VOLATILITY & TREND (GRAPHS) ---
    # UPDATED: Explicitly linking to Task 4
    st.subheader("4. Risk Profiling (Task 4): Trend & Volatility Graphs")
    st.markdown("Asset volatility ranked highest to lowest, color-coded by macro trend.")
    
    vol_col = [col for col in vol_df.columns if 'Vol' in col][0]
    
    # Replace the table with an actual Bar Graph
    vol_df_sorted = vol_df.sort_values(by=vol_col, ascending=False)
    
    fig_vol = px.bar(
        vol_df_sorted, 
        x='Stock', 
        y=vol_col, 
        color='Overall Trend Status',
        color_discrete_map={
            'Strong Upward': '#00cc66', 
            'Upward': '#66ff99',
            'Downward': '#ff4d4d', 
            'Sideways / Consolidation': '#a6a6a6'
        },
    )
    fig_vol.update_layout(xaxis_tickangle=-45, yaxis_title="Calculated Volatility Risk")
    st.plotly_chart(fig_vol, use_container_width=True)

    # --- INTERACTIVE DEEP DIVE: LINE GRAPHS ---
    st.divider()
    st.subheader("5. Deep Dive: Individual Asset Dynamics")
    st.markdown("Select an individual equity to inspect its historical trend overlay and rolling volatility profile.")
    
    # Create a dropdown menu
    stock_list = vol_df['Stock'].tolist()
    selected_stock = st.selectbox("Select a Stock:", stock_list)
    
    if selected_stock in raw_data.columns:
        # Extract the specific time series
        stock_series = raw_data[selected_stock].dropna()
        
        # Calculate moving average (Trend) and rolling standard dev (Volatility)
        sma_50 = stock_series.rolling(window=50).mean()
        rolling_vol = stock_series.pct_change().rolling(window=30).std()
        
        col_trend, col_vol = st.columns(2)
        
        with col_trend:
            # Line graph for Price and Trend
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(x=stock_series.index, y=stock_series.values, mode='lines', name='Daily Price', opacity=0.6))
            fig_trend.add_trace(go.Scatter(x=sma_50.index, y=sma_50.values, mode='lines', name='50-Day SMA Trend', line=dict(color='#ff7f0e', width=2)))
            fig_trend.update_layout(title=f"{selected_stock} - Price vs Trend", xaxis_title="Date", yaxis_title="Price (₹)")
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with col_vol:
            # Line graph for Volatility
            fig_roll_vol = px.line(
                x=rolling_vol.index, y=rolling_vol.values, 
                title=f"{selected_stock} - 30-Day Rolling Volatility"
            )
            # Layout handles the axes, Traces handle the line color!
            fig_roll_vol.update_layout(xaxis_title="Date", yaxis_title="Risk (Std Dev of Returns)")
            fig_roll_vol.update_traces(line_color='#d62728')
            
            st.plotly_chart(fig_roll_vol, use_container_width=True)