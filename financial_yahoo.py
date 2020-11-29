# %% import necessary modules
import yfinance as yf
import pandas as pd

# %% initialize system's parameters
dataset_period_parameter = '12mo'
dataset_interval_parameter = '1d'
'''
Note: Some companies do not have sufficient "minutely" or "hourly" data. 
Please retrieve data on a "per-day" basis in order to have a 
complete dataset consisting of all valid companies inside the list.  
'''
list_of_types = ['Open', 'High', 'Low', 'Close',
                 'Volume', 'Dividends', 'Stock Splits']
stock_market_type = list_of_types[3]  # 'Close'

# %% load name of companies
with open('load_companies.py') as f_h:
    exec(f_h.read())

# %% create a dataset of stock prices of loaded companies
main_ds = pd.DataFrame()
counter = 0
for a_company_name in set(companies_list[:]):
    counter += 1
    print(f'Downloading info. of the "{a_company_name} (# {counter})" company...')
    a_company = yf.Ticker(a_company_name)
    a_company_history = a_company.history(period=dataset_period_parameter,
                                          interval=dataset_interval_parameter)
    if a_company_history.empty:
        continue
    a_company_stock = a_company_history[stock_market_type]
    try:
        main_ds[a_company_name] = a_company_stock
    except:
        len_main_ds = len(main_ds.index)
        len_current_stock = len(a_company_stock.index)
        if len_current_stock < len_main_ds:
            error_message = 'Downloaded TimeSeries is shorter than expected.'
            raise ValueError(error_message)
        if len_current_stock > len_main_ds:
            print('Warning: Downloaded TimeSeries is longer than expected.\n'
                  'The last valid values are selected into the dataset.')
            a_company_stock = a_company_stock.iloc[len_current_stock-len_main_ds:]
            main_ds[a_company_name] = a_company_stock

# %% save the dataset into a ".csv" file
dataset_name = f'last-{dataset_period_parameter}--int-{dataset_interval_parameter}'
main_ds.to_csv(dataset_name + '.csv')

# %%
