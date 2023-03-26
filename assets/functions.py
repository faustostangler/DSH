import assets.helper as b3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from webdriver_manager.chrome import ChromeDriverManager
import unidecode
import string

import os

import pandas as pd

from google.cloud import storage
from io import BytesIO

import requests
from bs4 import BeautifulSoup
import unidecode
import string
import datetime
import time

# text functions
def wText(xpath: str, wait: WebDriverWait) -> str:
    """
    Finds and retrieves text from a web element using the provided xpath and wait object.
    
    Args:
    xpath (str): The xpath of the element to retrieve text from.
    wait (WebDriverWait): The wait object to use for finding the element.
    
    Returns:
    str: The text of the element, or an empty string if an exception occurs.
    """
    try:
        # Wait until the element is clickable, then retrieve its text.
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        text = element.text
        
        return text
    except Exception as e:
        # If an exception occurs, print the error message (if needed) and return an empty string.
        # print('wText', e)
        return ''

def wClick(xpath: str, wait: WebDriverWait) -> bool:
    """
    Finds and clicks on a web element using the provided xpath and wait object.
    
    Args:
    xpath (str): The xpath of the element to click.
    wait (WebDriverWait): The wait object to use for finding the element.
    
    Returns:
    bool: True if the element was found and clicked, False otherwise.
    """
    try:
        # Wait until the element is clickable, then click it.
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        return True
    except Exception as e:
        # If an exception occurs, print the error message (if needed) and return False.
        # print('wClick', e)
        return False

def wSelect(xpath: str, driver: webdriver.Chrome, wait: WebDriverWait) -> int:
    """
    Finds and selects a web element using the provided xpath and wait object.
    
    Args:
    xpath (str): The xpath of the element to select.
    driver (webdriver.Chrome): The Chrome driver object to use for selecting the element.
    wait (WebDriverWait): The wait object to use for finding the element.
    
    Returns:
    int: The value of the selected option, or an empty string if an exception occurs.
    """
    try:
        # Wait until the element is clickable, then click it.
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        
        # Get the Select object for the element, find the maximum option value, and select it.
        select = Select(driver.find_element(By.XPATH, xpath))
        options = [int(x.text) for x in select.options]
        batch = str(max(options))
        select.select_by_value(batch)
        
        return int(batch)
    except Exception as e:
        # If an exception occurs, print the error message (if needed) and return an empty string.
        # print('wSelect', e)
        return ''
   
def wSendKeys(xpath: str, keyword: str, wait: WebDriverWait) -> str:
    """
    Finds and sends keys to a web element using the provided xpath and wait object.
    
    Args:
    xpath (str): The xpath of the element to send keys to.
    keyword (str): The keyword to send to the element.
    wait (WebDriverWait): The wait object to use for finding the element.
    
    Returns:
    str: The keyword that was sent to the element, or an empty string if an exception occurs.
    """
    try:
        # Wait until the element is clickable, then send the keyword to it.
        input_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        input_element.send_keys(keyword)
        
        return keyword
    except Exception as e:
        # If an exception occurs, print the error message (if needed) and return an empty string.
        # print('wSendKeys', e)
        return ''

def wLink(xpath, wait, EC, By):
    """
    Finds and retrieves the href attribute of a web element using the provided xpath and wait object.
    
    Args:
        xpath (str): The xpath of the web element.
        wait (WebDriverWait): The wait object used to wait for the web element to be clickable.
        EC: The ExpectedConditions module used to check the expected conditions of the web element.
        By: The By module used to find the web element.
        
    Returns:
        href (str): The href attribute of the web element.
        '' (str): An empty string if the web element is not found or an exception occurs.
    """
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        href = element.get_attribute('href')
        return href
    except Exception as e:
        # print('wLink', e)
        return ''

def wRaw(xpath, wait):
  try:
    # Wait until the element is clickable, then retrieve its text.
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    raw_code = element.get_attribute("innerHTML")
    return raw_code
  except Exception as e:
    # If an exception occurs, print the error message (if needed) and return an empty string.
    # print('wText', e)
    return ''

def txt_cln(text):
    """
    Cleans text by removing any leading/trailing white space, converting it to lowercase, removing
    accents, punctuation, and converting to uppercase.
    
    Args:
    text (str): The input text to clean.
    
    Returns:
    str: The cleaned text.
    """
    try:
        # Convert text to string
        try:
            text = str(text)
        except Exception as e:
            print(text, 'is not convertible')
        # Remove accents, punctuation, and convert to uppercase
        text = unidecode.unidecode(text).translate(str.maketrans('', '', string.punctuation)).upper().strip()
    except Exception as e:
        print(e)
    return text

