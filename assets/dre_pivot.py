columns = [
'Companhia', 
'Trimestre',
'00.01 - Ações Ordinárias - Composição do Capital', 
'00.01.01 - Ações Ordinárias em Tesouraria - Composição do Capital', 
'00.01.02 - Ações Ordinárias Outras - Composição do Capital', 
'00.02 - Ações Preferenciais - Composição do Capital', 
'00.02.01 - Ações Prerenciais em Tesouraria - Composição do Capital', 
'00.02.02 - Ações Prerenciais Outras - Composição do Capital', 
'01 - Ativo Total - Balanço Patrimonial Ativo', 
'01.01 - Ativo Circulante de Curto Prazo - Balanço Patrimonial Ativo', 
'01.01.01 - Caixa e Disponibilidades de Caixa - Balanço Patrimonial Ativo', 
'01.01.02 - Aplicações Financeiras - Balanço Patrimonial Ativo', 
'01.01.03 - Contas a Receber - Balanço Patrimonial Ativo', 
'01.01.04 - Estoques - Balanço Patrimonial Ativo', 
'01.01.05 - Ativos Biológicos - Balanço Patrimonial Ativo', 
'01.01.06 - Tributos - Balanço Patrimonial Ativo', 
'01.01.07 - Despesas - Balanço Patrimonial Ativo', 
'01.01.09 - Outros Ativos Circulantes - Balanço Patrimonial Ativo', 
'01.02 - Ativo Não Circulante de Longo Prazo - Balanço Patrimonial Ativo', 
'01.02.01 - Ativos Financeiros - Balanço Patrimonial Ativo', 
'01.02.01.01 - Ativos Financeiros a Valor Justo - Balanço Patrimonial Ativo', 
'01.02.01.02 - Ativos Financeiros ao Custo Amortizado - Balanço Patrimonial Ativo', 
'01.02.01.03 - Contas a Receber - Balanço Patrimonial Ativo', 
'01.02.01.04 - Estoques - Balanço Patrimonial Ativo', 
'01.02.01.05 - Ativos Biológicos - Balanço Patrimonial Ativo', 
'01.02.01.06 - Tributos - Balanço Patrimonial Ativo', 
'01.02.01.07 - Despesas - Balanço Patrimonial Ativo', 
'01.02.01.09 - Outros Ativos Não Circulantes - Balanço Patrimonial Ativo', 
'01.02.02 - Investimentos Não Capex - Balanço Patrimonial Ativo', 
'01.02.02.01 - Propriedades - Balanço Patrimonial Ativo', 
'01.02.02.02 - Arrendamentos - Balanço Patrimonial Ativo', 
'01.02.03 - Imobilizados - Balanço Patrimonial Ativo', 
'01.02.03.01 - Imobilizados em Operação - Balanço Patrimonial Ativo', 
'01.02.03.02 - Imobilizados em Arrendamento - Balanço Patrimonial Ativo', 
'01.02.03.03 - Imobilizados em Andamento - Balanço Patrimonial Ativo', 
'01.02.04 - Intangível - Balanço Patrimonial Ativo', 
'01.03 - Empréstimos - Balanço Patrimonial Ativo', 
'01.04 - Tributos Diferidos - Balanço Patrimonial Ativo', 
'01.05 - Investimentos - Balanço Patrimonial Ativo', 
'01.05.01 - Participações em Coligadas - Balanço Patrimonial Ativo', 
'01.05.02 - Participações em Controladas - Balanço Patrimonial Ativo', 
'01.06 - Imobilizados - Balanço Patrimonial Ativo', 
'01.06.01 - Propriedades - Balanço Patrimonial Ativo', 
'01.06.02 - Arrendamento - Balanço Patrimonial Ativo', 
'01.06.03 - Tangíveis - Balanço Patrimonial Ativo', 
'01.07 - Intangíveis - Balanço Patrimonial Ativo', 
'01.07.01 - Intangíveis - Balanço Patrimonial Ativo', 
'01.07.02 - Goodwill - Balanço Patrimonial Ativo', 
'01.08 - Permanente - Balanço Patrimonial Ativo', 
'01.09.09 - Outros Ativos - Balanço Patrimonial Ativo', 
'02 - Passivo Total - Balanço Patrimonial Passivo', 
'02.01 - Passivo Circulante de Curto Prazo - Balanço Patrimonial Passivo', 
'02.01.01 - Obrigações Sociais e Trabalhistas - Balanço Patrimonial Passivo', 
'02.01.01.01 - Obrigações Sociais - Balanço Patrimonial Passivo', 
'02.01.01.02 - Obrigações Trabalhistas - Balanço Patrimonial Passivo', 
'02.01.01.09 - Outras Obrigações - Balanço Patrimonial Passivo', 
'02.01.02 - Fornecedores - Balanço Patrimonial Passivo', 
'02.01.02.01 - Fornecedores Nacionais - Balanço Patrimonial Passivo', 
'02.01.02.02 - Fornecedores Estrangeiros - Balanço Patrimonial Passivo', 
'02.01.03 - Obrigações Fiscais - Balanço Patrimonial Passivo', 
'02.01.03.01 - Obrigações Fiscais Federais - Balanço Patrimonial Passivo', 
'02.01.03.02 - Obrigações Fiscais Estaduais - Balanço Patrimonial Passivo', 
'02.01.03.03 - Obrigações Fiscais Municipais - Balanço Patrimonial Passivo', 
'02.01.03.09 - Outras Obrigações Fiscais - Balanço Patrimonial Passivo', 
'02.01.04 - Empréstimos, Financiamentos e Debêntures - Balanço Patrimonial Passivo', 
'02.01.04.01 - Empréstimos e Financiamentos - Balanço Patrimonial Passivo', 
'02.01.04.01.01 - Empréstimos e Financiamentos em Moeda Nacional - Balanço Patrimonial Passivo', 
'02.01.04.01.02 - Empréstimos e Financiamentos em Moeda Estrangeira - Balanço Patrimonial Passivo', 
'02.01.04.02 - Debêntures - Balanço Patrimonial Passivo', 
'02.01.04.03 - Arrendamentos - Balanço Patrimonial Passivo', 
'02.01.04.09 - Outros empréstimos, financiamentos e debêntures - Balanço Patrimonial Passivo', 
'02.01.05 - Outras Obrigações - Balanço Patrimonial Passivo', 
'02.01.05.01 - Passivos com Partes Relacionadas - Balanço Patrimonial Passivo', 
'02.01.05.09 - Outros - Balanço Patrimonial Passivo', 
'02.01.06 - Provisões - Balanço Patrimonial Passivo', 
'02.01.06.01 - Provisões Específicas - Balanço Patrimonial Passivo', 
'02.01.06.01.01 - Provisões Fiscais - Balanço Patrimonial Passivo', 
'02.01.06.01.02 - Provisões Trabalhistas e Previdenciárias - Balanço Patrimonial Passivo', 
'02.01.06.01.03 - Provisões para Benefícios a Empregados - Balanço Patrimonial Passivo', 
'02.01.06.01.04 - Provisões Judiciais Cíveis - Balanço Patrimonial Passivo', 
'02.01.06.01.05 - Outras Provisões Específicas - Balanço Patrimonial Passivo', 
'02.01.06.02 - Provisões Outras - Balanço Patrimonial Passivo', 
'02.01.06.02.01 - Provisões para Garantias - Balanço Patrimonial Passivo', 
'02.01.06.02.02 - Provisões para Reestruturação - Balanço Patrimonial Passivo', 
'02.01.06.02.03 - Provisões para Passivos Ambientais e de Desativação - Balanço Patrimonial Passivo', 
'02.01.07 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados - Balanço Patrimonial Passivo', 
'02.01.07.01 - Passivos sobre Ativos Não-Correntes a Venda - Balanço Patrimonial Passivo', 
'02.01.07.02 - Passivos sobre Ativos de Operações Descontinuadas - Balanço Patrimonial Passivo', 
'02.01.09 - Outros Passivos - Balanço Patrimonial Passivo', 
'02.02 - Passivo Não Circulante de Longo Prazo - Balanço Patrimonial Passivo', 
'02.02.01 - Empréstimos e Financiamentos de Longo Prazo - Balanço Patrimonial Passivo', 
'02.02.01.01 - Empréstimos e Financiamentos - Balanço Patrimonial Passivo', 
'02.02.01.01.01 - Empréstimos e Financiamentos em Moeda Nacional - Balanço Patrimonial Passivo', 
'02.02.01.01.02 - Empréstimos e Financiamentos em Moeda Estrangeira - Balanço Patrimonial Passivo', 
'02.02.01.02 - Debêntures - Balanço Patrimonial Passivo', 
'02.02.01.03 - Arrendamentos - Balanço Patrimonial Passivo', 
'02.02.02 - Outras Obrigações - Balanço Patrimonial Passivo', 
'02.02.02.01 - Com Partes Relacionadas - Balanço Patrimonial Passivo', 
'02.02.02.02 - Outras Obrigações - Balanço Patrimonial Passivo', 
'02.02.02.09 - Outros empréstimos, financiamentos e debêntures - Balanço Patrimonial Passivo', 
'02.02.03 - Tributos Diferidos - Balanço Patrimonial Passivo', 
'02.02.03.01 - Imposto de Renda e Contribuição Social - Balanço Patrimonial Passivo', 
'02.02.03.02 - Outros tributos diferidos - Balanço Patrimonial Passivo', 
'02.02.04 - Provisões - Balanço Patrimonial Passivo', 
'02.02.04.01 - Provisões Específicas - Balanço Patrimonial Passivo', 
'02.02.04.01.01 - Provisões Fiscais - Balanço Patrimonial Passivo', 
'02.02.04.01.02 - Provisões Trabalhistas e Previdenciárias - Balanço Patrimonial Passivo', 
'02.02.04.01.03 - Provisões para Benefícios a Empregados - Balanço Patrimonial Passivo', 
'02.02.04.01.04 - Provisões Judiciais Cíveis - Balanço Patrimonial Passivo', 
'02.02.04.02 - Outras Provisões - Balanço Patrimonial Passivo', 
'02.02.04.02.01 - Provisões para Garantias - Balanço Patrimonial Passivo', 
'02.02.04.02.02 - Provisões para Reestruturação - Balanço Patrimonial Passivo', 
'02.02.04.02.03 - Provisões para Passivos Ambientais e de Desativação - Balanço Patrimonial Passivo', 
'02.02.05 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados - Balanço Patrimonial Passivo', 
'02.02.05.01 - Passivos sobre Ativos Não-Correntes a Venda - Balanço Patrimonial Passivo', 
'02.02.05.02 - Passivos sobre Ativos de Operações Descontinuadas - Balanço Patrimonial Passivo', 
'02.02.06 - Lucros e Receitas a Apropriar - Balanço Patrimonial Passivo', 
'02.02.06.01 - Lucros a Apropriar - Balanço Patrimonial Passivo', 
'02.02.06.02 - Receitas a Apropriar - Balanço Patrimonial Passivo', 
'02.02.06.03 - Subvenções de Investimento a Apropriar - Balanço Patrimonial Passivo', 
'02.02.09 - Outros Passivos - Balanço Patrimonial Passivo', 
'02.03 - Patrimônio Líquido - Balanço Patrimonial Passivo', 
'02.03.01 - Capital Social - Balanço Patrimonial Passivo', 
'02.03.02 - Reservas de Capital - Balanço Patrimonial Passivo', 
'02.03.03 - Reservas de Reavaliação - Balanço Patrimonial Passivo', 
'02.03.04 - Reservas de Lucros - Balanço Patrimonial Passivo', 
'02.03.05 - Lucros ou Prejuízos Acumulados - Balanço Patrimonial Passivo', 
'02.03.06 - Ajustes de Avaliação Patrimonial - Balanço Patrimonial Passivo', 
'02.03.07 - Ajustes Acumulados de Conversão - Balanço Patrimonial Passivo', 
'02.03.08 - Outros Resultados Abrangentes - Balanço Patrimonial Passivo', 
'02.04 - Outros Passivos ou Provissões - Balanço Patrimonial Passivo', 
'03.01 - Receita Bruta - Demonstração do Resultado', 
'03.02 - Custo de Produção - Demonstração do Resultado', 
'03.03 - Resultado Bruto (Receita Líquida) - Demonstração do Resultado', 
'03.04 - Despesas Operacionais - Demonstração do Resultado', 
'03.04.01 - Despesas com Vendas - Demonstração do Resultado', 
'03.04.02 - Despesas Gerais e Administrativas - Demonstração do Resultado', 
'03.04.09 - Outras despesas, receitas ou equivalências - Demonstração do Resultado', 
'03.05 - LAJIR EBIT Resultado Antes do Resultado Financeiro e dos Tributos - Demonstração do Resultado', 
'03.06 - Resultado Financeiro (Não Operacional) - Demonstração do Resultado', 
'03.07 - Resultado Antes dos Tributos sobre o Lucro - Demonstração do Resultado', 
'03.08 - Impostos IRPJ e CSLL - Demonstração do Resultado', 
'03.09 - Resultado Líquido das Operações Continuadas - Demonstração do Resultado', 
'03.10 - Resultado Líquido das Operações Descontinuadas - Demonstração do Resultado', 
'03.11 - Lucro Líquido - Demonstração do Resultado', 
'06.01 - Caixa das Operações - Demonstração de Fluxo de Caixa', 
'06.01.01 - Caixa das Operações - Demonstração de Fluxo de Caixa', 
'06.01.02 - Variações de Ativos e Passivos - Demonstração de Fluxo de Caixa', 
'06.01.09 - Outros Caixas Operacionais - Demonstração de Fluxo de Caixa', 
'06.02 - Caixa de Investimentos CAPEX - Demonstração de Fluxo de Caixa', 
'06.02.01 - Investimentos - Demonstração de Fluxo de Caixa', 
'06.02.02 - Imobilizado e Intangível - Demonstração de Fluxo de Caixa', 
'06.02.03 - Aplicações Financeiras - Demonstração de Fluxo de Caixa', 
'06.02.04 - Coligadas e Controladas - Demonstração de Fluxo de Caixa', 
'06.02.05 - Juros sobre Capital Próprio e Dividendos - Demonstração de Fluxo de Caixa', 
'06.02.09 - Outros Caixas de Investimento - Demonstração de Fluxo de Caixa', 
'06.03 - Caixa de Financiamento - Demonstração de Fluxo de Caixa', 
'06.03.01 - Capital - Demonstração de Fluxo de Caixa', 
'06.03.02 - Ações e Acionistas - Demonstração de Fluxo de Caixa', 
'06.03.03 - Debêntures, empréstimos e financiamentos - Demonstração de Fluxo de Caixa', 
'06.03.04 - Credores - Demonstração de Fluxo de Caixa', 
'06.03.05 - Captações e Amortizações - Demonstração de Fluxo de Caixa', 
'06.03.06 - Juros JCP e Dividendos - Demonstração de Fluxo de Caixa', 
'06.03.09 - Outros Caixas de Financiamento - Demonstração de Fluxo de Caixa', 
'06.04 - Caixa da Variação Cambial - Demonstração de Fluxo de Caixa', 
'06.05 - Variação do Caixa - Demonstração de Fluxo de Caixa', 
'06.05.01 - Saldo Inicial do Caixa  - Demonstração de Fluxo de Caixa', 
'06.05.02 - Saldo Final do Caixa - Demonstração de Fluxo de Caixa', 
'07.01 - Receitas - Demonstração de Valor Adiconado', 
'07.01.01 - Vendas - Demonstração de Valor Adiconado', 
'07.01.02 - Outras Receitas - Demonstração de Valor Adiconado', 
'07.01.03 - Ativos Próprios - Demonstração de Valor Adiconado', 
'07.01.04 - Reversão de Créditos Podres - Demonstração de Valor Adiconado', 
'07.02 - Custos dos Insumos - Demonstração de Valor Adiconado', 
'07.02.01 - Custo de Mercadorias - Demonstração de Valor Adiconado', 
'07.02.02 - Custo de Materiais, Energia e Terceiros - Demonstração de Valor Adiconado', 
'07.02.03 - Valores Ativos - Demonstração de Valor Adiconado', 
'07.02.04 - Outros - Demonstração de Valor Adiconado', 
'07.03 - Valor Adicionado Bruto - Demonstração de Valor Adiconado', 
'07.04 - Retenções - Demonstração de Valor Adiconado', 
'07.04.01 - Depreciação e Amortização - Demonstração de Valor Adiconado', 
'07.04.02 - Outras retenções - Demonstração de Valor Adiconado', 
'07.05 - Valor Adicionado Líquido - Demonstração de Valor Adiconado', 
'07.06 - Valor Adicionado em Transferência - Demonstração de Valor Adiconado', 
'07.06.01 - Resultado de Equivalência Patrimonial - Demonstração de Valor Adiconado', 
'07.06.02 - Receitas Financeiras - Demonstração de Valor Adiconado', 
'07.06.03 - Outros - Demonstração de Valor Adiconado', 
'07.07 - Valor Adicionado Total a Distribuir - Demonstração de Valor Adiconado', 
'07.08 - Distribuição do Valor Adicionado - Demonstração de Valor Adiconado', 
'07.08.01 - Pessoal - Demonstração de Valor Adiconado', 
'07.08.01.01 - Remuneração Direta - Demonstração de Valor Adiconado', 
'07.08.01.02 - Benefícios - Demonstração de Valor Adiconado', 
'07.08.01.03 - FGTS - Demonstração de Valor Adiconado', 
'07.08.01.04 - Outros - Demonstração de Valor Adiconado', 
'07.08.02 - Impostos, Taxas e Contribuições - Demonstração de Valor Adiconado', 
'07.08.02.01 - Federais - Demonstração de Valor Adiconado', 
'07.08.02.02 - Estaduais - Demonstração de Valor Adiconado', 
'07.08.02.03 - Municipais - Demonstração de Valor Adiconado', 
'07.08.03 - Remuneração de Capital de Terceiros - Demonstração de Valor Adiconado', 
'07.08.03.01 - Juros Pagos - Demonstração de Valor Adiconado', 
'07.08.03.02 - Aluguéis - Demonstração de Valor Adiconado', 
'07.08.04 - Remuneração de Capital Próprio - Demonstração de Valor Adiconado', 
'07.08.04.01 - Juros sobre o Capital Próprio - Demonstração de Valor Adiconado', 
'07.08.04.02 - Dividendos - Demonstração de Valor Adiconado', 
'07.08.04.03 - Lucros Retidos - Demonstração de Valor Adiconado', 
'07.08.05 - Outros - Demonstração de Valor Adiconado', 
'11.01.01 - Capital de Giro (Ativos Circulantes - Passivos Circulantes) - Relações entre Ativos e Passivos', 
'11.01.02 - Liquidez (Ativos Circulantes por Passivos Circulantes) - Relações entre Ativos e Passivos', 
'11.01.03 - Ativos Circulantes de Curto Prazo por Ativos - Relações entre Ativos e Passivos', 
'11.01.04 - Ativos Não Circulantes de Longo Prazo por Ativos - Relações entre Ativos e Passivos', 
'11.02 - Passivos por Ativos - Relações entre Ativos e Passivos', 
'11.02.01 - Passivos Circulantes de Curto Prazo por Ativos - Relações entre Ativos e Passivos', 
'11.02.02 - Passivos Não Circulantes de Longo Prazo por Ativos - Relações entre Ativos e Passivos', 
'11.02.03 - Passivos Circulantes de Curto Prazo por Passivos - Relações entre Ativos e Passivos', 
'11.02.04 - Passivos Não Circulantes de Longo Prazo por Passivos - Relações entre Ativos e Passivos', 
'11.03 - Patrimônio Líquido por Ativos - Relações entre Ativos e Passivos', 
'11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido) - Relações entre Ativos e Passivos', 
'11.03.02 - Passivos por Patrimônio Líquido - Relações entre Ativos e Passivos', 
'11.03.02.01 - Passivos Circulantes de Curto Prazo por Patrimônio Líquido - Relações entre Ativos e Passivos', 
'11.03.02.02 - Passivos Não Circulantes de Longo Prazo por Patrimônio Líquido - Relações entre Ativos e Passivos', 
'11.04 - Capital Social por Patrimônio Líquido - Patrimônio', 
'11.05 - Reservas por Patrimônio Líquido - Patrimônio', 
'12.01 - Dívida Bruta - Dívida', 
'12.01.01 - Dívida Bruta Circulante de Curto Prazo - Dívida', 
'12.01.02 - Dívida Bruta Não Circulante de Longo Prazo - Dívida', 
'12.01.03 - Dívida Bruta Circulante de Curto Prazo por Dívida Bruta - Dívida', 
'12.01.04 - Dívida Bruta Não Circulante de Longo Prazo por Dívida Bruta - Dívida', 
'12.01.05 - Dívida Bruta em Moeda Nacional - Dívida', 
'12.01.06 - Dívida Bruta em Moeda Estrangeira - Dívida', 
'12.01.07 - Dívida Bruta em Moeda Nacional por Dívida Bruta - Dívida', 
'12.01.08 - Dívida Bruta em Moeda Estrangeira por Dívdida Bruta - Dívida', 
'12.02.01 - Dívida Bruta por Patrimônio Líquido - Dívida', 
'12.02.02 - Endividamento Financeiro - Dívida', 
'12.03 - Patrimônio Imobilizado em Capex, Investimentos Não Capex e Intangível Não Capex - Dívida', 
'12.03.01 - Patrimônio Imobilizado por Patrimônio Líquido - Dívida', 
'12.04 - Dívida Líquida - Dívida', 
'12.04.01 - Dívida Líquida por EBITDA - Dívida', 
'12.04.01 - Serviço da Dívida (Dívida Líquida por Resultado) - Dívida', 
'13.03 - Contas a Receber por Faturamento - Resultados Fundamentalistas', 
'13.03.01 - Contas a Receber Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas', 
'13.03.02 - Contas a Receber Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas', 
'13.04 - Estoques por Faturamento - Resultados Fundamentalistas', 
'13.04.01 - Estoques Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas', 
'13.04.02 - Estoques Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas', 
'13.05 - Ativos Biológicos por Faturamento - Resultados Fundamentalistas', 
'13.05.01 - Ativos Biológicos Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas', 
'13.05.02 - Ativos Biológicos Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas', 
'13.06 - Tributos por Faturamento - Resultados Fundamentalistas', 
'13.06.01 - Tributos Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas', 
'13.06.02 - Tributos Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas', 
'13.07 - Despesas por Faturamento - Resultados Fundamentalistas', 
'13.07.01 - Despesas Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas', 
'13.07.02 - Despesas Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas', 
'13.09 - Outros Ativos por Faturamento - Resultados Fundamentalistas', 
'13.09.01 - Outros Ativos Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas', 
'13.09.02 - Outros Ativos Não Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas', 
'14.01.01 - Receita por Ativos - Resultados Fundamentalistas', 
'14.01.02 - Receita por Patrimônio - Resultados Fundamentalistas', 
'14.02.01 - Coeficiente de Retorno (Resultado por Ativos) - Resultados Fundamentalistas', 
'14.02.02 - ROE (Resultado por Patrimônio) - Resultados Fundamentalistas', 
'14.03 - Capital Investido - Resultados Fundamentalistas', 
'14.03.01 - ROIC (Retorno por Capital Investido) - Resultados Fundamentalistas', 
'14.04.01 - ROAS (EBIT por Ativos) - Resultados Fundamentalistas', 
'15.01 - Remuneração de Capital - Resultados Fundamentalistas', 
'15.01.01 - Remuneração de Capital de Terceiros por Remuneração de Capital - Resultados Fundamentalistas', 
'15.01.01.01 - Juros Pagos por Remuneração de Capital de Terceiros - Resultados Fundamentalistas', 
'15.01.01.02 - Aluguéis por Remuneração de Capital de Terceiros - Resultados Fundamentalistas', 
'15.01.02 - Remuneração de Capital Próprio por Remuneração de Capital - Resultados Fundamentalistas', 
'15.01.02.01 - Juros Sobre o Capital Próprio por Remuneração de Capital Próprio - Resultados Fundamentalistas', 
'15.01.02.02 - Dividendos por Remuneração de Capital Próprio - Resultados Fundamentalistas', 
'15.01.02.03 - Lucros Retidos por Remuneração de Capital Próprio - Resultados Fundamentalistas', 
'15.02 - Remuneração de Capital por EBIT - Resultados Fundamentalistas', 
'15.02.01 - Impostos por EBIT - Resultados Fundamentalistas', 
'16.01 - Margem Bruta (Resultado Bruto (Receita Líquida) por Receita Bruto) - Resultados Fundamentalistas', 
'16.02 - Margem Operacional (Receitas Operacionais por Receita Bruta) - Resultados Fundamentalistas', 
'16.02.01 - Força de Vendas (Despesas com Vendas por Despesas Operacionais) - Resultados Fundamentalistas', 
'16.02.02 - Peso Administrativo (Despesas com Administração por Despesas Operacionais) - Resultados Fundamentalistas', 
'16.03 - Margem EBITDA (EBITDA por Resultado Bruto (Receita Líquida)) - Resultados Fundamentalistas', 
'16.03.01 - Margem EBIT (EBIT por Resultado Bruto (Receita Líquida)) - Resultados Fundamentalistas', 
'16.03.02 - Margem de Depreciação por Resultado Bruto (Receita Líquida) - Resultados Fundamentalistas', 
'16.04 - Margem Não Operacional (Resultado Não Operacional por Resultado Bruto (Receita Líquida)) - Resultados Fundamentalistas', 
'16.05 - Margem Líquida (Lucro Líquido por Receita Bruta) - Resultados Fundamentalistas', 
'17.01 - Caixa Total - Análise do Fluxo de Caixa', 
'17.02 - Caixa Livre - Análise do Fluxo de Caixa', 
'17.03.01 - Caixa de Investimentos por Caixa das Operações - Análise do Fluxo de Caixa', 
'17.03.02 - Caixa de Investimentos por EBIT - Análise do Fluxo de Caixa', 
'17.04 - Caixa Imobilizado - Análise do Fluxo de Caixa', 
'17.05 - FCFF simplificado (Caixa Livre para a Firma) - Análise do Fluxo de Caixa', 
'17.06 - FCFE simplificado (Caixa Livre para os Acionistas) - Análise do Fluxo de Caixa', 
'18.01 - Margem de Vendas por Valor Agregado - Análise do Valor Agregado', 
'18.02 - Custo dos Insumos por Valor Agregado - Análise do Valor Agregado', 
'18.03 - Valor Adicionado Bruto por Valor Agregado - Análise do Valor Agregado', 
'18.04 - Retenções por Valor Agregado - Análise do Valor Agregado', 
'18.05 - Valor Adicionado Líquido por Valor Agregado - Análise do Valor Agregado', 
'18.06 - Valor Adicionado em Transferência por Valor Agregado - Análise do Valor Agregado', 
'18.07 - Recursos Humanos por Valor Agregado - Análise do Valor Agregado', 
'18.07.01 - Remuneração Direta (Recursos Humanos) por Valor Agregado - Análise do Valor Agregado', 
'18.07.02 - Benefícios (Recursos Humanos) por Valor Agregado - Análise do Valor Agregado', 
'18.07.03 - FGTS (Recursos Humanos) por Valor Agregado - Análise do Valor Agregado', 
'18.08 - Impostos por Valor Agregado - Análise do Valor Agregado', 
'18.09 - Remuneração de Capital de Terceiros por Valor Agregado - Análise do Valor Agregado', 
'18.09.01 - Juros Pagos a Terceiros por Valor Agregado - Análise do Valor Agregado', 
'18.09.02 - Aluguéis Pagos a Terceiros por Valor Agregado - Análise do Valor Agregado', 
'18.10 - Remuneração de Capital Próprio por Valor Agregado - Análise do Valor Agregado', 
'18.10.01 - Juros Sobre Capital Próprio por Valor Agregado - Análise do Valor Agregado', 
'18.10.02 - Dividendos por Valor Agregado - Análise do Valor Agregado', 
'18.10.02 - Lucros Retidos por Valor Agregado - Análise do Valor Agregado', 
'18.11.01 - Alíquota de Impostos (Impostos, Taxas e Contribuições por Receita Bruta) - Análise do Valor Agregado', 
'18.11.02 - Taxa de Juros Pagos (Remuneração de Capital de Terceiros por Receita Bruta - Análise do Valor Agregado', 
'18.11.03 - Taxa de Proventos Gerados (Remuneração de Capital Próprio por Receita Bruta - Análise do Valor Agregado', 
]


