from deep_translator import GoogleTranslator
import csv
import time
import requests
import json
import comments_trends as ct
import os

api_key = "AIzaSyBX_81NTz0lNuc5xjPoLZcfm-b-VRbnDc8"

inicio = time.time()

folder_name = "top_trending"
folder_name_translate = 'top_trending_translate'
arquivos = os.listdir(folder_name)
count = 0

if not os.path.exists(folder_name_translate):
    os.makedirs(folder_name_translate)


for arq in arquivos:
    if os.path.exists(f'{folder_name}/{arq}'):
        count += 1
        arq2 = f'{folder_name_translate}/top_{count}_translate.csv'

        with open(f'{folder_name}/{arq}', 'r', encoding='utf-8') as leitura, open(arq2, 'w', newline='', encoding='utf-8') as escrita:
            reader = csv.reader(leitura)
            writer = csv.writer(escrita)
            count_linhas = 0

            
            for linha in reader:
                if count_linhas >= 100:
                    break
                
                if(len(linha) >= 2):
                    video_id = linha[0]
                    title = linha[1]
                    comment = linha[2]

                    try: 
                        translated = GoogleTranslator(source='auto', target='en').translate(comment)
                        writer.writerow([video_id, title, translated])
                
                        print(f"{count_linhas} - {video_id}: {translated}")
                        time.sleep(0.1)
                        count_linhas += 1
                
                    except Exception as e:
                        print(f"Erro durante a tradução ou conexão: {e}")
    
    else:
        print(f"Arquivo {arq} não encontrado.")

fim = time.time()
total = fim - inicio
print(f'Tempo de execução = {total} segundos')
