import assets.helper as b3

def my_periodic_task():
    ## BASE GROUND UPDATE
    # value = 'update_b3_companies'
    # value = b3.update_b3_companies(value)

    # value = 'world_markets'
    # value = b3.update_world_markets(value)

    ## B3 COMPANIES BALANCE SHEETS
    # value = 'nsd'
    # value = b3.get_nsd_links(value)

    # value = 'dre_raw'
    # value = b3.get_dre(value)

    # value = 'dre_math'
    # value = b3.dre_math(value)

    # value = 'dre_intel'
    # value = b3.dre_intel(value)

    value = 'dre_pivot'
    value = b3.dre_pivot(value)

    # value = 'dre_cvm'
    # value = b3.dre_cvm(value)

    ## MACROECONOMIC DATA 
    # BCB, Tesouro Nacional, YFinance, Investing, FRED, Alpha Vantage, Quandl, Pandas DataReader

    # BCB   url = f'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={dataInicial}&dataFinal={dataFinal}'
    # Tesouro Direto https://www.tesourotransparente.gov.br/ckan/dataset
    # yfinance !pip install yfinance -q -U
    # Investing 
    # Alpha Vantage
    # Quandl


    # value = 'yahoo_cotahist'
    # value = b3.yahoo_cotahist(value)

    value = 'yahoo quotes'
    value = b3.yahoo_quotes(value)

    # value = 'investing'
    # value = b3.eco_investing(value)

    print("All updated!")
try:
    if __name__ == "__main__":
        my_periodic_task()  
except Exception as e:
    print(e)
    pass