_0001_Ações_Ordinárias_Composição_do_Capital = '00.01 - Ações Ordinárias - Composição do Capital'
_000101_Ações_Ordinárias_em_Tesouraria_Composição_do_Capital = '00.01.01 - Ações Ordinárias em Tesouraria - Composição do Capital'
_000102_Ações_Ordinárias_Outras_Composição_do_Capital = '00.01.02 - Ações Ordinárias Outras - Composição do Capital'
_0002_Ações_Preferenciais_Composição_do_Capital = '00.02 - Ações Preferenciais - Composição do Capital'
_000201_Ações_Prerenciais_em_Tesouraria_Composição_do_Capital = '00.02.01 - Ações Prerenciais em Tesouraria - Composição do Capital'
_000202_Ações_Prerenciais_Outras_Composição_do_Capital = '00.02.02 - Ações Prerenciais Outras - Composição do Capital'
_01_Ativo_Total_Balanço_Patrimonial_Ativo = '01 - Ativo Total - Balanço Patrimonial Ativo'
_0101_Ativo_Circulante_de_Curto_Prazo_Balanço_Patrimonial_Ativo = '01.01 - Ativo Circulante de Curto Prazo - Balanço Patrimonial Ativo'
_010101_Caixa_e_Disponibilidades_de_Caixa_Balanço_Patrimonial_Ativo = '01.01.01 - Caixa e Disponibilidades de Caixa - Balanço Patrimonial Ativo'
_010102_Aplicações_Financeiras_Balanço_Patrimonial_Ativo = '01.01.02 - Aplicações Financeiras - Balanço Patrimonial Ativo'
_010103_Contas_a_Receber_Balanço_Patrimonial_Ativo = '01.01.03 - Contas a Receber - Balanço Patrimonial Ativo'
_010104_Estoques_Balanço_Patrimonial_Ativo = '01.01.04 - Estoques - Balanço Patrimonial Ativo'
_010105_Ativos_Biológicos_Balanço_Patrimonial_Ativo = '01.01.05 - Ativos Biológicos - Balanço Patrimonial Ativo'
_010106_Tributos_Balanço_Patrimonial_Ativo = '01.01.06 - Tributos - Balanço Patrimonial Ativo'
_010107_Despesas_Balanço_Patrimonial_Ativo = '01.01.07 - Despesas - Balanço Patrimonial Ativo'
_010109_Outros_Ativos_Circulantes_Balanço_Patrimonial_Ativo = '01.01.09 - Outros Ativos Circulantes - Balanço Patrimonial Ativo'
_0102_Ativo_Não_Circulante_de_Longo_Prazo_Balanço_Patrimonial_Ativo = '01.02 - Ativo Não Circulante de Longo Prazo - Balanço Patrimonial Ativo'
_010201_Ativos_Financeiros_Balanço_Patrimonial_Ativo = '01.02.01 - Ativos Financeiros - Balanço Patrimonial Ativo'
_01020101_Ativos_Financeiros_a_Valor_Justo_Balanço_Patrimonial_Ativo = '01.02.01.01 - Ativos Financeiros a Valor Justo - Balanço Patrimonial Ativo'
_01020102_Ativos_Financeiros_ao_Custo_Amortizado_Balanço_Patrimonial_Ativo = '01.02.01.02 - Ativos Financeiros ao Custo Amortizado - Balanço Patrimonial Ativo'
_01020103_Contas_a_Receber_Balanço_Patrimonial_Ativo = '01.02.01.03 - Contas a Receber - Balanço Patrimonial Ativo'
_01020104_Estoques_Balanço_Patrimonial_Ativo = '01.02.01.04 - Estoques - Balanço Patrimonial Ativo'
_01020105_Ativos_Biológicos_Balanço_Patrimonial_Ativo = '01.02.01.05 - Ativos Biológicos - Balanço Patrimonial Ativo'
_01020106_Tributos_Balanço_Patrimonial_Ativo = '01.02.01.06 - Tributos - Balanço Patrimonial Ativo'
_01020107_Despesas_Balanço_Patrimonial_Ativo = '01.02.01.07 - Despesas - Balanço Patrimonial Ativo'
_01020109_Outros_Ativos_Não_Circulantes_Balanço_Patrimonial_Ativo = '01.02.01.09 - Outros Ativos Não Circulantes - Balanço Patrimonial Ativo'
_010202_Investimentos_Não_Capex_Balanço_Patrimonial_Ativo = '01.02.02 - Investimentos Não Capex - Balanço Patrimonial Ativo'
_01020201_Propriedades_Balanço_Patrimonial_Ativo = '01.02.02.01 - Propriedades - Balanço Patrimonial Ativo'
_01020202_Arrendamentos_Balanço_Patrimonial_Ativo = '01.02.02.02 - Arrendamentos - Balanço Patrimonial Ativo'
_010203_Imobilizados_Balanço_Patrimonial_Ativo = '01.02.03 - Imobilizados - Balanço Patrimonial Ativo'
_01020301_Imobilizados_em_Operação_Balanço_Patrimonial_Ativo = '01.02.03.01 - Imobilizados em Operação - Balanço Patrimonial Ativo'
_01020302_Imobilizados_em_Arrendamento_Balanço_Patrimonial_Ativo = '01.02.03.02 - Imobilizados em Arrendamento - Balanço Patrimonial Ativo'
_01020303_Imobilizados_em_Andamento_Balanço_Patrimonial_Ativo = '01.02.03.03 - Imobilizados em Andamento - Balanço Patrimonial Ativo'
_010204_Intangível_Balanço_Patrimonial_Ativo = '01.02.04 - Intangível - Balanço Patrimonial Ativo'
_0103_Empréstimos_Balanço_Patrimonial_Ativo = '01.03 - Empréstimos - Balanço Patrimonial Ativo'
_0104_Tributos_Diferidos_Balanço_Patrimonial_Ativo = '01.04 - Tributos Diferidos - Balanço Patrimonial Ativo'
_0105_Investimentos_Balanço_Patrimonial_Ativo = '01.05 - Investimentos - Balanço Patrimonial Ativo'
_010501_Participações_em_Coligadas_Balanço_Patrimonial_Ativo = '01.05.01 - Participações em Coligadas - Balanço Patrimonial Ativo'
_010502_Participações_em_Controladas_Balanço_Patrimonial_Ativo = '01.05.02 - Participações em Controladas - Balanço Patrimonial Ativo'
_0106_Imobilizados_Balanço_Patrimonial_Ativo = '01.06 - Imobilizados - Balanço Patrimonial Ativo'
_010601_Propriedades_Balanço_Patrimonial_Ativo = '01.06.01 - Propriedades - Balanço Patrimonial Ativo'
_010602_Arrendamento_Balanço_Patrimonial_Ativo = '01.06.02 - Arrendamento - Balanço Patrimonial Ativo'
_010603_Tangíveis_Balanço_Patrimonial_Ativo = '01.06.03 - Tangíveis - Balanço Patrimonial Ativo'
_0107_Intangíveis_Balanço_Patrimonial_Ativo = '01.07 - Intangíveis - Balanço Patrimonial Ativo'
_010701_Intangíveis_Balanço_Patrimonial_Ativo = '01.07.01 - Intangíveis - Balanço Patrimonial Ativo'
_010702_Goodwill_Balanço_Patrimonial_Ativo = '01.07.02 - Goodwill - Balanço Patrimonial Ativo'
_0108_Permanente_Balanço_Patrimonial_Ativo = '01.08 - Permanente - Balanço Patrimonial Ativo'
_010909_Outros_Ativos_Balanço_Patrimonial_Ativo = '01.09.09 - Outros Ativos - Balanço Patrimonial Ativo'
_02_Passivo_Total_Balanço_Patrimonial_Passivo = '02 - Passivo Total - Balanço Patrimonial Passivo'
_0201_Passivo_Circulante_de_Curto_Prazo_Balanço_Patrimonial_Passivo = '02.01 - Passivo Circulante de Curto Prazo - Balanço Patrimonial Passivo'
_020101_Obrigações_Sociais_e_Trabalhistas_Balanço_Patrimonial_Passivo = '02.01.01 - Obrigações Sociais e Trabalhistas - Balanço Patrimonial Passivo'
_02010101_Obrigações_Sociais_Balanço_Patrimonial_Passivo = '02.01.01.01 - Obrigações Sociais - Balanço Patrimonial Passivo'
_02010102_Obrigações_Trabalhistas_Balanço_Patrimonial_Passivo = '02.01.01.02 - Obrigações Trabalhistas - Balanço Patrimonial Passivo'
_02010109_Outras_Obrigações_Balanço_Patrimonial_Passivo = '02.01.01.09 - Outras Obrigações - Balanço Patrimonial Passivo'
_020102_Fornecedores_Balanço_Patrimonial_Passivo = '02.01.02 - Fornecedores - Balanço Patrimonial Passivo'
_02010201_Fornecedores_Nacionais_Balanço_Patrimonial_Passivo = '02.01.02.01 - Fornecedores Nacionais - Balanço Patrimonial Passivo'
_02010202_Fornecedores_Estrangeiros_Balanço_Patrimonial_Passivo = '02.01.02.02 - Fornecedores Estrangeiros - Balanço Patrimonial Passivo'
_020103_Obrigações_Fiscais_Balanço_Patrimonial_Passivo = '02.01.03 - Obrigações Fiscais - Balanço Patrimonial Passivo'
_02010301_Obrigações_Fiscais_Federais_Balanço_Patrimonial_Passivo = '02.01.03.01 - Obrigações Fiscais Federais - Balanço Patrimonial Passivo'
_02010302_Obrigações_Fiscais_Estaduais_Balanço_Patrimonial_Passivo = '02.01.03.02 - Obrigações Fiscais Estaduais - Balanço Patrimonial Passivo'
_02010303_Obrigações_Fiscais_Municipais_Balanço_Patrimonial_Passivo = '02.01.03.03 - Obrigações Fiscais Municipais - Balanço Patrimonial Passivo'
_02010309_Outras_Obrigações_Fiscais_Balanço_Patrimonial_Passivo = '02.01.03.09 - Outras Obrigações Fiscais - Balanço Patrimonial Passivo'
_020104_Empréstimos__Financiamentos_e_Debêntures_Balanço_Patrimonial_Passivo = '02.01.04 - Empréstimos, Financiamentos e Debêntures - Balanço Patrimonial Passivo'
_02010401_Empréstimos_e_Financiamentos_Balanço_Patrimonial_Passivo = '02.01.04.01 - Empréstimos e Financiamentos - Balanço Patrimonial Passivo'
_0201040101_Empréstimos_e_Financiamentos_em_Moeda_Nacional_Balanço_Patrimonial_Passivo = '02.01.04.01.01 - Empréstimos e Financiamentos em Moeda Nacional - Balanço Patrimonial Passivo'
_0201040102_Empréstimos_e_Financiamentos_em_Moeda_Estrangeira_Balanço_Patrimonial_Passivo = '02.01.04.01.02 - Empréstimos e Financiamentos em Moeda Estrangeira - Balanço Patrimonial Passivo'
_02010402_Debêntures_Balanço_Patrimonial_Passivo = '02.01.04.02 - Debêntures - Balanço Patrimonial Passivo'
_02010403_Arrendamentos_Balanço_Patrimonial_Passivo = '02.01.04.03 - Arrendamentos - Balanço Patrimonial Passivo'
_02010409_Outros_empréstimos__financiamentos_e_debêntures_Balanço_Patrimonial_Passivo = '02.01.04.09 - Outros empréstimos, financiamentos e debêntures - Balanço Patrimonial Passivo'
_020105_Outras_Obrigações_Balanço_Patrimonial_Passivo = '02.01.05 - Outras Obrigações - Balanço Patrimonial Passivo'
_02010501_Passivos_com_Partes_Relacionadas_Balanço_Patrimonial_Passivo = '02.01.05.01 - Passivos com Partes Relacionadas - Balanço Patrimonial Passivo'
_02010509_Outros_Balanço_Patrimonial_Passivo = '02.01.05.09 - Outros - Balanço Patrimonial Passivo'
_020106_Provisões_Balanço_Patrimonial_Passivo = '02.01.06 - Provisões - Balanço Patrimonial Passivo'
_02010601_Provisões_Específicas_Balanço_Patrimonial_Passivo = '02.01.06.01 - Provisões Específicas - Balanço Patrimonial Passivo'
_0201060101_Provisões_Fiscais_Balanço_Patrimonial_Passivo = '02.01.06.01.01 - Provisões Fiscais - Balanço Patrimonial Passivo'
_0201060102_Provisões_Trabalhistas_e_Previdenciárias_Balanço_Patrimonial_Passivo = '02.01.06.01.02 - Provisões Trabalhistas e Previdenciárias - Balanço Patrimonial Passivo'
_0201060103_Provisões_para_Benefícios_a_Empregados_Balanço_Patrimonial_Passivo = '02.01.06.01.03 - Provisões para Benefícios a Empregados - Balanço Patrimonial Passivo'
_0201060104_Provisões_Judiciais_Cíveis_Balanço_Patrimonial_Passivo = '02.01.06.01.04 - Provisões Judiciais Cíveis - Balanço Patrimonial Passivo'
_0201060105_Outras_Provisões_Específicas_Balanço_Patrimonial_Passivo = '02.01.06.01.05 - Outras Provisões Específicas - Balanço Patrimonial Passivo'
_02010602_Provisões_Outras_Balanço_Patrimonial_Passivo = '02.01.06.02 - Provisões Outras - Balanço Patrimonial Passivo'
_0201060201_Provisões_para_Garantias_Balanço_Patrimonial_Passivo = '02.01.06.02.01 - Provisões para Garantias - Balanço Patrimonial Passivo'
_0201060202_Provisões_para_Reestruturação_Balanço_Patrimonial_Passivo = '02.01.06.02.02 - Provisões para Reestruturação - Balanço Patrimonial Passivo'
_0201060203_Provisões_para_Passivos_Ambientais_e_de_Desativação_Balanço_Patrimonial_Passivo = '02.01.06.02.03 - Provisões para Passivos Ambientais e de Desativação - Balanço Patrimonial Passivo'
_020107_Passivos_sobre_Ativos_Não_Correntes_a_Venda_e_Descontinuados_Balanço_Patrimonial_Passivo = '02.01.07 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados - Balanço Patrimonial Passivo'
_02010701_Passivos_sobre_Ativos_Não_Correntes_a_Venda_Balanço_Patrimonial_Passivo = '02.01.07.01 - Passivos sobre Ativos Não-Correntes a Venda - Balanço Patrimonial Passivo'
_02010702_Passivos_sobre_Ativos_de_Operações_Descontinuadas_Balanço_Patrimonial_Passivo = '02.01.07.02 - Passivos sobre Ativos de Operações Descontinuadas - Balanço Patrimonial Passivo'
_020109_Outros_Passivos_Balanço_Patrimonial_Passivo = '02.01.09 - Outros Passivos - Balanço Patrimonial Passivo'
_0202_Passivo_Não_Circulante_de_Longo_Prazo_Balanço_Patrimonial_Passivo = '02.02 - Passivo Não Circulante de Longo Prazo - Balanço Patrimonial Passivo'
_020201_Empréstimos_e_Financiamentos_de_Longo_Prazo_Balanço_Patrimonial_Passivo = '02.02.01 - Empréstimos e Financiamentos de Longo Prazo - Balanço Patrimonial Passivo'
_02020101_Empréstimos_e_Financiamentos_Balanço_Patrimonial_Passivo = '02.02.01.01 - Empréstimos e Financiamentos - Balanço Patrimonial Passivo'
_0202010101_Empréstimos_e_Financiamentos_em_Moeda_Nacional_Balanço_Patrimonial_Passivo = '02.02.01.01.01 - Empréstimos e Financiamentos em Moeda Nacional - Balanço Patrimonial Passivo'
_0202010102_Empréstimos_e_Financiamentos_em_Moeda_Estrangeira_Balanço_Patrimonial_Passivo = '02.02.01.01.02 - Empréstimos e Financiamentos em Moeda Estrangeira - Balanço Patrimonial Passivo'
_02020102_Debêntures_Balanço_Patrimonial_Passivo = '02.02.01.02 - Debêntures - Balanço Patrimonial Passivo'
_02020103_Arrendamentos_Balanço_Patrimonial_Passivo = '02.02.01.03 - Arrendamentos - Balanço Patrimonial Passivo'
_020202_Outras_Obrigações_Balanço_Patrimonial_Passivo = '02.02.02 - Outras Obrigações - Balanço Patrimonial Passivo'
_02020201_Com_Partes_Relacionadas_Balanço_Patrimonial_Passivo = '02.02.02.01 - Com Partes Relacionadas - Balanço Patrimonial Passivo'
_02020202_Outras_Obrigações_Balanço_Patrimonial_Passivo = '02.02.02.02 - Outras Obrigações - Balanço Patrimonial Passivo'
_02020209_Outros_empréstimos__financiamentos_e_debêntures_Balanço_Patrimonial_Passivo = '02.02.02.09 - Outros empréstimos, financiamentos e debêntures - Balanço Patrimonial Passivo'
_020203_Tributos_Diferidos_Balanço_Patrimonial_Passivo = '02.02.03 - Tributos Diferidos - Balanço Patrimonial Passivo'
_02020301_Imposto_de_Renda_e_Contribuição_Social_Balanço_Patrimonial_Passivo = '02.02.03.01 - Imposto de Renda e Contribuição Social - Balanço Patrimonial Passivo'
_02020302_Outros_tributos_diferidos_Balanço_Patrimonial_Passivo = '02.02.03.02 - Outros tributos diferidos - Balanço Patrimonial Passivo'
_020204_Provisões_Balanço_Patrimonial_Passivo = '02.02.04 - Provisões - Balanço Patrimonial Passivo'
_02020401_Provisões_Específicas_Balanço_Patrimonial_Passivo = '02.02.04.01 - Provisões Específicas - Balanço Patrimonial Passivo'
_0202040101_Provisões_Fiscais_Balanço_Patrimonial_Passivo = '02.02.04.01.01 - Provisões Fiscais - Balanço Patrimonial Passivo'
_0202040102_Provisões_Trabalhistas_e_Previdenciárias_Balanço_Patrimonial_Passivo = '02.02.04.01.02 - Provisões Trabalhistas e Previdenciárias - Balanço Patrimonial Passivo'
_0202040103_Provisões_para_Benefícios_a_Empregados_Balanço_Patrimonial_Passivo = '02.02.04.01.03 - Provisões para Benefícios a Empregados - Balanço Patrimonial Passivo'
_0202040104_Provisões_Judiciais_Cíveis_Balanço_Patrimonial_Passivo = '02.02.04.01.04 - Provisões Judiciais Cíveis - Balanço Patrimonial Passivo'
_02020402_Outras_Provisões_Balanço_Patrimonial_Passivo = '02.02.04.02 - Outras Provisões - Balanço Patrimonial Passivo'
_0202040201_Provisões_para_Garantias_Balanço_Patrimonial_Passivo = '02.02.04.02.01 - Provisões para Garantias - Balanço Patrimonial Passivo'
_0202040202_Provisões_para_Reestruturação_Balanço_Patrimonial_Passivo = '02.02.04.02.02 - Provisões para Reestruturação - Balanço Patrimonial Passivo'
_0202040203_Provisões_para_Passivos_Ambientais_e_de_Desativação_Balanço_Patrimonial_Passivo = '02.02.04.02.03 - Provisões para Passivos Ambientais e de Desativação - Balanço Patrimonial Passivo'
_020205_Passivos_sobre_Ativos_Não_Correntes_a_Venda_e_Descontinuados_Balanço_Patrimonial_Passivo = '02.02.05 - Passivos sobre Ativos Não-Correntes a Venda e Descontinuados - Balanço Patrimonial Passivo'
_02020501_Passivos_sobre_Ativos_Não_Correntes_a_Venda_Balanço_Patrimonial_Passivo = '02.02.05.01 - Passivos sobre Ativos Não-Correntes a Venda - Balanço Patrimonial Passivo'
_02020502_Passivos_sobre_Ativos_de_Operações_Descontinuadas_Balanço_Patrimonial_Passivo = '02.02.05.02 - Passivos sobre Ativos de Operações Descontinuadas - Balanço Patrimonial Passivo'
_020206_Lucros_e_Receitas_a_Apropriar_Balanço_Patrimonial_Passivo = '02.02.06 - Lucros e Receitas a Apropriar - Balanço Patrimonial Passivo'
_02020601_Lucros_a_Apropriar_Balanço_Patrimonial_Passivo = '02.02.06.01 - Lucros a Apropriar - Balanço Patrimonial Passivo'
_02020602_Receitas_a_Apropriar_Balanço_Patrimonial_Passivo = '02.02.06.02 - Receitas a Apropriar - Balanço Patrimonial Passivo'
_02020603_Subvenções_de_Investimento_a_Apropriar_Balanço_Patrimonial_Passivo = '02.02.06.03 - Subvenções de Investimento a Apropriar - Balanço Patrimonial Passivo'
_020209_Outros_Passivos_Balanço_Patrimonial_Passivo = '02.02.09 - Outros Passivos - Balanço Patrimonial Passivo'
_0203_Patrimônio_Líquido_Balanço_Patrimonial_Passivo = '02.03 - Patrimônio Líquido - Balanço Patrimonial Passivo'
_020301_Capital_Social_Balanço_Patrimonial_Passivo = '02.03.01 - Capital Social - Balanço Patrimonial Passivo'
_020302_Reservas_de_Capital_Balanço_Patrimonial_Passivo = '02.03.02 - Reservas de Capital - Balanço Patrimonial Passivo'
_020303_Reservas_de_Reavaliação_Balanço_Patrimonial_Passivo = '02.03.03 - Reservas de Reavaliação - Balanço Patrimonial Passivo'
_020304_Reservas_de_Lucros_Balanço_Patrimonial_Passivo = '02.03.04 - Reservas de Lucros - Balanço Patrimonial Passivo'
_020305_Lucros_ou_Prejuízos_Acumulados_Balanço_Patrimonial_Passivo = '02.03.05 - Lucros ou Prejuízos Acumulados - Balanço Patrimonial Passivo'
_020306_Ajustes_de_Avaliação_Patrimonial_Balanço_Patrimonial_Passivo = '02.03.06 - Ajustes de Avaliação Patrimonial - Balanço Patrimonial Passivo'
_020307_Ajustes_Acumulados_de_Conversão_Balanço_Patrimonial_Passivo = '02.03.07 - Ajustes Acumulados de Conversão - Balanço Patrimonial Passivo'
_020308_Outros_Resultados_Abrangentes_Balanço_Patrimonial_Passivo = '02.03.08 - Outros Resultados Abrangentes - Balanço Patrimonial Passivo'
_0204_Outros_Passivos_ou_Provissões_Balanço_Patrimonial_Passivo = '02.04 - Outros Passivos ou Provissões - Balanço Patrimonial Passivo'
_0301_Receita_Bruta_Demonstração_do_Resultado = '03.01 - Receita Bruta - Demonstração do Resultado'
_0302_Custo_de_Produção_Demonstração_do_Resultado = '03.02 - Custo de Produção - Demonstração do Resultado'
_0303_Resultado_Bruto__Receita_Líquida__Demonstração_do_Resultado = '03.03 - Resultado Bruto (Receita Líquida) - Demonstração do Resultado'
_0304_Despesas_Operacionais_Demonstração_do_Resultado = '03.04 - Despesas Operacionais - Demonstração do Resultado'
_030401_Despesas_com_Vendas_Demonstração_do_Resultado = '03.04.01 - Despesas com Vendas - Demonstração do Resultado'
_030402_Despesas_Gerais_e_Administrativas_Demonstração_do_Resultado = '03.04.02 - Despesas Gerais e Administrativas - Demonstração do Resultado'
_030409_Outras_despesas__receitas_ou_equivalências_Demonstração_do_Resultado = '03.04.09 - Outras despesas, receitas ou equivalências - Demonstração do Resultado'
_0305_LAJIR_EBIT_Resultado_Antes_do_Resultado_Financeiro_e_dos_Tributos_Demonstração_do_Resultado = '03.05 - LAJIR EBIT Resultado Antes do Resultado Financeiro e dos Tributos - Demonstração do Resultado'
_0306_Resultado_Financeiro__Não_Operacional__Demonstração_do_Resultado = '03.06 - Resultado Financeiro (Não Operacional) - Demonstração do Resultado'
_0307_Resultado_Antes_dos_Tributos_sobre_o_Lucro_Demonstração_do_Resultado = '03.07 - Resultado Antes dos Tributos sobre o Lucro - Demonstração do Resultado'
_0308_Impostos_IRPJ_e_CSLL_Demonstração_do_Resultado = '03.08 - Impostos IRPJ e CSLL - Demonstração do Resultado'
_0309_Resultado_Líquido_das_Operações_Continuadas_Demonstração_do_Resultado = '03.09 - Resultado Líquido das Operações Continuadas - Demonstração do Resultado'
_0310_Resultado_Líquido_das_Operações_Descontinuadas_Demonstração_do_Resultado = '03.10 - Resultado Líquido das Operações Descontinuadas - Demonstração do Resultado'
_0311_Lucro_Líquido_Demonstração_do_Resultado = '03.11 - Lucro Líquido - Demonstração do Resultado'
_0601_Caixa_das_Operações_Demonstração_de_Fluxo_de_Caixa = '06.01 - Caixa das Operações - Demonstração de Fluxo de Caixa'
_060101_Caixa_das_Operações_Demonstração_de_Fluxo_de_Caixa = '06.01.01 - Caixa das Operações - Demonstração de Fluxo de Caixa'
_060102_Variações_de_Ativos_e_Passivos_Demonstração_de_Fluxo_de_Caixa = '06.01.02 - Variações de Ativos e Passivos - Demonstração de Fluxo de Caixa'
_060109_Outros_Caixas_Operacionais_Demonstração_de_Fluxo_de_Caixa = '06.01.09 - Outros Caixas Operacionais - Demonstração de Fluxo de Caixa'
_0602_Caixa_de_Investimentos_CAPEX_Demonstração_de_Fluxo_de_Caixa = '06.02 - Caixa de Investimentos CAPEX - Demonstração de Fluxo de Caixa'
_060201_Investimentos_Demonstração_de_Fluxo_de_Caixa = '06.02.01 - Investimentos - Demonstração de Fluxo de Caixa'
_060202_Imobilizado_e_Intangível_Demonstração_de_Fluxo_de_Caixa = '06.02.02 - Imobilizado e Intangível - Demonstração de Fluxo de Caixa'
_060203_Aplicações_Financeiras_Demonstração_de_Fluxo_de_Caixa = '06.02.03 - Aplicações Financeiras - Demonstração de Fluxo de Caixa'
_060204_Coligadas_e_Controladas_Demonstração_de_Fluxo_de_Caixa = '06.02.04 - Coligadas e Controladas - Demonstração de Fluxo de Caixa'
_060205_Juros_sobre_Capital_Próprio_e_Dividendos_Demonstração_de_Fluxo_de_Caixa = '06.02.05 - Juros sobre Capital Próprio e Dividendos - Demonstração de Fluxo de Caixa'
_060209_Outros_Caixas_de_Investimento_Demonstração_de_Fluxo_de_Caixa = '06.02.09 - Outros Caixas de Investimento - Demonstração de Fluxo de Caixa'
_0603_Caixa_de_Financiamento_Demonstração_de_Fluxo_de_Caixa = '06.03 - Caixa de Financiamento - Demonstração de Fluxo de Caixa'
_060301_Capital_Demonstração_de_Fluxo_de_Caixa = '06.03.01 - Capital - Demonstração de Fluxo de Caixa'
_060302_Ações_e_Acionistas_Demonstração_de_Fluxo_de_Caixa = '06.03.02 - Ações e Acionistas - Demonstração de Fluxo de Caixa'
_060303_Debêntures__empréstimos_e_financiamentos_Demonstração_de_Fluxo_de_Caixa = '06.03.03 - Debêntures, empréstimos e financiamentos - Demonstração de Fluxo de Caixa'
_060304_Credores_Demonstração_de_Fluxo_de_Caixa = '06.03.04 - Credores - Demonstração de Fluxo de Caixa'
_060305_Captações_e_Amortizações_Demonstração_de_Fluxo_de_Caixa = '06.03.05 - Captações e Amortizações - Demonstração de Fluxo de Caixa'
_060306_Juros_JCP_e_Dividendos_Demonstração_de_Fluxo_de_Caixa = '06.03.06 - Juros JCP e Dividendos - Demonstração de Fluxo de Caixa'
_060309_Outros_Caixas_de_Financiamento_Demonstração_de_Fluxo_de_Caixa = '06.03.09 - Outros Caixas de Financiamento - Demonstração de Fluxo de Caixa'
_0604_Caixa_da_Variação_Cambial_Demonstração_de_Fluxo_de_Caixa = '06.04 - Caixa da Variação Cambial - Demonstração de Fluxo de Caixa'
_0605_Variação_do_Caixa_Demonstração_de_Fluxo_de_Caixa = '06.05 - Variação do Caixa - Demonstração de Fluxo de Caixa'
_060501_Saldo_Inicial_do_Caixa__Demonstração_de_Fluxo_de_Caixa = '06.05.01 - Saldo Inicial do Caixa  - Demonstração de Fluxo de Caixa'
_060502_Saldo_Final_do_Caixa_Demonstração_de_Fluxo_de_Caixa = '06.05.02 - Saldo Final do Caixa - Demonstração de Fluxo de Caixa'
_0701_Receitas_Demonstração_de_Valor_Adiconado = '07.01 - Receitas - Demonstração de Valor Adiconado'
_070101_Vendas_Demonstração_de_Valor_Adiconado = '07.01.01 - Vendas - Demonstração de Valor Adiconado'
_070102_Outras_Receitas_Demonstração_de_Valor_Adiconado = '07.01.02 - Outras Receitas - Demonstração de Valor Adiconado'
_070103_Ativos_Próprios_Demonstração_de_Valor_Adiconado = '07.01.03 - Ativos Próprios - Demonstração de Valor Adiconado'
_070104_Reversão_de_Créditos_Podres_Demonstração_de_Valor_Adiconado = '07.01.04 - Reversão de Créditos Podres - Demonstração de Valor Adiconado'
_0702_Custos_dos_Insumos_Demonstração_de_Valor_Adiconado = '07.02 - Custos dos Insumos - Demonstração de Valor Adiconado'
_070201_Custo_de_Mercadorias_Demonstração_de_Valor_Adiconado = '07.02.01 - Custo de Mercadorias - Demonstração de Valor Adiconado'
_070202_Custo_de_Materiais__Energia_e_Terceiros_Demonstração_de_Valor_Adiconado = '07.02.02 - Custo de Materiais, Energia e Terceiros - Demonstração de Valor Adiconado'
_070203_Valores_Ativos_Demonstração_de_Valor_Adiconado = '07.02.03 - Valores Ativos - Demonstração de Valor Adiconado'
_070204_Outros_Demonstração_de_Valor_Adiconado = '07.02.04 - Outros - Demonstração de Valor Adiconado'
_0703_Valor_Adicionado_Bruto_Demonstração_de_Valor_Adiconado = '07.03 - Valor Adicionado Bruto - Demonstração de Valor Adiconado'
_0704_Retenções_Demonstração_de_Valor_Adiconado = '07.04 - Retenções - Demonstração de Valor Adiconado'
_070401_Depreciação_e_Amortização_Demonstração_de_Valor_Adiconado = '07.04.01 - Depreciação e Amortização - Demonstração de Valor Adiconado'
_070402_Outras_retenções_Demonstração_de_Valor_Adiconado = '07.04.02 - Outras retenções - Demonstração de Valor Adiconado'
_0705_Valor_Adicionado_Líquido_Demonstração_de_Valor_Adiconado = '07.05 - Valor Adicionado Líquido - Demonstração de Valor Adiconado'
_0706_Valor_Adicionado_em_Transferência_Demonstração_de_Valor_Adiconado = '07.06 - Valor Adicionado em Transferência - Demonstração de Valor Adiconado'
_070601_Resultado_de_Equivalência_Patrimonial_Demonstração_de_Valor_Adiconado = '07.06.01 - Resultado de Equivalência Patrimonial - Demonstração de Valor Adiconado'
_070602_Receitas_Financeiras_Demonstração_de_Valor_Adiconado = '07.06.02 - Receitas Financeiras - Demonstração de Valor Adiconado'
_070603_Outros_Demonstração_de_Valor_Adiconado = '07.06.03 - Outros - Demonstração de Valor Adiconado'
_0707_Valor_Adicionado_Total_a_Distribuir_Demonstração_de_Valor_Adiconado = '07.07 - Valor Adicionado Total a Distribuir - Demonstração de Valor Adiconado'
_0708_Distribuição_do_Valor_Adicionado_Demonstração_de_Valor_Adiconado = '07.08 - Distribuição do Valor Adicionado - Demonstração de Valor Adiconado'
_070801_Pessoal_Demonstração_de_Valor_Adiconado = '07.08.01 - Pessoal - Demonstração de Valor Adiconado'
_07080101_Remuneração_Direta_Demonstração_de_Valor_Adiconado = '07.08.01.01 - Remuneração Direta - Demonstração de Valor Adiconado'
_07080102_Benefícios_Demonstração_de_Valor_Adiconado = '07.08.01.02 - Benefícios - Demonstração de Valor Adiconado'
_07080103_FGTS_Demonstração_de_Valor_Adiconado = '07.08.01.03 - FGTS - Demonstração de Valor Adiconado'
_07080104_Outros_Demonstração_de_Valor_Adiconado = '07.08.01.04 - Outros - Demonstração de Valor Adiconado'
_070802_Impostos__Taxas_e_Contribuições_Demonstração_de_Valor_Adiconado = '07.08.02 - Impostos, Taxas e Contribuições - Demonstração de Valor Adiconado'
_07080201_Federais_Demonstração_de_Valor_Adiconado = '07.08.02.01 - Federais - Demonstração de Valor Adiconado'
_07080202_Estaduais_Demonstração_de_Valor_Adiconado = '07.08.02.02 - Estaduais - Demonstração de Valor Adiconado'
_07080203_Municipais_Demonstração_de_Valor_Adiconado = '07.08.02.03 - Municipais - Demonstração de Valor Adiconado'
_070803_Remuneração_de_Capital_de_Terceiros_Demonstração_de_Valor_Adiconado = '07.08.03 - Remuneração de Capital de Terceiros - Demonstração de Valor Adiconado'
_07080301_Juros_Pagos_Demonstração_de_Valor_Adiconado = '07.08.03.01 - Juros Pagos - Demonstração de Valor Adiconado'
_07080302_Aluguéis_Demonstração_de_Valor_Adiconado = '07.08.03.02 - Aluguéis - Demonstração de Valor Adiconado'
_070804_Remuneração_de_Capital_Próprio_Demonstração_de_Valor_Adiconado = '07.08.04 - Remuneração de Capital Próprio - Demonstração de Valor Adiconado'
_07080401_Juros_sobre_o_Capital_Próprio_Demonstração_de_Valor_Adiconado = '07.08.04.01 - Juros sobre o Capital Próprio - Demonstração de Valor Adiconado'
_07080402_Dividendos_Demonstração_de_Valor_Adiconado = '07.08.04.02 - Dividendos - Demonstração de Valor Adiconado'
_07080403_Lucros_Retidos_Demonstração_de_Valor_Adiconado = '07.08.04.03 - Lucros Retidos - Demonstração de Valor Adiconado'
_070805_Outros_Demonstração_de_Valor_Adiconado = '07.08.05 - Outros - Demonstração de Valor Adiconado'
_110101_Capital_de_Giro__Ativos_Circulantes_Passivos_Circulantes__Relações_entre_Ativos_e_Passivos = '11.01.01 - Capital de Giro (Ativos Circulantes - Passivos Circulantes) - Relações entre Ativos e Passivos'
_110102_Liquidez__Ativos_Circulantes_por_Passivos_Circulantes__Relações_entre_Ativos_e_Passivos = '11.01.02 - Liquidez (Ativos Circulantes por Passivos Circulantes) - Relações entre Ativos e Passivos'
_110103_Ativos_Circulantes_de_Curto_Prazo_por_Ativos_Relações_entre_Ativos_e_Passivos = '11.01.03 - Ativos Circulantes de Curto Prazo por Ativos - Relações entre Ativos e Passivos'
_110104_Ativos_Não_Circulantes_de_Longo_Prazo_por_Ativos_Relações_entre_Ativos_e_Passivos = '11.01.04 - Ativos Não Circulantes de Longo Prazo por Ativos - Relações entre Ativos e Passivos'
_1102_Passivos_por_Ativos_Relações_entre_Ativos_e_Passivos = '11.02 - Passivos por Ativos - Relações entre Ativos e Passivos'
_110201_Passivos_Circulantes_de_Curto_Prazo_por_Ativos_Relações_entre_Ativos_e_Passivos = '11.02.01 - Passivos Circulantes de Curto Prazo por Ativos - Relações entre Ativos e Passivos'
_110202_Passivos_Não_Circulantes_de_Longo_Prazo_por_Ativos_Relações_entre_Ativos_e_Passivos = '11.02.02 - Passivos Não Circulantes de Longo Prazo por Ativos - Relações entre Ativos e Passivos'
_110203_Passivos_Circulantes_de_Curto_Prazo_por_Passivos_Relações_entre_Ativos_e_Passivos = '11.02.03 - Passivos Circulantes de Curto Prazo por Passivos - Relações entre Ativos e Passivos'
_110204_Passivos_Não_Circulantes_de_Longo_Prazo_por_Passivos_Relações_entre_Ativos_e_Passivos = '11.02.04 - Passivos Não Circulantes de Longo Prazo por Passivos - Relações entre Ativos e Passivos'
_1103_Patrimônio_Líquido_por_Ativos_Relações_entre_Ativos_e_Passivos = '11.03 - Patrimônio Líquido por Ativos - Relações entre Ativos e Passivos'
_110301_Equity_Multiplier__Ativos_por_Patrimônio_Líquido__Relações_entre_Ativos_e_Passivos = '11.03.01 - Equity Multiplier (Ativos por Patrimônio Líquido) - Relações entre Ativos e Passivos'
_110302_Passivos_por_Patrimônio_Líquido_Relações_entre_Ativos_e_Passivos = '11.03.02 - Passivos por Patrimônio Líquido - Relações entre Ativos e Passivos'
_11030201_Passivos_Circulantes_de_Curto_Prazo_por_Patrimônio_Líquido_Relações_entre_Ativos_e_Passivos = '11.03.02.01 - Passivos Circulantes de Curto Prazo por Patrimônio Líquido - Relações entre Ativos e Passivos'
_11030202_Passivos_Não_Circulantes_de_Longo_Prazo_por_Patrimônio_Líquido_Relações_entre_Ativos_e_Passivos = '11.03.02.02 - Passivos Não Circulantes de Longo Prazo por Patrimônio Líquido - Relações entre Ativos e Passivos'
_1104_Capital_Social_por_Patrimônio_Líquido_Patrimônio = '11.04 - Capital Social por Patrimônio Líquido - Patrimônio'
_1105_Reservas_por_Patrimônio_Líquido_Patrimônio = '11.05 - Reservas por Patrimônio Líquido - Patrimônio'
_1201_Dívida_Bruta_Dívida = '12.01 - Dívida Bruta - Dívida'
_120101_Dívida_Bruta_Circulante_de_Curto_Prazo_Dívida = '12.01.01 - Dívida Bruta Circulante de Curto Prazo - Dívida'
_120102_Dívida_Bruta_Não_Circulante_de_Longo_Prazo_Dívida = '12.01.02 - Dívida Bruta Não Circulante de Longo Prazo - Dívida'
_120103_Dívida_Bruta_Circulante_de_Curto_Prazo_por_Dívida_Bruta_Dívida = '12.01.03 - Dívida Bruta Circulante de Curto Prazo por Dívida Bruta - Dívida'
_120104_Dívida_Bruta_Não_Circulante_de_Longo_Prazo_por_Dívida_Bruta_Dívida = '12.01.04 - Dívida Bruta Não Circulante de Longo Prazo por Dívida Bruta - Dívida'
_120105_Dívida_Bruta_em_Moeda_Nacional_Dívida = '12.01.05 - Dívida Bruta em Moeda Nacional - Dívida'
_120106_Dívida_Bruta_em_Moeda_Estrangeira_Dívida = '12.01.06 - Dívida Bruta em Moeda Estrangeira - Dívida'
_120107_Dívida_Bruta_em_Moeda_Nacional_por_Dívida_Bruta_Dívida = '12.01.07 - Dívida Bruta em Moeda Nacional por Dívida Bruta - Dívida'
_120108_Dívida_Bruta_em_Moeda_Estrangeira_por_Dívdida_Bruta_Dívida = '12.01.08 - Dívida Bruta em Moeda Estrangeira por Dívdida Bruta - Dívida'
_120201_Dívida_Bruta_por_Patrimônio_Líquido_Dívida = '12.02.01 - Dívida Bruta por Patrimônio Líquido - Dívida'
_120202_Endividamento_Financeiro_Dívida = '12.02.02 - Endividamento Financeiro - Dívida'
_1203_Patrimônio_Imobilizado_em_Capex__Investimentos_Não_Capex_e_Intangível_Não_Capex_Dívida = '12.03 - Patrimônio Imobilizado em Capex, Investimentos Não Capex e Intangível Não Capex - Dívida'
_120301_Patrimônio_Imobilizado_por_Patrimônio_Líquido_Dívida = '12.03.01 - Patrimônio Imobilizado por Patrimônio Líquido - Dívida'
_1204_Dívida_Líquida_Dívida = '12.04 - Dívida Líquida - Dívida'
_120401_Dívida_Líquida_por_EBITDA_Dívida = '12.04.01 - Dívida Líquida por EBITDA - Dívida'
_120401_Serviço_da_Dívida__Dívida_Líquida_por_Resultado__Dívida = '12.04.01 - Serviço da Dívida (Dívida Líquida por Resultado) - Dívida'
_1303_Contas_a_Receber_por_Faturamento_Resultados_Fundamentalistas = '13.03 - Contas a Receber por Faturamento - Resultados Fundamentalistas'
_130301_Contas_a_Receber_Não_Circulantes_de_Curto_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.03.01 - Contas a Receber Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas'
_130302_Contas_a_Receber_Circulantes_de_Longo_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.03.02 - Contas a Receber Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas'
_1304_Estoques_por_Faturamento_Resultados_Fundamentalistas = '13.04 - Estoques por Faturamento - Resultados Fundamentalistas'
_130401_Estoques_Não_Circulantes_de_Curto_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.04.01 - Estoques Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas'
_130402_Estoques_Circulantes_de_Longo_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.04.02 - Estoques Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas'
_1305_Ativos_Biológicos_por_Faturamento_Resultados_Fundamentalistas = '13.05 - Ativos Biológicos por Faturamento - Resultados Fundamentalistas'
_130501_Ativos_Biológicos_Não_Circulantes_de_Curto_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.05.01 - Ativos Biológicos Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas'
_130502_Ativos_Biológicos_Circulantes_de_Longo_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.05.02 - Ativos Biológicos Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas'
_1306_Tributos_por_Faturamento_Resultados_Fundamentalistas = '13.06 - Tributos por Faturamento - Resultados Fundamentalistas'
_130601_Tributos_Não_Circulantes_de_Curto_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.06.01 - Tributos Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas'
_130602_Tributos_Circulantes_de_Longo_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.06.02 - Tributos Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas'
_1307_Despesas_por_Faturamento_Resultados_Fundamentalistas = '13.07 - Despesas por Faturamento - Resultados Fundamentalistas'
_130701_Despesas_Não_Circulantes_de_Curto_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.07.01 - Despesas Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas'
_130702_Despesas_Circulantes_de_Longo_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.07.02 - Despesas Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas'
_1309_Outros_Ativos_por_Faturamento_Resultados_Fundamentalistas = '13.09 - Outros Ativos por Faturamento - Resultados Fundamentalistas'
_130901_Outros_Ativos_Não_Circulantes_de_Curto_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.09.01 - Outros Ativos Não Circulantes de Curto Prazo por Faturamento - Resultados Fundamentalistas'
_130902_Outros_Ativos_Não_Circulantes_de_Longo_Prazo_por_Faturamento_Resultados_Fundamentalistas = '13.09.02 - Outros Ativos Não Circulantes de Longo Prazo por Faturamento - Resultados Fundamentalistas'
_140101_Receita_por_Ativos_Resultados_Fundamentalistas = '14.01.01 - Receita por Ativos - Resultados Fundamentalistas'
_140102_Receita_por_Patrimônio_Resultados_Fundamentalistas = '14.01.02 - Receita por Patrimônio - Resultados Fundamentalistas'
_140201_Coeficiente_de_Retorno__Resultado_por_Ativos__Resultados_Fundamentalistas = '14.02.01 - Coeficiente de Retorno (Resultado por Ativos) - Resultados Fundamentalistas'
_140202_ROE__Resultado_por_Patrimônio__Resultados_Fundamentalistas = '14.02.02 - ROE (Resultado por Patrimônio) - Resultados Fundamentalistas'
_1403_Capital_Investido_Resultados_Fundamentalistas = '14.03 - Capital Investido - Resultados Fundamentalistas'
_140301_ROIC__Retorno_por_Capital_Investido__Resultados_Fundamentalistas = '14.03.01 - ROIC (Retorno por Capital Investido) - Resultados Fundamentalistas'
_140401_ROAS__EBIT_por_Ativos__Resultados_Fundamentalistas = '14.04.01 - ROAS (EBIT por Ativos) - Resultados Fundamentalistas'
_1501_Remuneração_de_Capital_Resultados_Fundamentalistas = '15.01 - Remuneração de Capital - Resultados Fundamentalistas'
_150101_Remuneração_de_Capital_de_Terceiros_por_Remuneração_de_Capital_Resultados_Fundamentalistas = '15.01.01 - Remuneração de Capital de Terceiros por Remuneração de Capital - Resultados Fundamentalistas'
_15010101_Juros_Pagos_por_Remuneração_de_Capital_de_Terceiros_Resultados_Fundamentalistas = '15.01.01.01 - Juros Pagos por Remuneração de Capital de Terceiros - Resultados Fundamentalistas'
_15010102_Aluguéis_por_Remuneração_de_Capital_de_Terceiros_Resultados_Fundamentalistas = '15.01.01.02 - Aluguéis por Remuneração de Capital de Terceiros - Resultados Fundamentalistas'
_150102_Remuneração_de_Capital_Próprio_por_Remuneração_de_Capital_Resultados_Fundamentalistas = '15.01.02 - Remuneração de Capital Próprio por Remuneração de Capital - Resultados Fundamentalistas'
_15010201_Juros_Sobre_o_Capital_Próprio_por_Remuneração_de_Capital_Próprio_Resultados_Fundamentalistas = '15.01.02.01 - Juros Sobre o Capital Próprio por Remuneração de Capital Próprio - Resultados Fundamentalistas'
_15010202_Dividendos_por_Remuneração_de_Capital_Próprio_Resultados_Fundamentalistas = '15.01.02.02 - Dividendos por Remuneração de Capital Próprio - Resultados Fundamentalistas'
_15010203_Lucros_Retidos_por_Remuneração_de_Capital_Próprio_Resultados_Fundamentalistas = '15.01.02.03 - Lucros Retidos por Remuneração de Capital Próprio - Resultados Fundamentalistas'
_1502_Remuneração_de_Capital_por_EBIT_Resultados_Fundamentalistas = '15.02 - Remuneração de Capital por EBIT - Resultados Fundamentalistas'
_150201_Impostos_por_EBIT_Resultados_Fundamentalistas = '15.02.01 - Impostos por EBIT - Resultados Fundamentalistas'
_1601_Margem_Bruta__Resultado_Bruto__Receita_Líquida__por_Receita_Bruto__Resultados_Fundamentalistas = '16.01 - Margem Bruta (Resultado Bruto (Receita Líquida) por Receita Bruto) - Resultados Fundamentalistas'
_1602_Margem_Operacional__Receitas_Operacionais_por_Receita_Bruta__Resultados_Fundamentalistas = '16.02 - Margem Operacional (Receitas Operacionais por Receita Bruta) - Resultados Fundamentalistas'
_160201_Força_de_Vendas__Despesas_com_Vendas_por_Despesas_Operacionais__Resultados_Fundamentalistas = '16.02.01 - Força de Vendas (Despesas com Vendas por Despesas Operacionais) - Resultados Fundamentalistas'
_160202_Peso_Administrativo__Despesas_com_Administração_por_Despesas_Operacionais__Resultados_Fundamentalistas = '16.02.02 - Peso Administrativo (Despesas com Administração por Despesas Operacionais) - Resultados Fundamentalistas'
_1603_Margem_EBITDA__EBITDA_por_Resultado_Bruto__Receita_Líquida___Resultados_Fundamentalistas = '16.03 - Margem EBITDA (EBITDA por Resultado Bruto (Receita Líquida)) - Resultados Fundamentalistas'
_160301_Margem_EBIT__EBIT_por_Resultado_Bruto__Receita_Líquida___Resultados_Fundamentalistas = '16.03.01 - Margem EBIT (EBIT por Resultado Bruto (Receita Líquida)) - Resultados Fundamentalistas'
_160302_Margem_de_Depreciação_por_Resultado_Bruto__Receita_Líquida__Resultados_Fundamentalistas = '16.03.02 - Margem de Depreciação por Resultado Bruto (Receita Líquida) - Resultados Fundamentalistas'
_1604_Margem_Não_Operacional__Resultado_Não_Operacional_por_Resultado_Bruto__Receita_Líquida___Resultados_Fundamentalistas = '16.04 - Margem Não Operacional (Resultado Não Operacional por Resultado Bruto (Receita Líquida)) - Resultados Fundamentalistas'
_1605_Margem_Líquida__Lucro_Líquido_por_Receita_Bruta__Resultados_Fundamentalistas = '16.05 - Margem Líquida (Lucro Líquido por Receita Bruta) - Resultados Fundamentalistas'
_1701_Caixa_Total_Análise_do_Fluxo_de_Caixa = '17.01 - Caixa Total - Análise do Fluxo de Caixa'
_1702_Caixa_Livre_Análise_do_Fluxo_de_Caixa = '17.02 - Caixa Livre - Análise do Fluxo de Caixa'
_170301_Caixa_de_Investimentos_por_Caixa_das_Operações_Análise_do_Fluxo_de_Caixa = '17.03.01 - Caixa de Investimentos por Caixa das Operações - Análise do Fluxo de Caixa'
_170302_Caixa_de_Investimentos_por_EBIT_Análise_do_Fluxo_de_Caixa = '17.03.02 - Caixa de Investimentos por EBIT - Análise do Fluxo de Caixa'
_1704_Caixa_Imobilizado_Análise_do_Fluxo_de_Caixa = '17.04 - Caixa Imobilizado - Análise do Fluxo de Caixa'
_1705_FCFF_simplificado__Caixa_Livre_para_a_Firma__Análise_do_Fluxo_de_Caixa = '17.05 - FCFF simplificado (Caixa Livre para a Firma) - Análise do Fluxo de Caixa'
_1706_FCFE_simplificado__Caixa_Livre_para_os_Acionistas__Análise_do_Fluxo_de_Caixa = '17.06 - FCFE simplificado (Caixa Livre para os Acionistas) - Análise do Fluxo de Caixa'
_1801_Margem_de_Vendas_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.01 - Margem de Vendas por Valor Agregado - Análise do Valor Agregado'
_1802_Custo_dos_Insumos_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.02 - Custo dos Insumos por Valor Agregado - Análise do Valor Agregado'
_1803_Valor_Adicionado_Bruto_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.03 - Valor Adicionado Bruto por Valor Agregado - Análise do Valor Agregado'
_1804_Retenções_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.04 - Retenções por Valor Agregado - Análise do Valor Agregado'
_1805_Valor_Adicionado_Líquido_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.05 - Valor Adicionado Líquido por Valor Agregado - Análise do Valor Agregado'
_1806_Valor_Adicionado_em_Transferência_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.06 - Valor Adicionado em Transferência por Valor Agregado - Análise do Valor Agregado'
_1807_Recursos_Humanos_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.07 - Recursos Humanos por Valor Agregado - Análise do Valor Agregado'
_180701_Remuneração_Direta__Recursos_Humanos__por_Valor_Agregado_Análise_do_Valor_Agregado = '18.07.01 - Remuneração Direta (Recursos Humanos) por Valor Agregado - Análise do Valor Agregado'
_180702_Benefícios__Recursos_Humanos__por_Valor_Agregado_Análise_do_Valor_Agregado = '18.07.02 - Benefícios (Recursos Humanos) por Valor Agregado - Análise do Valor Agregado'
_180703_FGTS__Recursos_Humanos__por_Valor_Agregado_Análise_do_Valor_Agregado = '18.07.03 - FGTS (Recursos Humanos) por Valor Agregado - Análise do Valor Agregado'
_1808_Impostos_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.08 - Impostos por Valor Agregado - Análise do Valor Agregado'
_1809_Remuneração_de_Capital_de_Terceiros_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.09 - Remuneração de Capital de Terceiros por Valor Agregado - Análise do Valor Agregado'
_180901_Juros_Pagos_a_Terceiros_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.09.01 - Juros Pagos a Terceiros por Valor Agregado - Análise do Valor Agregado'
_180902_Aluguéis_Pagos_a_Terceiros_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.09.02 - Aluguéis Pagos a Terceiros por Valor Agregado - Análise do Valor Agregado'
_1810_Remuneração_de_Capital_Próprio_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.10 - Remuneração de Capital Próprio por Valor Agregado - Análise do Valor Agregado'
_181001_Juros_Sobre_Capital_Próprio_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.10.01 - Juros Sobre Capital Próprio por Valor Agregado - Análise do Valor Agregado'
_181002_Dividendos_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.10.02 - Dividendos por Valor Agregado - Análise do Valor Agregado'
_181002_Lucros_Retidos_por_Valor_Agregado_Análise_do_Valor_Agregado = '18.10.02 - Lucros Retidos por Valor Agregado - Análise do Valor Agregado'
_181101_Alíquota_de_Impostos__Impostos__Taxas_e_Contribuições_por_Receita_Bruta__Análise_do_Valor_Agregado = '18.11.01 - Alíquota de Impostos (Impostos, Taxas e Contribuições por Receita Bruta) - Análise do Valor Agregado'
_181102_Taxa_de_Juros_Pagos__Remuneração_de_Capital_de_Terceiros_por_Receita_Bruta_Análise_do_Valor_Agregado = '18.11.02 - Taxa de Juros Pagos (Remuneração de Capital de Terceiros por Receita Bruta - Análise do Valor Agregado'
_181103_Taxa_de_Proventos_Gerados__Remuneração_de_Capital_Próprio_por_Receita_Bruta_Análise_do_Valor_Agregado = '18.11.03 - Taxa de Proventos Gerados (Remuneração de Capital Próprio por Receita Bruta - Análise do Valor Agregado'
