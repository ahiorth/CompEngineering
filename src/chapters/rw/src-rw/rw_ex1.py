#%%
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
#https://blog.quantinsti.com/random-walk/
# Import the price data of General Motors

# initialize parameters
start_date = datetime(2020, 1, 1)
end_date = datetime(2021, 1, 1)
  
# get the data
data = yf.download('SPY', start = start_date,
                   end = end_date)
#%%
df = yf.download('GM','2008-01-02', '2020-2-27')
df['Adj Close'].plot(figsize=(10,7))
plt.legend()
plt.grid()
plt.show()
df.tail()
# %%

msft = yf.Ticker("MSFT")
# get all stock info
msft.info

# get historical market data
hist = msft.history(period="1mo")

# show meta information about the history (requires history() to be called first)
msft.history_metadata

# %%