# selenium functions
def load_browser():
    """
    Launches chromedriver and creates a wait object.
    
    Returns:
    tuple: A tuple containing a WebDriver instance and a WebDriverWait instance.
    """
    # Define the options for the ChromeDriver.
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--no-sandbox')  # Avoid sandboxing.
    options.add_argument('--disable-dev-shm-usage')  # Disable shared memory usage.
    options.add_argument('--disable-blink-features=AutomationControlled')  # Disable automated control.
    # options = Options()
    options.add_argument('start-maximized')  # Maximize the window on startup.

    # Install and start the ChromeDriver service, passing in the options.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Define the exceptions to ignore during WebDriverWait.
    exceptions_ignore = (NoSuchElementException, StaleElementReferenceException)
    
    # Create a WebDriverWait instance for the driver, using the specified wait time and exceptions to ignore.
    wait = WebDriverWait(driver, b3.driver_wait_time, ignored_exceptions=exceptions_ignore)
    b3.set_driver_and_wait(driver, wait)

    # Return a tuple containing the driver and the wait object.
    return driver, wait

def get_company(i, driver, wait):
  """
  Retrieves company information from a web page using the provided index, Selenium driver and wait object.

  Args:
  - i (int): Index of the company to retrieve information from
  - driver (selenium.webdriver): Selenium WebDriver object used to interact with the web page
  - wait (selenium.webdriver.support.ui.WebDriverWait): WebDriverWait object used to wait for elements to load

  Returns:
  - company (list): A list of company information, in the following order:
      - pregao (str): Company trading name
      - company_name (str): Company full name
      - cvm (str): Company CVM code
      - listagem (str): Company stock listing
      - ticker (str): Company ticker symbol
      - tickers (str): Other ticker symbols associated with the company
      - asin (str): ASIN codes associated with the company
      - cnpj (str): Company CNPJ number
      - site (str): Company website
      - setor (str): Company sector
      - subsetor (str): Company subsetor
      - segmento (str): Company segment
      - atividade (str): Company main activity
      - escriturador (str): Company scrip agent
      - url (str): URL to the company overview page
  """
  # listagem
  try:
    list_dict = dict(zip(b3.l1, b3.l2))
    xpath = f'//*[@id="nav-bloco"]/div/div[{i}]/div/div/p[3]'
    listagem = wText(xpath, wait)
    for word, replacement in list_dict.items():
      listagem = txt_cln(listagem.replace(word, replacement))
  except Exception as e:
    listagem = ''

  # pregao
  try:
    xpath = f'//*[@id="nav-bloco"]/div/div[{i}]/div/div/p[2]'
    pregao = txt_cln(wText(xpath, wait))
  except Exception as e:
    pregao = ''
  
  # company name
  try:
    xpath = f'//*[@id="nav-bloco"]/div/div[{i}]/div/div/p[1]'
    company_name = txt_cln(wText(xpath, wait))
  except Exception as e:
    company_name = ''

  # get more details
  item = wClick(f'//*[@id="nav-bloco"]/div/div[{i}]/div', wait)
  click = wClick(f'//*[@id="accordionHeading2"]/div/div/a', wait)
  div1 = wText(f'//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]', wait).splitlines()
  div15 = wText(f'//*[@id="accordionBody2"]', wait)
  div2 = wText(f'//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[2]', wait).splitlines()

  # cnpj
  try:
    cnpj = div1[div1.index('CNPJ')+1]
  except Exception as e:
    cnpj = ''

  # atividade principal
  try:
    atividade = div1[div1.index('Atividade Principal')+1]
  except Exception as e:
    atividade = ''

  # setor, subsetor e segmento
  try:
    setor = div1[div1.index('Classificação Setorial')+1]
    segmento = setor.split(' / ')[2].strip()
    subsetor = setor.split(' / ')[1].strip()
    setor = setor.split(' / ')[0].strip()
  except Exception as e:
    setor = ''
    subsetor = ''
    segmento = ''

  # site
  try:
    site = div1[div1.index('Site')+1]
  except Exception as e:
    site = ''

  # cvm code
  div15b = div15.splitlines()
  try:
    cvm = driver.current_url.split('/')[5]
  except Exception as e:
    cvm = ''

  # ticker
  try:
    ticker = driver.current_url.split('/')[6]
  except Exception as e:
    print('ticker', e)
    ticker = ''

  # tickers asin
  try:
    list_size = div15b.index('Código CVM')
  except Exception as e:
    list_size = len(div15b)

  try:
    div15b = div15b[1:list_size]
    tickers = '/'.join(div15b[0::2])
    asin = '/'.join(div15b[1::2])
  except Exception as e:
    tickers = ''
    asin = ''

  # escriturador
  try:
    escriturador = [div2 for div2 in div2 if 'Instituição' in div2][0].split(':')[1].split()
    escriturador = txt_cln(' '.join(pd.Series(escriturador).drop_duplicates().tolist()))
  except Exception as e:
    escriturador = ''

  # url
  url = f'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/main/{cvm}/{ticker}/overview?language=pt-br'

  company = [pregao, company_name, cvm, listagem, ticker, tickers, asin, cnpj, site, setor, subsetor, segmento, atividade, escriturador, url]

  return company

