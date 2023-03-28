# Importing required libraries
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import matplotlib as mpl

# Setting user-agent in header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Function collecting data and plotting stock prices


def plot_stock_prices():
    stock_symbol = entry.get()

    # Make a GET request to Yahoo Finance for Apple Inc. historical stock data
    response = requests.get(
        f'https://finance.yahoo.com/quote/{stock_symbol}/history?p={stock_symbol}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the historical stock prices for Apple Inc.
    prices = []
    dates = []
    cols = []
    rows = soup.find_all(
        'tr', {'class': 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'})

    # Display error message if no data available for stock symbol
    if not rows:
        messagebox.showerror("Error", "No data available for stock symbol")
        return

    for i in range(7):
        row = rows[i]
        cols = row.find_all(name='td', class_="Py(10px) Pstart(10px)")
        price = cols[3].text.replace(',', '')
        date_col = row.find_all(
            name='td', class_='Py(10px) Ta(start) Pend(10px)')
        date = date_col[0].text
        prices.append(float(price))
        dates.append(date)

    # Reverse the lists so that the most recent date is at the end
    prices.reverse()
    dates.reverse()

    # Set the custom style using matplotlib
    mpl.rcParams['figure.facecolor'] = '#252422'
    mpl.rcParams['axes.facecolor'] = '#403d39'
    mpl.rcParams['grid.color'] = '#fffcf2'
    mpl.rcParams['xtick.color'] = '#fffcf2'
    mpl.rcParams['ytick.color'] = '#fffcf2'
    mpl.rcParams['text.color'] = '#fffcf2'
    mpl.rcParams['axes.labelcolor'] = '#fffcf2'

    # Create a line chart of the historical stock prices
    plt.clf()
    plt.plot(dates, prices, color='#eb5e28')
    plt.grid()
    plt.title(f'Last 7 Day Close Price For {stock_symbol}')
    plt.xlabel('Date')
    plt.xticks(fontsize=7)
    plt.ylabel('Price ($)')
    plt.show()


# Create a simple GUI with a text entry field and a button
root = tk.Tk()
root.title("Stock Price Plotter")
root.configure(bg='#403d39')
root.geometry('250x100')

# Label text for stock entry field
label = tk.Label(root, text="ENTER STOCK SYMBOL:", bg='#403d39',
                 fg='#fffcf2', font=('Arial', 10, 'bold'))
label.pack(pady=(5, 5))

# Text entry
entry = tk.Entry(root, bg='#fffcf2')
entry.pack()

# Button using plot_stock_price function to collect and plot data
button = tk.Button(root, text="Plot Stock Prices",
                   command=plot_stock_prices, bg='#eb5e28', fg='#fffcf2')
button.pack(pady=(10, 5))

root.mainloop()
