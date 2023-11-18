from . import helper as b3
from . import main

import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import requests
import zipfile
import io
import os
from lxml import html

import multiprocessing
from multiprocessing import Pool

# load databases
def get_databases_from_cvm(math='', cvm_local='', cvm_web='', math_local='', math_web=''):
    """
    Retrieves and processes CVM databases, merging local and web data to create updated mathematical representations.

    This function manages the local and web versions of CVM databases, updating and calculating mathematical data.
    It merges local and web data to provide a comprehensive view.

    Args:
        math (dict, optional): Pre-loaded math data. Defaults to an empty dictionary.
        cvm_local (dict, optional): Pre-loaded local CVM data. Defaults to an empty dictionary.
        cvm_web (dict, optional): Pre-loaded web CVM data. Defaults to an empty dictionary.
        math_local (dict, optional): Pre-loaded local math data. Defaults to an empty dictionary.
        math_web (dict, optional): Pre-loaded web math data. Defaults to an empty dictionary.

    Returns:
        dict: Merged and updated math data based on local and web sources.
    """
    # initialize variables
    cvm_local, cvm_web, cvm_updated = {}

    try:
        # prepare cvm_local and cvm_web
        if not cvm_local:
            try:
                cvm_local = main.load_pkl(f'{b3.app_folder}/temp_'+'cvm_local')
            except Exception as e:
                cvm_local = {}
        if not cvm_web:
            cvm_web = get_web_database()
            # print('debug cvm_web clean load x')
            # cvm_web = main.load_pkl(f'{b3.app_folder}/temp_'+'cvm_web')

        # Compare web (new) data to local (old) data. Extract only updated rows
        cvm_updated = updated_rows(cvm_local, cvm_web)
        cvm_updated = main.save_pkl(cvm_updated, f'{b3.app_folder}/temp_'+'cvm_updated')
        # print('fast cvm_updated debug')
        # cvm_updated = main.load_pkl(f'{b3.app_folder}/temp_'+'cvm_updated')

    except Exception as e:
        pass

    return cvm_local, cvm_web, cvm_updated

# from web
def get_web_database():
    # initialize variables
    categories = ''
    demonstrativos_cvm = ''
    meta_dict = {}
    cvm_web = pd.DataFrame()

    try:
        filelist_df, last_update = get_database_filelist()

        dataframes = download_csv_files_from_cvm_web(filelist_df)
        dataframes = main.save_pkl(dataframes, f'{b3.app_folder}/temp_' + 'dataframes')
        # print('fast debug dataframes')
        # dataframes = main.load_pkl(f'{b3.app_folder}/temp_' + 'dataframes')

        cvm_web, links = group_dataframes_by_year(dataframes)
        cvm_web = main.save_pkl(cvm_web, f'{b3.app_folder}/temp_' + 'dataframes_by_year')
        # print('fast debug dataframes by year')
        # cvm_web = main.load_pkl(f'{b3.app_folder}/temp_' + 'dataframes_by_year')

        links = main.save_pkl(links, f'{b3.app_folder}/temp_' + 'links')
        # print('fast debug links')
        # links = main.load_pkl(f'{b3.app_folder}/temp_' + 'links')

        cvm_web = clean_dataframe(cvm_web)
        cvm_web = main.save_pkl(cvm_web, f'{b3.app_folder}/temp_' + 'cvm_web')
        # print('fast debug cvm_web cvm_web_clean')
        # cvm_web = main.load_pkl(f'{b3.app_folder}/temp_' + 'cvm_web')

        # Get metadata and categories from filelist
        try:
            meta_dict = get_metadados(filelist_df['filename'].to_list())
            categories = get_categories(filelist_df['filename'].to_list())
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

def get_database_filelist():
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
    filelist_df = get_database_filelist_links()
    filelist_df = main.save_pkl(filelist_df, f'{b3.app_folder}/temp_filelist_df')
    # print('fast debug filelist_df')
    # filelist_df = main.load_pkl(f'{b3.app_folder}/temp_filelist_df')
    
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

