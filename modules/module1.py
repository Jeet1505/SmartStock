"""
Author       : Jeet
Date         : 2025-03-17
Version      : 2.1 (Alpha Vantage Edition)
Description  : AI Investment Agent to compare stock performance using Alpha Vantage API and generate a PDF report.
"""

import streamlit as st
import json
import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from dotenv import load_dotenv

# Load API key
load_dotenv()
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")

# Constants
CACHE_FILE = "stock_cache.json"

def run():
    st.header("📊 Stock Comparison Tool (Alpha Vantage)")
    st.caption("Compare stock performance using Alpha Vantage. Generate PDF reports.")

    stock1 = st.text_input("Enter first stock symbol (e.g., AAPL)")
    stock2 = st.text_input("Enter second stock symbol (e.g., MSFT)")

    if stock1 and stock2:
        data1 = get_stock_information(stock1.upper())
        data2 = get_stock_information(stock2.upper())

        if not data1 or not data2:
            st.error("Failed to retrieve data for one or both stocks.")
        else:
            st.subheader(f"Comparison: {stock1.upper()} vs {stock2.upper()}")
            st.write(data1)
            st.write(data2)

            pdf_path = create_pdf_report(data1, data2)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF Report", f, file_name="stock_comparison_alpha.pdf")

def get_stock_information(symbol):
    """Fetch stock data from Alpha Vantage."""
    if not ALPHA_API_KEY:
        st.error("Alpha Vantage API key not found. Set it in the .env file.")
        return None

    cache_data = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            try:
                cache_data = json.load(file)
            except json.JSONDecodeError:
                cache_data = {}

    if symbol in cache_data:
        return cache_data[symbol]

    try:
        quote_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_API_KEY}"
        overview_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_API_KEY}"

        quote_data = requests.get(quote_url).json().get("Global Quote", {})
        overview_data = requests.get(overview_url).json()

        if not quote_data or "01. symbol" not in quote_data:
            raise ValueError("Invalid stock symbol or no data available")

        stock_data = {
            "Name": overview_data.get("Name", "N/A"),
            "Symbol": symbol,
            "Market Cap": f"${round(float(overview_data.get('MarketCapitalization', 0)) / 1e9, 2)} Billion",
            "Current Price": f"${quote_data.get('05. price', 'N/A')}",
            "52-Week High": f"${overview_data.get('52WeekHigh', 'N/A')}",
            "52-Week Low": f"${overview_data.get('52WeekLow', 'N/A')}"
        }

        cache_data[symbol] = stock_data
        with open(CACHE_FILE, "w") as file:
            json.dump(cache_data, file)

        return stock_data

    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

def create_pdf_report(stock1, stock2, filename="stock_comparison_alpha.pdf"):
    file_path = os.path.join(os.getcwd(), filename)
    pdf = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Stock Comparison Report (Alpha Vantage)", styles['h1']))
    story.append(Spacer(1, 12))

    for stock in [stock1, stock2]:
        story.append(Paragraph(f"Stock: {stock.get('Name')} ({stock.get('Symbol')})", styles['h2']))
        for key, value in stock.items():
            if key != "Symbol":
                story.append(Paragraph(f"{key}: {value}", styles['Normal']))
        story.append(Spacer(1, 12))

    pdf.build(story)
    return file_path
