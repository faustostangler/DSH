graphs_1 = {
    'Equity Multiplier': {
        'description': 'bla-bla-bla equity', 
        'data': {
            'title': ['Equity Multiplier', 'Reais (R$)', 'Porcentagem (%)'],
            'left': ['01 - Ativo Total', '02.03 - Patrimônio Líquido'],
            'right': ['11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido)']
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'cumulative', 'normalization': True, 'range': 'flexible'},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': False}
        }
    },
}
graphs_2 = {
    'Proporção dos Ativos': {
        'description': 'bla-bla-bla equity', 
        'data': {
            'title': ['Proporção dos Ativos', 'Reais (R$)', 'Porcentagem (%)'],
            'left': ['11.01.03 - Ativos Circulantes de Curto Prazo por Ativos', '11.01.04 - Ativos Não Circulantes de Longo Prazo por Ativos'],
            'right': []
        },
        'options': {
            'left': {'shape': 'area', 'mode': 'cumulative', 'normalization': True, 'range': 'flexible'},
            'right': {'shape': 'line', 'mode': 'standalone', 'normalization': True}
        }
    }
}

