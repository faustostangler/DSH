import assets.helper as b3
import assets.functions as run

intelacoes = run.compose_intel()
intelacoes = run.save_pkl(intelacoes, f'{b3.app_folder}/intelacoes')
print('done')