import assets.functions as run
from typing import Any

from selenium import webdriver

import pandas as pd

import os
import time

# variables 0
url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/?language=pt-br' 
search_url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br' 
driver_wait_time = 2

# variables 1
app_folder = 'datasets/'
cols_b3_companies = ['pregao', 'company_name', 'cvm', 'listagem', 'ticker', 'tickers', 'asin', 'cnpj', 'site', 'setor', 'subsetor', 'segmento', 'atividade', 'escriturador', 'url']
cols_b3_tickers = ['ticker', 'company_name']
cols_world_markets = ['symbol', 'shortName', 'longName', 'exchange', 'market', 'quoteType']
cols_yahoo = {'symbol': 'str', 'shortName': 'str', 'longName': 'str', 'exchange': 'category', 'market': 'category', 'quoteType': 'category', 'ticker': 'str', 'exchange_y': 'category', 'tick_y': 'str', 'tick': 'str'}
cols_info = ['symbol', 'shortName', 'longName', 'longBusinessSummary', 'exchange', 'quoteType', 'market', 'sector', 'industry', 'website', 'logo_url', 'country', 'state', 'city', 'address1', 'phone', 'returnOnEquity', 'beta3Year', 'beta', 'recommendationKey', 'recommendationMean']
cols_nsd = ['company', 'dri', 'dri2', 'dre', 'data', 'versao', 'auditor', 'auditor_rt', 'cancelamento', 'protocolo', 'envio', 'url', 'nsd']
cols_dre = ['Companhia', 'Trimestre', 'Demonstrativo', 'Conta', 'Descrição', 'Valor','Url']

# variables 2
driver = wait = None

def set_driver_and_wait(new_driver, new_wait):
    global driver, wait
    driver = new_driver
    wait = new_wait

# variables 3
local_path = os.curdir + '/'
data_path = local_path + app_folder
data_path = run.check_or_create_folder(data_path)
# raw_data_path = data_path + 'raw/'
# raw_data_path = run.check_or_create_folder(raw_data_path)

# google cloud storage gcs
json_key_file = 'credentials\storage admin.json'
bucket_name = 'b3_bovespa_bucket'


# system stages
def update_b3_companies(value: str) -> str:
    """
    Update missing companies from the provided dataframe by searching the web using the provided driver and wait object.

    Args:
    - value: Any, initial value
    - driver: WebDriver, instance of the web driver
    - wait: Any, instance of the wait object

    Returns:
    - str: status message
    """

    # run browser
    driver, wait = run.load_browser()

    try:
        # Get the total number of companies and pages
        driver.get(search_url)
        batch = run.wSelect(f'//*[@id="selectPage"]', driver, wait)
        companies = run.wText(f'//*[@id="divContainerIframeB3"]/form/div[1]/div/div/div[1]/p/span[1]', wait)
        companies = int(companies.replace('.',''))
        pages = int(companies/batch)

        value = f'found {companies} companies in {pages+1} pages'
        print(value)

        # Get all available companies directly from the web
        df_name = 'b3_tickers'
        b3_tickers = run.read_or_create_dataframe(df_name, cols_b3_companies)

        for page in range(0, pages+1):
            driver.get(search_url)
            time.sleep(1)
            run.wSelect(f'//*[@id="selectPage"]', driver, wait)

            click = 0
            while click-1 < page-1:
                run.wClick(f'//*[@id="listing_pagination"]/pagination-template/ul/li[10]/a', wait)
                time.sleep(0.5)
                click += 1
            value = f'page {page}, clique {click}'
            # raw_code_xpath = '//*[@id="nav-bloco"]/div'
            time.sleep(1)

            for item in range(0, batch):
                ticker = run.wText(f'//*[@id="nav-bloco"]/div/div[{item+1}]/div/div/h5', wait)
                company_name = run.txt_cln(run.wText(f'//*[@id="nav-bloco"]/div/div[{item+1}]/div/div/p[1]', wait))
                keyword = [ticker, company_name]
                b3_tickers = pd.concat([b3_tickers, pd.DataFrame([keyword], columns=cols_b3_tickers)])
                progress = ((page*batch+item+1)/companies)*100
                progress = format(progress, '.2f') + '%'
                value = f'página {page+1}/{pages+1}, item {item+1}/{batch}, total {page*batch+item+1}/{companies}, {progress}, ["{ticker} {company_name}"]'
                print(value)
                if page*batch+item+2 == companies:
                    break 

        # Drop any duplicate values in the b3_tickers dataframe
        b3_tickers.drop_duplicates(inplace=True)

        # Update the missing companies from the database
        df_name = 'b3_companies'
        b3_companies = run.read_or_create_dataframe(df_name, cols_b3_companies)
        b3_keywords = []

        # Create a list of all current companies in the b3_companies dataframe
        for index, row in b3_companies.iterrows():
            try:
                b3_keywords.append(' '.join([str(row['ticker']), str(row['company_name'])]))
            except Exception as e:
                print(row)
                pass

        counter = 0
        size = len(b3_tickers)

        # Loop through each company in the b3_tickers dataframe
        for index, row in b3_tickers.iterrows():
            counter +=1
            keyword = str(row['ticker']) + ' ' + str(row['company_name'])
            if keyword not in b3_keywords:
                driver.get(url)

                keyword = run.wSendKeys(f'//*[@id="keyword"]', keyword, wait)
                keyword = run.wClick(f'//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div/div[3]/button', wait)

                company = run.get_company(1, driver, wait)
                b3_companies = pd.concat([b3_companies, pd.DataFrame([company], columns=cols_b3_companies)])

                print(counter, size-counter, company)
            else:
                print(counter, size-counter, keyword)

            break
        b3_companies.drop_duplicates(inplace=True)
        
        b3_companies = run.save_and_pickle(b3_companies, df_name)
        # b3_companies.to_pickle(data_path + f'{df_name}.zip')

        # Close the driver and exit the script
        driver.close()
        driver.quit()

        value = f'{len(b3_companies)} companies updated'
        print(value)



    except Exception as e:
        value = str(e) + value
    return value
           