def get_ticker_keywords(raw_code):
  from bs4 import BeautifulSoup

  # Initialize a list to hold the keyword information
  keywords = []

  for inner_html in raw_code:
     # Parse the raw HTML source code
    soup = BeautifulSoup(inner_html, 'html.parser')

    # Find all the card elements
    cards = soup.find_all('div', class_='card-body')

    # Loop through each card element and extract the ticker and company name
    for card in cards:
      try:
        # Extract the ticker and company name from the card element
        ticker = txt_cln(card.find('h5', class_='card-title2').text)
        company_name = txt_cln(card.find('p', class_='card-title').text)
        pregao = txt_cln(card.find('p', class_='card-text').text)
        listagem = txt_cln(card.find('p', class_='card-nome').text)

        
        # Append the ticker and company name to the keyword list
        keyword = [ticker, company_name]
        keywords.append(keyword)
        print(keyword)
      except Exception as e:
        # print(e)
        pass


  df = pd.DataFrame(keywords, columns=['ticker', 'company_name'])
  df.reset_index(drop=True, inplace=True)
  df.drop_duplicates(inplace=True)
  return df

# os functions
def check_or_create_folder(folder):
    """
    Check if the given folder exists, and create it if it doesn't.

    Args:
    folder (str): the path of the folder to be checked/created.

    Returns:
    str: the path of the folder.
    """
    try:
        if not os.path.exists(folder): 
            os.makedirs(folder)  # create folder if it doesn't exist
    except Exception as e:
        print('Error occurred while creating folder:', e)
    return folder

# pandas functions
def read_or_create_dataframe(file_name, cols):
    """
    Read a pandas DataFrame from a compressed file, or create an empty DataFrame if the file doesn't exist.

    Args:
    file_name (str): the name of the file (without the extension) to read/create.
    cols (list): a list of column names for the DataFrame.

    Returns:
    pd.DataFrame: the DataFrame read from the file, or an empty DataFrame if the file doesn't exist.
    """
    # Construct the full path to the file using the varsys data_path.
    file_path = os.path.join(b3.data_path, f'{file_name}.zip')
    try:
      df = download_from_gcs(file_name)
      pass
    except Exception as e:
      try:
        df = pd.read_pickle(file_path)  # Try to read the file as a pickle.
        # df = upload_to_gcs(df, file_name)
      except Exception as e:
        # print(f'Error occurred while reading file {file_name}: {e}')
        df = pd.DataFrame(columns=b3.cols_nsd)
        
    df.drop_duplicates(inplace=True)  # Remove any duplicate rows (if any).
    
    print(f'{file_name}: total {len(df)} items')
    return df

def save_and_pickle(df, df_name):
  df.to_pickle(b3.data_path + f'{df_name}.zip')
  df = upload_to_gcs(df, df_name)

  return df

# nsd_functions
def nsd_range(nsd, safety_factor):
  # start
  try:
    start = int(max(nsd['nsd'])) + 1
  except:
    start = 1

  # find the gap in days from today to max 'envio' date
  last_date = nsd['envio'].max().date()
  today = datetime.datetime.now().date()
  days_gap = (today - last_date).days

  # group nsd by day
  nsd_per_day = nsd.groupby(nsd['envio'].dt.date)['nsd'].count()

  # find the average nsd items per day group, and other things
  avg_nsd_per_day = nsd_per_day.mean()
  max_nsd_per_day = nsd_per_day.max()
  max_date_nsd_per_day = nsd_per_day.idxmax()

  # calculate the expected items up to today
  expected_nsd = int(avg_nsd_per_day * (days_gap + safety_factor) * safety_factor)

  # end
  end = start + expected_nsd

  # range
  start = start
  end = start + expected_nsd 

  return start-1, end

def nsd_dates(nsd, safety_factor):
  # find the gap in days from today to max 'envio' date
  last_date = nsd['envio'].max().date()
  today = datetime.datetime.now().date()
  days_gap = (today - last_date).days
  
  # find the maximum 'nsd' gap
  max_gap = int(((nsd['nsd'].diff().max() + safety_factor) * 0.1))

  # group nsd by day
  nsd_per_day = nsd.groupby(nsd['envio'].dt.date)['nsd'].count()

  # find the average nsd items per day group, and other things
  avg_nsd_per_day = nsd_per_day.mean()
  max_nsd_per_day = nsd_per_day.max()
  max_date_nsd_per_day = nsd_per_day.idxmax()

  # last_date and previous safe date 
  back_days = round(max_gap / avg_nsd_per_day)
  limit_date = datetime.datetime.now().date() - datetime.timedelta(days=back_days)

  return last_date, limit_date, max_gap

