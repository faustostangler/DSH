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
import numpy as np

from google.cloud import storage
import io
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup
import unidecode
import string
import datetime
import time

import pickle
from urllib.parse import urljoin
import zipfile
from lxml import html

# general functions
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

def clean_text(text):
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

def remaining_time(start_time, size, i):
  # # elapsed time
  # running_time = (time.time() - start_time)
  # avg_time_per_item = running_time / (i + 1)
  # # remaining time
  # remaining_time = size * avg_time_per_item
  # hours, remainder = divmod(int(float(remaining_time)), 3600)
  # minutes, seconds = divmod(remainder, 60)
  # remaining_time_formatted = f'{int(hours)}h {int(minutes):02}m {int(seconds):02}s'

  # return avg_time_per_item, remaining_time_formatted

  counter = i + 1
  remaining_items = size - counter
  
  # Calculate the percentage of completion
  percentage = counter / size
  
  # Calculate the elapsed time
  running_time = time.time() - start_time
  
  # Calculate the average time taken per item
  avg_time_per_item = running_time / counter
  
  # Calculate the remaining time based on the average time per item
  remaining_time = remaining_items * avg_time_per_item
  
  # Convert remaining time to hours, minutes, and seconds
  hours, remainder = divmod(int(remaining_time), 3600)
  minutes, seconds = divmod(remainder, 60)
  
  # Format remaining time as a string
  remaining_time_formatted = f'{int(hours)}h {int(minutes):02}m {int(seconds):02}s'
  
  # Create a progress string with all the calculated values
  progress = (
    f'{percentage:.2%} '
    f'{counter}+{remaining_items}, '
    f'{avg_time_per_item:.6f}s per item, '
    f'Remaining: {remaining_time_formatted}'
  )

  return progress

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
      listagem = clean_text(listagem.replace(word, replacement))
  except Exception as e:
    listagem = ''

  # pregao
  try:
    xpath = f'//*[@id="nav-bloco"]/div/div[{i}]/div/div/p[2]'
    pregao = clean_text(wText(xpath, wait))
  except Exception as e:
    pregao = ''
  
  # company name
  try:
    xpath = f'//*[@id="nav-bloco"]/div/div[{i}]/div/div/p[1]'
    company_name = clean_text(wText(xpath, wait))
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
    escriturador = clean_text(' '.join(pd.Series(escriturador).drop_duplicates().tolist()))
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
        ticker = clean_text(card.find('h5', class_='card-title2').text)
        company_name = clean_text(card.find('p', class_='card-title').text)
        pregao = clean_text(card.find('p', class_='card-text').text)
        listagem = clean_text(card.find('p', class_='card-nome').text)

        
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
def read_or_create_dataframe(filename, cols):
    """
    Read a pandas DataFrame from a compressed file, or create an empty DataFrame if the file doesn't exist.

    Args:
    filename (str): the name of the file (without the extension) to read/create.
    cols (list): a list of column names for the DataFrame.

    Returns:
    pd.DataFrame: the DataFrame read from the file, or an empty DataFrame if the file doesn't exist.
    """
    # Construct the full path to the file using the varsys data_path.
    filepath = os.path.join(b3.data_path, f'{filename}.zip')
    try:
      df = download_from_gcs(filename)
      pass
    except Exception as e:
      try:
        df = pd.read_pickle(filepath)  # Try to read the file as a pickle.
        # df = upload_to_gcs(df, filename)
      except Exception as e:
        # print(f'Error occurred while reading file {filename}: {e}')
        df = pd.DataFrame(columns=cols)
        
    df.drop_duplicates(inplace=True)  # Remove any duplicate rows (if any).
    
    print(f'{filename}: total {len(df)} items')
    return df[cols]

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
    filename = 'nsd_links'
    nsd = read_or_create_dataframe(filename, b3.cols_nsd)
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

    nsd = nsd_recent_new.copy()

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
    dre.loc[:, 'Companhia'] = dre['Companhia'].str.replace(' EM RECUPERACAO JUDICIAL', '')
    dre.loc[:, 'Companhia'] = dre['Companhia'].str.replace(' EM LIQUIDACAO EXTRAJUDICIAL', '')
    dre.loc[:, 'Companhia'] = dre['Companhia'].str.replace(' EM LIQUIDACAO', '')

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
      try:
        item = f'{key[0]} {datetime.datetime.strptime(key[1], "%d/%m/%Y").year}'
      except Exception as e:
        item = f'{key[0]} {key[1].year}'
      if item not in years:
          years.append(item)

  return years

def process_dataframe(df):
    try:
      df['Trimestre'] = pd.to_datetime(df['Trimestre'], format='%d/%m/%Y')
      # df = df.assign(updated = lambda x: x['Companhia'].astype('string') + ' ' + x['Trimestre'].dt.year.astype(str))

      num_chunks = int(np.ceil(len(df) / b3.chunksize))
      df_updated = pd.DataFrame()
      for i in range(num_chunks):
          df_chunk = df.iloc[i * b3.chunksize: (i + 1) * b3.chunksize]
          df_chunk = df_chunk.assign(updated = lambda x: x['Companhia'].astype('string') + ' ' + x['Trimestre'].dt.year.astype('string'))
          df_updated = pd.concat([df_updated, df_chunk], ignore_index=True)

    except Exception as e:
        pass
    return df_updated

def fix_to_datetime(df, column):
    
  try:
    df[column] = df[column].apply(lambda x: pd.to_datetime(x, format='%d/%m/%Y', errors='ignore'))
  except Exception as e:
     pass
  try:
    df[column] = df[column].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='ignore'))
  except Exception as e:
     pass
  return df

def process_dataframe_trimestre(df):
    try:
      df = fix_to_datetime(df, 'Trimestre')

      num_chunks = int(np.ceil(len(df) / b3.chunksize))
      df_updated = pd.DataFrame()
      
      if num_chunks == 0:
        df['demosheet'] = ''
        df_updated = df      
      else:
        for i in range(num_chunks):
          df_chunk = df.iloc[i * b3.chunksize: (i + 1) * b3.chunksize]
          df_chunk = df_chunk.assign(demosheet = lambda x: x['Companhia'].astype('string') + ' ' + x['Trimestre'].dt.strftime('%d/%m/%Y'))
          df_updated = pd.concat([df_updated, df_chunk], ignore_index=True)

    except Exception as e:
        pass
    return df_updated

def dre_prepare(dre_raw, dre_math):
  years = get_dre_years(dre_raw, dre_math)

  # create 'update' columns
  dre_raw = process_dataframe(dre_raw)
  dre_math = process_dataframe(dre_math)

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

  # # format to string
  # try:
  #   dre_raw['Trimestre'] = dre_raw['Trimestre'].dt.strftime('%d/%m/%Y')
  # except Exception as e:
  #   pass
  # try:
  #   dre_math['Trimestre'] = dre_math['Trimestre'].dt.strftime('%d/%m/%Y')
  # except Exception as e:
  #   pass

  return dre_raw, dre_math

def get_math(dre_raw, dre_math):
   # do the math
  math = dre_raw.groupby([dre_raw['Companhia'], dre_raw['Trimestre'].dt.year, dre_raw['Conta']], group_keys=False)

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

def math_magic(key, df, size, cias, l):
  progress = (l/size)
  if key in cias:
      status = True
      if l % (b3.bin_size*10) == 0:
          print(f'{l} {(size-l)} {progress:.4%}')
      # print(key, 'done')
      pass
  else:
      status = False
      # print(f'{l} {(size-l)} {progress:.4%} {key[0]} {key[1]} {key[2]}')
      cias.append(key)

      # remove df duplicates Trimestres and keep higher/newer nsd values
      df = df.drop_duplicates(subset=['Trimestre'], keep='last').sort_values('Url', ascending=False)
      if df.iloc[0,3][:1] in b3.last_quarters or df.iloc[0,3][:1] in b3.all_quarters:
          i3 = i6 = i9 = i12 = 0
          v3 = v6 = v9 = v12 = 0

          # find out values for each month
          try:
              df_march = df[df['Trimestre'].dt.month == 3]
              i3 = df_march.index[0]
              v3 = df_march['Valor'].max()
          except Exception as e:
              pass
          try:
              df_june = df[df['Trimestre'].dt.month == 6]
              i6 = df_june.index[0]
              v6 = df_june['Valor'].max()
          except Exception as e:
              pass
          try:
              df_september = df[df['Trimestre'].dt.month == 9]
              i9 = df_september.index[0]
              v9 = df_september['Valor'].max()

          except Exception as e:
              pass
          try:
              df_december = df[df['Trimestre'].dt.month == 12]
              i12 = df_december.index[0]
              v12 = df_december['Valor'].max()
          except Exception as e:
              pass

          # do the @#$%&! b3 math
          try:
              if df.iloc[0,3][:1] in b3.last_quarters:
                  v12 = v12 - (v9 + v6 + v3)
          except Exception as e:
              print('last_quarters', e, df.iloc[0])

          try:
              if df.iloc[0,3][:1] in b3.all_quarters:
                  v3 = v3 - 0
                  v6 = v6 - (v3)
                  v9 = v9 - (v6 + v3)
                  v12 = v12 - (v9 + v6 + v3)

          except Exception as e:
              print('all_quarters', e, df.iloc[0])

          # update values
          if i3 != 0 and v3:
              df.loc[i3, 'Valor'] = [v3]
          if i6 != 0 and v6:
              df.loc[i6, 'Valor'] = [v6]
          if i9 != 0 and v9:
              df.loc[i9, 'Valor'] = [v9]
          if i12 != 0 and v12:
              df.loc[i12, 'Valor'] = [v12]

  return df, cias, status, key

# intel pre inteligence
def division(div1, div2):
    try:
        result = div1/div2
    except Exception as e:
        result = 0
    return result

def list_merge(li1, li2):
    # merge li1 + li2 and remove duplicates ['a', 'b'] + ['b', 'c'] = ['a', 'b', 'c']
    li3 = []
    [li3.append(i) for i in li1 + li2 if i not in li3]
    return li3

def list_subtract(li1, li2):
    # remove li2 from li1  ['a', 'b'] - ['b', 'c'] = ['a']
    li3 = [i for i in li1 if i not in li2]
    return li3

def list_inclusives(li1, li2):
    # only common_terms ['a', 'b'] and ['b', 'c'] = ['b']
    li3 = [value for value in li1 if value in li2]
    return li3

def list_exclusives(li1, li2):
    # only unique items from both lists ['a', 'b'] - ['b', 'c'] = ['a', 'c']
    li3 = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li3

def item_to_list(item):
    if type(item) is str:
        item = [item]
    if type(item) is tuple:
        item = list(item)
    if type(item) is list:
        item = [clean_text(word) for word in item]
        item = '|'.join(item)

    return item

def filter_df_old(df='', line='', exact='', exact_exclusion='', startswith='', startswith_not='', endswith='', endswith_not='', contains='', contains_not='', levelmin='', levelmax=''):
    mask = ''

    try:
        if line != '':
            empty_mask = ~((df.index == False) & (df.index == True))
            exact_mask = exact_exclusion_mask = startswith_mask = startswith_not_mask = endswith_mask = endswith_not_mask = contains_mask = contains_not_mask = levelmin_mask = levelmax_mask = empty_mask

            # exact
            if exact != '':
                item = exact
                exact_mask = (df[line] == item).replace({np.nan: False})

            # exact exclusion
            if exact_exclusion != '':
                item = exact_exclusion
                exact_exclusion_mask = ~(df[line] == item).replace({np.nan: False})

            # startswith
            if startswith != '':
                item = item_to_list(startswith)
                item = item.split('|')[0]
                startswith_mask = (df[line].apply(lambda word: clean_text(word)).str[:len(item)] == item).replace({np.nan: False})

            # startswith_not
            if startswith_not != '':
                item = item_to_list(startswith_not)
                item = item.split('|')[0]
                startswith_not_mask = ~(df[line].apply(lambda word: clean_text(word)).str[:len(item)] == item).replace({np.nan: False})

            # endswith
            if endswith != '':
                item = item_to_list(endswith)
                item = item.split('|')[0]
                endswith_mask = (df[line].apply(lambda word: clean_text(word)).str[-len(item):] == item).replace({np.nan: False})

            # endswith_not
            if endswith_not != '':
                item = item_to_list(endswith_not)
                item = item.split('|')[0]
                endswith_not_mask = ~(df[line].apply(lambda word: clean_text(word)).str[-len(item):] == item).replace({np.nan: False})

            # contains
            if contains != '':
                item = item_to_list(contains)
                contains_mask = df[line].apply(lambda word: clean_text(word)).str.contains(item, case=False).replace({np.nan: False})

            # contains_not
            if contains_not != '':
                item = item_to_list(contains_not)
                contains_not_mask = ~df[line].apply(lambda word: clean_text(word)).str.contains(item, case=False).replace({np.nan: False})

            # levelmin
            if levelmin != '':
                item = int(levelmin)
                levelmin_mask = df[line].str.len() >= 1+(item-1)*3

            # levelmax
            if levelmax != '':
                item = int(levelmax)
                levelmax_mask = df[line].str.len() <= 1+(item-1)*3


            mask = exact_mask & exact_exclusion_mask & startswith_mask & startswith_not_mask & endswith_mask & endswith_not_mask & contains_mask & contains_not_mask & levelmin_mask & levelmax_mask
    except Exception as e:
        print('error zise 0')    

    return mask

def filter_df(df='', line='', exact='', exact_exclusion='', startswith='', startswith_not='', endswith='', endswith_not='', contains='', contains_not='', levelmin='', levelmax=''):
    mask = pd.Series(True, index=df.index)

    try:
        if line != '':
            # exact
            if exact != '':
                mask &= (df[line] == exact)

            # exact exclusion
            if exact_exclusion != '':
                mask &= ~(df[line] == exact_exclusion)

            cleaned = df[line].str.strip()

            # startswith
            if startswith != '':
                mask &= cleaned.str.startswith(startswith)

            # startswith_not
            if startswith_not != '':
                mask &= ~cleaned.str.startswith(startswith_not)

            # endswith
            if endswith != '':
                mask &= cleaned.str.endswith(endswith)

            # endswith_not
            if endswith_not != '':
                mask &= ~cleaned.str.endswith(endswith_not)

            # contains
            if contains != '':
                mask &= cleaned.str.contains(contains, case=False)

            # contains_not
            if contains_not != '':
                mask &= ~cleaned.str.contains(contains_not, case=False)

            # levelmin
            if levelmin != '':
                mask &= (cleaned.str.len() >= 1+(int(levelmin)-1)*3)

            # levelmax
            if levelmax != '':
                mask &= (cleaned.str.len() <= 1+(int(levelmax)-1)*3)

    except Exception as e:
        print(f'error zise 0: {e}')    

    return mask

def filter_conditions(df, line, conditions):
    mask = pd.Series(True, index=df.index)

    for condition, value in conditions.items():
        operation = condition.split('_', 1)[1]
        if operation in ["startswith", "startswith_not", "endswith", "endswith_not", "contains", "contains_not"]:
            value = item_to_list(value)

        if operation == "exact":
            mask &= (df[line] == value).replace({np.nan: False})
        elif operation == "exact_exclusion":
            mask &= (df[line] != value).replace({np.nan: False})
        elif operation == "startswith":
            mask &= (df[line].apply(lambda word: clean_text(word)).str[:len(value)] == value).replace({np.nan: False})
        elif operation == "startswith_not":
            mask &= (df[line].apply(lambda word: clean_text(word)).str[:len(value)] != value).replace({np.nan: False})
        elif operation == "endswith":
            mask &= (df[line].apply(lambda word: clean_text(word)).str[-len(value):] == value).replace({np.nan: False})
        elif operation == "endswith_not":
            mask &= (df[line].apply(lambda word: clean_text(word)).str[-len(value):] != value).replace({np.nan: False})
        elif operation == "contains":
            mask &= df[line].str.contains(value, case=False).replace({np.nan: False})
        elif operation == "contains_not":
            mask &= ~df[line].str.contains(value, case=False).replace({np.nan: False})
        elif operation == "levelmin":
            mask &= (df[line].str.len() >= 1 + (int(value) - 1) * 3).replace({np.nan: False})
        elif operation == "levelmax":
            mask &= (df[line].str.len() <= 1 + (int(value) - 1) * 3).replace({np.nan: False})

    return mask

def get_dtp_line_old(df='', demo='', name='', 
    conta_exact='', conta_exact_exclusion='', conta_startswith='', conta_startswith_not='', conta_endswith='', conta_endswith_not='', conta_contains='', conta_contains_not='', conta_levelmin='', conta_levelmax='', 
    descricao_exact='', descricao_exact_exclusion='', descricao_startswith='', descricao_startswith_not='', descricao_endswith='', descricao_endswith_not='', descricao_contains='', descricao_contains_not=''
    ):
    '''
    Return filtered DRE using 'Conta' and 'Descrição' and combinations parameters. Inform dataframe and name for exclusive line
    
    Options are 'exact', 'startswith', 'endswith', contains', positive or negative with '_not'. Exclusive for Conta: 'levelmin' and 'levelmax' of hierarquical levels

    Optional Parameters for Conta
    ----------
    conta_exact : str
        Get all exact string in 'Conta'

    conta_exact_exclusion : str
        Get all but exact string in 'Conta'

    conta_startswith : str
        Get all starting with string in 'Conta'

    conta_startswith_not : str
        Get all but starting with string in 'Conta'

    conta_endswith : str
        Get all ending with string in 'Conta'

    conta_endswith_not : str
        Get all but ending with string in 'Conta'

    conta_contains : str
        Get all containing strings in 'Conta'

    conta_contains_not : str
        Get all but containing strings in 'Conta'

    Optional Parameters for Descrição
    ----------
    descricao_exact : str
        Get all exact string in 'Descrição'

    descricao_exact_exclusion : str
        Get all but exact string in 'Descrição'

    descricao_startswith : str
        Get all starting with string in 'Descrição'

    descricao_startswith_not : str
        Get all but starting with string in 'Descrição'

    descricao_endswith : str
        Get all ending with string in 'Descrição'

    descricao_endswith_not : str
        Get all but ending with string in 'Descrição'

    descricao_contains : str
        Get all containing strings in 'Descrição'

    descricao_contains_not : str
        Get all but containing strings in 'Descrição'

    Returns
    -------
    df
        Returns filtered dataframe

'''
    try:

        empty_mask = ~((df.index == False) & (df.index == True))
        mask_conta = mask_descricao = empty_mask

        if conta_exact or conta_exact_exclusion or conta_startswith or conta_startswith_not or conta_endswith or conta_endswith_not or conta_contains or conta_contains_not or conta_levelmin or conta_levelmax:
            mask_conta = filter_df(line='Conta', df=df, exact=conta_exact, exact_exclusion=conta_exact_exclusion, startswith=conta_startswith, startswith_not=conta_startswith_not, endswith=conta_endswith, endswith_not=conta_endswith_not, contains=conta_contains, contains_not=conta_contains_not, levelmin=conta_levelmin, levelmax=conta_levelmax)

        if descricao_exact or descricao_exact_exclusion or descricao_startswith or descricao_startswith_not or descricao_endswith or descricao_endswith_not or descricao_contains or descricao_contains_not:
            mask_descricao = filter_df(line='Descrição', df=df, exact=descricao_exact, exact_exclusion=descricao_exact_exclusion, startswith=descricao_startswith, startswith_not=descricao_startswith_not, endswith=descricao_endswith, endswith_not=descricao_endswith_not, contains=descricao_contains, contains_not=descricao_contains_not)

        if len(df[mask_conta & mask_descricao]) > 0:
            dict_empty = {}
            dict_empty['Companhia'] = df.loc[df.index[0], 'Companhia']
            dict_empty['Trimestre'] = df.loc[df.index[0], 'Trimestre']
            dict_empty['Demonstrativo'] = demo
            dict_empty['Conta'] = name.split(' - ')[0]
            dict_empty['Descrição'] = name.split(' - ')[1]
            dict_empty['Valor'] = df[mask_conta & mask_descricao]['Valor'].max()
            dict_empty['Url'] = df.loc[df.index[0], 'Url']
            dict_empty['nsd'] = df.loc[df.index[0], 'nsd']
            result = pd.DataFrame([dict_empty])
            # result = df[mask_conta & mask_descricao]
        else:
            dict_empty = {}
            dict_empty['Companhia'] = df.loc[df.index[0], 'Companhia']
            dict_empty['Trimestre'] = df.loc[df.index[0], 'Trimestre']
            dict_empty['Demonstrativo'] = demo
            dict_empty['Conta'] = name.split(' - ')[0]
            dict_empty['Descrição'] = name.split(' - ')[1]
            dict_empty['Valor'] = 0.0
            dict_empty['Url'] = df.loc[df.index[0], 'Url']
            dict_empty['nsd'] = df.loc[df.index[0], 'nsd']
            result = pd.DataFrame([dict_empty])
    except Exception as e:
        print('xc', e)    

    return result

