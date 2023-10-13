graphs_0 = {
    'Equity Multiplier': {
        'description': 'O Multiplicador de Patrimônio Líquido (Equity Multiplier) é uma métrica financeira que avalia a alavancagem financeira de uma empresa, calculada como o total de ativos dividido pelo patrimônio líquido total. Em termos práticos, um valor acima de 2.0 é frequentemente visto como elevado, indicando uma maior dependência de dívidas para financiar ativos e, portanto, um perfil de risco potencialmente mais alto. Valores abaixo de 1.5, por outro lado, são geralmente vistos como baixos, sugerindo uma abordagem financeira mais conservadora com menor alavancagem de dívida, mas possivelmente indicando um crescimento mais cauteloso. ', 
        'data': {
            'title': ['Equity Multiplier', 'Reais (R$)', 'Unitário (un)'],
            'left': ['01 - Ativo Total', '02.03 - Patrimônio Líquido'],
            'right': ['11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido)']
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'cumulative', 'normalization': True, 'range': 'flexible'},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False}
        }
    },
    'Equity Multiplier2': {
        'description': 'bla-bla-bla equity', 
        'data': {
            'title': ['Equity Multiplier - 2', 'Reais (R$)', 'Unitário (un)'],
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
    'Proporção dos Ativos': {
        'description': 'bla-bla-bla equity', 
        'data': {
            'title': ['Proporção dos Ativos', 'Reais (R$)', 'Unitário (un)'],
            'left': ['11.01.03 - Ativos Circulantes de Curto Prazo por Ativos', '11.01.04 - Ativos Não Circulantes de Longo Prazo por Ativos'],
            'right': []
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'cumulative', 'normalization': True, 'range': 'flexible'},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': True}
        }
    }
}