def get_nsd(n):
  nsd_url = f'https://www.rad.cvm.gov.br/ENET/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento={n}&CodigoTipoInstituicao=1'
  # Getting the HTML content from the URL
  response = requests.get(nsd_url)
  html_content = response.text

  # Parsing the HTML content with BeautifulSoup
  soup = BeautifulSoup(html_content, 'html.parser')

  # Extracting company
  nomeCompanhia_tag = soup.find('span', {'id': 'lblNomeCompanhia'})
  company = nomeCompanhia_tag.text.strip()
  company = unidecode.unidecode(company).upper()

  # Extracting dri and dri2
  nomeDRI_tag = soup.find('span', {'id': 'lblNomeDRI'})
  dri = nomeDRI_tag.text.strip().split(' - ')[0]
  dri = unidecode.unidecode(dri).upper()
  dri2 = nomeDRI_tag.text.strip().split(' - ')[-1].replace('(', '').replace(')', '')
  dri2 = unidecode.unidecode(dri2).upper()

  # Extracting 'FCA', data and versao
  descricaoCategoria_tag = soup.find('span', {'id': 'lblDescricaoCategoria'})
  descricaoCategoria = descricaoCategoria_tag.text.strip()
  versao = descricaoCategoria.split(' - ')[-1]
  data = descricaoCategoria.split(' - ')[1]
  dre = descricaoCategoria.split(' - ')[0]
  dre = unidecode.unidecode(dre).upper()

  # Extracting auditor
  lblAuditor_tag = soup.find('span', {'id': 'lblAuditor'})
  auditor = lblAuditor_tag.text.strip().split(' - ')[0]
  auditor = unidecode.unidecode(auditor).upper()

  # Extracting auditor_rt
  lblResponsavelTecnico_tag = soup.find('span', {'id': 'lblResponsavelTecnico'})
  auditor_rt = lblResponsavelTecnico_tag.text.strip()
  auditor_rt = unidecode.unidecode(auditor_rt).upper()

  # Extracting protocolo
  lblProtocolo_tag = soup.find('span', {'id': 'lblProtocolo'})
  protocolo = lblProtocolo_tag.text.strip()

  # Extracting '2010' and envio
  lblDataDocumento_tag = soup.find('span', {'id': 'lblDataDocumento'})
  lblDataDocumento = lblDataDocumento_tag.text.strip()

  lblDataEnvio_tag = soup.find('span', {'id': 'lblDataEnvio'})
  envio = lblDataEnvio_tag.text.strip()
  envio = datetime.datetime.strptime(envio, "%d/%m/%Y %H:%M:%S")

  # cancelamento
  cancelamento_tag = soup.find('span', {'id': 'lblMotivoCancelamentoReapresentacao'})
  cancelamento = cancelamento_tag.text.strip()
  cancelamento = unidecode.unidecode(cancelamento).upper()

  # url
  url = nsd_url

  # company
  row = [company, dri, dri2, dre, data, versao, auditor, auditor_rt, cancelamento, protocolo, envio, url, n]

  return row

def clean_nsd(nsd):
  nsd.reset_index(drop=True, inplace=True)
  nsd['nsd'] = pd.to_numeric(nsd['url'].str.replace('https://www.rad.cvm.gov.br/ENET/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento=','', regex=False).str.replace('&CodigoTipoInstituicao=1','', regex=False), errors='coerce')
  nsd['nsd'] = nsd['nsd'].astype(str).str.replace('.0','', regex=False)
  nsd.set_index('nsd', inplace=True)

  try:  
    nsd['company'] = nsd['company'].astype('category')
    nsd['dri'] = nsd['dri'].astype('category')
    nsd['dri2'] = nsd['dri2'].astype('category')
    nsd['dre'] = nsd['dre'].astype('category')
    nsd['data'] = nsd['data'].astype('category')
    nsd['versao'] = nsd['versao'].astype('category')
    nsd['envio'] = pd.to_datetime(nsd['envio'], format='%d/%m/%Y %H:%M:%S', infer_datetime_format=True)
  except Exception as e:
    pass
  
  try:
    nsd = nsd[b3.cols_nsd]
  except Exception as e:
    # cols.remove('nsd')
    # nsd = nsd[b3.cols_nsd]
      pass
  nsd = nsd.dropna()

  # mask1 = nsd['auditor'] == ''
  # mask2 = nsd['auditor'].isnull()
  # nsd = nsd[~mask1 & ~mask2]

  # filter and sort
  nsd.sort_values(by=['company', 'data', 'versao'], ascending=[True, True, True], inplace=True)

  return nsd

