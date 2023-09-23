rules = [
    ['01 - Ativo Total', [('conta_exact', '1')]],
    ['01.01 - Ativo Circulante de Curto Prazo', [('conta_exact', '1.01')]], 
    ['01.01.01 - Caixa e Disponibilidades de Caixa', [
        ('conta_startswith', '1.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['caixa', 'equivalent'])
    ]], 
    ['1.01.01.01 - Caixa and Equivalentes de Caixa', [
        ('conta_startswith', '1.01.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['caixa', 'equivalent', 'banco']),
    ]],
    ['1.01.01.02 - Aplicações Financeiras', [
        ('conta_startswith', '1.01.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['aplica', 'liquidez imediata']),
    ]],
    ['1.01.01.03 - Depósitos and Retidos', [
        ('conta_startswith', '1.01.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['depósito', 'retido', 'débito']),
    ]],
    ['1.01.01.09 - Others', [
        ('conta_startswith', '1.01.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['caixa', 'equivalent', 'banco', 'aplica', 'liquidez imediata', 'depósito', 'retido', 'débito']),
    ]], 
    ['01.01.02 - Aplicações Financeiras', [
        ('conta_startswith', '1.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['aplica', 'depósito', 'reserv', 'saldo', 'centra', 'interfinanceir', 'crédit']),
        ('conta_contains_not', ['1.01.01', '1.01.06']), 
    ]], 
    ['1.01.02.01 - Aplicações ao Custo Amortizado', [
        ('conta_startswith', '1.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['amortiz']),
    ]],
    ['1.01.02.02 - Aplicações a Valor Justo', [
        ('conta_startswith', '1.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['valor justo']),
        ('descricao_contains_not', ['através']),
    ]],
    ['1.01.02.03 - Aplicações através do Resultado', [
        ('conta_startswith', '1.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['resultado']),
        ('descricao_contains_not', ['outro']),
    ]],
    ['1.01.02.09 - Aplicações através de Outros Resultados', [
        ('conta_startswith', '1.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['outro']),
    ]], 
    ['01.01.03 - Contas a Receber', [
        ('conta_startswith', '1.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['conta']), 
    ]], 
    ['1.01.03.01 - Clientes', [
        ('conta_startswith', '1.01.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['cliente']),
    ]], 
    ['1.01.03.09 - Outras Contas a Receber', [
        ('conta_startswith', '1.01.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['conta']),
    ]], 
    ['01.01.04 - Estoques', [
        ('conta_startswith', '1.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['estoq'])
    ]],
    ['1.01.04.01 - Produtos Acabados', [
        ('conta_startswith', '1.01.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['acabad']),
    ]],
    ['1.01.04.02 - Produtos em Elaboração', [
        ('conta_startswith', '1.01.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['elabora']),
    ]],
    ['1.01.04.03 - Adiantamento a Fornecedores', [
        ('conta_startswith', '1.01.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['fornecedor']),
    ]],
    ['1.01.04.09 - Outros Estoques', [
        ('conta_startswith', '1.01.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['estoq']),
    ]],
    ['01.01.05 - Ativos Biológicos', [
        ('conta_startswith', '1.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['biológic']), 
    ]], 
        ['1.01.05.01 - Rebanho Bovino', [
        ('conta_startswith', '1.01.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['rebanho bovino']),
    ]],
    ['1.01.05.02 - Rebanho Equino', [
        ('conta_startswith', '1.01.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['rebanho equino']),
    ]],
    ['1.01.05.09 - Outros', [
        ('conta_startswith', '1.01.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['rebanho bovino', 'rebanho equino']),
    ]],
    ['01.01.06 - Tributos', [
            ('conta_startswith', '1.01.'),
            ('conta_levelmin', 3),
            ('conta_levelmax', 3),
            ('descricao_contains', ['tribut']), 
        ]], 
    ['1.01.06.01 - Tributos Correntes a Recuperar', [
        ('conta_startswith', '1.01.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['tributos correntes a recuperar']),
    ]],
    ['01.01.07 - Despesas', [
        ('conta_startswith', '1.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['despes']), 
    ]], 
    ['1.01.07.01 - Despesas Antecipadas', [
        ('conta_startswith', '1.01.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['antecip']),
    ]],
    ['1.01.07.02 - Despesas de Exercícios Seguintes', [
        ('conta_startswith', '1.01.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['exercício']),
    ]],
    ['1.01.07.03 - Adiantamentos', [
        ('conta_startswith', '1.01.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['adiantamento']),
    ]],
    ['1.01.07.04 - Prêmios de Seguros', [
        ('conta_startswith', '1.01.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['prêmio', 'seguro']),
    ]],
    ['01.01.09 - Outros Ativos Circulantes', [
        ('conta_startswith', '1.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['outr']),
        ('descricao_contains_not', ['aplica', 'depósito', 'reserv', 'saldo', 'centra', 'interfinanceir', 'crédit', 'conta', 'estoque', 'biológic', 'tribut', 'despes']),
        ('conta_contains_not', ['1.01.01', '1.01.02', '1.01.03', '1.01.04', '1.01.05', '1.01.06', '1.01.07'])
    ]], 
    ['1.01.09.09 - Outros', [
        ('conta_startswith', '1.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['outr']),
        ('descricao_contains_not', ['aplica', 'depósito', 'reserv', 'saldo', 'centra', 'interfinanceir', 'crédit', 'conta', 'estoque', 'biológic', 'tribut', 'despes']),
        ('conta_contains_not', ['1.01.01', '1.01.02', '1.01.03', '1.01.04', '1.01.05', '1.01.06', '1.01.07'])
    ]],
    ['01.02 - Ativo Não Circulante de Longo Prazo', [('conta_exact', '1.02')]],
    ['01.02.01 - Ativos Financeiros', [
        ('conta_startswith', '1.02.01'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains_not', ['investiment', 'imobilizad', 'intangív', 'difer']), 
    ]], 
    ['1.02.01.01 - Aplicações Financeiras Avaliadas a Valor Justo', [
        ('conta_startswith', '1.02.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['valor justo']),
        ('descricao_contains_not', ['abrangent', 'resultado'])
    ]],
    ['1.02.01.01.01 - Títulos para Negociação', [
        ('conta_startswith', '1.02.01.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['negocia'])
    ]],
    ['1.02.01.01.02 - Títulos para Venda', [
        ('conta_startswith', '1.02.01.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['venda'])
    ]],
    ['1.02.01.01.03 - Títulos a Valor Justo', [
        ('conta_startswith', '1.02.01.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['just'])
    ]],
    ['1.02.01.01.09 - Outros Titulos e valores mobiliarios', [
        ('conta_startswith', '1.02.01.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['negocia', 'venda', 'just'])
    ]],
    ['1.02.01.02 - Aplicações Financeiras Avaliadas ao Custo Amortizado', [
        ('conta_startswith', '1.02.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['custo amortizado']),
    ]],
    ['1.02.01.02.01 - Títulos Mantidos até o Vencimento', [
        ('conta_startswith', '1.02.01.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['vencimento']),
    ]],
    ['1.02.01.02.02 - Instrumentos Financeiros Derivativos', [
        ('conta_startswith', '1.02.01.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['derivativ']),
    ]],
    ['1.02.01.02.03 - Títulos, Valores Mobiliários e Aplicações Financeiras', [
        ('conta_startswith', '1.02.01.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['mobiliár']),
    ]],
    ['1.02.01.02.04 - Aplicações Financeiras', [
        ('conta_startswith', '1.02.01.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['aplica']),
    ]],
    ['1.02.01.02.05 - Depósitos', [
        ('conta_startswith', '1.02.01.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['depósit']),
    ]],
    ['1.02.01.02.09 - Outros', [
        ('conta_startswith', '1.02.01.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['vencimento', 'derivativ', 'mobiliár', 'aplica', 'depósit']),
    ]], 
    ['1.02.01.03 - Contas a Receber', [
        ('conta_startswith', '1.02.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['conta', 'receber']),
    ]],
    ['1.02.01.03.01 - Clientes', [
        ('conta_startswith', '1.02.01.03.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['client']),
    ]],
    ['1.02.01.03.02 - Outras Contas a Receber', [
        ('conta_startswith', '1.02.01.03.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['cont']),
    ]],
    ['1.02.01.03.09 - Aplicações e Títulos', [
        ('conta_startswith', '1.02.01.03.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['títulos', 'aplica']),
        ('descricao_contains_not', ['client', 'cont'])
    ]],
    ['1.02.01.04 - Estoques', [
        ('conta_startswith', '1.02.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['estoq']),
    ]],
    ['1.02.01.04.01 - Clientes', [
        ('conta_startswith', '1.02.01.04.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['client']),
    ]],
    ['1.02.01.04.02 - Outras Contas a Receber', [
        ('conta_startswith', '1.02.01.04.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['a receber']),
    ]],
     ['1.02.01.04.09 - Outros', [
        ('conta_startswith', '1.02.01.04.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['client', 'a receber']),
    ]],
    ['1.02.01.05 - Ativos Biológicos', [
        ('conta_startswith', '1.02.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['biológic']),
    ]],
    ['1.02.01.06 - Tributos Diferidos', [
        ('conta_startswith', '1.02.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['diferid']),
    ]],
    ['1.02.01.06.01 - Imposto de Renda e Contribuição Social Diferidos', [
        ('conta_startswith', '1.02.01.06.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['imposto de renda', 'contribuição social']),
    ]],
    ['1.02.01.06.09 - Outros Impostos', [
        ('conta_startswith', '1.02.01.06.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['imposto de renda', 'contribuição social']),
    ]],
    ['1.02.01.07 - Despesas Antecipadas', [
        ('conta_startswith', '1.02.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['antecipad']),
    ]],
    ['1.02.01.07.01 - Imposto de Renda e Contribuição Social Diferidos', [
        ('conta_startswith', '1.02.01.07.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['renda', 'contrib'])
    ]],
    ['1.02.01.07.09 - Outros Impostos Diferidos', [
        ('conta_startswith', '1.02.01.07.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['renda', 'contrib'])
    ]],
    ['1.02.01.09 - Outros Ativos Não Circulantes', [
        ('conta_startswith', '1.02.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['outr']),
        ('descricao_contains_not', ['outros resultados abrangentes', 'resultado''custo amortizado', 'conta', 'receber', 'estoq', 'biológic', 'diferid', 'antecipad', 'relacionad']),
    ]],
    ['01.02.02 - Investimentos', [
        ('conta_startswith', '1.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['investiment']), 
    ]], 
    ['1.02.02.01 - Participações Societárias', [
        ('conta_startswith', '1.02.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['societárias']),
    ]],
    ['1.02.02.01.01 - Participações em Coligadas', [
        ('conta_startswith', '1.02.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['coligad']),
    ]],
    ['1.02.02.01.02 - Participações em Controladas em Conjunto', [
        ('conta_startswith', '1.02.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['conjunto']),
    ]],
    ['1.02.02.01.03 - Participações em Controladas', [
        ('conta_startswith', '1.02.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['controlad']),
    ]],
    ['1.02.02.01.04 - Outras Participações Societárias', [
        ('conta_startswith', '1.02.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['societ']),
    ]],
    ['1.02.02.01.09 - Outros Investimentos', [
        ('conta_startswith', '1.02.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['investimentos']),
    ]],
    ['1.02.02.02 - Propriedades para Investimento', [
        ('conta_startswith', '1.02.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['investimento']),
    ]], 
    ['1.02.02.02.01 - Terrenos', [
        ('conta_startswith', '1.02.02.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['terrenos'])
    ]],
    ['1.02.02.02.02 - Propriedades para Investimento', [
        ('conta_startswith', '1.02.02.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['propriedade para invest', 'propriedades para invest'])
    ]],
    ['1.02.02.02.04 - Obras de Arte e Adornos', [
        ('conta_startswith', '1.02.02.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['obras de arte'])
    ]],
    ['1.02.02.02.05 - Ajustes e Reclassificações', [
        ('conta_startswith', '1.02.02.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['ajuste', 'equivalência', 'reclassificação']),
    ]], 
    ['1.02.02.02.09 - Outros Investimentos', [
        ('conta_startswith', '1.02.02.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['outros'])
    ]],
    ['01.02.03 - Imobilizado', [
        ('conta_startswith', '1.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['imobilizad']), 
    ]], 
    ['1.02.03.01 - Imobilizado em Operação', [
        ('conta_startswith', '1.02.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['operação']),
    ]],
    ['1.02.03.02 - Imobilizado em Andamento', [
        ('conta_startswith', '1.02.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['andamento']),
    ]],
    ['1.02.03.03 - Imobilizado Arrendado', [
        ('conta_startswith', '1.02.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['arrendado']),
    ]],
    ['1.02.03.04 - Direito de Uso', [
        ('conta_startswith', '1.02.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['uso']),
    ]], 
    ['01.02.04 - Intangível', [
        ('conta_startswith', '1.02.02'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['intangív']), 
    ]], 
     ['1.02.04.01 - Intangíveis', [
        ('conta_startswith', '1.02.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['intangíveis']),
    ]],
    ['1.02.04.02 - Goodwill', [
        ('conta_startswith', '1.02.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['goodwill']),
    ]], 
   ['01.02.05 - Diferido', [
        ('conta_startswith', '1.02.02'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['difer']), 
    ]], 
    ['2.01.01 - Obrigações Sociais e Trabalhistas', [
        ('conta_startswith', '2.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['sociais']),
    ]],
    ['2.01.01.01 - Obrigações Sociais', [
        ('conta_startswith', '2.01.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['sociais']),
    ]],
    ['2.01.01.02 - Obrigações Trabalhistas', [
        ('conta_startswith', '2.01.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['trabalh']),
    ]],
    ['2.01.02 - Fornecedores', [
        ('conta_startswith', '2.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['fornecedores']),
    ]],
    ['2.01.02.01 - Fornecedores Nacionais', [
        ('conta_startswith', '2.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['nacionais']),
    ]],
    ['2.01.02.02 - Fornecedores Estrangeiros', [
        ('conta_startswith', '2.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['estrangeiros']),
    ]], 
    ['2.01.03 - Obrigações Fiscais', [
        ('conta_startswith', '2.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['fiscais']),
    ]],
    ['2.01.03.01 - Obrigações Fiscais Federais', [
        ('conta_startswith', '2.01.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['federais']),
    ]],
    ['2.01.03.02 - Obrigações Fiscais Estaduais', [
        ('conta_startswith', '2.01.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['estaduais']),
    ]],
    ['2.01.03.03 - Obrigações Fiscais Municipais', [
        ('conta_startswith', '2.01.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['municipais']),
    ]], 
    ['2.01.04 - Empréstimos e Financiamentos', [
        ('conta_startswith', '2.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['empréstimos']),
    ]],
    ['2.01.04.01 - Empréstimos e Financiamentos', [
        ('conta_startswith', '2.01.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['emprést'])
    ]],
    ['2.01.04.01.01 - Em Moeda Nacional', [
        ('conta_startswith', '2.01.04.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['moeda nacion']),
    ]],
    ['2.01.04.01.02 - Em Moeda Estrangeira', [
        ('conta_startswith', '2.01.04.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['moeda estrang']),
    ]],
    ['2.01.04.02 - Debêntures', [
        ('conta_startswith', '2.01.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['debênt'])
    ]],
    ['2.01.04.02.01 - Debêntures', [
        ('conta_startswith', '2.01.04.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['debênt']),
    ]],
    ['2.01.04.02.02 - Empréstimos e Financiamentos', [
        ('conta_startswith', '2.01.04.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['emprést', 'financ', 'leasing', 'arrend']),
        ('descricao_contains_not', ['debênt']),
    ]],
    ['2.01.04.02.03 - Derivativos', [
        ('conta_startswith', '2.01.04.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['deriv']),
        ('descricao_contains_not', ['emprést', 'debênt']),
    ]],
    ['2.01.04.02.04 - Partes Relacionadas', [
        ('conta_startswith', '2.01.04.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['relacion']),
        ('descricao_contains_not', ['deriv', 'emprést', 'debênt']),
    ]], 
    ['2.01.04.03 - Financiamento por Arrendamento Financeiro', [
        ('conta_startswith', '2.01.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['arrend'])
    ]],
    ['2.01.04.03.01 - Arrendamento/Leasing', [
        ('conta_startswith', '2.01.04.03.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['arrend', 'leas']),
    ]],
    ['2.01.04.03.02 - Instrumento Financeiro Derivativo', [
        ('conta_startswith', '2.01.04.03.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['derivativ']),
    ]],
    ['2.01.04.03.03 - Obrigação com Outorga', [
        ('conta_startswith', '2.01.04.03.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['outorga']),
    ]], 
    ['2.01.04.03.09 - Outros', [
        ('conta_startswith', '2.01.04.03.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['outros']),
        ('descricao_contains_not', ['arrend', 'leas', 'derivativ', 'outorga'])
    ]], 
    ['2.01.05 - Outras Obrigações', [
        ('conta_startswith', '2.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['outras']),
    ]],
    ['2.01.05.01 - Passivos com Partes Relacionadas', [
        ('conta_startswith', '2.01.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['partes relacionadas']),
    ]],
    ['2.01.05.01.01 - Débitos com Coligadas', [
        ('conta_startswith', '2.01.05.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['coligad']),
    ]],
    ['2.01.05.01.02 - Débitos com Controladores', [
        ('conta_startswith', '2.01.05.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['controlador']),
    ]],
    ['2.01.05.01.03 - Débitos com Outras Partes Relacionadas', [
        ('conta_startswith', '2.01.05.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['outras', 'relacionad']),
    ]],
    ['2.01.05.01.04 - Débitos com Controladas', [
        ('conta_startswith', '2.01.05.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['controlad']),
    ]],
    ['2.01.05.02 - Outros', [
        ('conta_startswith', '2.01.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['outros']),
    ]] ,
    ['2.01.05.02.01 - Dividendos e JCP a Pagar', [
        ('conta_startswith', '2.01.05.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['dividend', 'jcp']),
    ]],
    ['2.01.05.02.02 - Obrigações por Pagamentos Baseados em Ações', [
        ('conta_startswith', '2.01.05.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['pagament', 'ações']),
    ]],
    ['2.01.05.02.03 - Dividendo Mínimo Obrigatório a Pagar', [
        ('conta_startswith', '2.01.05.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['dividend', 'mínimo', 'obrigatór']),
    ]],
    ['2.01.05.02.04 - Outras Contas a Pagar', [
        ('conta_startswith', '2.01.05.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['outr', 'conta']),
    ]],
    ['2.01.05.02.05 - Others', [
        ('conta_startswith', '2.01.05.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['dividend', 'jcp', 'pagament', 'ações', 'mínimo', 'obrigatór', 'outr', 'conta']),
    ]],
    ['2.01.06 - Provisões', [
        ('conta_startswith', '2.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['provisões']),
    ]],
    ['2.01.06.01 - Provisões para Passivos Ambientais e de Desativação', [
        ('conta_startswith', '2.01.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ambient', 'desativ']),
    ]],
    ['2.01.06.01.01 - Provisões Fiscais', [
        ('conta_startswith', '2.01.06.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['fiscal']),
    ]],
    ['2.01.06.01.02 - Provisões Cíveis', [
        ('conta_startswith', '2.01.06.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['cíve']),
    ]],
    ['2.01.06.01.03 - Provisões Previdenciárias e Trabalhistas', [
        ('conta_startswith', '2.01.06.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['previd', 'trabalh']),
    ]],
    ['2.01.06.01.04 - Provisões para Benefícios a Empregados', [
        ('conta_startswith', '2.01.06.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['benefícios empreg']),
    ]],
    ['2.01.06.01.05 - Provisão para Imposto de Renda e Contribuição Social', [
        ('conta_startswith', '2.01.06.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['imposto renda', 'contribuição social']),
    ]],
    ['2.01.06.01.09 - Outros Provisões', [
        ('conta_startswith', '2.01.06.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['fiscal', 'cíve', 'previd', 'trabalh', 'benefícios empreg', 'imposto renda', 'contribuição social']),
    ]],
    ['2.01.06.02 - Provisões Fiscais', [
        ('conta_startswith', '2.01.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['fiscal']),
    ]],
    ['2.01.06.02.01 - Provisões para Passivos Ambientais e de Desativação', [
        ('conta_startswith', '2.01.06.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['ambient', 'desativ']),
    ]],
    ['2.01.06.02.02 - Provisões para Garantias', [
        ('conta_startswith', '2.01.06.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['garant']),
    ]],
    ['2.01.06.02.03 - Provisões para Reestruturação', [
        ('conta_startswith', '2.01.06.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['reestrut']),
    ]],
    ['2.01.06.02.04 - Outras Provisões', [
        ('conta_startswith', '2.01.06.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['outras prov']),
    ]],
    ['2.01.06.02.05 - Provisão para manutenção', [
        ('conta_startswith', '2.01.06.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['manuten']),
    ]],
    ['2.01.06.02.99 - Outros', [
        ('conta_startswith', '2.01.06.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['ambient', 'desativ', 'garant', 'reestrut', 'outras prov', 'manuten']),
    ]],
    ['2.01.06.03 - Provisões para Benefícios a Empregados', [
        ('conta_startswith', '2.01.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['benefício', 'empregado']),
    ]],
    ['2.01.06.04 - Provisões Cíveis', [
        ('conta_startswith', '2.01.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['cíve']),
    ]],
    ['2.01.06.05 - Provisões para Garantias', [
        ('conta_startswith', '2.01.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['garantia']),
    ]],
    ['2.01.06.06 - Outros', [
        ('conta_startswith', '2.01.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['ambient', 'desativ', 'fiscal', 'benefício', 'empregado', 'cíve', 'garantia']),
    ]],
    ['2.01.07 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados', [
        ('conta_startswith', '2.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['venda']),
    ]],
    ['2.01.07.01 - Passivos sobre Ativos Não-Correntes a Venda', [
        ('conta_startswith', '2.01.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['não-correntes a venda']),
    ]],
    ['2.01.07.01.01 - Passivos Relacionados ao Ativo Mantidos para Venda', [
        ('conta_startswith', '2.01.07.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['ativo mantidos para venda']),
    ]],
    ['2.01.07.01.02 - Parcela Tarifária do Poder Concedente', [
        ('conta_startswith', '2.01.07.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['tarifár']),
    ]],
    ['2.01.07.01.03 - Passivos sobre Ativos de Operações Descontinuadas', [
        ('conta_startswith', '2.01.07.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['operaç']),
    ]],
    ['2.01.07.01.04 - Passivos Não Circulantes Disponíveis para Venda', [
        ('conta_startswith', '2.01.07.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['não circulantes']),
    ]],
    ['2.01.07.02 - Passivos sobre Ativos de Operações Descontinuadas', [
        ('conta_startswith', '2.01.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['operações descontinuadas']),
    ]],
    ['2.01.07.02.01 - Passivo de Operações Descontinuada', [
        ('conta_startswith', '2.01.07.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['descontinuad']),
    ]],
    ['2.01.07.02.02 - Passivos Mantidos para Venda', [
        ('conta_startswith', '2.01.07.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['mantid']),
    ]],
    ['2.01.07.02.03 - Dividendos a Pagar', [
        ('conta_startswith', '2.01.07.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['dividend']),
    ]],
    ['2.02.01 - Empréstimos e Financiamentos', [
        ('conta_startswith', '2.02.01'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['emprést']),
    ]],
    ['2.02.01.01 - Empréstimos e Financiamentos', [
        ('conta_startswith', '2.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['emprést']),
    ]],
    ['2.02.01.01.01 - Em Moeda Nacional', [
        ('conta_startswith', '2.02.01.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['nacional']),
        ('conta_contains_not', ['2.01.04.01.01', '2.01.04.03.01', '2.02.01.03.01'])
    ]],
    ['2.02.01.01.02 - Em Moeda Estrangeira', [
        ('conta_startswith', '2.02.01.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['estrangeira']),
        ('conta_contains_not', ['2.01.04.01.02', '2.01.04.03.02', '2.02.01.03.02'])
    ]], 
    ['2.02.01.02 - Debêntures', [
        ('conta_startswith', '2.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['debên']),
    ]],
    ['2.02.01.02.01 - Debêntures', [
        ('conta_startswith', '2.02.01.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['debên', 'emprést', 'leasing']),
    ]],
    ['2.02.01.02.02 - Derivativos', [
        ('conta_startswith', '2.02.01.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['deriv']),
    ]],
    ['2.02.01.02.03 - Others', [
        ('conta_startswith', '2.02.01.02.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['debên', 'emprést', 'leasing', 'deriv']),
    ]], 
    ['2.02.01.03 - Financiamento por Arrendamento Financeiro', [
        ('conta_startswith', '2.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['arrendamento finan']),
    ]],
    ['2.02.01.03.01 - Arrendamento/Leasing', [
        ('conta_startswith', '2.02.01.03.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['arrend', 'leas', 'mercantil']),
    ]], 
    ['2.02.01.03.09 - Outros', [
        ('conta_startswith', '2.02.01.03.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['arrend', 'leas', 'mercantil']),
    ]], 
    ['2.02.01.04 - Financiamento por Arrendamento', [
        ('conta_startswith', '2.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['arrendamento']),
        ('descricao_contains_not', ['finan'])
    ]],
    ['2.02.02 - Outras Obrigações', [
        ('conta_startswith', '2.02.02'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['outras']),
    ]],
    ['2.02.02.01 - Passivos com Partes Relacionadas', [
        ('conta_startswith', '2.02.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['partes relacionadas']),
    ]],
    ['2.02.02.01.01 - Débitos com Coligadas', [
        ('conta_startswith', '2.02.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['coligadas'])
    ]],
    ['2.02.02.01.02 - Débitos com Controladores', [
        ('conta_startswith', '2.02.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['controladores'])
    ]],
    ['2.02.02.01.03 - Débitos com Outras Partes Relacionadas', [
        ('conta_startswith', '2.02.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['outras', 'partes'])
    ]],
    ['2.02.02.01.04 - Débitos com Controladas', [
        ('conta_startswith', '2.02.02.01.'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['controladas'])
    ]], 
    ['2.02.02.09 - Outros', [
        ('conta_startswith', '2.02.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['outros']),
    ]], 
    ['2.02.03 - Tributos Diferidos', [
        ('conta_startswith', '2.02.03'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['tribut']),
    ]],
    ('2.02.03.01 - Imposto de Renda e Contribuição Social Diferidos', [
        ('conta_startswith', '2.02.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['imposto', 'renda', 'contribuição', 'social', 'diferidos']),
    ]),
    ['2.02.04 - Provisões', [
        ('conta_startswith', '2.02.04'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['provis']),
    ]],
    ['2.02.04.01 - Provisões', [
        ('conta_startswith', '2.02.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['provisõ']),
    ]],
    ['2.02.04.02 - Provisões para Passivos Ambientais e de Desativação', [
        ('conta_startswith', '2.02.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ambient', 'desativ']),
    ]],
    ['2.02.04.03 - Provisões Fiscais Previdenciárias Trabalhistas e Cíveis', [
        ('conta_startswith', '2.02.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['fiscal', 'previd', 'trabalh']),
    ]],
    ['2.02.04.04 - Outras Provisões', [
        ('conta_startswith', '2.02.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['outras']),
    ]],
    ['2.02.04.05 - Provisões Cíveis', [
        ('conta_startswith', '2.02.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['cível']),
    ]],
    ['2.02.04.09 - Outros', [
        ('conta_startswith', '2.02.04.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['provisõ', 'ambient', 'desativ', 'fiscal', 'previd', 'trabalh', 'outras', 'cível']),
    ]],
    ['2.02.05 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados', [
        ('conta_startswith', '2.02.05'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['passiv']),
    ]],
    ['2.02.05.01 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados', [
        ('conta_startswith', '2.02.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['não-correntes a venda e descontinuados']),
    ]],
    ['2.02.05.02 - Passivos sobre Ativos Não-Correntes a Venda', [
        ('conta_startswith', '2.02.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['não-correntes a venda']),
        ('descricao_contains_not', ['descontinuados'])
    ]],
    ['2.02.05.03 - Passivos sobre Ativos de Operações Descontinuadas', [
        ('conta_startswith', '2.02.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['operações descontinuadas']),
    ]],
    ['2.02.05.09 - Outros', [
        ('conta_startswith', '2.02.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['não-correntes a venda e descontinuados', 'não-correntes a venda', 'operações descontinuadas']),
    ]],
    ['2.02.06 - Lucros e Receitas a Apropriar', [
        ('conta_startswith', '2.02.06'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['lucros']),
    ]],
    ['2.02.06.01 - Lucros a Apropriar', [
        ('conta_startswith', '2.02.06'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['lucros']),
    ]],
    ['2.02.06.02 - Receitas a Apropriar', [
        ('conta_startswith', '2.02.06'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['receitas']),
    ]],
    ['2.02.06.03 - Subvenções de Investimento a Apropriar', [
        ('conta_startswith', '2.02.06'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['subvenç']),
    ]],
    ['02.03 - Patrimônio Líquido Consolidado', [('conta_exact', '2.03')]],
    ['2.03.01 - Capital Social Realizado', [
        ('conta_startswith', '2.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['capital social realizado']),
    ]],
    ['2.03.01.01 - Capital Social', [
        ('conta_startswith', '2.03.01'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['capital', 'subscrito', 'nacional', 'estrangeiro', 'ações ordinárias', 'ações preferenciais'])
    ]],
    ['2.03.01.02 - Ações', [
        ('conta_startswith', '2.03.01'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ações'])
    ]],
    ['2.03.01.03 - Emissão', [
        ('conta_startswith', '2.03.01'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['custo', 'emissão', 'títulos patrimoniais'])
    ]],
    ['2.03.01.09 - Outros', [
        ('conta_startswith', '2.03.01'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['capital', 'subscrito', 'nacional', 'estrangeiro', 'ações', 'custo', 'emissão', 'títulos patrimoniais'])
    ]],
    ['2.03.02 - Reservas de Capital', [
        ('conta_startswith', '2.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['reservas de capital']),
    ]],
    ['2.03.02.01 - Adiantamento para Futuro Aumento de Capital', [
        ('conta_startswith', '2.03.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['adiantamento', 'futuro', 'aumento']),
    ]],
    ['2.03.02.02 - Ações em Tesouraria', [
        ('conta_startswith', '2.03.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ações', 'tesouraria']),
    ]],
    ['2.03.02.03 - Ágio na Emissão de Ações', [
        ('conta_startswith', '2.03.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ágio', 'emissão']),
    ]],
    ['2.03.02.04 - Alienação de Bônus de Subscrição', [
        ('conta_startswith', '2.03.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['alienação', 'bônus', 'subscrição']),
    ]],
    ['2.03.02.05 - Opções Outorgadas', [
        ('conta_startswith', '2.03.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['opções', 'outorgadas']),
    ]],
    ['2.03.02.09 - Outros', [
        ('conta_startswith', '2.03.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['adiantamento', 'futuro', 'aumento', 'ações', 'tesouraria', 'ágio', 'emissão', 'alienação', 'bônus', 'subscrição', 'opções', 'outorgadas']),
    ]],
    ['2.03.03 - Reservas de Reavaliação', [
        ('conta_startswith', '2.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['reservas de reavaliação']),
    ]],
    ['2.03.03.01 - Reservas de Reavaliação', [
        ('conta_startswith', '2.03.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['reavaliaç'])
    ]],
    ['2.03.03.02 - Ativos Próprios', [
        ('conta_startswith', '2.03.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['próprio', 'propios', 'própros', 'prórprios', 'própro'])
    ]],
    ['2.03.03.03 - Ativos Controladas', [
        ('conta_startswith', '2.03.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['controlad'])
    ]],
    ['2.03.03.04 - Avaliação Patrimonial', [
        ('conta_startswith', '2.03.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['avaliaç', 'patrimonial', 'patrinomial'])
    ]],
    ['2.03.03.05 - Ajustes de Avaliação Patrimonial', [
        ('conta_startswith', '2.03.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ajust', 'avaliaç'])
    ]],
    ['2.03.03.09 - Outros', [
        ('conta_startswith', '2.03.03.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['reavaliaç', 'próprio', 'propios', 'própros', 'prórprios', 'própro', 'controlad', 'avaliaç', 'patrimonial', 'patrinomial', 'ajust'])
    ]], 
    ['2.03.04 - Reservas de Lucros', [
        ('conta_startswith', '2.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['reservas de lucros']),
    ]],
    ['2.03.04.01 - Reserva de Incentivos Fiscais', [
        ('conta_startswith', '2.03.04'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['incentivos fiscais']),
    ]],
    ['2.03.04.02 - Reservas de Lucros', [
        ('conta_startswith', '2.03.04'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['reservas de lucros']),
    ]],
    ['2.03.04.03 - Reserva Estatutária', [
        ('conta_startswith', '2.03.04'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['estatutári']),
    ]],
    ['2.03.04.04 - Reserva para Contingências', [
        ('conta_startswith', '2.03.04'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['contingên']),
    ]],
    ['2.03.04.05 - Reserva de Lucros a Realizar', [
        ('conta_startswith', '2.03.04'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['lucros a realizar']),
    ]],
    ['2.03.04.09 - Outros', [
        ('conta_startswith', '2.03.04'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['incentivos fiscais', 'reservas de lucros', 'estatutári', 'contingên', 'lucros a realizar'])
    ]], 
    ['2.03.05 - Lucros/Prejuízos Acumulados', [
        ('conta_startswith', '2.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['lucros/prejuízos acumulados']),
    ]],
    ['2.03.06 - Ajustes de Avaliação Patrimonial', [
        ('conta_startswith', '2.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['ajustes de avaliação patrimonial']),
    ]],
    ['2.03.06.01 - Ajustes de Avaliação Patrimonial', [
        ('conta_startswith', '2.03.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ajuste', 'avaliação', 'patrimonial']),
    ]],
    ['2.03.06.02 - Custo Atribuído', [
        ('conta_startswith', '2.03.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['custo atribuído']),
    ]],
    ['2.03.06.03 - Investimentos Permanentes', [
        ('conta_startswith', '2.03.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['investimento permanente']),
    ]],
    ['2.03.06.04 - Ativos Próprios', [
        ('conta_startswith', '2.03.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ativo próprio']),
    ]],
    ['2.03.06.05 - Ajustes acumulados de conversão', [
        ('conta_startswith', '2.03.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ajuste acumulado', 'conversão']),
    ]],
    ['2.03.06.06 - Resultado nas operações com acionistas não controladores', [
        ('conta_startswith', '2.03.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['resultado', 'operação', 'acionista', 'não controlador']),
    ]],
    ['2.03.06.07 - Ganho (Perda) com benefícios pós-emprego', [
        ('conta_startswith', '2.03.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ganho', 'perda', 'benefício', 'pós-emprego']),
    ]],
    ['2.03.06.08 - Ativos de Controladas', [
        ('conta_startswith', '2.03.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ativo controlada']),
    ]],
    ['2.03.06.09 - Outros', [
        ('conta_startswith', '2.03.06.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['ajuste', 'avaliação', 'patrimonial', 'custo atribuído', 
                                    'investimento permanente', 'ativo próprio', 'ajuste acumulado', 
                                    'conversão', 'resultado', 'operação', 'acionista', 'não controlador', 
                                    'ganho', 'perda', 'benefício', 'pós-emprego', 'ativo controlada'])
    ]], 
    ['2.03.07 - Ajustes Acumulados de Conversão', [
        ('conta_startswith', '2.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['ajustes acumulados de conversão']),
    ]],
    ['2.03.07.01 - Ajustes Acumulados de Conversão', [
        ('conta_startswith', '2.03.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ajustes acumulados de conversão'])
    ]],
    ['2.03.07.02 - Debêntures Perpétuas', [
        ('conta_startswith', '2.03.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['debêntures perpétuas'])
    ]],
    ['2.03.07.03 - Créditos Quirografários a Converter', [
        ('conta_startswith', '2.03.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['créditos quirografários a converter'])
    ]],
    ['2.03.07.04 - Ajuste Lei 11.638/07', [
        ('conta_startswith', '2.03.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['ajuste lei 11.638/07'])
    ]],
    ['2.03.07.09 - Outros', [
        ('conta_startswith', '2.03.07.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', [
            'ajustes acumulados de conversão',
            'debêntures perpétuas',
            'créditos quirografários a converter',
            'ajuste lei 11.638/07'
        ])
    ]], 
    ['2.03.08 - Outros Resultados Abrangentes', [
        ('conta_startswith', '2.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['outros resultados abrangentes']),
    ]],
    ['2.03.08.01 - Outros Resultados Abrangentes', [
        ('conta_startswith', '2.03.08.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['abrangent'])
    ]],
    ['2.03.08.02 - Ajustes', [
        ('conta_startswith', '2.03.08.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['ajust'])
    ]],
    ['2.03.08.03 - Equivalência Patrimonial', [
        ('conta_startswith', '2.03.08.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['equivalência'])
    ]],
    ['2.03.08.04 - Transações', [
        ('conta_startswith', '2.03.08.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['transaç'])
    ]],
    ['2.03.08.09 - Outros', [
        ('conta_startswith', '2.03.08.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3)
    ]], 
    ['2.03.09 - Participação dos Acionistas Não Controladores', [
        ('conta_startswith', '2.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['participação dos acionistas não controladores']),
    ]],
    ['3.01 - Receita de Venda de Bens e/ou Serviços', [('conta_exact', '3.01')]],
    ['3.01.01 - Mercado Interno', [
        ('conta_startswith', '3.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['mercado interno']),
    ]],
    ['3.01.02 - Mercado Externo', [
        ('conta_startswith', '3.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['mercado externo']),
    ]],
    ['3.01.03 - Receita bruta de vendas e serviços', [
        ('conta_startswith', '3.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['receita bruta de vendas e serviços']),
    ]],
    ['3.01.04 - Deduções da Receita Bruta', [
        ('conta_startswith', '3.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['deduções da receita bruta']),
    ]],
    ['3.01.05 - Receita Bruta', [
        ('conta_startswith', '3.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['receita bruta']),
    ]],
    ['3.01.09 - Outros', [
        ('conta_startswith', '3.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains_not', ['mercado interno', 'mercado externo', 
                                    'receita bruta de vendas e serviços', 
                                    'deduções da receita bruta', 'receita bruta'])
    ]],
    ['3.02 - Custo dos Bens e/ou Serviços Vendidos', [('conta_exact', '3.02')]],
    ['3.02.01 - Materiais, Equipamentos e Veículos', [
        ('conta_startswith', '3.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['materiais']),
        ('descricao_not_contains', ['serviços', 'construção', 'depreciação', 'outro'])
    ]],
    ['3.02.02 - Serviços', [
        ('conta_startswith', '3.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['serviços']),
        ('descricao_not_contains', ['materiais', 'construção', 'depreciação', 'outro'])
    ]],
    ['3.02.03 - Custo de Construção', [
        ('conta_startswith', '3.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['custo', 'construção']),
        ('descricao_not_contains', ['serviços', 'materiais', 'depreciação', 'outro'])
    ]],
    ['3.02.09 - Outros', [
        ('conta_startswith', '3.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_not_contains', ['serviços', 'materiais', 'construção', 'depreciação'])
    ]], 
    ['3.03 - Resultado Bruto', [('conta_exact', '3.03')]],
    ['3.04 - Despesas e Receitas Operacionais', [('conta_exact', '3.04')]],
    ['3.04.01 - Despesas com Vendas', [
        ('conta_startswith', '3.04.01'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['vend'])
    ]],
    ['3.04.02 - Despesas Gerais e Administrativas', [
        ('conta_startswith', '3.04.02'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['gerais e administr'])
    ]],
    ['3.04.03 - Perdas pela Não Recuperabilidade de Ativos', [
        ('conta_startswith', '3.04.03'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['não recuper'])
    ]],
    ['3.04.04 - Outras Receitas Operacionais', [
        ('conta_startswith', '3.04.04'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['outras receitas oper'])
    ]],
    ['3.04.05 - Outras Despesas Operacionais', [
        ('conta_startswith', '3.04.05'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['outras despesas oper'])
    ]],
    ['3.04.06 - Resultado de Equivalência Patrimonial', [
        ('conta_startswith', '3.04.06'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['equival'])
    ]],
    ['3.05 - LAJIR ou EBIT (Lucro Antes do Resultado Financeiro e dos Tributos)', [('conta_exact', '3.05')]],
    ['3.06 - Resultado Financeiro', [('conta_exact', '3.06')]],
    ['3.06.01 - Receitas Financeiras', [
        ('conta_startswith', '3.06.01'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['receitas financeir']),
    ]],
    ['3.06.02 - Despesas Financeiras', [
        ('conta_startswith', '3.06.02'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['despesas financeir']),
    ]], 
    ['3.07 - Resultado Antes dos Tributos sobre o Lucro', [('conta_exact', '3.07')]],
    ['3.08 - Imposto de Renda e Contribuição Social sobre o Lucro', [('conta_exact', '3.08')]],
    ['3.08.01 - Corrente', [
        ('conta_startswith', '3.08.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['corrent'])
    ]],
    ['3.08.02 - Diferido', [
        ('conta_startswith', '3.08.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['diferid'])
    ]], 
    ['3.09 - Resultado Líquido das Operações Continuadas', [
        ('conta_startswith', '3.'),
        ('conta_levelmax', 2),
        ('descricao_contains', ['continuad']),
        ('descricao_contains_not', ['descontinuad', 'lucro'])
    ]],
    ['3.10 - Resultado Líquido das Operações Descontinuadas', [
        ('conta_startswith', '3.'),
        ('conta_levelmax', 2),
        ('descricao_contains', ['descontinuad']), 
    ]],
    ['3.10.01 - Lucro/Prejuízo Líquido das Operações Descontinuadas', [
        ('conta_startswith', '3.10'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['lucro', 'prejuízo líquido das operações descontinuadas'])
    ]],
    ['3.10.02 - Ganhos/Perdas Líquidas sobre Ativos de Operações Descontinuadas', [
        ('conta_startswith', '3.10'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['ganho', 'perda líquida sobre ativos de operações descontinuadas'])
    ]],
    ['3.11 - Lucro/Prejuízo Consolidado do Período', [
        ('conta_startswith', '3'),
        ('descricao_contains', ['período']),
        ('conta_levelmax', 2),
        ('descricao_contains_not', ['equival', 'líquid'])
    ]],
    ['3.11.01 - Atribuído a Sócios da Empresa Controladora', [
        ('conta_startswith', '3.11.01'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['controlador']),
        ('descricao_contains_not', ['não controlador'])
    ]],
    ['3.11.02 - Atribuído a Sócios Não Controladores', [
        ('conta_startswith', '3.11.02'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['não controlador'])
    ]],
    ['4.01 - Outros Resultados Abrangentes', [
        ('conta_startswith', '4.'),
        ('conta_levelmin', 2),
        ('conta_levelmax', 2),
        ('descricao_contains', ['outros resultados abrang'])
    ]],
    ['4.02 - Lucro Líquido do Período', [
        ('conta_startswith', '4.'),
        ('conta_levelmin', 2),
        ('conta_levelmax', 2),
        ('descricao_contains', ['lucro líquido do período'])
    ]],
    ['4.02.01 - Ajustes Acumulados de Conversão', [
        ('conta_startswith', '4.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['ajustes acumulados de convers']),
    ]],
    ['4.02.02 - Realização da Reserva de Reavaliação', [
        ('conta_startswith', '4.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['realização da reserva de reav']),
    ]],
    ['4.02.03 - Hedge Accounting', [
        ('conta_startswith', '4.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['hedge']),
    ]],
    ['4.02.04 - Reserva de reavaliação reflexa', [
        ('conta_startswith', '4.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['reserva de reavaliação reflex']),
    ]],
    ['4.02.09 - Outros', [
        ('conta_startswith', '4.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains_not', ['ajustes acumulados de convers', 'realização da reserva de reav', 'hedge', 'reserva de reavaliação reflex']),
    ]],
    ['4.03 - Resultado Abrangente do Período', [
        ('conta_startswith', '4.'),
        ('conta_levelmin', 2),
        ('conta_levelmax', 2),
        ('descricao_contains', ['resultado abrangente do período'])
    ]],
    ['4.03.01 - Atribuído a Sócios da Empresa Controladora', [
        ('conta_startswith', '4.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['controlador']),
        ('descricao_contains_not', ['não']),
    ]],
    ['4.03.02 - Atribuído a Sócios Não Controladores', [
        ('conta_startswith', '4.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['não controlador']), 
    ]], 
    ['4.04 - Lucro Líquido Consolidado do Período', [
        ('conta_startswith', '4.'),
        ('conta_levelmin', 2),
        ('conta_levelmax', 2),
        ('descricao_contains', ['lucro líquido consolidado'])
    ]],
    ['4.05 - Resultado Abrangente Consolidado do Período', [
        ('conta_startswith', '4.'),
        ('conta_levelmin', 2),
        ('conta_levelmax', 2),
        ('descricao_contains', ['resultado abrangente consolidado'])
    ]], 
    ['6.01 - Caixa Operacional', [('conta_exact', '6.01')]],
    ['6.01.01 - Caixa Gerado nas Operações', [
        ('conta_startswith', '6.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['caixa gerado nas operações'])
    ]],
    ['6.01.01.01 - Depreciação e Amortização', [
        ('conta_startswith', '6.01.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['deprecia'])
    ]],
    ['6.01.01.02 - Equivalência Patrimonial', [
        ('conta_startswith', '6.01.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', ['equival'])
    ]],
    ['6.01.01.09 - Outros', [
        ('conta_startswith', '6.01.01.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['deprecia', 'equival'])
    ]], 
    ['6.01.02 - Variações nos Ativos e Passivos', [
        ('conta_startswith', '6.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['variações nos ativos e passivos'])
    ]],
    ['6.01.02.01 - Fornecedores', [
        ('conta_startswith', '6.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', 'forneced')
    ]],
    ['6.01.02.02 - Estoques', [
        ('conta_startswith', '6.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', 'estoq')
    ]],
    ['6.01.02.03 - Impostos a recuperar', [
        ('conta_startswith', '6.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', 'impost')
    ]],
    ['6.01.02.04 - Depósitos judiciais', [
        ('conta_startswith', '6.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', 'judic')
    ]],
    ['6.01.02.05 - Outras contas a pagar', [
        ('conta_startswith', '6.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', 'contas')
    ]],
    ['6.01.02.09 - Outros', [
        ('conta_startswith', '6.01.02.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['forneced', 'estoq', 'impost', 'contas'])
    ]], 
    ['6.01.09 - Outros', [
        ('conta_startswith', '6.01.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['outros', 'receita diferida', 'depósitos judiciais']),
    ]], 
    ['6.02 - Caixa Investimento', [('conta_exact', '6.02')]],
    ['6.02.01 - Aquisição de imobilizado', [
        ('conta_startswith', '6.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['imobilizad']),
    ]],
    ['6.02.02 - Investimentos', [
        ('conta_startswith', '6.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['investiment']),
    ]],
    ['6.02.03 - Aquisição de intangível', [
        ('conta_startswith', '6.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['intang']),
    ]],
    ['6.02.09 - Outros', [
        ('conta_startswith', '6.02.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains_not', ['imobilizad', 'investiment', 'intang'])
    ]],
    ['6.03 - Caixa Financiamento', [('conta_exact', '6.03')]],
    ['6.03.01 - Dividendos pagos', [
        ('conta_startswith', '6.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['dividend'])
    ]],
    ['6.03.02 - Empréstimos Pagos', [
        ('conta_startswith', '6.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['empréstimos', 'emprestimo', 'captação de empr']), 
    ]],
    ['6.03.03 - Empréstimos Tomados', [
        ('conta_startswith', '6.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['empréstimos', 'emprestimo']),
        ('descricao_contains_not', ['pagamento'])
    ]],
    ['6.03.04 - Aumento de capital', [
        ('conta_startswith', '6.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['aumento de capital'])
    ]],
    ['6.03.05 - Financiamentos', [
        ('conta_startswith', '6.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['financiament'])
    ]],
    ['6.03.06 - Debêntures', [
        ('conta_startswith', '6.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['debêntur', 'debentur'])
    ]],
    ['6.03.07 - Arrendamento', [
        ('conta_startswith', '6.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['arrendament'])
    ]],
    ['6.03.08 - Mútuos', [
        ('conta_startswith', '6.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['mútuos', 'mutuos'])
    ]],
    ['6.03.09 - Outros', [
        ('conta_startswith', '6.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains_not', ['dividend', 'empréstimos', 'emprestimo', 'captação de empr', 'aumento de capital', 'financiament', 'debêntur', 'debentur', 'arrendament', 'mútuos', 'mutuos'])
    ]], 
    ['6.04 - Variação Cambial', [('conta_exact', '6.04')]],
    ['6.05 - Variação do Caixa', [('conta_exact', '6.05')]],
    ['6.05.01 - Caixa Saldo Inicial', [
        ('conta_startswith', '6.05.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['inicial'])
    ]],
    ['6.05.02 - Caixa Saldo Final', [
        ('conta_startswith', '6.03.'),
        ('conta_levelmin', 3),
        ('conta_levelmax', 3),
        ('descricao_contains', ['fina'])
    ]],
    ['7.01 - Receitas', [
        ('conta_startswith', '7.01'),
        ('conta_levelmin', 2),
        ('conta_levelmax', 2),
        ('descricao_contains', ['receit']),
    ]],
    ['7.01.01 - Vendas de Mercadorias, Produtos e Serviços', [('conta_exact', '7.01.01')]],
    ['7.01.02 - Outras Receitas', [('conta_exact', '7.01.02')]],
    ['7.01.03 - Receitas de Construção de Ativos Próprios', [('conta_exact', '7.01.03')]],
    ['7.01.04 - Reversão de Créditos Liquidação Duvidosa', [('conta_exact', '7.01.04')]],
    ['7.02 - Insumos Adquiridos de Terceiros', [
        ('conta_startswith', '7.02'),
        ('conta_levelmin', 2),
        ('conta_levelmax', 2),
        ('descricao_contains', ['insumos']),
    ]],
    ['7.02.01 - Custo de Mercadorias, Produtos e Serviços', [('conta_exact', '7.02.01')]],
    ['7.02.02 - Materiais, Energia, Serviços de Terceiros e Outros', [('conta_exact', '7.02.02')]],
    ['7.02.03 - Recuperação de Valores Ativos', [('conta_exact', '7.02.03')]],
    ['7.02.04 - Outros', [('conta_exact', '7.02.04')]],
    ['7.03 - Valor Adicionado Bruto', [('conta_exact', '7.03')]],
    ['7.04 - Retenções', [
        ('conta_startswith', '7.04'),
        ('conta_levelmin', 2),
        ('conta_levelmax', 2),
        ('descricao_contains', ['reten']),
    ]],
    ['7.04.01 - Depreciação, Amortização e Exaustão', [('conta_exact', '7.04.01')]],
    ['7.04.02 - Outras	', [('conta_exact', '7.04.02')]],
    ['7.05 - Valor Adicionado Líquido', [('conta_exact', '7.05')]],
    ['7.06 - Vlr Adicionado Recebido em Transferência', [
        ('conta_startswith', '7.06'),
        ('conta_levelmin', 2),
        ('conta_levelmax', 2),
        ('descricao_contains', ['transferên']),
    ]],
    ['7.06.01 - Resultado de Equivalência Patrimonial', [('conta_exact', '7.06.01')]],
    ['7.06.02 - Receitas Financeiras', [('conta_exact', '7.06.02')]],
    ['7.06.03 - Outros', [('conta_exact', '7.06.03')]],
    ['7.07 - Valor Adicionado Total a Distribuir', [('conta_exact', '7.07')]],
    ['7.08 - Distribuição do Valor Adicionado', [('conta_exact', '7.08')]],
    ['7.08.01 - Pessoal', [('conta_exact', '7.08.01')]],
    ['7.08.01.01 - Remuneração Direta', [('conta_exact', '7.08.01.01')]],
    ['7.08.01.02 - Benefícios', [('conta_exact', '7.08.01.02')]],
    ['7.08.01.03 - FGTS', [('conta_exact', '7.08.01.03')]],
    ['7.08.01.04 - Outros', [('conta_exact', '7.08.01.04')]],
    ['7.08.01.04.01 - Participação dos Empregados nos Lucros', [
        ('conta_startswith', '7.08.01.04'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['lucro', 'participa'])
    ]],
    ['7.08.01.04.02 - Comissões sobre Vendas', [
        ('conta_startswith', '7.08.01.04'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['comiss', 'vend'])
    ]],
    ['7.08.01.04.03 - Honorários da Administração', [
        ('conta_startswith', '7.08.01.04'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains', ['honorár', 'adminis'])
    ]],
    ['7.08.01.04.09 - Outros', [
        ('conta_startswith', '7.08.01.04'),
        ('conta_levelmin', 5),
        ('conta_levelmax', 5),
        ('descricao_contains_not', ['lucro', 'participa', 'comiss', 'vend', 'honorár', 'adminis']), 
    ]], 
    ['7.08.02 - Impostos, Taxas e Contribuições', [('conta_exact', '7.08.02')]],
    ['7.08.02.01 - Federais', [('conta_exact', '7.08.02.01')]],
    ['7.08.02.02 - Estaduais', [('conta_exact', '7.08.02.02')]],
    ['7.08.02.03 - Municipais', [('conta_exact', '7.08.02.03')]],
    ['7.08.03 - Remuneração de Capitais de Terceiros', [('conta_exact', '7.08.03')]],
    ['7.08.03.01 - Juros', [('conta_exact', '7.08.03.01')]],
    ['7.08.03.02 - Aluguéis', [('conta_exact', '7.08.03.02')]],
    ['7.08.03.03 - Outras', [('conta_exact', '7.08.03.03')]],
    ['7.08.04 - Remuneração de Capitais Próprios', [('conta_exact', '7.08.04')]],
    ['7.08.04.01 - Juros sobre o Capital Próprio', [('conta_exact', '7.08.04.01')]],
    ['7.08.04.02 - Dividendos', [('conta_exact', '7.08.04.02')]],
    ['7.08.04.03 - Lucros Retidos/Prejuízo do Período', [('conta_exact', '7.08.04.03')]],
    ['7.08.04.04 - Participação dos Não Controladores nos Lucros Retidos', [('conta_exact', '7.08.04.04')]],
    ['7.08.05 - Outros', [('conta_exact', '7.08.05')]],
    ['7.08.05.01 - Lucros (Prejuízo) de Operações Descontinuadas', [
        ('conta_startswith', '7.08.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', 'operações descontinuadas'),
    ]],
    ['7.08.05.02 - Incentivo Fiscal', [
        ('conta_startswith', '7.08.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', 'incentivo fiscal'),
    ]],
    ['7.08.05.03 - Juros', [
        ('conta_startswith', '7.08.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', 'juros'),
    ]],
    ['7.08.05.04 - Reserva Legal', [
        ('conta_startswith', '7.08.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains', 'reserva legal'),
    ]],
    ['7.08.05.09 - Outros', [
        ('conta_startswith', '7.08.05.'),
        ('conta_levelmin', 4),
        ('conta_levelmax', 4),
        ('descricao_contains_not', ['operações descontinuadas', 'incentivo fiscal', 'juros', 'reserva legal']),
    ]], 
]
