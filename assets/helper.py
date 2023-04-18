import assets.functions as run
from typing import Any

from selenium import webdriver

import pandas as pd

import os
import time
import datetime

# variables 0
url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/?language=pt-br' 
search_url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br' 
start = 1
batch = 120
bins = 20
bin_size = 50
chunksize = 10**6  # Adjust this value based on your available memory

# variables 1
app_folder = 'datasets/'
cols_b3_companies = ['pregao', 'company_name', 'cvm', 'listagem', 'ticker', 'tickers', 'asin', 'cnpj', 'site', 'setor', 'subsetor', 'segmento', 'atividade', 'escriturador', 'url']
cols_b3_tickers = ['ticker', 'company_name']
cols_world_markets = ['symbol', 'shortName', 'longName', 'exchange', 'market', 'quoteType']
cols_yahoo = {'symbol': 'str', 'shortName': 'str', 'longName': 'str', 'exchange': 'category', 'market': 'category', 'quoteType': 'category', 'ticker': 'str', 'exchange_y': 'category', 'tick_y': 'str', 'tick': 'str'}
cols_info = ['symbol', 'shortName', 'longName', 'longBusinessSummary', 'exchange', 'quoteType', 'market', 'sector', 'industry', 'website', 'logo_url', 'country', 'state', 'city', 'address1', 'phone', 'returnOnEquity', 'beta3Year', 'beta', 'recommendationKey', 'recommendationMean']
cols_cotahist = ['TICKER', 'tick', 'Symbol', 'Symbol Type', 'Exchange', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close', 'Dividends', 'Stock Splits']
# cols_cotahist = ['Date', 'open', 'high', 'low', 'close', 'volume', 'adjusted close', 'dividend amount', 'split coefficient']
cols_cotahist = ['company', 'symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Dividends', 'Stock Splits']
company_info_cols = ['market', 'sector', 'industry', 'country', 'state', 'city', 'zip', 'quoteType', 'exchange', 'financialCurrency', 'symbol', 'shortName', 'longName', 'longBusinessSummary', 'currency', 'recommendationKey', 'recommendationMean', 'fullTimeEmployees', 'website', 'logo_url', 'address1', 'address2', 'phone']
cols_nsd = ['company', 'dri', 'dri2', 'dre', 'data', 'versao', 'auditor', 'auditor_rt', 'cancelamento', 'protocolo', 'envio', 'url', 'nsd']
cols_dre = ['Companhia', 'Trimestre', 'Demonstrativo', 'Conta', 'Descrição', 'Valor','Url']
cols_dre_math = ['Companhia', 'Trimestre', 'Demonstrativo', 'Conta', 'Descrição', 'Valor', 'Url', 'nsd']
cols_all =  cols_b3_companies + company_info_cols + cols_cotahist + cols_dre

# Remove specific elements from the list using list comprehension
to_move = ['Companhia', 'Trimestre', 'Date', 'ticker']
cols_all = [col for col in cols_all if col not in to_move]
cols_all = to_move + cols_all

demo = ['Demonstrações Financeiras Padronizadas', 'Informações Trimestrais']
cmbGrupo = ['Dados da Empresa']
cmbQuadro = ['Demonstração do Resultado', 'Balanço Patrimonial Ativo', 'Balanço Patrimonial Passivo', 'Demonstração do Fluxo de Caixa', 'Demonstração de Valor Adicionado', 'Demonstração do Resultado Abrangente']

last_quarters = ['3', '4']
all_quarters = ['6', '7']


# dre new columns
fsdemo = 'FS_Demonstrativo'
fsdesc = 'FS_Descrição'
fscol = 'FS_Conta'
fsval = 'FS_Valor'

columns = ['Companhia', 'Trimestre', 'Demonstrativo', 'Conta', 'Descrição', 'Valor', 'Url', 'nsd', 'demosheet']
columns = ['Companhia', 'Trimestre', 'Demonstrativo', 'Conta', 'Descrição', 'Valor', 'Url', 'nsd']


# variables 2
driver_wait_time = 2
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
        driver.get(search_url)
        time.sleep(1)
        run.wSelect(f'//*[@id="selectPage"]', driver, wait)
        raw_code = []
        for page in range(0, pages+1):
            xpath = '//*[@id="nav-bloco"]/div'
            inner_html = run.wRaw(xpath, wait)
            raw_code.append(inner_html)
            run.wClick(f'//*[@id="listing_pagination"]/pagination-template/ul/li[10]/a', wait)
            time.sleep(0.5)
            value = f'page {page+1}'
            print(value)
        b3_tickers = run.get_ticker_keywords(raw_code)

        # Update the missing companies from the database
        file_name = df_name = 'b3_companies'
        b3_companies = run.read_or_create_dataframe(df_name, cols_b3_companies)
        b3_keywords = []

        # Create a list of all current companies in the b3_companies dataframe
        for index, row in b3_companies.iterrows():
            try:
                b3_keywords.append(' '.join([str(row['ticker']), str(row['company_name'])]))
            except Exception as e:
                print(row)
                pass

        size = len(b3_tickers)

        # Loop through each company in the b3_tickers dataframe
        avpi = []
        start_time = time.time()
        for i, row in b3_tickers.iterrows():
            progress = run.remaining_time(start_time, size, i)
            avpi.append(progress.split(',')[3])
            pd.DataFrame(avpi).to_csv(app_folder + file_name + '.csv', index=False)
            
            keyword = str(row['ticker']) + ' ' + str(row['company_name'])
            if keyword not in b3_keywords:
                driver.get(url)

                keyword = run.wSendKeys(f'//*[@id="keyword"]', keyword, wait)
                keyword = run.wClick(f'//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div/div[3]/button', wait)

                company = run.get_company(1, driver, wait)
                b3_companies = pd.concat([b3_companies, pd.DataFrame([company], columns=cols_b3_companies)])

                print(f'{progress}, {company}')
                if (size - i -1) % (bin_size) == 0:
                    b3_companies.fillna('', inplace=True)
                    b3_companies.reset_index(drop=True, inplace=True)
                    b3_companies.drop_duplicates(inplace=True)
                    
                    b3_companies = run.save_and_pickle(b3_companies, df_name)
                    print(f'partial save')
            else:
                print(f'{progress}, {keyword}')
        b3_companies.fillna('', inplace=True)
        b3_companies.reset_index(drop=True, inplace=True)
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
           
def update_world_markets(value):
  """
  Updates the world markets data and saves it as a compressed pickle file.

  Args:
  value (str): A string value to be appended with "done".

  Returns:
  str: A string value appended with "done" to indicate the completion of the function.

  """
  # world stock symbols - https://polygon.io/stocks
  # cols = ['market', 'abbreviation', 'totalCount', 'lastUpdated', 'index']
  import credentials.keys
  from stocksymbol import StockSymbol

  # world markets
  ss = StockSymbol(credentials.keys.polygon)
  world_markets = pd.DataFrame(ss.market_list)
  index = pd.DataFrame(ss.index_list)

  world_markets.drop(labels='index', axis=1, inplace=True)

  world_markets = pd.merge(index, world_markets, how='outer')
  world_markets = world_markets[['market', 'abbreviation', 'totalCount', 'lastUpdated', 'indexName', 'indexId']]
  world_markets.fillna('', inplace=True)

  # world_markets[['market', 'abbreviation']] = world_markets[['market', 'abbreviation']].apply(run.txt_cln)
  world_markets = world_markets.sort_values(by=['market','indexName'])

  try:
    abbreviation = world_markets['abbreviation'].unique()
  except Exception as e:
    abbreviation = []

  file_name = df_name = 'world_markets'
  world_markets = pd.DataFrame(columns=cols_world_markets)

  avpi = []
  start_time = time.time()
  size = len(abbreviation)
  # world companies
  for index, abbrv in enumerate(abbreviation):
    progress = run.remaining_time(start_time, size, index)
    avpi.append(progress.split(',')[3])
    pd.DataFrame(avpi).to_csv(app_folder + file_name + '.csv', index=False)
    try:
      df = pd.DataFrame(ss.get_symbol_list(market=abbrv)) # "us" or "america" will also work
      world_markets = pd.concat([world_markets, df], ignore_index=True)
      print(f'{progress}, {abbrv}, {len(df)} new, {len(world_markets)} total companies')
    except Exception as e:
      pass

  world_markets = world_markets.copy()
  world_markets['market'] = world_markets['market'].map(lambda x: x.replace('_market', ''))
  world_markets.fillna('', inplace=True)
  world_markets.drop_duplicates(inplace=True)
  
  # expand sufixes
  world_markets[['ticker', 'exchange_country']] = world_markets['symbol'].str.split('.', expand=True)
  world_markets['ticker_type'] = ''

  # expand Brazil Ticker Sufixes
  mask = (world_markets['market'] == 'br')
  br_world_markets = world_markets[mask]

  # adjustments
  br_world_markets.loc[:, 'ticker_type'] = br_world_markets['ticker'].str[4:]
  br_world_markets = br_world_markets.copy()
  br_world_markets['ticker'] = br_world_markets['ticker'].str[:4]

  world_markets = pd.merge(world_markets, br_world_markets, how='left')
  world_markets.fillna('', inplace=True)

  # Save
  world_markets = run.save_and_pickle(world_markets, df_name)

  return value

def yahoo_cotahist(value):
    # import yfinance as yf

    # df_name = 'world_companies'
    # world_companies = run.read_or_create_dataframe(df_name, cols_world_markets)

    # df_name = 'company_info'
    # company_info = run.read_or_create_dataframe(df_name, cols_info)

    # c_info = pd.DataFrame(columns=cols_info)

    # # filter missing companies
    # mask = world_companies['symbol'].isin(company_info['symbol'].unique())
    # downloaded_companies = world_companies[mask]
    # missing_companies = world_companies[~mask]

    # for c, company in enumerate(missing_companies.itertuples()):
    #   downloaded = (len(downloaded_companies)+c+1)
    #   print(f'{downloaded} {len(missing_companies)-(c+1)} of {len(world_companies)} {downloaded/len(world_companies):.4%} {company[5]} {company[4]}:{company[1]} {company[3]}')
    #   ticker  = yf.Ticker(company[1])
    #   try:
    #     c_info2 = pd.DataFrame([ticker.info])
    #     c_info2['symbol'] = company[1]
    #     c_info = pd.concat([c_info, c_info2], ignore_index=True)
    #   except Exception as e:
    #     pass

    # if (downloaded) % varsys.bin_size == 0:
    #   if not c_info.empty:
    #     # load
    #     company_info = pd.read_pickle(varsys.data_path + f'{df_name}.zip')

    #     # save
    #     try:
    #       company_info = pd.concat([company_info, c_info], ignore_index=True)

    #       try:
    #         company_info = company_info.drop(['companyOfficers'], axis=1, errors='ignore')
    #         company_info.drop_duplicates(inplace=True)
    #       except Exception as e:
    #         pass
            
    #       company_info.to_pickle(varsys.data_path + f'{df_name}.zip')

    #       company_info = pd.DataFrame(columns=cols_info)
    #       c_info = pd.DataFrame(columns=cols_info)

    #       print(f'partial save')
    #     except Exception as e:
    #       print(e)

    # # final save
    # company_info = pd.concat([company_info, c_info], ignore_index=True)
    # company_info.sort_values(by=['market', 'exchange', 'quoteType', 'sector', 'industry', 'symbol'], inplace=True)

    # try:
    #   company_info = company_info.drop(['companyOfficers'], axis=1, errors='ignore')
    #   company_info.drop_duplicates(inplace=True)
    # except Exception as e:
    #   pass

    # company_info.to_pickle(varsys.data_path + f'{df_name}.zip')

    # company_info = pd.DataFrame(columns=cols_info)
    # c_info = pd.DataFrame(columns=cols_info)

    value='please refactor using yahooquery, nothing done here'
    return value

import pandas as pd
import datetime
import time
import itertools
from alpha_vantage.timeseries import TimeSeries
import credentials.keys

def historical_quotes(value):
    # Create an API key rotator
    alpha_vantage = credentials.keys.alpha_vantage
    api_key_rotator = itertools.cycle(alpha_vantage)

    def get_api_key():
        key = next(api_key_rotator)
        return key

    file_name = 'world_markets'
    world_markets = run.read_or_create_dataframe(file_name, cols_world_markets)
    file_name = 'cotahist'
    cotahist = run.read_or_create_dataframe(file_name, cols_cotahist)
    file_name = 'b3_companies'
    b3_companies = run.read_or_create_dataframe(file_name, cols_b3_companies)
    ticker_pairs = [(pregao, ticker.strip()) for i, pregao in b3_companies['pregao'].items() for ticker in str(b3_companies.loc[i, 'tickers']).split('/') if ticker]

    def get_alpha_vantage_data(pregao, ticker):
        # Initialize the TimeSeries object with the first API key
        api_key = get_api_key()
        try:
            ts = TimeSeries(key=api_key, output_format='pandas')
            data, metadata = ts.get_daily_adjusted(ticker, outputsize='full')
            data.reset_index(inplace=True)
            data.columns = cols_cotahist[2:]
            # data['symbol'] = ticker
            data.insert(0, 'company', pregao)
            data.insert(1, 'symbol', ticker)
        except Exception as e:
            data = pd.DataFrame()
            print(f'failed {api_key} {pregao} {ticker}')
            pass
        return data, api_key

    size = len(ticker_pairs)
    start_time = time.time()
    # Perform the main loop and download required data
    for i, ticker in enumerate(ticker_pairs):
        pregao = ticker[0]
        ticker = ticker[1] + '.SAO'
        progress = run.remaining_time(start_time, size, i)

        try:
            data, key = get_alpha_vantage_data(pregao, ticker)
            cotahist = pd.concat([cotahist, data], ignore_index=True).drop_duplicates()
            file_name = 'cotahist'
            cotahist = run.save_and_pickle(cotahist, file_name)
            print(f'{progress}, {key} {pregao} {ticker}')
        except Exception as e:
            print(f'{key} {pregao} {ticker} failed')
            pass
        time.sleep(2)

    return value


def get_nsd_links(value):
    safety_factor = 1.8

    gap = 0

    file_name = 'nsd_links'
    cols_nsd = ['company', 'dri', 'dri2', 'dre', 'data', 'versao', 'auditor', 'auditor_rt', 'cancelamento', 'protocolo', 'envio', 'url', 'nsd']
    nsd = run.read_or_create_dataframe(file_name, cols_nsd)
    nsd['envio'] = pd.to_datetime(nsd['envio'], dayfirst=True)

    start, end = run.nsd_range(nsd, safety_factor)
    print(f'from {start} to {end}')

    avpi = []
    start_time = time.time()
    size = (end-start)
    for i, n in enumerate(range(start, end)):
        progress = run.remaining_time(start_time, size, i)
        avpi.append(progress.split(',')[3])
        pd.DataFrame(avpi).to_csv(app_folder + file_name + '.csv', index=False)
        # interrupt conditions
        last_date, limit_date, max_gap = run.nsd_dates(nsd, safety_factor)
        if last_date > limit_date:
            if gap == max_gap:
                break

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            # add nsd row to dataframe
            row = run.get_nsd(n)
            nsd = pd.concat([nsd, pd.DataFrame([row], columns=cols_nsd)])
            print(f'{progress}, {row[-1]}, {row[10]}, {row[4]}, {row[3]}, {row[0]}')
            # reset gap
            gap = 0
        except Exception as e:
            # increase gap count
            gap += 1
            print(progress, n)

        if (n-1) % bin_size == 0:
            nsd = run.save_and_pickle(nsd, file_name)
            print('partial save')

    nsd = run.save_and_pickle(nsd, file_name)
    print('final save')


    return value

def get_dre(value):
  # download new dre from nsd list
  file_name = f'dre_raw'
  dre = run.read_or_create_dataframe(file_name, cols_dre)
  df = pd.DataFrame(columns=cols_dre)

  # get new nsd links to download not yet downloaded in dre
  nsd = run.get_new_dre_links(dre)

  driver, wait = run.load_browser()

  size = len(nsd)
  start_time = time.time()
  for l, line in enumerate(nsd.itertuples()):
    progress = run.remaining_time(start_time, size, l)

    # read and concat quarters from nsd (and all dre in each quarter)
    quarter = run.read_quarter(line, driver, wait)
    df = pd.concat([df, quarter], ignore_index=True)

    print(f'{progress}, {run.clean_text(line[1])}, {line[5]}')
    
    if (size-l-1) % (bin_size) == 0:
      dre = pd.concat([dre, df], ignore_index=True)

      dre = run.save_and_pickle(dre, file_name)
      df = pd.DataFrame(columns=cols_dre)
      print('partial save')

  dre['Trimestre'] = pd.to_datetime(dre['Trimestre'], format='%d/%m/%Y')
  dre.sort_values(by=['Companhia', 'Trimestre', 'Url', 'Conta'], ascending=[True, False, True, True], inplace=True)
  dre['Trimestre'] = dre['Trimestre'].dt.strftime('%d/%m/%Y')
  dre.drop_duplicates(inplace=True, keep='last')
  dre = run.save_and_pickle(dre, file_name)
  print('final save')


  return value

def dre_math(value):
  file_name = 'dre_raw'
  dre_raw = run.read_or_create_dataframe(file_name, cols_dre_math)
  dre_raw = run.clean_dre_math(dre_raw)

  file_name = 'dre_math'
  dre_math = run.read_or_create_dataframe(file_name, cols_dre_math)
  dre_math = run.clean_dre_math(dre_math)
  # last company fix
  try:
    dre_math['Companhia'] = dre_math['Companhia'].astype('category').cat.as_ordered()
    dre_math = dre_math[dre_math['Companhia'] != dre_math['Companhia'].max()]
    # print(f"{dre_math['Companhia'].max()} is out!")
  except Exception as e:
     print(e)

  dre_raw, dre_math = run.dre_prepare(dre_raw, dre_math)

  cias, math = run.get_math(dre_raw, dre_math)
  size = len(math)
  print(f'Total of {size} items (items in company quarters) new to process')
  df_temp = pd.DataFrame(columns=cols_dre_math)

  avpi = []
  start_time = time.time()
  for l, key in enumerate(math):
    progress = run.remaining_time(start_time, size, l)
    avpi.append(progress.split(',')[3])

    df, cias, status, key_cia = run.math_magic(key[0], key[1], size, cias, l)
    df_temp = pd.concat([df_temp, df], axis=0, ignore_index=True)

    if (size-l-1) % (bin_size*100) == 0 and status != True:
        pd.DataFrame(avpi).to_csv(app_folder + file_name + '.csv', index=False)

        dre_math = pd.concat([dre_math, df_temp], axis=0, ignore_index=True)
        df_temp = pd.DataFrame(columns=cols_dre_math)

        dre_math.drop_duplicates(inplace=True)
        file_name = 'dre_math'
        dre_math = run.save_and_pickle(dre_math, file_name)
        print(f'partial save {progress} {key_cia[0]} {key_cia[1]}')

  dre_math = pd.concat([dre_math, df_temp], axis=0, ignore_index=True)
  dre_math.drop_duplicates(inplace=True)
  file_name = 'dre_math'
  dre_math = run.save_and_pickle(dre_math, file_name)


  return value

def dre_intel(value):
    # existing dre_math (raw) to be converted by inteligence and then pivoted
    file_name = 'dre_math'
    dre_math = run.read_or_create_dataframe(file_name, cols_dre_math)
    dre_math = run.clean_dre_math(dre_math)
    
    file_name = 'dre_intel'
    dre_intel = run.read_or_create_dataframe(file_name, cols_dre_math)

    # demosheet contains ['Companhia', 'Trimestre']
    ds = ['Companhia', 'Trimestre']

    # get unique ds for dre_math (all ds)
    ds_math = dre_math[ds].drop_duplicates()
    dre_math = run.process_dataframe_trimestre(dre_math)

    # get unique ds for dre_intel (processed ds)
    ds_intel = dre_intel[ds].drop_duplicates()
    dre_intel = run.process_dataframe_trimestre(dre_intel)

    # get unprocessed ds for dre_math (dre_math[~mask]), mask = proccessed ds
    try:
        processed_ds = dre_intel['demosheet']
        mask = dre_math['demosheet'].isin(processed_ds)
        dre_processed = dre_math[mask].drop('demosheet', axis=1)
        dre = dre_math[~mask].drop('demosheet', axis=1)
    except Exception as e:
        dre = dre_math

    # demonstrativos trimestrais padronizados
    demosheet = dre.groupby(ds, group_keys=False)
    size = len(demosheet.groups.keys())
    unique_companies = dre['Companhia'].nunique()
    trimestres_by_company = int(size/unique_companies)
    print(f'{size} DTP únicos, de {unique_companies} Companhias com em média {trimestres_by_company} Trimestres cada')
    
    avpi = []
    start_time = time.time()
    for item, group in enumerate(demosheet):
        progress = run.remaining_time(start_time, size, item)
        avpi.append(progress.split(',')[3])

        df = group[1]
        group = group[0]
        companhia = group[0]
        trimestre = group[1].strftime('%d/%m/%Y')
       
        df1 = run.inteligence_dre(df)
        df2 = run.fundamentalist_dre(df1, group)

        dre_intel = pd.concat([dre_intel.reset_index(drop=True).drop_duplicates(), df2], ignore_index=True)
        print(f'{progress} {df2.shape[0]} {companhia} {trimestre}')

        if (size-item-1) % (bin_size/10) == 0:
            pd.DataFrame(avpi).to_csv(app_folder + file_name + '.csv', index=False)

            dre_intel = dre_intel.astype(str)
            dre_intel = dre_intel.reset_index(drop=True).drop_duplicates().fillna(0)
            dre_intel = run.save_and_pickle(dre_intel, file_name)
            print('partial save')


    dre_intel = dre_intel.reset_index(drop=True).drop_duplicates().fillna(0)
    dre_intel = run.save_and_pickle(dre_intel, file_name)
    print('final save')

    return value

def dre_pivot(value):
    file_name = 'dre_intel'
    dre_intel = run.read_or_create_dataframe(file_name, cols_dre_math)
    dre_intel = run.clean_dre_math(dre_intel)

    dre_intel['CDD'] = dre_intel['Conta'].astype('str') + ' - ' + dre_intel['Descrição'].astype('str') + ' - ' + dre_intel['Demonstrativo'].astype('str')
    groups = dre_intel.groupby(by='Companhia', group_keys=False)

    file_name = 'dre_pivot'
    dre_pivot = run.read_or_create_dataframe(file_name, cols_dre_math)

    avpi = []
    start_time = time.time()
    size = len(groups)

    # groupby intel to transform into pivot
    for item, group in enumerate(groups):
        progress = run.remaining_time(start_time, size, item)
        avpi.append(progress.split(',')[3])
    
        company = group[0]
        group = group[1]
    
        pivot = pd.pivot_table(data=group, index=['Trimestre'], columns=['CDD'], values=['Valor'], aggfunc='max', fill_value=0.0)
        pivot.columns = pivot.columns.droplevel(0)
        pivot['Companhia'] = company
        pivot = pivot.reset_index()
        cols = pivot.columns.to_list()
        cols.insert(0, cols.pop())
        pivot = pivot[cols]

        dre_pivot = pd.concat([dre_pivot, pivot], ignore_index=True)
        print(f'{progress} {company} {group.shape}')
        pd.DataFrame(avpi).to_csv(app_folder + file_name + '.csv', index=False)

    # save
    dre_pivot = run.save_and_pickle(dre_pivot, file_name)
    print('saved')

    return value

def dre_merge(value):
   
    dre_pivot, b3_companies, cotahist, company_info = run.load_and_clean_basic_dfs()

    # part 1 - LOAD CHUNKS
    # Load dre_merge by concat chunks
    file_name = f'dre_merge'
    dre_merge = run.concat_chunks(file_name)
    
    cias = dre_merge['Companhia'].unique().tolist() if 'Companhia' in dre_merge.columns else []
    # get all part files in data folder
    processed_files = [file for file in os.listdir(data_path) if file.startswith(file_name + '_part_') and file.endswith('.zip')]

    # check if the new directory exists, and create it if it does not
    merge_path = f'{data_path}/merged'
    if not os.path.exists(merge_path):
        os.makedirs(merge_path)

    # read each file and concat only new (not in cia) company
    df_temp = []
    df_size = 0
    for i, current_file in enumerate(processed_files):
        print(f'{i+1} {len(processed_files)-(i+1)} {(i+1)/len(processed_files):.2%} {current_file}')
        df = run.read_or_create_dataframe(current_file, cols_dre_math)
        dfs = df['Companhia'].unique()
        for j, company in enumerate(dfs):
            if company not in cias:
                df_company = df[df['Companhia'] == company]
                df_size += df_company.shape[0]
                df_company = df_company.sort_values(by=['Trimestre'], ascending=[True])
                df_company.to_pickle(merge_path + '/' + company + '.zip')
            print(j+1, len(dfs)-j, company, df_company.shape[0], df_size)

    # save df by company
    dre_merge.groupby(['Companhia'])
    # Save in chunks
    dre_merge = run.save_chunks(dre_merge, file_name)

    # part 2 - FILTER NEW dre_pivot

    file_name = f'dre_merge'
    dre_merge = run.concat_chunks(file_name)


    return value