# dre
def clean_dre(dre):
  try:
    dre['nsd'] = pd.to_numeric(dre['Url'].str.replace('https://www.rad.cvm.gov.br/ENET/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento=','', regex=False).str.replace('&CodigoTipoInstituicao=1','', regex=False), errors='ignore')
    dre.sort_values(by=['nsd'], ascending=[False], inplace=True)

    dre['Companhia'] = dre['Companhia'].astype('category')
    dre['Demonstrativo'] = dre['Demonstrativo'].astype('category')
    dre['Conta'] = dre['Conta'].astype('category')
    dre['Descrição'] = dre['Descrição'].astype('category')
    dre['Url'] = dre['Url'].astype('category')
    dre['nsd'] = dre['nsd'].astype('category')

    # dre['Trimestre'] = pd.to_datetime(dre['Trimestre'], format='%d/%m/%Y')
    dre['Trimestre'] = pd.to_datetime(dre['Trimestre'], yearfirst=True, dayfirst=True, infer_datetime_format=True)

    dre['Valor'] = pd.to_numeric(dre['Valor'], errors='coerce')
  except Exception as e:
     pass

  try:
     dre = dre[b3.cols_dre]
  except Exception as e:
     pass

  return dre

def get_new_dre_links(dre):
      # load links
    file_name = 'nsd_links'
    nsd = read_or_create_dataframe(file_name, b3.cols_nsd)
    nsd = clean_nsd(nsd)

    # filter most recent by company and data, drop duplicates, keep most recent
    the_most_recent = nsd[['company', 'data']].copy()
    the_most_recent.drop_duplicates(inplace=True, keep='last')

    # filter nsd by recent and repeated
    nsd_repeated = nsd.loc[~nsd.index.isin(the_most_recent.index)]
    nsd_recent = nsd.loc[nsd.index.isin(the_most_recent.index)]

    dre_options = nsd['dre'].unique().tolist()
    dre_options.sort()
    mask0 = (nsd['dre'] == dre_options[0]) # 'DEMONSTRACOES FINANCEIRAS PADRONIZADAS'
    mask1 = (nsd['dre'] == dre_options[1]) # 'FORMULARIO CADASTRAL'
    mask2 = (nsd['dre'] == dre_options[2]) # 'FORMULARIO DE REFERENCIA'
    mask3 = (nsd['dre'] == dre_options[3]) # 'INFORMACOES TRIMESTRAIS'
    mask4 = (nsd['dre'] == dre_options[4]) # 'INFORME TRIMESTRAL DE SECURITIZADORA'
    nsd_dre = nsd[mask0 | mask3].copy()
    nsd_cad = nsd[mask1].copy()
    nsd_ref = nsd[mask2].copy()
    nsd_sec = nsd[mask4].copy()

    # filter by type
    nsd = nsd_dre

    # dre processing
    dre = clean_dre(dre)

    try:
        # remove dre not in nsd (so to re-download the new ones)
        mask = dre['Url'].isin(nsd['url'])
        dre_old = dre[~mask].copy() # Contém as linhas do dataframe dre com URLs que não estão presentes no dataframe nsd.
        dre_new = dre[mask].copy() # Contém as linhas do dataframe dre com URLs que estão presentes no dataframe nsd.
    except Exception as e:
        dre_old = dre.copy()
        dre_new = dre.copy()

    try:
        # remove nsd that is in the dre_new
        mask = nsd['url'].isin(dre_new['Url'])
        nsd_recent_old = nsd[mask] # Contém as linhas do dataframe nsd com URLs que estão presentes no dataframe dre_new, que Contém as linhas do dataframe dre com URLs que estão presentes no dataframe nsd.
        nsd_recent_new = nsd[~mask] # Contém as linhas do dataframe nsd com URLs que não estão presentes no dataframe dre_new, que Contém as linhas do dataframe dre com URLs que estão presentes no dataframe nsd.
        # O dataframe nsd_recent_new 
        # contém as linhas de nsd que têm URLs exclusivas de nsd, 
        # ou seja, não compartilhadas com dre_new. 
        # Já o dataframe dre_new 
        # contém as linhas de dre que têm URLs compartilhadas com nsd.
    except Exception as e:
        nsd_recent_old = nsd_dre.copy()
        nsd_recent_new = nsd_dre.copy()

    nsd = nsd_recent_new

    nsd['data'] = pd.to_datetime(nsd['data'], format='%d/%m/%Y')
    nsd = nsd.sort_values(by=['company', 'data'])
    nsd['data'] = nsd['data'].dt.strftime('%d/%m/%Y')

    print(len(nsd), 'total,', len(dre_old), 'financial statements to update and', len(nsd_recent_new), 'new financial statements to download')

    return nsd

