import assets.functions as run
from typing import Any

from selenium import webdriver

import pandas as pd

import os
import time
import datetime

global duration
duration = time.time()

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
cols_nsd = ['company', 'dri', 'dri2', 'dre', 'data', 'versao', 'auditor', 'auditor_rt', 'cancelamento', 'protocolo', 'envio', 'url', 'nsd']
cols_dre = ['Companhia', 'Trimestre', 'Demonstrativo', 'Conta', 'Descrição', 'Valor','Url']
cols_dre_math = ['Companhia', 'Trimestre', 'Demonstrativo', 'Conta', 'Descrição', 'Valor', 'Url', 'nsd']

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
driver_wait_time = 5
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

# dre_cvm variables
base_cvm = "https://dados.cvm.gov.br/dados/CIA_ABERTA/"
xpath_cvm = '/html/body/div[1]/pre'
url_setorial = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/classification?language=pt-br'
download_folder = 'downloads'
url_companies_info = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br'

start_year = 2010
session = run.requests.Session() # Inicializar uma sessão
filelist = [] # Lista para armazenar links de arquivos CSV e ZIP
visited_subfolders = set() # Conjunto para armazenar subpastas já visitadas


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
        start_time = time.time()
        for i, (index, row) in enumerate(b3_tickers.iterrows()):
            counter +=1
            keyword = str(row['ticker']) + ' ' + str(row['company_name'])
            if keyword not in b3_keywords:
                driver.get(url)

                keyword = run.wSendKeys(f'//*[@id="keyword"]', keyword, wait)
                keyword = run.wClick(f'//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div/div[3]/button', wait)

                company = run.get_company(1, driver, wait)
                b3_companies = pd.concat([b3_companies, pd.DataFrame([company], columns=cols_b3_companies)])
            else:
                pass
            print(run.remaining_time(start_time, len(b3_keywords), i), counter, size-counter, keyword)
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
    Updates the world markets data based on stock symbols and saves the result.
    
    Args:
        value (str): A string to be appended with "done".
    
    Returns:
        str: The input string appended with "done" to indicate completion.
    """
    import credentials.keys
    from stocksymbol import StockSymbol

    # Initialize StockSymbol with credentials
    ss = StockSymbol(credentials.keys.polygon)
    
    # Retrieve world markets and indices data
    world_markets = pd.DataFrame(ss.market_list)
    index_data = pd.DataFrame(ss.index_list)
    world_markets.drop(labels='index', axis=1, inplace=True)
    world_markets = pd.merge(index_data, world_markets, how='outer')
    
    # Cleaning and organizing world_markets DataFrame
    world_markets = world_markets[['market', 'abbreviation', 'totalCount', 'lastUpdated', 'indexName', 'indexId']]
    world_markets.fillna('', inplace=True)
    world_markets.sort_values(by=['market','indexName'], inplace=True)
    
    # Retrieve all unique abbreviations
    abbreviation = world_markets['abbreviation'].unique()
    
    # Initialize world_companies DataFrame
    cols_world_markets = ['market', 'abbreviation', 'ticker', 'exchange_country', 'ticker_type']
    world_companies = pd.DataFrame(columns=cols_world_markets)
    
    # Populate world_companies with data for each abbreviation
    start_time = time.time()
    for index, abbrv in enumerate(abbreviation):
        try:
            df = pd.DataFrame(ss.get_symbol_list(market=abbrv))
            world_companies = pd.concat([world_companies, df], ignore_index=True)
        except Exception:
            df = pd.DataFrame()
        print(run.remaining_time(start_time, len(abbreviation), index), f' {abbrv}, {len(df)} new {len(world_companies)} total companies')

    # Clean and organize world_companies DataFrame
    world_companies['market'] = world_companies['market'].str.replace('_market', '')
    world_companies.fillna('', inplace=True)
    world_companies.drop_duplicates(inplace=True)
    
    # Expand ticker and country information from symbol
    world_companies[['ticker', 'exchange_country']] = world_companies['symbol'].str.split(pat='.', n=1, expand=True)
    world_companies['ticker_type'] = ''
    
    # Handle specific adjustments for Brazil
    mask = world_companies['market'] == 'br'
    brazil_tickers = world_companies[mask].copy()
    brazil_tickers['ticker_type'] = brazil_tickers['ticker'].str[4:]
    brazil_tickers['ticker'] = brazil_tickers['ticker'].str[:4]
    
    world_companies.update(brazil_tickers)
    
    # Save the DataFrame
    world_companies = run.save_and_pickle(world_companies, 'world_companies')
    
    return 'done ' + value

def yahoo_cotahist(value):
    import yfinance as yf

    df_name = 'world_companies'
    world_companies = run.read_or_create_dataframe(df_name, cols_world_markets)

    df_name = 'company_info'
    company_info = run.read_or_create_dataframe(df_name, cols_info)

    c_info = pd.DataFrame(columns=cols_info)

    # filter missing companies
    mask = world_companies['symbol'].isin(company_info['symbol'].unique())
    downloaded_companies = world_companies[mask]
    missing_companies = world_companies[~mask]

    for c, company in enumerate(missing_companies.itertuples()):
      downloaded = (len(downloaded_companies)+c+1)
      print(f'{downloaded} {len(missing_companies)-(c+1)} of {len(world_companies)} {downloaded/len(world_companies):.4%} {company[5]} {company[4]}:{company[1]} {company[3]}')
      ticker  = yf.Ticker(company[1])
      try:
        c_info2 = pd.DataFrame([ticker.info])
        c_info2['symbol'] = company[1]
        c_info = pd.concat([c_info, c_info2], ignore_index=True)
      except Exception as e:
        pass

    if (downloaded) % varsys.bin_size == 0:
      if not c_info.empty:
        # load
        company_info = pd.read_pickle(varsys.data_path + f'{df_name}.zip')

        # save
        try:
          company_info = pd.concat([company_info, c_info], ignore_index=True)

          try:
            company_info = company_info.drop(['companyOfficers'], axis=1, errors='ignore')
            company_info.drop_duplicates(inplace=True)
          except Exception as e:
            pass
            
          company_info.to_pickle(varsys.data_path + f'{df_name}.zip')

          company_info = pd.DataFrame(columns=cols_info)
          c_info = pd.DataFrame(columns=cols_info)

          print(f'partial save')
        except Exception as e:
          print(e)

    # final save
    company_info = pd.concat([company_info, c_info], ignore_index=True)
    company_info.sort_values(by=['market', 'exchange', 'quoteType', 'sector', 'industry', 'symbol'], inplace=True)

    try:
      company_info = company_info.drop(['companyOfficers'], axis=1, errors='ignore')
      company_info.drop_duplicates(inplace=True)
    except Exception as e:
      pass

    company_info.to_pickle(varsys.data_path + f'{df_name}.zip')

    company_info = pd.DataFrame(columns=cols_info)
    c_info = pd.DataFrame(columns=cols_info)

    value='please refactor using yahooquery, nothing done here'
    return value

def get_nsd_links(value):
    acoes = run.get_composicao_acionaria()

    nsd = run.get_nsd_content()

    return value

def get_dre(value):
  # download new dre from nsd list
  filename = f'dre_raw'
  dre = run.read_or_create_dataframe(filename, cols_dre)
  df = pd.DataFrame(columns=cols_dre)

  # get new nsd links to download not yet downloaded in dre
  nsd = run.get_new_dre_links(dre)

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

    # read and concat quarters from nsd (and all dre in each quarter)
    quarter = run.read_quarter(line, driver, wait)
    df = pd.concat([df, quarter], ignore_index=True)

    print(f'{l+1}, {(size-l-1)}, {((l+1) / size) * 100:.6f}%, {run.clean_text(line[1])}, {line[5]}, {remaining_time_formatted}')
    
    if (size-l-1) % (bin_size) == 0:
      dre = pd.concat([dre, df], ignore_index=True)

      dre = run.save_and_pickle(dre, filename)
      df = pd.DataFrame(columns=cols_dre)
      print('partial save')

  dre['Trimestre'] = pd.to_datetime(dre['Trimestre'], format='%d/%m/%Y')
  dre.sort_values(by=['Companhia', 'Trimestre', 'Url', 'Conta'], ascending=[True, False, True, True], inplace=True)
  dre['Trimestre'] = dre['Trimestre'].dt.strftime('%d/%m/%Y')
  dre.drop_duplicates(inplace=True, keep='last')
  dre = run.save_and_pickle(dre, filename)
  print('final save')


  return value

def dre_math(value):
  filename = 'dre_raw'
  dre_raw = run.read_or_create_dataframe(filename, cols_dre_math)
  dre_raw = run.clean_dre_math(dre_raw)

  filename = 'dre_math'
  dre_math = run.read_or_create_dataframe(filename, cols_dre_math)
  dre_math = run.clean_dre_math(dre_math)
  # last company fix
  try:
    dre_math['Companhia'] = dre_math['Companhia'].astype('category').cat.as_ordered()
    dre_math = dre_math[dre_math['Companhia'] != dre_math['Companhia'].max()]
    # print(f"{dre_math['Companhia'].max()} is out!")
  except Exception as e:
     print(e)

  dre_raw, dre_math = run.dre_prepare(dre_raw, dre_math)

  cias, math = run.do_the_math(dre_raw, dre_math)
  size = len(math)
  print(f'Total of {size} items (items in company quarters) new to process')
  df_temp = pd.DataFrame(columns=cols_dre_math)

  avpi = []
  start_time = time.time()
  for l, key in enumerate(math):
    progress = run.remaining_time(start_time, size, l)

    df, cias, status, key_cia = run.math_magic(key[0], key[1], size, cias, l)
    df_temp = pd.concat([df_temp, df], axis=0, ignore_index=True)

    avpi.append(f'{progress[0]:.6f}')
    if (size-l-1) % (bin_size*100) == 0 and status != True:
        pd.DataFrame(avpi).to_csv(app_folder + filename + '.csv', index=False)

        dre_math = pd.concat([dre_math, df_temp], axis=0, ignore_index=True)
        df_temp = pd.DataFrame(columns=cols_dre_math)

        dre_math.drop_duplicates(inplace=True)
        filename = 'dre_math'
        dre_math = run.save_and_pickle(dre_math, filename)
        print(f'partial save {l+1}, {(size-l-1)}, {((l+1) / size) * 100:.6f}%, {progress[0]:.6f}s, {progress[1]} {key_cia[0]} {key_cia[1]}')

  dre_math = pd.concat([dre_math, df_temp], axis=0, ignore_index=True)
  dre_math.drop_duplicates(inplace=True)
  filename = 'dre_math'
  dre_math = run.save_and_pickle(dre_math, filename)


  return value

def dre_intel(value):
    # existing dre_math (raw) to be converted by inteligence and then pivoted
    filename = 'dre_math'
    dre_math = run.read_or_create_dataframe(filename, cols_dre_math)
    dre_math = run.clean_dre_math(dre_math)
    
    filename = 'dre_intel'
    dre_intel = run.read_or_create_dataframe(filename, cols_dre_math)

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

        df = group[1]
        group = group[0]
        companhia = group[0]
        trimestre = group[1].strftime('%d/%m/%Y')
       
        df1 = run.inteligence_dre(df)
        df2 = run.fundamentalist_dre(df1, group)

        dre_intel = pd.concat([dre_intel.reset_index(drop=True).drop_duplicates(), df2], ignore_index=True)
        print(f'{item+1} {size-item-1} {((item+1)/(size)):.2%} {progress[0]:.6f}s, {progress[1]} {df2.shape[0]} {companhia} {trimestre}')

        avpi.append(f'{progress[0]:.6f}')
        if (size-item-1) % (bin_size/10) == 0:
            pd.DataFrame(avpi).to_csv(app_folder + filename + '.csv', index=False)

            dre_intel = dre_intel.astype(str)
            dre_intel = dre_intel.reset_index(drop=True).drop_duplicates().fillna(0)
            dre_intel = run.save_and_pickle(dre_intel, filename)
            print('partial save')


    dre_intel = dre_intel.reset_index(drop=True).drop_duplicates().fillna(0)
    dre_intel = run.save_and_pickle(dre_intel, filename)
    print('final save')

    return value

def dre_pivot(value):
    filename = 'dre_intel'
    dre_intel = run.read_or_create_dataframe(filename, cols_dre_math)
    dre_intel = run.clean_dre_math(dre_intel)

    dre_intel['CDD'] = dre_intel['Conta'].astype('str') + ' - ' + dre_intel['Descrição'].astype('str') + ' - ' + dre_intel['Demonstrativo'].astype('str')
    groups = dre_intel.groupby(by='Companhia', group_keys=False)

    filename = 'dre_pivot'
    dre_pivot = run.read_or_create_dataframe(filename, cols_dre_math)

    avpi = []
    start_time = time.time()
    size = len(groups)

    # groupby intel to transform into pivot
    for item, group in enumerate(groups):
        progress = run.remaining_time(start_time, size, item)
        company = group[0]
        group = group[1]

        avpi.append(f'{progress[0]:.6f}')

        pivot = pd.pivot_table(data=group, index=['Trimestre'], columns=['CDD'], values=['Valor'], aggfunc='max', fill_value=0.0)
        pivot.columns = pivot.columns.droplevel(0)
        pivot['Companhia'] = company
        pivot = pivot.reset_index()
        cols = pivot.columns.to_list()
        cols.insert(0, cols.pop())
        pivot = pivot[cols]

        dre_pivot = pd.concat([dre_pivot, pivot], ignore_index=True)
        print(f'{item+1} {len(groups)-item-1} {(item+1)/(len(groups)):.2%} {progress[0]:.6f}s {progress[1]} {company} {group.shape}')

    # save
    dre_pivot = run.save_and_pickle(dre_pivot, filename)
    print('saved')

    return value

def dre_cvm(value):
  fund = run.load_database()

def yahoo_quotes(value):
  fund = run.load_database()

  quotes = run.integrate_yahoo_quotes(fund)
  quotes = run.save_pkl(quotes, f'{app_folder}quotes')

  return value