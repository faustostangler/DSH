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
    manual_entries = []
    return manual_entries

def get_default_lines():
    """
    Provide the default lines' information used to generate the graphs.
    
    Returns:
    - A list of dictionaries containing information about each default line.
    """
    lines_info = [
{
    'line': '00.01.01 - Ações ON',
    'title': '00.01.01 - Ações ON',
    'header': 'Ações Ordinárias Nominativas',
    'footer': 'Ações ON são aquelas que conferem ao acionista o direito de voto. Em quantidades normais, indica uma participação padrão na empresa. Valores ascendentes podem indicar um aumento na confiança dos investidores na governança da empresa. Valores em declínio podem indicar preocupações sobre a governança ou desinteresse dos investidores em ter voz ativa nas decisões da empresa.',
    'description': 'Ações ON (Ordinárias Nominativas) são aquelas que conferem ao acionista o direito de voto nas assembleias da empresa. Esse tipo de ação é comum em empresas que desejam ter um grupo de acionistas com poder de decisão mais ativo. Em geral, os acionistas com ações ON têm maior interesse em acompanhar de perto as operações e estratégias da empresa.', 
}, 
{
    'line': '00.01.02 - Ações ON em Tesouraria',
    'title': '00.01.02 - Ações ON em Tesouraria',
    'header': 'Ações Ordinárias Nominativas em Tesouraria',
    'footer': 'Ações ON em Tesouraria são aquelas que foram recompradas pela empresa e não foram canceladas ou reemitidas. Em quantidades normais, indica uma gestão de capital eficaz. Valores altos podem sinalizar que a empresa vê suas próprias ações como um bom investimento. Valores em declínio podem indicar uma possível reemissão ou venda dessas ações.',
    'description': 'Ações ON em Tesouraria referem-se às ações ordinárias que foram compradas de volta pela empresa e estão retidas em sua tesouraria. Essas ações não têm direito a voto e não recebem dividendos. As empresas recompram suas próprias ações por várias razões, incluindo para recompensar os funcionários ou para melhorar os indicadores financeiros.', 
}, 
{
    'line': '00.02.01 - Ações PN',
    'title': '00.02.01 - Ações PN',
    'header': 'Ações Preferenciais Nominativas',
    'footer': 'Ações PN são aquelas que oferecem preferência no recebimento de dividendos ou no reembolso do capital. Em quantidades normais, indica um equilíbrio na estrutura de capital da empresa. Valores ascendentes podem indicar uma busca por financiamento sem diluir o poder de voto. Valores baixos podem sinalizar uma preferência por financiamento via ações ordinárias ou outras formas.',
    'description': 'Ações PN (Preferenciais Nominativas) não dão direito de voto ou têm esse direito restrito, mas, em contrapartida, oferecem preferência no pagamento de dividendos ou no reembolso do capital em caso de liquidação da empresa. São comuns em empresas que desejam captar recursos sem diluir o controle acionário.', 
}, 
{
    'line': '00.02.01 - Ações PN',
    'title': '00.02.01 - Ações PN',
    'header': 'Ações Preferenciais Nominativas',
    'footer': 'Ações PN são aquelas que oferecem preferência no recebimento de dividendos ou no reembolso do capital. Em quantidades normais, indica um equilíbrio na estrutura de capital da empresa. Valores ascendentes podem indicar uma busca por financiamento sem diluir o poder de voto. Valores baixos podem sinalizar uma preferência por financiamento via ações ordinárias ou outras formas.',
    'description': 'Ações PN (Preferenciais Nominativas) não dão direito de voto ou têm esse direito restrito, mas, em contrapartida, oferecem preferência no pagamento de dividendos ou no reembolso do capital em caso de liquidação da empresa. São comuns em empresas que desejam captar recursos sem diluir o controle acionário.', 
},
    ]
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
    lines_info = get_default_lines()

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
                    'title': line["title"], 
                    'header': line["header"], 
                    'description': line["description"], 
                    'footer': line["footer"], 
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
                        'title': line["title"], 
                        'header': line["header"], 
                        'description': line["description"], 
                        'footer': line["footer"], 
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