def get_database_filelist_links():
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
    filelist = main.gather_links(url)
    folders = set()

    # Extract folder URLs from file links
    for url in filelist:
        folder_url = '/'.join(url.split('/')[:-1])
        folders.add(folder_url)

    fileinfo_df = []
    start_time = time.time()
    # Loop through folder URLs and extract file information
    for i, url in enumerate(folders):
        print(main.remaining_time(start_time, len(folders), i))
        response = requests.get(url, headers=main.header_random())
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

def download_csv_files_from_cvm_web(filelist_df, types=['itr', 'dfp']):
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
            response = requests.get(zip_url, headers=main.header_random())

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

                        print('  ' + '  ' + main.remaining_time(start_time_3, len(zip_ref.infolist()), k), fileinfo.filename.lower())
            print('  ' + main.remaining_time(start_time_2, len(download_files), j))
        print(main.remaining_time(start_time, len(types), i))
    print(f'Total {len(dataframes)} databases found and {total_rows} lines downloaded')
    return dataframes

def group_dataframes_by_year(dataframes):
    cvm_web = [df for df in dataframes if len(df) > 0 and ('con' in df['FILENAME'][0] or 'ind' in df['FILENAME'][0])]
    links = [df for df in dataframes if len(df) > 0 and ('con' not in df['FILENAME'][0] and 'ind' not in df['FILENAME'][0])]

    print('... split by year')
    cvm_web = group_dataframes_by_year_yearly(cvm_web)
    links = group_dataframes_by_year_yearly(links)

    # Rename column for consistency
    for year in links.keys():
        links[year].rename(columns={'VERSAO': 'VERSAO_LINK'}, inplace=True)

    return cvm_web, links

def group_dataframes_by_year_yearly(df_list):
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
        print(year, main.remaining_time(start_time, len(df_list), i))

        # Check if the year is already a key in the dictionary, if not, create a list for it
        if year not in df_y:
            df_y[year] = []
        
        # Append the DataFrame to the list for the respective year
        df_y[year].append(df)

    print('... concatenating')
    start_time = time.time()

    # Concatenate DataFrames within each year's list
    for i, (year, df_list) in enumerate(df_y.items()):
        print(year, main.remaining_time(start_time, len(df_y), i))
        df_y[year] = pd.concat(df_list, ignore_index=True)

    return df_y

def clean_dataframe(dict_of_df):
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

        # Vectorized adjustment of VL_CONTA according to ESCALA_MOEDA
        mask = df['ESCALA_MOEDA'] == 'MIL'
        df.loc[mask, 'VL_CONTA'] *= 1000
        df.loc[mask, 'ESCALA_MOEDA'] = 'UNIDADE'

        # Filter unnecessary lines
        df = df.drop_duplicates(subset=['CNPJ_CIA', 'AGRUPAMENTO', 'CD_CONTA', 'DT_REFER', 'COLUNA_DF'], keep='first')

        df = parallel_multiprocessing(clean_dataframe_parallel, df)

        dict_of_df[year] = df

        print(year, main.remaining_time(start_time, len(dict_of_df), i))
    return dict_of_df

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
    metafiles = [filelink for filelink in filelist if "meta" in filelink]

    for file in metafiles:
        response = b3.session.get(file)
        response.raise_for_status()

        if file.endswith('.zip'):
            zip = zipfile.ZipFile(io.BytesIO(response.content))

            for filein_zip in zip.namelist():
                with zip.open(filein_zip) as zipfilecontent:
                    filecontent = zipfilecontent.read().decode('utf-8', errors='ignore')
                    d = extract_meta(filecontent)
                    meta_dict[filein_zip.split('.')[0]] = d
        elif file.endswith('.txt'):
            filecontent = response.content.decode('iso-8859-1')
            d = extract_meta(filecontent)
            filename = file.split('/')[-1].split('.')[0]
            meta_dict[filename] = d

    return meta_dict

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
    # metafiles = [filelink for filelink in filelist if "meta" in filelink]
    # files = [filelink for filelink in filelist if "meta" not in filelink]

    for filelink in filelist:
        cat = '/'.join(filelink.replace(b3.base_cvm,'').split('/')[:-2])
        categories.add(cat)
    categories = sorted(list(categories))

    return categories