def read_quarter(line, driver, wait):
  try:
    # initialize quarter dataframe
    quarter = pd.DataFrame(columns=b3.cols_dre)

    # get url
    url = f'https://www.rad.cvm.gov.br/ENET/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento={line[0]}&CodigoTipoInstituicao=1'
    driver.get(url)

    for quadro in b3.cmbQuadro:
      # concat quadro to quarter
      global table
      table = read_cmbQuadro(quadro, line, driver, wait)
      table['Companhia'] = line[1]
      table['Trimestre'] = line[5]
      table['Url'] = line[12]
      table['Demonstrativo'] = quadro
      try:
        quarter = pd.concat([quarter, table], ignore_index=True)
      except Exception as e:
        # print(e)
        pass

    for grupo in b3.cmbGrupo:
      table = read_cmbGrupo(grupo, line, driver, wait)
      try:
        quarter = pd.concat([quarter, table], ignore_index=True)
      except Exception as e:
        # print(e)
        pass
    
    quarter['Companhia'] = quarter['Companhia'].apply(txt_cln)
    quarter['Trimestre'] = pd.to_datetime(quarter['Trimestre'], format='%d/%m/%Y')

    return quarter
  except Exception as e:
    # print(e)
    pass

def read_cmbQuadro(quadro, line, driver, wait):
  try:
      # select item
      xpath = '//*[@id="cmbQuadro"]'
      selectBox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
      selectBox = Select(driver.find_element(By.XPATH, xpath))
      selectBox.select_by_visible_text(quadro)

      # selenium enter frame
      xpath = '//*[@id="iFrameFormulariosFilho"]'
      frame = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
      frame = driver.find_elements(By.XPATH, xpath)
      driver.switch_to.frame(frame[0])

      # get unidade de conta
      milhao = 1000000
      xpath = '//*[@id="TituloTabelaSemBorda"]'
      if '(Reais Mil)' in wText(xpath, wait):
          unidade = 1000 / milhao
      else:
          unidade = 1 / milhao

      # read and clean quadro
      table = pd.read_html(driver.page_source, header=0)[0]

      # selenium exit frame
      driver.switch_to.parent_frame()

      # clean and format table
      column_index = 2  # For the third column, the index is 2 (0-based indexing)
      table = table.iloc[:, 0:3]
      table = table.rename(columns={table.columns[column_index]: 'Valor'})
      table.iloc[:, column_index] = pd.to_numeric(table.iloc[:, column_index].str.replace('.', '', regex=False))
      table['Valor'] = pd.to_numeric(table['Valor'], errors='coerce')
      table.fillna(0, inplace=True)
      table['Valor'] = table['Valor'].astype(float) * unidade

      # time.sleep(random.uniform(0,1))

  except Exception as e:
      # print(e)
      pass
  return table

def read_cmbGrupo(grupo, line, driver, wait):
    try:
        # select item
        xpath = '//*[@id="cmbGrupo"]'
        selectBox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        selectBox = Select(driver.find_element(By.XPATH, xpath))
        selectBox.select_by_visible_text(grupo)

		# selenium enter frame
        xpath = '//*[@id="iFrameFormulariosFilho"]'
        frame = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        frame = driver.find_elements(By.XPATH, xpath)
        driver.switch_to.frame(frame[0])

		# read and clean quadro
        table = pd.read_html(driver.page_source, header=0, thousands='.')[0]

		# selenium exit frame
        driver.switch_to.parent_frame()

        # clean and format table
        for x in ['x']:
            break
        on = on_tes = on_outras = pn = pn_tes = pn_outras = 0
        # Ordinárias
        mask = table[table.columns[0]] == 'Ordinárias'
        on = pd.to_numeric(table[mask].iloc[0,1].replace('.', '' ))
        try:
            on_tes = pd.to_numeric(table[mask].iloc[1,1].replace('.', '' ))
        except Exception as e:
            pass
        try:
            on_outras = pd.to_numeric(table[mask].iloc[2,1].replace('.', '' ))
        except Exception as e:
            pass
        # preferenciais
        mask = table[table.columns[0]] == 'Preferenciais'
        pn = pd.to_numeric(table[mask].iloc[0,1].replace('.', '' ))
        try:
            pn_tes = pd.to_numeric(table[mask].iloc[1,1].replace('.', '' ))
        except Exception as e:
            pass
        try:
            pn_outras = pd.to_numeric(table[mask].iloc[2,1].replace('.', '' ))
        except Exception as e:
            pass

        # get unidade de conta
        milhao = 1
        if '(Mil)' in table.columns[0]:
                unidade = 1000/milhao
        else:
                unidade = 1/milhao
        # prepare dataframe
        demo = 'Composição do Capital'
        table = []
        table.append([line[1], line[5], demo, '0.01', 'Ações Ordinárias', on*unidade, line[12]])
        table.append([line[1], line[5], demo, '0.01.01', 'Ações Ordinárias em Tesouraria', on_tes*unidade, line[12]])
        table.append([line[1], line[5], demo, '0.01.02', 'Ações Ordinárias Outras', on_outras*unidade, line[12]])
        table.append([line[1], line[5], demo, '0.02', 'Ações Preferenciais', pn*unidade, line[12]])
        table.append([line[1], line[5], demo, '0.02.01', 'Ações Preferenciais em Tesouraria', pn_tes*unidade, line[12]])
        table.append([line[1], line[5], demo, '0.02.02', 'Ações Preferenciais Outras', pn_outras*unidade, line[12]])
        table = pd.DataFrame(table, columns=b3.cols_dre)

    except Exception as e:
        print(e, 'find me')
        pass
    return table