def get_dtp_line_gtp1(df='', demo='', name='', 
    conta_exact='', conta_exact_exclusion='', conta_startswith='', conta_startswith_not='', conta_endswith='', conta_endswith_not='', conta_contains='', conta_contains_not='', conta_levelmin='', conta_levelmax='', 
    descricao_exact='', descricao_exact_exclusion='', descricao_startswith='', descricao_startswith_not='', descricao_endswith='', descricao_endswith_not='', descricao_contains='', descricao_contains_not=''
    ):

    mask_conta = filter_df(line='Conta', df=df, exact=conta_exact, exact_exclusion=conta_exact_exclusion, startswith=conta_startswith, startswith_not=conta_startswith_not, endswith=conta_endswith, endswith_not=conta_endswith_not, contains=conta_contains, contains_not=conta_contains_not, levelmin=conta_levelmin, levelmax=conta_levelmax)
    mask_descricao = filter_df(line='Descrição', df=df, exact=descricao_exact, exact_exclusion=descricao_exact_exclusion, startswith=descricao_startswith, startswith_not=descricao_startswith_not, endswith=descricao_endswith, endswith_not=descricao_endswith_not, contains=descricao_contains, contains_not=descricao_contains_not)

    dict_empty = {}
    dict_empty['Companhia'] = df.loc[df.index[0], 'Companhia']
    dict_empty['Trimestre'] = df.loc[df.index[0], 'Trimestre']
    dict_empty['Demonstrativo'] = demo
    dict_empty['Conta'] = name.split(' - ')[0]
    dict_empty['Descrição'] = name.split(' - ')[1]
    dict_empty['Valor'] = 0.0  # Initialize the value with 0.0
    dict_empty['Url'] = df.loc[df.index[0], 'Url']
    dict_empty['nsd'] = df.loc[df.index[0], 'nsd']

    filtered_df = df[mask_conta & mask_descricao]

    if len(filtered_df) > 0:
        dict_empty['Valor'] = filtered_df['Valor'].max()

    result = pd.DataFrame([dict_empty])

    return result

def get_dtp_line(df, demo, name, **conditions):
    conditions_conta = {k: v for k, v in conditions.items() if k.startswith('conta_')}
    conditions_descricao = {k: v for k, v in conditions.items() if k.startswith('descricao_')}

    mask_conta = filter_conditions(df, 'Conta', conditions_conta)
    mask_descricao = filter_conditions(df, 'Descrição', conditions_descricao)
    mask = mask_conta & mask_descricao

    # Populate result dataframe based on the mask
    try:
        line = {
            'Companhia': df.loc[df.index[0], 'Companhia'],
            'Trimestre': df.loc[df.index[0], 'Trimestre'],
            'Demonstrativo': demo,
            'Conta': name.split(' - ')[0],
            'Descrição': name.split(' - ')[1],
            'Valor': df[mask]['Valor'].max() if len(df[mask]) > 0 else 0.0,
            'Url': df.loc[df.index[0], 'Url'],
            'nsd': df.loc[df.index[0], 'nsd']
        }
    except Exception as e:
       pass    
    return pd.DataFrame([line])

def get_dtp_lines(df, demo, df_lines):
    dtp = [] # demonstrativos trimestrais padronizados

    for name, conditions in df_lines:
        kwargs = {}
        for condition, value in conditions:
            kwargs[condition] = value

        line = get_dtp_line(df=df, demo=demo, name=name, **kwargs)
        dtp.append(line)

    return pd.concat(dtp, ignore_index=True)

# intel pre fundamentalist
def eval_formula(md, formula):
  try:
    result = eval(formula)
  except Exception as e:
    result = None
    # print(f'error {e} in {formula}')
  return result
     
def fundamentaline(line, title='', valor=''):
    fsdesc = 'Descrição'
    fscol = 'Conta'
    fsval = 'Valor'
    
    sep = ' - '
    conta = title.split(sep)[0]
    desc = title.replace(conta + sep, '')

    line[fsdesc] = desc
    line[fscol] = conta
    line[fsval] = valor

    return line

def add_fundamental_line(df, line, title, valor=None):
    fsdesc = 'Descrição'
    fscol = 'Conta'
    fsval = 'Valor'
    sep = ' - '

    conta = title.split(sep)[0]
    desc = title.replace(conta + sep, '')

    new_line = line.copy()
    new_line[fsdesc] = desc
    new_line[fscol] = conta
    new_line[fsval] = valor

    df = pd.concat([df, pd.DataFrame([line])], ignore_index=True).drop_duplicates()
    return df

def calc_fundamentalist(md, *keys):
  try:
    return sum(md[key] for key in keys)
  except Exception as e:
    return 0.0

