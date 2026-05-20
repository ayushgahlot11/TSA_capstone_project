# 2026 Capstone Project: Predicting Stocks and Building a Smart Portfolio (NSE India)

## Project Overview
This project is a complete automated system for trading stocks. The goal is to use historical data to predict where stock prices will go in the short term. Using these predictions, the system builds a safe, well-balanced portfolio using 26 stocks from the National Stock Exchange of India (NSE). 

To do this, the system uses statistical models to guess future prices. It also measures how risky and unpredictable each stock is. Finally, it uses a mixed strategy to decide exactly how much money to invest in each stock, aiming to grow the money while protecting it from sudden market crashes.

## Key Features
* **Automatic Data Collection:** It automatically downloads daily stock market data using Yahoo Finance.
* **Market Trend Checking:** It looks at the last 30 days of price swings and compares short-term and long-term averages to figure out if a stock is generally going up or down.
* **Two-Model Prediction System:** It pits two different forecasting models against each other to see which one makes better predictions.
* **Safety-First Investing (Risk-Adjusted Sizing):** It puts more money into stable, reliable stocks and less money into jumpy, unpredictable stocks to protect the overall budget.
* **Live Simulation:** It tests the strategy on unseen data, acting like a real trading bot that automatically filters out bad stocks and only buys the ones it thinks will make a profit.

## How to Run This on Your Computer
To set up this project and run the code yourself, make sure you have Python 3.9 or newer installed.

1. Download (clone) the project to your computer:
   ```bash
   git clone <https://github.com/ayushgahlot11/TSA_capstone_project.git>
   cd TSA_Capstone_2026
   ```