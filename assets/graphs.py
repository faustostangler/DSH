import assets.helper as b3
import assets.functions as run
import re

def construct_graphs(df):
    # Step 1: Initialize the main dictionary
    graphs_manual = {}


    # Step 2: Add the first section key to the main dictionary
    graphs_manual['01'] = {}

    # Step 3: Add the first line key to the first section
    graphs_manual['01'][0] = {}

    # Step 4: Add the first plot key-value to the first line

    line = '01 - Ativo Total'
    graphs_manual['01'][0][0] = {
        'info': {
            'title': f'{line}',
            'header': f'{line}',
            'footer': f'{line}',
            'description': f'Linha {line} do balanço estruturado. Graph generator'
        },
        'data': {
            'axis': ['Reais (R$)', 'Porcentagem (%)'],
            'left': [line],
            'right': [run.cagr(line, df)]
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2]},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'outliers': False, 'range': 'flexible'}, 
        }, 
    }

    sub_lines = [column for column in df.columns if column.startswith(line.split(' - ')[0] + '.') and column.count('.') == line.count('.') + 1]
    graphs_manual['01'][0][1] = {
        'info': {
            'title': f'{line} - Composição Relativa',
            'header': f'{line} header relativo',
            'footer': f'{line} footer relativo',
            'description': f'{line} description relativa',
        }, 
        'data': {
            'axis': ['Reais (R$)', 'Porcentagem (%)'],
            'left': sub_lines,
            # 'right': ['PLACEHOLDER_for_run.cagr_function_result'],  # Placeholder for run.cagr function
        },
        'options': {
            'left': {'shape': 'line', 'mode': 'standalone', 'normalization': False,},
            # 'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'outliers': False, 'range': 'flexible'}, 
        }
    }

    # -----

    # Step 2: Add the first section key to the main dictionary
    graphs_manual['02'] = {}

    # Step 3: Add the first line key to the first section
    graphs_manual['02'][0] = {}

    # Step 4: Add the first plot key-value to the first line

    line = '02 - Passivo Total'
    graphs_manual['02'][0][0] = {
        'info': {
            'title': f'{line}',
            'header': f'{line}',
            'footer': f'{line}',
            'description': f'Linha {line} do balanço estruturado. Graph generator'
        },
        'data': {
            'axis': ['Reais (R$)', 'Porcentagem (%)'],
            'left': [line],
            'right': [run.cagr(line, df)]
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2]},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'outliers': False, 'range': 'flexible'}, 
        }, 
    }

    sub_lines = [column for column in df.columns if column.startswith(line.split(' - ')[0] + '.') and column.count('.') == line.count('.') + 1]

    graphs_manual['02'][0][1] = {
        'info': {
            'title': f'{line} - Composição Relativa',
            'header': f'{line} header relativo',
            'footer': f'{line} footer relativo',
            'description': f'{line} description relativa',
        }, 
        'data': {
            'axis': ['Reais (R$)', 'Porcentagem (%)'],
            'left': sub_lines,
            # 'right': ['PLACEHOLDER_for_run.cagr_function_result'],  # Placeholder for run.cagr function
        },
        'options': {
            'left': {'shape': 'line', 'mode': 'standalone', 'normalization': False,},
            # 'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'outliers': False, 'range': 'flexible'}, 
        }
    }

    # -----

    # Step 2: Add the first section key to the main dictionary
    graphs_manual['03'] = {}

    # Step 3: Add the first line key to the first section
    graphs_manual['03'][0] = {}

    # Step 4: Add the first plot key-value to the first line

    line = '03.11 - Lucro Líquido'
    graphs_manual['03'][0][0] = {
        'info': {
            'title': f'{line}',
            'header': f'{line}',
            'footer': f'{line}',
            'description': f'Linha {line} do balanço estruturado. Graph generator'
        },
        'data': {
            'axis': ['Reais (R$)', 'Porcentagem (%)'],
            'left': [line],
            'right': [run.cagr(line, df)]
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'standalone', 'normalization': False, 'mma': [3, 2]},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'outliers': False, 'range': 'flexible'}, 
        }, 
    }

    sub_lines = [column for column in df.columns if column.startswith(line.split(' - ')[0] + '.') and column.count('.') == line.count('.') + 1]

    graphs_manual['03'][0][1] = {
        'info': {
            'title': f'{line} - Composição Relativa',
            'header': f'{line} header relativo',
            'footer': f'{line} footer relativo',
            'description': f'{line} description relativa',
        }, 
        'data': {
            'axis': ['Reais (R$)', 'Porcentagem (%)'],
            'left': sub_lines,
            # 'right': ['PLACEHOLDER_for_run.cagr_function_result'],  # Placeholder for run.cagr function
        },
        'options': {
            'left': {'shape': 'line', 'mode': 'standalone', 'normalization': False,},
            # 'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False, 'outliers': False, 'range': 'flexible'}, 
        }
    }
    return graphs_manual