# math
def clean_dre_math(dre):
  try:
    # clean
    dre['Companhia'] = dre['Companhia'].str.replace(' EM RECUPERACAO JUDICIAL', '')
    dre['Companhia'] = dre['Companhia'].str.replace(' EM LIQUIDACAO EXTRAJUDICIAL', '')
    dre['Companhia'] = dre['Companhia'].str.replace(' EM LIQUIDACAO', '')


    # standartization
    dre['Companhia'] = dre['Companhia'].astype('category')
    dre['Demonstrativo'] = dre['Demonstrativo'].astype('category')
    dre['Trimestre'] = pd.to_datetime(dre['Trimestre'], yearfirst=True, dayfirst=True, infer_datetime_format=True)
    dre['Conta'] = dre['Conta'].astype('str')
    dre['Conta'] = dre['Conta'].astype('category')
    dre['Descrição'] = dre['Descrição'].astype('category')
    dre['Valor'] = pd.to_numeric(dre['Valor'], errors='coerce')
    dre['Url'] = dre['Url'].astype('category')
    dre['nsd'] = pd.to_numeric(dre['Url'].str.replace('https://www.rad.cvm.gov.br/ENET/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento=','', regex=False).str.replace('&CodigoTipoInstituicao=1','', regex=False), errors='ignore')
    dre['nsd'] = dre['nsd'].astype('str')
    dre['nsd'] = dre['nsd'].astype('category')

    dre.reset_index(drop=True, inplace=True)
    dre = (dre.sort_values(by=['Companhia', 'Trimestre', 'Conta'],
                        key=lambda col: pd.to_datetime(col, format='%d/%m/%Y') if col.name == 'Trimestre' else col))

    dre = dre[b3.cols_dre_math]
  except Exception as e:
    pass
  return dre

def get_dre_years(dre_raw, dre_math):
     # Get all Different Companhia and Trimestres
  try:
    raw = dre_raw.groupby(['Companhia', 'Trimestre'], group_keys=False)
    math = dre_math.groupby(['Companhia', 'Trimestre'], group_keys=False)

    difference = set(raw.groups.keys()) - set(math.groups.keys())
  except Exception as e:
    raw = dre_raw.groupby(['Companhia', 'Trimestre'], group_keys=False)
    difference = set(raw.groups.keys())

  difference = sorted(list(difference), key=lambda x: (x[0], x[1]))

  years = []
  for key in difference:
      item = f'{key[0]} {key[1].year}'
      if item not in years:
          years.append(item)
  
  return years

def dre_prepare(dre_raw, dre_math):
  years = get_dre_years(dre_raw, dre_math)

  # create 'update' columns
  dre_raw = dre_raw.assign(updated = lambda x: x['Companhia'].astype(str) + ' ' + x['Trimestre'].dt.year.astype(str))
  try:
      dre_math = dre_math.assign(updated = lambda x: x['Companhia'].astype(str) + ' ' + x['Trimestre'].dt.year.astype(str))
  except Exception as e:
    try:
      dre_math = dre_math.assign(updated = lambda x: x['Companhia'].astype(str) + ' ' + x['Trimestre'].astype(str))
    except Exception as e:
       pass

  # remove years from dre_math = remove years from existing dataframe
  try:
    mask_math = dre_math['updated'].isin(years)
    dre_math = dre_math[~mask_math][b3.cols_dre_math]
  except Exception as e:
    dre_math = dre_math

  # filter dre_raw by years = keep years from dataframe to be processed
  try:
    mask_raw = dre_raw['updated'].isin(years)
    dre_raw = dre_raw[mask_raw][b3.cols_dre_math]
  except Exception as e:
     dre_raw = dre_raw

  return dre_raw, dre_math

def get_math(dre_raw, dre_math):
    # do the math
  last_quarters = ['3', '4']
  all_quarters = ['6', '7']

  math = dre_raw.groupby([dre_raw['Companhia'], dre_raw['Trimestre'].dt.year, dre_raw['Conta']], group_keys=False)
  size = len(math)
  print(f'Total of {size} items (items in company quarters) new to process')

  try:
      cias_grouped = dre_math.groupby([dre_math['Companhia'], dre_math['Trimestre'].dt.year, dre_math['Conta']], group_keys=False)
  except Exception as e:
    try:
      cias_grouped = dre_math.groupby([dre_math['Companhia'], dre_math['Trimestre'], dre_math['Conta']], group_keys=False)
    except Exception as e:
      pass

  try:
    cias = []
    for key in cias_grouped:
      cias.append(key[0])
  except Exception as e:
     cias = []

  return cias, math

