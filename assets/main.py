from . import helper as b3
from . import cloud

import os 
import pandas as pd
import pickle
import time
import winsound

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random

import unidecode
import string
import re

# operating system
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

# general
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
  beep()

  return progress

def beep(frequency=5000, duration=50):
    winsound.Beep(frequency, duration)
    return True

# pandas dataframes
def read_or_create_dataframe(filename, cols):
    """
    Read a pandas DataFrame from a compressed file stored in Google Cloud Storage, or create an empty DataFrame if the file doesn't exist.
    First, attempts to download and pickle the DataFrame from Google Cloud Storage. If this fails, it tries to read a local pickled version.
    If both attempts fail, it creates an empty DataFrame with the specified columns.

    Args:
        filename (str): The name of the file (without the extension) to read/create.
        cols (list): A list of column names for the DataFrame.

    Returns:
        pd.DataFrame: The DataFrame read from the file, or an empty DataFrame if the file doesn't exist.
    """
    filepath = os.path.join(b3.data_path, f'{filename}.zip')  # Construct the full path to the file

    try:
        # Attempt to download the DataFrame from Google Cloud Storage and save it locally
        df = cloud.download_from_gcs(filename+'errorgoogle')
        df = save_and_pickle(df, filename)
    except Exception as e:
        # If the first attempt fails, try to read a local pickled version of the DataFrame
        try:
            df = pd.read_pickle(filepath)
            df = cloud.upload_to_gcs(df, filename)
        except Exception as e:
            # If both attempts fail, create an empty DataFrame
            df = pd.DataFrame(columns=cols)
        
    df.drop_duplicates(inplace=True)  # Remove any duplicate rows
    print(f'{filename}: total {len(df)} items')
    return df[cols]

def save_and_pickle(df, filename):
    """
    Save a DataFrame as a pickled file and upload it to Google Cloud Storage.

    Args:
        df (pd.DataFrame): The DataFrame to be saved and uploaded.
        filename (str): The name of the file to save the DataFrame.

    Returns:
        pd.DataFrame: The original DataFrame after attempting to save and upload.
    """
    try:
        # Save the DataFrame as a pickled file locally and then upload to Google Cloud Storage
        df.to_pickle(f'{b3.data_path}/{filename}.zip')
        df = cloud.upload_to_gcs(df, filename)
    except Exception as e:
        # If saving or uploading fails, the function will pass silently
        pass
    return df

# fast pkl
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
    #     with zipf.open(f'{filename}.pkl', 'r') as datafile:
    #         data = pickle.load(datafile)

    return data

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
    #     with zipf.open(f'{filename}.pkl', 'w') as datafile:
    #         pickle.dump(data, datafile)

    return data

# web grabber
def gather_links(url):
    """
    Recursively gathers links to files with specific extensions from a given URL.

    This function navigates through web pages starting from the given URL, collecting links to files
    with specific extensions (.csv, .zip, .txt). It avoids revisiting subfolders and is capable of 
    traversing subdirectories.

    Args:
        url (str): The URL to start gathering links from.

    Returns:
        list: A list of gathered file links with specified extensions.
    """

    # Mark the subfolder as visited to avoid revisiting
    b3.visited_subfolders.add(url)

    # Fetch the content from the URL
    response = b3.session.get(url)
    response.raise_for_status()

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Iterate through all anchor tags to find links
    for link in soup.find_all("a"):
        href = link.get("href")
        full_link = urljoin(url, href)

        # Check if the link is not visited and starts with the base URL
        if full_link.startswith(b3.base_cvm) and full_link not in b3.visited_subfolders:
            # Append to the filelist if the link ends with the desired file extensions
            if full_link.endswith((".csv", ".zip", ".txt")):
                b3.filelist.append(full_link)
            # Recursively call gather_links for subdirectories
            elif full_link.endswith("/"):
                gather_links(full_link)

    return b3.filelist

def header_random():
    """
    Generate a random HTTP header for web requests.

    This function creates a random HTTP header by selecting a random user agent, referer, and language.
    It helps in simulating different types of web requests, which can be useful for web scraping or API calls
    where varying the headers can help in avoiding detection as a bot.

    Returns:
        dict: A dictionary containing the headers with keys 'User-Agent', 'Referer', and 'Accept-Language'.
    """

    # Select a random user agent from a predefined list
    user_agent = random.choice(b3.USER_AGENTS)

    # Select a random referer from a predefined list
    referer = random.choice(b3.REFERERS)

    # Select a random language from a predefined list
    language = random.choice(b3.LANGUAGES)

    # Construct the headers dictionary
    headers = {
        'User-Agent': user_agent,
        'Referer': referer,
        'Accept-Language': language
    }

    # Return the constructed headers
    return headers

# text
def clean_text(text):
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

def word_to_remove(text):
    """
    Removes specified words from a text content.

    This function takes a text content (string) and removes specified words from it.
    The words to remove are defined in the 'words_to_remove' list which is a part of the b3 object.

    Args:
        text (str): The content of the text to be cleaned.

    Returns:
        str: The cleaned text content without the specified words.
    """
    # Create a regular expression pattern based on the words to remove
    pattern = '|'.join(map(re.escape, b3.words_to_remove))

    # Replace occurrences of any word in the pattern with an empty string
    text = re.sub(pattern, '', text)

    return text