# multiprocessing
def parallel_multiprocessing(func, df):
    """
    Applies a function to a DataFrame using parallel processing.

    This function splits a DataFrame into several parts equal to the number of CPU cores available,
    and then applies a given function to each part in parallel. After processing, it concatenates 
    the results back into a single DataFrame. This is useful for speeding up processing on large DataFrames.

    Args:
        func (callable): The function to be applied to each split of the DataFrame.
        df (pd.DataFrame): The DataFrame to be processed.

    Returns:
        pd.DataFrame: The DataFrame after the function has been applied to each part.
    """
    # Determine the number of cores available
    n_cores = multiprocessing.cpu_count()

    # Split the DataFrame into parts equal to the number of cores
    df_split = np.array_split(df, n_cores)

    # Create a multiprocessing pool and apply the function to each part
    with multiprocessing.Pool(n_cores) as pool:
        df = pd.concat(pool.map(func, df_split))

    # Return the concatenated DataFrame
    return df

def clean_dataframe_parallel(df):
    """
    Cleans specific columns of a pandas DataFrame in parallel.

    This function applies text cleaning and word removal processes to the 'DENOM_CIA' column 
    of the given DataFrame. The cleaning process is intended to standardize the text data in this column.

    Args:
        df (pd.DataFrame): The DataFrame to be cleaned.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """

    # Apply text cleaning to the 'DENOM_CIA' column
    df['DENOM_CIA'] = df['DENOM_CIA'].apply(main.clean_text)

    # Further clean 'DENOM_CIA' by removing specific words
    df['DENOM_CIA'] = df['DENOM_CIA'].apply(main.word_to_remove)

    return df

# calculus
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

def calculate_math(cvm, where):
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
    start_time = time.time()
    for i, (year, df) in enumerate(cvm.items()):
        try:
            math[year] = main.load_pkl(f'{b3.app_folder}/temp_math_{where}_{year}')
        except Exception as e:
            problem_column = 'COLUNA_DF'

            # Split the DataFrame into two parts based on NaN values in COLUNA_DF
            df_without_coluna_df = df[df[problem_column].isna()]
            df_with_coluna_df = df.dropna(subset=[problem_column])

            # Grouping with and without COLUNA_DF
            group_cols = [col for col in b3.unique_sheet_cols if col != problem_column]
            grouped_without = df_without_coluna_df.groupby(group_cols, group_keys=False)
            grouped_with = df_with_coluna_df.groupby(b3.unique_sheet_cols, group_keys=False)

            # Initialize the calculated dataframes
            calculated_df_without = pd.DataFrame()
            calculated_df_with = pd.DataFrame()

            # Set up a progress bar to track the processing of each group
            with tqdm(total=grouped_without.ngroups, desc=f"Calculating quarter values for year {year} part 1") as pbar:
                # Use a lambda to pass the progress bar to the wrapper_apply function
                calculated_df_without = grouped_without.apply(lambda group: wrapper_apply(group, pbar)).reset_index(drop=True)

            # Set up a progress bar to track the processing of each group
            with tqdm(total=grouped_with.ngroups, desc=f"Calculating quarter values for year {year} part 2") as pbar:
                # Use a lambda to pass the progress bar to the wrapper_apply function
                calculated_df_with = grouped_with.apply(lambda group: wrapper_apply(group, pbar)).reset_index(drop=True)

            # Combine the results
            calculated_df = pd.concat([calculated_df_without, calculated_df_with])

            # Save the calculated dataframe to the math dictionary and to files
            math[year] = calculated_df

            # math = main.save_pkl(math, f'{b3.app_folder}/math_local')
            math[year] = main.save_pkl(math[year], f'{b3.app_folder}/temp_math_{where}_{year}')
            print(main.remaining_time(start_time, len(cvm), i))

    return math