# storage functions
def upload_to_gcs(df, df_name):
    """Uploads a pandas DataFrame to Google Cloud Storage (GCS) as a zipped pickle file.

    Args:
        df (pandas.DataFrame): The DataFrame to be uploaded.
        df_name (str): The name to be used for the uploaded file (excluding the '.zip' extension).

    Returns:
        pandas.DataFrame: The input DataFrame.

    Raises:
        google.auth.exceptions.DefaultCredentialsError: If no valid credentials are found.
        google.api_core.exceptions.NotFound: If the specified bucket or JSON key file does not exist.
        google.cloud.exceptions.GoogleCloudError: If there was an error during the upload operation.

    """
    try:
      # GCS configuration
      destination_blob_name = f'{df_name}.zip'

      # Initialize GCS client
      client = storage.Client.from_service_account_json(b3.json_key_file)
      bucket = client.get_bucket(b3.bucket_name)

      # Save DataFrame to a bytes buffer as a zipped pickle file
      buffer = BytesIO()
      df.to_pickle(buffer, compression='zip')
      buffer.seek(0)

      # Upload the buffer to GCS
      blob = bucket.blob(destination_blob_name)
      blob.upload_from_file(buffer, content_type='application/zip')
    except Exception as e:
      # print(e)
      pass
    return df

def download_from_gcs(df_name):
    """Downloads a zipped pickle file from Google Cloud Storage (GCS) and returns its contents as a pandas DataFrame.

    Args:
        df_name (str): The name of the file to download (excluding the '.zip' extension).

    Returns:
        pandas.DataFrame: The contents of the downloaded file as a DataFrame.

    Raises:
        google.auth.exceptions.DefaultCredentialsError: If no valid credentials are found.
        google.api_core.exceptions.NotFound: If the specified bucket or JSON key file does not exist.
        google.cloud.exceptions.GoogleCloudError: If there was an error during the download operation.
        ValueError: If the downloaded file cannot be read as a pandas DataFrame.

    """
    # GCS configuration
    source_blob_name = f'{df_name}.zip'

    # Initialize GCS client
    client = storage.Client.from_service_account_json(b3.json_key_file)
    bucket = client.get_bucket(b3.bucket_name)

    # Download the zipped DataFrame from GCS to a bytes buffer
    buffer = BytesIO()
    blob = bucket.blob(source_blob_name)
    blob.download_to_file(buffer)
    buffer.seek(0)

    # Load the zipped DataFrame into a Pandas DataFrame
    df = pd.read_pickle(buffer, compression='zip')
    return df

# test functions
def pdf_download():
  import assets.helper as b3
  import requests
  import json
  import base64
  from google.cloud import storage
  from io import BytesIO

  # Set the required properties
  codigoInstituicao = 2
  numeroProtocolo = 1043145
  token = '6LdVyiwaAAAAABobBnLknCD5VGGkmH9snlJBxCyr'
  versaoCaptcha = 'V3'


  # Send the request
  base_url = 'https://www.rad.cvm.gov.br/ENET/'
  url = base_url + "frmExibirArquivoIPEExterno.aspx/ExibirPDF"
  headers = {"Content-Type": "application/json; charset=utf-8"}

  for numeroProtocolo in range (1043146, 1043146+2):
      # # Define the JSON payload
      # data = {
      #     "codigoInstituicao": codigoInstituicao,
      #     "numeroProtocolo": numeroProtocolo,
      #     "token": token,
      #     "versaoCaptcha": versaoCaptcha, 
      # }
      # response = requests.post(url, headers=headers, data=json.dumps(data))
      # # Get the base64-encoded PDF data from the response
      # pdf_data = response.json()['d']

      # # Decode base64-encoded PDF data
      # pdf_bytes = base64.b64decode(pdf_data)

      # # Save PDF data to file
      # with open(f"{numeroProtocolo}.pdf", "wb") as f:
      #     f.write(pdf_bytes)

      
      url = f"https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&numSequencia=567876&numVersao=1&numProtocolo={numeroProtocolo}&descTipo=IPE&CodigoInstituicao=1"
      response = requests.get(url)

      # Save PDF file to Google Cloud Service
      # GCS configuration
      destination_blob_name = f'{numeroProtocolo}.pdf'

      # Initialize GCS client
      client = storage.Client.from_service_account_json(b3.json_key_file)
      bucket = client.get_bucket(b3.bucket_name)

      # Upload the PDF file to GCS
      blob = bucket.blob(destination_blob_name)
      blob.upload_from_string(response.content, content_type='application/pdf')
      # blob.upload_from_string(pdf_bytes, content_type='application/pdf')


      print(numeroProtocolo)

