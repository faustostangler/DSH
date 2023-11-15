import assets.helper as b3

from typing import Dict, List, Union, Tuple, Optional, Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
 
import unidecode
import string

import os
import re

import pandas as pd
import numpy as np
import math
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import plotly.graph_objects as go
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots


from google.cloud import storage
import json
import gzip
import io
import base64

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

from tqdm import tqdm
import shutil

import random

import multiprocessing
from multiprocessing import Pool

import winsound

# general functions
def sys_beep(frequency=5000, duration=50):
    winsound.Beep(frequency, duration)
    return True

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

def sys_clean_text(text):
    """
    Cleans text by removing any leading/trailing white space, converting it to lowercase, removing
    accents, punctuation, and converting to uppercase.
    
    Args:
    text (str): The input text to clean.
    
    Returns:
    str: The cleaned text.
    """
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception as e:
            print(f"{text} is not convertible to string: {e}")
            return text

    # Remove accents, punctuation, and convert to uppercase
    text = unidecode.unidecode(text).translate(str.maketrans('', '', string.punctuation)).upper().strip()

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    return text

def sys_remaining_time(start_time, size, i):
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
  sys_beep()

  return progress

def sys_header_random():
    user_agent = random.choice(b3.USER_AGENTS)
    referer = random.choice(b3.REFERERS)
    language = random.choice(b3.LANGUAGES)

    headers = {
        'User-Agent': user_agent,
        'Referer': referer,
        'Accept-Language': language
    }

    return headers

# selenium functions
def load_browser_old():
    """
    Launches chromedriver and creates a wait object.
    
    Returns:
    tuple: A tuple containing a WebDriver instance and a WebDriverWait instance.
    """
    try:
        # Define the options for the ChromeDriver.
        options = Options()
        # options.add_argument('--headless')  # Run in headless mode.
        options.add_argument('--no-sandbox')  # Avoid sandboxing.
        options.add_argument('--disable-dev-shm-usage')  # Disable shared memory usage.
        options.add_argument('--disable-blink-features=AutomationControlled')  # Disable automated control.
        # options = Options()
        options.add_argument('start-maximized')  # Maximize the window on startup.

        # chrome_browser_path = "C:\\path_to_chrome\\chrome-win64\\chrome.exe"
        chromedriver_path = "D:\\Fausto Stangler\\Documentos\\Python\\DSH\\chromedriver-win64\\chromedriver.exe"
        options = webdriver.ChromeOptions()
        # options.binary_location = chrome_browser_path

        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        print('raw browser load')
        # Install and start the ChromeDriver service, passing in the options.
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Define the exceptions to ignore during WebDriverWait.
        exceptions_ignore = (NoSuchElementException, StaleElementReferenceException)
        
        # Create a WebDriverWait instance for the driver, using the specified wait time and exceptions to ignore.
        wait = WebDriverWait(driver, b3.driver_wait_time, ignored_exceptions=exceptions_ignore)
        b3.set_driver_and_wait(driver, wait)
    except Exception as e:
        pass
    # Return a tuple containing the driver and the wait object.
    return driver, wait

def sys_load_browser(chromedriver_path="D:\\Fausto Stangler\\Documentos\\Python\\DSH\\chromedriver-win64\\chromedriver.exe", driver_wait_time=5):
    """
    Launches chromedriver and creates a wait object.
    
    Parameters:
    - chromedriver_path (str): The path to the chromedriver executable.
    - driver_wait_time (int): The time to wait for elements to appear.
    
    Returns:
    tuple: A tuple containing a WebDriver instance and a WebDriverWait instance.
    """
    driver_wait_time = b3.driver_wait_time
    try:
        # Define the options for the ChromeDriver.
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # Run in headless mode.
        options.add_argument('--no-sandbox')  # Avoid sandboxing.
        options.add_argument('--disable-dev-shm-usage')  # Disable shared memory usage.
        options.add_argument('--disable-blink-features=AutomationControlled')  # Disable automated control.
        options.add_argument('start-maximized')  # Maximize the window on startup.

        # Initialize the ChromeDriver.
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        
        # Define the exceptions to ignore during WebDriverWait.
        exceptions_ignore = (NoSuchElementException, StaleElementReferenceException)
        
        # Create a WebDriverWait instance for the driver, using the specified wait time and exceptions to ignore.
        wait = WebDriverWait(driver, driver_wait_time, ignored_exceptions=exceptions_ignore)
    except Exception as e:
        print(f"Error initializing browser: {str(e)}")
        return None, None
    
    # Return a tuple containing the driver and the wait object.
    return driver, wait

def get_company(i, driver, wait): # old def, is it usefull, is another one better??
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
    xpath = f'//*[@id="nav-bloco"]/div/div[{i}]/div/div/p[3]'
    listagem = wText(xpath, wait)
    list_dict = dict(zip(b3.listagem_siglas, b3.listagem_extenso))
    for word, replacement in list_dict.items():
      listagem = sys_clean_text(listagem.replace(word, replacement))
  except Exception as e:
    listagem = ''

  # company name
  try:
    xpath = f'//*[@id="nav-bloco"]/div/div[{i}]/div/div/p[1]'
    company_name = sys_clean_text(wText(xpath, wait))
  except Exception as e:
    company_name = ''

  # pregao
  try:
    xpath = f'//*[@id="nav-bloco"]/div/div[{i}]/div/div/p[2]'
    pregao = sys_clean_text(wText(xpath, wait))
  except Exception as e:
    pregao = company_name
  
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
    segmento = sys_clean_text(setor.split(' / ')[2].strip())
    subsetor = sys_clean_text(setor.split(' / ')[1].strip())
    setor = sys_clean_text(setor.split(' / ')[0].strip())
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
    escriturador = sys_clean_text(' '.join(pd.Series(escriturador).drop_duplicates().tolist()))
  except Exception as e:
    escriturador = ''

  # url
  url = f'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/main/{cvm}/{ticker}/overview?language=pt-br'

  company = [pregao, company_name, cvm, listagem, ticker, tickers, asin, cnpj, site, setor, subsetor, segmento, atividade, escriturador, url]

  return company

def b3_get_ticker_keywords(raw_code):
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
        ticker = sys_clean_text(card.find('h5', class_='card-title2').text)
        company_name = sys_clean_text(card.find('p', class_='card-title').text)
        pregao = sys_clean_text(card.find('p', class_='card-text').text)
        listagem = sys_clean_text(card.find('p', class_='card-nome').text)
        if listagem:
            for abbr, full_name in b3.abbreviations_dict.items():
                new_listagem = sys_clean_text(listagem.replace(abbr, full_name))
                if new_listagem != listagem:
                    listagem = new_listagem
                    break  # Break out of the loop if a replacement was made

        # Append the ticker and company name to the keyword list
        keyword = [ticker, company_name, pregao, listagem]
        keywords.append(keyword)
        # print(keyword)
      except Exception as e:
        # print(e)
        pass


  df = pd.DataFrame(keywords, columns=['ticker', 'company_name', 'pregao', 'listagem'])
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
def sys_read_or_create_dataframe(filename, cols):
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
      df = sys_download_from_gcs(filename+'errorgoogle')
      df = sys_save_and_pickle(df, filename)
      pass
    except Exception as e:
      try:
        df = pd.read_pickle(filepath)  # Try to read the file as a pickle.
        df = sys_upload_to_gcs(df, filename)
      except Exception as e:
        # print(f'Error occurred while reading file {filename}: {e}')
        df = pd.DataFrame(columns=cols)
        
    df.drop_duplicates(inplace=True)  # Remove any duplicate rows (if any).
    
    print(f'{filename}: total {len(df)} items')
    return df[cols]

def sys_save_and_pickle(df, filename):
  try:
      df.to_pickle(f'{b3.data_path}/{filename}.zip')
      print('google upload fast debug')
    #   df = sys_upload_to_gcs(df, filename)
  except Exception as e:
      pass
  return df

# nsd_functions
def nsd_nsd_range(nsd, safety_factor=1.8):
  # start
  try:
    start = int(max(nsd['nsd'].astype(int))) + 1
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
  expected_nsd = int(avg_nsd_per_day * (days_gap + 1) * safety_factor)

  # end
  end = start + expected_nsd

  # range
  start = start
  end = start + expected_nsd 

  print(f'from {start} to {end}')

  return start, end

def nsd_nsd_dates(nsd, safety_factor=1.8):
  safety_factor = b3.safety_factor
  try:
    # find the gap in days from today to max 'envio' date
    last_date = nsd['envio'].max().date()
    today = datetime.datetime.now().date()
    days_gap = (today - last_date).days
    
    # find the maximum 'nsd' gap
    try:
        max_gap = int(((nsd['nsd'].astype(int).diff().max() + safety_factor) * 0.1))
    except Exception as e:
        max_gap = int(((1 + safety_factor) * 0.1))

    # group nsd by day
    nsd_per_day = nsd.groupby(nsd['envio'].dt.date)['nsd'].count()

    # find the average nsd items per day group, and other things
    avg_nsd_per_day = nsd_per_day.mean()
    max_nsd_per_day = nsd_per_day.max()
    max_date_nsd_per_day = nsd_per_day.idxmax()

    # last_date and previous safe date 
    back_days = round(max_gap / avg_nsd_per_day)
    limit_date = datetime.datetime.now().date() - datetime.timedelta(days=back_days)

  except Exception as e:
    last_date, limit_date, max_gap = pd.to_datetime('1970-01-02').date(), datetime.datetime.now().date(), b3.max_gap

  return last_date, limit_date, max_gap

def nsd_get_nsd(nsd):
  nsd_url = f'https://www.rad.cvm.gov.br/ENET/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento={nsd}&CodigoTipoInstituicao=1'
  # Getting the HTML content from the URL
  response = requests.get(nsd_url, headers=sys_header_random())
  html_content = response.text

  # Parsing the HTML content with BeautifulSoup
  soup = BeautifulSoup(html_content, 'html.parser')

  # Extracting company
  nomeCompanhia_tag = soup.find('span', {'id': 'lblNomeCompanhia'})
  company = nomeCompanhia_tag.text.strip()
  company = unidecode.unidecode(company).upper()
  company = sys_clean_text(company)
  company = sys_word_to_remove(company)
  
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

  data = [company, dri, dri2, dre, data, versao, auditor, auditor_rt, cancelamento, protocolo, envio, url, nsd]
  data = [sys_clean_text(item) if item not in [company, envio, url] else item for item in data]
      
  return data

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

def nsd_get_nsd_content():
    try:
        safety_factor = b3.safety_factor
        gap = 0

        filename = 'nsd_links'
        cols_nsd = ['company', 'dri', 'dri2', 'dre', 'data', 'versao', 'auditor', 'auditor_rt', 'cancelamento', 'protocolo', 'envio', 'url', 'nsd']

        nsd = sys_read_or_create_dataframe(filename, cols_nsd)
        if not nsd.empty:
            nsd['envio'] = pd.to_datetime(nsd['envio'], dayfirst=True)
            start, end = nsd_nsd_range(nsd, safety_factor)
        else:
            start, end = 1, 100

        start_time = time.time()
        for i, n in enumerate(range(start, end)):
            # interrupt conditions
            last_date, limit_date, max_gap = nsd_nsd_dates(nsd, safety_factor)
            if last_date > limit_date:
                if gap == max_gap:
                    break

            progress = sys_remaining_time(start_time, end-start, i)
            try:
                # add nsd row to dataframe
                row = nsd_get_nsd(n)
                nsd = pd.concat([nsd, pd.DataFrame([row], columns=cols_nsd)])
                print(n, progress, row[10], row[4], row[3], row[0])
                # reset gap
                gap = 0
            except Exception as e:
                # increase gap count
                gap += 1
                print(n, progress)

            # if n% b3.bin_size == 0:
            if (end-start - i - 1)% b3.bin_size == 0:
                nsd = sys_save_and_pickle(nsd, filename)
                print('partial save')

        nsd = sys_save_and_pickle(nsd, filename)
        # print('final save')
    except Exception as e:
        pass

    return nsd

def stk_get_acoes(driver, wait, url):
    try:
        select_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cmbGrupo']")))

        # Once the element is clickable, create a Select object and select the option
        select = Select(select_element)
        select.select_by_visible_text("Dados da Empresa")

        iframe_element = driver.find_element(By.ID, "iFrameFormulariosFilho")
        driver.switch_to.frame(iframe_element)
        table = driver.find_element(By.XPATH, "//*[@id='UltimaTabela']/table")

        # Read the table data into a Pandas DataFrame
        dados = pd.read_html(table.get_attribute('outerHTML'))[0]
        driver.switch_to.default_content()

        on = pd.to_numeric(dados.iloc[2, 1].replace('.', '').replace(',', ''))
        pn = pd.to_numeric(dados.iloc[3, 1].replace('.', '').replace(',', ''))
        on_tes = pd.to_numeric(dados.iloc[6, 1].replace('.', '').replace(',', ''))
        pn_tes = pd.to_numeric(dados.iloc[7, 1].replace('.', '').replace(',', ''))
        unidade = 'UNIDADE'
        match = re.search(r'\((.*?)\)', dados.iloc[0,0])
        if match:
            unidade = match.group(1).upper()
        
        acoes = [on, pn, on_tes, pn_tes, unidade, url]
    except Exception as e:
        acoes = [0, 0, 0, 0, 'UNIDADE', url]
        pass

    return acoes

def stk_synchronize_nsd_and_acoes(filtered_nsd, acoes):
    """
    Update and synchronize the nsd and acoes dataframes.

    This function processes the nsd dataframe to include only the rows with specific 'dre' types,
    indicating they are either quarterly reports or standardized financial statements.
    It then renames columns to match those in acoes, converts the 'nsd' column to integers, and
    sorts the data to put the most recent documents at the top. After filtering out duplicates,
    the function extracts the 'nsd' from the URL in the acoes dataframe and merges the two dataframes.
    It removes any rows in acoes that have an 'nsd' less than the maximum for their respective company
    and quarter. Finally, it filters out any URLs from filtered_nsd that are present in acoes,
    ensuring no overlap between the two dataframes in terms of URLs.

    Parameters:
    nsd (DataFrame): The nsd dataframe to be processed.
    acoes (DataFrame): The acoes dataframe to be updated based on nsd.

    Returns:
    DataFrame: The updated filtered_nsd dataframe with duplicates and outdated entries removed.
    DataFrame: The updated acoes dataframe with only the most recent entries for each company and quarter.
    """
    filtered_nsd = filtered_nsd.copy()
    
    # Renomear colunas para que 'company' se torne 'Companhia' e 'data' se torne 'Trimestre'.
    # Isso é necessário para que as colunas correspondam às de acoes, permitindo futuras comparações e combinações.
    filtered_nsd.rename(columns={'company': 'Companhia', 'data': 'Trimestre'}, inplace=True)

    # Extrair o número sequencial do documento (nsd) da URL no DataFrame acoes.
    # Isso é feito dividindo a URL em partes e pegando o número que aparece logo após 'Documento='.
    acoes['nsd'] = acoes['URL'].apply(lambda x: int(x.split('Documento=')[-1].split('&')[0]))

    # Converter a coluna 'Trimestre' em acoes para o tipo datetime, assim como fizemos com filtered_nsd.
    acoes['Trimestre'] = pd.to_datetime(acoes['Trimestre'], errors='coerce', format='%d%m%Y')

    # Agrupar filtered_nsd por Companhia e Trimestre e pegar o maior nsd para cada grupo.
    # Isso nos dá o documento mais recente para cada empresa e trimestre.
    nsd_max_filtered_nsd = filtered_nsd.groupby(['Companhia', 'Trimestre'])['nsd'].max().reset_index()

    # Fazer um merge (junção) entre acoes e nsd_max_filtered_nsd para combinar as linhas com base em Companhia e Trimestre.
    # Adicionamos um indicador para ver se a linha resultante é uma correspondência ('both') ou não ('left_only').
    # Isso ajuda a identificar quais linhas em acoes têm um documento correspondente em nsd que é o mais recente.

    acoes['Trimestre'] = pd.to_datetime(acoes['Trimestre'], errors='coerce')
    acoes['nsd'] = acoes['nsd'].astype(int)

    nsd_max_filtered_nsd['Trimestre'] = pd.to_datetime(nsd_max_filtered_nsd['Trimestre'], errors='coerce')
    nsd_max_filtered_nsd['nsd'] = nsd_max_filtered_nsd['nsd'].astype(int)

    acoes_updated = pd.merge(acoes, nsd_max_filtered_nsd, on=['Companhia', 'Trimestre', 'nsd'], how='left', indicator=True)

    # Realizar outra junção entre acoes e nsd_max_filtered_nsd para comparar os nsd.
    # Desta vez, a junção é feita para trazer o nsd máximo ao lado do nsd atual em acoes.
    acoes_updated = pd.merge(acoes, nsd_max_filtered_nsd, on=['Companhia', 'Trimestre'], how='left', suffixes=('', '_max'))

    # Remover as linhas de acoes onde o nsd é menor que o nsd máximo para a respectiva Companhia e Trimestre.
    # Isso efetivamente atualiza acoes para manter apenas as entradas mais recentes.
    acoes_most_recent = acoes_updated[acoes_updated['nsd'] >= acoes_updated['nsd_max']].drop(columns=['nsd_max'])

    # Obter uma lista de URLs presentes em acoes_most_recent para saber quais URLs devemos remover de filtered_nsd.
    urls_to_remove = acoes_most_recent['URL'].unique()

    # Filtrar filtered_nsd para remover as linhas cuja URL está na lista de urls_to_remove.
    # Isso assegura que não haja sobreposição entre acoes_most_recent e filtered_nsd em termos de URLs.
    filtered_nsd = filtered_nsd[~filtered_nsd['url'].isin(urls_to_remove)]

    # Revert the column names in filtered_nsd to their original state
    filtered_nsd = filtered_nsd.copy()
    filtered_nsd.rename(columns={'Companhia': 'company', 'Trimestre': 'data'}, inplace=True)
    
    # Drop the 'nsd' and 'nsd_max' columns from acoes_updated
    acoes_updated.drop(columns=['nsd', 'nsd_max'], inplace=True)
    
    return filtered_nsd, acoes_updated

def stk_stock_values_units(row):
    """
    Adjust the stock values in a DataFrame row based on the unit of measurement.

    If the unit is 'MIL', multiply the stock values (Ações ON, Ações PN, Ações ON em Tesouraria,
    Ações PN em Tesouraria) by 1000 to convert them to 'UNIDADE'. The 'Unidade' field is then 
    updated to 'UNIDADE'.

    Parameters:
    row (pd.Series): A row of a DataFrame that contains stock values and a unit field.

    Returns:
    pd.Series: The adjusted row with updated stock values if the unit was 'MIL'.
    """
    # Verifica se a unidade é 'MIL' e faz os ajustes necessários
    if row['Unidade'] == 'MIL':
        # Multiplica os valores de ações por 1000
        row['Ações ON'] *= 1000
        row['Ações PN'] *= 1000
        row['Ações ON em Tesouraria'] *= 1000
        row['Ações PN em Tesouraria'] *= 1000
        # Atualiza a unidade para 'UNIDADE'
        row['Unidade'] = 'UNIDADE'

    return row

def stk_stock_values_magnitude_values(data_series):
    """
    Ajusta os valores de uma série temporal para garantir que a ordem de magnitude seja consistente.

    Esta função percorre os valores da série temporal e compara a ordem de magnitude de cada 
    valor com o valor anterior. Se a diferença entre as ordens de magnitude for exatamente 3,
    o valor atual será ajustado (multiplicado por 1000) até que as ordens de magnitude sejam iguais.

    Args:
    data_series (array-like): Uma série temporal de valores numéricos.

    Returns:
    array-like: A série temporal com os valores ajustados.
    """

    # Ajustando os valores na série temporal
    for i in range(1, len(data_series)):
        value_1 = data_series[i - 1]
        value_2 = data_series[i]

        # Evitando logaritmo de zero
        if value_1 == 0 or value_2 == 0:
            continue

        # Calculando a ordem de magnitude de cada valor
        magnitude_1 = int(math.floor(math.log10(abs(value_1))))
        magnitude_2 = int(math.floor(math.log10(abs(value_2))))

        # Ajustando value_2 se a diferença de ordem de magnitude for igual a 3
        while magnitude_1 - magnitude_2 == 3:
            value_2 *= 1000
            magnitude_2 = int(math.floor(math.log10(abs(value_2))))

        # Atualizando o valor na série
        data_series[i] = value_2

    return data_series

def stk_fix_stock_values(acoes):
    """
    Ajusta os valores de estoque e unidades para cada companhia no DataFrame 'acoes'.

    Primeiro, o DataFrame é ordenado por companhia e trimestre. Em seguida, para cada companhia,
    são feitos ajustes nas unidades de estoque e na magnitude dos valores das ações.
    Os ajustes são realizados para as colunas 'Ações ON' e 'Ações PN'.

    Args:
    acoes (pd.DataFrame): DataFrame contendo os dados das ações das companhias.

    Returns:
    pd.DataFrame: DataFrame com os valores ajustados.
    """

    # Ordenando o DataFrame por companhia e trimestre
    acoes = acoes.sort_values(by=['Companhia', 'Trimestre'], ascending=[True, True])

    # Iterando sobre cada companhia única no DataFrame 'acoes'
    for company in acoes['Companhia'].unique():
        # Filtrando os dados da companhia atual
        mask = acoes['Companhia'] == company
        df = acoes[mask].copy()

        # Aplicando ajustes de unidade de estoque
        df = df.apply(stk_stock_values_units, axis=1)
        df['Unidade'] = 'UNIDADE'  # Atualizando a unidade para 'UNIDADE'

        # Ajustando a magnitude dos valores de ações
        for col in ['Ações ON', 'Ações PN']:
            data_series = df[col].to_numpy()  # Convertendo a coluna em um array NumPy
            df[col] = stk_stock_values_magnitude_values(data_series)  # Ajustando a magnitude

        # Atualizando o DataFrame original 'acoes' com os valores ajustados
        for col in ['Ações ON', 'Ações PN', 'Unidade']:
            acoes.loc[df.index, col] = df[col]

    return acoes

def stk_get_composicao_acionaria():
    """
    Obtém e processa a composição acionária de várias empresas a partir de fontes de dados.

    Esta função carrega dados de duas fontes (nsd e acoes), filtra e sincroniza esses dados
    com base em critérios específicos. Em seguida, navega em URLs específicas para coletar 
    informações acionárias adicionais. Finalmente, salva os resultados processados.

    Returns:
    pd.DataFrame: DataFrame atualizado com informações acionárias de várias empresas.
    """
    try:
        # Carregar DataFrames nsd e acoes
        nsd = nsd_get_nsd_content()

        filename = 'acoes'
        columns = ['Companhia', 'Trimestre', 'Ações ON', 'Ações PN', 'Ações ON em Tesouraria', 'Ações PN em Tesouraria', 'Unidade', 'URL']
        acoes = sys_read_or_create_dataframe(filename, columns)

        # Filtrar nsd para relatórios trimestrais ou demonstrações financeiras padronizadas
        selected_dre = ['INFORMACOES TRIMESTRAIS', 'DEMONSTRACOES FINANCEIRAS PADRONIZADAS']
        filtered_nsd = nsd[nsd['dre'].isin(selected_dre)].copy()

        # Processar filtered_nsd para converter tipos de dados e remover duplicatas
        filtered_nsd['nsd'] = filtered_nsd['nsd'].astype(int)
        filtered_nsd.sort_values(by='nsd', ascending=True, inplace=True)
        filtered_nsd['data'] = pd.to_datetime(filtered_nsd['data'], errors='coerce', format='%d%m%Y')
        filtered_nsd.drop_duplicates(subset=['company', 'data'], keep='last', inplace=True)

        # Sincronizar filtered_nsd e acoes
        if len(acoes) > 0:
            filtered_nsd, acoes = stk_synchronize_nsd_and_acoes(filtered_nsd, acoes)

        # Ordenar filtered_nsd
        filtered_nsd.sort_values(by=['company', 'data'], ascending=[True, True], inplace=True)

        # Iniciar o processo de coleta de dados da web
        driver, wait = sys_load_browser()

        # Processar cada linha em filtered_nsd para coletar dados acionários
        start_time = time.time()
        on_old = -1  # Para verificar variabilidade
        company_old = -1  # Para verificar variabilidade

        # Iterando sobre cada linha do DataFrame 'filtered_nsd'
        for j, (i, row) in enumerate(filtered_nsd.iterrows()):
            # Extraindo informações da linha atual
            company = row['company']
            data = row['data']
            url = row['url']
        
            # Acessando a URL para coletar dados acionários
            driver.get(url)

            # Coletando dados de ações da companhia na URL e concatenando com informações existentes
            data = [company, data] + stk_get_acoes(driver, wait, url)

            # Verificando se há uma mudança nas ações ON desde a última iteração para a mesma companhia
            if data[2] != on_old and on_old >= 0 and company == company_old:
                # Marcando a linha para atenção caso haja uma mudança significativa
                data[6] = data[6] + ' ATTENTION PLEASE'

            # Atualizando as variáveis de controle para a próxima iteração
            on_old = data[2]
            company_old = data[0]

            # Adicionando os dados coletados ao DataFrame 'acoes'
            acoes = pd.concat([acoes, pd.DataFrame([data], columns=columns)], ignore_index=True)
        
            # Exibindo o tempo restante estimado para o processo
            print(sys_remaining_time(start_time, len(filtered_nsd), j), i, data[0], data[1], data[2], data[3], data[4], data[5])

            # Salvando parcialmente os dados a cada 'b3.bin_size' iterações
            if (len(filtered_nsd) - j - 1) % b3.bin_size == 0:
                acoes = sys_save_and_pickle(acoes, filename)
                print('partial save')

        # Finalizar o navegador
        driver.quit() 

        # Remove linhas duplicadas no DataFrame 'acoes'
        acoes = acoes.drop_duplicates()  

        # Aplica funções de ajuste aos valores de estoque e unidades
        acoes = stk_fix_stock_values(acoes)  

        # Salva o DataFrame 'acoes' em um arquivo (como um pickle) para uso futuro
        acoes = sys_save_and_pickle(acoes, filename)  

        print('final save')

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    return acoes

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
    nsd = sys_read_or_create_dataframe(filename, b3.cols_nsd)
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
    # time.sleep(1)

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