def math_calculations_adjustments(group):
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

    row = group.iloc[0]
    # print(row['ANO'], row['CNPJ_CIA'], row['AGRUPAMENTO'], row['DT_REFER'], row['BALANCE_SHEET'], row['CD_CONTA'])
  
    sheet = group['BALANCE_SHEET'].iloc[0]
    
    # If the group's 'BALANCE_SHEET' value belongs to the fluxo_de_caixa category, apply quarter adjustments.
    if sheet in fluxo_de_caixa:
        group = adjust_quarters(group)
    # If the group's 'BALANCE_SHEET' value belongs to the resultados category, filter and adjust the last quarter.
    elif sheet in resultados:
        group = adjust_last_quarter(group)
    # If the group's 'BALANCE_SHEET' value doesn't match the above categories, return the original group without adjustments.
    return group

def extract_updated_rows(df_local, df_web, df_columns, year):

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

def updated_rows(cvm_local, cvm_web):
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
        cvm_updated[year] = extract_updated_rows(df_local, df_web, df_columns, year)
        main.beep()
    return cvm_updated

# math
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

def get_math_from_b3_cvm():
#         # math_local = cvm_calculate_math(cvm_local, where='local')
#         # math_local = main.save_pkl(math_local, f'{b3.app_folder}/temp_'+'math_local')
#         print('fast_debug_local_math')
#         math_local = main.load_pkl(f'{b3.app_folder}/temp_math_local')

#         # df_merged = main.save_pkl(cvm_web[2011], f'{b3.app_folder}/temp_df_merge_to_math_pre')

#         # math_web = cvm_calculate_math(cvm_web, where='web')
#         # math_web = main.save_pkl(math_web, f'{b3.app_folder}/temp_'+'math_web')
#         # # print('fast_debug_web_math')
#         # # math_web = main.load_pkl(f'{b3.app_folder}/temp_math_web')

#         cvm_updated = main.load_pkl(f'{b3.app_folder}/temp_'+'cvm_updated')
#         math_updated = calculate_math(cvm_updated, where='updated')
#         math_updated = main.save_pkl(math_updated, f'{b3.app_folder}/temp_'+'math_updated')
#         # print('fast_debug_updated_math')
#         # math_updated = main.load_pkl(f'{b3.app_folder}/temp_math_updated')

#         # math_local
#         try:
#             math_local = main.load_pkl(f'{b3.app_folder}/temp_'+'math')
#         except Exception as e:
#             math_local = {}
# # try:
#     # math_local = math_from_cvm(cvm_local) # shortcut to load math per year, not necessary unless huge huge database
#     # math_local = get_calculated_math(cvm_local) # this is where the groupby transformation mathmagic happens
#     # math_local = main.save_pkl(math_local, f'{b3.app_folder}/math_local')
# # except Exception as e:

#         # math_web
#         try:
#             math_web = main.load_pkl(f'{b3.app_folder}/math_web')
#         except Exception as e:
#             cvm_local, math_web = updated_rows(cvm_local, cvm_web)

#         math = math_merge(math_local, math_web)
#     return math

    b3_cvm = main.load_pkl(f'{b3.app_folder}/b3_cvm')

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

# helper functions
def wrapper_apply(group, pbar):
    """Wrapper function for applying adjustments and updating the progress bar."""
    result = math_calculations_adjustments(group)
    pbar.update(1)  # Update the progress bar by one step
    # sys_beep()
    return result
