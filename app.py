#APP STREAMLIT : (commande : streamlit run XX/dashboard.py depuis le dossier python)
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
#import time
import math
from urllib.request import urlopen
import json
import requests
#from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")


def get_response(url):
    response = requests.get(url)
    print(response)
    return response.json()

            
    #######################################
    # HOME PAGE - MAIN CONTENT
    #######################################

    #Titre principal

html_temp = """
    <div style="background-color: gray; padding:10px; border-radius:10px">
    <h1 style="color: white; text-align:center">Dashboard - Markers</h1>
    </div>
    <p style="font-size: 20px; font-weight: bold; text-align:center">
    Finance</p>
    """
st.markdown(html_temp, unsafe_allow_html=True)

with st.expander("What is this app for?"):
        st.write("This app is used to display financial markers") 


#----------------------------------------------------------------
# Load the data
#-----------------------------------------------------------------

# Create a Yahoo Finance ticker objects
stock_SP = yf.Ticker('^SPX')
stock_10y_futures = yf.Ticker('ZNZ23.CBT')
stock_3m_interest = yf.Ticker('^IRX')
stock_10y_interest = yf.Ticker('^TNX')
stock_vix_index = yf.Ticker('^VIX')
        
# Fetch historical data for the stocks
historical_data_SP = stock_SP.history(period='10y')
historical_data_10y_futures = stock_10y_futures.history(period='1y')
historical_data_3m_interest = stock_3m_interest.history(period='10y')
historical_data_10y_interest = stock_10y_interest.history(period='10y')
historical_data_vix_index = stock_vix_index.history(period='10y')

# Extract the closing prices for 1 year
prices_SP = historical_data_SP['Close']
prices_10y_futures = historical_data_10y_futures['Close']
prices_3m_interest = historical_data_3m_interest['Close']
prices_10y_interest = historical_data_10y_interest['Close']
prices_vix_index = historical_data_vix_index['Close']

# Extract 2-year US interest rate for the last 10 years

