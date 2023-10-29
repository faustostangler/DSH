import assets.helper as b3
import assets.functions as run
import assets.lines

def get_manual_entries(df):
    """
    Fetch manual entries for the graphs.
    
    Parameters:
    - df: DataFrame (not utilized in this function, but kept for consistency).
    
    Returns:
    - manual_entries: List of dictionaries containing manual graph data.
    """

    return assets.lines.manual_entries

def get_default_entries(df):
    """
    Generate default graph items based on the provided lines information.
    
    Parameters:
    - df: DataFrame containing the data.
    
    Returns:
    - default_entries: Dictionary of generated graph items.
    """
    # choose which set of lines to import and plot
    lines = assets.lines.report

    # basic info
    cagr = 'O CAGR, ou Taxa de Crescimento Anual Composta, avalia o crescimento médio anual do indicador ao longo do intervalo, ignorando as flutuações, e mostra o ritmo médio de crescimento anual no período.'
    mma = 'A Média Móvel mostra a tendência central e os limites da variação do indicador no período, na forma de uma faixa típica de valores. Essencialmente, nos mostra o caminho e se o indicador está dentro ou fora da variação normal passada.'

    # Extract unique groups (first two digits) from the lines
    groups = set(entry['line'][:2] for entry in lines)
    groups = sorted(groups)
    
    default_entries = {}
    for group in groups:
        filtered_lines = [entry for entry in lines if entry['line'].startswith(group)]
        default_entries[group] = {}
        for l, line in enumerate(filtered_lines):
            # Construct graph info based on line data
            default_entries[group][l] = {}
            default_entries[group][l][0] = {
                'info': {
                    'title': f'{line["title"]}', 
                    'header': f'{line["header"]}', 
                    'description': f'{line["description"]}', 
                    # 'mma': f'{mma}', 
                    # 'cagr': f'{cagr}', 
                    'footer': f'{line["footer"]}', 
                }, 
                'data': {
                    'axis': ['Reais (RS)', 'Porcentagem (%)'], 
                    'left': [line["line"]], 
                    # 'right': [run.cagr(line["line"], df)], 
                }, 
                'options': {
                    'left': {'shape': 'area', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2], },
                    'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'outliers': False, }, 
                }, 
            }
            # sublines = [column for column in df.columns if column.startswith(line["line"].split(' - ')[0] + '.') and column.count('.') == line["line"].count('.') + 1]
            # if sublines: 
            #     default_entries[group][l][1] = {
            #         'info': {
            #             'title': f'{line["title"]}', 
            #             'header': f'{line["header"]} - Composição Relativa', 
            #             'description': f'{line["description"]}', 
            #             'footer': 'Ao olhar para um gráfico normalizado, estamos vendo uma comparação de como essas linhas mudaram em relação ao seu começo. Não estamos vendo os valores reais, mas sim o quão rápido ou devagar cada linha cresceu ou diminuiu em comparação com as outras. Isso nos ajuda a entender qual linha teve maior crescimento ou queda ao longo do tempo em relação às outras linhas e ao todo, mesmo que todas pareçam ter aumentado ou diminuído. Em essência, é como comparar a proporção de diferentes populações de animais, vendo como elas variaram entre si desde o início.', 
            #         }, 
            #         'data': {
            #             'axis': ['Porcentagem (%)', 'Porcentagem (%)'],
            #             'left': sublines,
            #         },
            #         'options': {
            #             'left': {'shape': 'line', 'mode': 'standalone', 'normalization': True,},
            #         }
            #     }


    return default_entries

def construct_graphs(df):
    """
    Merge default graph items with manual entries to construct the full graph structure.
    
    Parameters:
    - df: DataFrame containing the data.
    
    Returns:
    - default_entries: Dictionary containing the merged graph items.
    """
    # Get default graphs
    default_entries = get_default_entries(df)
    
    # Get manual entries
    manual_entries = get_manual_entries(df)

    # Integrate manual entries into the default_entries structure
    merged_entries = {**default_entries, **manual_entries}

    # filter non-existing entries
    filtered_entries = merged_entries.copy()
    # Iterate over each main key-value pair in merged_entries
    for main_key, main_value in list(filtered_entries.items()):
        for sub_key, sub_value in list(main_value.items()):
            # Dive into the nested structure to reach the 'data' dictionary
            data_dict = sub_value.get(0, {}).get('data', {})
            
            # Filter items for keys starting with 'left' or 'right'
            keys_to_check = list(data_dict.keys())  # Make a copy of keys
            for key in keys_to_check:
                items = data_dict[key]
                if key.startswith('left') or key.startswith('right'):
                    filtered_items_list = [item for item in items if item in df.columns]
                    if filtered_items_list:
                        data_dict[key] = filtered_items_list
                    else:
                        # Remove the key if it's empty after filtering
                        del data_dict[key]
            
            # Check if both 'left' and 'right' keys are empty, then remove the main key
            if not data_dict.get('left') and not data_dict.get('right'):
                del filtered_entries[main_key]

    return filtered_entries
