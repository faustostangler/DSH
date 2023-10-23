import assets.helper as b3
import assets.functions as run

def get_manual_entries(df):
    """
    Fetch manual entries for the graphs.
    
    Parameters:
    - df: DataFrame (not utilized in this function, but kept for consistency).
    
    Returns:
    - manual_entries: List of dictionaries containing manual graph data.
    """
    # Define manual entries with their respective groupings
    # manual entries are preceeded by a group dict
    manual_entries = [
        { '99': {
            'info': {
                'title': 'Manual Title 1', 
                'header': 'Manual Header 1', 
                'description': 'Manual Description 1', 
                'footer': 'Manual Footer 1', 
            }, 
            'data': { # choose wisely
                'axis': ['Reais (RS)', 'Porcentagem (%)'], 
                # 'left': [df.column_name], 
                # 'right': [run.cagr(df.column_name, df)],
            }, 
            'options': { # format accordingly
                # 'left': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2], },
                # 'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'outliers': False, }, 
            }, 
        }, }, 
        { '99': {
            'info': {
                'title': 'Manual Title 2', 
                'header': 'Manual Header 2', 
                'description': 'Manual Description 2', 
                'footer': 'Manual Footer 2', 
            }, 
            'data': { # choose wisely
                'axis': ['Reais (RS)', 'Porcentagem (%)'], 
                # 'left': [df.column_name], 
                # 'right': [run.cagr(df.column_name, df)],
            }, 
            'options': { # format accordingly
                # 'left': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2], },
                # 'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'outliers': False, }, 
            }, 
        }, }, 
    ]

    # Filter out manual entries where 'title' is not in df.columns or its sum is 0
    manual_entries = [entry for entry_group in manual_entries for key, entry in entry_group.items() if entry['info']['title'] in df.columns and df[entry['info']['title']].sum() != 0]

    manual_entries = []
    return manual_entries

def get_default_lines(df):
    """
    Provide the default lines' information used to generate the graphs.
    
    Returns:
    - A list of dictionaries containing information about each default line.
    """
    from assets.plots import lines_info

    # Filter out lines where the sum in the DataFrame is 0
    lines_info = [line for line in lines_info if line['line'] in df.columns and df[line['line']].sum() != 0]

    return lines_info

def get_default_graphs(df):
    """
    Generate default graph items based on the provided lines information.
    
    Parameters:
    - df: DataFrame containing the data.
    
    Returns:
    - default_graphs: Dictionary of generated graph items.
    """
    # Fetch default line information
    lines_info = get_default_lines(df)
    cagr = 'O CAGR, ou Taxa de Crescimento Anual Composta, avalia o crescimento médio anual do indicador ao longo do intervalo, ignorando as flutuações, e mostra o ritmo médio de crescimento anual no período.'
    mma = 'A Média Móvel mostra a tendência central e os limites da variação do indicador no período, na forma de uma faixa típica de valores. Essencialmente, nos mostra o caminho e se o indicador está dentro ou fora da variação normal passada.'

    # Extract unique groups (first two digits) from the lines_info
    groups = set(entry['line'][:2] for entry in lines_info)
    groups = sorted(groups)
    
    default_graphs = {}
    for group in groups:
        filtered_lines = [entry for entry in lines_info if entry['line'].startswith(group)]
        default_graphs[group] = {}
        for l, line in enumerate(filtered_lines):
            # Construct graph info based on line data
            default_graphs[group][l] = {}
            default_graphs[group][l][0] = {
                'info': {
                    'title': f'{line["title"]}', 
                    'header': f'{line["header"]}', 
                    'description': f'{line["description"]}', 
                    'mma': f'{mma}', 
                    'cagr': f'{cagr}', 
                    'footer': f'{line["footer"]}', 
                }, 
                'data': {
                    'axis': ['Reais (RS)', 'Porcentagem (%)'], 
                    'left': [line["line"]], 
                    'right': [run.cagr(line["line"], df)], 
                }, 
                'options': {
                    'left': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2], },
                    'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'outliers': False, }, 
                }, 
            }
            sublines = [column for column in df.columns if column.startswith(line["line"].split(' - ')[0] + '.') and column.count('.') == line["line"].count('.') + 1]
            if sublines: 
                default_graphs[group][l][1] = {
                    'info': {
                        'title': f'{line["title"]}', 
                        'header': f'{line["header"]} - Composição Relativa', 
                        'description': f'{line["description"]}', 
                        'footer': 'Ao olhar para um gráfico normalizado, estamos vendo uma comparação de como essas linhas mudaram em relação ao seu começo. Não estamos vendo os valores reais, mas sim o quão rápido ou devagar cada linha cresceu ou diminuiu em comparação com as outras. Isso nos ajuda a entender qual linha teve maior crescimento ou queda ao longo do tempo em relação às outras linhas e ao todo, mesmo que todas pareçam ter aumentado ou diminuído. Em essência, é como comparar a proporção de diferentes populações de animais, vendo como elas variaram entre si desde o início.', 
                    }, 
                    'data': {
                        'axis': ['Porcentagem (%)', 'Porcentagem (%)'],
                        'left': sublines,
                    },
                    'options': {
                        'left': {'shape': 'line', 'mode': 'standalone', 'normalization': True,},
                    }
                }


    return default_graphs

def construct_graphs(df):
    """
    Merge default graph items with manual entries to construct the full graph structure.
    
    Parameters:
    - df: DataFrame containing the data.
    
    Returns:
    - default_graphs: Dictionary containing the merged graph items.
    """
    # Get default graphs
    default_graphs = get_default_graphs(df)
    
    # Get manual entries
    manual_entries = get_manual_entries(df)

    # Integrate manual entries into the default_graphs structure
    for group_data in manual_entries:
        for group, entries in group_data.items():
            if group not in default_graphs:
                default_graphs[group] = {}
            for key, new_entry in entries.items():
                # Identify the next available sub-key
                next_subkey = max(default_graphs[group].keys(), default=-1) + 1
                default_graphs[group][next_subkey] = new_entry

    return default_graphs