def do_the_math(dre_raw, dre_math):
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
      if l% (b3.bin_size*10) == 0:
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
        item = [sys_clean_text(word) for word in item]
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
                startswith_mask = (df[line].apply(lambda word: sys_clean_text(word)).str[:len(item)] == item).replace({np.nan: False})

            # startswith_not
            if startswith_not != '':
                item = item_to_list(startswith_not)
                item = item.split('|')[0]
                startswith_not_mask = ~(df[line].apply(lambda word: sys_clean_text(word)).str[:len(item)] == item).replace({np.nan: False})

            # endswith
            if endswith != '':
                item = item_to_list(endswith)
                item = item.split('|')[0]
                endswith_mask = (df[line].apply(lambda word: sys_clean_text(word)).str[-len(item):] == item).replace({np.nan: False})

            # endswith_not
            if endswith_not != '':
                item = item_to_list(endswith_not)
                item = item.split('|')[0]
                endswith_not_mask = ~(df[line].apply(lambda word: sys_clean_text(word)).str[-len(item):] == item).replace({np.nan: False})

            # contains
            if contains != '':
                item = item_to_list(contains)
                contains_mask = df[line].apply(lambda word: sys_clean_text(word)).str.contains(item, case=False).replace({np.nan: False})

            # contains_not
            if contains_not != '':
                item = item_to_list(contains_not)
                contains_not_mask = ~df[line].apply(lambda word: sys_clean_text(word)).str.contains(item, case=False).replace({np.nan: False})

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
            mask &= (df[line].apply(lambda word: sys_clean_text(word)).str[:len(value)] == value).replace({np.nan: False})
        elif operation == "startswith_not":
            mask &= (df[line].apply(lambda word: sys_clean_text(word)).str[:len(value)] != value).replace({np.nan: False})
        elif operation == "endswith":
            mask &= (df[line].apply(lambda word: sys_clean_text(word)).str[-len(value):] == value).replace({np.nan: False})
        elif operation == "endswith_not":
            mask &= (df[line].apply(lambda word: sys_clean_text(word)).str[-len(value):] != value).replace({np.nan: False})
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
  # legacy??
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
    new_lines.append(fundamentaline(line=line.copy(), title='16.03 - Margem EBITDA (EBITDA por Resultado Bruto (Receita Líquida)))', valor=eval_formula(md, "division(ebitda,md['_0303_resultado_bruto_receita_liquida'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='16.03.01 - Margem EBIT (EBIT por Resultado Bruto (Receita Líquida)))', valor=eval_formula(md, "division(md['_0305_lajir_ebit_resultado_antes_do_resultado_financeiro_e_dos_tributos'],md['_0303_resultado_bruto_receita_liquida'])")))
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
    new_lines.append(fundamentaline(line=line.copy(), title='18.11.02 - Taxa de Juros Pagos (Remuneração de Capital de Terceiros por Receita Bruta)', valor=eval_formula(md, "division(md['_070803_remuneracao_de_capital_de_terceiros'],md['_0301_receita_bruta'])")))
    new_lines.append(fundamentaline(line=line.copy(), title='18.11.03 - Taxa de Proventos Gerados (Remuneração de Capital Próprio por Receita Bruta)', valor=eval_formula(md, "division(md['_070804_remuneracao_de_capital_proprio'],md['_0301_receita_bruta'])")))
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
          key = sys_clean_text(row['Conta'] + ' - ' + row['Descrição']).split('  ')
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
def sys_upload_to_gcs(df, df_name):
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
      blob.upload__local(buffer, content_type='application/zip')
    except Exception as e:
      # print(e)
      pass
    return df

def sys_download_from_gcs(df_name):
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
      response = requests.get(url, headers=sys_header_random())

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

def sys_save_pkl(data, filename):
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
    #     with zipf.open(f'{filename}.pkl', 'w') as datafile:
    #         pickle.dump(data, datafile)

    return data

def sys_load_pkl(filename):
    """Loads data from a pickle file.

    Args:
        filename (str): The name of the pickle file (excluding the '.pkl' extension).

    Returns:
        The loaded data.
    """
    with open(f'{filename}.pkl', 'rb') as f:
        data = pickle.load(f)
    # with zipfile.ZipFile(f'{filename}.zip', 'r') as zipf:
    #     with zipf.open(f'{filename}.pkl', 'r') as datafile:
    #         data = pickle.load(datafile)

    return data

def create_demofile():
    """Creates a demo dictionary by loading pickled dataframes for each year.

    Args:
        start_year (int): The starting year for loading dataframes.

    Returns:
        dict: A dictionary containing loaded demo dataframes for each year.
    """
    try:
        cvm_web = {}
        years = range(b3.start_year, datetime.datetime.now().year + 1)
        start_time = time.time()

        for i, year in enumerate(years):
            print(sys_remaining_time(start_time, len(years), i))
            dataframe = sys_load_pkl(f'{b3.app_folder}/dataframe_{year}')
            cvm_web[year] = dataframe
    except Exception as e:
        # print(e)
        pass
    return cvm_web

def sys_gather_links(url):
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
        sys_gather_links(full_link)
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

def cvm_get_metadados(filelist):
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
    metafiles = [filelink for filelink in filelist if "meta" in filelink]

    for file in metafiles:
        response = b3.session.get(file)
        response.raise_for_status()

        if file.endswith('.zip'):
            zipfile = zipfile.ZipFile(io.BytesIO(response.content))

            for filein_zip in zipfile.namelist():
                with zipfile.open(filein_zip) as zipfilecontent:
                    filecontent = zipfilecontent.read().decode('utf-8', errors='ignore')
                    d = extract_meta(filecontent)
                    meta_dict[filein_zip.split('.')[0]] = d
        elif file.endswith('.txt'):
            filecontent = response.content.decode('iso-8859-1')
            d = extract_meta(filecontent)
            filename = file.split('/')[-1].split('.')[0]
            meta_dict[filename] = d

    return meta_dict

def cvm_get_categories(filelist):
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
    # metafiles = [filelink for filelink in filelist if "meta" in filelink]
    # files = [filelink for filelink in filelist if "meta" not in filelink]

    for filelink in filelist:
        cat = '/'.join(filelink.replace(b3.base_cvm,'').split('/')[:-2])
        categories.add(cat)
    categories = sorted(list(categories))

    return categories

def cvm_get_database_filelist_links():
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
    url = b3.base_cvm
    print(f'... connecting to web "{url}"')
    print(f'    to get list of available files for download')
    filelist = sys_gather_links(url)
    folders = set()

    # Extract folder URLs from file links
    for url in filelist:
        folder_url = '/'.join(url.split('/')[:-1])
        folders.add(folder_url)

    fileinfo_df = []
    start_time = time.time()
    # Loop through folder URLs and extract file information
    for i, url in enumerate(folders):
        print(sys_remaining_time(start_time, len(folders), i))
        response = requests.get(url, headers=sys_header_random())
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

def cvm_download_csv_files_from_cvm_web(filelist_df, types=['itr', 'dfp']):
    """
    Downloads and processes database files based on specified DEMONSTRATIVO values.

    This function takes a list of DEMONSTRATIVO values and a DataFrame containing file information.
    It downloads and processes database files associated with the specified DEMONSTRATIVO values.
    The downloaded CSV files are extracted, metadata is extracted from filenames, and data is loaded
    into pandas DataFrames with added metadata columns.

    Args:
        cvm_webs (list): A list of DEMONSTRATIVO values to filter files.
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
    for i, demonstrativo in enumerate(types):
        # Retrieve the list of files based on the specified 'DEMONSTRATIVO'
        download_files = [filelink for filelink in filelist if 'meta' not in filelink and demonstrativo in filelink]

        # Iterate through the list of URLs
        start_time_2 = time.time()
        for j, zip_url in enumerate(download_files):
            response = requests.get(zip_url, headers=sys_header_random())

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

                        print('  ' + '  ' + sys_remaining_time(start_time_3, len(zip_ref.infolist()), k), fileinfo.filename.lower())
            print('  ' + sys_remaining_time(start_time_2, len(download_files), j))
        print(sys_remaining_time(start_time, len(types), i))
    print(f'Total {len(dataframes)} databases found and {total_rows} lines downloaded')
    return dataframes

def sys_word_to_remove(text):
    """
    Removes specified words from a text content.

    This function takes a text content (string) and removes specified words from it.
    The words to remove are defined in the 'words_to_remove' list.

    Args:
        text (str): The content of the text to be cleaned.

    Returns:
        str: The cleaned text content without the specified words.
    """
    pattern = '|'.join(map(re.escape, b3.words_to_remove))
    text = re.sub(pattern, '', text)
    return text

def sys_adjust_vl_conta(row):
    if row['ESCALA_MOEDA'] == 'MIL':
        row['VL_CONTA'] = row['VL_CONTA'] * 1000
        row['ESCALA_MOEDA'] = 'UNIDADE'

    return row

def cvm_group_dataframes_by_year_yearly(df_list):
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
        print(year, sys_remaining_time(start_time, len(df_list), i))

        # Check if the year is already a key in the dictionary, if not, create a list for it
        if year not in df_y:
            df_y[year] = []
        
        # Append the DataFrame to the list for the respective year
        df_y[year].append(df)

    print('... concatenating')
    start_time = time.time()

    # Concatenate DataFrames within each year's list
    for i, (year, df_list) in enumerate(df_y.items()):
        print(year, sys_remaining_time(start_time, len(df_y), i))
        df_y[year] = pd.concat(df_list, ignore_index=True)

    return df_y

def sys_multiprocessing(func, df):
    n_cores = multiprocessing.cpu_count()
    df_split = np.array_split(df, n_cores)
    with multiprocessing.Pool(n_cores) as pool:
        df = pd.concat(pool.map(func, df_split))
    return df

def cvm_clean_dataframe_parallel(df):
    df['DENOM_CIA'] = df['DENOM_CIA'].apply(sys_clean_text)
    df['DENOM_CIA'] = df['DENOM_CIA'].apply(sys_word_to_remove)
    return df

def parallel_process_dfs(func, list_of_dfs, df_web, df_columns):
    n_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(n_cores)

    # Prepare arguments for each function call including the year
    func_args = [(df, df_web, df_columns, year) for year, df in list_of_dfs.items()]

    # Process each DataFrame in parallel and collect results
    processed_dfs = pool.starmap(func, func_args)

    pool.close()
    pool.join()

    # Convert list of tuples (year, DataFrame) back into a dictionary
    return {year: df for year, df in processed_dfs}

def cvm_clean_dataframe(dict_of_df):
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
    # Change data types for columns
    category_columns = ['FILENAME', 'DEMONSTRATIVO', 'BALANCE_SHEET', 'ANO', 'AGRUPAMENTO', 'CNPJ_CIA', 'VERSAO', 'DENOM_CIA', 'CD_CVM', 'GRUPO_DFP', 'MOEDA', 'ESCALA_MOEDA', 'CD_CONTA', 'DS_CONTA','ST_CONTA_FIXA', 'COLUNA_DF', ]
    datetime_columns = ['DT_REFER', 'DT_FIM_EXERC', 'DT_INI_EXERC', ]
    numeric_columns = ['VL_CONTA', ]

    print('... cleaning database')
    start_time = time.time()
    for i, (year, df) in enumerate(dict_of_df.items()):
        
        # Remove extra rows based on specific conditions
        try:
            df = df[df['ORDEM_EXERC'] == 'ÚLTIMO']
            df = df.drop(columns=['ORDEM_EXERC'])
        except Exception as e:
            # print(e)
            pass
        
        # Convert specified columns to specified formats
        for col in category_columns:
            try:
                df[col] = df[col].astype('category')
            except Exception as e:
                pass
        for col in datetime_columns:
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception as e:
                pass
        for col in numeric_columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except Exception as e:
                pass

        # Filter unnecessary lines
        df = df[df['DT_INI_EXERC'] == df['DT_INI_EXERC'].min()]

        # Vectorized adjustment of VL_CONTA according to ESCALA_MOEDA
        mask = df['ESCALA_MOEDA'] == 'MIL'
        df.loc[mask, 'VL_CONTA'] *= 1000
        df.loc[mask, 'ESCALA_MOEDA'] = 'UNIDADE'

        df = sys_multiprocessing(cvm_clean_dataframe_parallel, df)

        dict_of_df[year] = df

        print(year, sys_remaining_time(start_time, len(dict_of_df), i))
    return dict_of_df

def cvm_group_dataframes_by_year(dataframes):
    cvm_web = [df for df in dataframes if len(df) > 0 and ('con' in df['FILENAME'][0] or 'ind' in df['FILENAME'][0])]
    links = [df for df in dataframes if len(df) > 0 and ('con' not in df['FILENAME'][0] and 'ind' not in df['FILENAME'][0])]

    print('... split by year')
    cvm_web = cvm_group_dataframes_by_year_yearly(cvm_web)
    links = cvm_group_dataframes_by_year_yearly(links)

    # Rename column for consistency
    for year in links.keys():
        links[year].rename(columns={'VERSAO': 'VERSAO_LINK'}, inplace=True)

    return cvm_web, links

def cvm_get_database_filelist():
    """
    Update the cvm_web files based on new data from filelist_df.

    This function updates the cvm_web files by downloading new data based on filelist_df.
    It follows several steps to achieve this and also extracts metadata and categories.

    Args:
    None

    Returns:
    dict: Updated cvm_web data.
    dict: Metadata information.
    list: List of demonstrativos_cvm.

    """
    # Retrieve DataFrame containing file links from base_cvm URL
    filelist_df = cvm_get_database_filelist_links()
    filelist_df = sys_save_pkl(filelist_df, f'{b3.app_folder}/temp_filelist_df')
    # print('fast debug filelist_df')
    # filelist_df = sys_load_pkl(f'{b3.app_folder}/temp_filelist_df')
    
    # Find the maximum date in the filelist_df
    last_update2 = filelist_df['date'].max().strftime('%Y-%m-%d')

    try:
        # Read last update date from 'last_update.txt' if available, else set to '1970-01-01'
        with open(f'{b3.app_folder}/last_update.txt', 'r') as f:
            last_update = f.read().strip()
        if not last_update:
            last_update = '1970-01-01'
    except Exception as e:
        last_update = '1970-01-01'

    # Filter filelist_df to include only files with dates greater than last_update
    filelist_df = filelist_df[filelist_df['date'] > (pd.to_datetime(last_update) + pd.DateOffset(days=0))]
    print(f'{len(filelist_df)} new files to download')

    return filelist_df, last_update2

def cvm_get_web_database():
    try:
        filelist_df, last_update = cvm_get_database_filelist()

        dataframes = cvm_download_csv_files_from_cvm_web(filelist_df)
        dataframes = sys_save_pkl(dataframes, f'{b3.app_folder}/temp_' + 'dataframes')
        # print('fast debug dataframes')
        # dataframes = sys_load_pkl(f'{b3.app_folder}/temp_' + 'dataframes')

        cvm_web, links = cvm_group_dataframes_by_year(dataframes)
        cvm_web = sys_save_pkl(cvm_web, f'{b3.app_folder}/temp_' + 'dataframes_by_year')
        # print('fast debug dataframes by year')
        # cvm_web = sys_load_pkl(f'{b3.app_folder}/temp_' + 'dataframes_by_year')

        # print('fast debug dataframessss')
        # cvm_web = {k: v for k, v in cvm_web.items() if k == 2020}
        # cvm_web = sys_load_pkl(f'{b3.app_folder}/temp_' + 'cvm_web')

        links = sys_save_pkl(links, f'{b3.app_folder}/temp_' + 'links')
        # print('fast debug links')
        # links = sys_load_pkl(f'{b3.app_folder}/temp_' + 'links')

        cvm_web = cvm_clean_dataframe(cvm_web)
        cvm_web = sys_save_pkl(cvm_web, f'{b3.app_folder}/temp_' + 'cvm_web_clean')
        # print('fast debug cvm_web cvm_web_cleaned')
        # cvm_web = sys_load_pkl(f'{b3.app_folder}/temp_' + 'cvm_web_clean')

        # Save cvm_web as local cvm
        # if len(cvm_web) > 0:
        #     cvm_web = sys_save_pkl(cvm_web, f'{b3.app_folder}/cvm_web')
        # print('fast debug cvm_web save local')

        # Get metadata and categories from filelist
        try:
            meta_dict = cvm_get_metadados(filelist_df['filename'].to_list())
            categories = cvm_get_categories(filelist_df['filename'].to_list())
            demonstrativos_cvm = []
            for cat in categories:
                term = 'DOC/'
                if term in cat:
                    demonstrativos_cvm.append(str(cat).replace(term,'').lower())
        except Exception as e:
            pass

        try:
            # Write the maximum date from filtered filelist_df to 'last_update.txt'
            print('last update', last_update)
            with open(f'{b3.app_folder}/last_update.txt', 'w') as f:
                f.write(last_update)
        except Exception as e:
            pass

        # Print results
        try:
            total_fields = sum((i + 1) * len(d) for i, d in enumerate(meta_dict.values()))
            print(f'{b3.base_cvm}')
            print(f'Encontradas {len(categories)} categorias com {len(meta_dict)} arquivos meta contendo {total_fields} campos')
            if demonstrativos_cvm:
                print(demonstrativos_cvm)
        except Exception as e:
            pass
    except Exception as e:
        pass
    return cvm_web

def adjust_quarters(group_df):
    """
    Adjust the 'VL_CONTA' values for each quarter by subtracting the previous quarter's value.
    
    Args:
    - group_df (pd.DataFrame): A DataFrame containing quarterly data for a specific group.

    Returns:
    - pd.DataFrame: The same DataFrame with adjusted 'VL_CONTA' values.
    """
    
    # Extract the VL_CONTA values for each quarter. If a value is not present for a quarter, default to 0.
    # This ensures that the adjustments are based on the correct values even if data for a particular quarter is missing.
    q1_value = group_df.loc[group_df['DT_REFER'].dt.quarter == 1, 'VL_CONTA'].values[0] if not group_df.loc[group_df['DT_REFER'].dt.quarter == 1, 'VL_CONTA'].empty else 0
    q2_value = group_df.loc[group_df['DT_REFER'].dt.quarter == 2, 'VL_CONTA'].values[0] if not group_df.loc[group_df['DT_REFER'].dt.quarter == 2, 'VL_CONTA'].empty else 0
    q3_value = group_df.loc[group_df['DT_REFER'].dt.quarter == 3, 'VL_CONTA'].values[0] if not group_df.loc[group_df['DT_REFER'].dt.quarter == 3, 'VL_CONTA'].empty else 0
    q4_value = group_df.loc[group_df['DT_REFER'].dt.quarter == 4, 'VL_CONTA'].values[0] if not group_df.loc[group_df['DT_REFER'].dt.quarter == 4, 'VL_CONTA'].empty else 0
    
    # Calculate adjustments based on the difference between quarters.
    q4_adj = q4_value - q3_value
    q3_adj = q3_value - q2_value
    q2_adj = q2_value - q1_value

    # Apply the calculated adjustments to the DataFrame.
    group_df.loc[group_df['DT_REFER'].dt.quarter == 4, 'VL_CONTA'] = q4_adj
    group_df.loc[group_df['DT_REFER'].dt.quarter == 3, 'VL_CONTA'] = q3_adj
    group_df.loc[group_df['DT_REFER'].dt.quarter == 2, 'VL_CONTA'] = q2_adj

    return group_df

def filter_last_quarter(group_df):
    """
    Filter out rows for the second and third quarters unless the 'DT_REFER' quarter matches the 'DT_INI_EXERC' quarter.
    
    Args:
    - group_df (pd.DataFrame): A DataFrame containing quarterly data for a specific group.

    Returns:
    - pd.DataFrame: A filtered DataFrame.
    """
    
    # Create a mask to identify rows where the DT_REFER quarter is 2 or 3, but doesn't match the DT_INI_EXERC quarter.
    mask = ~group_df['DT_REFER'].dt.quarter.isin([2, 3]) | (group_df['DT_REFER'].dt.quarter == group_df['DT_INI_EXERC'].dt.quarter)
    group_df = group_df[mask]
    return group_df

def adjust_last_quarter(group_df):
    """
    For the last quarter (Q4), adjust the 'VL_CONTA' value by subtracting the sum of the values from the first three quarters.
    
    Args:
    - group_df (pd.DataFrame): A DataFrame containing quarterly data for a specific group.

    Returns:
    - pd.DataFrame: The DataFrame with adjusted 'VL_CONTA' values for Q4.
    """
    
    # Extract the 'VL_CONTA' values for the first three quarters.
    q1_value = group_df.loc[group_df['DT_REFER'].dt.quarter == 1]['VL_CONTA'].values[0] if not group_df.loc[group_df['DT_REFER'].dt.quarter == 1, 'VL_CONTA'].empty else 0
    q2_value = group_df.loc[group_df['DT_REFER'].dt.quarter == 2]['VL_CONTA'].values[0] if not group_df.loc[group_df['DT_REFER'].dt.quarter == 2, 'VL_CONTA'].empty else 0
    q3_value = group_df.loc[group_df['DT_REFER'].dt.quarter == 3]['VL_CONTA'].values[0] if not group_df.loc[group_df['DT_REFER'].dt.quarter == 3, 'VL_CONTA'].empty else 0

    # Adjust the Q4 value by subtracting the sum of Q1, Q2, and Q3 values.
    mask = group_df['DT_REFER'].dt.quarter == 4
    group_df.loc[mask, 'VL_CONTA'] -= (q1_value + q2_value + q3_value)

    return group_df

def cvm_math_calculations_adjustments(group):
    """
    Apply the appropriate adjustment logic based on the 'BALANCE_SHEET' value of the group.
    
    Args:
    - group (pd.DataFrame): A DataFrame containing data for a specific group.

    Returns:
    - pd.DataFrame: The adjusted DataFrame.
    """
    # Lists defining the types of balance sheets:

    # 'patrimonial' refers to balance sheets that detail a company's assets and liabilities.
    # 'BPA' stands for "Balance Sheet - Active" and represents the company's assets.
    # 'BPP' stands for "Balance Sheet - Passive" and represents the company's liabilities.
    patrimonial = ['BPA', 'BPP']

    # 'resultados' refers to balance sheets that detail a company's revenues and expenses over a specific period.
    # 'DRA' stands for "Statement of Revenue - Accumulated" and represents the accumulated revenues over a year.
    # 'DRE' stands for "Statement of Revenue - Exercise" and represents the revenues for a specific financial exercise.
    resultados = ['DRA', 'DRE']

    # 'fluxo_de_caixa' refers to cash flow statements detailing the inflows and outflows of cash.
    # 'DFC_MI' represents the "Direct Method of Cash Flow - Individual".
    # 'DFC_MD' represents the "Direct Method of Cash Flow - Consolidated".
    # 'DVA' stands for "Added Value Statement".
    # 'DMPL' stands for "Statement of Changes in Equity".
    fluxo_de_caixa = ['DFC_MI', 'DFC_MD', 'DVA']

    # other stuff
    other = ['DMPL']

    sheet = group['BALANCE_SHEET'].iloc[0]
    
    # If the group's 'BALANCE_SHEET' value belongs to the fluxo_de_caixa category, apply quarter adjustments.
    if sheet in fluxo_de_caixa:
        return adjust_quarters(group)
    # If the group's 'BALANCE_SHEET' value belongs to the resultados category, filter and adjust the last quarter.
    elif sheet in resultados:
        group = filter_last_quarter(group)
        return adjust_last_quarter(group)
    # If the group's 'BALANCE_SHEET' value doesn't match the above categories, return the original group without adjustments.
    else:
        return group

def cvm_extract_updated_rows(df_local, df_web, df_columns, year):

    # Define the list of columns that should not be included as key columns for merging.
    compare_columns = ['VL_CONTA']

    # Generate the list of key columns for merging by excluding the columns listed in no_columns.
    key_columns = [col for col in df_columns if col not in compare_columns]

    # updated values
    # Merge the local and web DataFrames based on the key columns, and an indicator column 
    df_updated_values = pd.merge(df_local, df_web, on=key_columns, how='outer', suffixes=('_local', '_web'), indicator=True)

    existing_lines = df_updated_values['_merge'] == 'left_only'  # Rows that exist only in the local DataFrame.
    new_lines = df_updated_values['_merge'] == 'right_only'  # Rows that exist only in the web DataFrame.
    updated_lines = (df_updated_values['_merge'] == 'both') & (df_updated_values['VL_CONTA_local'] != df_updated_values['VL_CONTA_web'])  # Rows that exist in both but have different 'VL_CONTA' values.

    # Define conditions to determine which values to keep in the merged DataFrame.
    conditions = [
        existing_lines, 
        new_lines, 
        updated_lines, 
    ]

    # Define the choices corresponding to each condition.
    choices = [
        df_updated_values['VL_CONTA_local'],  # existing_lines = Keep the local value for 'VL_CONTA' if the row is from local only.
        df_updated_values['VL_CONTA_web'],    # new_lines = Keep the web value for 'VL_CONTA' if the row is from web only.
        df_updated_values['VL_CONTA_web']     # updated_lines = Keep the web value for 'VL_CONTA' if the values differ between local and web.
    ]

    # Apply the conditions to create a new 'VL_CONTA' column in the merged DataFrame.
    df_updated_values['VL_CONTA'] = np.select(conditions, choices, default=df_updated_values['VL_CONTA_web'])

    # updated rows (rows with updated values)
    # Create a mask to identify rows that have been updated or are new from the web DataFrame.
    updated_rows_mask = (new_lines | updated_lines)

    # Use the mask to filter the merged DataFrame to only include updated or new rows.
    df_updated_rows = df_updated_values[updated_rows_mask]

    # updated_quarters
    # Define the columns to be used for the final filtering.
    quarter_col = ['']
    unique_sheet_cols = ['CNPJ_CIA', 'AGRUPAMENTO', 'CD_CONTA', 'DS_CONTA', 'COLUNA_DF']

    filter_cols = [col for col in unique_sheet_cols if col not in quarter_col]
    df_updated_rows[filter_cols]

    # Perform an inner merge to filter the original merged DataFrame using the updated rows 
    # and keep only the rows with matching values in the specified filter columns.
    df_updated_quarters = pd.merge(
        df_updated_rows[filter_cols].drop_duplicates(),  # Only the columns to match from the updated rows.
        df_updated_values,  # The original merged DataFrame - the updated complete df
        on=filter_cols,  # Columns to match on 
        how='inner'  # Keep only matches found in both DataFrames.
    )
    df_updated_quarters = df_updated_quarters.sort_values(by=['CNPJ_CIA', 'AGRUPAMENTO', 'CD_CONTA', 'DS_CONTA', 'COLUNA_DF', 'DT_REFER', ])[df_columns]
    

    # Display the number of updated rows.
    print(f'{year} {len(df_updated_rows)}/{len(df_updated_values)} linhas foram atualizadas')

    return df_updated_quarters

def cvm_updated_rows(cvm_local, cvm_web):
    """
    Merge two dictionaries of dataframes and extract updated rows.

    The function performs an outer merge on two dictionaries of dataframes, `cvm_local` (existing data) 
    and `cvm_web` (new data). The purpose is to update old financial data with new financial data and 
    to identify rows which have been updated for future mathematical transformations.

    Parameters:
    - cvm_local (dict): Dictionary with years as keys and existing financial data as values (pandas DataFrames).
    - cvm_web (dict): Dictionary with years as keys and new financial data as values (pandas DataFrames).

    Returns:
    - tuple: Two dictionaries of dataframes - the first contains the merged data, and the second contains the updated rows.

    """
    
    # Yearly updated data.
    cvm_updated = {}
    # Compile a list of years present in either local or web data.
    years = sorted(set(cvm_local.keys()).union(cvm_web.keys()))

    # Get column names from the earliest year's data.
    df_columns = (
        cvm_local.get(min(years), pd.DataFrame()).columns
        if min(years) in cvm_local
        else cvm_web[min(years)].columns
    )

    # Process each year's data.
    for year in years:
        # Obtain local and web data for the year.
        df_local = cvm_local.get(year, pd.DataFrame(columns=df_columns))
        df_web = cvm_web.get(year, pd.DataFrame(columns=df_columns))

        # Update rows by comparing local and web data.
        cvm_updated[year] = cvm_extract_updated_rows(df_local, df_web, df_columns, year)
        sys_beep()
    return cvm_updated

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
    try:
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
    except Exception as e:
        companies_by_str_port = {('ind', 'con'): 0, 'con': 0, 'ind': 0}

    return companies_by_str_port

def cvm_wrapper_apply(group, pbar):
    """Wrapper function for applying adjustments and updating the progress bar."""
    result = cvm_math_calculations_adjustments(group)
    pbar.update(1)  # Update the progress bar by one step
    # sys_beep()
    return result

def cvm_calculate_math(cvm, where):
    """
    Apply adjustments to dataframes for each year in the cvm dict.

    Parameters:
    - cvm (dict): Dictionary with years as keys and financial dataframes as values.

    Returns:
    - dict: Dictionary with years as keys and adjusted dataframes as values.
    """
    # Initialize a dictionary to store the calculated dataframes for each year
    math = {}

    # Loop through each year in the cvm dictionary
    for year, df_merged in cvm.items():
        try:
            math[year] = sys_load_pkl(f'{b3.app_folder}/temp_math_{where}_{year}')
        except Exception as e:
            # Group the DataFrame by the specified columns
            grouped = df_merged.groupby(b3.unique_sheet_cols, group_keys=False)

            # Set up a progress bar to monitor the processing of each group
            with tqdm(total=grouped.ngroups, desc=f"Calculating quarter values for year {year}") as pbar:
                # Use lambda to pass the progress bar to the function
                calculated_df = grouped.apply(lambda group: cvm_wrapper_apply(group, pbar)).reset_index(drop=True)
            
            # Save the calculated dataframe to the math dictionary and to files
            math[year] = calculated_df
            # math = sys_save_pkl(math, f'{b3.app_folder}/math_local')
            math[year] = sys_save_pkl(math[year], f'{b3.app_folder}/temp_math_{where}_{year}')

    return math

def process_year_data(year, df_merged, where):
    """
    Processa dados financeiros para um ano específico e salva o resultado.

    Tenta carregar um DataFrame previamente processado e salvo. Se isso falhar (por exemplo, se o arquivo não existir),
    processa o DataFrame fornecido, aplica ajustes matemáticos e salva o resultado.

    Args:
    - year (int): O ano correspondente ao DataFrame.
    - df_merged (pd.DataFrame): O DataFrame a ser processado.
    - where (str): Identificador que determina onde salvar o arquivo processado.

    Returns:
    - tuple: Uma tupla contendo o ano e o DataFrame processado.
    """
    try:
        # Tenta carregar um DataFrame previamente processado.
        return year, sys_load_pkl(f'{b3.app_folder}/temp_math_{where}_{year}')
    except Exception as e:
        try:
            # Se falhar, processa o DataFrame.
            print(f'INICIANDO {b3.app_folder}/temp_math_{where}_{year}')

            # Agrupa o DataFrame 'df_merged' por múltiplas colunas-chave. 
            grouped = df_merged.groupby(b3.unique_sheet_cols, group_keys=False)

            # Aplica uma função de ajuste matemático a cada grupo no DataFrame agrupado.
            calculated_df = grouped.apply(lambda group: cvm_math_calculations_adjustments(group)).reset_index(drop=True)

            # Salva o DataFrame processado e ajustado em um arquivo
            sys_save_pkl(calculated_df, f'{b3.app_folder}/temp_math_{where}_{year}')

            print(f'{b3.app_folder}/temp_math_{where}_{year} FINALIZADO')
        except Exception as e:
            # Em caso de falha, retorna o DataFrame original.
            calculated_df = df_merged
        return year, calculated_df

def cvm_calculate_math_multiprocessing(cvm, where):
    """
    Calcula ajustes matemáticos para cada ano em um dicionário de DataFrames e retorna os resultados.

    Utiliza processamento paralelo para processar os DataFrames de cada ano. 
    Cada DataFrame é processado pela função 'process_year_data'.

    Args:
    - cvm (dict): Dicionário com anos como chaves e DataFrames como valores.
    - where (str): Identificador para determinar onde salvar os arquivos processados.

    Returns:
    - dict: Dicionário com anos como chaves e DataFrames processados como valores.
    """
    math = {}
    # Prepara argumentos para processamento paralelo.
    args = [(year, df_merged, where) for year, df_merged in cvm.items()]

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        # Processa cada DataFrame em paralelo e coleta os resultados
        results = pool.starmap(process_year_data, args)

    for year, calculated_df in results:
        # Dicionário de anos com os dataframes calculados
        math[year] = calculated_df

    return math

def year_to_company(cvm_web):
# Get all unique companies across all years
    all_companies = set()
    for i, (year, df) in enumerate(cvm_web.items()):
        all_companies.update(df['DENOM_CIA'].unique())

    # Initialize the final dictionary with companies as keys
    companies = {}

    # Populate the company_dict
    start_time = time.time()
    try:
        for i, company in enumerate(all_companies):
        #   if company == 'ALPARGATAS SA':
            print(sys_remaining_time(start_time, len(all_companies), i))
            company_df = []  # This will hold dataframes for each year for the company
            for j, (year, df) in enumerate(cvm_web.items()):
                company_data = df[df['DENOM_CIA'] == company]
                company_df.append(company_data)
            companies[company] = pd.concat(company_df, ignore_index=True)
    except Exception as e:
        pass    
        # Concatenate the data for the company across all years

    companies = sys_save_pkl(companies, f'{b3.app_folder}/database')
    return companies

def get_diff(df1, df2):
    # Create a mask to identify rows in df2 where 'VL_CONTA' is different from df1
    mask_diff = df1['VL_CONTA'] != df2['VL_CONTA']

    # Initialize an empty list to store DataFrames with differences
    df_math = []

    # Iterate through rows in df2 that have differences in 'VL_CONTA'
    for i, (idx, row) in enumerate(df2[mask_diff].iterrows()):
        # Print information about the difference
        print(
            f"{row['DENOM_CIA']}, {row['AGRUPAMENTO']}, {row['DT_REFER'].strftime('%Y-%m-%d')}, "
            f"Old Value: {int(df1.loc[idx, 'VL_CONTA'])} -> New Value: {int(row['VL_CONTA'])}, "
            f"{row['CD_CONTA']}, {row['DS_CONTA']}")

        # Create filters to identify rows in df2 that match the current difference
        filter_mask_cia = df2['DENOM_CIA'] == row['DENOM_CIA']
        filter_mask_agg = df2['AGRUPAMENTO'] == row['AGRUPAMENTO']
        filter_mask_conta = df2['CD_CONTA'] == row['CD_CONTA']
        filter_mask_year = df2['DT_REFER'].dt.year == row['DT_REFER'].year

        # Combine filters to create a mask for the matching rows in df2
        mask = filter_mask_cia & filter_mask_agg & filter_mask_conta & filter_mask_year

        # Append the filtered matching rows to the list
        df_math.append(df2[mask])

    # If there are matching rows, concatenate them into a single DataFrame
    if df_math:
        df_math = pd.concat(df_math, ignore_index=False)

    # Return the DataFrame containing differences
    return df_math

def create_df_math(df_old, df_web):
    year = 2019
    try:
        mask_cia = df_web[year]['DENOM_CIA'] == 'ALPARGATAS SA'
        mask_agg = df_web[year]['AGRUPAMENTO'] == 'con'
        mask_quarter = df_web[year]['DT_REFER'] == '2014-06-30'
        mask_sheet = df_web[year]['BALANCE_SHEET'] == 'BPA'
        mask_CD_CONTA = df_web[year]['CD_CONTA'] == '1'
        mask = mask_cia & mask_agg & mask_quarter & mask_sheet & mask_CD_CONTA
        df_web[year].loc[mask, 'VL_CONTA'] = 1000000.0
    except Exception as e:
        pass

    try:
        mask_cia = df_web[year+1]['DENOM_CIA'] == 'ALPARGATAS SA'
        mask_agg = df_web[year+1]['AGRUPAMENTO'] == 'con'
        mask_quarter = df_web[year+1]['DT_REFER'] == '2015-09-30'
        mask_sheet = df_web[year+1]['BALANCE_SHEET'] == 'DRE'
        mask_CD_CONTA = df_web[year+1]['CD_CONTA'] == '3.01'
        mask = mask_cia & mask_agg & mask_quarter & mask_sheet & mask_CD_CONTA
        df_web[year+1].loc[mask, 'VL_CONTA'] = 1000000.0
    except Exception as e:
        pass

    try:
        mask_cia = df_web[year+2]['DENOM_CIA'] == 'ALPARGATAS SA'
        mask_agg = df_web[year+2]['AGRUPAMENTO'] == 'con'
        mask_quarter = df_web[year+2]['DT_REFER'] == '2016-12-31'
        mask_sheet = df_web[year+2]['BALANCE_SHEET'] == 'DFC_MI'
        mask_CD_CONTA = df_web[year+2]['CD_CONTA'] == '6.01'
        mask = mask_cia & mask_agg & mask_quarter & mask_sheet & mask_CD_CONTA
        df_web[year+2].loc[mask, 'VL_CONTA'] = 1000000.0
    except Exception as e:
        pass

   # Iterate through the years and DataFrames in df_web
    # Initialize the dictionary to store differences
    df_math = {}

    for year, df in df_web.items():
        # Check if the year is in the past
        if year in df_old and df_old[year].shape == df_web[year].shape:
            # Call the get_diff function to identify and extract differences
            dfs = get_diff(df_old[year], df_web[year])
            
            # Check if there are differences found
            if len(dfs) > 0:
                # Store the differences in the dictionary using the year as the key
                df_math[year] = dfs
            else: 
                df_math[year] = df_web[year]
        else:
            # If the year is not in df_old or the shapes don't match, store the entire df_web[year]
            df_math[year] = df_web[year]

    return df_math.copy()

def merge_cvm_math(cvm_web, df_math):
    for year in cvm_web.keys():
        # Update df_cvm['VL_CONTA'] using the values from df_math['VL_CONTA']
        cvm_web[year].loc[df_math[year].index, 'VL_CONTA'] = df_math[year]['VL_CONTA']
    return cvm_web

def merge_math(math_existing, math_web):
    df1 = math_existing
    df2 = math_web

    # The key columns used to determine unique rows
    key_columns = ['DENOM_CIA', 'AGRUPAMENTO', 'CD_CONTA', 'DT_REFER']

    # Create an empty dictionary to store the merged dataframes for each year
    df_merged = {}
    try:
        # https://chat.openai.com/c/ba8fa5e3-d96f-4db6-8900-864b3561809e
        # https://chat.openai.com/c/4d86bf87-0f68-4df2-8bfc-93ee143c9cac
        # https://chat.openai.com/c/938e4bbc-0d46-4c2e-ad7e-ed07c76859b3
        # https://chat.openai.com/c/a68f7b71-fa50-4d90-9df9-f6a961acb3bf  

        # Iterate over each year present in either df1 or df2
        for year in set(df1.keys()).union(df2.keys()):
            print(year)
            # Check if the year exists in df2 (the newer dataframe)
            if year in df2:
                # Start with the data from df2 for this year
                merged_df = df2[year].copy()
                
                # Check if the year also exists in df1 (the older dataframe)
                if year in df1:
                    # Determine the rows in df1[year] that are not present in df2[year]
                    # based on the key columns
                    mask = ~df1[year].set_index(key_columns).index.isin(df2[year].set_index(key_columns).index)
                    
                    # Filter df1[year] to only these rows
                    extra_rows = df1[year][mask]
                    
                    # Use pandas.concat to combine the dataframes
                    merged_df = pd.concat([merged_df, extra_rows], ignore_index=False)
            else:
                # If the year doesn't exist in df2, then just use the data from df1
                merged_df = df1[year].copy()

            # Store the merged dataframe for this year in the df_merged dictionary
            df_merged[year] = merged_df

        # At this point, df_merged will have the merged data for each year
        # print(len(df_merged))
    except Exception as e:
       pass
    return df_merged

def math_from_cvm(cvm_local):
    math_local = {}
    years = sorted(cvm_local.keys())
    df_columns = cvm_local[min(years)].columns
    for year in years:
        try:
            math_local[year] = sys_load_pkl(f'{b3.app_folder}/math_web_{year}')
        except Exception as e:
            math_local[year] = pd.DataFrame(columns=df_columns)

    return math_local

def math_merge(math_local, math_web):
    print('... math merge')
    math = {}
    years = sorted(set(math_local.keys()).union(math_web.keys()))
    try:
        df_columns = math_local[min(years)].columns
    except Exception as e:
        df_columns = math_web[min(years)].columns
    value_column = 'VL_CONTA'
    key_columns = [col for col in df_columns if col != value_column]

    try:
        for year in years:
            print(year)
            df_local = math_local.get(year, pd.DataFrame(columns=df_columns))
            df_web = math_web.get(year, pd.DataFrame(columns=df_columns))

            # Merge dataframes based on key columns
            df_merged = pd.merge(df_local, df_web, on=key_columns, how='outer', suffixes=('_now', '_new'))

            # Check if VL_CONTA in df_web contains a value, if it does, use it, otherwise use df_local's value
            mask = ~df_merged[f'{value_column}_new'].isna()
            df_merged[value_column] = np.where(mask, df_merged[f'{value_column}_new'], df_merged[f'{value_column}_now'])

            # Drop temporary columns
            df_merged.drop(columns=[f'{value_column}_now', f'{value_column}_new'], inplace=True)

            # Store the updated dataframe in the math dictionary
            math[year] = df_merged[df_columns]

    except Exception as e:
        # Handle exception (for now, just passing)
        pass

    return math

def companies_from_math(math):
    print('... extracting company info')
    company = {}

    # Iterate over each year in math
    for year, df in math.items():
        print(year)
        # Group by 'DENOM_CIA'
        for company_name, group in df.groupby('DENOM_CIA'):
            # Check if the company is already a key in the companies dictionary
            if company_name not in company:
                company[company_name] = group
            else:
                # Concatenate the new group to the existing dataframe for that company
                company[company_name] = pd.concat([company[company_name], group])

    return dict(sorted(company.items()))

def cvm_get_databases_from_cvm(math='', cvm_local='', cvm_web='', math_local='', math_web=''):
    try:
        # prepare cvm_local and cvm_web
        if not cvm_local:
            try:
                cvm_local = sys_load_pkl(f'{b3.app_folder}/cvm')
            except Exception as e:
                cvm_local = {}
        if not cvm_web:
            cvm_web = cvm_get_web_database()

        # Compare web (new) data to local (old) data. Extract only updated rows
        cvm_updated = cvm_updated_rows(cvm_local, cvm_web)
        cvm_updated = sys_save_pkl(cvm_updated, f'{b3.app_folder}/temp_'+'cvm_updated')
        # print('fast cvm_updated debug')
        # cvm_updated = sys_load_pkl(f'{b3.app_folder}/temp_'+'cvm_updated')

        # cvm_local = sys_load_pkl(f'{b3.app_folder}/cvm')
        # math_local = cvm_calculate_math(cvm_local, where='local')
        # math_local = sys_save_pkl(math_local, f'{b3.app_folder}/temp_'+'math_local')
        print('fast_debug_local_math')
        math_local = sys_load_pkl(f'{b3.app_folder}/temp_math_local')

        # cvm_web = sys_load_pkl(f'{b3.app_folder}/temp_'+'cvm_updated')
        # math_web = cvm_calculate_math(cvm_web, where='web')
        # math_web = sys_save_pkl(math_web, f'{b3.app_folder}/temp_'+'math_web')
        print('fast_debug_web_math')
        math_web = sys_load_pkl(f'{b3.app_folder}/temp_math_web')

        cvm_updated = sys_load_pkl(f'{b3.app_folder}/temp_'+'cvm_updated')
        math_updated = cvm_calculate_math(cvm_updated, where='updated')
        math_updated = sys_save_pkl(math_updated, f'{b3.app_folder}/temp_'+'math_updated')
        # print('fast_debug_updated_math')
        # math_updated = sys_load_pkl(f'{b3.app_folder}/temp_math_updated')

        # math_local
        try:
            math_local = sys_load_pkl(f'{b3.app_folder}/temp_'+'math')
        except Exception as e:
            math_local = {}
# try:
    # math_local = math_from_cvm(cvm_local) # shortcut to load math per year, not necessary unless huge huge database
    # math_local = get_calculated_math(cvm_local) # this is where the groupby transformation mathmagic happens
    # math_local = sys_save_pkl(math_local, f'{b3.app_folder}/math_local')
# except Exception as e:

        # math_web
        try:
            math_web = sys_load_pkl(f'{b3.app_folder}/math_web')
        except Exception as e:
            cvm_local, math_web = cvm_updated_rows(cvm_local, cvm_web)

        math = math_merge(math_local, math_web)

    except Exception as e:
        pass

    return math

def get_math_from_b3_cvm():
    b3_cvm = sys_load_pkl(f'{b3.app_folder}/b3_cvm')

    # Initialize a new dictionary to hold the results
    math = {}

    # Iterate through each sector's dataframe in the b3_cvm dictionary
    for sector, df in b3_cvm.items():
        print(sector)
        # Extract unique years in the current dataframe
        unique_years = df['ANO'].unique()
        for year in unique_years:
            # Filter the dataframe to include only rows corresponding to the current year
            year_df = df[df['ANO'] == year]
            
            # If the year is already a key in the dictionary, append the new dataframe to its list
            if year in math:
                math[year].append(year_df)
            else:
                math[year] = [year_df]

    # After looping through all sectors, concatenate all lists in the dictionary to create the final dataframes
    for year, df_list in math.items():
        print(year)
        math[year] = pd.concat(df_list, ignore_index=True)

    return math

def get_classificacao_setorial(setorial=''):
    driver, wait = sys_load_browser()
    driver.get(b3.url_setorial)
    # time.sleep(1)

    # Find the download link using the XPATH you provided
    download_link_element = driver.find_element(By.XPATH, '//*[@id="divContainerIframeB3"]/div/div/app-companies-home-filter-classification/form/div[2]/div[3]/div[2]/p/a')
    url = download_link_element.get_attribute('href')
    time.sleep(3)
    response = requests.get(url, headers=sys_header_random())
    filename = url.split("/")[-1]

    with open(filename, 'wb') as f:
        f.write(response.content)

    # Step 2: Extract the zip
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(b3.download_folder)

    # Assuming only one .xlsx file inside the zip
    xlsx_file = [f for f in os.listdir(b3.download_folder) if f.endswith('.xlsx')][0]

    # Step 3: Read the Excel file
    setorial = pd.read_excel(os.path.join(b3.download_folder, xlsx_file))
    shutil.rmtree(b3.download_folder)
    driver.quit()

    # clean up setorial# Modifying the extraction method based on the updated insights

    # First, let's identify the start of the data based on the header
    start_row = setorial[setorial.eq("SETOR ECONÔMICO").any(axis=1)].index[0] + 1
    end_row = setorial[setorial.eq("(DR1) BDR Nível 1").any(axis=1)].index[0] - 1

    # Extracting the relevant data starting from the identified row
    subset_df = setorial.loc[start_row:end_row].reset_index(drop=True)
    subset_df.columns = ['SETOR', 'SUBSETOR', 'SEGMENTO/DENOM_CIA', 'CIA_CODE', 'CIA_LISTAGEM']

    # Initialize the columns
    subset_data = {
        'SETOR': [],
        'SUBSETOR': [],
        'SEGMENTO': [],
        'DENOM_CIA': [],
        'CIA_CODE': [],
        'CIA_LISTAGEM': []
    }
    # Temporary variables to hold the current SETOR, SUBSETOR, and SEGMENTO
    current_setor = None
    current_subsetor = None
    current_segmento = None

    # Iterate through the rows
    for i, row in subset_df.iterrows():
        col_1, col_2, col_3, col_4, col_5 = row
        
        # Company row
        if pd.notnull(col_3) and pd.notnull(col_4):
            if col_3.strip() != 'SEGMENTO':
                subset_data['SETOR'].append(current_setor.strip() if current_setor else None)
                subset_data['SUBSETOR'].append(current_subsetor.strip() if current_subsetor else None)
                subset_data['SEGMENTO'].append(current_segmento.strip() if current_segmento else None)
                subset_data['DENOM_CIA'].append(col_3.strip())
                subset_data['CIA_CODE'].append(col_4.strip())
                subset_data['CIA_LISTAGEM'].append(col_5.strip() if pd.notnull(col_5) else '')

        # SEGMENTO row
        elif pd.notnull(col_3) and pd.isnull(col_4):
            current_setor = col_1 if pd.notnull(col_1) else None
            current_subsetor = col_2 if pd.notnull(col_2) else None  # Reset the SUBSETOR if it's NaN
            current_segmento = col_3 if pd.notnull(col_3) else None  # Reset the SEGMENTO if it's NaN

        # SUBSETOR row
        elif pd.notnull(col_2):
            current_setor = col_1 if pd.notnull(col_1) else None
            current_subsetor = col_2 if pd.notnull(col_2) else None  # Reset the SUBSETOR if it's NaN
            current_segmento = col_3 if pd.notnull(col_3) else None  # Reset the SEGMENTO if it's NaN

        # SETOR row
        elif pd.notnull(col_1):
            current_setor = col_1 if pd.notnull(col_1) else None
            current_subsetor = col_2 if pd.notnull(col_2) else None  # Reset the SUBSETOR if it's NaN
            current_segmento = col_3 if pd.notnull(col_3) else None  # Reset the SEGMENTO if it's NaN

    # Convert the data to a DataFrame
    setorial = pd.DataFrame(subset_data)
    setorial['SETOR'] = setorial['SETOR'].fillna(method='ffill')
    setorial['SUBSETOR'] = setorial['SUBSETOR'].fillna(method='ffill')
    setorial['SEGMENTO'] = setorial['SEGMENTO'].fillna(method='ffill')
    setorial['CIA_LISTAGEM'].fillna('', inplace=True)
    for col in setorial.columns:
        setorial [col]= setorial[col].apply(clean_text)

    return setorial

def get_companies(math, company):
    # Initialize a new dictionary to hold the results
    b3_cvm = {}

    # Iterate through each year's dataframe in the math dictionary
    for year, df in math.items():
        print(year)
        # Merge the dataframe for that year with company_b3 based on CNPJ
        merged_df = pd.merge(df, company, how='left', left_on='CNPJ_CIA', right_on='CNPJ')
        
        # Group by 'SETOR' and store each group's dataframe in a list inside the new dictionary
        for sector, sector_df in merged_df.groupby('SETOR'):
            # If the sector is already a key in the dictionary, append the new dataframe to its list
            if sector in b3_cvm:
                b3_cvm[sector].append(sector_df)
            else:
                b3_cvm[sector] = [sector_df]

    # After looping through all years, concatenate all lists in the dictionary to create the final dataframes
    for sector, df_list in b3_cvm.items():
        print(sector)
        b3_cvm[sector] = pd.concat(df_list, ignore_index=True)

    b3_cvm = sys_save_pkl(b3_cvm, f'{b3.app_folder}/b3_cvm')

    return b3_cvm

def b3_get_company_full_info(data, full_company_info):
    data = data[1:]  # Removing the name as it's already processed

    # Remove empty or whitespace-only items
    data = [item for item in data if item.strip()]

    # Bookholder (assuming "Instituição:" is the identifier)
    bookholder_pattern = r'Instituição: (.+)'
    for item in reversed(data):
        match = re.search(bookholder_pattern, item)
        if match:
            full_company_info["escriturador"] = match.group(1).strip()
            data.remove(item)
            break

    # Site
    site_pattern = r'(?:http[s]?://)?(?://)?(?:www\.)?[a-zA-Z0-9-]+\.(?:com|org|edu|net|[a-z]{2}|com\.[a-z]{2})[^\s]*'
    for item in reversed(data):
        match = re.search(site_pattern, item)
        if match:
            full_company_info["site"] = match.group()
            data.remove(item)
            break

    # Setor (with subcategories)
    setor_pattern = r'.+/.+/.+'
    for item in reversed(data):
        match = re.search(setor_pattern, item)
        if match:
            sector_classification = match.group()
            setor, subsetor, segmento = sector_classification.split(' / ') if sector_classification else (None, None, None)
            full_company_info["setor"] = sys_clean_text(setor)
            full_company_info["subsetor"] = sys_clean_text(subsetor)
            full_company_info["segmento"] = sys_clean_text(segmento)
            data.remove(item)
            break

    # CNPJ
    cnpj_pattern = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
    for item in data:
        match = re.search(cnpj_pattern, item)
        if match:
            full_company_info["cnpj"] = match.group()
            data.remove(item)
            break

    # Atividade (assuming it's a short description without special characters)
    for item in reversed(data):
        if 5 < len(item):
            full_company_info["atividade"] = item.strip()
            data.remove(item)
            break

    return full_company_info

def get_companies_from_b3_cards(driver, wait):
    """
    Grabs company details from the current page.
    
    Returns:
    list: A list of dictionaries containing company details.
    """
    max_retries = 5
    sleep_time = 0.1
    company_list_from_web = []

    # Attempt to scrape company details from the current page
    for attempt in range(max_retries):
        try:
            # Extract company details
            time.sleep(sleep_time*5)
            company_names = [elem.text.strip() for elem in wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="nav-bloco"]/div/div/div/div/p[@class="card-title"]')))]
            trading_names = [elem.text.strip() for elem in wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="nav-bloco"]/div/div/div/div/p[@class="card-text"]')))]
            trading_codes = [elem.text.strip() for elem in wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="nav-bloco"]/div/div/div/div/h5[@class="card-title2"]')))]
            listagem_values = [elem.text.strip() for elem in wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="nav-bloco"]/div/div/div/div/p[3]')))]

            # Create and append dictionaries with the company details
            for i in range(len(company_names)):
                company_list_from_web.append({
                    'COMPANHIA': sys_clean_text(company_names[i]),
                    'PREGAO': trading_names[i],
                    'TICK': trading_codes[i],
                    'LISTAGEM': listagem_values[i]
                })
            break
        except Exception as e:
            print('th' + 'i' * (attempt + 1) + 'nking...')
            time.sleep(sleep_time)

    return company_list_from_web

def get_b3_companies_from_site(driver, wait, url):
    # Initialize the list to store new companies' details
    company_list_from_web = []
    max_retries = 5
    sleep_time = 0.1
    driver.get(url)
    try:
        # Attempt to set the dropdown to display the maximum number of companies per page
        for attempt in range(max_retries):
            try:
                # Select the last option in the dropdown (maximum display count)
                dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="divContainerIframeB3"]/form/div[3]/div[1]/select')))
                all_options = dropdown.find_elements(By.XPATH, './/option')
                companies_per_page = int(all_options[-1].text.strip())
                all_options[-1].click()

                # Calculate the total number of pages required to display all companies
                total_companies_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="divContainerIframeB3"]/form/div[1]/div/div/div[1]/p/span[1]')))
                total_companies = int(total_companies_element.text.replace('.', '').strip())
                total_pages = (total_companies // companies_per_page) + (1 if total_companies% companies_per_page > 0 else 0)
                break
            except Exception as e:
                print('th' + 'i' * (attempt + 1) + 'nking...')
                time.sleep(sleep_time)

        # Loop through each page and scrape company details
        start_time = time.time()
        for tp in range(total_pages):
            print(sys_remaining_time(start_time, total_pages, tp))

            # Attempt to scrape company details from the current page
            for attempt in range(max_retries):
                try:
                    # Use the get_companies() function to extract the details
                    companies_in_page = get_companies_from_b3_cards(driver, wait)
                    company_list_from_web.extend(companies_in_page)
                    break
                except Exception as e:
                    print('th' + 'i' * (attempt + 1) + 'nking...')
                    time.sleep(sleep_time)

            # Move to the next page if not on the last page
            if tp < total_pages - 1:
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="listing_pagination"]/pagination-template/ul/li[10]/a')))
                next_button.click()

    except Exception as e:
        pass

    return company_list_from_web

def b3_grab_from_web_OLD(driver, wait, url): # OLD DEF, or still usefull. b3_get_companies is it better??
    """
    Update missing companies from the provided dataframe by searching the web using the provided driver and wait object.

    Args:
    - value: Any, initial value
    - driver: WebDriver, instance of the web driver
    - wait: Any, instance of the wait object

    Returns:
    - str: status message
    """
    b3_companies_local = sys_read_or_create_dataframe('b3_companies', b3.cols_b3_companies)

    try:
        # Get the total number of companies and pages
        driver.get(b3.search_url)
        batch = wSelect(f'//*[@id="selectPage"]', driver, wait)
        companies = wText(f'//*[@id="divContainerIframeB3"]/form/div[1]/div/div/div[1]/p/span[1]', wait)
        companies = int(companies.replace('.',''))
        pages = int(companies/batch)

        value = f'found {companies} companies in {pages+1} pages'
        print(value)

        # Get all available companies directly from the web
        # driver.get(search_url)
        # time.sleep(1)
        wSelect(f'//*[@id="selectPage"]', driver, wait)
        raw_code = []
        start_time = time.time()
        for i, page in enumerate(range(0, pages+1)):
            xpath = '//*[@id="nav-bloco"]/div'
            inner_html = wRaw(xpath, wait)
            raw_code.append(inner_html)
            wClick(f'//*[@id="listing_pagination"]/pagination-template/ul/li[10]/a', wait)
            time.sleep(0.5)
            value = f'page {page+1}'
            print(sys_remaining_time(start_time, pages+1, i), value)
        b3_companies_tickers = get_ticker_keywords(raw_code)

        # Update the missing companies from the database
        b3_companies_local_keywords = []
        # Create a list of all current companies in the b3_companies dataframe
        for index, row in b3_companies_local.iterrows():
            try:
                b3_companies_local_keywords.append(' '.join([str(row['ticker']), str(row['company_name'])]))
            except Exception as e:
                print(row)
                pass

        counter = 0
        size = len(b3_companies_tickers)

        # Loop through each company in the b3_companies_tickers dataframe
        start_time = time.time()
        for i, (index, row) in enumerate(b3_companies_tickers.iterrows()):
            counter +=1
            new_keyword = str(row['ticker']) + ' ' + str(row['company_name'])
            if new_keyword not in b3_companies_local_keywords:
                driver.get(b3.url)

                kw = wSendKeys(f'//*[@id="keyword"]', new_keyword, wait)
                kw = wClick(f'//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div/div[3]/button', wait)

                company = get_company(1, driver, wait)
                b3_companies_local = pd.concat([b3_companies_local, pd.DataFrame([company], columns=b3.cols_b3_companies)])
            else:
                pass
            print(sys_remaining_time(start_time, len(b3_companies_tickers), i), counter, size-counter, new_keyword)
            if (len(b3_companies_tickers) - i - 1) % b3.bin_size == 0:
                b3_companies_local = sys_save_and_pickle(b3_companies_local, 'b3_companies')
                print('partial save')
        b3_companies_local.fillna('', inplace=True)
        b3_companies_local.reset_index(drop=True, inplace=True)
        b3_companies_local.drop_duplicates(subset='url', inplace=True)
        
        b3_companies_local = sys_save_and_pickle(b3_companies_local, 'b3_companies')
        # b3_companies.to_pickle(data_path + f'{df_name}.zip')

        # Close the driver and exit the script
        driver.close()
        driver.quit()

        value = f'{len(b3_companies_local)} companies updated'
        print(value)

    except Exception as e:
        pass
    return b3_companies_local

def get_new_companies_from_b3(driver, wait, url):
    cols = ['COMPANHIA', 'PREGAO', 'TICK', 'LISTAGEM']

    # print('debug 1')
    company_list_from_web = b3_grab_from_web(driver, wait, url) # new way

    return company_list_from_web

def b3_get_company_info(row, driver, wait):
    # Define columns and constants
    max_retries = 5
    sleep_time = 0.1

    full_company_info = {}

    full_company_info['ticker'] = row['ticker']
    full_company_info['company_name'] = row['company_name']
    full_company_info['pregao'] = row['pregao']
    full_company_info['listagem'] = row['listagem']

    # 1 Searching for the company using its name
    for attempt in range(max_retries):
        try:
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="keyword"]')))
            search_box.clear()
            search_box.send_keys(f"{full_company_info['ticker']} {full_company_info['company_name']}")

            search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div/div[3]/button')))
            search_button.click()
            break
        except Exception as e:
            print('o' * (attempt + 1) + 'ps..')
            time.sleep(sleep_time)

    # 2 Selecting the company's card from the results
    for attempt in range(max_retries):
        try:
            # Wait for the cards container to be present
            cards_container = wait.until(EC.presence_of_element_located((By.ID, "nav-bloco")))

            # Find all the cards within the container
            cards = cards_container.find_elements(By.XPATH, ".//div[contains(@class, 'card h-100 clickable')]")

            # Iterate through the cards to find the one that matches the company information
            for card in cards:
                ticker = sys_clean_text(card.find_element(By.XPATH, ".//h5[@class='card-title2']").text)
                company_name = sys_clean_text(card.find_element(By.XPATH, ".//p[@class='card-title']").text)

                # If the card's pregao and company_name match the company information, click the card
                if ticker == full_company_info['ticker'] and company_name == full_company_info['company_name']:
                    card.click()  # Click the matching card
                    break  # Exit the loop after clicking the correct card

        except Exception as e:
            print('o' * (attempt + 1) + 'ps..')
            time.sleep(sleep_time)
        break

    # 3 Extracting the CVM code from the company's URL
    for attempt in range(max_retries):
        try:
            current_url = driver.current_url
            full_company_info['url'] = current_url
            cvm_code = current_url.split('/')[-3]
            int(cvm_code)  # Validates if the code is numeric
            full_company_info['cvm_code'] = cvm_code
            break
        except Exception as e:
            full_company_info['url'] = ''
            full_company_info['cvm_code'] = ''
            
            print('o' * (attempt + 1) + 'ps..')
            time.sleep(sleep_time)

    # 4 Extracting general company information
    for attempt in range(max_retries):
        try:
            full_company_info['cnpj'] = ''
            full_company_info['atividade'] = ''
            full_company_info['setor'] = 'NENHUM'
            full_company_info['subsetor'] = 'NENHUM'
            full_company_info['segmento'] = 'NENHUM'
            full_company_info['site'] = ''
            full_company_info['escriturador'] = ''
            full_company_info['stock_holders'] = ''

            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//p[@class="card-linha"]')))
            data = [element.text.strip() for element in elements]
            full_company_info = b3_get_company_full_info(data, full_company_info)
            break
        except Exception as e:
            print('o' * (attempt + 1) + 'ps..')
            time.sleep(sleep_time)

    # 5 Extracting tickers and ISIN codes
    for attempt in range(max_retries):
        try:
            table_html = driver.find_element(By.XPATH, '//*[@id="accordionBody2"]/div/table').get_attribute('outerHTML')
            table_df = pd.read_html(table_html, header=0)[0]
            full_company_info['tickers'] = ', '.join(table_df.iloc[:, 0].tolist())
            full_company_info['isins'] = ', '.join(table_df.iloc[:, 1].tolist())
            break
        except Exception as e:
            full_company_info['tickers'], full_company_info['isins'] = None, None
            time.sleep(sleep_time)

    # 6 Extracting major stock_holders
    for attempt in range(max_retries):
        try:
            table_html = driver.find_element(By.XPATH, '//*[@id="accordionBodyTwo"]/div/table').get_attribute('outerHTML')
            tables = pd.read_html(table_html)
            stock_holders = tables[0].copy().iloc[:-1, :]
            stock_holders.iloc[:, 1:] = stock_holders.iloc[:, 1:] / 100
            stock_holders['Nome'] = stock_holders['Nome'].apply(sys_clean_text) # Apply sys_clean_text only to the 'Nome' column in the DataFrame
            stock_holders['companhia'] = full_company_info['company_name']
            stock_holders['cnpj'] = full_company_info['cnpj']
            stock_holders['setor'] = full_company_info['setor']
            stock_holders['subsetor'] = full_company_info['subsetor']
            stock_holders['segmento'] = full_company_info['segmento']
            full_company_info['stock_holders'] = stock_holders.to_dict(orient='records')
            break
        except Exception as e:
            stock_holders = pd.DataFrame()
            full_company_info[''] = stock_holders.to_dict(orient='records')
            time.sleep(sleep_time)
            break
    return full_company_info

def b3_get_b3_tickers(driver, wait, url):
    try:
        # Get the total number of companies and pages
        driver.get(url)
        batch = wSelect(f'//*[@id="selectPage"]', driver, wait)
        companies = wText(f'//*[@id="divContainerIframeB3"]/form/div[1]/div/div/div[1]/p/span[1]', wait)
        companies = int(companies.replace('.',''))
        pages = int(companies/batch)

        value = f'found {companies} companies in {pages+1} pages'
        print(value)

        # Get all available companies directly from the web
        # driver.get(search_url)
        # time.sleep(1)
        wSelect(f'//*[@id="selectPage"]', driver, wait)
        raw_code = []
        start_time = time.time()
        for i, page in enumerate(range(0, pages+1)):
            xpath = '//*[@id="nav-bloco"]/div'
            inner_html = wRaw(xpath, wait)
            raw_code.append(inner_html)
            wClick(f'//*[@id="listing_pagination"]/pagination-template/ul/li[10]/a', wait)
            time.sleep(0.5)
            value = f'page {page+1}'
            print(sys_remaining_time(start_time, pages+1, i), value)
        b3_companies_tickers = b3_get_ticker_keywords(raw_code)
    except Exception as e:
        pass

    return b3_companies_tickers

def b3_get_company_extra_cnpj_info(response):
    # Parse the HTML snippet
    tree = html.fromstring(response.text)
    
    # Dictionary to store the extracted information
    info = {
        "CNPJ": "",
        "Razão Social": "",
        "Nome Fantasia": "",
        "Data da Abertura": "",
        "Porte": "",
        "Natureza Jurídica": "",
        "Opção pelo MEI": "",
        "Opção pelo Simples": "",
        "Capital Social": "",
        "Tipo": "",
        "Situação": "",
        "Logradouro": "",
        "Bairro": "",
        "CEP": "",
        "Município": "",
        "Estado": ""
    }
    
    # Extract information from <p> elements
    p_elements = tree.xpath('//p')
    for p in p_elements:
        text_content = p.text_content()
        
        # Example to extract "CNPJ"
        if 'CNPJ:' in text_content:
            cnpj = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', text_content)
            if cnpj:
                info['CNPJ'] = cnpj.group(0)
        
        # Similarly, you can add conditions to extract other pieces of information
        # Example to extract "Razão Social"
        if 'Razão Social:' in text_content:
            razao_social = p.xpath('.//b[@class="copy"]/text()')
            if razao_social:
                info['Razão Social'] = sys_clean_text(razao_social[0])
        
        if 'Nome Fantasia:' in text_content:
            nome_fantasia = p.xpath('.//b[@class="copy"]/text()')
            if nome_fantasia:
                info['Nome Fantasia'] = sys_clean_text(nome_fantasia[0])
        
        # Extract "Data da Abertura"
        if 'Data da Abertura:' in text_content:
            data_abertura = re.search(r'\d{2}/\d{2}/\d{4}', text_content)
            if data_abertura:
                info['Data da Abertura'] = data_abertura.group(0)
        
        # Extract "Porte"
        if 'Porte:' in text_content:
            porte = text_content.split(':')[-1].strip()
            info['Porte'] = porte
        
        # Extract "Natureza Jurídica"
        if 'Natureza Jurídica:' in text_content:
            natureza_juridica = p.xpath('.//b[@class="copy"]/text()')
            if natureza_juridica:
                info['Natureza Jurídica'] = natureza_juridica[0]
        
        # Extract "Opção pelo MEI"
        if 'Opção pelo MEI:' in text_content:
            opcao_mei = text_content.split(':')[-1].strip()
            info['Opção pelo MEI'] = opcao_mei
        
        # Extract "Opção pelo Simples"
        if 'Opção pelo Simples:' in text_content:
            opcao_simples = text_content.split(':')[-1].strip()
            info['Opção pelo Simples'] = opcao_simples
        
        # Extract "Capital Social"
        if 'Capital Social:' in text_content:
            capital_social_str = p.xpath('.//b[@class="copy"]/text()')
            if capital_social_str:
                # Extract numbers, ignore R$ and commas, replace decimal separator
                capital_social_num = re.sub(r'[^\d,]', '', capital_social_str[0]).replace(',', '.')
                info['Capital Social'] = float(capital_social_num)
    
            # Extract "Tipo"
        if 'Tipo:' in text_content:
            tipo = p.xpath('.//b[@class="copy"]/text()')
            if tipo:
                info['Tipo'] = tipo[0]
        
        # Extract "Situação"
        if 'Situação:' in text_content:
            situacao = p.xpath('.//b[@class="copy"]/text()')
            if situacao:
                info['Situação'] = situacao[0]

        # Extract "Logradouro"
        if 'Logradouro:' in text_content:
            logradouro = p.xpath('.//b[@class="copy"]/text()')
            if logradouro:
                info['Logradouro'] = logradouro[0]

        # Extract "Bairro"
        if 'Bairro:' in text_content:
            bairro = p.xpath('.//b[@class="copy"]/text()')
            if bairro:
                info['Bairro'] = bairro[0]

        # Extract "CEP"
        if 'CEP:' in text_content:
            cep = re.search(r'\d{5}-\d{3}', text_content)
            if cep:
                info['CEP'] = cep.group(0)
        
        # Extract "Município"
        if 'Município:' in text_content:
            municipio = text_content.split(':')[-1].strip()
            info['Município'] = municipio
        
        # Extract "Estado"
        if 'Estado:' in text_content:
            estado = text_content.split(':')[-1].strip()
            info['Estado'] = estado

    # Return the extracted information
    return info

def change_col_type(df, str_cols, float_cols):
    """
    Modifica os tipos de colunas de um dataframe.

    Parâmetros:
    df (pandas.DataFrame): O dataframe para modificar.
    str_cols (list): Lista de nomes de colunas para converter para string.
    float_cols (list): Lista de nomes de colunas para converter para float.

    Retorna:
    pandas.DataFrame: O dataframe com os tipos de colunas alterados.
    """
    # Convertendo as colunas para float se estiverem presentes no dataframe
    float_cols_present = [col for col in float_cols if col in df.columns]
    df[float_cols_present] = df[float_cols_present].apply(lambda col: col.astype(float))

    # Convertendo as colunas para str se estiverem presentes no dataframe
    str_cols_present = [col for col in str_cols if col in df.columns]
    df[str_cols_present] = df[str_cols_present].apply(lambda col: col.astype(str))

    return df

def b3_get_companies(url):
    """
    Scrape company details from the B3 website and update a local database of companies.

    Parameters:
    - url (str): The URL of the B3 website's page containing the list of companies.

    Returns:
    - pd.DataFrame: A dataframe containing details of companies.

    Notes:
    This function performs the following tasks:
    1. Accesses the B3 website and scrapes company details such as name, trading name, trading code, etc.
    2. Updates the local database with new companies found.
    3. For each new company, accesses its detail page on the B3 website to scrape additional details.
    4. The function makes use of multiple retries to handle timeouts and missing elements during the scraping process.
    """

    # Define columns and constants
    max_retries = 5
    sleep_time = 0.1
    key_columns = ['ticker', 'company_name', 'pregao', 'listagem']
    b3_cols = b3.cols_b3_companies + b3.col_b3_companies_extra_columns
    b3_cols_float = ['Capital Social']
    b3_str_cols = [col for col in b3_cols if col not in  b3_cols_float]
    col_types = {col: 'float' if col in b3_cols_float else 'str' for col in b3_cols}

    # Initialize the browser and load the URL
    driver, wait = sys_load_browser()
    # time.sleep(1)

    # Scrape detailed data for each new company
    b3_companies_tickers = b3_get_b3_tickers(driver, wait, url)
    
    for col in b3_cols:
        if col not in b3_companies_tickers.columns:
            b3_companies_tickers[col] = ''
    b3_companies_tickers = b3_companies_tickers[b3_cols]
    b3_companies_tickers = sys_save_pkl(b3_companies_tickers, 'temp_b3_companies_tickers')
    # print('fast temp b3_companies')
    # b3_companies_tickers = sys_load_pkl('temp_b3_companies_tickers')

    # company = b3_grab_from_web(driver, wait, url) # new way
    companies_local = sys_read_or_create_dataframe('company', b3_cols).fillna('')

    # anti-join operation
    merged = pd.merge(companies_local, b3_companies_tickers, how='outer', on=key_columns, indicator=True)
    update_strict = merged[merged['_merge'] == 'right_only'][key_columns] # only companies new in web
    update_broad = merged[merged['_merge'] != 'left_only'][key_columns] # all companies from web
    updated = update_strict

    try:
        driver.get(b3.url)
        # time.sleep(1)

        size = len(updated)
        # Iterate through the new companies to extract detailed information
        new_companies = []
        start_time = time.time()
        for i, (index, row) in enumerate(updated.iterrows()):
            driver.get(b3.url)
            new_company = b3_get_company_info(row, driver, wait)
            new_company = pd.DataFrame([new_company], columns=b3_cols).astype(col_types).fillna('')
            new_company['Capital Social'] = new_company['Capital Social'].replace(np.nan, 0.0)
            new_company = new_company.replace('nan', '')
            # new_company['Capital Social'] = pd.to_numeric(new_company['Capital Social'], errors='coerce').astype('float')

            extra = ''
            try:
                if not new_company.empty:
                    cnpj = new_company['cnpj'][0]
                    if cnpj:
                        url = f'https://cnpj.biz/{cnpj}'
                        response = requests.get(url, headers=sys_header_random())
                        extra = b3_get_company_extra_cnpj_info(response)
                        extra = pd.DataFrame([extra], columns=b3_cols).astype(col_types).fillna('')
                    else:
                        extra = pd.DataFrame([], columns=b3_cols)

            except Exception as e:
                extra = pd.DataFrame([], columns=b3_cols)
            extra = extra.reset_index(drop=True)
            new_company = pd.merge(new_company[b3.cols_b3_companies], extra[b3.col_b3_companies_extra_columns], left_on='cnpj', right_on='CNPJ', how='outer').fillna('').reset_index(drop=True)
            new_companies.append(new_company)
            
            print(sys_remaining_time(start_time, size, i), row['ticker'], row['company_name'])

            if (size-i-1) % (b3.bin_size) == 0:
                temp = pd.concat(new_companies).reset_index(drop=True)
                temp['Capital Social'] = pd.to_numeric(temp['Capital Social'], errors='coerce').astype('float')
                temp['Capital Social'] = temp['Capital Social'].replace(np.nan, 0.0)
                temp = pd.merge(companies_local, temp, on=b3_cols, how='outer', indicator=False).fillna('').drop_duplicates(subset=key_columns, keep='last').reset_index(drop=True)
                temp = sys_save_and_pickle(temp, 'company')

    # Handle any exceptions that might have occurred during scraping
    except Exception as e:
        print(f"Error encountered: {str(e)}")

    # Ensure the browser is closed regardless of any exceptions
    finally:
        driver.quit()

    # Merge existing and updated companies back again
    try:
        company = pd.concat(new_companies).reset_index(drop=True)
        company['Capital Social'] = pd.to_numeric(company['Capital Social'], errors='coerce').astype('float')
        company['Capital Social'] = company['Capital Social'].replace(np.nan, 0.0)
        company = pd.merge(companies_local, company, on=b3_cols, how='outer', indicator=False).fillna('').drop_duplicates(subset=key_columns, keep='last').reset_index(drop=True)
        company = sys_save_and_pickle(company, 'company')

    except Exception as e:
        pass

    return company

def get_setores(url):
    # initialization
        # Set the maximum number of retries and sleep time.
        # Initialize an empty list, setorial.
    max_retries = 5
    sleep_time = 0.1
    setorial = []

    # Navigate to the specified URL
        # Load the browser and navigate to the given URL.
    driver, wait = sys_load_browser()
    driver.get(url)
    # time.sleep(1)

    # Locate the select element for sector dropdown
        # Identify the dropdown for sectors using its XPath.
        # Wait until the dropdown is available for interaction.
    select_element_xpath = '//*[@id="divContainerIframeB3"]/div/div/app-companies-home-filter-classification/form/div[1]/div/div/select'
    dropdown = wait.until(EC.presence_of_element_located((By.XPATH, select_element_xpath)))
    select = Select(dropdown)
    
    # Iterate through each option in the dropdown. For each option in the dropdown:
        # Try to select it and fetch its corresponding rows.
        # If an error occurs, refresh the page and retry.
        # Append the fetched rows to the setorial list.
    for idx, opt in enumerate(select.options):
        # opt = opt.get_attribute('value')
        for attempt in range(max_retries):
            try:
                # Re-fetch elements
                time.sleep(sleep_time*20)
                dropdown = wait.until(EC.presence_of_element_located((By.XPATH, select_element_xpath)))
                select = Select(dropdown)
                option = select.options[idx]
                option_value = option.get_attribute("value")
                select.select_by_value(option_value)
                setor = sys_clean_text(option_value)
                # Extract table data for the selected option
                table_xpath = '//*[@id="divContainerIframeB3"]/div/div/app-companies-home-filter-classification/form/table'
                rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{table_xpath}/tbody/tr")))
                data = get_segmentos(driver, wait, option_value)
                setorial.append(data)
                break
            except Exception as e:
                driver.refresh()  # Refresh the page
                print('o' * (attempt + 1) + 'ps.. in the SETOR SELECTION', e)

    setorial2 = pd.DataFrame(setorial)
    
    return setorial2

def get_segmentos(driver, wait, option_value):
    setorial = []
    max_retries = 5
    sleep_time = 0.1
    # Store the current URL before processing any segment
    current_url = driver.current_url

    # Extract table data
    table_xpath = '//*[@id="divContainerIframeB3"]/div/div/app-companies-home-filter-classification/form/table'
    rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{table_xpath}/tbody/tr")))

    for idx, _ in enumerate(rows):
        # time.sleep(sleep_time*20)
        # Re-locate rows each time to avoid stale element exceptions
        rows_fresh = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{table_xpath}/tbody/tr")))
        row = rows_fresh[idx]

        setor = sys_clean_text(option_value)
        subsetor = row.find_element(By.XPATH, "td[1]").text
        subsetor = sys_clean_text(subsetor)

        try:
            segmentos = row.find_elements(By.XPATH, "td[2]/p/a")
        except Exception as e:
            segmentos = wait.until(EC.presence_of_all_elements_located((By.XPATH, "td[2]/p/a")))
        
        for seg_idx, _ in enumerate(segmentos):
            # Re-fetch rows and segment links
            time.sleep(sleep_time*20)
            rows_fresh = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{table_xpath}/tbody/tr")))
            row = rows_fresh[idx]
            try:
                segmentos_fresh = row.find_elements(By.XPATH, "td[2]/p/a")
            except Exception as e:
                segmentos_fresh = wait.until(EC.presence_of_all_elements_located((By.XPATH, "td[2]/p/a")))
            item = segmentos_fresh[seg_idx]
            segmento = sys_clean_text(item.text)
            item.click()

            link = driver.current_url
            companies = get_companies_from_b3_cards(driver, wait)

            for company in companies:
                company_row = [sys_clean_text(setor), subsetor, segmento, link]
                company_row.extend([company[key] for key in ['COMPANHIA', 'PREGAO', 'TICK', 'LISTAGEM']])
                setorial.append(company_row)

            print(f'{sys_clean_text(setor)}: {subsetor}: {segmento}: {len(companies)}:')
            print(f'{[company["TICK"] for company in companies]}')
            for attempt in range(max_retries):
                try:
                    # Return to the original page
                    driver.get(current_url)
                    time.sleep(sleep_time*20)
                    table_xpath = '//*[@id="divContainerIframeB3"]/div/div/app-companies-home-filter-classification/form/table'
                    rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{table_xpath}/tbody/tr")))

                    # Ensure the dropdown is still set to the current setor
                    select_element_xpath = '//*[@id="divContainerIframeB3"]/div/div/app-companies-home-filter-classification/form/div[1]/div/div/select'
                    dropdown = wait.until(EC.presence_of_element_located((By.XPATH, select_element_xpath)))
                    select = Select(dropdown)
                    select.select_by_value(option_value)

                    # Re-fetching the rows after navigating back to the page
                    rows_fresh = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{table_xpath}/tbody/tr")))
                    # time.sleep(2)
                    break
                except Exception as e:
                    driver.refresh()  # Refresh the page
                    print('o' * (attempt + 1) + 'ps..')
                    time.sleep(sleep_time)
                    
    return setorial

def get_full_setorial_data(url):
    # Load browser
    setorial = get_setores(url)
    return setorial

def convert_columns(df, threshold=0.1):
    """
    Convert suitable columns to 'category', 'numeric', and 'datetime' datatypes.
    
    Args:
        df (pd.DataFrame): The input dataframe.
        
    Returns:
        pd.DataFrame: The dataframe with columns converted to appropriate datatypes.
    """
    
    # Convert to 'category'
    # Select columns of type 'object'
    object_columns = df.select_dtypes(include=['object']).columns

    # Calculate the number of unique values for each object column
    unique_counts = df[object_columns].nunique()

    # Identify columns where the ratio of unique values to total rows is less than the threshold
    categorical_columns = unique_counts[unique_counts / len(df) <= threshold].index.tolist()

    for col in categorical_columns:
        df[col] = df[col].astype('category')
    
    # Convert to 'numeric'
    # Assuming numeric columns have 'VL_' prefix or any other identifiable pattern
    numeric_columns = [col for col in df.columns if 'VL_' in col]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convert to 'datetime'
    datetime_columns = [col for col in df.columns if 'DT_' in col]
    for col in datetime_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df

def apply_intel_rules(df, rules):
    """
    Apply a set of intelligent rules to transform a DataFrame based on certain conditions.

    Parameters:
    - df (pd.DataFrame): The input DataFrame to be transformed.
    - rules (list): A list of rules where each rule is a tuple containing a string and a list of conditions.
                    The string defines the new CD_CONTA and DS_CONTA values, and the list contains the conditions.

    Returns:
    - df_web (pd.DataFrame): The transformed DataFrame.

    Example Rule:
    ('6.01.01.09 - Outros', [('conta_startswith', '6.01.01.'), ('conta_level_exact', 4), ('descricao_contains_not', 'forneced')])

    This rule will match rows where CD_CONTA starts with '6.01.01.' and has exactly 4 levels, and DS_CONTA does not contain 'forneced'.
    The matched rows will then have their CD_CONTA set to '6.01.01.09' and DS_CONTA set to 'Outros'.
    """
    
    # Create an empty DataFrame with the same columns as the input DataFrame
    df_web = pd.DataFrame(columns=df.columns)
    
    try:
        # Get the current time to calculate processing duration
        start_time = time.time()

        # Loop through each rule
        for r, (line, conditions) in enumerate(rules):
            # Create a mask initialized to all True values (same length as df)
            mask = pd.Series([True] * len(df))
            line_CD, line_DS = line.split(' - ', 1)

            # Apply each condition in the rule
            for condition, criteria in conditions:
                # Check if condition requires string operations like startswith, contains, etc.
                condition_part = condition.split('_')[1] if '_' in condition else condition

                # Prepare the criteria for string operations
                if condition_part in ["contains", "startswith", "endswith", "contains_not", "startswith_not", "endswith_not"]:
                    if type(criteria) is str:
                        criteria = [criteria]
                    if type(criteria) is tuple:
                        criteria = list(criteria)
                    if condition_part in ["contains", "startswith", "endswith"]:
                        criteria = [word.lower() for word in criteria]
                        criteria_str = '|'.join(criteria)  # Convert to string

                # CD_CONTA criteria
                # Check if the CD_CONTA value is exactly equal to the given criteria
                if condition == 'conta_exact':
                    mask &= df['CD_CONTA'] == criteria

                # Check if the CD_CONTA value starts with the given criteria
                elif condition == 'conta_startswith':
                    mask &= df['CD_CONTA'].str.startswith(criteria_str)

                # Check if the CD_CONTA value ends with the given criteria
                elif condition == 'conta_endswith':
                    mask &= df['CD_CONTA'].str.endswith(criteria_str)

                # Check if the CD_CONTA value contains the given criteria
                elif condition == 'conta_contains':
                    mask &= df['CD_CONTA'].str.contains(criteria_str)

                # Check if the CD_CONTA value is not equal to the given criteria
                elif condition == 'conta_exact_not':
                    mask &= df['CD_CONTA'] != criteria

                # Check if the CD_CONTA value does not start with the given criteria
                elif condition == 'conta_startswith_not':
                    mask &= ~df['CD_CONTA'].str.startswith(criteria_str)

                # Check if the CD_CONTA value does not end with the given criteria
                elif condition == 'conta_endswith_not':
                    mask &= ~df['CD_CONTA'].str.endswith(criteria_str)

                # Check if the CD_CONTA value does not contain the given criteria
                elif condition == 'conta_contains_not':
                    mask &= ~df['CD_CONTA'].str.contains(criteria_str)

                # Check if the level of CD_CONTA is greater than or equal to the given criteria
                elif condition == 'conta_level_min':
                    mask &= df['CD_CONTA'].str.count('\.') + 1 >= criteria

                # Check if the level of CD_CONTA is less than or equal to the given criteria
                elif condition == 'conta_level_max':
                    mask &= df['CD_CONTA'].str.count('\.') + 1 <= criteria

                # Check if the level of CD_CONTA is exactly equal to the given criteria
                elif condition == 'conta_level_exact':
                    mask &= df['CD_CONTA'].str.count('\.') + 1 == criteria


                # DS_CONTA criteria
                # Check if the DS_CONTA value is exactly equal to the given criteria
                elif condition == 'descricao_exact':
                    mask &= df['DS_CONTA'] == criteria

                # Check if the DS_CONTA value starts with the given criteria
                elif condition == 'descricao_startswith':
                    mask &= df['DS_CONTA'].str.startswith(criteria_str)

                # Check if the DS_CONTA value ends with the given criteria
                elif condition == 'descricao_endswith':
                    mask &= df['DS_CONTA'].str.endswith(criteria_str)

                # Check if the DS_CONTA value contains the given criteria (case-insensitive)
                elif condition == 'descricao_contains':
                    mask &= df['DS_CONTA'].str.lower().str.contains(criteria_str)

                # Check if the DS_CONTA value is not equal to the given criteria
                elif condition == 'descricao_exact_not':
                    mask &= df['DS_CONTA'] != criteria

                # Check if the DS_CONTA value does not start with the given criteria
                elif condition == 'descricao_startswith_not':
                    mask &= ~df['DS_CONTA'].str.startswith(criteria_str)

                # Check if the DS_CONTA value does not end with the given criteria
                elif condition == 'descricao_endswith_not':
                    mask &= ~df['DS_CONTA'].str.endswith(criteria_str)

                # Check if the DS_CONTA value does not contain the given criteria (case-insensitive)
                elif condition == 'descricao_contains_not':
                    mask &= ~df['DS_CONTA'].str.lower().str.contains(criteria_str)

            # Extract rows matching the mask and modify their CD_CONTA and DS_CONTA values
            matching_rows = df[mask].copy()
            matching_rows['CD_CONTA'] = line_CD
            matching_rows['DS_CONTA'] = line_DS
            matching_rows['CD_CONTA_original'] = df[mask]['CD_CONTA']
            matching_rows['DS_CONTA_original'] = df[mask]['DS_CONTA']
            
            # Append the modified rows to the new DataFrame
            df_web = pd.concat([df_web, matching_rows])

            # Print progress and diagnostics
            print(sys_remaining_time(start_time, len(rules), r), line, 'matching rows', len(matching_rows))
            if len(matching_rows) < 1:
                pass

    # Catch any exception and continue
    except Exception as e:
        pass

    return df_web

def get_rules():
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

    rules = [
        # Conditions for the CD_CONTA Column:
        
        # 1. Exact match for CD_CONTA

        # 2. CD_CONTA starts with a specific value
        # (['Nome do Novo DS_CONTA', [('conta_startswith', 'valor_inicial')]]),
        
        # 3. CD_CONTA ends with a specific value
        # (['Nome do Novo DS_CONTA', [('conta_endswith', 'valor_final')]]),
        
        # 4. CD_CONTA contains a specific value (case-insensitive)
        # (['Nome do Novo DS_CONTA', [('conta_contains', 'texto_a_procurar')]]),
        
        # 5. CD_CONTA does not contain a specific value (case-insensitive)
        # (['Nome do Novo DS_CONTA', [('conta_contains_not', 'texto_a_evitar')]]),
        
        # 6. Minimum number of levels in CD_CONTA (based on '.')
        # (['Nome do Novo DS_CONTA', [('conta_levelmin', 'min_levels')]]),
        
        # 7. Maximum number of levels in CD_CONTA (based on '.')
        # (['Nome do Novo DS_CONTA', [('conta_levelmax', 'max_levels')]]),
        
        # 8. CD_CONTA is in a specified list of values
        # (['Nome do Novo DS_CONTA', [('conta_in_list', ['valor1', 'valor2', 'valor3'])]]),
        
        # 9. CD_CONTA is not in a specified list of values
        # (['Nome do Novo DS_CONTA', [('conta_not_in_list', ['valor1', 'valor2'])]]),
        
        # 10. CD_CONTA matches a specified regular expression
        # (['Nome do Novo DS_CONTA', [('conta_regex', 'expressao_regular_aqui')]]),
        
        # Conditions for the DS_CONTA Column:
        
        # 1. Exact match for DS_CONTA
        # (['Nome do Novo DS_CONTA', [('descricao_exact', 'valor_exato')]]),
        
        # 2. DS_CONTA starts with a specific value
        # (['Nome do Novo DS_CONTA', [('descricao_startswith', 'valor_inicial')]]),
        
        # 3. DS_CONTA ends with a specific value
        # (['Nome do Novo DS_CONTA', [('descricao_endswith', 'valor_final')]]),
        
        # 4. DS_CONTA contains a specific value (case-insensitive)
        # (['Nome do Novo DS_CONTA', [('descricao_contains', 'texto_a_procurar')]]),
        
        # 5. DS_CONTA does not contain a specific value (case-insensitive)
        # (['Nome do Novo DS_CONTA', [('descricao_contains_not', 'texto_a_evitar')]]),
        
        # 6. DS_CONTA is in a specified list of values
        # (['Nome do Novo DS_CONTA', [('descricao_in_list', ['valor1', 'valor2', 'valor3'])]]),
        
        # 7. DS_CONTA is not in a specified list of values
        # (['Nome do Novo DS_CONTA', [('descricao_not_in_list', ['valor1', 'valor2'])]]),
        
        # 8. DS_CONTA matches a specified regular expression
        # (['Nome do Novo DS_CONTA', [('descricao_regex', 'expressao_regular_aqui')]]),



        # Balanço Patrimonial Ativo
		('01 - Ativo Total', [('conta_exact', '1')]),
		('01.01 - Ativo Circulante de Curto Prazo', [('conta_exact', '1.01')]),
		('01.01.01 - Caixa e Disponibilidades de Caixa', [('conta_exact', '1.01.01')]),
		('01.01.02 - Aplicações Financeiras', [('conta_startswith', '1.01.'), ('conta_levelmin', 3), ('conta_levelmax', 3), ('descricao_contains', ['aplica', 'depósito', 'reserv', 'saldo', 'centra', 'interfinanceir', 'crédit']), ('conta_contains_not', ['1.01.01', '1.01.06'])]),
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

        # Balanço Patrimonial Passivo
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

        # Demonstração do Resultado
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

        # Demonstração de Fluxo de Caixa
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

        # Demonstração de Valor Adiconado
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
        ('07.08.05 - Outros', [('conta_exact', '7.08.05')])

    ]

    return rules

def choose_agrupamento(group):
    if 'con' in group['AGRUPAMENTO'].values:
        return group[group['AGRUPAMENTO'] == 'con']
    else:
        return group[group['AGRUPAMENTO'] == 'ind']

def prepare_b3_cvm(b3_cvm):
    columns = ['CNPJ_CIA', 'DENOM_CIA', 'DT_REFER', 'CD_CONTA', 'DS_CONTA', 'VL_CONTA']
    intel_b3 = {}

    try:
        from assets.rules import rules
        rules = get_rules()
        start_time_b3 = time.time()
        for k, (key, df) in enumerate(b3_cvm.items()):
            print(key, sys_remaining_time(start_time_b3, len(b3_cvm), k))
            # Apply the function to each group
            df = df[[item for item in df.columns if item != "ACIONISTAS"]] # remove ACIONISTAS from df
            df = df.groupby(['CNPJ_CIA', 'DT_REFER'], group_keys=False).apply(choose_agrupamento).reset_index(drop=True)
            intel_b3[key] = apply_intel_rules(df, rules)
            intel_b3[key].to_csv(f'{key}_intel.csv')
    except Exception as e:
        print(e)
        pass
    return intel_b3

def process_stock_data(group, acoes):
    company, quarter = group.name
    
    # Filter acoes based on company and quarter
    mask = acoes['DENOM_CIA'] == company
    mask &= acoes['DT_REFER'] == quarter

    # Concatenate and ffill
    return pd.concat([group, acoes[mask]], ignore_index=True).ffill()

def compose_intel(acoes, intel_b3):
    # Process the acoes and return the result
    acoes['Trimestre'] = pd.to_datetime(acoes['Trimestre'], errors='coerce', dayfirst=True)
    acoes['BALANCE_SHEET'] = 'STK'
    column_mapping = {
        'Ações ON': '00.01.01',
        'Ações PN': '00.02.01',
        'Ações ON em Tesouraria': '00.01.02',
        'Ações PN em Tesouraria': '00.02.02'
    }
    acoes = acoes.rename(columns={"Companhia": "DENOM_CIA", "Trimestre": "DT_REFER"})

    acoes = acoes.melt(id_vars=['DENOM_CIA', 'DT_REFER', 'BALANCE_SHEET'], 
                            value_vars=['Ações ON', 'Ações PN', 'Ações ON em Tesouraria', 'Ações PN em Tesouraria'],
                            var_name='DS_CONTA', value_name='VL_CONTA').sort_values(by=['DENOM_CIA', 'DT_REFER', 'DS_CONTA'])

    acoes['CD_CONTA'] = acoes['DS_CONTA'].map(column_mapping)
    intelacoes = {}

    start_time = time.time()
    for i, (setor, df) in enumerate(intel_b3.items()):
        df = df.groupby(['DENOM_CIA', 'DT_REFER']).apply(process_stock_data, acoes=acoes).reset_index(drop=True)
        intelacoes[setor] = df

        intelacoes[setor].to_pickle(f'{setor}_intelacoes.pkl')

        print(sys_remaining_time(start_time, len(intel_b3), i), setor)
    return intelacoes

def calculate_fund(rules_fund, sheet, company, quarter):
    rows = []
    try:
        for i, data in enumerate(rules_fund):
            vl = 0
            sh, cd, ds, operation, items = data
            if operation == 'add':
                vl = sheet[sheet['CD_CONTA'].isin(list(items))]['VL_CONTA'].sum()

            elif operation == 'sub':
                minuend = sheet[sheet['CD_CONTA'] == items[0]]['VL_CONTA'].sum()
                subtrahend = sheet[sheet['CD_CONTA'] == items[1]]['VL_CONTA'].sum()
                vl = minuend - subtrahend

            elif operation == 'div':
                dividend = sheet[sheet['CD_CONTA'] == items[0]]['VL_CONTA'].sum()
                divisor = sheet[sheet['CD_CONTA'] == items[1]]['VL_CONTA'].sum()
                # vl = dividend / divisor
                vl = dividend / divisor if divisor != 0 and not pd.isna(dividend) and not pd.isna(divisor) else np.nan

            elif operation == 'pct':
                dividend = sheet[sheet['CD_CONTA'] == items[0]]['VL_CONTA'].sum()
                divisor = sheet[sheet['CD_CONTA'] == items[1]]['VL_CONTA'].sum()
                # vl = dividend / divisor
                vl = 100 * dividend / divisor if divisor != 0 and not pd.isna(dividend) and not pd.isna(divisor) else np.nan

            elif operation == 'mul':
                vl = sheet[sheet['CD_CONTA'].isin(list(items))]['VL_CONTA'].prod()

            row = [company, quarter, sh, cd, ds, vl]
            rows.append(row)

    except Exception as e:
        pass
    return rows

def get_rules_fund():
    rules = [
        ('EQT', '11.01.01', 'Capital de Giro (Ativos Circulantes - Passivos Circulantes)', 'sub', ('01.01', '02.01')), 
        ('EQT', '11.01.02', 'Liquidez (Ativos Circulantes por Passivos Circulantes)', 'pct', ('01.01', '02.01')), 
        ('EQT', '11.01.03', 'Ativos Circulantes de Curto Prazo por Ativos', 'pct', ('01.01', '01')),
        ('EQT', '11.01.04', 'Ativos Não Circulantes de Longo Prazo por Ativos', 'pct', ('01.02', '01')), 
        ('EQT', '11.02', 'Passivos por Ativos', 'pct', ('02', '01')),
        ('EQT', '11.02.01', 'Passivos Circulantes de Curto Prazo por Ativos', 'pct', ('02.01', '01')),
        ('EQT', '11.02.02', 'Passivos Não Circulantes de Longo Prazo por Ativos', 'pct', ('02.02', '01')),
        ('EQT', '11.02.03', 'Passivos Circulantes de Curto Prazo por Passivos', 'pct', ('02.01', '02')),
        ('EQT', '11.02.04', 'Passivos Não Circulantes de Longo Prazo por Passivos', 'pct', ('02.02', '02')),
        ('EQT', '11.03', 'Patrimônio Líquido por Ativos', 'pct', ('02.03', '01')),
        ('EQT', '11.03.01', 'Equity Multiplier (Ativos por Patrimônio Líquido)', 'pct', ('01', '02.03')),
        ('EQT', '11.03.02', 'Passivos por Patrimônio Líquido', 'pct', ('02', '02.03')),
        ('EQT', '11.03.02.01', 'Passivos Circulantes de Curto Prazo por Patrimônio Líquido', 'pct', ('02.01', '02.03')),
        ('EQT', '11.03.02.02', 'Passivos Não Circulantes de Longo Prazo por Patrimônio Líquido', 'pct', ('02.02', '02.03')),
        ('EQT', '11.03.03', 'Soma das Reservas do Patrimônio Líquido', 'add', ('02.03.02', '02.03.03', '02.03.04')), 
        ('EQT', '11.03.04', 'Patrimônio Imobilizado', 'add', ('01.02.02', '01.02.03', '01.02.04')), 
        ('EQT', '11.03.05', 'Remuneração do Capital Total(Terceiros + Próprio)', 'add', ('07.08.03', '07.08.04')), 

        ('EQT', '11.04', 'Capital Social por Patrimônio Líquido', 'pct', ('02.03.01', '02.03')),

        ('EQT', '12.01.01', 'Caixa', 'add', ('01.01.01', )), 

        ('PFT', '12.03.01', 'Contas a Receber Não Circulantes de Curto Prazo por Faturamento', 'pct', ('01.01.03', '03.01')), 
        ('PFT', '12.03.02', 'Contas a Receber Circulantes de Longo Prazo Prazo por Faturamento', 'pct', ('01.02.01.03', '03.01')), 
        ('PFT', '13.04.01', 'Estoques Não Circulantes de Curto Prazo por Faturamento', 'pct', ('01.01.04', '03.01')),
        ('PFT', '13.04.02', 'Estoques Circulantes de Longo Prazo por Faturamento', 'pct', ('01.02.01.04', '03.01')),
        ('PFT', '13.05.01', 'Ativos Biológicos Não Circulantes de Curto Prazo por Faturamento', 'pct', ('01.01.05', '03.01')),
        ('PFT', '13.05.02', 'Ativos Biológicos Circulantes de Longo Prazo por Faturamento', 'pct', ('01.02.01.05', '03.01')),
        ('EQT', '13.06.01', 'Tributos Não Circulantes de Curto Prazo por Faturamento', 'pct', ('01.01.06', '03.01')),
        ('EQT', '13.06.02', 'Tributos Circulantes de Longo Prazo por Faturamento', 'pct', ('01.02.01.06', '03.01')),
        ('EQT', '13.07.01', 'Despesas Não Circulantes de Curto Prazo por Faturamento', 'pct', ('01.01.07', '03.01')),
        ('EQT', '13.07.02', 'Despesas Circulantes de Longo Prazo por Faturamento', 'pct', ('01.02.01.07', '03.01')),
        ('EQT', '13.09.01', 'Outros Ativos Não Circulantes de Curto Prazo por Faturamento', 'pct', ('01.01.09', '03.01')),
        ('EQT', '13.09.02', 'Outros Ativos Não Circulantes de Longo Prazo por Faturamento', 'pct', ('01.02.01.09', '03.01')),

        ('PFT', '14.01.01', 'Receita por Ativos', 'pct', ('03.01', '01')),
        ('PFT', '14.01.02', 'Receita por Patrimônio', 'pct', ('03.01', '02.03')),
        ('PFT', '14.02.01', 'Coeficiente de Retorno (Resultado por Ativos)', 'pct', ('03.11', '01')),
        ('PFT', '14.04.01', 'ROE (Resultado por Patrimônio)', 'pct', ('03.11', '02.03')),
        ('PFT', '14.05.01', 'ROAS (EBIT por Ativos)', 'pct', ('03.05', '01')),

        ('EQT', '15.01.01.01', 'Juros Pagos por Remuneração de Capital de Terceiros', 'pct', ('07.08.03.01', '07.08.03')),
        ('EQT', '15.01.01.02', 'Aluguéis por Remuneração de Capital de Terceiros', 'pct', ('07.08.03.02', '07.08.03')),
        ('EQT', '15.01.02.01', 'Juros Pagos por Remuneração de Capital Próprio', 'pct', ('07.08.04.01', '07.08.04')),
        ('EQT', '15.01.02.02', 'Dividendos por Remuneração de Capital Próprio', 'pct', ('07.08.04.02', '07.08.04')),
        ('EQT', '15.01.02.03', 'Lucros Retidos por Remuneração de Capital Próprio', 'pct', ('07.08.04.03', '07.08.04')),
        ('EQT', '15.02.01', 'Impostos por EBIT', 'pct', ('03.08', '03.05')),

        ('PFT', '16.01', 'Margem Bruta (Resultado Bruto (Receita Líquida) por Receita Bruto)', 'pct', ('03.03', '03.01')),
        ('PFT', '16.02', 'Margem Operacional (Receitas Operacionais por Receita Bruta)', 'pct', ('03.04', '03.01')),
        ('PFT', '16.02.01', 'Força de Vendas (Despesas com Vendas por Despesas Operacionais)', 'pct', ('03.04.01', '03.04')),
        ('PFT', '16.02.02', 'Peso Administrativo (Despesas com Administração por Despesas Operacionais)', 'pct', ('03.04.02', '03.04')),
        ('PFT', '16.03.01', 'Margem EBIT (EBIT por Resultado Bruto (Receita Líquida))', 'pct', ('03.05', '03.03')),
        ('PFT', '16.03.02', 'Margem de Depreciação por Resultado Bruto (Receita Líquida)', 'pct', ('07.04.01', '03.03')),
        ('PFT', '16.04', 'Margem Não Operacional (Resultado Não Operacional por Resultado Bruto (Receita Líquida))', 'pct', ('03.06', '03.03')),
        ('PFT', '16.05', 'Margem Líquida (Lucro Líquido por Receita Bruta)', 'pct', ('03.11', '03.01')),

        ('PFT', '18.01', 'Margem de Vendas por Valor Agregado', 'pct', ('07.01.01', '07.07')),
        ('PFT', '18.02', 'Custo dos Insumos por Valor Agregado', 'pct', ('07.02', '07.07')),
        ('PFT', '18.03', 'Valor Adicionado Bruto por Valor Agregado', 'pct', ('07.03', '07.07')),
        ('PFT', '18.04', 'Retenções por Valor Agregado', 'pct', ('07.04', '07.07')),
        ('PFT', '18.05', 'Valor Adicionado Líquido por Valor Agregado', 'pct', ('07.05', '07.07')),
        ('PFT', '18.06', 'Valor Adicionado em Transferência por Valor Agregado', 'pct', ('07.06', '07.07')),
        ('PFT', '18.07', 'Recursos Humanos por Valor Agregado', 'pct', ('07.08.01', '07.07')),
        ('PFT', '18.07.01', 'Remuneração Direta (Recursos Humanos) por Valor Agregado', 'pct', ('07.08.01.01', '07.07')),
        ('PFT', '18.07.02', 'Benefícios (Recursos Humanos) por Valor Agregado', 'pct', ('07.08.01.02', '07.07')),
        ('PFT', '18.07.03', 'FGTS (Recursos Humanos) por Valor Agregado', 'pct', ('07.08.01.03', '07.07')),
        ('PFT', '18.08', 'Impostos por Valor Agregado', 'pct', ('07.08.02', '07.07')),
        ('PFT', '18.09', 'Remuneração de Capital de Terceiros por Valor Agregado', 'pct', ('07.08.03', '07.07')),
        ('PFT', '18.09.01', 'Juros Pagos a Terceiros por Valor Agregado', 'pct', ('07.08.03.01', '07.07')),
        ('PFT', '18.09.02', 'Aluguéis Pagos a Terceiros por Valor Agregado', 'pct', ('07.08.03.02', '07.07')),
        ('PFT', '18.10', 'Remuneração de Capital Próprio por Valor Agregado', 'pct', ('07.08.04', '07.07')),
        ('PFT', '18.10.01', 'Juros Sobre Capital Próprio por Valor Agregado', 'pct', ('07.08.04.01', '07.07')),
        ('PFT', '18.10.02', 'Dividendos por Valor Agregado', 'pct', ('07.08.04.02', '07.07')),
        ('PFT', '18.10.02', 'Lucros Retidos por Valor Agregado', 'pct', ('07.08.04.03', '07.07')),
        ('PFT', '18.11.01', 'Alíquota de Impostos (Impostos, Taxas e Contribuições por Receita Bruta)', 'pct', ('07.08.02', '03.01')),
        ('PFT', '18.11.02', 'Taxa de Juros Pagos (Remuneração de Capital de Terceiros por Receita Bruta)', 'pct', ('07.08.03', '03.01')),
        ('PFT', '18.11.03', 'Taxa de Proventos Gerados (Remuneração de Capital Próprio por Receita Bruta)', 'pct', ('07.08.04', '03.01')),
    ]
    return rules

def get_sheet_data(sheet):
    sheet_data = {}
    try:
        sheet_data['curto_prazo_moeda_nacional'] = sheet[sheet['CD_CONTA'] == '02.01.04.01.01']['VL_CONTA'].sum()
        sheet_data['curto_prazo_moeda_estrangeira'] = sheet[sheet['CD_CONTA'] == '02.01.04.01.02']['VL_CONTA'].sum()
        sheet_data['curto_prazo_debentures'] = sheet[sheet['CD_CONTA'] == '02.01.04.02']['VL_CONTA'].sum()
        sheet_data['curto_prazo_arrendamentos'] = sheet[sheet['CD_CONTA'] == '02.01.04.03']['VL_CONTA'].sum()
        sheet_data['curto_prazo_outros'] = sheet[sheet['CD_CONTA'] == '02.01.04.09']['VL_CONTA'].sum()

        sheet_data['longo_prazo_moeda_nacional'] = sheet[sheet['CD_CONTA'] == '02.02.01.01.01']['VL_CONTA'].sum()
        sheet_data['longo_prazo_moeda_estrangeira'] = sheet[sheet['CD_CONTA'] == '02.02.01.01.02']['VL_CONTA'].sum()
        sheet_data['longo_prazo_debentures'] = sheet[sheet['CD_CONTA'] == '02.02.01.02']['VL_CONTA'].sum()
        sheet_data['longo_prazo_arrendamentos'] = sheet[sheet['CD_CONTA'] == '02.02.01.03']['VL_CONTA'].sum()
        sheet_data['longo_prazo_outros'] = sheet[sheet['CD_CONTA'] == '02.02.02.09']['VL_CONTA'].sum()

        sheet_data['caixa'] = sheet[sheet['CD_CONTA'] == '01.01.01']['VL_CONTA'].sum()

        # Patrimônio e Reservas
        sheet_data['reservas_de_capital'] = sheet[sheet['CD_CONTA'] == '02.03.02']['VL_CONTA'].sum()
        sheet_data['reservas_de_reavaliacao'] = sheet[sheet['CD_CONTA'] == '02.03.03']['VL_CONTA'].sum()
        sheet_data['reservas_de_lucros'] = sheet[sheet['CD_CONTA'] == '02.03.04']['VL_CONTA'].sum()
        sheet_data['patrimonio'] = sheet[sheet['CD_CONTA'] == '02.03']['VL_CONTA'].sum()
        sheet_data['investimentos_nao_capex'] = sheet[sheet['CD_CONTA'] == '01.02.02']['VL_CONTA'].sum()
        sheet_data['imobilizados'] = sheet[sheet['CD_CONTA'] == '01.02.03']['VL_CONTA'].sum()
        sheet_data['intangivel'] = sheet[sheet['CD_CONTA'] == '01.02.04']['VL_CONTA'].sum()
        sheet_data['patrimonio_imobilizado'] = sheet_data['investimentos_nao_capex'] + sheet_data['imobilizados'] + sheet_data['intangivel']

        # Operational
        sheet_data['ebit'] = sheet[sheet['CD_CONTA'] == '03.05']['VL_CONTA'].sum()
        sheet_data['da'] = sheet[sheet['CD_CONTA'] == '07.04.01']['VL_CONTA'].sum()
        sheet_data['receita'] = sheet[sheet['CD_CONTA'] == '03.01']['VL_CONTA'].sum()
        sheet_data['receita_liquida'] = sheet[sheet['CD_CONTA'] == '03.03']['VL_CONTA'].sum()
        sheet_data['resultado'] = sheet[sheet['CD_CONTA'] == '03.11']['VL_CONTA'].sum()
        sheet_data['contas_curto_prazo'] = sheet[sheet['CD_CONTA'] == '01.01.03']['VL_CONTA'].sum()
        sheet_data['contas_longo_prazo'] = sheet[sheet['CD_CONTA'] == '01.02.01.03']['VL_CONTA'].sum()
        sheet_data['estoque_curto_prazo'] = sheet[sheet['CD_CONTA'] == '01.01.04']['VL_CONTA'].sum()
        sheet_data['estoque_longo_prazo'] = sheet[sheet['CD_CONTA'] == '01.02.01.04']['VL_CONTA'].sum()
        sheet_data['biologico_curto_prazo'] = sheet[sheet['CD_CONTA'] == '01.01.05']['VL_CONTA'].sum()
        sheet_data['biologico_longo_prazo'] = sheet[sheet['CD_CONTA'] == '01.02.01.05']['VL_CONTA'].sum()
        sheet_data['tributos_curto_prazo'] = sheet[sheet['CD_CONTA'] == '01.01.06']['VL_CONTA'].sum()
        sheet_data['tributos_longo_prazo'] = sheet[sheet['CD_CONTA'] == '01.02.01.06']['VL_CONTA'].sum()
        sheet_data['despesas_curto_prazo'] = sheet[sheet['CD_CONTA'] == '01.01.07']['VL_CONTA'].sum()
        sheet_data['despesas_longo_prazo'] = sheet[sheet['CD_CONTA'] == '01.02.01.07']['VL_CONTA'].sum()
        sheet_data['outros_curto_prazo'] = sheet[sheet['CD_CONTA'] == '01.01.09']['VL_CONTA'].sum()
        sheet_data['outros_longo_prazo'] = sheet[sheet['CD_CONTA'] == '01.02.01.09']['VL_CONTA'].sum()

        # Caixa
        sheet_data['caixa_operacoes'] = sheet[sheet['CD_CONTA'] == '06.01']['VL_CONTA'].sum()
        sheet_data['caixa_investimentos_capex'] = sheet[sheet['CD_CONTA'] == '06.02']['VL_CONTA'].sum()
        sheet_data['caixa_financiamentos'] = sheet[sheet['CD_CONTA'] == '06.03']['VL_CONTA'].sum()
        sheet_data['caixa_investimentos'] = sheet[sheet['CD_CONTA'] == '06.02.01']['VL_CONTA'].sum()
        sheet_data['caixa_imobilizado_intangivel'] = sheet[sheet['CD_CONTA'] == '06.02.02']['VL_CONTA'].sum()
        sheet_data['caixa_livre'] = sheet_data['caixa_operacoes'] + sheet_data['caixa_investimentos_capex']
        sheet_data['caixa_total'] = sheet_data['caixa_operacoes'] + sheet_data['caixa_investimentos_capex'] + sheet_data['caixa_financiamentos']
        sheet_data['caixa_imobilizado'] = sheet_data['caixa_financiamentos'] + sheet_data['caixa_imobilizado_intangivel']

        # Remuneração de capital
        sheet_data['remuneracao_capital_terceiros'] = sheet[sheet['CD_CONTA'] == '07.08.03']['VL_CONTA'].sum()
        sheet_data['remuneracao_capital_proprio'] = sheet[sheet['CD_CONTA'] == '07.08.03']['VL_CONTA'].sum()
        sheet_data['dividendos_obrigatorios'] = sheet[sheet['CD_CONTA'] == '08.01']['VL_CONTA'].sum()

        # Calculations
        sheet_data['ebitda'] = sheet_data['ebit'] + sheet_data['da']

        sheet_data['divida_bruta_curto_prazo'] = sheet_data['curto_prazo_moeda_nacional'] + sheet_data['curto_prazo_moeda_estrangeira'] + sheet_data['curto_prazo_debentures'] + sheet_data['curto_prazo_arrendamentos'] + sheet_data['curto_prazo_outros']
        sheet_data['divida_bruta_longo_prazo'] = sheet_data['longo_prazo_moeda_nacional'] + sheet_data['longo_prazo_moeda_estrangeira'] + sheet_data['longo_prazo_debentures'] + sheet_data['longo_prazo_arrendamentos'] + sheet_data['longo_prazo_outros']
        sheet_data['divida_bruta'] = sheet_data['divida_bruta_curto_prazo'] + sheet_data['divida_bruta_longo_prazo']
        sheet_data['divida_moeda_estrangeira'] = sheet_data['curto_prazo_moeda_estrangeira'] + sheet_data['longo_prazo_moeda_estrangeira']
        sheet_data['divida_moeda_nacional'] = (sheet_data['divida_bruta_curto_prazo'] + sheet_data['divida_bruta_longo_prazo']) - sheet_data['divida_moeda_estrangeira']
        sheet_data['divida_liquida'] = -1 * (sheet_data['divida_bruta'] - sheet_data['caixa'])
        sheet_data['divida_liquida_resultado'] = sheet_data['divida_liquida'] / sheet_data['resultado'] if sheet_data['resultado'] != 0 and not pd.isna(sheet_data['divida_liquida']) and not pd.isna(sheet_data['resultado']) else np.nan

        sheet_data['endividamento_financeiro'] = sheet_data['divida_bruta'] / sheet_data['patrimonio'] if sheet_data['patrimonio'] != 0 and not pd.isna(sheet_data['divida_bruta']) and not pd.isna(sheet_data['patrimonio']) else np.nan
        sheet_data['patrimonio_imobilizado_por_patrimonio'] = sheet_data['patrimonio_imobilizado'] / sheet_data['patrimonio'] if sheet_data['patrimonio'] != 0 and not pd.isna(sheet_data['patrimonio_imobilizado']) and not pd.isna(sheet_data['patrimonio']) else np.nan
        sheet_data['divida_liquida_por_ebitda'] = sheet_data['divida_liquida'] / sheet_data['ebitda'] if sheet_data['ebitda'] != 0 and not pd.isna(sheet_data['divida_liquida']) and not pd.isna(sheet_data['ebitda']) else np.nan

        sheet_data['contas_faturamento'] = (sheet_data['contas_curto_prazo'] + sheet_data['contas_longo_prazo']) / sheet_data['receita'] if sheet_data['receita'] != 0 and not pd.isna(sheet_data['contas_curto_prazo']) and not pd.isna(sheet_data['contas_longo_prazo']) and not pd.isna(sheet_data['receita']) else np.nan
        sheet_data['estoques_faturamento'] = (sheet_data['estoque_curto_prazo'] + sheet_data['estoque_longo_prazo']) / sheet_data['receita'] if sheet_data['receita'] != 0 and not pd.isna(sheet_data['estoque_curto_prazo']) and not pd.isna(sheet_data['estoque_longo_prazo']) and not pd.isna(sheet_data['receita']) else np.nan
        sheet_data['ativos_biologicos_faturamento'] = (sheet_data['biologico_curto_prazo'] + sheet_data['biologico_longo_prazo']) / sheet_data['receita'] if sheet_data['receita'] != 0 and not pd.isna(sheet_data['biologico_curto_prazo']) and not pd.isna(sheet_data['biologico_longo_prazo']) and not pd.isna(sheet_data['receita']) else np.nan
        sheet_data['tributos_faturamento'] = (sheet_data['tributos_curto_prazo'] + sheet_data['tributos_longo_prazo']) / sheet_data['receita'] if sheet_data['receita'] != 0 and not pd.isna(sheet_data['tributos_curto_prazo']) and not pd.isna(sheet_data['tributos_longo_prazo']) and not pd.isna(sheet_data['receita']) else np.nan
        sheet_data['despesas_faturamento'] = (sheet_data['despesas_curto_prazo'] + sheet_data['despesas_longo_prazo']) / sheet_data['receita'] if sheet_data['receita'] != 0 and not pd.isna(sheet_data['despesas_curto_prazo']) and not pd.isna(sheet_data['despesas_longo_prazo']) and not pd.isna(sheet_data['receita']) else np.nan
        sheet_data['outros_faturamento'] = (sheet_data['outros_curto_prazo'] + sheet_data['outros_longo_prazo']) / sheet_data['receita'] if sheet_data['receita'] != 0 and not pd.isna(sheet_data['outros_curto_prazo']) and not pd.isna(sheet_data['outros_longo_prazo']) and not pd.isna(sheet_data['receita']) else np.nan

        sheet_data['reservas'] = sheet_data['reservas_de_capital'] + sheet_data['reservas_de_reavaliacao'] + sheet_data['reservas_de_lucros']
        if sheet_data['patrimonio'] != 0 and not pd.isna(sheet_data['reservas_de_capital']) and not pd.isna(sheet_data['patrimonio']):
            sheet_data['reservas_patrimonio'] = sheet_data['reservas_de_capital'] / sheet_data['patrimonio']
        else:
            sheet_data['reservas_patrimonio'] = np.nan
        sheet_data['divida_bruta_por_patrimonio'] = sheet_data['divida_bruta'] / sheet_data['patrimonio'] if sheet_data['patrimonio'] != 0 and not pd.isna(sheet_data['divida_bruta']) and not pd.isna(sheet_data['patrimonio']) else np.nan

        sheet_data['remuneracao_capital'] = sheet_data['remuneracao_capital_terceiros'] + sheet_data['remuneracao_capital_proprio']

        sheet_data['roic'] = sheet_data['resultado'] / sheet_data['patrimonio'] if sheet_data['patrimonio'] != 0 and not pd.isna(sheet_data['resultado']) and not pd.isna(sheet_data['patrimonio']) else np.nan
        sheet_data['rem_cap_terceiros_por_rem_cap'] = sheet_data['remuneracao_capital_terceiros'] / sheet_data['remuneracao_capital'] if sheet_data['remuneracao_capital'] != 0 and not pd.isna(sheet_data['remuneracao_capital_terceiros']) and not pd.isna(sheet_data['remuneracao_capital']) else np.nan
        sheet_data['rem_cap_proprio_por_rem_cap'] = sheet_data['remuneracao_capital_proprio'] / sheet_data['remuneracao_capital'] if sheet_data['remuneracao_capital'] != 0 and not pd.isna(sheet_data['remuneracao_capital_proprio']) and not pd.isna(sheet_data['remuneracao_capital']) else np.nan
        sheet_data['rem_cap_por_ebit'] = sheet_data['remuneracao_capital'] / sheet_data['ebit'] if sheet_data['ebit'] != 0 and not pd.isna(sheet_data['remuneracao_capital']) and not pd.isna(sheet_data['ebit']) else np.nan

        sheet_data['margem_ebitda'] = sheet_data['ebitda'] / sheet_data['receita_liquida'] if sheet_data['receita_liquida'] != 0 and not pd.isna(sheet_data['ebitda']) and not pd.isna(sheet_data['receita_liquida']) else np.nan
        sheet_data['margem_ebit'] = sheet_data['ebit'] / sheet_data['receita_liquida'] if sheet_data['receita_liquida'] != 0 and not pd.isna(sheet_data['ebit']) and not pd.isna(sheet_data['receita_liquida']) else np.nan

        sheet_data['caixa_investimentos_por_operacoes'] = sheet_data['caixa_investimentos'] / sheet_data['caixa_operacoes'] if sheet_data['caixa_operacoes'] != 0 and not pd.isna(sheet_data['caixa_investimentos']) and not pd.isna(sheet_data['caixa_operacoes']) else np.nan
        sheet_data['caixa_investimentos_por_ebit'] = sheet_data['caixa_investimentos'] / sheet_data['ebit'] if sheet_data['ebit'] != 0 and not pd.isna(sheet_data['caixa_investimentos']) and not pd.isna(sheet_data['ebit']) else np.nan
    except Exception as e:
        pass
    return sheet_data

def append_rows(sheet, rows, company, quarter):
    try:
        sheet_data = get_sheet_data(sheet)

        rows.append([company, quarter, 'EQT', '11.04.01', 'Reservas do Patrimônio', sheet_data['reservas']])
        rows.append([company, quarter, 'EQT', '11.04.02', 'Reservas por Patrimônio', sheet_data['reservas_patrimonio']])
        
        rows.append([company, quarter, 'DBT', '12.01.01', 'Caixa', sheet_data['caixa']])
        rows.append([company, quarter, 'DBT', '12.01.02', 'Dívida Bruta', sheet_data['divida_bruta']])
        rows.append([company, quarter, 'DBT', '12.01.03', 'Dívida Líquida', sheet_data['divida_liquida']])
        rows.append([company, quarter, 'DBT', '12.01.02.01', 'Dívida Bruta Circulante de Curto Prazo', sheet_data['divida_bruta_curto_prazo']])
        rows.append([company, quarter, 'DBT', '12.01.02.02', 'Dívida Bruta Não Circulante de Longo Prazo Prazo', sheet_data['divida_bruta_longo_prazo']])
        rows.append([company, quarter, 'DBT', '12.01.02.03', 'Dívida Bruta em Moeda Nacional', sheet_data['divida_moeda_nacional']])
        rows.append([company, quarter, 'DBT', '12.01.02.04', 'Dívida Bruta em Moeda Estrangeira', sheet_data['divida_moeda_estrangeira']])
        rows.append([company, quarter, 'EQT', '12.02.01', 'Dívida Bruta por Patrimônio Líquido', sheet_data['divida_bruta_por_patrimonio']])
        rows.append([company, quarter, 'DBT', '12.02.02', 'Endividamento Financeiro', sheet_data['endividamento_financeiro']])
        rows.append([company, quarter, 'EQT', '12.03.01', 'Patrimônio Imobilizado em Capex, Investimentos Não Capex e Intangível Não Capex', sheet_data['patrimonio_imobilizado']])
        rows.append([company, quarter, 'EQT', '12.03.02', 'Patrimônio Imobilizado por Patrimônio', sheet_data['patrimonio_imobilizado_por_patrimonio']])
        rows.append([company, quarter, 'PFT', '12.04.01', 'Dívida Líquida por EBITDA', sheet_data['divida_liquida_por_ebitda']])

        rows.append([company, quarter, 'PFT', '13.01', 'LAJIDA EBITDA Resultado Antes do Resultado Financeiro e dos Tributos mais Depreciação e Amortização', sheet_data['ebitda']])
        rows.append([company, quarter, 'PFT', '13.03', 'Contas por Faturamento', sheet_data['contas_faturamento']])
        rows.append([company, quarter, 'PFT', '13.04', 'Estoques por Faturamento', sheet_data['estoques_faturamento']])
        rows.append([company, quarter, 'PFT', '13.05', 'Ativos Biológicos por Faturamento', sheet_data['ativos_biologicos_faturamento']])
        rows.append([company, quarter, 'PFT', '13.06', 'Tributos por Faturamento', sheet_data['tributos_faturamento']])
        rows.append([company, quarter, 'PFT', '13.07', 'Despesas por Faturamento', sheet_data['despesas_faturamento']])
        rows.append([company, quarter, 'PFT', '13.09', 'Outros por Faturamento', sheet_data['outros_faturamento']])

        rows.append([company, quarter, 'EQT', '14.03', 'Capital Investido', sheet_data['patrimonio']])
        rows.append([company, quarter, 'EQT', '14.03.01', 'ROIC (Retorno por Capital Investido)', sheet_data['roic']])
        
        rows.append([company, quarter, 'EQT', '15.01', 'Remuneração de Capital', sheet_data['remuneracao_capital']])
        rows.append([company, quarter, 'EQT', '15.01.01', 'Remuneração de Capital de Terceiros por Remuneração de Capital', sheet_data['rem_cap_terceiros_por_rem_cap']])
        rows.append([company, quarter, 'EQT', '15.01.02', 'Remuneração de Capital Próprio por Remuneração de Capital', sheet_data['rem_cap_proprio_por_rem_cap']])
        rows.append([company, quarter, 'EQT', '15.02', 'Remuneração de Capital por EBIT', sheet_data['rem_cap_por_ebit']])
        
        rows.append([company, quarter, 'EQT', '16.03', 'Margem EBITDA (EBITDA por Resultado Bruto (Receita Líquida)', sheet_data['margem_ebitda']])
        rows.append([company, quarter, 'EQT', '16.03.01', 'Margem EBIT (EBIT por Resultado Bruto (Receita Líquida)', sheet_data['margem_ebit']])

        rows.append([company, quarter, 'CSH', '17.01', 'Caixa Livre', sheet_data['caixa_livre']])
        rows.append([company, quarter, 'CSH', '17.02', 'Caixa Total', sheet_data['caixa_total']])
        rows.append([company, quarter, 'CSH', '17.03', 'Caixa de Investimentos', sheet_data['caixa_investimentos']])
        rows.append([company, quarter, 'CSH', '17.03.01', 'Caixa de Investimentos por Caixa das Operações', sheet_data['caixa_investimentos_por_operacoes']])
        rows.append([company, quarter, 'CSH', '17.03.02', 'Caixa de Investimentos por EBIT', sheet_data['caixa_investimentos_por_ebit']])
        rows.append([company, quarter, 'CSH', '17.04', 'Caixa Imobilizado', sheet_data['caixa_imobilizado']])
        rows.append([company, quarter, 'CSH', '17.05', 'FCFF simplificado (Caixa Livre para a Firma)', sheet_data['caixa_operacoes'] - sheet_data['caixa_imobilizado']])
        rows.append([company, quarter, 'CSH', '17.06', 'FCFE simplificado (Caixa Livre para os Acionistas)', sheet_data['caixa_operacoes'] - sheet_data['dividendos_obrigatorios']])

    except Exception as e:
        pass
    return rows

def compose_fund(intelacoes):
    cols = ['DENOM_CIA', 'DT_REFER', 'BALANCE_SHEET', 'CD_CONTA', 'DS_CONTA', 'VL_CONTA']
    rules = get_rules_fund()
    fund = {}

    try:
        start_time = time.time()
        for i, (setor, df) in enumerate(intelacoes.items()):
            df_fund = pd.DataFrame(columns=df.columns)
            sheets = df.groupby(['DENOM_CIA', 'DT_REFER'])
            df_list = []  # Initialize an empty list for the dataframes

            start_time_2 = time.time()
            for j, (key, sheet) in enumerate(sheets):
                company, quarter = key
                rows = calculate_fund(rules, sheet=sheet, company=company, quarter=quarter)
                rows = append_rows(sheet, rows, company, quarter)
                rows = pd.DataFrame(rows, columns=cols)
                
                # Append the combined dataframe to the list
                sheet = pd.concat([sheet, rows]).ffill().drop_duplicates()
                df_list.append(sheet)

                if j% (b3.bin_size * 2) == 0:
                    print(setor, company, sys_remaining_time(start_time_2, len(sheets), j))

            # Concatenate all dataframes in the list
            df_fund = pd.concat([df_fund, pd.concat(df_list, ignore_index=True)], ignore_index=True)
            fund[setor] = df_fund
            df_fund.to_pickle(f'{setor}_fund.pkl')
            print(setor, sys_remaining_time(start_time, len(intelacoes), i))
    except Exception as e:
        pass
    return fund

def load_database():
    """
    This function loads a series of databases in a specific order, with each database potentially
    depending on previous ones. If a database cannot be loaded, it's generated based on its dependencies.
    
    Order & Dependencies:
    1. 'acoes' 
        - Directly loaded or generated using get_composicao_acionaria()
    
    2. 'intelacoes'
        - Depends on: 'acoes' & 'intel_b3'
        - Loaded directly or generated using compose_intel()

    3. 'intel_b3'
        - Depends on: 'b3_cvm'
        - Loaded directly or generated using prepare_b3_cvm()

    4. 'b3_cvm'
        - Depends on: 'company' & 'math'
        - Loaded directly or generated using get_companies()

    5. 'company'
        - Directly loaded or generated using b3_get_companies(b3.search_url)

    6. 'math'
        - Directly loaded or generated using get_math_from_b3_cvm()

    7. 'fund'
        - Depends on: 'intelacoes'
        - Loaded directly or generated using compose_fund()

    Returns:
        fund (dict): The final loaded or generated database.
    """
    Step 1: Load or prepare 'acoes'
    acoes = stk_get_composicao_acionaria()
    # print('fast debug acoes')
    # filename = 'acoes'
    # columns = ['Companhia', 'Trimestre', 'Ações ON', 'Ações PN', 'Ações ON em Tesouraria', 'Ações PN em Tesouraria', 'URL']
    # acoes = sys_read_or_create_dataframe(filename, columns)

    # Step 2: Load or prepare 'fund'
    try:
        fund = sys_load_pkl(f'{b3.app_folder}/fund')
    except Exception as e:
        # Nested step: Load or prepare 'intelacoes'
        try:
            intelacoes = sys_load_pkl(f'{b3.app_folder}/intelacoes')
        except Exception as e:
            # Nested step: Load or prepare 'intel_b3'
            try:
                intel_b3 = sys_load_pkl(f'{b3.app_folder}/intel_b3')
            except Exception as e:
                # Further nested step: Load or prepare 'b3_cvm'
                try:
                    b3_cvm = sys_load_pkl(f'{b3.app_folder}/b3_cvm')
                except Exception as e:
                    # Further nested step: Load or prepare 'company'
                    try:
                        company = b3_get_companies(b3.search_url)
                        # print('fast debug b3_company')
                        # filename = 'company'
                        # b3_cols = b3.cols_b3_companies + b3.col_b3_companies_extra_columns
                        # company = sys_read_or_create_dataframe('company', b3_cols).fillna('')
                    except Exception as e:
                        pass

                    # Further nested step: Load or prepare 'math'
                    try:
                        math = sys_load_pkl(f'{b3.app_folder}/math')
                    except Exception as e:
                        cvm = cvm_get_databases_from_cvm()
                        math = get_math_from_b3_cvm()
                        math = sys_save_pkl(math, f'{b3.app_folder}/math')
                    
                    # Use 'math' and 'company' to prepare 'b3_cvm'
                    b3_cvm = get_companies(math, company)
                    b3_cvm = sys_save_pkl(b3_cvm, f'{b3.app_folder}/b3_cvm')
                
                # Use 'b3_cvm' to prepare 'intel_b3'
                intel_b3 = prepare_b3_cvm(b3_cvm)
                intel_b3 = sys_save_pkl(intel_b3, f'{b3.app_folder}/intel_b3')

            # Use 'intel_b3' to prepare 'intelacoes'
            intelacoes = compose_intel(acoes, intel_b3)
            intelacoes = sys_save_pkl(intelacoes, f'{b3.app_folder}/intelacoes')
        
        # Use 'intelacoes' to prepare 'fund'
        fund = compose_fund(intelacoes)
        fund = sys_save_pkl(fund, f'{b3.app_folder}/fund')



    return fund

def save_sss(df_fund):
    setores = []
    for setor, df in df_fund.items():
        columns=['SETOR', 'SUBSETOR', 'SEGMENTO', 'PREGAO']
        setores.append(df[columns].drop_duplicates())
        print(setor)
    sss = pd.concat(setores)
    sss = sss.applymap(clean_text)

    sss = sys_save_pkl(sss, f'{b3.app_folder}/sss')

    return df_fund

def date_to_unix(date_string, date_format='%Y-%m-%d'):
    """
    Convert a date string to UNIX timestamp.
    
    Parameters:
    - date_string (str): The date string to convert.
    - date_format (str, optional): The format of the date string. Default is '%Y-%m-%d'.
    
    Returns:
    - int: UNIX timestamp representing the input date_string.
    """
    # Parse the input date_string using the specified date_format.
    dt = datetime.datetime.strptime(date_string, date_format)
    
    # Convert the datetime object to a UNIX timestamp (integer).
    unix_timestamp = int(dt.timestamp())
    
    return unix_timestamp

def get_yahoo_quotes(ticker, start_date, end_date=pd.Timestamp.today().strftime('%Y-%m-%d'), country='brazil', interval='1d', events='history', includeAdjustedClose=True):
    '''
    Generate a Yahoo Finance URL for downloading historical stock data.
    
    Parameters:
    - ticker (str or list of str): The stock ticker symbol(s) or a list of symbols.
    - start_date (str): The start date in the format 'YYYY-MM-DD'.
    - end_date (str, optional): The end date in the format 'YYYY-MM-DD'. Defaults to today's date.
    - interval (str, optional): Data interval (e.g., '1d' for daily data). Default is '1d'.
    - events (str, optional): Type of data to request. Default is 'history'.
    - includeAdjustedClose (bool, optional): Whether to include the adjusted close price. Default is True.
    
    Returns:
    - dict: A dictionary of DataFrames containing historical stock data for the specified ticker(s).
    '''
    # Base URL for Yahoo Finance API
    base_url = 'https://query1.finance.yahoo.com/v7/finance/download/'

    # Convert start and end dates to UNIX timestamps
    period1 = date_to_unix(start_date)
    period2 = date_to_unix(end_date)

    # Ensure ticker is a list
    if type(ticker) is str:
        ticker = [ticker]

    quotes = {}  # Dictionary to store historical data for each ticker
    # start_time = run.time.time()
    for i, tick in enumerate(ticker):
        # Append '.SA' to ticker symbol if the country is Brazil
        t = tick + '.SA' if country == 'brazil' else tick

        # Construct the Yahoo Finance URL for the given parameters
        url = f'{base_url}{t}?period1={period1}&period2={period2}&interval={interval}&events={events}&includeAdjustedClose={includeAdjustedClose}'

        try:
            # Read data from the URL into a DataFrame
            df = pd.read_csv(url)
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.set_index('Date')

            # Store the DataFrame in the quotes dictionary
            quotes[tick] = df
            # print(run.sys_remaining_time(start_time, len(ticker), i), tick)
        except Exception as e:
            pass

    return quotes  # Return the dictionary of historical stock data

def yahoo_quotes(fund, quotes, start_date='1970-01-02'):
    '''
    Retrieve historical stock data for a fund's tickers from Yahoo Finance.

    Parameters:
    - fund (dict): A dictionary containing fund data, where keys are sectors and values are DataFrames.
    - start_date (str, optional): The start date for historical data retrieval in the format 'YYYY-MM-DD'. Default is '1970-01-02'.

    Returns:
    - dict: A dictionary of historical stock data for the specified fund's tickers.
    '''
    start_time = time.time()

    # Iterate over sectors and their associated DataFrames in the fund dictionary
    for i, (setor, df) in enumerate(fund.items()):
        # Extract unique ticker information for the sector's DataFrame
        df_tickers = df[['CNPJ_CIA', 'PREGAO', 'TICKERS']].drop_duplicates()
        
        # Clean and split ticker strings into lists if necessary
        df_tickers['TICKERS'] = df_tickers['TICKERS'].apply(lambda x: [item.strip() for item in x.split(',')] if isinstance(x, str) else x)

        start_time_2 = time.time()
        # Iterate over tickers in the sector
        for j, (index, row) in enumerate(df_tickers.iterrows()):
            cnpj, pregao, ticker = row
            try:
                max_date = max(df.index.max() for df in quotes[pregao].values()) + pd.Timedelta(days=1)
                start_date = max(pd.Timestamp(start_date), max_date).strftime('%Y-%m-%d')

                if start_date < pd.Timestamp.today().strftime('%Y-%m-%d'):
                    # Retrieve historical stock data using the get_yahoo_quotes function
                    df_quotes = get_yahoo_quotes(ticker, start_date=start_date)
                    
                    # Store the retrieved data in the quotes dictionary
                    quotes[pregao] = df_quotes
                
                    # Print progress information
                    print(sys_remaining_time(start_time, len(fund), i), setor, sys_remaining_time(start_time_2, len(df_tickers), j), pregao, ', '.join(ticker))
            except Exception as e:
                pass

    return quotes  # Return the dictionary of historical stock data

def quotes_update(fund, quotes, quotes_new):
    '''
    Update existing historical stock data with new data from a second source.

    Parameters:
    - quotes (dict): A dictionary of existing historical stock data.
    - quotes_new (dict): A dictionary of new historical stock data to be merged with the existing data.

    Returns:
    - dict: An updated dictionary of historical stock data.
    '''
    start_time = time.time()
        # Iterate over sectors and their associated DataFrames in the fund dictionary
    for i, (setor, df) in enumerate(fund.items()):
        # Extract unique ticker information for the sector's DataFrame
        df_tickers = df[['CNPJ_CIA', 'PREGAO', 'TICKERS']].drop_duplicates()
        
        # Clean and split ticker strings into lists if necessary
        df_tickers['TICKERS'] = df_tickers['TICKERS'].apply(lambda x: [y.strip() for y in x.split(',')] if isinstance(x, str) else x)
        
        for j, (index, row) in enumerate(df_tickers.iterrows()):
            cnpj, pregao, ticker = row
            if ticker:
                for k, tick in enumerate(ticker):
                    try:
                        # Retrieve the existing and new data for the ticker
                        df1 = quotes[pregao][tick]
                        df2 = quotes_new[pregao][tick]
                        
                        # Concatenate and deduplicate the data
                        df = pd.concat([df1, df2])
                        df = df[~df.index.duplicated(keep='first')]
                        
                        # Update the data in the quotes dictionary
                        quotes[pregao][tick] = df
                    except Exception as e:
                        pass

    return quotes  # Return the updated dictionary of historical stock data

def integrate_yahoo_quotes(fund):
    '''
    Retrieve, update, and save historical stock data for a fund using Yahoo Finance.

    Returns:
    - dict: A dictionary of historical stock data.
    '''
    try:
        # Attempt to load existing quotes from a pickle file
        quotes = sys_load_pkl(f'{b3.app_folder}/quotes')
    except Exception as e:
        # If loading fails, retrieve initial quotes using Yahoo Finance and save them
        no_quotes = {}
        quotes = yahoo_quotes(fund, no_quotes)
        quotes = sys_save_pkl(quotes, f'{b3.app_folder}/quotes')
    
    # Retrieve new quotes from Yahoo Finance starting from the determined start date
    quotes_new = yahoo_quotes(fund, quotes)
    
    # Update existing quotes with the new data
    quotes = quotes_update(fund, quotes, quotes_new)
    
    return quotes  # Return the dictionary of historical stock data

def preprocess_data(df):
    # Convert specific columns to object type and 'DT_REFER' to datetime
    df[['VERSAO', 'CD_CVM']] = df[['VERSAO', 'CD_CVM']].astype('object')
    df['DT_REFER'] = pd.to_datetime(df['DT_REFER'])
    return df

def pivot_data(df):
    # Extract unique combinations of DT_REFER and PREGAO without the account details and get an unique mapping between the dates, PREGAO, and the pivoted account data.
    df_unique = df.reset_index(drop=True).drop_duplicates(subset=['DT_REFER', 'PREGAO']).drop(['CD_CONTA', 'DS_CONTA', 'VL_CONTA'], axis=1)

    # Pivot for CD_CONTA
    df_pivot = df.pivot_table(index=['DT_REFER', 'PREGAO'], 
                              columns=['CD_CONTA', 'DS_CONTA'], 
                              values='VL_CONTA', 
                              aggfunc='sum').reset_index()

    # Flatten the multi-level columns after pivot
    df_pivot.columns = [' - '.join(col).strip(' - ') for col in df_pivot.columns.values]

    df_merge = pd.merge(df_unique, df_pivot, on=['DT_REFER', 'PREGAO'])

    # Set index and handle missing values
    df_merge = df_merge.set_index(['DT_REFER', 'PREGAO'], drop=True)

    return df_merge

def resample_data(df):
    # Group by 'PREGAO' and apply resampling
    df_resampled = (df.reset_index()
                     .groupby('PREGAO')
                     .apply(lambda group: group.set_index('DT_REFER').resample('D').asfreq().ffill().bfill().fillna(0))
                     .drop('PREGAO', axis=1))  # Drop the redundant 'PREGAO' column introduced by `groupby`
    return df_resampled

def merge_with_bigdata(df, bigdata):
    try:
        df = df.reset_index()
    except Exception as e:
        pass
    df['DT_REFER'] = pd.to_datetime(df['DT_REFER'])

    try:
        bigdata = bigdata.reset_index()
    except Exception as e:
        pass
    bigdata['Date'] = pd.to_datetime(bigdata['Date'])
    
    companies = df['PREGAO'].unique()
    filtered_bigdata = bigdata[bigdata['PREGAO'].isin(companies)]

    # choose inner for limited time range, outer for wider time range
    df_merged = pd.merge(filtered_bigdata, df, left_on=['Date', 'PREGAO'], right_on=['DT_REFER', 'PREGAO'], how='inner')

    df_merged = df_merged.sort_values(by=['PREGAO', 'Date'])
    df_merged = df_merged.groupby('PREGAO', group_keys=False).apply(lambda group: group.ffill().bfill()).fillna(0).reset_index(drop=True)

    df_merged = df_merged.set_index('Date', drop=True)

    return df_merged

def cleanup_dataframe(df):
    try:
        # Remove unwanted index
        df = df.drop_duplicates(subset='index', keep='first')
    except Exception as e:
        pass

    try:
        # Remove the columns named 'level_0' and 'index' from the dataframe
        df = df[[col for col in df.columns if col not in ['level_0', 'index']]]
    except Exception as e:
        pass

    try:        
        # Convert the 'VERSAO' and 'CD_CVM' column values
        columns_to_convert = ['VERSAO', 'CD_CVM', 'COLUNA_DF']

        for col in columns_to_convert:
            try:
                df[col] = df[col].astype(int)
            except Exception as e:
                pass
            df[col] = df[col].astype(str)
    except Exception as e:
        pass

    try:
        # Convert the 'DT' columns values to datetime format
        datetime_cols = [col for col in df.columns if col.startswith('DT')]
        df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime)
    except Exception as e:
        pass

    try:
        # Add prefix to the column names
        quote_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        new_cols = {col: f"50.{i:02} - {col}" for i, col in enumerate(quote_cols, start=1)}
        df.rename(columns=new_cols, inplace=True)

        # Identify all columns that start with a digit and convert them to float
        num_cols = [col for col in df.columns if col[0].isdigit()]
        df[num_cols] = df[num_cols].astype('float64')

    except Exception as e:
        pass

    try:
        # Uncommented the conversion to category as it's commented in the original code
        # category_columns = [col for col in df.select_dtypes(include=['object']).columns if "original" not in col.lower()]
        # df[category_columns] = df[category_columns].astype('category')
        pass
    except Exception as e:
        pass

    try:
        # Convert the 'Date' column to datetime format (if it isn't already)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
    except Exception as e:
        pass

    return df

def add_metrics(df):
    # Ensure no division by zero for all columns
    df.replace(0, np.nan, inplace=True)

    # add now df columns and metrics here
    df['00.03.01 - Ações Emitidas'] = df['00.01.01 - Ações ON'] + df['00.02.01 - Ações PN']
    df['00.03.02 - Ações em Tesouraria'] = df['00.01.02 - Ações ON em Tesouraria'] + df['00.02.02 - Ações PN em Tesouraria']
    df['00.04.01 - Ações em Circulação'] = df['00.03.01 - Ações Emitidas'] - df['00.03.02 - Ações em Tesouraria']

    df['51.01.01 - Lucro por Ação'] = df['03.11 - Lucro Líquido'] / df['00.04.01 - Ações em Circulação']
    df['51.01.02 - Valor Patrimonial por Ação'] = df['02.03 - Patrimônio Líquido'] / df['00.04.01 - Ações em Circulação']
    df['51.01.03 - Valor de Mercado (Preço do Total de Ações)'] =  df['50.05 - Adj Close'] * df['00.04.01 - Ações em Circulação']
    df['51.01.04 - Receita por Ação'] = df['03.01 - Receita Bruta'] / df['00.04.01 - Ações em Circulação']
    df['51.01.05 - Valor da Firma (Enterprise Value)'] = df['51.01.03 - Valor de Mercado (Preço do Total de Ações)'] + df['12.01.02 - Dívida Bruta'] - df['01.01.01 - Caixa e Disponibilidades de Caixa']

    df['52.01.01 - Preço do Lucro (P/L)'] = df['50.05 - Adj Close'] / df['51.01.01 - Lucro por Ação']
    df['52.01.02 - Preço do Patrimônio (P/VPA)'] = df['50.05 - Adj Close'] / df['51.01.02 - Valor Patrimonial por Ação']
    df['52.01.03 - Preço do EBIT (Resultado Operacional) (P/EBIT)'] = df['51.01.03 - Valor de Mercado (Preço do Total de Ações)'] / df['03.05 - LAJIR EBIT Resultado Antes do Resultado Financeiro e dos Tributos']
    df['52.01.04 - Preço do FCO (Caixa Operacional) (P/FCO)'] = df['50.05 - Adj Close'] / df['06.01 - Caixa das Operações']
    df['52.01.05 - Preço da Receita (Faturamento Bruto) (PSR)'] = df['50.05 - Adj Close'] / df['51.01.04 - Receita por Ação']

    return df

def merge_quotes(fund, quotes):
    bigdata = []
    try:
        for pregao, d in quotes.items():
            for ticker, df in d.items():
                df['PREGAO'] = pregao  # Set or update 'PREGAO' column
                df['TICKER'] = ticker  # Set or update 'TICKER' column
                bigdata.append(df)
        bigdata = pd.concat(bigdata, ignore_index=False)
    except Exception as e:
        pass

    df_preplot = {}
    try:
        # pivot, merge, resample, cleanup and add metrics
        start_time = time.time()
        for i, (setor, df) in enumerate(fund.items()):
            df = preprocess_data(df) # ok
            df = pivot_data(df)
            df = resample_data(df)
            df = merge_with_bigdata(df, bigdata)
            df = cleanup_dataframe(df)

            df = df.groupby('PREGAO', group_keys=False).apply(add_metrics)

            df_preplot[setor] = df

            print(setor, sys_remaining_time(start_time, len(fund), i))
    except Exception as e:
        pass

    try:
        # Define the path to the folder
        folder_path = os.path.join(b3.app_folder, b3.company_folder)
        if not os.path.exists(folder_path):
            # Create the folder
            os.makedirs(folder_path)
    except Exception as e:
        pass

    try:
        # save per company file (for size and speed)
        start_time = time.time()
        for i, (setor, df) in enumerate(df_preplot.items()):
            companies = df['PREGAO'].unique()
            for i2, company in enumerate(companies):
                mask = df['PREGAO'] == company
                df_temp = df[mask]
                try:
                    df_temp = sys_save_pkl(df_temp, f'{b3.app_folder}/{b3.company_folder}/{company}')
                except Exception as e:
                    pass
            print(setor, sys_remaining_time(start_time, len(df_preplot), i))
    except Exception as e:
        pass

    return df_preplot

# macro
def get_bcb_series():
    pass

# dash
def normalize_data(df, subcolumns):
    """
    Normalize data columns in a dataframe to their percentage of row-wise total.

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe containing data to be normalized.
    subcolumns : list of str
        List of column names to be normalized.

    Returns:
    --------
    normalized_df : pd.DataFrame
        Dataframe with normalized columns.
    """
    # Filter subcolumns to include only columns that actually exist in df
    subcolumns = [col for col in subcolumns if col in df.columns]

    # Make a copy of the specified columns to prevent modifying the original dataframe
    temp_df = df[subcolumns].copy()
    
    # Remove columns where the sum is close to zero
    temp_df = temp_df.loc[:, (temp_df.sum(axis=0) > 1e-10)]

    # Ensure there are no NaN values at the start of the columns
    # [You might adapt this as per your requirement]
    temp_df = temp_df.dropna(subset=temp_df.columns, how='all')
    
    # Calculate the total of the specified columns row-wise
    temp_df['total'] = temp_df.sum(axis=1)

    # Normalize each specified column by its percentage of the row-wise total
    for column in temp_df.columns:
        if column != 'total':
            temp_df[column] = temp_df.apply(
                lambda row: round(row[column] / row['total'] * 100, 2) if row['total'] != 0 else 0, 
                axis=1
            )
        
    # Drop the total column and return the normalized dataframe
    normalized_df = temp_df.drop(columns=['total'])
    
    return normalized_df

def exclude_outliers(item, df, multiplier=1.5):
    """
    Exclude outliers from a data series using 
    the Interquartile Range (IQR) method and a personalized multiplier.

    Parameters:
    -----------
    data_series : pd.Series
        The original data series from which outliers will be excluded.
    multiplier : float
        The multiplier for the IQR. Outliers are defined as values below 
        Q1 - (multiplier * IQR) or above Q3 + (multiplier * IQR).

    Returns:
    --------
    inliers : pd.Series
        The data series with outliers excluded.
    """
    data_series = df[item] if isinstance(item, str) else item

    # Calculate the first (Q1) and third (Q3) quartiles
    Q1 = data_series.quantile(0.25)
    Q3 = data_series.quantile(0.75)
    
    # Calculate the Interquartile Range (IQR)
    IQR = Q3 - Q1
    
    # Define lower and upper bounds for inliers
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    # Identify and return inliers
    inliers = data_series[(data_series > lower_bound) & (data_series < upper_bound)]
    
    return inliers

def cagr(item, df, years=3):
    """
    Calculate the Compound Annual Growth Rate (CAGR) for a given data series.
    
    Parameters:
    -----------
    item : str or pd.Series
        The actual values for which the CAGR will be calculated. 
        Can be a string (column name) or a pandas Series.
    years : int
        The number of years over which the CAGR will be calculated.
    
    Returns:
    --------
    data_series : pd.Series
        The CAGR values.
    """
    # Retrieve the data series from the dataframe if item is a string (column name)
    data_series = df[item] if isinstance(item, str) else item

    # Calculate the CAGR: [ (Ending Value / Beginning Value) ^ (1 / Number of Years) ] - 1
    # Shift the original data series by the number of periods to calculate the growth rate
    data_series = ((data_series / data_series.shift(periods=round(21*12*years))) ** (1/years)) - 1
    
    # Convert CAGR to percentage and smooth (accordingly to year) the series by taking a moving average, and round the series to two decimal places
    data_series = data_series * 100
    data_series = data_series.rolling(window=int(years*4)).mean()
    data_series = data_series.round(2)
    
    # Name it appropriately
    data_series.name = f'CAGR {years}a - {data_series.name.split(" - ")[1]}'

    return data_series

def ofs(item, df, years=3):
    """
    Calculate the Oscillator Following the Stock (OFS) for a given data series.

    Parameters:
    -----------
    data_serie : pd.Series
        The actual values for which the OFS oscillator will be calculated.
    window : int
        The window size for calculating the moving average and standard deviation.

    Returns:
    --------
    ofs : pd.Series
        The OFS oscillator values, smoothed with a moving average.
    """
    data_series = df[item] if isinstance(item, str) else item

    # Calculate the moving average (mma) and standard deviation (std)
    mma = data_series.rolling(window=int(21*12*years)).mean()
    std = data_series.rolling(window=int(21*12*years)).std()
    
    # Define the high and low levels
    high_level = mma + 2 * std
    low_level = mma - 2 * std
    
    # Calculate the OFS oscillator, where +2 std=100 and -2 std=-100
    data_series = ((data_series - low_level) / (high_level - low_level)) * 20 - 10
    
    # Smooth the OFS oscillator with a moving average
    data_series = data_series.rolling(window=int(years*4)).mean()

    # Name the series appropriately
    data_series.name = f'OFS {years}a - {data_series.name.split(" - ")[1]}'

    return data_series

def plot_tweak(plot_info: Dict[str, Any], df: pd.DataFrame) -> go.Figure:
    """
    Generates a custom Plotly figure based on the provided data and visualization options.
    
    Parameters:
    ----------
    df : pd.DataFrame
        The primary data source containing the columns to be plotted.
        
    plot_info : dict
        Contains metadata and various configurations for plotting. The dictionary should have the keys:
        - 'plot_title' : str
            Main title of the plot.
        - 'data' : dict
            Contains column names/series and axis titles for plotting. Sub-keys should be:
            - 'left' : List containing columns or series to be plotted on the left y-axis.
            - 'right' : List containing columns or series to be plotted on the right y-axis.
            - 'axis' : List containing the left y-axis title and right y-axis title.
        - 'options' : dict, optional
            Contains visualization options for left and right data. Each side (left/right) can have:
            - 'shape' : str, optional (default is 'line')
                Shape of the plot, either 'line' or 'area'.
            - 'mode' : str, optional (default is 'standalone')
                Data representation mode, either 'standalone' or 'cumulative'.
            - 'legendgroup' : str, optional
                String to combine legend items into a group.
            - 'normalization' : bool, optional (default is False)
                Indicates if the data should be normalized.
            - 'mma': tuple of (float, float), optional
                Contains values for a moving average and its multiplier for standard deviation. 
                Format is (moving_average_period, standard_deviation_multiplier). None by default.
            - 'outliers': bool, optional (default is False)
                Indicates if outliers should be excluded.
            - 'flexible_range': bool, optional (default is False)
                If True, the max_min range logic is not applied. If False, it is applied.
            - 'range': bool or str, optional (default is False)
                Determines the logic used to set the y-axis bounds:
                - 'flexible': No custom logic, Plotly determines y-axis bounds.
                - False: Upper bound is set to the nearest power of 10 above the maximum data value.
                - 'half': Upper bound is set to the nearest multiple of 5 above the maximum data value.
                - 'full': Upper bound is set to the nearest power of 10 above the maximum data value.
            
    Returns:
    -------
    plotly.graph_objs.Figure
        The generated Plotly figure.
        
    Notes:
    -----
    The 'data' dictionary within 'plot_info' should contain keys for 'left', 'right', and 'axis' to specify data series 
    and axis titles. If 'axis' is not provided, default empty titles are used. 'left' and 'right' should contain lists of 
    column names or Pandas Series objects that represent the data to be plotted on the left and right y-axes, respectively.
    
    The 'options' dictionary within 'plot_info' provides additional configurations for shaping the visual aspects of the plot.
    Different options can be specified for 'left' and 'right' side data.
    """

    def get_data_from_item(item: Union[str, pd.Series], normalize: bool=False, 
                        columns_for_normalization: Optional[List[str]]=None, 
                        exclude_outliers_multiplier: Optional[float]=None, 
                        ofs: Optional[Any]=None) -> pd.DataFrame:
        """
        Retrieve data from either dataframe columns or directly from a pandas Series, 
        with optional outlier exclusion and z-score calculation.

        Parameters:
        ----------
        item : Union[str, pd.Series]
            The column name (str) or actual data (pd.Series) to be retrieved and processed.
        normalize : bool, optional (default is False)
            If True, the data will be normalized.
        columns_for_normalization : List[str], optional
            List of column names used for normalization if `item` is a column name.
        exclude_outliers_multiplier : float, optional
            If provided, outliers will be excluded based on this multiplier.
        ofs : any, optional
            [Explanation needed for this parameter]

        Returns:
        -------
        pd.DataFrame
            A DataFrame containing the retrieved and possibly processed data.
        """
        try:
            data_series = df[item] if isinstance(item, str) else item

            if normalize:
                if isinstance(item, str):
                    # If item is a string (column name), normalize using other columns if provided
                    data_series = normalize_data(df, columns_for_normalization or [item])[item]
                else:
                    # If item is a Series, normalize only the series
                    data_series = (data_series - data_series.min()) / (data_series.max() - data_series.min())

            if exclude_outliers_multiplier is not None:
                data_series = exclude_outliers(data_series, exclude_outliers_multiplier)

        except Exception as e:
            return pd.DataFrame(index=df.index)

        return data_series

    def get_trace(
        item: Union[str, pd.Series], group: str, shape: str, mode: str, 
        normalization: bool, columns_for_normalization: Optional[List[str]] = None, 
        mma: Optional[Tuple[float, float]] = None, 
        exclude_outliers_multiplier: Optional[float] = None) -> List[dict]:
        """
        Get trace(s) for the provided item with specified configurations.
        
        Parameters:
        ----------
        item : Union[str, pd.Series]
            The column name or actual data to be retrieved and processed.
        group : str
            The group for the trace which is used for stacking groups of traces.
        shape : str
            The shape of the plot, either 'line' or 'area'.
        mode : str
            Data representation mode, either 'standalone' or 'cumulative'.
        normalization : bool
            Indicates if the data should be normalized.
        columns_for_normalization : List[str], optional
            List of column names used for normalization if `item` is a column name.
        mma : Tuple[float, float], optional
            Contains values for a moving average and its multiplier for standard deviation.
            Format is (moving_average_period, standard_deviation_multiplier). None by default.
        exclude_outliers_multiplier : float, optional
            If provided, outliers will be excluded based on this multiplier.
        
        Returns:
        -------
        List[dict]
            A list of trace dictionaries, which contain the data and style options 
            for each trace that will be added to the plot.
        """
        column_data = get_data_from_item(
            item, normalization, columns_for_normalization, 
            exclude_outliers_multiplier
        )
        # Basic trace
        try:
            trace = {
                'x': column_data.index,
                'y': column_data,
                'name': item.split(' - ')[1] if isinstance(item, str) else item.name,
                'fill': 'tonexty' if shape == 'area' and mode == 'cumulative' else 
                        'tozeroy' if shape == 'area' else 'none',
                'stackgroup': group if mode == 'cumulative' else None
            }

            traces = [trace]

            # Statistics based on MMA
            if mma:
                window = int(21 * 12 * mma[0])
                rolling_average = column_data.rolling(window=window).mean()
                rolling_std = column_data.rolling(window=window).std()
                
                # MMA trace
                traces.append({
                    'x': column_data.index,
                    'y': rolling_average,
                    'mode': 'lines',
                    'name': f'Média {(mma[0]):.0f}a ± {mma[1]}dp',
                    'line': {'color': 'green'}, 
                    'legendgroup': 'mma', 
                })

                # Traces for ± standard deviations from the MMA
                traces.append({
                    'x': column_data.index,
                    'y': rolling_average + mma[1] * rolling_std,
                    'mode': 'lines',
                    'name': f'+{mma[1]} STD',
                    'line': {'color': 'green', 'dash': 'dash'}, 
                    'legendgroup': 'mma', 
                    'showlegend': False, 
                })

                traces.append({
                    'x': column_data.index,
                    'y': rolling_average - mma[1] * rolling_std,
                    'mode': 'lines',
                    'name': f'-{mma[1]} STD',
                    'line': {'color': 'green', 'dash': 'dash'}, 
                    'legendgroup': 'mma', 
                    'showlegend': False, 
                })

        except Exception as e:
            return []

        return traces

    def update_axis_bounds(fig: go.Figure, side: str, g_max: float, g_min: float, 
        options: Dict[str, Union[bool, str, float, Tuple[float, float]]], 
        default_settings: Dict[str, Union[bool, str, float, Tuple[float, float]]]) -> None:
        """
        Updates the axis bounds of a Plotly figure based on provided options and default settings.

        Parameters:
        ----------
        fig : go.Figure
            The Plotly figure object to be updated.
        side : str
            Specifies which y-axis ('left' or 'right') to update.
        g_max : float
            The global maximum value in the data to be plotted on the specified y-axis.
        g_min : float
            The global minimum value in the data to be plotted on the specified y-axis.
        options : dict
            Contains visualization options for left and right data. Each side (left/right) can have:
            - 'shape' : str, optional (default is 'line')
                Shape of the plot, either 'line' or 'area'.
            - 'mode' : str, optional (default is 'standalone')
                Data representation mode, either 'standalone' or 'cumulative'.
            - 'legendgroup' : str, optional
                String to combine legend items into a group.
            - 'normalization' : bool, optional (default is False)
                Indicates if the data should be normalized.
            - 'mma': tuple of (float, float), optional
                Contains values for a moving average and its multiplier for standard deviation. 
                Format is (moving_average_period, standard_deviation_multiplier). None by default.
            - 'outliers': bool, optional (default is False)
                Indicates if outliers should be excluded.
            - 'range': bool or str, optional (default is False)
                Determines the logic used to set the y-axis bounds:
                - 'flexible': No custom logic, Plotly determines y-axis bounds.
                - False: Upper bound is set to the nearest power of 10 above the maximum data value.
                - 'half': Upper bound is set to the nearest multiple of 5 above the maximum data value.
                - 'full': Upper bound is set to the nearest power of 10 above the maximum data value.
        default_settings : dict
            A dictionary containing default visualization settings, should have keys similar to `options`.
            
        Returns:
        -------
        None
            The function modifies the `fig` object in-place and does not return anything.
        """
        range_option = options.get(side, {}).get('range', default_settings['range'])
        
        # Check if range logic should be applied
        if (
            range_option not in ['flexible', 'full'] and 
            g_max != float('-inf') and 
            g_min != float('inf')
        ):
            # Determine upper bound
            if range_option == 'half':
                upper_bound = 5 * 10 ** math.ceil(math.log10(g_max) - 1)
            elif range_option == False:  # or any other invalid value
                upper_bound = 10 ** math.ceil(math.log10(g_max))
            upper_bound = upper_bound if g_max > 0 else g_max
            
            # Determine lower bound
            lower_bound = 10 ** math.floor(math.log10(g_min)) if g_min > 0 else g_min
            
            # Update layout
            axis_key = 'yaxis' if side == 'left' else 'yaxis2'
            fig.update_layout({axis_key: dict(range=[lower_bound, upper_bound])})

    info = plot_info['info']
    data = plot_info['data']
    options = plot_info.get('options', {})

    # Initialize the figure object and variables
    company, ticker = df[['PREGAO', 'TICKER']].iloc[0]
    fig = go.Figure()

   # Default settings for visualization
    default_settings = {
        'shape': 'line',
        'mode': 'standalone',
        'legendgroup': None,
        'normalization': False, 
        'normalization_columns': None, 
        'mma': None, 
        'outliers': None, 
        'range': 'flexible', 
    }
    
    # Flags to determine if we have data on either side
    left_data_exists = any(item.startswith('left') for item in data.keys())
    right_data_exists = any(item.startswith('right') for item in data.keys())

    # Initialize variables for storing the global max and min values for each side
    global_max = {'left': float('-inf'), 'right': float('-inf')}
    global_min = {'left': float('inf'), 'right': float('inf')}

    # Process each side separately
    for side, items in data.items():
        # Skip if the side is 'title'
        if side == 'title':
            continue
        
        # Determine the base side (left or right)
        side_base = 'left' if 'left' in side else 'right' if 'right' in side else None
        
        if side_base:
            # Get the options for this side, if any
            side_options = {**default_settings, **options.get(side, {})}
            
            # Generate traces for this side
            for item in items:
                traces = get_trace(item, side, 
                                   side_options['shape'],
                                   side_options['mode'],
                                   side_options['normalization'],
                                   side_options['normalization_columns'] or items, 
                                   side_options['mma'],
                                   side_options['outliers'],
                                   )
                for trace in traces:
                    if side_options.get('legendgroup'):
                        trace['legendgroup'] = side_options['legendgroup']
                    
                    # If side contains 'right', assign to yaxis2
                    trace['yaxis'] = 'y2' if 'right' in side and left_data_exists else 'y1'

                    # Update global min and max
                    y_values = trace['y']
                    if not y_values.empty:
                        max_val = max(y_values)
                        min_val = min(y_values)
                        global_max[side_base] = max(global_max[side_base], max_val)
                        global_min[side_base] = min(global_min[side_base], min_val)
                        # print('debug data', info['header'], global_max[side_base], global_min[side_base])

                    fig.add_trace(go.Scatter(**trace))

    # Figure Update Layout
    fig.update_layout(
        template='plotly_white',
        # xxx changes
        # where plot_title is the key of your graphs_0 dict that you're currently processing. This may require a small restructuring in how you call plot_tweak, ensuring that the title is passed as a parameter.
        # title_text=f'{ticker} ({company}) {data.get("title", ["", "", ""])[0]}',
        title_text=f'{ticker} ({company}) {info["title"]}',

        # xxx changes
        xaxis_title='Data',
        yaxis_title=data.get('axis', ["", ""])[0],
        yaxis2={'title': data.get('axis', ["", ""])[1], 'overlaying': 'y', 'side': 'right'} if left_data_exists and right_data_exists else {},

        legend=dict(
            orientation='h',
            font_size=10,
        ),
        # width=6.27 * 200,  # converting inches to 96 pixels for width
        # height=3.52 * 200,  # converting inches to 96 pixels for height
    )
    
    # Applying the flexible_range logic. Note: The logic is NOT applied if flexible_range is True. If it's False, it IS applied.
    update_axis_bounds(fig, 'left', global_max['left'], global_min['left'], options, default_settings)
    update_axis_bounds(fig, 'right', global_max['right'], global_min['right'], options, default_settings)

    return fig

def convert_series_to_list(graphs_dict):
    for section_key, section_value in graphs_dict.items():
        for line_key, line_value in section_value.items():
            for plot_key, plot_value in line_value.items():
                if 'data' in plot_value:
                    data = plot_value['data']
                    for axis in ['left', 'right']:
                        if axis in data:
                            new_data_list = []
                            for item in data[axis]:
                                if isinstance(item, pd.Series):
                                    series_data = [[item.name, str(idx), val] for idx, val in item.items()]
                                    new_data_list.append(series_data)
                                else:
                                    new_data_list.append(item)
                            data[axis] = new_data_list
    return graphs_dict

def serialize_data(data):
    """
    Convert dictionary data into a JSON string.
    """
    return json.dumps(data)

def compress_data(data: str) -> str:
    """
    Compress a string and return it as a base64 encoded string.
    """
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='w') as f:
        f.write(data.encode())
    compressed_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return compressed_data

def convert_and_compress(graphs_dict):
    """
    Convert a dictionary into a list, serialize it, and compress it.
    Returns compressed data.
    """
    graphs_as_list = convert_series_to_list(graphs_dict)
    serialized_data = serialize_data(graphs_as_list)
    compressed_data = compress_data(serialized_data)
    return compressed_data

def reverse_to_series(graphs_dict):
    # Iterate through each section of the graph
    for section_key, section_value in graphs_dict.items():
        for line_key, line_value in section_value.items():
            for plot_key, plot_value in line_value.items():
                if 'data' in plot_value:
                    data = plot_value['data']
                    for axis in ['left', 'right']:
                        if axis in data:
                            new_data_list = []
                            for item in data[axis]:
                                # Check if the item is a list of lists
                                if isinstance(item, list) and item and isinstance(item[0], list):
                                    # Check if it can be converted to a pd.Series
                                    try:
                                        series_name = item[0][0]

                                        # Extracting datetime index
                                        index = pd.to_datetime([elem[1] for elem in item])

                                        # Extracting values and converting to float or NaN
                                        values = [float(elem[2]) if elem[2] != 'nan' else np.nan for elem in item]

                                        # Creating the series
                                        series = pd.Series(data=values, index=index, name=series_name)
                                        new_data_list.append(series)
                                    except:
                                        new_data_list.append(item)
                                else:
                                    new_data_list.append(item)
                            data[axis] = new_data_list
    return graphs_dict

def deserialize_data(data_str):
    """
    Convert a JSON string into dictionary data.
    Convert string keys that are numbers into integers (except for the top level).
    """
    data = json.loads(data_str)

    def int_key_converter(obj):
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_key = int(key) if key.isdigit() else key
                new_obj[new_key] = int_key_converter(value)
            return new_obj
        return obj

    for key in data:
        data[key] = int_key_converter(data[key])

    return data

def decompress_data(compressed_data: str) -> str:
    """
    Decompress a base64 encoded string and return it as a decoded string.
    """
    buffer = io.BytesIO(base64.b64decode(compressed_data))
    with gzip.GzipFile(fileobj=buffer, mode='r') as f:
        decompressed_data = f.read().decode()
    return decompressed_data

def decompress_and_convert(compressed_data):
    """
    Decompress the data, deserialize it, and convert the result back into the original dictionary structure.
    Returns the dictionary.
    """
    decompressed_str = decompress_data(compressed_data)
    deserialized_data = deserialize_data(decompressed_str)
    original_data = reverse_to_series(deserialized_data)
    return original_data
 
def clean_df(df):
    df = df.copy()
    # Remove the columns named 'level_0' and 'index' from the dataframe
    df = df[[col for col in df.columns if col not in ['level_0', 'index']]]
    # Convert the 'VERSAO' column values to integers, then to strings (objects)
    df['VERSAO'] = df['VERSAO'].astype(int).astype(str)
    # Convert the 'CD_CVM' column values to integers, then to strings (objects)
    df['CD_CVM'] = df['CD_CVM'].astype(int).astype(str)
    # Convert the 'DT' columns values to datetime format
    datetime_cols = [col for col in df.columns if col.startswith('DT')]
    df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime)
    # Convert the 'COLUNA_DF' column values to strings (objects)
    df['COLUNA_DF'] = df['COLUNA_DF'].astype(str)
    # Identify all columns that start with a digit
    float_cols = [col for col in df.columns if col[0].isdigit()]
    df[float_cols] = df[float_cols].astype('float64')
    # Identify all object columns that do not contain the word "original" (case-insensitive) in their name
    # category_columns = [col for col in df.select_dtypes(include=['object']).columns if "original" not in col.lower()]
    # df[category_columns] = df[category_columns].astype('category')
    df['Date'] = pd.to_datetime(df['Date'])  # Convert the 'Date' column to datetime format (if it isn't already)
    df = df.set_index('Date')

    return df