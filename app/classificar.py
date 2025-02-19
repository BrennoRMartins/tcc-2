
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
import os, json, csv, time

inicio = time.time()
DATA_DIR = 'data'
respostas = []
tokenizer = RobertaTokenizerFast.from_pretrained("EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("EmoRoBERTa")

emotion = pipeline('sentiment-analysis', 
                    model='EmoRoBERTa')

folder_name_translate = 'top_trending_translate'
folder_name_emotion = 'resultado'
arquivos = os.listdir(folder_name_translate)
count = 0

if not os.path.exists(folder_name_emotion):
    os.makedirs(folder_name_emotion)

for arq in arquivos:
    if os.path.exists(f'{folder_name_translate}/{arq}'):
        count += 1
        arq2 = f'{folder_name_emotion}/top_{count}_emotion.csv'

        with open(f'{folder_name_translate}/{arq}', 'r', encoding='utf-8') as leitura, open(arq2, 'w', newline='', encoding='utf-8') as escrita:
            reader = csv.reader(leitura)
            writer = csv.writer(escrita)

            writer.writerow(['video_id', 'title', 'comment', 'emotion_label', 'emotion_score'])
            
            respostas = []
            count_linhas = 0
            for linha in reader:
                if len(linha) >= 2:
                    video_id = linha[0]
                    title = linha[1]
                    comment = linha[2]   
                    
                    try:
                        emotion_labels = emotion(comment)
        
                        if emotion_labels and isinstance(emotion_labels, list):
                            emotion_label = emotion_labels[0]['label']
                            emotion_score = emotion_labels[0]['score']
                        else:
                            emotion_label = ''
                            emotion_score = ''

                        writer.writerow([video_id, title, comment, emotion_label, emotion_score])

                        print(f"{count_linhas} - {video_id}: {comment}")
                        print(f"Emoção: {emotion_label}, Score: {emotion_score}")
                        
                        count_linhas += 1
                    except Exception as e:
                        print(f"Erro durante a classificação de emoções: {e}")
                else:
                    print(f"Linha inválida ou vazia ignorada: {linha}")
    
    else:
        print(f"Arquivo {arq} não encontrado.")

fim = time.time()
total = fim - inicio
print(f'Tempo de execução = {total} segundos')