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

# variables 1
app_folder = 'datasets/'
cols_b3_companies = ['pregao', 'company_name', 'cvm', 'listagem', 'ticker', 'tickers', 'asin', 'cnpj', 'site', 'setor', 'subsetor', 'segmento', 'atividade', 'escriturador', 'url']
cols_b3_tickers = ['ticker', 'company_name']
cols_world_markets = ['symbol', 'shortName', 'longName', 'exchange', 'market', 'quoteType']
cols_yahoo = {'symbol': 'str', 'shortName': 'str', 'longName': 'str', 'exchange': 'category', 'market': 'category', 'quoteType': 'category', 'ticker': 'str', 'exchange_y': 'category', 'tick_y': 'str', 'tick': 'str'}
cols_info = ['symbol', 'shortName', 'longName', 'longBusinessSummary', 'exchange', 'quoteType', 'market', 'sector', 'industry', 'website', 'logo_url', 'country', 'state', 'city', 'address1', 'phone', 'returnOnEquity', 'beta3Year', 'beta', 'recommendationKey', 'recommendationMean']
cols_nsd = ['company', 'dri', 'dri2', 'dre', 'data', 'versao', 'auditor', 'auditor_rt', 'cancelamento', 'protocolo', 'envio', 'url', 'nsd']
cols_dre = ['Companhia', 'Trimestre', 'Demonstrativo', 'Conta', 'Descrição', 'Valor','Url']

demo = ['Demonstrações Financeiras Padronizadas', 'Informações Trimestrais']
cmbGrupo = ['Dados da Empresa']
cmbQuadro = ['Demonstração do Resultado', 'Balanço Patrimonial Ativo', 'Balanço Patrimonial Passivo', 'Demonstração do Fluxo de Caixa', 'Demonstração de Valor Adicionado', 'Demonstração do Resultado Abrangente']

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

  df_name = 'world_companies'
  world_companies = pd.DataFrame(columns=cols_world_markets)

  # world companies
  for index, abbrv in enumerate(abbreviation):
    try:
      df = pd.DataFrame(ss.get_symbol_list(market=abbrv)) # "us" or "america" will also work
      world_companies = pd.concat([world_companies, df], ignore_index=True)
      print(f'{abbrv} {index}+{len(abbreviation)-1-index} markets {index/(len(abbreviation)-1):.2%}, {len(df)} new, {len(world_companies)} total companies')
    except Exception as e:
      pass

  world_companies = world_companies.copy()
  world_companies['market'] = world_companies['market'].map(lambda x: x.replace('_market', ''))
  world_companies.fillna('', inplace=True)
  world_companies.drop_duplicates(inplace=True)
  
  # expand sufixes
  world_companies[['ticker', 'exchange_country']] = world_companies['symbol'].str.split('.', expand=True)
  world_companies['ticker_type'] = ''

  # expand Brazil Ticker Sufixes
  mask = (world_companies['market'] == 'br')
  br_world_companies = world_companies[mask]

  # adjustments
  br_world_companies['ticker_type'] = br_world_companies['ticker'].str[4:]
  br_world_companies = br_world_companies.copy()
  br_world_companies['ticker'] = br_world_companies['ticker'].str[:4]

  world_companies = pd.merge(world_companies, br_world_companies, how='left')
  world_companies.fillna('', inplace=True)

  # Save
  world_companies = run.save_and_pickle(world_companies, df_name)

  value = 'done ' + value
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

def get_nsd_links(value):
    safety_factor = 1.8

    gap = 0
    start_time = time.time()

    file_name = 'nsd_links'
    cols_nsd = ['company', 'dri', 'dri2', 'dre', 'data', 'versao', 'auditor', 'auditor_rt', 'cancelamento', 'protocolo', 'envio', 'url', 'nsd']
    nsd = run.read_or_create_dataframe(file_name, cols_nsd)
    nsd['envio'] = pd.to_datetime(nsd['envio'], dayfirst=True)

    start, end = run.nsd_range(nsd, safety_factor)
    print(f'from {start} to {end}')

    for i, n in enumerate(range(start, end)):
        # interrupt conditions
        last_date, limit_date, max_gap = run.nsd_dates(nsd, safety_factor)
        if last_date > limit_date:
            if gap == max_gap:
                break

        # elapsed time
        running_time = (time.time() - start_time)
        elapsed_time = '{:.6f}'.format(running_time/(i+1))
        minutes, seconds = divmod(round(float(running_time)), 60)
        elapsed_time_formatted = f'{int(minutes)}m {int(seconds)}s'
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            # add nsd row to dataframe
            row = run.get_nsd(n)
            nsd = pd.concat([nsd, pd.DataFrame([row], columns=cols_nsd)])
            print(row[-1], row[10], now, elapsed_time, row[4], row[3], row[0], elapsed_time_formatted)
            # reset gap
            gap = 0
        except Exception as e:
            # increase gap count
            gap += 1
            print(n, elapsed_time)

        if n % bin_size == 0:
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
  nsd['data'] = pd.to_datetime(nsd['data'], format='%d/%m/%Y')
  nsd = nsd.sort_values(by=['company', 'data'])
  nsd['data'] = nsd['data'].dt.strftime('%d/%m/%Y')

  driver, wait = run.load_browser()

  size = len(nsd)
  start_time = time.time()
  for l, line in enumerate(nsd.itertuples()):
    # elapsed time
    running_time = (time.time() - start_time)
    avg_time_per_item = running_time / (l + 1)
    elapsed_time = f'{running_time / (l + 1):.6f}'
    # remaining time
    remaining_time = size * avg_time_per_item
    hours, remainder = divmod(int(float(remaining_time)), 3600)
    minutes, seconds = divmod(remainder, 60)
    remaining_time_formatted = f'{int(hours)}h {int(minutes)}m {int(seconds)}s'

    # read table
    # read and concat quarters from nsd (and all dre in each quarter)
    quarter = run.read_quarter(line, driver, wait)
    df = pd.concat([df, quarter], ignore_index=True)

    print(f'{l+1}, {(size-l-1-1)}, {((l+1) / size) * 100:.6f}%, {run.txt_cln(line[1])}, {line[5]}, {remaining_time_formatted}')
    
    if (size-l) % (bin_size) == 0:
      dre = pd.concat([dre, df], ignore_index=True)

      dre = run.save_and_pickle(df, file_name)
      df = pd.DataFrame(columns=cols_dre)
      print('partial save')

  dre.drop_duplicates(inplace=True, keep='first')
  dre.sort_values(by=['Companhia', 'Trimestre', 'Conta'], ascending=[True, False, True], inplace=True)
  dre = run.save_and_pickle(df, file_name)
  print('final save')


  return value