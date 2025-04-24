"""
Author       : Jeet
Date         : 2025-03-17
Version      : 2.0 (Finnhub Edition)
Description  : AI Investment Agent to compare stock performance using Finnhub API and generate a PDF report.
"""

import streamlit as st
import json
import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Constants
CACHE_FILE = "stock_cache_finnhub.json"
from dotenv import load_dotenv
load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


# Streamlit UI Initialization
st.title("AI Investment Agent 📊 (Finnhub Edition)")
st.caption("Compare stock performance using financial data. Generates PDF reports.")

def get_stock_information(symbol, api_key):
    """
    Fetch stock data from Finnhub API.
    """
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
        # Get stock quote
        quote_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
        profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={api_key}"

        quote_res = requests.get(quote_url)
        profile_res = requests.get(profile_url)

        quote_data = quote_res.json()
        profile_data = profile_res.json()

        if "name" not in profile_data:
            raise ValueError("Invalid stock symbol or no data available")

        stock_data = {
            "Name": profile_data.get("name", "N/A"),
            "Symbol": symbol,
            "Market Cap": f"${profile_data.get('marketCapitalization', 'N/A')} Billion",
            "Current Price": f"${quote_data.get('c', 'N/A')}",
            "52-Week High": f"${quote_data.get('h', 'N/A')}",
            "52-Week Low": f"${quote_data.get('l', 'N/A')}"
        }

        cache_data[symbol] = stock_data
        with open(CACHE_FILE, "w") as file:
            json.dump(cache_data, file)

        return stock_data

    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None


def create_pdf_report(stock1, stock2, filename="stock_comparison_finnhub.pdf"):
    file_path = os.path.join(os.getcwd(), filename)
    pdf = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Stock Comparison Report (Finnhub)", styles['h1']))
    story.append(Spacer(1, 12))

    for stock in [stock1, stock2]:
        story.append(Paragraph(f"Stock: {stock.get('Name')} ({stock.get('Symbol')})", styles['h2']))
        for key, value in stock.items():
            if key != "Symbol":
                story.append(Paragraph(f"{key}: {value}", styles['Normal']))
        story.append(Spacer(1, 12))

    pdf.build(story)
    return file_path

#main app module
def run_module_1():
    """
    Run the Stock Comparison Module.
    """
    if FINNHUB_API_KEY:
        stock1 = st.text_input("Enter first stock symbol (e.g., AAPL)")
        stock2 = st.text_input("Enter second stock symbol (e.g., MSFT)")

        if stock1 and stock2:
            data1 = get_stock_information(stock1.upper(), FINNHUB_API_KEY)
            data2 = get_stock_information(stock2.upper(), FINNHUB_API_KEY)

            if not data1 or not data2:
                st.error("Failed to retrieve data for one or both stocks.")
            else:
                st.subheader(f"Comparison: {stock1.upper()} vs {stock2.upper()}")
                st.write(data1)
                st.write(data2)

                pdf_path = create_pdf_report(data1, data2)
                with open(pdf_path, "rb") as f:
                    st.download_button("Download PDF Report", f, file_name="stock_comparison_finnhub.pdf")
    else:
        st.warning("Please enter your Finnhub API Key.")