import assets.helper as b3
import assets.functions as run
import re

df_columns = run.load_pkl(f'{b3.app_folder}df_columns')

def restrict_level(col):
    """Check if a column name corresponds to level 1 or 2 based on the number of dots."""
    # Splitting the column name by ' - ' and counting the number of dots in the first part
    num_dots = col.split(' - ')[0].count('.')
    
    # If the number of dots is 0 (level 1) or 1 (level 2), return True
    if num_dots in [0, 1]:
        return True
    return False


def default_plots(df):
    # Extracting the relevant columns based on the condition provided
    relevant_columns = [col for col in df.columns if col[0].isdigit() and restrict_level(col)]
    
    # Extracting the unique first levels from the column names and sorting them
    first_levels = sorted(list(set([item[:2] for item in relevant_columns])))

    graphs_grouped = {}

    for level in first_levels:
        graphs = {}
        index = 0  # Reset the index for each level
        for line in relevant_columns:
            if line.startswith(level):
                if df[line].sum() != 'x':
                    graphs[index] = {}
                    graph_dict = {
                        'info': {
                            'title': f'{line}',
                            'header': f'{line}',
                            'footer': f'{line}',
                            'description': f'Linha {line} do balanço estruturado',
                            }, 
                        'data': {
                            'axis': ['Reais (R$)', 'Porcentagem (%)'],
                            'left': [line],
                            'right': [run.cagr(line, df)], 
                            # 'right': [line], 
                            },
                        'options': {
                            'left': {'shape': 'area', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2], },
                            'right': {'shape': 'ine', 'mode': 'standalone', 'normalization': False, 'outliers': False, 'range': 'flexible'}, 
                        }, 
                    }
                    graphs[index][0] = graph_dict  # Add the main graph_dict to the graphs dictionary with the current index
                    # Checking for sub-lines
                    sub_lines = [column for column in df.columns if column.startswith(line.split(' - ')[0] + '.') and column.count('.') == line.count('.') + 1]
                    
                    # If sub_lines exist, create additional graph_dicts for the current index
                    # for sub_line in sub_lines:
                    #     # ... Your logic to define graph_dict for sub_lines goes here ...
                    #     sub_graph_dict_1 = {
                    #         'info': {
                    #             'title': f'{line} - Composição Relativa',
                    #             'header': f'{line}',
                    #             'footer': f'{line}',
                    #             'description': f'Linha {line} do balanço estruturado, com a composição relativa de cada sub-item, que permite visualizar quanto cada item representa em relação ao todo ao longo do tempo',
                    #             }, 
                    #         'data': {
                    #             'axis': ['Porcentagem (%)'],
                    #             'left': sub_lines,
                    #             },
                    #         'options': {
                    #             'left': {'shape': 'line', 'mode': 'standalone', 'normalization': True,},
                    #             }, 
                    #         }
                    #     graphs[index][1] = sub_graph_dict_1

                    index += 1  # Increment the index for the next item
                    # break
        graphs_grouped[level] = graphs
        # break
    
    return graphs_grouped

graphs_default = default_plots(df_columns)

graphs_0 = {
    'Plot Title': {
        'info': {
            'header': 'CardHeader', 
            'footer': 'CardFooter', 
            'description': 'Plot explanation', 
        }, 
        'data': {
            'axis': ['Reais (R$)', 'Unitário (un)'],
            'left': ['01 - Ativo Total', '02.03 - Patrimônio Líquido'],
            'right': ['11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido)']
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'cumulative', 'normalization': True, 'range': 'flexible'},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2]}
        }
    },
    'Equity Multiplier2': {
        'info': {
            'description': 'Plot explanation', 
            # 'description': 'O Multiplicador de Patrimônio Líquido (Equity Multiplier) é uma métrica financeira que avalia a alavancagem financeira de uma empresa, calculada como o total de ativos dividido pelo patrimônio líquido total. Em termos práticos, um valor acima de 2.0 é frequentemente visto como elevado, indicando uma maior dependência de dívidas para financiar ativos e, portanto, um perfil de risco potencialmente mais alto. Valores abaixo de 1.5, por outro lado, são geralmente vistos como baixos, sugerindo uma abordagem financeira mais conservadora com menor alavancagem de dívida, mas possivelmente indicando um crescimento mais cauteloso. ', 
            'header': 'CardHeader', 
            'footer': 'CardFooter', 
        }, 
        'data': {
            'axis': ['Reais (R$)', 'Unitário (un)'],
            'left': ['01 - Ativo Total', '02.03 - Patrimônio Líquido'],
            'right': ['11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido)']
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'standalone', 'normalization': False, 'range': 'flexible'},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False}
        }
    },
}
graphs_1 = {
    'Plot Title2': {
        'info': {
            'description': 'Plot explanation', 
            'header': 'CardHeader', 
            'footer': 'CardFooter', 
        }, 
        'data': {
            'axis': ['Reais (R$)', 'Unitário (un)'],
            'left': ['01 - Ativo Total', '02.03 - Patrimônio Líquido'],
            'right': ['11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido)']
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'cumulative', 'normalization': True, 'range': 'flexible'},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2]}
        }
    },
}

graphs_0 = {
    'Plot Title': {
        'info': {
            'header': 'CardHeader', 
            'footer': 'CardFooter', 
            'description': 'Plot explanation', 
        }, 
        'data': {
            'axis': ['Reais (R$)', 'Unitário (un)'],
            'left': ['01 - Ativo Total', '02.03 - Patrimônio Líquido'],
            'right': ['11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido)']
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'cumulative', 'normalization': True, 'range': 'flexible'},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2]}
        }
    },
    'Equity Multiplier2': {
        'info': {
            'description': 'Plot explanation', 
            # 'description': 'O Multiplicador de Patrimônio Líquido (Equity Multiplier) é uma métrica financeira que avalia a alavancagem financeira de uma empresa, calculada como o total de ativos dividido pelo patrimônio líquido total. Em termos práticos, um valor acima de 2.0 é frequentemente visto como elevado, indicando uma maior dependência de dívidas para financiar ativos e, portanto, um perfil de risco potencialmente mais alto. Valores abaixo de 1.5, por outro lado, são geralmente vistos como baixos, sugerindo uma abordagem financeira mais conservadora com menor alavancagem de dívida, mas possivelmente indicando um crescimento mais cauteloso. ', 
            'header': 'CardHeader', 
            'footer': 'CardFooter', 
        }, 
        'data': {
            'axis': ['Reais (R$)', 'Unitário (un)'],
            'left': ['01 - Ativo Total', '02.03 - Patrimônio Líquido'],
            'right': ['11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido)']
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'standalone', 'normalization': False, 'range': 'flexible'},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False}
        }
    },
}
graphs_1 = {
    'Plot Title2': {
        'info': {
            'description': 'Plot explanation', 
            'header': 'CardHeader', 
            'footer': 'CardFooter', 
        }, 
        'data': {
            'axis': ['Reais (R$)', 'Unitário (un)'],
            'left': ['01 - Ativo Total', '02.03 - Patrimônio Líquido'],
            'right': ['11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido)']
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'cumulative', 'normalization': True, 'range': 'flexible'},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2]}
        }
    },
}