# 2023      
csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2023/all?field_tdr_date_value=2023&type=daily_treasury_yield_curve&page&_format=csv'
req = requests.get(csv_url, verify=False)
url_content = req.content
csv_file = open('2023_rates.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
rates_2023 = pd.read_csv('2023_rates.csv')
rates_2023['Date'] = pd.to_datetime(rates_2023['Date'], format='%m/%d/%Y')
# Set the date column as the index
rates_2023.set_index('Date', inplace=True)

# 2022
csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2022/all?field_tdr_date_value=2022&type=daily_treasury_yield_curve&page&_format=csv'
req = requests.get(csv_url, verify=False)
url_content = req.content
csv_file = open('2022_rates.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
rates_2022 = pd.read_csv('2022_rates.csv')
rates_2022['Date'] = pd.to_datetime(rates_2022['Date'], format='%m/%d/%Y')
# Set the date column as the index
rates_2022.set_index('Date', inplace=True)
rates_2022_2023 = pd.concat([rates_2023, rates_2022], ignore_index=False)

# 2021
csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2021/all?field_tdr_date_value=2021&type=daily_treasury_yield_curve&page&_format=csv'
req = requests.get(csv_url, verify=False)
url_content = req.content
csv_file = open('2021_rates.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
rates_2021 = pd.read_csv('2021_rates.csv')
rates_2021['Date'] = pd.to_datetime(rates_2021['Date'], format='%m/%d/%Y')
# Set the date column as the index
rates_2021.set_index('Date', inplace=True)
rates_2021_2023 = pd.concat([rates_2022_2023, rates_2021], ignore_index=False)

# 2020

csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2020/all?field_tdr_date_value=2020&type=daily_treasury_yield_curve&page&_format=csv'
req = requests.get(csv_url, verify=False)
url_content = req.content
csv_file = open('2020_rates.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
rates_2020 = pd.read_csv('2020_rates.csv')
rates_2020['Date'] = pd.to_datetime(rates_2020['Date'], format='%m/%d/%Y')
# Set the date column as the index
rates_2020.set_index('Date', inplace=True)
rates_2020_2023 = pd.concat([rates_2021_2023, rates_2020], ignore_index=False)

# 2019

csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2019/all?field_tdr_date_value=2019&type=daily_treasury_yield_curve&page&_format=csv'
req = requests.get(csv_url, verify=False)
url_content = req.content
csv_file = open('2019_rates.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
rates_2019 = pd.read_csv('2019_rates.csv')
rates_2019['Date'] = pd.to_datetime(rates_2019['Date'], format='%m/%d/%Y')
# Set the date column as the index
rates_2019.set_index('Date', inplace=True)
rates_2019_2023 = pd.concat([rates_2020_2023, rates_2019], ignore_index=False)

# 2018

csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2018/all?field_tdr_date_value=2018&type=daily_treasury_yield_curve&page&_format=csv'
req = requests.get(csv_url, verify=False)
url_content = req.content
csv_file = open('2018_rates.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
rates_2018 = pd.read_csv('2018_rates.csv')
rates_2018['Date'] = pd.to_datetime(rates_2018['Date'], format='%m/%d/%Y')
# Set the date column as the index
rates_2018.set_index('Date', inplace=True)
rates_2018_2023 = pd.concat([rates_2019_2023, rates_2018], ignore_index=False)

# 2017

csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2017/all?field_tdr_date_value=2017&type=daily_treasury_yield_curve&page&_format=csv'
req = requests.get(csv_url, verify=False)
url_content = req.content
csv_file = open('2017_rates.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
rates_2017 = pd.read_csv('2017_rates.csv')
rates_2017['Date'] = pd.to_datetime(rates_2017['Date'], format='%m/%d/%Y')
# Set the date column as the index
rates_2017.set_index('Date', inplace=True)
rates_2017_2023 = pd.concat([rates_2018_2023, rates_2017], ignore_index=False)

# 2016

csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2016/all?field_tdr_date_value=2016&type=daily_treasury_yield_curve&page&_format=csv'
req = requests.get(csv_url, verify=False)
url_content = req.content
csv_file = open('2016_rates.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
rates_2016 = pd.read_csv('2016_rates.csv')
rates_2016['Date'] = pd.to_datetime(rates_2016['Date'], format='%m/%d/%Y')
# Set the date column as the index
rates_2016.set_index('Date', inplace=True)
rates_2016_2023 = pd.concat([rates_2017_2023, rates_2016], ignore_index=False)

# 2015

csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2015/all?field_tdr_date_value=2015&type=daily_treasury_yield_curve&page&_format=csv'
req = requests.get(csv_url, verify=False)
url_content = req.content
csv_file = open('2015_rates.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
rates_2015 = pd.read_csv('2015_rates.csv')
rates_2015['Date'] = pd.to_datetime(rates_2015['Date'], format='%m/%d/%Y')
# Set the date column as the index
rates_2015.set_index('Date', inplace=True)
rates_2015_2023 = pd.concat([rates_2016_2023, rates_2015], ignore_index=False)

# 2014

csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2014/all?field_tdr_date_value=2014&type=daily_treasury_yield_curve&page&_format=csv'
req = requests.get(csv_url, verify=False)
url_content = req.content
csv_file = open('2014_rates.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
rates_2014 = pd.read_csv('2014_rates.csv')
rates_2014['Date'] = pd.to_datetime(rates_2014['Date'], format='%m/%d/%Y')
# Set the date column as the index
rates_2014.set_index('Date', inplace=True)
rates_2014_2023 = pd.concat([rates_2015_2023, rates_2014], ignore_index=False)

rates_2014_2023_2y = rates_2014_2023['2 Yr']
    
#-------------------------------------------------------
# Show the financial markers from the API
#-------------------------------------------------------

# Function to evaluate the status of the marker

def evaluate_status(current_price, historical_df, quantile_percentile=0.33):
    
    # Calculate the rolling quantile based on historical prices
    window_size = len(historical_df)  # Use all historical data
    quantile_value = historical_df.quantile(q=quantile_percentile)

    if current_price < quantile_value:
        return "low"
    elif quantile_value <= current_price <= 2 * quantile_value:
        return "medium"
    else:
        return "high"
#----------------------------------------------------------------------

st.header('‍Financial markers')

            #Calling the API : 

API_url = "http://13.36.215.155/"
json_url = get_response(API_url)
#st.write("## Json {}".format(json_url))
API_data = json_url
API_data_sp = API_data["S&P500 front month index futures prices"]
API_data_10y_futures = API_data["10-year US Treasuries futures prices"]
API_data_3m_rate = API_data["US dollar 3-month interest rate"]
API_data_2y_rate = API_data["US dollar 2-year interest rate"]
API_data_10y_rate = API_data["US dollar 10-year interest rate"]
API_data_vix = API_data["VIX Index"]
API_data_10y_bund = API_data["10-year German Bund price"]

# Show the data and status of S&P500 front month index futures prices
st.write('S&P500 front month index futures prices:')
st.write(API_data_sp)
# Evaluate the status of the current price
status_of_current_price = evaluate_status(API_data_sp, prices_SP)
# Print the status
#st.write('Status:', status_of_current_price)
st.write(f"<span style='color:red'>Status: {status_of_current_price}</span>", unsafe_allow_html=True)


# Show the data and status of 10-year US Treasuries futures prices
st.write('10-year US Treasuries futures prices:')
st.write(API_data_10y_futures)
# Evaluate the status of the current price
status_of_current_price = evaluate_status(API_data_10y_futures, prices_10y_futures)
# Print the status
#st.write('Status:', status_of_current_price)
st.write(f"<span style='color:red'>Status: {status_of_current_price}</span>", unsafe_allow_html=True)

# Show the data and status of US dollar 3-month interest rate
st.write('US dollar 3-month interest rate:')
st.write(API_data_3m_rate)
# Evaluate the status of the current price
status_of_current_price = evaluate_status(API_data_3m_rate, prices_3m_interest)
# Print the status
#st.write('Status:', status_of_current_price)
st.write(f"<span style='color:red'>Status: {status_of_current_price}</span>", unsafe_allow_html=True)

# Show the data and status of US dollar 2-year interest rate
st.write('US dollar 2-year interest rate:')
st.write(API_data_2y_rate)
# Evaluate the status of the current price
status_of_current_price = evaluate_status(API_data_2y_rate, rates_2014_2023_2y)
# Print the status
#st.write('Status:', status_of_current_price)
st.write(f"<span style='color:red'>Status: {status_of_current_price}</span>", unsafe_allow_html=True)

# Show the data and status of US dollar 10-year interest rate
st.write('US dollar 10-year interest rate:')
st.write(API_data_10y_rate)
# Evaluate the status of the current price
status_of_current_price = evaluate_status(API_data_10y_rate, prices_10y_interest)
# Print the status
#st.write('Status:', status_of_current_price)
st.write(f"<span style='color:red'>Status: {status_of_current_price}</span>", unsafe_allow_html=True)

# Show the data and status of VIX Index
st.write('VIX Index:')
st.write(API_data_10y_rate)
# Evaluate the status of the current price
status_of_current_price = evaluate_status(API_data_vix, prices_vix_index)
# Print the status
#st.write('Status:', status_of_current_price)
st.write(f"<span style='color:red'>Status: {status_of_current_price}</span>", unsafe_allow_html=True)

st.write('10-year German Bund price:')
st.write(API_data["10-year German Bund price"])

#----------------------------------------------------------------
# Show the plot for 1 year historical prices for the SP500 index
#-----------------------------------------------------------------

st.header('‍Evolution of the S&P 500 index')

# Select the time range
number_sp = st.selectbox('Select the evolution time range in months (S&P 500)', [120, 60, 36, 12, 6, 3, 1])
days_sp = int((number_sp / 12) * 252)

fig, ax = plt.subplots()
prices_SP[-days_sp:].plot(ax=ax)
plt.ylabel('S&P 500 index')
plt.xlabel('Date')
st.pyplot(fig)
          
#-----------------------------------------------------------------------------------------
# Show the plot for 1 year historical prices for the 10-year US Treasuries futures prices
#-----------------------------------------------------------------------------------------

st.header('‍Evolution of the 10-year US Treasuries futures prices')

# Select the time range
number_10f = st.selectbox('Select the evolution time range in months (10-year Futures)', [6, 3, 1])
days_10f = int((number_10f / 12) * 252)

fig, ax = plt.subplots()
prices_10y_futures[-days_10f:].plot(ax=ax)
plt.ylabel('10-year US Treasuries futures prices')
plt.xlabel('Date')
st.pyplot(fig)
                   
#-----------------------------------------------------------------------------------------
# Show the plot for 1 year historical prices for the US dollar 3-month interest rate
#-----------------------------------------------------------------------------------------

st.header('‍Evolution of the US dollar 3-month interest rate')

# Select the time range
number_3mr = st.selectbox('Select the evolution time range in months (3-month Rate)', [120, 60, 36, 12, 6, 3, 1])
days_3mr = int((number_3mr / 12) * 252)

fig, ax = plt.subplots()
prices_3m_interest[-days_3mr:].plot(ax=ax)
plt.ylabel('US dollar 3-month interest rate')
plt.xlabel('Date')
st.pyplot(fig)
          
#-----------------------------------------------------------------------------------------
# Show the plot for 1 year historical prices for the US dollar 10-year interest rate
#-----------------------------------------------------------------------------------------

st.header('‍Evolution of the US dollar 10-year interest rate')

# Select the time range
number_10yr = st.selectbox('Select the evolution time range in months (10-year Rate)', [120, 60, 36, 12, 6, 3, 1])
days_10yr = int((number_10yr / 12) * 252)

fig, ax = plt.subplots()
prices_10y_interest[-days_10yr:].plot(ax=ax)
plt.ylabel('US dollar 10-year interest rate')
plt.xlabel('Date')
st.pyplot(fig)
          
#-----------------------------------------------------------------------------------------
# Show the plot for 1 year historical prices for the VIX Index
#-----------------------------------------------------------------------------------------

st.header('‍Evolution of the VIX Index')

# Select the time range
number_vix = st.selectbox('Select the evolution time range in months (VIX Index)', [120, 60, 36, 12, 6, 3, 1])
days_vix = int((number_vix / 12) * 252)

fig, ax = plt.subplots()
prices_vix_index[-days_vix:].plot(ax=ax)
plt.ylabel('VIX Index')
plt.xlabel('Date')
st.pyplot(fig)
     
#-----------------------------------------------------------------------------------------
# Show the plot for 1 year historical prices for the US dollar 2-year interest rate
#-----------------------------------------------------------------------------------------

st.header('‍Evolution of the US dollar 2-year interest rate')

# Select the time range
number_2yr = st.selectbox('Select the evolution time range in months (2-year Rate)', [120, 60, 36, 12, 6, 3, 1])
days_2yr = int((number_2yr / 12) * 252)

fig, ax = plt.subplots()
rates_2014_2023_2y[:days_2yr].plot(ax=ax)
plt.ylabel('US dollar 2-year interest rate')
plt.xlabel('Date')
st.pyplot(fig)

#--------------------------------------------------------------------------------------------------------
# Show the plot for 1 year historical prices for the Spread between 2-year and 3-month US interest rates
#--------------------------------------------------------------------------------------------------------
prices_10y_interest.index = prices_10y_interest.index.date
difference_10year_2year = prices_10y_interest - rates_2014_2023_2y

st.header('‍The difference between the 10-year and 2-year US dollar interest rates')
fig, ax = plt.subplots()
difference_10year_2year.plot(ax=ax, label='The difference between the 10-year and 2-year US dollar interest rates')
plt.xlabel('Date')
ax.legend()
st.pyplot(fig)

#--------------------------------------------------------------------------------------------------------
# Show the plot for 1 year historical prices for the Spread between 10-year and 2-year US interest rates
#--------------------------------------------------------------------------------------------------------
prices_3m_interest.index = prices_3m_interest.index.date
difference_2year_3month = rates_2014_2023_2y - prices_3m_interest

st.header('‍The difference between the 2-year and 3-month US dollar interest rates')
fig, ax = plt.subplots()
difference_2year_3month.plot(ax=ax, label='The difference between the 2-year and 3-month US dollar interest rates')
plt.xlabel('Date')
ax.legend()
st.pyplot(fig)
          

#streamlit run streamlit_app.py
