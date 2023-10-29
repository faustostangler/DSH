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
    manual_entries = [{
        '99': {
            0: {
                'info': {
                    'title': '99 - PVPA', 
                    'header': 'Manual Header 1', 
                    'description': 'Manual Description 1', 
                    'footer': 'Manual Footer 1'
                },
                'data': {
                    'axis': ['Reais (RS)', 'Porcentagem (%)'],
                    'left': ['99 - PVPA']
                },
                'options': {
                    'left': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2]}
                }, 
            },
            1: {
                'info': {
                    'title': '99 - PVPA', 
                    'header': 'Manual Header 1', 
                    'description': 'Manual Description 1', 
                    'footer': 'Manual Footer 1'
                },
                'data': {
                    'axis': ['Reais (RS)', 'Porcentagem (%)'],
                    'left': ['99 - PVPA']
                },
                'options': {
                    'left': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2]}
                }, 
            }, 
        }, 
    }]

    # Filter out manual entries where 'title' is not in df.columns or its sum is 0
    filtered_manual_entries = {
        group_key: {
            plot_key: plot_value 
            for plot_key, plot_value in group_value.items() 
            if 'info' in plot_value and plot_value['info'].get('title') in df.columns and df[plot_value['info']['title']].sum() != 0
        } 
        for group_key, group_value in manual_entries[0].items()
    }
    
    filtered_manual_entries = {k: v for k, v in filtered_manual_entries.items() if v}  # Remove groups without valid plots

    return [filtered_manual_entries]  # Return as a list

def get_default_graphs(df):
    """
    Generate default graph items based on the provided lines information.
    
    Parameters:
    - df: DataFrame containing the data.
    
    Returns:
    - default_graphs: Dictionary of generated graph items.
    """
    # choose which set of lines to import and plot
    import assets.lines
    lines = assets.lines.report

    # Filter out lines where the sum in the DataFrame is 0
    lines = [line for line in lines if line['line'] in df.columns and df[line['line']].sum() != 0]

    # basic info
    cagr = 'O CAGR, ou Taxa de Crescimento Anual Composta, avalia o crescimento médio anual do indicador ao longo do intervalo, ignorando as flutuações, e mostra o ritmo médio de crescimento anual no período.'
    mma = 'A Média Móvel mostra a tendência central e os limites da variação do indicador no período, na forma de uma faixa típica de valores. Essencialmente, nos mostra o caminho e se o indicador está dentro ou fora da variação normal passada.'

    # Extract unique groups (first two digits) from the lines
    groups = set(entry['line'][:2] for entry in lines)
    groups = sorted(groups)
    
    default_graphs = {}
    for group in groups:
        filtered_lines = [entry for entry in lines if entry['line'].startswith(group)]
        default_graphs[group] = {}
        for l, line in enumerate(filtered_lines):
            # Construct graph info based on line data
            default_graphs[group][l] = {}
            default_graphs[group][l][0] = {
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
            #     default_graphs[group][l][1] = {
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
