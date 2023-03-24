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
    options.add_argument('start-maximized')  # Maximize the window on startup.
    # options = Options()

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
        print(f'Error occurred while reading file {file_name}: {e}')
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

