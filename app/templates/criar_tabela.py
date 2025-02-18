import psycopg2 as ps
import csv, os


folder = 'resultado'
arquivos = os.listdir(folder)

emotion_sets = {
    "tristeza": ["sadness", "grief", "loneliness", "regret", "disappointment"],
    "amor": ["love", "admiration", "approval", "caring", "desire"],
    "alegria": ["joy", "relief", "amusement", "gratitude", 
                "pride", "optimism", "realization", "excitement"],
    "curiosidade": ["curiosity", "excitement", "amusement"],
    "medo": ["fear", "nervousness", "excitement", "amusement"],
    "nojo": ["disgust", "embarrassment", "remorse", "disappointment", "disapproval"],
    "raiva": ["anger", "annoyance", "nervousness", "remorse"],
    "surpresa": ["surprise", "admiration", "confusion"]
}

def calcular_e_armazenar_rankings():
    conn = ps.connect(host='localhost', database='tcc', user='postgres', password='123')

    if conn:
        cursor = conn.cursor()
        
        # Obtenha a lista única de video_ids e seus títulos
        cursor.execute("SELECT DISTINCT video_id, title FROM scores")
        videos = cursor.fetchall()

        for video_id, title in videos:
            # Calcule a pontuação total (excluindo emoções neutras)
            query_total = '''
            SELECT SUM(score) 
            FROM scores
            WHERE video_id = %s AND emotion_label != 'neutral'
            '''
            cursor.execute(query_total, (video_id,))
            total_score = cursor.fetchone()[0]

            # Se `total_score` for None, significa que não há dados para o vídeo
            if total_score is None or total_score == 0:
                continue  # Pula esse vídeo

            for set_name, emotions in emotion_sets.items():
                # Calcule a pontuação do conjunto específico de emoções
                query_individual = f'''
                SELECT SUM(score) 
                FROM scores
                WHERE video_id = %s AND emotion_label = ANY(%s)
                '''
                cursor.execute(query_individual, (video_id, emotions))
                individual_score = cursor.fetchone()[0] or 0  # Define 0 se não houver pontuação

                # Calcule a pontuação normalizada
                normalized_score = individual_score / total_score

                # Insira o resultado na tabela 'rankings'
                insert_query = '''
                INSERT INTO rankings (video_id, title, emotion_set, normalized_score)
                VALUES (%s, %s, %s, %s)
                '''
                cursor.execute(insert_query, (video_id, title, set_name, normalized_score))

        # Confirme as alterações
        conn.commit()
        cursor.close()
        conn.close()
        print("Pontuações normalizadas e títulos calculados e armazenados na tabela 'rankings'.")


conn = ps.connect(host='localhost', database='tcc', user='postgres', password='123')
cursor = conn.cursor()

create_scores ='''
CREATE TABLE IF NOT EXISTS scores(
    id SERIAL PRIMARY KEY, 
    video_id VARCHAR(50),
    title TEXT, 
    comment TEXT, 
    emotion_label VARCHAR(50), 
    score DOUBLE PRECISION
)
'''

create_rankings = '''
CREATE TABLE IF NOT EXISTS rankings (
    video_id VARCHAR,
    title VARCHAR,
    emotion_set VARCHAR,
    normalized_score FLOAT
);

'''

cursor.execute(create_scores)
cursor.execute(create_rankings)

for arq in arquivos:
    if(os.path.exists(f'{folder}/{arq}')):
        with open(f'{folder}/{arq}', 'r', encoding='utf-8') as arq2:
            reader = csv.reader(arq2)
            next(reader)

            for linha in reader:
                video_id = linha[0]
                title = linha[1]
                comment = linha[2]
                emotion_label = linha[3]
                score = float(linha[4])

                inserir = '''
                INSERT INTO scores (video_id, title, comment, emotion_label, score) 
                VALUES (%s, %s, %s, %s, %s)
                '''
                cursor.execute(inserir, (video_id, title, comment, emotion_label, score))

conn.commit()
calcular_e_armazenar_rankings()


cursor.close()
conn.close()