def get_new_lines(md, line):
  try:
    # formulas
    formulas = [
      # Relações Entre Ativos e Passivos
        ('_020302_reservas_de_capital', '_020303_reservas_de_reavaliacao', '_020304_reservas_de_lucros'),
      # Dívida
        ('_0201040101_emprestimos_e_financiamentos_em_moeda_nacional', '_0201040102_emprestimos_e_financiamentos_em_moeda_estrangeira', '_02010402_debentures', '_02010403_arrendamentos', '_02010409_outros_emprestimos_financiamentos_e_debentures'),
        ('_0202010101_emprestimos_e_financiamentos_em_moeda_nacional', '_0202010102_emprestimos_e_financiamentos_em_moeda_estrangeira', '_02020102_debentures', '_02020103_arrendamentos', '_02020209_outros_emprestimos_financiamentos_e_debentures'),
        ('_0201040102_emprestimos_e_financiamentos_em_moeda_estrangeira', '_0202010102_emprestimos_e_financiamentos_em_moeda_estrangeira'),
        ('_010101_caixa_e_disponibilidades_de_caixa',),
        ('_010202_investimentos_nao_capex', '_010203_imobilizados', '_010204_intangivel'),
        ('_0305_lajir_ebit_resultado_antes_do_resultado_financeiro_e_dos_tributos', '_070401_depreciacao_e_amortizacao'),
      # Resultados Fundamentalistas
        ('_0203_patrimonio_liquido',),
        ('_010101_caixa_e_disponibilidades_de_caixa',),
        ('_070803_remuneracao_de_capital_de_terceiros', '_070804_remuneracao_de_capital_proprio'),
      # Análise do Fluxo de Caixa
        ('_0601_caixa_das_operacoes', '_0602_caixa_de_investimentos_capex'),
        ('_0603_caixa_de_financiamento',),
        ('_060201_investimentos', '_060202_imobilizado_e_intangivel'),
    ]

    results = [calc_fundamentalist(md, *keys) for keys in formulas]
    r = results[0]
    dbcp = results[1]
    dblp = results[2]
    dme = results[3]
    dmn = dbcp + dblp - dme
    dl = -1 * ((dbcp + dblp) - results[4])
    pi = results[5]
    ebitda = results[6]
    ci_base = results[7]
    caixa_e_disponibilidades_de_caixa = results[8]
    rc = results[9]
    cl = results[10]
    ct = cl + results[11]
    ci = results[12]
  except Exception as e:
    pass

  # lines
  try:
    new_lines = []
    # Relações Entre Ativos e Passivos
    line['Demonstrativo'] = 'Relações entre Ativos e Passivos'
    new_lines.append(fundamentaline(line=line.copy(), title='11.01.01 - Capital de Giro (Ativos Circulantes - Passivos Circulantes)', valor=eval_formula(md, "md['_0101_ativo_circulante_de_curto_prazo']-md['_0201_passivo_circulante_de_curto_prazo']")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.01.02 - Liquidez (Ativos Circulantes por Passivos Circulantes)', valor=eval_formula(md, "division(md['_0101_ativo_circulante_de_curto_prazo'], md['_0201_passivo_circulante_de_curto_prazo'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.01.03 - Ativos Circulantes de Curto Prazo por Ativos', valor=eval_formula(md, "division(md['_0101_ativo_circulante_de_curto_prazo'],md['_01_ativo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.01.04 - Ativos Não Circulantes de Longo Prazo por Ativos', valor=eval_formula(md, "division(md['_0102_ativo_nao_circulante_de_longo_prazo'],md['_01_ativo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.02 - Passivos por Ativos', valor=eval_formula(md, "division((md['_02_passivo_total']-md['_0203_patrimonio_liquido']),md['_01_ativo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.02.01 - Passivos Circulantes de Curto Prazo por Ativos', valor=eval_formula(md, "division(md['_0201_passivo_circulante_de_curto_prazo'],md['_01_ativo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.02.02 - Passivos Não Circulantes de Longo Prazo por Ativos', valor=eval_formula(md, "division(md['_0202_passivo_circulante_de_longo_prazo'],md['_01_ativo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.02.03 - Passivos Circulantes de Curto Prazo por Passivos', valor=eval_formula(md, "division(md['_0201_passivo_circulante_de_curto_prazo'],md['_02_passivo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.02.04 - Passivos Não Circulantes de Longo Prazo por Passivos', valor=eval_formula(md, "division(md['_0202_passivo_circulante_de_longo_prazo'],md['_02_passivo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.03 - Patrimônio Líquido por Ativos', valor=eval_formula(md, "division(md['_0203_patrimonio_liquido'],md['_01_ativo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido)', valor=eval_formula(md, "division(md['_01_ativo_total'],md['_0203_patrimonio_liquido'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.03.02 - Passivos por Patrimônio Líquido', valor=eval_formula(md, "division((md['_0201_passivo_circulante_de_curto_prazo']+md['_0202_passivo_circulante_de_longo_prazo']),md['_0203_patrimonio_liquido'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.03.02.01 - Passivos Circulantes de Curto Prazo por Patrimônio Líquido', valor=eval_formula(md, "division(md['_0201_passivo_circulante_de_curto_prazo'],md['_0203_patrimonio_liquido'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.03.02.02 - Passivos Não Circulantes de Longo Prazo por Patrimônio Líquido', valor=eval_formula(md, "division(md['_0202_passivo_nao_circulante_de_longo_prazo'],md['_0203_patrimonio_liquido'])")))

    # Patrimônio
    line['Demonstrativo'] = 'Patrimônio'
    new_lines.append(fundamentaline(line=line.copy(), title='11.04 - Capital Social por Patrimônio Líquido', valor=eval_formula(md, "division(md['_020301_capital_social'],md['_0203_patrimonio_liquido'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='11.05 - Reservas por Patrimônio Líquido', valor=eval_formula(md, "division(r,md['_0203_patrimonio_liquido'])")))

    # Dívida
    line['Demonstrativo'] = 'Dívida'
    new_lines.append(fundamentaline(line=line.copy(), title='12.01 - Dívida Bruta', valor=eval_formula(md, "db")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.01.01 - Dívida Bruta Circulante de Curto Prazo', valor=eval_formula(md, "dbcp")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.01.02 - Dívida Bruta Não Circulante de Longo Prazo', valor=eval_formula(md, "dblp")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.01.03 - Dívida Bruta Circulante de Curto Prazo por Dívida Bruta', valor=eval_formula(md, "division(dbcp, db)")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.01.04 - Dívida Bruta Não Circulante de Longo Prazo por Dívida Bruta', valor=eval_formula(md, "division(dblp, db)")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.01.05 - Dívida Bruta em Moeda Nacional', valor=eval_formula(md, "dmn")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.01.06 - Dívida Bruta em Moeda Estrangeira', valor=eval_formula(md, "dme")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.01.07 - Dívida Bruta em Moeda Nacional por Dívida Bruta', valor=eval_formula(md, "division(dmn, db")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.01.08 - Dívida Bruta em Moeda Estrangeira por Dívdida Bruta', valor=eval_formula(md, "division(dme, db")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.02.01 - Dívida Bruta por Patrimônio Líquido', valor=eval_formula(md, "division(db,md['_0203_patrimonio_liquido'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.02.02 - Endividamento Financeiro', valor=eval_formula(md, "division(db,(db+md['_0203_patrimonio_liquido'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.03 - Patrimônio Imobilizado em Capex, Investimentos Não Capex e Intangível Não Capex', valor=eval_formula(md, "pi")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.03.01 - Patrimônio Imobilizado por Patrimônio Líquido', valor=eval_formula(md, "division(pi,md['_0203_patrimonio_liquido'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.04 - Dívida Líquida', valor=eval_formula(md, "dl")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.04.01 - Dívida Líquida por EBITDA', valor=eval_formula(md, "division(dl,ebitda")))
    new_lines.append(fundamentaline(line=line.copy(), title='12.04.01 - Serviço da Dívida (Dívida Líquida por Resultado)', valor=eval_formula(md, "division(dl,md['_0311_lucro_liquido'])")))

    # Resultados Fundamentalistas
    line['Demonstrativo'] = 'Resultados Fundamentalistas'
    new_lines.append(fundamentaline(line=line.copy(), title='13.03 - Contas a Receber por Faturamento', valor=eval_formula(md, "division((md['_010103_contas_a_receber']+md['_01020103_contas_a_receber']),md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.03.01 - Contas a Receber Não Circulantes de Curto Prazo por Faturamento', valor=eval_formula(md, "division(md['_010103_contas_a_receber'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.03.02 - Contas a Receber Circulantes de Longo Prazo por Faturamento', valor=eval_formula(md, "division(md['_01020103_contas_a_receber'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.04 - Estoques por Faturamento', valor=eval_formula(md, "division((md['_010104_estoques']+md['_01020104_estoques']),md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.04.01 - Estoques Não Circulantes de Curto Prazo por Faturamento', valor=eval_formula(md, "division(md['_010104_estoques'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.04.02 - Estoques Circulantes de Longo Prazo por Faturamento', valor=eval_formula(md, "division(md['_01020104_estoques'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.05 - Ativos Biológicos por Faturamento', valor=eval_formula(md, "division((md['_010105_ativos_biologicos']+md['_01020105_ativos_biologicos']),md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.05.01 - Ativos Biológicos Não Circulantes de Curto Prazo por Faturamento', valor=eval_formula(md, "division(md['_010105_ativos_biologicos'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.05.02 - Ativos Biológicos Circulantes de Longo Prazo por Faturamento', valor=eval_formula(md, "division(md['_01020105_ativos_biologicos'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.06 - Tributos por Faturamento', valor=eval_formula(md, "division((md['_010106_tributos']+md['_01020106_tributos']),md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.06.01 - Tributos Não Circulantes de Curto Prazo por Faturamento', valor=eval_formula(md, "division(md['_010106_tributos'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.06.02 - Tributos Circulantes de Longo Prazo por Faturamento', valor=eval_formula(md, "division(md['_01020106_tributos'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.07 - Despesas por Faturamento', valor=eval_formula(md, "division((md['_010107_despesas']+md['_01020107_despesas']),md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.07.01 - Despesas Não Circulantes de Curto Prazo por Faturamento', valor=eval_formula(md, "division(md['_010107_despesas'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.07.02 - Despesas Circulantes de Longo Prazo por Faturamento', valor=eval_formula(md, "division(md['_01020107_despesas'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.09 - Outros Ativos por Faturamento', valor=eval_formula(md, "division((md['_010109_outros_ativos_circulantes']+md['_01020109_outros_ativos_nao_circulantes']),md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.09.01 - Outros Ativos Não Circulantes de Curto Prazo por Faturamento', valor=eval_formula(md, "division(md['_010109_outros_ativos_circulantes'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='13.09.02 - Outros Ativos Não Circulantes de Longo Prazo por Faturamento', valor=eval_formula(md, "division(md['_01020109_outros_ativos_nao_circulantes'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='14.01.01 - Receita por Ativos', valor=eval_formula(md, "division(md['_0301_receita_bruta'],md['_01_ativo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='14.01.02 - Receita por Patrimônio', valor=eval_formula(md, "division(md['_0301_receita_bruta'],md['_0203_patrimonio_liquido'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='14.02.01 - Coeficiente de Retorno (Resultado por Ativos)', valor=eval_formula(md, "division(md['_0311_lucro_liquido'],md['_01_ativo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='14.02.02 - ROE (Resultado por Patrimônio)', valor=eval_formula(md, "division(md['_0311_lucro_liquido'],md['_0203_patrimonio_liquido'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='14.03 - Capital Investido', valor=eval_formula(md, "ci")))
    new_lines.append(fundamentaline(line=line.copy(), title='14.03.01 - ROIC (Retorno por Capital Investido)', valor=eval_formula(md, "division(md['_0311_lucro_liquido'],ci")))
    new_lines.append(fundamentaline(line=line.copy(), title='14.04.01 - ROAS (EBIT por Ativos)', valor=eval_formula(md, "division(md['_0305_lajir_ebit_resultado_antes_do_resultado_financeiro_e_dos_tributos'],md['_01_ativo_total'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='15.01 - Remuneração de Capital', valor=eval_formula(md, "rc")))
    new_lines.append(fundamentaline(line=line.copy(), title='15.01.01 - Remuneração de Capital de Terceiros por Remuneração de Capital', valor=eval_formula(md, "division(md['_070803_remuneracao_de_capital_de_terceiros'],rc")))
    new_lines.append(fundamentaline(line=line.copy(), title='15.01.01.01 - Juros Pagos por Remuneração de Capital de Terceiros', valor=eval_formula(md, "division(md['_07080301_juros_pagos'],md['_070803_remuneracao_de_capital_de_terceiros'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='15.01.01.02 - Aluguéis por Remuneração de Capital de Terceiros', valor=eval_formula(md, "division(md['_07080302_alugueis'],md['_070803_remuneracao_de_capital_de_terceiros'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='15.01.02 - Remuneração de Capital Próprio por Remuneração de Capital', valor=eval_formula(md, "division(md['_070804_remuneracao_de_capital_proprio'],rc")))
    new_lines.append(fundamentaline(line=line.copy(), title='15.01.02.01 - Juros Sobre o Capital Próprio por Remuneração de Capital Próprio', valor=eval_formula(md, "division(md['_07080401_juros_sobre_o_capital_proprio'],md['_070804_remuneracao_de_capital_proprio'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='15.01.02.02 - Dividendos por Remuneração de Capital Próprio', valor=eval_formula(md, "division(md['_07080402_dividendos'],md['_070804_remuneracao_de_capital_proprio'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='15.01.02.03 - Lucros Retidos por Remuneração de Capital Próprio', valor=eval_formula(md, "division(md['_07080403_lucros_retidos'],md['_070804_remuneracao_de_capital_proprio'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='15.02 - Remuneração de Capital por EBIT', valor=eval_formula(md, "division(rc,md['_0305_lajir_ebit_resultado_antes_do_resultado_financeiro_e_dos_tributos'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='15.02.01 - Impostos por EBIT', valor=eval_formula(md, "division(md['_0308_impostos_irpj_e_csll'],md['_0305_lajir_ebit_resultado_antes_do_resultado_financeiro_e_dos_tributos'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='16.01 - Margem Bruta (Resultado Bruto (Receita Líquida) por Receita Bruto)', valor=eval_formula(md, "division(md['_0303_resultado_bruto_receita_liquida'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='16.02 - Margem Operacional (Receitas Operacionais por Receita Bruta)', valor=eval_formula(md, "division(md['_0304_despesas_operacionais'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='16.02.01 - Força de Vendas (Despesas com Vendas por Despesas Operacionais)', valor=eval_formula(md, "division(md['_030401_despesas_com_vendas'],md['_0304_despesas_operacionais'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='16.02.02 - Peso Administrativo (Despesas com Administração por Despesas Operacionais)', valor=eval_formula(md, "division(md['_030402_despesas_gerais_e_administrativas'],md['_0304_despesas_operacionais'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='16.03 - Margem EBITDA (EBITDA por Resultado Bruto (Receita Líquida))', valor=eval_formula(md, "division(ebitda,md['_0303_resultado_bruto_receita_liquida'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='16.03.01 - Margem EBIT (EBIT por Resultado Bruto (Receita Líquida))', valor=eval_formula(md, "division(md['_0305_lajir_ebit_resultado_antes_do_resultado_financeiro_e_dos_tributos'],md['_0303_resultado_bruto_receita_liquida'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='16.03.02 - Margem de Depreciação por Resultado Bruto (Receita Líquida)', valor=eval_formula(md, "division(md['_070401_depreciacao_e_amortizacao'],md['_0303_resultado_bruto_receita_liquida'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='16.04 - Margem Não Operacional (Resultado Não Operacional por Resultado Bruto (Receita Líquida))', valor=eval_formula(md, "division(md['_0306_resultado_financeiro_nao_operacional'],md['_0303_resultado_bruto_receita_liquida'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='16.05 - Margem Líquida (Lucro Líquido por Receita Bruta)', valor=eval_formula(md, "division(md['_0311_lucro_liquido'],md['_0301_receita_bruta'])")))

    # Análise do Fluxo de Caixa
    line['Demonstrativo'] = 'Análise do Fluxo de Caixa'
    new_lines.append(fundamentaline(line=line.copy(), title='17.01 - Caixa Total', valor=eval_formula(md, "ct")))
    new_lines.append(fundamentaline(line=line.copy(), title='17.02 - Caixa Livre', valor=eval_formula(md, "cl")))
    new_lines.append(fundamentaline(line=line.copy(), title='17.03.01 - Caixa de Investimentos por Caixa das Operações', valor=eval_formula(md, "division(md['_0602_caixa_de_investimentos_capex'],md['_0601_caixa_das_operacoes'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='17.03.02 - Caixa de Investimentos por EBIT', valor=eval_formula(md, "division(md['_0602_caixa_de_investimentos_capex'],md['_0305_lajir_ebit_resultado_antes_do_resultado_financeiro_e_dos_tributos'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='17.04 - Caixa Imobilizado', valor=eval_formula(md, "ci")))
    new_lines.append(fundamentaline(line=line.copy(), title='17.05 - FCFF simplificado (Caixa Livre para a Firma)', valor=eval_formula(md, "md['_0601_caixa_das_operacoes']-ci")))
    new_lines.append(fundamentaline(line=line.copy(), title='17.06 - FCFE simplificado (Caixa Livre para os Acionistas)', valor=eval_formula(md, "md['_0601_caixa_das_operacoes']-ci-md['_0801_dividendos_minimos_obrigatorios'])")))

    # Análise de Valor Agragado
    line['Demonstrativo'] = 'Análise do Valor Agregado'
    new_lines.append(fundamentaline(line=line.copy(), title='18.01 - Margem de Vendas por Valor Agregado', valor=eval_formula(md, "division(md['_070101_vendas'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.02 - Custo dos Insumos por Valor Agregado', valor=eval_formula(md, "division(md['_0702_custos_dos_insumos'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.03 - Valor Adicionado Bruto por Valor Agregado', valor=eval_formula(md, "division(md['_0703_valor_adicionado_bruto'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.04 - Retenções por Valor Agregado', valor=eval_formula(md, "division(md['_0704_retencoes'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.05 - Valor Adicionado Líquido por Valor Agregado', valor=eval_formula(md, "division(md['_0705_valor_adicionado_liquido'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.06 - Valor Adicionado em Transferência por Valor Agregado', valor=eval_formula(md, "division(md['_0706_valor_adicionado_em_transferencia'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.07 - Recursos Humanos por Valor Agregado', valor=eval_formula(md, "division(md['_070801_pessoal'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.07.01 - Remuneração Direta (Recursos Humanos) por Valor Agregado', valor=eval_formula(md, "division(md['_07080101_remuneracao_direta'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.07.02 - Benefícios (Recursos Humanos) por Valor Agregado', valor=eval_formula(md, "division(md['_07080102_beneficios'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.07.03 - FGTS (Recursos Humanos) por Valor Agregado', valor=eval_formula(md, "division(md['_07080103_fgts'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.08 - Impostos por Valor Agregado', valor=eval_formula(md, "division(md['_070802_impostos_taxas_e_contribuicoes'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.09 - Remuneração de Capital de Terceiros por Valor Agregado', valor=eval_formula(md, "division(md['_070803_remuneracao_de_capital_de_terceiros'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.09.01 - Juros Pagos a Terceiros por Valor Agregado', valor=eval_formula(md, "division(md['_07080301_juros_pagos'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.09.02 - Aluguéis Pagos a Terceiros por Valor Agregado', valor=eval_formula(md, "division(md['_07080302_alugueis'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.10 - Remuneração de Capital Próprio por Valor Agregado', valor=eval_formula(md, "division(md['_070804_remuneracao_de_capital_proprio'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.10.01 - Juros Sobre Capital Próprio por Valor Agregado', valor=eval_formula(md, "division(md['_07080401_juros_sobre_o_capital_proprio'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.10.02 - Dividendos por Valor Agregado', valor=eval_formula(md, "division(md['_07080402_dividendos'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.10.02 - Lucros Retidos por Valor Agregado', valor=eval_formula(md, "division(md['_07080403_lucros_retidos'],md['_0707_valor_adicionado_total_a_distribuir'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.11.01 - Alíquota de Impostos (Impostos, Taxas e Contribuições por Receita Bruta)', valor=eval_formula(md, "division(md['_070802_impostos_taxas_e_contribuicoes'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.11.02 - Taxa de Juros Pagos (Remuneração de Capital de Terceiros por Receita Bruta', valor=eval_formula(md, "division(md['_070803_remuneracao_de_capital_de_terceiros'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.11.03 - Taxa de Proventos Gerados (Remuneração de Capital Próprio por Receita Bruta', valor=eval_formula(md, "division(md['_070804_remuneracao_de_capital_proprio'],md['_0301_receita_bruta'])")))
  except Exception as e:
    pass

  return new_lines

# intel
def inteligence_dre_old(df):
    try:
        demo0 = demo = 'Composição do Capital'
        df_a = get_dtp_line(df=df, demo=demo, name='00.01 - Ações Ordinárias', conta_exact='0.01')
        df_b = get_dtp_line(df=df, demo=demo, name='00.02 - Ações Preferenciais', conta_exact='0.02')
        df_c = get_dtp_line(df=df, demo=demo, name='00.01.01 - Ações Ordinárias em Tesouraria', conta_exact='0.01.01')
        df_d = get_dtp_line(df=df, demo=demo, name='00.01.02 - Ações Ordinárias Outras', conta_exact='0.01.02')
        df_e = get_dtp_line(df=df, demo=demo, name='00.02.01 - Ações Prerenciais em Tesouraria', conta_exact='0.02.01')
        df_f = get_dtp_line(df=df, demo=demo, name='00.02.02 - Ações Prerenciais Outras', conta_exact='0.02.02')
        d0 = pd.concat([df_a, df_b, df_c, df_d, df_e, df_f], ignore_index=True)

        demo1 = demo = 'Balanço Patrimonial Ativo'
        df_a = get_dtp_line(df=df, demo=demo, name='01 - Ativo Total', conta_exact='1')
        df_b = get_dtp_line(df=df, demo=demo, name='01.01 - Ativo Circulante de Curto Prazo', conta_exact='1.01')
        df_c = get_dtp_line(df=df, demo=demo, name='01.01.01 - Caixa e Disponibilidades de Caixa', conta_exact='1.01.01')
        df_d = get_dtp_line(df=df, demo=demo, name='01.01.02 - Aplicações Financeiras', conta_startswith='1.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['aplica', 'depósito', 'reserv', 'saldo', 'centra', 'interfinanceir', 'crédit'], conta_contains_not=['1.01.01', '1.01.02', '1.01.06'])
        df_e = get_dtp_line(df=df, demo=demo, name='01.01.03 - Contas a Receber', conta_startswith='1.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['conta'])
        df_f = get_dtp_line(df=df, demo=demo, name='01.01.04 - Estoques', conta_startswith='1.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['estoque'])
        df_g = get_dtp_line(df=df, demo=demo, name='01.01.05 - Ativos Biológicos', conta_startswith='1.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['biológic'])
        df_h = get_dtp_line(df=df, demo=demo, name='01.01.06 - Tributos', conta_startswith='1.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['tribut'])
        df_i = get_dtp_line(df=df, demo=demo, name='01.01.07 - Despesas', conta_startswith='1.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['despes'])
        df_j = get_dtp_line(df=df, demo=demo, name='01.01.09 - Outros Ativos Circulantes', conta_startswith='1.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains='outr', descricao_contains_not=['aplica', 'depósito', 'reserv', 'saldo', 'centra', 'interfinanceir', 'crédit', 'conta', 'estoque', 'biológic', 'tribut', 'despes'], conta_contains_not=['1.01.01', '1.01.02', '1.01.03', '1.01.04', '1.01.05', '1.01.06', '1.01.07'])
        df_k = get_dtp_line(df=df, demo=demo, name='01.02 - Ativo Não Circulante de Longo Prazo', conta_exact='1.02')
        df_l = get_dtp_line(df=df, demo=demo, name='01.02.01 - Ativos Financeiros', conta_startswith='1.02.', descricao_contains_not=['investiment', 'imobilizad', 'intangív'])
        df_m = get_dtp_line(df=df, demo=demo, name='01.02.01.01 - Ativos Financeiros a Valor Justo', conta_startswith='1.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains='valor justo', descricao_contains_not='custo amortizado')
        df_n = get_dtp_line(df=df, demo=demo, name='01.02.01.02 - Ativos Financeiros ao Custo Amortizado', conta_startswith='1.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains='custo amortizado', descricao_contains_not='valor justo')
        df_o = get_dtp_line(df=df, demo=demo, name='01.02.01.03 - Contas a Receber', conta_startswith='1.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains='conta')
        df_p = get_dtp_line(df=df, demo=demo, name='01.02.01.04 - Estoques', conta_startswith='1.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains='estoque')
        df_q = get_dtp_line(df=df, demo=demo, name='01.02.01.05 - Ativos Biológicos', conta_startswith='1.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains='biológic')
        df_r = get_dtp_line(df=df, demo=demo, name='01.02.01.06 - Tributos', conta_startswith='1.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains='tribut')
        df_s = get_dtp_line(df=df, demo=demo, name='01.02.01.07 - Despesas', conta_startswith='1.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains='despes')
        df_t = get_dtp_line(df=df, demo=demo, name='01.02.01.09 - Outros Ativos Não Circulantes', conta_startswith='1.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains_not=['valor justo', 'custo amortizado', 'conta', 'estoque', 'biológic', 'tribut', 'despes'])
        df_u = get_dtp_line(df=df, demo=demo, name='01.02.02 - Investimentos Não Capex', conta_startswith='1.02.', descricao_contains=['investiment'])
        df_v = get_dtp_line(df=df, demo=demo, name='01.02.02.01 - Propriedades - Investimentos Não Capex', conta_startswith='1.02.', conta_levelmin=3 ,descricao_contains=['propriedad'])
        df_w = get_dtp_line(df=df, demo=demo, name='01.02.02.02 - Arrendamentos - Investimentos Não Capex', conta_startswith='1.02.', conta_levelmin=3 ,descricao_contains=['arrendam'], descricao_contains_not=['sotware', 'imobilizad', 'intangív', 'direit'])
        df_x = get_dtp_line(df=df, demo=demo, name='01.02.03 - Imobilizados', conta_startswith='1.02.', descricao_contains=['imobilizad'])
        df_y = get_dtp_line(df=df, demo=demo, name='01.02.03.01 - Imobilizados em Operação', conta_startswith='1.02.03.', descricao_contains=['operaç'])
        df_z = get_dtp_line(df=df, demo=demo, name='01.02.03.02 - Imobilizados em Arrendamento', conta_startswith='1.02.03.', descricao_contains=['arrend'])
        df_aa = get_dtp_line(df=df, demo=demo, name='01.02.03.03 - Imobilizados em Andamento', conta_startswith='1.02.03.', descricao_contains=['andament'])
        df_ab = get_dtp_line(df=df, demo=demo, name='01.02.04 - Intangível', conta_startswith='1.02.', descricao_contains=['intangív'])
        df_ac = get_dtp_line(df=df, demo=demo, name='01.03 - Empréstimos', conta_startswith='1.', conta_levelmax=2, descricao_contains='empréstimo')
        df_ad = get_dtp_line(df=df, demo=demo, name='01.04 - Tributos Diferidos', conta_startswith='1.', conta_levelmax=2, descricao_contains='tributo')
        df_ae = get_dtp_line(df=df, demo=demo, name='01.05 - Investimentos', conta_startswith='1.', conta_levelmax=2, descricao_contains='investimento')
        df_af = get_dtp_line(df=df, demo=demo, name='01.05.01 - Participações em Coligadas', conta_startswith='1.', conta_levelmin=3, conta_levelmax=3, descricao_contains='coligad')
        df_ag = get_dtp_line(df=df, demo=demo, name='01.05.02 - Participações em Controladas', conta_startswith='1.', conta_levelmin=3, conta_levelmax=3, descricao_contains='controlad')
        df_ah = get_dtp_line(df=df, demo=demo, name='01.06 - Imobilizados', conta_startswith='1.', conta_levelmax=2, descricao_contains='imobilizado')
        df_ai = get_dtp_line(df=df, demo=demo, name='01.06.01 - Propriedades - Investimentos Não Capex', conta_startswith='1.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['1.02.'], descricao_contains=['propriedad', 'imóve'])
        df_aj = get_dtp_line(df=df, demo=demo, name='01.06.02 - Arrendamento - Investimentos Não Capex', conta_startswith='1.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['1.02.'], descricao_contains='arrendam')
        df_ak = get_dtp_line(df=df, demo=demo, name='01.06.03 - Tangíveis - Investimentos Não Capex', conta_startswith='1.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['1.02.'], descricao_contains=['arrendam', 'equipamento'])
        df_al = get_dtp_line(df=df, demo=demo, name='01.07 - Intangíveis', conta_startswith='1.', conta_levelmax=2, descricao_contains='intangíve')
        df_am = get_dtp_line(df=df, demo=demo, name='01.07.01 - Intangíveis', conta_startswith='1.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['1.02.'], descricao_contains='intangíve')
        df_an = get_dtp_line(df=df, demo=demo, name='01.07.02 - Goodwill', conta_startswith='1.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['1.02.'], descricao_contains='goodwill')
        df_ao = get_dtp_line(df=df, demo=demo, name='01.08 - Permanente', conta_startswith='1.0', conta_levelmax=2, descricao_contains='permanente')
        df_ap = get_dtp_line(df=df, demo=demo, name='01.09 - Outros Ativos', conta_startswith='1.0', conta_levelmax=2, conta_contains_not=['1.01', '1.02'], descricao_contains_not=['empréstimo', 'tributo', 'investimento', 'imobilizado', 'intangíve', 'permanente'])
        df_aq = get_dtp_line(df=df, demo=demo, name='01.09.01 - Depreciação e Amortização Acumuladas', conta_startswith='1.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['depreciaç', 'amortizaç'])
        df_ar = get_dtp_line(df=df, demo=demo, name='01.09.09 - Outros Ativos', conta_startswith='1.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['1.01.', '1.02'], descricao_contains_not=['depreciaç', 'amortizaç', 'empréstimo', 'tributo', 'investimento', 'imobilizado', 'intangíve', 'permanente', 'goodwill', 'arrendam', 'equipamento', 'propriedad', 'imóve', 'coligad', 'controlad'])
        d1 = pd.concat([df_a, df_b, df_c, df_d, df_e, df_f, df_g, df_h, df_i, df_j, df_k, df_l, df_m, df_n, df_o, df_p, df_q, df_r, df_s, df_t, df_u, df_v, df_w, df_x, df_y, df_z, df_aa, df_ab, df_ac, df_ad, df_ae, df_af, df_ag, df_ah, df_ai, df_aj, df_ak, df_al, df_am, df_an, df_ao, df_ap, df_aq, df_ar], ignore_index=True)
        
        demo2 = demo = 'Balanço Patrimonial Passivo'
        df_a = get_dtp_line(df=df, demo=demo, name='02 - Passivo Total', conta_exact='2')
        df_b = get_dtp_line(df=df, demo=demo, name='02.01 - Passivo Circulante de Curto Prazo', conta_startswith='2.', conta_levelmin=2, conta_levelmax=2, descricao_contains=['circulante', 'o resultado', 'amortizado', 'negociaç'], descricao_contains_not=['não', 'patrimônio', 'fisca'])
        df_c = get_dtp_line(df=df, demo=demo, name='02.01.01 - Obrigações Sociais e Trabalhistas', conta_startswith='2.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['obrigações sociais'])
        df_d = get_dtp_line(df=df, demo=demo, name='02.01.01.01 - Obrigações Sociais', conta_startswith='2.01.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['socia'])
        df_e = get_dtp_line(df=df, demo=demo, name='02.01.01.02 - Obrigações Trabalhistas', conta_startswith='2.01.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['trabalhista'])
        df_f = get_dtp_line(df=df, demo=demo, name='02.01.01.09 - Outras Obrigações', conta_startswith='2.01.01', conta_levelmin=4, conta_levelmax=4, descricao_contains_not=['socia', 'trabalhista'])
        df_g = get_dtp_line(df=df, demo=demo, name='02.01.02 - Fornecedores', conta_startswith='2.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['fornecedor'])
        df_h = get_dtp_line(df=df, demo=demo, name='02.01.02.01 - Fornecedores Nacionais', conta_startswith=['2.01.01.''2.01.02'], conta_levelmin=4, conta_levelmax=4, descricao_contains=['fornecedores nacionais'])
        df_i = get_dtp_line(df=df, demo=demo, name='02.01.02.02 - Fornecedores Estrangeiros', conta_startswith=['2.01.01.''2.01.02'], conta_levelmin=4, conta_levelmax=4, descricao_contains=['fornecedores estrangeiros'])
        df_j = get_dtp_line(df=df, demo=demo, name='02.01.03 - Obrigações Fiscais', conta_startswith='2.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['obrigaç', 'fisca'], descricao_contains_not='socia')
        df_k = get_dtp_line(df=df, demo=demo, name='02.01.03.01 - Obrigações Fiscais Federais', conta_startswith='2.01.03', conta_levelmin=4, conta_levelmax=4, descricao_contains=['federa'])
        df_l = get_dtp_line(df=df, demo=demo, name='02.01.03.02 - Obrigações Fiscais Estaduais', conta_startswith='2.01.03', conta_levelmin=4, conta_levelmax=4, descricao_contains=['estadua'])
        df_m = get_dtp_line(df=df, demo=demo, name='02.01.03.03 - Obrigações Fiscais Municipais', conta_startswith='2.01.03', conta_levelmin=4, conta_levelmax=4, descricao_contains=['municipa'])
        df_n = get_dtp_line(df=df, demo=demo, name='02.01.03.09 - Outras Obrigações Fiscais', conta_startswith='2.01.03', conta_levelmin=4, conta_levelmax=4, descricao_contains_not=['federa', 'estadua', 'municipa'])
        df_o = get_dtp_line(df=df, demo=demo, name='02.01.04 - Empréstimos, Financiamentos e Debêntures', conta_startswith='2.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['empréstimo', 'financiamento'])
        df_p = get_dtp_line(df=df, demo=demo, name='02.01.04.01 - Empréstimos e Financiamentos', conta_startswith='2.01.04', conta_levelmin=4, conta_levelmax=4, descricao_contains=['empréstimo', 'financiamento'])
        df_q = get_dtp_line(df=df, demo=demo, name='02.01.04.01 - Empréstimos e Financiamentos', conta_startswith='2.01.04', conta_levelmin=4, conta_levelmax=4, descricao_contains=['empréstimo', 'financiamento'])
        df_r = get_dtp_line(df=df, demo=demo, name='02.01.04.01.01 - Empréstimos e Financiamentos em Moeda Nacional', conta_startswith='2.01.04.01', conta_levelmin=5, conta_levelmax=5, descricao_contains=['naciona'])
        df_s = get_dtp_line(df=df, demo=demo, name='02.01.04.01.02 - Empréstimos e Financiamentos em Moeda Estrangeira', conta_startswith='2.01.04.01', conta_levelmin=5, conta_levelmax=5, descricao_contains=['estrangeir'])
        df_t = get_dtp_line(df=df, demo=demo, name='02.01.04.02 - Debêntures', conta_startswith='2.01.04', conta_levelmin=4, conta_levelmax=4, descricao_contains=['debentur'])
        df_u = get_dtp_line(df=df, demo=demo, name='02.01.04.03 - Arrendamentos', conta_startswith='2.01.04', conta_levelmin=4, conta_levelmax=4, descricao_contains=['arrendament'])
        df_v = get_dtp_line(df=df, demo=demo, name='02.01.04.09 - Outros empréstimos, financiamentos e debêntures', conta_startswith='2.01.04', conta_levelmin=4, conta_levelmax=4, descricao_contains_not=['empréstimo', 'financiamento', 'debentur', 'arrendament'])
        df_w = get_dtp_line(df=df, demo=demo, name='02.01.05 - Outras Obrigações', conta_startswith='2.01.05', conta_levelmin=3, conta_levelmax=3, descricao_contains=['outr', 'relaç'])
        df_x = get_dtp_line(df=df, demo=demo, name='02.01.05.01 - Passivos com Partes Relacionadas', conta_startswith='2.01.05', conta_levelmin=4, conta_levelmax=4, descricao_contains=['partes relacionadas'])
        df_y = get_dtp_line(df=df, demo=demo, name='02.01.05.09 - Outros', conta_startswith='2.01.05', conta_levelmin=4, conta_levelmax=4, descricao_contains_not=['partes relacionadas'])
        df_z = get_dtp_line(df=df, demo=demo, name='02.01.06 - Provisões', conta_startswith='2.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['provis'])
        df_aa = get_dtp_line(df=df, demo=demo, name='02.01.06.01 - Provisões Específicas', conta_startswith='2.01.06.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['provis'])
        df_ab = get_dtp_line(df=df, demo=demo, name='02.01.06.01.01 - Provisões Fiscais', conta_startswith='2.01.06.01.01', conta_levelmin=5, conta_levelmax=5, descricao_contains=['fisca'])
        df_ac = get_dtp_line(df=df, demo=demo, name='02.01.06.01.02 - Provisões Trabalhistas e Previdenciárias', conta_startswith='2.01.06.01.02', conta_levelmin=5, conta_levelmax=5, descricao_contains=['trabalhist'])
        df_ad = get_dtp_line(df=df, demo=demo, name='02.01.06.01.03 - Provisões para Benefícios a Empregados', conta_startswith='2.01.06.01.03', conta_levelmin=5, conta_levelmax=5, descricao_contains=['benefício'])
        df_ae = get_dtp_line(df=df, demo=demo, name='02.01.06.01.04 - Provisões Judiciais Cíveis', conta_startswith='2.01.06.01.04', conta_levelmin=5, conta_levelmax=5, descricao_contains=['cív'])
        df_af = get_dtp_line(df=df, demo=demo, name='02.01.06.01.05 - Outras Provisões Específicas', conta_startswith='2.01.06.01.05', conta_levelmin=5, conta_levelmax=5, descricao_contains=['outr'])
        df_ag = get_dtp_line(df=df, demo=demo, name='02.01.06.02 - Provisões Outras', conta_startswith='2.01.06.02', conta_levelmin=4, conta_levelmax=4, descricao_contains=['provis'])
        df_ah = get_dtp_line(df=df, demo=demo, name='02.01.06.02.01 - Provisões para Garantias', conta_startswith='2.01.06.02', conta_levelmin=5, conta_levelmax=5, descricao_contains=['garantia'])
        df_ai = get_dtp_line(df=df, demo=demo, name='02.01.06.02.02 - Provisões para Reestruturação', conta_startswith='2.01.06.02', conta_levelmin=5, conta_levelmax=5, descricao_contains=['reestrutura'])
        df_aj = get_dtp_line(df=df, demo=demo, name='02.01.06.02.03 - Provisões para Passivos Ambientais e de Desativação', conta_startswith='2.01.06.02', conta_levelmin=5, conta_levelmax=5, descricao_contains=['ambient'])
        df_ak = get_dtp_line(df=df, demo=demo, name='02.01.07 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados', conta_startswith='2.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['Passivos sobre ativos'])
        df_al = get_dtp_line(df=df, demo=demo, name='02.01.07.01 - Passivos sobre Ativos Não-Correntes a Venda', conta_startswith='2.01.07.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['venda'])
        df_am = get_dtp_line(df=df, demo=demo, name='02.01.07.02 - Passivos sobre Ativos de Operações Descontinuadas', conta_startswith='2.01.07.02', conta_levelmin=4, conta_levelmax=4, descricao_contains=['descontinuad'])
        df_an = get_dtp_line(df=df, demo=demo, name='02.01.09 - Outros Passivos', conta_startswith='2.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains_not=['obrigações sociais', 'fornecedor', 'obrigaç', 'fisca', 'empréstimo', 'financiamento', 'provis', 'Passivos sobre ativos'])
        df_ao = get_dtp_line(df=df, demo=demo, name='02.02 - Passivo Não Circulante de Longo Prazo', conta_startswith='2.', conta_levelmin=2, conta_levelmax=2, descricao_contains=['longo prazo', 'não circulante', 'ngeociação', 'fisca', 'provis', 'exercício', 'outr', 'venda'], descricao_contains_not=['patrimônio'])
        df_ap = get_dtp_line(df=df, demo=demo, name='02.02.01 - Empréstimos e Financiamentos de Longo Prazo', conta_startswith='2.02', conta_levelmin=3, conta_levelmax=3, descricao_contains=['empréstim', 'financiament'])
        df_aq = get_dtp_line(df=df, demo=demo, name='02.02.01.01 - Empréstimos e Financiamentos', conta_startswith='2.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['empréstim', 'financiament'])
        df_ar = get_dtp_line(df=df, demo=demo, name='02.02.01.01.01 - Empréstimos e Financiamentos em Moeda Nacional', conta_startswith='2.02.01.01', conta_levelmin=5, conta_levelmax=5, descricao_contains=['naciona'])
        df_as = get_dtp_line(df=df, demo=demo, name='02.02.01.01.02 - Empréstimos e Financiamentos em Moeda Estrangeira', conta_startswith='2.02.01.01', conta_levelmin=5, conta_levelmax=5, descricao_contains=['estrangeir'])
        df_at = get_dtp_line(df=df, demo=demo, name='02.02.01.02 - Debêntures', conta_startswith='2.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['debentur'])
        df_au = get_dtp_line(df=df, demo=demo, name='02.02.01.03 - Arrendamentos', conta_startswith='2.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['arrendament'])
        df_av = get_dtp_line(df=df, demo=demo, name='02.02.02.09 - Outros empréstimos, financiamentos e debêntures', conta_startswith='2.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains_not=['empréstimo', 'financiamento', 'debentur', 'arrendament'])
        df_aw = get_dtp_line(df=df, demo=demo, name='02.02.02 - Outras Obrigações', conta_startswith='2.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['obriga'])
        df_ax = get_dtp_line(df=df, demo=demo, name='02.02.02.01 - Com Partes Relacionadas', conta_startswith='2.02.02.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['relacionad'])
        df_ay = get_dtp_line(df=df, demo=demo, name='02.02.02.02 - Outras Obrigações', conta_startswith='2.02.02.02', conta_levelmin=4, conta_levelmax=4, descricao_contains=['outr'])
        df_az = get_dtp_line(df=df, demo=demo, name='02.02.03 - Tributos Diferidos', conta_startswith='2.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['tributo'])
        df_ba = get_dtp_line(df=df, demo=demo, name='02.02.03.01 - Imposto de Renda e Contribuição Social', conta_startswith='2.02.03', conta_levelmin=4, conta_levelmax=4, descricao_contains=['imposto de renda', 'contribuição social'])
        df_bb = get_dtp_line(df=df, demo=demo, name='02.02.03.02 - Outros tributos diferidos', conta_startswith='2.02.03', conta_levelmin=4, conta_levelmax=4, descricao_contains_not=['imposto de renda', 'contribuição social'])
        df_bc = get_dtp_line(df=df, demo=demo, name='02.02.04 - Provisões', conta_startswith='2.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['provis'])
        df_bd = get_dtp_line(df=df, demo=demo, name='02.02.04.01 - Provisões Específicas', conta_startswith='2.02.04.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['provis'])
        df_be = get_dtp_line(df=df, demo=demo, name='02.02.04.01.01 - Provisões Fiscais', conta_startswith='2.02.04.01.01', conta_levelmin=5, conta_levelmax=5, descricao_contains=['fisca'])
        df_bf = get_dtp_line(df=df, demo=demo, name='02.02.04.01.02 - Provisões Trabalhistas e Previdenciárias', conta_startswith='2.02.04.01.02', conta_levelmin=5, conta_levelmax=5, descricao_contains=['trabalhist'])
        df_bg = get_dtp_line(df=df, demo=demo, name='02.02.04.01.03 - Provisões para Benefícios a Empregados', conta_startswith='2.02.04.01.03', conta_levelmin=5, conta_levelmax=5, descricao_contains=['benefício'])
        df_bh = get_dtp_line(df=df, demo=demo, name='02.02.04.01.04 - Provisões Judiciais Cíveis', conta_startswith='2.02.04.01.04', conta_levelmin=5, conta_levelmax=5, descricao_contains=['cív'])
        df_bi = get_dtp_line(df=df, demo=demo, name='02.02.04.02 - Outras Provisões', conta_startswith='2.02.04.02', conta_levelmin=4, conta_levelmax=4, descricao_contains=['provis'])
        df_bj = get_dtp_line(df=df, demo=demo, name='02.02.04.02.01 - Provisões para Garantias', conta_startswith='2.02.04.02', conta_levelmin=5, conta_levelmax=5, descricao_contains=['garantia'])
        df_bk = get_dtp_line(df=df, demo=demo, name='02.02.04.02.02 - Provisões para Reestruturação', conta_startswith='2.02.04.02', conta_levelmin=5, conta_levelmax=5, descricao_contains=['reestrutura'])
        df_bl = get_dtp_line(df=df, demo=demo, name='02.02.04.02.03 - Provisões para Passivos Ambientais e de Desativação', conta_startswith='2.02.04.02', conta_levelmin=5, conta_levelmax=5, descricao_contains=['ambient'])
        df_bm = get_dtp_line(df=df, demo=demo, name='02.02.05 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados', conta_startswith='2.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['Passivos sobre ativos'])
        df_bn = get_dtp_line(df=df, demo=demo, name='02.02.05.01 - Passivos sobre Ativos Não-Correntes a Venda', conta_startswith='2.02.05.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['venda'])
        df_bo = get_dtp_line(df=df, demo=demo, name='02.02.05.02 - Passivos sobre Ativos de Operações Descontinuadas', conta_startswith='2.02.05.02', conta_levelmin=4, conta_levelmax=4, descricao_contains=['descontinuad'])
        df_bp = get_dtp_line(df=df, demo=demo, name='02.02.06 - Lucros e Receitas a Apropriar', conta_startswith='2.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['lucros e receitas'])
        df_bq = get_dtp_line(df=df, demo=demo, name='02.02.06.01 - Lucros a Apropriar', conta_startswith='2.02.06.01', conta_levelmin=4, conta_levelmax=4, descricao_contains=['lucr'])
        df_br = get_dtp_line(df=df, demo=demo, name='02.02.06.02 - Receitas a Apropriar', conta_startswith='2.02.06.02', conta_levelmin=4, conta_levelmax=4, descricao_contains=['receit'])
        df_bs = get_dtp_line(df=df, demo=demo, name='02.02.06.03 - Subvenções de Investimento a Apropriar', conta_startswith='2.02.06.03', conta_levelmin=4, conta_levelmax=4, descricao_contains=['subvenç'])
        df_bt = get_dtp_line(df=df, demo=demo, name='02.02.09 - Outros Passivos', conta_startswith=['2.02.07', '2.02.08', '2.02.09'], conta_levelmin=3, conta_levelmax=3)
        df_bu = get_dtp_line(df=df, demo=demo, name='02.03 - Patrimônio Líquido', conta_startswith='2.', conta_levelmin=2, conta_levelmax=2, descricao_contains='patrimônio')
        df_bv = get_dtp_line(df=df, demo=demo, name='02.03.01 - Capital Social', conta_startswith='2.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['2.01', '2.02'], descricao_contains=['capital social'])
        df_bw = get_dtp_line(df=df, demo=demo, name='02.03.02 - Reservas de Capital', conta_startswith='2.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['2.01', '2.02'], descricao_contains=['reservas de capital'])
        df_bx = get_dtp_line(df=df, demo=demo, name='02.03.03 - Reservas de Reavaliação', conta_startswith='2.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['2.01', '2.02'], descricao_contains=['reservas de reavaliaç'])
        df_by = get_dtp_line(df=df, demo=demo, name='02.03.04 - Reservas de Lucros', conta_startswith='2.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['2.01', '2.02'], descricao_contains=['reservas de lucro'])
        df_bz = get_dtp_line(df=df, demo=demo, name='02.03.05 - Lucros ou Prejuízos Acumulados', conta_startswith='2.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['2.01', '2.02'], descricao_contains=['lucro', 'prejuízo', 'acumulad'], descricao_contains_not='reserva')
        df_ca = get_dtp_line(df=df, demo=demo, name='02.03.06 - Ajustes de Avaliação Patrimonial', conta_startswith='2.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['2.01', '2.02'], descricao_contains=['avaliação patrimonial'])
        df_cb = get_dtp_line(df=df, demo=demo, name='02.03.07 - Ajustes Acumulados de Conversão', conta_startswith='2.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['2.01', '2.02'], descricao_contains=['ajustes acumulados'])
        df_cc = get_dtp_line(df=df, demo=demo, name='02.03.08 - Outros Resultados Abrangentes', conta_startswith='2.', conta_levelmin=3, conta_levelmax=3, conta_startswith_not=['2.01', '2.02'], descricao_contains=['resultados abrangentes'])
        df_cd = get_dtp_line(df=df, demo=demo, name='02.04 - Outros Passivos ou Provissões', conta_startswith=['2.04', '2.05', '2.06', '2.07', '2.08', '2.09'], conta_levelmin=2, conta_levelmax=2, descricao_contains_not='patrimonio')
        d2 = pd.concat([df_a, df_b, df_c, df_d, df_e, df_f, df_g, df_h, df_i, df_j, df_k, df_l, df_m, df_n, df_o, df_p, df_q, df_r, df_s, df_t, df_u, df_v, df_w, df_x, df_y, df_z, df_aa, df_ab, df_ac, df_ad, df_ae, df_af, df_ag, df_ah, df_ai, df_aj, df_ak, df_al, df_am, df_an, df_ao, df_ap, df_aq, df_ar, df_as, df_at, df_au, df_av, df_aw, df_ax, df_ay, df_az, df_ba, df_bb, df_bc, df_bd, df_be, df_bf, df_bg, df_bh, df_bi, df_bj, df_bk, df_bl, df_bm, df_bn, df_bo, df_bp, df_bq, df_br, df_bs, df_bt, df_bu, df_bv, df_bw, df_bx, df_by, df_bz, df_ca, df_cb, df_cc, df_cd], ignore_index=True)

        demo3 = demo = 'Demonstração do Resultado'
        df_a = get_dtp_line(df=df, demo=demo, name='03.01 - Receita Bruta', conta_exact='3.01')
        df_b = get_dtp_line(df=df, demo=demo, name='03.02 - Custo de Produção', conta_exact='3.02')
        df_c = get_dtp_line(df=df, demo=demo, name='03.03 - Resultado Bruto (Receita Líquida)', conta_exact='3.03')
        df_d = get_dtp_line(df=df, demo=demo, name='03.04 - Despesas Operacionais', conta_exact='3.04')
        df_e = get_dtp_line(df=df, demo=demo, name='03.04.01 - Despesas com Vendas', conta_exact='3.04.01')
        df_f = get_dtp_line(df=df, demo=demo, name='03.04.02 - Despesas Gerais e Administrativas', conta_exact='3.04.02')
        df_g = get_dtp_line(df=df, demo=demo, name='03.04.09 - Outras despesas, receitas ou equivalências', conta_levelmin=3, conta_levelmax=3, conta_startswith=['3.04.'], conta_startswith_not=['3.04.01', '3.04.02'])
        df_h = get_dtp_line(df=df, demo=demo, name='03.05 - LAJIR EBIT Resultado Antes do Resultado Financeiro e dos Tributos', conta_exact='3.05')
        df_i = get_dtp_line(df=df, demo=demo, name='03.06 - Resultado Financeiro (Não Operacional)', conta_exact='3.06')
        df_j = get_dtp_line(df=df, demo=demo, name='03.07 - Resultado Antes dos Tributos sobre o Lucro', conta_exact='3.07')
        df_k = get_dtp_line(df=df, demo=demo, name='03.08 - Impostos IRPJ e CSLL', conta_exact='3.08')
        df_l = get_dtp_line(df=df, demo=demo, name='03.09 - Resultado Líquido das Operações Continuadas', conta_exact='3.09')
        df_m = get_dtp_line(df=df, demo=demo, name='03.10 - Resultado Líquido das Operações Descontinuadas', conta_exact='3.10')
        df_n = get_dtp_line(df=df, demo=demo, name='03.11 - Lucro Líquido', conta_exact='3.11')
        d3 = pd.concat([df_a, df_b, df_c, df_d, df_e, df_f, df_g, df_h, df_i, df_j, df_k, df_l, df_m, df_n], ignore_index=True)

        demo6 = demo = 'Demonstração de Fluxo de Caixa'
        # imobilizado e intangível
        df_a = get_dtp_line(df=df, demo=demo, name='06.01 - Caixa das Operações', conta_exact='6.01')
        df_b = get_dtp_line(df=df, demo=demo, name='06.01.01 - Caixa das Operações', conta_startswith='6.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['operac'], descricao_contains_not=['ativ', 'print(e)iv', 'despes', 'ingress', 'pagament', 'receb', 'arrendament', 'aquisic'])
        df_c = get_dtp_line(df=df, demo=demo, name='06.01.02 - Variações de Ativos e Passivos', conta_startswith='6.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['ativ'], descricao_contains_not=['operac', 'imob', 'intangív', 'adiantament', 'provis', 'permanent', 'despes', 'pagament', 'recebiment', 'caixa', 'derivativ', 'judicia', ])
        df_d = get_dtp_line(df=df, demo=demo, name='06.01.09 - Outros Caixas Operacionais', conta_startswith='6.01.', conta_levelmin=3, conta_levelmax=3, descricao_contains_not=['ativ', 'operac'])
        df_e = get_dtp_line(df=df, demo=demo, name='06.02 - Caixa de Investimentos CAPEX', conta_exact='6.02')
        # imobilizado e intangível
        kw60201 = ['investiment', 'mobiliár', 'derivativ', 'propriedad']
        kw60202 = ['imob', 'intangív']
        kw60203 = ['financeir']
        kw60204 = ['coligad', 'controlad', 'ligad']
        kw60205 = ['juro', 'jcp', 'jscp', 'dividend']
        kw602 = []
        [kw602.append(i) for i in kw60201 + kw60202 + kw60203 + kw60204 + kw60205 if i not in kw602]
        df_f = get_dtp_line(df=df, demo=demo, name='06.02.01 - Investimentos', conta_startswith='6.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60201, descricao_contains_not=list_subtract(kw602, kw60201))
        df_g = get_dtp_line(df=df, demo=demo, name='06.02.02 - Imobilizado e Intangível', conta_startswith='6.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60202, descricao_contains_not=list_subtract(kw602, kw60202))
        df_h = get_dtp_line(df=df, demo=demo, name='06.02.03 - Aplicações Financeiras', conta_startswith='6.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60203, descricao_contains_not=list_subtract(kw602, kw60203))
        df_i = get_dtp_line(df=df, demo=demo, name='06.02.04 - Coligadas e Controladas', conta_startswith='6.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60204, descricao_contains_not=list_subtract(kw602, kw60204))
        df_j = get_dtp_line(df=df, demo=demo, name='06.02.05 - Juros sobre Capital Próprio e Dividendos', conta_startswith='6.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60205, descricao_contains_not=list_subtract(kw602, kw60205))
        df_k = get_dtp_line(df=df, demo=demo, name='06.02.09 - Outros Caixas de Investimento', conta_startswith='6.02.', conta_levelmin=3, conta_levelmax=3, descricao_contains_not=kw602)
        df_l = get_dtp_line(df=df, demo=demo, name='06.03 - Caixa de Financiamento', conta_exact='6.03')
        # dividend juros jcp, jscp bonifica, 
        kw60301 = ['capital']
        kw60302 = ['ação', 'ações', 'acionist']
        kw60303 = ['debentur', 'empréstim', 'financiam']
        kw60304 = ['credor']
        kw60305 = ['amortizaç', 'captaç']
        kw60306 = ['dividend', 'juros', 'jcp', 'bonifica']
        kw603 = []
        [kw603.append(i) for i in kw60301 + kw60302 + kw60303 + kw60304 + kw60305 + kw60306 if i not in kw603]
        df_m = get_dtp_line(df=df, demo=demo, name='06.03.01 - Capital', conta_startswith='6.03.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60301, descricao_contains_not=list_subtract(kw603, kw60301))
        df_n = get_dtp_line(df=df, demo=demo, name='06.03.02 - Ações e Acionistas', conta_startswith='6.03.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60302, descricao_contains_not=list_subtract(kw603, kw60302))
        df_o = get_dtp_line(df=df, demo=demo, name='06.03.03 - Debêntures, empréstimos e financiamentos', conta_startswith='6.03.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60303, descricao_contains_not=list_subtract(kw603, kw60303))
        df_p = get_dtp_line(df=df, demo=demo, name='06.03.04 - Credores', conta_startswith='6.03.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60304, descricao_contains_not=list_subtract(kw603, kw60304))
        df_q = get_dtp_line(df=df, demo=demo, name='06.03.05 - Captações e Amortizações', conta_startswith='6.03.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60305, descricao_contains_not=list_subtract(kw603, kw60305))
        df_r = get_dtp_line(df=df, demo=demo, name='06.03.06 - Juros JCP e Dividendos', conta_startswith='6.03.', conta_levelmin=3, conta_levelmax=3, descricao_contains=kw60306, descricao_contains_not=list_subtract(kw603, kw60306))
        df_s = get_dtp_line(df=df, demo=demo, name='06.03.09 - Outros Caixas de Financiamento', conta_startswith='6.03.', conta_levelmin=3, conta_levelmax=3, descricao_contains_not=kw603)
        df_t = get_dtp_line(df=df, demo=demo, name='06.04 - Caixa da Variação Cambial', conta_exact='6.04')
        df_u = get_dtp_line(df=df, demo=demo, name='06.05 - Variação do Caixa', conta_exact='6.05')
        df_v = get_dtp_line(df=df, demo=demo, name='06.05.01 - Saldo Inicial do Caixa ', conta_exact='6.05.01')
        df_w = get_dtp_line(df=df, demo=demo, name='06.05.02 - Saldo Final do Caixa', conta_exact='6.05.02')
        d6 = pd.concat([df_a, df_b, df_c, df_d, df_e, df_f, df_g, df_h, df_i, df_j, df_k, df_l, df_m, df_n, df_o, df_p, df_q, df_r, df_s, df_t, df_u, df_v, df_w], ignore_index=True)

        demo7 = demo = 'Demonstração de Valor Adiconado'
        df_a = get_dtp_line(df=df, demo=demo, name='07.01 - Receitas', conta_startswith='7.', descricao_contains=['receita'], descricao_contains_not='líquid')
        df_b = get_dtp_line(df=df, demo=demo, name='07.01.01 - Vendas', conta_exact='7.01.01')
        df_c = get_dtp_line(df=df, demo=demo, name='07.01.02 - Outras Receitas', conta_exact='7.01.02')
        df_d = get_dtp_line(df=df, demo=demo, name='07.01.03 - Ativos Próprios', conta_exact='7.01.03')
        df_e = get_dtp_line(df=df, demo=demo, name='07.01.04 - Reversão de Créditos Podres', conta_exact='7.01.04')
        df_f = get_dtp_line(df=df, demo=demo, name='07.02 - Custos dos Insumos', conta_startswith='7.', descricao_contains=['insumos adquiridos', 'intermediação financeira', 'provis'])
        df_g = get_dtp_line(df=df, demo=demo, name='07.02.01 - Custo de Mercadorias', conta_exact='7.02.01')
        df_h = get_dtp_line(df=df, demo=demo, name='07.02.02 - Custo de Materiais, Energia e Terceiros', conta_exact='7.02.02')
        df_i = get_dtp_line(df=df, demo=demo, name='07.02.03 - Valores Ativos', conta_exact='7.02.03')
        df_j = get_dtp_line(df=df, demo=demo, name='07.02.04 - Outros', conta_exact='7.02.04')
        df_k = get_dtp_line(df=df, demo=demo, name='07.03 - Valor Adicionado Bruto', conta_startswith='7.', descricao_contains=['valor adicionado bruto'])
        df_l = get_dtp_line(df=df, demo=demo, name='07.04 - Retenções', conta_startswith='7.', descricao_contains=['retenç', 'Benefíci', 'sinistr'])
        df_m = get_dtp_line(df=df, demo=demo, name='07.04.01 - Depreciação e Amortização', conta_startswith='7.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['deprecia', 'amortiza', 'exaust'])
        df_n = get_dtp_line(df=df, demo=demo, name='07.04.02 - Outras retenções', conta_exact='7.04.02')
        df_o = get_dtp_line(df=df, demo=demo, name='07.05 - Valor Adicionado Líquido', conta_startswith='7.', descricao_contains=['valor adicionado líquid', 'receita operacional'], conta_startswith_not='7.01', descricao_contains_not='transferência')
        df_p = get_dtp_line(df=df, demo=demo, name='07.06 - Valor Adicionado em Transferência', conta_startswith='7.', descricao_contains=['transferência'])
        df_q = get_dtp_line(df=df, demo=demo, name='07.06.01 - Resultado de Equivalência Patrimonial', conta_startswith='7.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['equivalencia patrimonial'])
        df_r = get_dtp_line(df=df, demo=demo, name='07.06.02 - Receitas Financeiras', conta_exact='7.06.02')
        df_s = get_dtp_line(df=df, demo=demo, name='07.06.03 - Outros', conta_exact='7.06.03')
        df_t = get_dtp_line(df=df, demo=demo, name='07.07 - Valor Adicionado Total a Distribuir', conta_startswith='7.', descricao_contains=['total a distribuir'])
        df_u = get_dtp_line(df=df, demo=demo, name='07.08 - Distribuição do Valor Adicionado', conta_startswith='7.', descricao_contains=['Distribuição do Valor Adicionado'])
        df_v = get_dtp_line(df=df, demo=demo, name='07.08.01 - Pessoal', conta_startswith='7.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['pessoal'])
        df_w = get_dtp_line(df=df, demo=demo, name='07.08.01.01 - Remuneração Direta', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['remuneração direta'])
        df_x = get_dtp_line(df=df, demo=demo, name='07.08.01.02 - Benefícios', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['benefícios'])
        df_y = get_dtp_line(df=df, demo=demo, name='07.08.01.03 - FGTS', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['F.G.T.S.', 'fgts'])
        df_z = get_dtp_line(df=df, demo=demo, name='07.08.01.04 - Outros', conta_exact='7.08.01.04')
        df_aa = get_dtp_line(df=df, demo=demo, name='07.08.02 - Impostos, Taxas e Contribuições', conta_startswith='7.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['imposto', 'taxa', 'contribuiç'])
        df_ab = get_dtp_line(df=df, demo=demo, name='07.08.02.01 - Federais', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['federa'])
        df_ac = get_dtp_line(df=df, demo=demo, name='07.08.02.02 - Estaduais', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['estadua'])
        df_ad = get_dtp_line(df=df, demo=demo, name='07.08.02.03 - Municipais', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['municipa'])
        df_ae = get_dtp_line(df=df, demo=demo, name='07.08.03 - Remuneração de Capital de Terceiros', conta_startswith='7.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['remuneraç', 'capital', 'terceir'], descricao_contains_not='própri')
        df_af = get_dtp_line(df=df, demo=demo, name='07.08.03.01 - Juros Pagos', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['juro'], descricao_contains_not='propri')
        df_ag = get_dtp_line(df=df, demo=demo, name='07.08.03.02 - Aluguéis', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['alugue'])
        df_ah = get_dtp_line(df=df, demo=demo, name='07.08.04 - Remuneração de Capital Próprio', conta_startswith='7.', conta_levelmin=3, conta_levelmax=3, descricao_contains=['remuneraç', 'capital', 'própri'], descricao_contains_not='terceir')
        df_ai = get_dtp_line(df=df, demo=demo, name='07.08.04.01 - Juros sobre o Capital Próprio', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['juros sobre', 'jcp'])
        df_aj = get_dtp_line(df=df, demo=demo, name='07.08.04.02 - Dividendos', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['dividend'])
        df_ak = get_dtp_line(df=df, demo=demo, name='07.08.04.03 - Lucros Retidos', conta_startswith='7.', conta_levelmin=4, conta_levelmax=4, descricao_contains=['lucros retidos'])
        df_al = get_dtp_line(df=df, demo=demo, name='07.08.05 - Outros', conta_exact='7.08.05')
        d7 = pd.concat([df_a, df_b, df_c, df_d, df_e, df_f, df_g, df_h, df_i, df_j, df_k, df_l, df_m, df_n, df_o, df_p, df_q, df_r, df_s, df_t, df_u, df_v, df_w, df_x, df_y, df_z, df_aa, df_ab, df_ac, df_ad, df_ae, df_af, df_ag, df_ah, df_ai, df_aj, df_ak, df_al], ignore_index=True)

        try:
            result = pd.concat([d0, d1, d2, d3, d6, d7], ignore_index=True).drop_duplicates()
        except Exception as e:
            print('ac', e)
    except Exception as e:
        print('ad', e)

    return result

def inteligence_dre(df):
    try:
        d0_demo = 'Composição do Capital'
        d0_lines = [
            ('00.01 - Ações Ordinárias', [('conta_exact', '0.01')]),
            ('00.02 - Ações Preferenciais', [('conta_exact', '0.02')]),
            ('00.01.01 - Ações Ordinárias em Tesouraria', [('conta_exact', '0.01.01')]),
            ('00.01.02 - Ações Ordinárias Outras', [('conta_exact', '0.01.02')]),
            ('00.02.01 - Ações Prerenciais em Tesouraria', [('conta_exact', '0.02.01')]),
            ('00.02.02 - Ações Prerenciais Outras', [('conta_exact', '0.02.02')]),
        ]
        d0 = get_dtp_lines(df, d0_demo, d0_lines)
        
        d1_demo = 'Balanço Patrimonial Ativo'
        d1_lines = [
            ('01 - Ativo Total', [('conta_exact', '1')]),
            ('01.01 - Ativo Circulante de Curto Prazo', [('conta_exact', '1.01')]),
            ('01.01.01 - Caixa e Disponibilidades de Caixa', [('conta_exact', '1.01.01')]),
            ('01.01.02 - Aplicações Financeiras', [('conta_startswith', '1.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['aplica', 'depósito', 'reserv', 'saldo', 'centra', 'interfinanceir', 'crédit']), ('conta_contains_not', ['1.01.01', '1.01.02', '1.01.06'])]),
            ('01.01.03 - Contas a Receber', [('conta_startswith', '1.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['conta'])]),
            ('01.01.04 - Estoques', [('conta_startswith', '1.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['estoque'])]),
            ('01.01.05 - Ativos Biológicos', [('conta_startswith', '1.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['biológic'])]),
            ('01.01.06 - Tributos', [('conta_startswith', '1.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['tribut'])]),
            ('01.01.07 - Despesas', [('conta_startswith', '1.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['despes'])]),
            ('01.01.09 - Outros Ativos Circulantes', [('conta_startswith', '1.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', 'outr'), ('descricao_contains_not', ['aplica', 'depósito', 'reserv', 'saldo', 'centra', 'interfinanceir', 'crédit', 'conta', 'estoque', 'biológic', 'tribut', 'despes']), ('conta_contains_not', ['1.01.01', '1.01.02', '1.01.03', '1.01.04', '1.01.05', '1.01.06', '1.01.07'])]),
            ('01.02 - Ativo Não Circulante de Longo Prazo', [('conta_exact', '1.02')]),
            ('01.02.01 - Ativos Financeiros', [('conta_startswith', '1.02.'), ('descricao_contains_not', ['investiment', 'imobilizad', 'intangív'])]),
            ('01.02.01.01 - Ativos Financeiros a Valor Justo', [('conta_startswith', '1.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'valor justo'), ('descricao_contains_not', 'custo amortizado')]),
            ('01.02.01.02 - Ativos Financeiros ao Custo Amortizado', [('conta_startswith', '1.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'custo amortizado'), ('descricao_contains_not', 'valor justo')]),
            ('01.02.01.03 - Contas a Receber', [('conta_startswith', '1.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'conta')]),
            ('01.02.01.04 - Estoques', [('conta_startswith', '1.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'estoque')]),
            ('01.02.01.05 - Ativos Biológicos', [('conta_startswith', '1.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'biológic')]),
            ('01.02.01.06 - Tributos', [('conta_startswith', '1.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'tribut')]),
            ('01.02.01.07 - Despesas', [('conta_startswith', '1.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'despes')]),
            ('01.02.01.09 - Outros Ativos Não Circulantes', [('conta_startswith', '1.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains_not', ['valor justo', 'custo amortizado', 'conta', 'estoque', 'biológic', 'tribut', 'despes'])]),
            ('01.02.02 - Investimentos Não Capex', [('conta_startswith', '1.02.'), ('descricao_contains', ['investiment'])]),
            ('01.02.02.01 - Propriedades - Investimentos Não Capex', [('conta_startswith', '1.02.'), ('conta_levelmin', 3), ('descricao_contains', ['propriedad'])]),
            ('01.02.02.02 - Arrendamentos - Investimentos Não Capex', [('conta_startswith', '1.02.'), ('conta_levelmin', 3), ('descricao_contains', ['arrendam']), ('descricao_contains_not', ['sotware', 'imobilizad', 'intangív', 'direit'])]),
            ('01.02.03 - Imobilizados', [('conta_startswith', '1.02.'), ('descricao_contains', ['imobilizad'])]),
            ('01.02.03.01 - Imobilizados em Operação', [('conta_startswith', '1.02.03.'), ('descricao_contains', ['operaç'])]),
            ('01.02.03.02 - Imobilizados em Arrendamento', [('conta_startswith', '1.02.03.'), ('descricao_contains', ['arrend'])]),
            ('01.02.03.03 - Imobilizados em Andamento', [('conta_startswith', '1.02.03.'), ('descricao_contains', ['andament'])]),
            ('01.02.04 - Intangível', [('conta_startswith', '1.02.'), ('descricao_contains', ['intangív'])]),
            ('01.03 - Empréstimos', [('conta_startswith', '1.'), ('conta_levelmax', 2), ('descricao_contains', 'empréstimo')]),
            ('01.04 - Tributos Diferidos', [('conta_startswith', '1.'), ('conta_levelmax', 2), ('descricao_contains', 'tributo')]),
            ('01.05 - Investimentos', [('conta_startswith', '1.'), ('conta_levelmax', 2), ('descricao_contains', 'investimento')]),
            ('01.05.01 - Participações em Coligadas', [('conta_startswith', '1.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', 'coligad')]),
            ('01.05.02 - Participações em Controladas', [('conta_startswith', '1.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', 'controlad')]),
            ('01.06 - Imobilizados', [('conta_startswith', '1.'), ('conta_levelmax', 2), ('descricao_contains', 'imobilizado')]),
            ('01.06.01 - Propriedades - Investimentos Não Capex', [('conta_startswith', '1.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['1.02.']), ('descricao_contains', ['propriedad', 'imóve'])]),
            ('01.06.02 - Arrendamento - Investimentos Não Capex', [('conta_startswith', '1.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['1.02.']), ('descricao_contains', 'arrendam')]),
            ('01.06.03 - Tangíveis - Investimentos Não Capex', [('conta_startswith', '1.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['1.02.']), ('descricao_contains', ['arrendam', 'equipamento'])]),
            ('01.07 - Intangíveis', [('conta_startswith', '1.'), ('conta_levelmax', 2), ('descricao_contains', 'intangíve')]),
            ('01.07.01 - Intangíveis', [('conta_startswith', '1.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['1.02.']), ('descricao_contains', 'intangíve')]),
            ('01.07.02 - Goodwill', [('conta_startswith', '1.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['1.02.']), ('descricao_contains', 'goodwill')]),
            ('01.08 - Permanente', [('conta_startswith', '1.0'), ('conta_levelmax', 2), ('descricao_contains', 'permanente')]),
            ('01.09.09 - Outros Ativos', [('conta_startswith', '1.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['1.01.', '1.02']), ('descricao_contains_not', ['depreciaç', 'amortizaç', 'empréstimo', 'tributo', 'investimento', 'imobilizado', 'intangíve', 'permanente', 'goodwill', 'arrendam', 'equipamento', 'propriedad', 'imóve', 'coligad', 'controlad'])]),
        ]
        d1 = get_dtp_lines(df, d1_demo, d1_lines)

        d2_demo = 'Balanço Patrimonial Passivo'
        d2_lines = [
              ('02 - Passivo Total', [('conta_exact', '2')]),
              ('02.01 - Passivo Circulante de Curto Prazo', [('conta_startswith', '2.'), ('conta_levelmin', 2), ('conta_levelmax', 2), ('descricao_contains', ['circulante', 'o resultado', 'amortizado', 'negociaç']), ('descricao_contains_not', ['não', 'patrimônio', 'fisca'])]),
              ('02.01.01 - Obrigações Sociais e Trabalhistas', [('conta_startswith', '2.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['obrigações sociais'])]),
              ('02.01.01.01 - Obrigações Sociais', [('conta_startswith', '2.01.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['socia'])]),
              ('02.01.01.02 - Obrigações Trabalhistas', [('conta_startswith', '2.01.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['trabalhista'])]),
              ('02.01.01.09 - Outras Obrigações', [('conta_startswith', '2.01.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains_not', ['socia', 'trabalhista'])]),
              ('02.01.02 - Fornecedores', [('conta_startswith', '2.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['fornecedor'])]),
              ('02.01.02.01 - Fornecedores Nacionais', [('conta_startswith', ['2.01.01.', '2.01.02']), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['fornecedores nacionais'])]),
              ('02.01.02.02 - Fornecedores Estrangeiros', [('conta_startswith', ['2.01.01.', '2.01.02']), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['fornecedores estrangeiros'])]),
              ('02.01.03 - Obrigações Fiscais', [('conta_startswith', '2.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['obrigaç', 'fisca']), ('descricao_contains_not', 'socia')]),
              ('02.01.03.01 - Obrigações Fiscais Federais', [('conta_startswith', '2.01.03'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['federa'])]),
              ('02.01.03.02 - Obrigações Fiscais Estaduais', [('conta_startswith', '2.01.03'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['estadua'])]),
              ('02.01.03.03 - Obrigações Fiscais Municipais', [('conta_startswith', '2.01.03'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'municipa')]),
              ('02.01.03.09 - Outras Obrigações Fiscais', [('conta_startswith', '2.01.03'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains_not', ['federa', 'estadua', 'municipa'])]),
              ('02.01.04 - Empréstimos, Financiamentos e Debêntures', [('conta_startswith', '2.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['empréstimo', 'financiamento'])]),
              ('02.01.04.01 - Empréstimos e Financiamentos', [('conta_startswith', '2.01.04'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['empréstimo', 'financiamento'])]),
              ('02.01.04.01 - Empréstimos e Financiamentos', [('conta_startswith', '2.01.04'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['empréstimo', 'financiamento'])]),
              ('02.01.04.01.01 - Empréstimos e Financiamentos em Moeda Nacional', [('conta_startswith', '2.01.04.01'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', 'naciona')]),
              ('02.01.04.01.02 - Empréstimos e Financiamentos em Moeda Estrangeira', [('conta_startswith', '2.01.04.01'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', 'estrangeir')]),
              ('02.01.04.02 - Debêntures', [('conta_startswith', '2.01.04'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'debentur')]),
              ('02.01.04.03 - Arrendamentos', [('conta_startswith', '2.01.04'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'arrendament')]),
              ('02.01.04.09 - Outros empréstimos, financiamentos e debêntures', [('conta_startswith', '2.01.04'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains_not', ['empréstimo', 'financiamento', 'debentur', 'arrendament'])]),
              ('02.01.05 - Outras Obrigações', [('conta_startswith', '2.01.05'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['outr', 'relaç'])]),
              ('02.01.05.01 - Passivos com Partes Relacionadas', [('conta_startswith', '2.01.05'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['partes relacionadas'])]),
              ('02.01.05.09 - Outros', [('conta_startswith', '2.01.05'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains_not', ['partes relacionadas'])]),
              ('02.01.06 - Provisões', [('conta_startswith', '2.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['provis'])]),
              ('02.01.06.01 - Provisões Específicas', [('conta_startswith', '2.01.06.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['provis'])]),
              ('02.01.06.01.01 - Provisões Fiscais', [('conta_startswith', '2.01.06.01.01'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['fisca'])]),
              ('02.01.06.01.02 - Provisões Trabalhistas e Previdenciárias', [('conta_startswith', '2.01.06.01.02'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['trabalhist'])]),
              ('02.01.06.01.03 - Provisões para Benefícios a Empregados', [('conta_startswith', '2.01.06.01.03'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['benefício'])]),
              ('02.01.06.01.04 - Provisões Judiciais Cíveis', [('conta_startswith', '2.01.06.01.04'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['cív'])]),
              ('02.01.06.01.05 - Outras Provisões Específicas', [('conta_startswith', '2.01.06.01.05'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['outr'])]),
              ('02.01.06.02 - Provisões Outras', [('conta_startswith', '2.01.06.02'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['provis'])]),
              ('02.01.06.02.01 - Provisões para Garantias', [('conta_startswith', '2.01.06.02'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['garantia'])]),
              ('02.01.06.02.02 - Provisões para Reestruturação', [('conta_startswith', '2.01.06.02'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['reestrutura'])]),
              ('02.01.06.02.03 - Provisões para Passivos Ambientais e de Desativação', [('conta_startswith', '2.01.06.02'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['ambient'])]),
              ('02.01.07 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados', [('conta_startswith', '2.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['Passivos sobre ativos'])]),
              ('02.01.07.01 - Passivos sobre Ativos Não-Correntes a Venda', [('conta_startswith', '2.01.07.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['venda'])]),
              ('02.01.07.02 - Passivos sobre Ativos de Operações Descontinuadas', [('conta_startswith', '2.01.07.02'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['descontinuad'])]),
              ('02.01.09 - Outros Passivos', [('conta_startswith', '2.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains_not', ['obrigações sociais', 'fornecedor', 'obrigaç', 'fisca', 'empréstimo', 'financiamento', 'provis', 'Passivos sobre ativos'])]),
              ('02.02 - Passivo Não Circulante de Longo Prazo', [('conta_startswith', '2.'), ('conta_levelmin', 2), ('conta_levelmax', 2), ('descricao_contains', ['longo prazo', 'não circulante', 'ngeociação', 'fisca', 'provis', 'exercício', 'outr', 'venda']), ('descricao_contains_not', ['patrimônio'])]),
              ('02.02.01 - Empréstimos e Financiamentos de Longo Prazo', [('conta_startswith', '2.02'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['empréstim', 'financiament'])]),
              ('02.02.01.01 - Empréstimos e Financiamentos', [('conta_startswith', '2.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['empréstim', 'financiament'])]),
              ('02.02.01.01.01 - Empréstimos e Financiamentos em Moeda Nacional', [('conta_startswith', '2.02.01.01'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['naciona'])]),
              ('02.02.01.01.02 - Empréstimos e Financiamentos em Moeda Estrangeira', [('conta_startswith', '2.02.01.01'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['estrangeir'])]),
              ('02.02.01.02 - Debêntures', [('conta_startswith', '2.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['debentur'])]),
              ('02.02.01.03 - Arrendamentos', [('conta_startswith', '2.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['arrendament'])]),
              ('02.02.02.09 - Outros empréstimos, financiamentos e debêntures', [('conta_startswith', '2.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains_not', ['empréstimo', 'financiamento', 'debentur', 'arrendament'])]),
              ('02.02.02 - Outras Obrigações', [('conta_startswith', '2.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['obriga'])]),
              ('02.02.02.01 - Com Partes Relacionadas', [('conta_startswith', '2.02.02.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['relacionad'])]),
              ('02.02.02.02 - Outras Obrigações', [('conta_startswith', '2.02.02.02'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['outr'])]),
              ('02.02.03 - Tributos Diferidos', [('conta_startswith', '2.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', 'tributo')]),
              ('02.02.03.01 - Imposto de Renda e Contribuição Social', [('conta_startswith', '2.02.03'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['imposto de renda', 'contribuição social'])]),
              ('02.02.03.02 - Outros tributos diferidos', [('conta_startswith', '2.02.03'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains_not', ['imposto de renda', 'contribuição social'])]),
              ('02.02.04 - Provisões', [('conta_startswith', '2.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', 'provis')]),
              ('02.02.04.01 - Provisões Específicas', [('conta_startswith', '2.02.04.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'provis')]),
              ('02.02.04.01.01 - Provisões Fiscais', [('conta_startswith', '2.02.04.01.01'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', 'fisca')]),
              ('02.02.04.01.02 - Provisões Trabalhistas e Previdenciárias', [('conta_startswith', '2.02.04.01.02'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', 'trabalhist')]),
              ('02.02.04.01.03 - Provisões para Benefícios a Empregados', [('conta_startswith', '2.02.04.01.03'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', 'benefício')]),
              ('02.02.04.01.04 - Provisões Judiciais Cíveis', [('conta_startswith', '2.02.04.01.04'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', 'cív')]),
              ('02.02.04.02 - Outras Provisões', [('conta_startswith', '2.02.04.02'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'provis')]),
              ('02.02.04.02.01 - Provisões para Garantias', [('conta_startswith', '2.02.04.02'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', 'garantia')]),
              ('02.02.04.02.02 - Provisões para Reestruturação', [('conta_startswith', '2.02.04.02'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', 'reestrutura')]),
              ('02.02.04.02.03 - Provisões para Passivos Ambientais e de Desativação', [('conta_startswith', '2.02.04.02'), ('conta_levelmin', 5), ('conta_levelmax', 5), ('descricao_contains', ['ambient'])]),
              ('02.02.05 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados', [('conta_startswith', '2.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['Passivos sobre ativos'])]),
              ('02.02.05.01 - Passivos sobre Ativos Não-Correntes a Venda', [('conta_startswith', '2.02.05.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['venda'])]),
              ('02.02.05.02 - Passivos sobre Ativos de Operações Descontinuadas', [('conta_startswith', '2.02.05.02'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['descontinuad'])]),
              ('02.02.06 - Lucros e Receitas a Apropriar', [('conta_startswith', '2.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['lucros e receitas'])]),
              ('02.02.06.01 - Lucros a Apropriar', [('conta_startswith', '2.02.06.01'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['lucr'])]),
              ('02.02.06.02 - Receitas a Apropriar', [('conta_startswith', '2.02.06.02'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['receit'])]),
              ('02.02.06.03 - Subvenções de Investimento a Apropriar', [('conta_startswith', '2.02.06.03'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['subvenç'])]),
              ('02.02.09 - Outros Passivos', [('conta_startswith', ['2.02.07', '2.02.08', '2.02.09']), ('conta_levelmin', 3), ('conta_levelmax', 3)]),
              ('02.03 - Patrimônio Líquido', [('conta_startswith', '2.'), ('conta_levelmin', 2), ('conta_levelmax', 2), ('descricao_contains', 'patrimônio')]),
              ('02.03.01 - Capital Social', [('conta_startswith', '2.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['2.01', '2.02']), ('descricao_contains', ['capital social'])]),
              ('02.03.02 - Reservas de Capital', [('conta_startswith', '2.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['2.01', '2.02']), ('descricao_contains', ['reservas de capital'])]),
              ('02.03.03 - Reservas de Reavaliação', [('conta_startswith', '2.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['2.01', '2.02']), ('descricao_contains', ['reservas de reavaliaç'])]),
              ('02.03.04 - Reservas de Lucros', [('conta_startswith', '2.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['2.01', '2.02']), ('descricao_contains', ['reservas de lucro'])]),
              ('02.03.05 - Lucros ou Prejuízos Acumulados', [('conta_startswith', '2.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['2.01', '2.02']), ('descricao_contains', ['lucro', 'prejuízo', 'acumulad']), ('descricao_contains_not', 'reserva')]),
              ('02.03.06 - Ajustes de Avaliação Patrimonial', [('conta_startswith', '2.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['2.01', '2.02']), ('descricao_contains', ['avaliação patrimonial'])]),
              ('02.03.07 - Ajustes Acumulados de Conversão', [('conta_startswith', '2.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['2.01', '2.02']), ('descricao_contains', ['ajustes acumulados'])]),
              ('02.03.08 - Outros Resultados Abrangentes', [('conta_startswith', '2.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith_not', ['2.01', '2.02']), ('descricao_contains', ['resultados abrangentes'])]),
              ('02.04 - Outros Passivos ou Provissões', [('conta_startswith', ['2.04', '2.05', '2.06', '2.07', '2.08', '2.09']), ('conta_levelmin', 2), ('conta_levelmax', 2), ('descricao_contains_not', 'patrimonio')]),
        ]
        d2 = get_dtp_lines(df, d2_demo, d2_lines)

        d3_demo = 'Demonstração do Resultado'
        d3_lines = [
            ('03.01 - Receita Bruta', [('conta_exact', '3.01')]),
            ('03.02 - Custo de Produção', [('conta_exact', '3.02')]),
            ('03.03 - Resultado Bruto (Receita Líquida)', [('conta_exact', '3.03')]),
            ('03.04 - Despesas Operacionais', [('conta_exact', '3.04')]),
            ('03.04.01 - Despesas com Vendas', [('conta_exact', '3.04.01')]),
            ('03.04.02 - Despesas Gerais e Administrativas', [('conta_exact', '3.04.02')]),
            ('03.04.09 - Outras despesas, receitas ou equivalências', [('conta_levelmin', 3), ('conta_levelmax', 3), ('conta_startswith', ['3.04.']), ('conta_startswith_not', ['3.04.01', '3.04.02'])]),
            ('03.05 - LAJIR EBIT Resultado Antes do Resultado Financeiro e dos Tributos', [('conta_exact', '3.05')]),
            ('03.06 - Resultado Financeiro (Não Operacional)', [('conta_exact', '3.06')]),
            ('03.07 - Resultado Antes dos Tributos sobre o Lucro', [('conta_exact', '3.07')]),
            ('03.08 - Impostos IRPJ e CSLL', [('conta_exact', '3.08')]),
            ('03.09 - Resultado Líquido das Operações Continuadas', [('conta_exact', '3.09')]),
            ('03.10 - Resultado Líquido das Operações Descontinuadas', [('conta_exact', '3.10')]),
            ('03.11 - Lucro Líquido', [('conta_exact', '3.11')]),
        ]
        d3 = get_dtp_lines(df, d3_demo, d3_lines)

        d6_demo = 'Demonstração de Fluxo de Caixa'
        # imobilizado e intangível
        kw60201 = ['investiment', 'mobiliár', 'derivativ', 'propriedad']
        kw60202 = ['imob', 'intangív']
        kw60203 = ['financeir']
        kw60204 = ['coligad', 'controlad', 'ligad']
        kw60205 = ['juro', 'jcp', 'jscp', 'dividend']
        kw602 = list(set(kw60201 + kw60202 + kw60203 + kw60204 + kw60205))
        # dividend juros jcp, jscp bonifica, 
        kw60301 = ['capital']
        kw60302 = ['ação', 'ações', 'acionist']
        kw60303 = ['debentur', 'empréstim', 'financiam']
        kw60304 = ['credor']
        kw60305 = ['amortizaç', 'captaç']
        kw60306 = ['dividend', 'juros', 'jcp', 'bonifica']
        kw603 = list(set(kw60301 + kw60302 + kw60303 + kw60304 + kw60305 + kw60306))
        d6_lines = [
            ('06.01 - Caixa das Operações', [('conta_exact', '6.01')]),
            ('06.01.01 - Caixa das Operações', [('conta_startswith', '6.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['operac']), ('descricao_contains_not', ['ativ', 'print(e)iv', 'despes', 'ingress', 'pagament', 'receb', 'arrendament', 'aquisic'])]),
            ('06.01.02 - Variações de Ativos e Passivos', [('conta_startswith', '6.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['ativ']), ('descricao_contains_not', ['operac', 'imob', 'intangív', 'adiantament', 'provis', 'permanent', 'despes', 'pagament', 'recebiment', 'caixa', 'derivativ', 'judicia'])]),
            ('06.01.09 - Outros Caixas Operacionais', [('conta_startswith', '6.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains_not', ['ativ', 'operac'])]),
            ('06.02 - Caixa de Investimentos CAPEX', [('conta_exact', '6.02')]),
            ('06.02.01 - Investimentos', [('conta_startswith', '6.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60201), ('descricao_contains_not', list_subtract(kw602, kw60201))]),
            ('06.02.02 - Imobilizado e Intangível', [('conta_startswith', '6.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60202), ('descricao_contains_not', list_subtract(kw602, kw60202))]),
            ('06.02.03 - Aplicações Financeiras', [('conta_startswith', '6.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60203), ('descricao_contains_not', list_subtract(kw602, kw60203))]),
            ('06.02.04 - Coligadas e Controladas', [('conta_startswith', '6.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60204), ('descricao_contains_not', list_subtract(kw602, kw60204))]),
            ('06.02.05 - Juros sobre Capital Próprio e Dividendos', [('conta_startswith', '6.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60205), ('descricao_contains_not', list_subtract(kw602, kw60205))]),
            ('06.02.09 - Outros Caixas de Investimento', [('conta_startswith', '6.02.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains_not', kw602)]),
            ('06.03 - Caixa de Financiamento', [('conta_exact', '6.03')]),
            ('06.03.01 - Capital', [('conta_startswith', '6.03.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60301), ('descricao_contains_not', list_subtract(kw603, kw60301))]),
            ('06.03.02 - Ações e Acionistas', [('conta_startswith', '6.03.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60302), ('descricao_contains_not', list_subtract(kw603, kw60302))]),
            ('06.03.03 - Debêntures, empréstimos e financiamentos', [('conta_startswith', '6.03.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60303), ('descricao_contains_not', list_subtract(kw603, kw60303))]),
            ('06.03.04 - Credores', [('conta_startswith', '6.03.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60304), ('descricao_contains_not', list_subtract(kw603, kw60304))]),
            ('06.03.05 - Captações e Amortizações', [('conta_startswith', '6.03.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60305), ('descricao_contains_not', list_subtract(kw603, kw60305))]),
            ('06.03.06 - Juros JCP e Dividendos', [('conta_startswith', '6.03.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', kw60306), ('descricao_contains_not', list_subtract(kw603, kw60306))]),
            ('06.03.09 - Outros Caixas de Financiamento', [('conta_startswith', '6.03.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains_not', kw603)]),
            ('06.04 - Caixa da Variação Cambial', [('conta_exact', '6.04')]),
            ('06.05 - Variação do Caixa', [('conta_exact', '6.05')]),
            ('06.05.01 - Saldo Inicial do Caixa ', [('conta_exact', '6.05.01')]),
            ('06.05.02 - Saldo Final do Caixa', [('conta_exact', '6.05.02')]),
        ]
        d6 = get_dtp_lines(df, d6_demo, d6_lines)

        d7_demo = 'Demonstração de Valor Adiconado'
        d7_lines = [
              ('07.01 - Receitas', [('conta_startswith', '7.'), ('descricao_contains', ['receita']), ('descricao_contains_not', 'líquid')]),
              ('07.01.01 - Vendas', [('conta_exact', '7.01.01')]),
              ('07.01.02 - Outras Receitas', [('conta_exact', '7.01.02')]),
              ('07.01.03 - Ativos Próprios', [('conta_exact', '7.01.03')]),
              ('07.01.04 - Reversão de Créditos Podres', [('conta_exact', '7.01.04')]),
              ('07.02 - Custos dos Insumos', [('conta_startswith', '7.'), ('descricao_contains', ['insumos adquiridos', 'intermediação financeira', 'provis'])]),
              ('07.02.01 - Custo de Mercadorias', [('conta_exact', '7.02.01')]),
              ('07.02.02 - Custo de Materiais, Energia e Terceiros', [('conta_exact', '7.02.02')]),
              ('07.02.03 - Valores Ativos', [('conta_exact', '7.02.03')]),
              ('07.02.04 - Outros', [('conta_exact', '7.02.04')]),
              ('07.03 - Valor Adicionado Bruto', [('conta_startswith', '7.'), ('descricao_contains', ['valor adicionado bruto'])]),
              ('07.04 - Retenções', [('conta_startswith', '7.'), ('descricao_contains', ['retenç', 'Benefíci', 'sinistr'])]),
              ('07.04.01 - Depreciação e Amortização', [('conta_startswith', '7.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['deprecia', 'amortiza', 'exaust'])]),
              ('07.04.02 - Outras retenções', [('conta_exact', '7.04.02')]),
              ('07.05 - Valor Adicionado Líquido', [('conta_startswith', '7.'), ('descricao_contains', ['valor adicionado líquid', 'receita operacional']), ('conta_startswith_not', '7.01'), ('descricao_contains_not', 'transferência')]),
              ('07.06 - Valor Adicionado em Transferência', [('conta_startswith', '7.'), ('descricao_contains', ['transferência'])]),
              ('07.06.01 - Resultado de Equivalência Patrimonial', [('conta_startswith', '7.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['equivalencia patrimonial'])]),
              ('07.06.02 - Receitas Financeiras', [('conta_exact', '7.06.02')]),
              ('07.06.03 - Outros', [('conta_exact', '7.06.03')]),
              ('07.07 - Valor Adicionado Total a Distribuir', [('conta_startswith', '7.'), ('descricao_contains', ['total a distribuir'])]),
              ('07.08 - Distribuição do Valor Adicionado', [('conta_startswith', '7.'), ('descricao_contains', 'Distribuição do Valor Adicionado')]),
              ('07.08.01 - Pessoal', [('conta_startswith', '7.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', 'pessoal')]),
              ('07.08.01.01 - Remuneração Direta', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'remuneração direta')]),
              ('07.08.01.02 - Benefícios', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'benefícios')]),
              ('07.08.01.03 - FGTS', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['F.G.T.S.', 'fgts'])]),
              ('07.08.01.04 - Outros', [('conta_exact', '7.08.01.04')]),
              ('07.08.02 - Impostos, Taxas e Contribuições', [('conta_startswith', '7.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['imposto', 'taxa', 'contribuiç'])]),
              ('07.08.02.01 - Federais', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'federa')]),
              ('07.08.02.02 - Estaduais', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'estadua')]),
              ('07.08.02.03 - Municipais', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'municipa')]),
              ('07.08.03 - Remuneração de Capital de Terceiros', [('conta_startswith', '7.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['remuneraç', 'capital', 'terceir']), ('descricao_contains_not', 'própri')]),
              ('07.08.03.01 - Juros Pagos', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['juro']), ('descricao_contains_not', 'propri')]),
              ('07.08.03.02 - Aluguéis', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', 'alugue')]),
              ('07.08.04 - Remuneração de Capital Próprio', [('conta_startswith', '7.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['remuneraç', 'capital', 'própri']), ('descricao_contains_not', 'terceir')]),
              ('07.08.04.01 - Juros sobre o Capital Próprio', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['juros sobre', 'jcp'])]),
              ('07.08.04.02 - Dividendos', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['dividend'])]),
              ('07.08.04.03 - Lucros Retidos', [('conta_startswith', '7.'), ('conta_levelmin', 4), ('conta_levelmax', 4), ('descricao_contains', ['lucros retidos'])]),
              ('07.08.05 - Outros', [('conta_exact', '7.08.05')]),
        ]
        d7 = get_dtp_lines(df, d7_demo, d7_lines)
        
        result = pd.concat([d0, d1, d2, d3, d6, d7], ignore_index=True).drop_duplicates()
    except Exception as e:
        print('error', e)
        result = pd.DataFrame()

    return result

def fundamentalist_dre(df, group):
    try:
      new_lines = []
      # create md_list (magic dre items list)
      md = {}
      for _, row in df.iterrows():
          key = clean_text(row['Conta'] + ' - ' + row['Descrição']).split('  ')
          key = '_' + str(key[0]) + '_' + key[1].replace(' ','_').lower()
          md[key] = row['Valor']
      md_list = [*md.keys()]

      # create line
      line = {col:df[col][df.index[0]] for col in df.columns.to_list()}
      line['Valor'] = None

      new_lines = pd.DataFrame(get_new_lines(md, line))

      result = pd.concat([df, new_lines], ignore_index=True).drop_duplicates()

    except Exception as e:
       print(f'error {e}')
       pass

    return result

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
      buffer = io.BytesIO()
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
    buffer = io.BytesIO()
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

# dre_cvm

def save_pkl(data, filename):
    """Saves data to a pickle file.

    Args:
        data: The data to be saved.
        filename (str): The name of the pickle file (excluding the '.pkl' extension).

    Returns:
        The input data.
    """
    with open(f'{filename}.pkl', 'wb') as f:
        pickle.dump(data, f)
    # with zipfile.ZipFile(f'{filename}.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
    #     # Save the data as a Pickle file within the zip archive
    #     with zipf.open(f'{filename}.pkl', 'w') as data_file:
    #         pickle.dump(data, data_file)

    return data

def load_pkl(filename):
    """Loads data from a pickle file.

    Args:
        filename (str): The name of the pickle file (excluding the '.pkl' extension).

    Returns:
        The loaded data.
    """
    with open(f'{filename}.pkl', 'rb') as f:
        data = pickle.load(f)
    # with zipfile.ZipFile(f'{filename}.zip', 'r') as zipf:
    #     with zipf.open(f'{filename}.pkl', 'r') as data_file:
    #         data = pickle.load(data_file)

    return data

def create_demo_file():
    """Creates a demo dictionary by loading pickled dataframes for each year.

    Args:
        start_year (int): The starting year for loading dataframes.

    Returns:
        dict: A dictionary containing loaded demo dataframes for each year.
    """
    try:
        demo_cvm = {}
        years = range(b3.start_year, datetime.datetime.now().year + 1)
        start_time = time.time()

        for i, year in enumerate(years):
            print(remaining_time(start_time, len(years), i))
            dataframe = load_pkl(f'{b3.app_folder}dataframe_{year}')
            demo_cvm[year] = dataframe
    except Exception as e:
        # print(e)
        pass
    return demo_cvm

def gather_links(url):
  """
  Recursively gathers links to files with specific extensions from a given URL.

  Args:
    url (str): The URL to start gathering links from.
    base_url (str): The base URL to filter links.
    visited_subfolders (set): A set to keep track of visited subfolders.
    filelist (list): A list to store the gathered file links.

  Returns:
    list: A list of gathered file links.
  """

  b3.visited_subfolders.add(url)  # Marcar a subpasta como visitada
  response = b3.session.get(url)
  response.raise_for_status()
  soup = BeautifulSoup(response.content, "html.parser")

  for link in soup.find_all("a"):
    href = link.get("href")
    full_link = urljoin(url, href)

    if full_link.startswith(b3.base_cvm) and full_link not in b3.visited_subfolders:
      if full_link.endswith((".csv", ".zip", ".txt")):
        b3.filelist.append(full_link)
      elif full_link.endswith("/"):
        gather_links(full_link)
  return b3.filelist

def extract_meta(content):
    """
    Extracts metadata from content using specific formatting patterns.

    This function extracts metadata from the provided content, assuming the content
    follows a certain pattern where metadata blocks are separated by "-----------------------"
    and each block contains metadata fields with "Campo" and "Descrição" entries.

    Args:
        content (str): The content from which metadata needs to be extracted.

    Returns:
        dict: A dictionary containing extracted metadata, where keys are metadata field names ("Campo")
              and values are corresponding descriptions ("Descrição").

    Example:
        If content contains metadata in the following format:
        -----------------------
        Campo: Field1
        Descrição: Description for Field1
        -----------------------
        Campo: Field2
        Descrição: Description for Field2
        -----------------------
        The function would return: {'Field1': 'Description for Field1', 'Field2': 'Description for Field2'}
    """
    meta_dict = {}
    blocks = content.split("-----------------------\r\nCampo: ")[1:]
    
    for block in blocks:
        lines = block.strip().split("\r\n")
        campo = lines[0]
        descricao = None
        
        for line in lines:
            if 'Descrição' in line or 'Descrio' in line:
                descricao = line.split(':')[1].strip()
                break
        
        if descricao is not None:
            meta_dict[campo] = descricao
    
    return meta_dict

def get_metadados(filelist):
    """
    Extracts and processes metadata from files in the provided list of file links.

    This function takes a list of file links as input and processes the files to extract metadata.
    It specifically targets files with "meta" in their links and supports both zip files and text files.
    For zip files, it extracts metadata from each file within the zip archive.
    For text files, it decodes the content using 'iso-8859-1' encoding and extracts metadata.

    Args:
        filelist (list): A list of file links containing files with metadata.

    Returns:
        dict: A dictionary containing extracted metadata, where keys are extracted from filenames
              and values are metadata extracted from the corresponding files.

    Raises:
        requests.exceptions.HTTPError: If there is an HTTP error while fetching file content.
    """
    meta_dict = {}
    meta_files = [filelink for filelink in filelist if "meta" in filelink]

    for file in meta_files:
        response = b3.session.get(file)
        response.raise_for_status()

        if file.endswith('.zip'):
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))

            for filein_zip in zip_file.namelist():
                with zip_file.open(filein_zip) as zip_filecontent:
                    filecontent = zip_filecontent.read().decode('utf-8', errors='ignore')
                    d = extract_meta(filecontent)
                    meta_dict[filein_zip.split('.')[0]] = d
        elif file.endswith('.txt'):
            filecontent = response.content.decode('iso-8859-1')
            d = extract_meta(filecontent)
            filename = file.split('/')[-1].split('.')[0]
            meta_dict[filename] = d

    return meta_dict

def get_categories(filelist):
    """
    Extracts and returns categories from a list of file links.

    This function extracts categories from the provided list of file links by considering
    the directory structure relative to the base URL. It sorts and returns a list of unique categories.

    Args:
        filelist (list): A list of file links.

    Returns:
        list: A sorted list of unique categories derived from the file links.

    Example:
        If filelist contains file links like:
        ["https://example.com/files/category1/file1.csv", "https://example.com/files/category2/file2.csv"]
        The function would return: ['category1', 'category2']
    """
    categories = set()
    # meta_files = [filelink for filelink in filelist if "meta" in filelink]
    # files = [filelink for filelink in filelist if "meta" not in filelink]

    for filelink in filelist:
        cat = '/'.join(filelink.replace(b3.base_cvm,'').split('/')[:-2])
        categories.add(cat)
    categories = sorted(list(categories))

    return categories

def get_filelink_df(base_cvm):
    """
    Retrieves file links and associated dates from a list of URLs.

    This function takes a list of URLs (filelist) and extracts folder URLs from the list.
    It then visits each folder URL, extracts file information using an XPath expression,
    and filters the information based on the current year.
    
    Args:
        filelist (list): A list of URLs containing file links.

    Returns:
        pandas.DataFrame: A DataFrame containing file names and dates for the current year.
    """
    filelist = gather_links(base_cvm)
    folders = set()

    # Extract folder URLs from file links
    for url in filelist:
        folder_url = '/'.join(url.split('/')[:-1])
        folders.add(folder_url)

    fileinfo_df = []
    start_time = time.time()
    # Loop through folder URLs and extract file information
    for i, url in enumerate(folders):
        print(remaining_time(start_time, len(folders), i))
        response = requests.get(url)
        response.raise_for_status()
        tree = html.fromstring(response.content)
        contents = tree.xpath(b3.xpath_cvm) 

        # Extract content and process file information
        for content in contents:
            lines = content.text_content().split('\r\n')
            for line in lines:
                parts = line.split()
                if len(parts) >= 3:
                    filename = url + '/' + parts[0]
                    date = pd.to_datetime(f'{parts[1]}', format='%d-%b-%Y')
                    fileinfo_df.append([filename, date])

    # Create and filter DataFrame for the current year
    fileinfo_df = pd.DataFrame(fileinfo_df, columns=['filename', 'date'])

    return fileinfo_df

def download_database(demo_cvms, filelist_df):
    """
    Downloads and processes database files based on specified DEMONSTRATIVO values.

    This function takes a list of DEMONSTRATIVO values and a DataFrame containing file information.
    It downloads and processes database files associated with the specified DEMONSTRATIVO values.
    The downloaded CSV files are extracted, metadata is extracted from filenames, and data is loaded
    into pandas DataFrames with added metadata columns.

    Args:
        demo_cvms (list): A list of DEMONSTRATIVO values to filter files.
        filelist_df (pandas.DataFrame): A DataFrame containing file names and dates.

    Returns:
        list: A list of pandas DataFrames containing processed database files.
    """
    filelist = filelist_df['filename'].to_list()
    total_size = 0  
    total_size_csv = 0
    total_rows = 0
    dataframes = []
    start_time = time.time()

    # Iterate through DEMONSTRATIVO values
    for i, demonstrativo in enumerate(demo_cvms):
        print(remaining_time(start_time, len(demo_cvms), i))
        # Retrieve the list of files based on the specified 'DEMONSTRATIVO'
        download_files = [filelink for filelink in filelist if 'meta' not in filelink and demonstrativo in filelink]

        # Iterate through the list of URLs
        start_time_2 = time.time()
        for j, zip_url in enumerate(download_files):
            print('  ' + remaining_time(start_time_2, len(download_files), j))
            response = requests.get(zip_url)

            # Check if the download was successful
            if response.status_code == 200:
                # Get the size of the downloaded file
                filesize = len(response.content) / (1024 ** 2)
                total_size += filesize

                # Extract the zip file in memory
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                    # Iterate through the files in the zip
                    start_time_3 = time.time()
                    for k, fileinfo in enumerate(zip_ref.infolist()):
                        print('  ' + '  ' + remaining_time(start_time_3, len(zip_ref.infolist()), k))
                        # Check if the file is a CSV
                        if fileinfo.filename.lower().endswith('.csv'):
                            # Extract the CSV file
                            csv_content = zip_ref.read(fileinfo.filename)
                            csv_filename = os.path.basename(fileinfo.filename)

                            # Extract metadata from the CSV filename
                            meta_csv = csv_filename.replace('cia_aberta_', '').replace('.csv', '').split('_')
                            ano = meta_csv[-1]
                            demonstrativo = meta_csv[0]
                            meta_csv = meta_csv[1:-1]
                            if len(meta_csv) > 0:
                                agrupamento = meta_csv[-1]
                                meta_csv = meta_csv[:-1]
                            else:
                                agrupamento = ''
                            balance_sheet = '_'.join(meta_csv)

                            # Read CSV content into a pandas DataFrame
                            csv_data = pd.read_csv(io.BytesIO(csv_content), encoding='iso-8859-1', sep=';')

                            # Add metadata columns to the DataFrame
                            csv_data.insert(0, 'FILENAME', csv_filename)
                            csv_data.insert(1, 'DEMONSTRATIVO', demonstrativo)
                            csv_data.insert(2, 'BALANCE_SHEET', balance_sheet)
                            csv_data.insert(3, 'ANO', ano)
                            csv_data.insert(4, 'AGRUPAMENTO', agrupamento)

                            # Append the DataFrame to the list
                            dataframes.append(csv_data)
                            total_rows += len(csv_data)

    print(f'Total {len(dataframes)} databases found and {total_rows} lines downloaded')
    return dataframes

def yearly(df_list):
    """
    Organizes a list of DataFrames by year.

    This function takes a list of DataFrames and organizes them by year based on the 'DT_REFER' column.
    It creates a dictionary where keys represent years and values are lists of DataFrames for each year.
    It then concatenates the DataFrames within each year's list and returns the organized dictionary.

    Args:
        df_list (list): A list of DataFrames to be organized.

    Returns:
        dict: A dictionary where keys are years and values are concatenated DataFrames for each year.
    """
    df_y = {}
    start_time = time.time()
    # Iterate through each DataFrame in the 'df_list'
    for i, df in enumerate(df_list):
        # Get the year from the 'DT_REFER' column
        year = pd.to_datetime(df['DT_REFER']).dt.year.iloc[0]
        print(year, remaining_time(start_time, len(df_list), i))

        # Check if the year is already a key in the dictionary, if not, create a list for it
        if year not in df_y:
            df_y[year] = []
        
        # Append the DataFrame to the list for the respective year
        df_y[year].append(df)

    print('concatenating')
    start_time = time.time()

    # Concatenate DataFrames within each year's list
    for i, (year, df_list) in enumerate(df_y.items()):
        print(year, remaining_time(start_time, len(df_y), i))
        df_y[year] = pd.concat(df_list, ignore_index=True)

    return df_y

def clean_cell(cell):
    """
    Removes specified words from a cell content.

    This function takes a cell content (string) and removes specified words from it.
    The words to remove are defined in the 'words_to_remove' list.

    Args:
        cell (str): The content of the cell to be cleaned.

    Returns:
        str: The cleaned cell content without the specified words.
    """
    words_to_remove = ['  EM LIQUIDACAO', ' EM LIQUIDACAO', ' EXTRAJUDICIAL', '  EM RECUPERACAO JUDICIAL', '  EM REC JUDICIAL', ' EM RECUPERACAO JUDICIAL']
    for word in words_to_remove:
        if word in cell:
            cell = cell.replace(word, '').strip()
    return cell

def clean_dataframes(dict_of_df):
    """
    Cleans and preprocesses DataFrames in a dictionary.

    This function takes a dictionary of DataFrames and performs various cleaning operations on each DataFrame.
    It removes extra rows, cleans up text columns, converts specified columns to datetime format,
    and applies a text cleaning function to specific columns.

    Args:
        dict_of_df (dict): A dictionary where keys are years and values are DataFrames.

    Returns:
        dict: A dictionary with cleaned and preprocessed DataFrames.
    """
    start_time = time.time()
    for i, (year, df) in enumerate(dict_of_df.items()):
        print(year, remaining_time(start_time, len(dict_of_df), i))
        
        # Remove extra rows based on specific conditions
        try:
            df = df[df['ORDEM_EXERC'] == 'ÚLTIMO']
            df = df.drop(columns=['ORDEM_EXERC'])
        except Exception as e:
            # print(e)
            pass
        
        # Clean up text in 'DENOM_CIA' column
        try:
            df['DENOM_CIA'] = df['DENOM_CIA'].apply(clean_text)
        except Exception as e:
            pass

        # Convert specified columns to datetime format
        try:
            df[col_datetime] = df[col_datetime].apply(pd.to_datetime)
        except Exception as e:
            pass

        # Apply a text cleaning function to 'DENOM_CIA' column
        df['DENOM_CIA'] = df['DENOM_CIA'].apply(clean_cell)

        dict_of_df[year] = df

    return dict_of_df

def group_by_year(dataframes):
    demo_cvm = [df for df in dataframes if len(df) > 0 and ('con' in df['FILENAME'][0] or 'ind' in df['FILENAME'][0])]
    links = [df for df in dataframes if len(df) > 0 and ('con' not in df['FILENAME'][0] and 'ind' not in df['FILENAME'][0])]

    print('split by year')
    demo_cvm = yearly(demo_cvm)
    links = yearly(links)

    print('clean up dataframes')
    demo_cvm = clean_dataframes(demo_cvm)
    links = clean_dataframes(links)

    # Rename column for consistency
    for year in links.keys():
        links[year].rename(columns={'VERSAO': 'VERSAO_LINK'}, inplace=True)
    
    return demo_cvm, links

def clean_DT_INI_EXERC(demo_cvm):
    """
    Filters and cleans the 'DT_INI_EXERC' column in DataFrames.

    This function takes a dictionary of DataFrames and filters each DataFrame based on the 'DT_INI_EXERC' column.
    It keeps rows where the 'DT_INI_EXERC' column matches the year's starting date (January 1) or is NaN.

    Args:
        demo_cvm (dict): A dictionary where keys are years and values are DataFrames.

    Returns:
        dict: A dictionary with DataFrames filtered and cleaned based on the 'DT_INI_EXERC' column.
    """
    try:
        lines_removed = 0
        for i, (year, df) in enumerate(demo_cvm.items()):
            size = len(df)
            
            # Apply the condition to filter the DataFrame
            mask = (df['DT_INI_EXERC'] == pd.to_datetime(str(year) + '-01-01')) | df['DT_INI_EXERC'].isna()
            df_filtered = df[mask].copy()  # Make a copy to avoid modifying the original DataFrame
            
            # Update the dictionary with the filtered DataFrame
            demo_cvm[year] = df_filtered
            
            lines_removed += size - len(df_filtered)
            print(year, remaining_time(start_time, len(demo_cvm), i))
        
        print(f'{lines_removed} lines removed')
    except Exception as e:
        pass

    return demo_cvm

def update_cvm_files():
    """
    Update the demo_cvm files based on new data from filelist_df.

    Args:
    filelist_df (pd.DataFrame): DataFrame containing file links and dates.

    Returns:
    dict: Updated demo_cvm data.

    This function updates the demo_cvm files by downloading new data based on filelist_df.
    It first retrieves the DataFrame containing file links from the base_cvm URL.
    It reads the last update date from 'last_update.txt' and filters the filelist_df to include only files
    with dates greater than the last update. The last update date is then updated in 'last_update.txt'.
    The function downloads the database files for 'itr' and 'dfp' demo_cvm types, groups the dataframes by year,
    and cleans the DT_INI_EXERC column in the demo_cvm data. It also loads the existing demo_cvm data and
    updates missing years with data from demo_cvm_existing. The updated demo_cvm data is saved and returned.

    Additionally, the function retrieves metadata and categories from the filelist. It extracts specific
    demonstrativos_cvm and prints the results including base_cvm URL, the number of categories,
    the count of meta files, and the total fields. Finally, it prints the list of demonstrativos_cvm.

    """
    # Retrieve DataFrame containing file links from base_cvm URL
    filelist_df = get_filelink_df(b3.base_cvm)
    last_update2 = filelist_df['date'].max().strftime('%Y-%m-%d')
    filelist = filelist_df['filename'].to_list()

    try:
        # Read last update date from 'last_update.txt' if available, else set to '1970-01-01'
        with open(f'{b3.app_folder}last_update.txt', 'r') as f:
            last_update = f.read().strip()
        if not last_update:
            last_update = '1970-01-01'
    except Exception as e:
        last_update = '1970-01-01'

    # Filter filelist_df to include only files with dates greater than last_update
    filelist_df = filelist_df[filelist_df['date'] > (pd.to_datetime(last_update) + pd.DateOffset(days=1))]

    # List of demo_cvm types to download
    demo_cvms = ['itr', 'dfp']

    # Download database files for demo_cvms and group dataframes by year
    dataframes = download_database(demo_cvms, filelist_df)
    demo_cvm, links = group_by_year(dataframes)

    # Clean the DT_INI_EXERC column in demo_cvm data
    demo_cvm = clean_DT_INI_EXERC(demo_cvm)

    print('saving updated database (may take up to 5 min)')
    # Load existing demo_cvm data
    try:
        demo_cvm_existing = load_pkl(f'{b3.app_folder}database')
    except Exception as e:
        demo_cvm_existing = {}

    # Update demo_cvm with values from demo_cvm_existing if missing years
    for year, df in demo_cvm_existing.items():
        if year not in demo_cvm:
            demo_cvm[year] = df
    demo_cvm = OrderedDict(sorted(demo_cvm.items()))

    # Save updated demo_cvm data

    category_columns = ['FILENAME', 'DEMONSTRATIVO', 'BALANCE_SHEET', 'ANO', 'AGRUPAMENTO', 'CNPJ_CIA', 'VERSAO', 'DENOM_CIA', 'CD_CVM', 'GRUPO_DFP', 'MOEDA', 'ESCALA_MOEDA', 'CD_CONTA', 'DS_CONTA','ST_CONTA_FIXA', 'COLUNA_DF', ]
    datetime_columns = ['DT_REFER', 'DT_FIM_EXERC', 'DT_INI_EXERC', ]
    numeric_columns = ['VL_CONTA', ]

    # Change data types for columns
    for year, df in demo_cvm.items():
        for column in df.columns:
            if column in category_columns:
                try:
                    df[column] = df[column].astype('category')
                except Exception as e:
                    pass
            elif column in datetime_columns:
                try:
                    df[column] = pd.to_datetime(df[column])
                except Exception as e:
                    pass
            elif column in numeric_columns:
                try:
                    df[column] = pd.to_numeric(df[column], errors='ignore')
                except Exception as e:
                    pass

    # Save demo_cvm as pickle
    if not filelist_df.empty:
        demo_cvm = save_pkl(demo_cvm, f'{b3.app_folder}database')

    try:
        # Write the maximum date from filtered filelist_df to 'last_update.txt'
        print('last update', last_update2)
        with open(f'{b3.app_folder}last_update.txt', 'w') as f:
            f.write(last_update2)
    except Exception as e:
        pass

    # Get metadata and categories from filelist
    meta_dict = get_metadados(filelist)
    categories = get_categories(filelist)
    demonstrativos_cvm = []
    for cat in categories:
        term = 'DOC/'
        if term in cat:
            demonstrativos_cvm.append(cat.replace(term,'').lower())

    # Print results
    total_fields = sum((i + 1) * len(d) for i, d in enumerate(meta_dict.values()))
    print(f'{b3.base_cvm}')
    print(f'Encontradas {len(categories)} categorias com {len(meta_dict)} arquivos meta contendo {total_fields} campos')
    print(demonstrativos_cvm)

    return demo_cvm, meta_dict, demonstrativos_cvm

def get_companies_by_str_port(df):
    """
    Get a list of companies grouped by 'ind' and 'con' in a structured report.

    Args:
        df (pd.DataFrame): DataFrame containing financial data.

    Returns:
        dict: Dictionary with keys 'ind', 'con', and ('ind', 'con') combinations
              mapped to lists of corresponding 'DENOM_CIA' values.

    This function calculates the list of companies grouped by 'ind' (individual) and 'con'
    (consolidated) in a structured report. It utilizes a pivot table to count occurrences of
    'ind' and 'con' for each company and reporting date. The resulting dictionary stores
    'ind' and 'con' as keys and their corresponding 'DENOM_CIA' values.

    Example:
        To use this function, provide a DataFrame containing financial data ('df') as input.
        The function will return a dictionary with keys 'ind', 'con', and ('ind', 'con')
        combinations, each mapped to lists of 'DENOM_CIA' values belonging to that group.
    """
    # Create a pivot table to count occurrences of 'ind' and 'con'
    pivot_table = df.pivot_table(index=['DENOM_CIA', 'DT_REFER'], columns='AGRUPAMENTO', aggfunc='size', fill_value=0)
    
    # Convert counts to boolean values (True if count > 0, else False)
    pivot_table = pivot_table.applymap(lambda x: True if x > 0 else False)
    pivot_table = pivot_table[['ind'] + [col for col in pivot_table.columns if col != 'ind' and col != 'con'] + ['con']]

    # Get unique combinations of rows as tuples
    combinations = set(map(tuple, pivot_table.to_numpy()))

    # Create a dictionary to store combinations and corresponding 'DENOM_CIA'
    companies_by_str_port = {}

    # Find matching 'DENOM_CIA' for each combination
    for combination in combinations:
        relest_individual = combination[0]
        relest_consolidado = combination[1]
        cias = pivot_table[(pivot_table['ind'] == relest_individual) & (pivot_table['con'] == relest_consolidado)].index.get_level_values('DENOM_CIA').unique()
        key = ('ind', 'con')
        if relest_consolidado and not relest_individual:
            key = 'con'
        if not relest_consolidado and relest_individual:
            key = 'ind'

        companies_by_str_port[key] = cias

    return companies_by_str_port

def perform_math_magic(demo_cvm, max_iterations=20000000):
    """
    Perform 'magic' calculations on the DataFrame demo_cvm based on specified quarters.

    Args:
        demo_cvm (dict): Dictionary of DataFrames containing financial data.
        last_quarters (list): List of quarters considered as last quarters.
        all_quarters (list): List of quarters considered as all quarters.
        max_iterations (int): Maximum number of iterations to perform.

    Returns:
        dict: Updated demo_cvm with 'magic' calculations.

    This function iterates through the provided demo_cvm DataFrames, performs calculations based on specified quarters,
    and updates the 'VL_CONTA' values where necessary.
    """
    try:
        print('entering the smart mathmagic world... It takes long time, came back tomorrow... ')
        start_time = time.time()
        # Iterate through each year's DataFrame
        for n1, (year, demonstrativo_cvm) in enumerate(demo_cvm.items()):
            companies_by_str_port = get_companies_by_str_port(demonstrativo_cvm)
            print(f"{year} {len(demonstrativo_cvm):,.0f} lines, {len(demonstrativo_cvm['DENOM_CIA'].unique())} companies, {'/'.join([f'{len(companies)} {key}' for key, companies in companies_by_str_port.items()])}")
            print(year, remaining_time(start_time, len(demo_cvm), n1))
            # Convert DT_REFER to datetime
            demonstrativo_cvm['DT_REFER'] = pd.to_datetime(demonstrativo_cvm['DT_REFER'])
            groups = demonstrativo_cvm.groupby(['DENOM_CIA', 'AGRUPAMENTO'], group_keys=False)
            start_time_2 = time.time()
            for n2, (key, group) in enumerate(groups):
                print('  ', remaining_time(start_time_2, len(groups), n2))
                company = key[0]
                agg = key[1]
                subgroups = group.groupby(['CD_CONTA', 'DS_CONTA'], group_keys=False)
                
                start_time_3 = time.time()
                for n3, (index, df) in enumerate(subgroups):
                    # print('  ', '  ', remaining_time(start_time_3, len(subgroups), n3))
                    conta_first = index[0][0]
                   
                    try:
                        i1 = df[df['DT_REFER'].dt.quarter == 1].index[0]
                        q1 = df[df['DT_REFER'].dt.quarter == 1]['VL_CONTA'].iloc[0]
                    except Exception:
                        q1 = 0
                    try:
                        i2 = df[df['DT_REFER'].dt.quarter == 2].index[0]
                        q2 = df[df['DT_REFER'].dt.quarter == 2]['VL_CONTA'].iloc[0]
                    except Exception:
                        q2 = 0
                    try:
                        i3 = df[df['DT_REFER'].dt.quarter == 3].index[0]
                        q3 = df[df['DT_REFER'].dt.quarter == 3]['VL_CONTA'].iloc[0]
                    except Exception:
                        q3 = 0
                    try:
                        i4 = df[df['DT_REFER'].dt.quarter == 4].index[0]
                        q4 = df[df['DT_REFER'].dt.quarter == 4]['VL_CONTA'].iloc[0]
                    except Exception:
                        q4 = 0

                    update = False
                    try:
                        # Perform calculations based on specified quarters and update flag
                        if conta_first in b3.last_quarters and i4:
                            q4 = q4 - (q3)
                            update = True
                        elif conta_first in b3.all_quarters and i2 and i3 and i4:
                            q4 = q4 - (q3)
                            q3 = q3 - (q2)
                            q2 = q2 - (q1)
                            update = True
                    except Exception as e:
                        update = False

                    if update:
                        # Update 'VL_CONTA' values
                        try:
                           demonstrativo_cvm.loc[i1, 'VL_CONTA'] = q1
                        except Exception as e:
                            pass
                        try:
                           demonstrativo_cvm.loc[i2, 'VL_CONTA'] = q2
                        except Exception as e:
                            pass
                        try:
                           demonstrativo_cvm.loc[i3, 'VL_CONTA'] = q3
                        except Exception as e:
                            pass
                        try:
                           demonstrativo_cvm.loc[i4, 'VL_CONTA'] = q4
                        except Exception as e:
                            pass

                    if n3 > max_iterations:
                        break
                if n2 > max_iterations:
                    break
            demo_cvm[year] = demonstrativo_cvm
            if n1 > max_iterations:
                break
    except Exception as e:
       pass
    return demo_cvm

def year_to_company(demo_cvm):
# Get all unique companies across all years
    all_companies = set()
    for i, (year, df) in enumerate(demo_cvm.items()):
        all_companies.update(df['DENOM_CIA'].unique())

    # Initialize the final dictionary with companies as keys
    companies = {}

    # Populate the company_dict
    start_time = time.time()
    try:
        for i, company in enumerate(all_companies):
          if company == 'ALPARGATAS SA':
            print(remaining_time(start_time, len(all_companies), i))
            company_df = []  # This will hold dataframes for each year for the company
            for j, (year, df) in enumerate(demo_cvm.items()):
                company_data = df[df['DENOM_CIA'] == company]
                company_df.append(company_data)
            companies[company] = pd.concat(company_df, ignore_index=True)
    except Exception as e:
        pass    
        # Concatenate the data for the company across all years

    companies = save_pkl(companies, f'{b3.app_folder}database')
    return companies