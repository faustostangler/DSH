from . import helper as b3
from . import main
from . import cvm

def load_database():
    """
    This function loads a series of databases in a specific order, with each database potentially
    depending on previous ones. If a database cannot be loaded, it's generated based on its dependencies.
    
    Order & Dependencies:
    1. 'acoes' 
        - Directly loaded or generated using get_composicao_acionaria()
    
    2. 'intelacoes'
        - Depends on: 'acoes' & 'intel_b3'
        - Loaded directly or generated using compose_intel()

    3. 'intel_b3'
        - Depends on: 'b3_cvm'
        - Loaded directly or generated using prepare_b3_cvm()

    4. 'b3_cvm'
        - Depends on: 'company' & 'math'
        - Loaded directly or generated using get_companies()

    5. 'company'
        - Directly loaded or generated using b3_get_companies(b3.search_url)

    6. 'math'
        - Directly loaded or generated using get_math_from_b3_cvm()

    7. 'fund'
        - Depends on: 'intelacoes'
        - Loaded directly or generated using compose_fund()

    Returns:
        fund (dict): The final loaded or generated database.
    """
    # # Step 1: Load or prepare 'acoes'
    # acoes = stk_get_composicao_acionaria()
    print('fast debug acoes')
    filename = 'acoes'
    columns = ['Companhia', 'Trimestre', 'Ações ON', 'Ações PN', 'Ações ON em Tesouraria', 'Ações PN em Tesouraria', 'URL']
    # acoes = sys_read_or_create_dataframe(filename, columns)

    # Step 2: Load or prepare 'fund'
    try:
        fund = main.load_pkl(f'{b3.app_folder}/fund')
    except Exception as e:
        # Nested step: Load or prepare 'intelacoes'
        try:
            intelacoes = main.load_pkl(f'{b3.app_folder}/intelacoes')
        except Exception as e:
            # Nested step: Load or prepare 'intel_b3'
            try:
                intel_b3 = main.load_pkl(f'{b3.app_folder}/intel_b3')
            except Exception as e:
                # Further nested step: Load or prepare 'b3_cvm'
                try:
                    b3_cvm = main.load_pkl(f'{b3.app_folder}/b3_cvm')
                except Exception as e:
                    # Further nested step: Load or prepare 'company'
                    try:
                        # company = b3_get_companies(b3.search_url)
                        print('fast debug b3_company')
                        filename = 'company'
                        b3_cols = b3.cols_b3_companies + b3.col_b3_companies_extra_columns
                        company = main.read_or_create_dataframe('company', b3_cols).fillna('')
                    except Exception as e:
                        pass

                    # Further nested step: Load or prepare 'math'
                    try:
                        math = main.load_pkl(f'{b3.app_folder}/math')
                    except Exception as e:
                        cvm_local, cvm_web, cvm_updated = cvm.get_databases_from_cvm()
                        math_df = get_math_from_b3_cvm()
                        math_df = sys_save_pkl(math, f'{b3.app_folder}/math')
                    
                    # Use 'math' and 'company' to prepare 'b3_cvm'
                    b3_cvm = get_companies(math, company)
                    b3_cvm = sys_save_pkl(b3_cvm, f'{b3.app_folder}/b3_cvm')
                
                # Use 'b3_cvm' to prepare 'intel_b3'
                intel_b3 = prepare_b3_cvm(b3_cvm)
                intel_b3 = sys_save_pkl(intel_b3, f'{b3.app_folder}/intel_b3')

            # Use 'intel_b3' to prepare 'intelacoes'
            intelacoes = compose_intel(acoes, intel_b3)
            intelacoes = sys_save_pkl(intelacoes, f'{b3.app_folder}/intelacoes')
        
        # Use 'intelacoes' to prepare 'fund'
        fund = compose_fund(intelacoes)
        fund = sys_save_pkl(fund, f'{b3.app_folder}/fund')



    return fund
