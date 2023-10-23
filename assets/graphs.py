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
    lines_info = [
{
    'line': '00.01.01 - Ações ON',
    'title': '00.01.01 - Ações ON',
    'header': 'Ações Ordinárias Nominativas',
    'description': 'Quantidades normais de Ações ON indicam uma participação padrão na empresa. Valores ascendentes mostram confiança na governança da empresa, enquanto declínios podem refletir preocupações sobre a governança.',
    'footer': 'Ações ON, ou Ações Ordinárias Nominativas, são uma das formas mais tradicionais de investimento no mercado acionário. Ao adquirir uma ação ON, o investidor passa a ser um dos proprietários da empresa, mesmo que de forma parcial, e tem o direito de participar das decisões da empresa através do voto em assembleias. Diferentemente das ações preferenciais (PN), que em muitos casos não concedem direito de voto ou o restringem, as ações ON garantem essa participação ativa. Se pensarmos em uma grande empresa como uma cidade, as ações ON seriam como os títulos de cidadania que permitem a participação em decisões importantes da cidade.', 
},
{
    'line': '00.01.02 - Ações ON em Tesouraria',
    'title': '00.01.02 - Ações ON em Tesouraria',
    'header': 'Ações Ordinárias Nominativas em Tesouraria',
    'description': 'Ações ON em Tesouraria em quantidades normais sugerem uma gestão eficaz do capital. Altas quantidades podem indicar que a empresa vê valor em suas próprias ações, enquanto declínios podem sinalizar potenciais reemissões.',
    'footer': 'As Ações ON em Tesouraria surgem quando uma empresa, por alguma razão estratégica, decide recomprar suas próprias ações no mercado. Estas ações, após serem recompradas, não são destruídas, mas sim mantidas em tesouraria e podem ser reemitidas no futuro, se a empresa assim decidir. Esta estratégia pode ser adotada por diversos motivos, desde a empresa acreditar que suas ações estão sendo subavaliadas no mercado e, portanto, seriam um bom investimento, até a necessidade de cumprir obrigações com programas de remuneração baseados em ações. Se pensarmos em um artista que produz diversas obras de arte, as Ações em Tesouraria seriam como as obras que ele decide não vender e manter em sua coleção pessoal, podendo, no futuro, decidir vendê-las ou usá-las de outra forma.', 
},
{
    'line': '00.02.01 - Ações PN',
    'title': '00.02.01 - Ações PN',
    'header': 'Ações Preferenciais Nominativas',
    'description': 'Ações PN em quantidades normais mostram equilíbrio na estrutura de capital da empresa. Valores ascendentes podem refletir busca por financiamento sem diluição de controle, enquanto declínios sugerem preferência por outras formas de financiamento.',
    'footer': 'Ações PN, ou Ações Preferenciais Nominativas, são aquelas que conferem a seus detentores alguns privilégios em relação às ações ordinárias, especialmente no que tange ao recebimento de dividendos ou reembolso de capital. Diferentemente das ações ON, as ações PN não dão direito pleno de voto nas assembleias, mas em compensação, oferecem vantagens como receber dividendos antes ou receber um valor maior em dividendos. Também, em caso de venda ou liquidação da empresa, os detentores de ações PN têm prioridade no recebimento dos valores. Pense em uma sala de cinema onde alguns assentos são mais confortáveis e oferecem uma visão privilegiada da tela. Quem possui esses assentos talvez não possa escolher o filme que será exibido, mas com certeza terá uma experiência de visualização superior.', 
},
{
    'line': '00.02.02 - Ações PN em Tesouraria',
    'title': '00.02.02 - Ações PN em Tesouraria',
    'header': 'Ações Preferenciais Nominativas em Tesouraria',
    'description': 'Quantidades normais de Ações PN em Tesouraria indicam gestão eficaz do capital. Altas quantidades podem sinalizar que a empresa vê valor em suas ações preferenciais, enquanto declínios podem indicar futuras reemissões.',
    'footer': 'As Ações PN em Tesouraria são, basicamente, ações preferenciais que a empresa decidiu recomprar e manter em sua posse, sem destruí-las. Isso pode ocorrer por diversas razões, desde a empresa considerar que suas ações estão subvalorizadas no mercado, até a necessidade de atender a programas de remuneração baseados em ações para seus executivos. Estas ações, enquanto em tesouraria, não têm direito a voto e não recebem dividendos. A melhor forma de compreender isso é pensar em um escritor famoso que, ao ver seus livros sendo vendidos por um preço muito baixo, decide comprá-los e guardá-los. Ele acredita no valor de sua obra e decide que, no momento certo, pode vendê-los por um valor mais justo ou até mesmo distribuí-los de alguma forma especial.', 
},
{
    'line': '01 - Ativo Total',
    'title': '01 - Ativo Total',
    'header': 'Totalidade dos Bens e Direitos',
    'description': 'O Ativo Total representa a soma de todos os bens e direitos que uma empresa possui em um determinado momento. Valores ascendentes podem indicar crescimento e expansão da empresa, enquanto declínios podem sinalizar venda de ativos ou redução das operações.',
    'footer': 'O Ativo Total é a consolidação de todos os recursos controlados por uma entidade, resultantes de eventos passados e dos quais se espera que a entidade obtenha benefícios econômicos futuros. É a combinação dos ativos circulantes (aqueles que serão convertidos em dinheiro ou consumidos no ciclo operacional) e dos ativos não circulantes (bens e direitos que não serão convertidos em dinheiro no curto prazo). Pense no Ativo Total como uma grande caixa onde uma empresa armazena tudo o que possui, desde dinheiro em caixa até prédios e maquinários.', 
},
{
    'line': '01.01 - Ativo Circulante de Curto Prazo',
    'title': '01.01 - Ativo Circulante de Curto Prazo',
    'header': 'Bens e Direitos de Curto Prazo',
    'description': 'O Ativo Circulante refere-se a bens e direitos que serão convertidos em dinheiro ou consumidos no ciclo operacional da empresa, geralmente dentro de um ano. Aumentos podem indicar maior liquidez, enquanto declínios podem sugerir problemas de caixa iminente.',
    'footer': 'O Ativo Circulante de Curto Prazo engloba os recursos que a empresa espera converter em dinheiro ou consumir em um período tipicamente de até um ano. Isso inclui itens como dinheiro em caixa, contas a receber, estoques e outros ativos que são rapidamente líquidos. Imagine que você tem uma mochila onde guarda tudo o que vai usar durante o dia: sua carteira, chaves, lanche, celular e carregador. Esta mochila é semelhante ao Ativo Circulante, pois contém itens que você espera usar ou consumir rapidamente.', 
},
{
    'line': '01.01.01 - Caixa e Disponibilidades de Caixa',
    'title': '01.01.01 - Caixa e Disponibilidades de Caixa',
    'header': 'Recursos Financeiros Imediatos',
    'description': 'Representa o dinheiro disponível imediatamente para a empresa, seja em caixa ou em contas bancárias. Aumentos significam mais liquidez imediata, enquanto declínios podem sinalizar problemas de fluxo de caixa.',
    'footer': 'O "Caixa e Disponibilidades de Caixa" refere-se ao dinheiro que a empresa tem em mãos e em suas contas bancárias. Estes são os recursos mais líquidos que uma empresa possui e podem ser usados imediatamente para pagar dívidas, fazer investimentos ou cobrir despesas operacionais. Pense nisso como o dinheiro que você tem na carteira e na conta corrente: é de fácil acesso e pode ser usado a qualquer momento.', 
},
{
    'line': '01.01.02 - Aplicações Financeiras',
    'title': '01.01.02 - Aplicações Financeiras',
    'header': 'Investimentos de Curto Prazo',
    'description': 'Referem-se a investimentos que a empresa fez com a expectativa de retorno financeiro em curto prazo. Aumentos podem indicar uma boa gestão de caixa, enquanto declínios podem sinalizar resgates para cobrir necessidades de caixa.',
    'footer': 'Aplicações Financeiras são investimentos realizados por empresas em produtos financeiros, como CDBs, fundos de investimento ou títulos públicos, com o objetivo de obter um retorno financeiro. Estes investimentos são geralmente feitos com excessos de caixa, ou seja, dinheiro que a empresa não precisa usar imediatamente. Pense nisso como quando você decide colocar parte do seu salário em uma poupança ou em um fundo de investimento: você espera que esse dinheiro cresça ao longo do tempo.', 
},
{
    'line': '01.01.03 - Contas a Receber',
    'title': '01.01.03 - Contas a Receber',
    'header': 'Valores a Serem Recebidos',
    'description': 'São valores que a empresa tem direito de receber por vendas ou serviços prestados. Aumentos podem indicar boas vendas a prazo, enquanto declínios podem sinalizar recebimentos ou problemas nas vendas.',
    'footer': 'Contas a Receber representam as vendas ou serviços que uma empresa realizou, mas pelos quais ainda não recebeu pagamento. É uma forma de crédito que as empresas oferecem a seus clientes. Imagine que você tenha vendido um objeto antigo para um amigo, mas ele te pagará apenas no próximo mês. Esse valor que ele te deve é semelhante a uma "conta a receber" em seu orçamento pessoal.', 
},
{
    'line': '01.01.04 - Estoques',
    'title': '01.01.04 - Estoques',
    'header': 'Produtos em Armazenamento',
    'description': 'São os bens que a empresa tem armazenados para venda ou uso em produção. Aumentos podem indicar produção acima das vendas, enquanto declínios podem sinalizar vendas robustas ou problemas de produção.',
    'footer': 'Estoques compreendem todos os produtos e materiais que uma empresa tem em armazenamento, seja para venda direta ou para serem usados na produção de outros bens. Estes itens são fundamentais para o funcionamento contínuo das operações. Pense nos estoques como a despensa da sua casa: você armazena alimentos e outros itens essenciais para garantir que terá o que precisa nos próximos dias ou semanas.', 
},

    ]

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
    cagr = 'O CAGR, ou Taxa de Crescimento Anual Composta, avalia o crescimento médio anual do indicador ao longo do perído, ignorando as flutuações, e mostra o ritmo médio de crescimento anual no período.'
    mma = 'A Média Móvel mostra a tendência central e os limites do indicador e sua variação usual no período, na forma de uma faixa típica de valores. Essencialmente, nos mostra o caminho e se o indicador está dentro ou fora da variação normal passada.'

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
                    'description': f'{line["description"]} {mma} {cagr}', 
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
