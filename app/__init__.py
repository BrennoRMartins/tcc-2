from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS
import db
from pathlib import Path

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET']) 
def index(): 
     return render_template('index.html')

@app.route('/ranking.html', methods=['GET'])
def ranking():
    return render_template('ranking.html')

@app.route('/avaliar.html', methods=['GET'])
def avaliar():
    return render_template('avaliar.html')

#rankings de emocao
@app.route('/rankings', methods=['GET'])
def ranquear():
    emotion = request.args.get('emotion')

    try:
        connection = db.conn()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT normalized_score, video_id, title
            FROM rankings
            WHERE emotion_set = %s
            ORDER BY normalized_score DESC
            LIMIT 3
            """
            cursor.execute(query, (emotion,))
            results = cursor.fetchall()
            videos = [{'video_id': row[1], 'title': row[2], 'score': row[0]} for row in results]

            cursor.close()
            connection.close()

            return jsonify(videos)

    except Exception as e:
        print(e)
        return jsonify({e}), 500

#graficos
@app.route('/chart-data', methods=['GET'])
def chart_data():
    video_id = request.args.get('video_id')

    try:
        connection = db.conn()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT emotion_set, normalized_score
            FROM rankings
            WHERE video_id = %s
            ORDER BY normalized_score DESC
            """
            cursor.execute(query, (video_id,))
            results = cursor.fetchall()
            data = [{'emotion_set': row[0], 'normalized_score': row[1]} for row in results]

            cursor.close()
            connection.close()

            return jsonify(data)

    except Exception as e:
        print(e)
        return jsonify(e), 500
    
@app.route('/agradecimento')
def agradecimento():
    return render_template('agradecimento.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        rating = request.form['rating']
        comment = request.form['comment']
        email = request.form['email']
        connection = db.conn()
        if connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO feedback (estrelas, comentario, email)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (rating, comment, email))
            connection.commit()

            cursor.close()
            connection.close()

            return render_template('agradecimento.html')
        else:
            return jsonify({"error": "Erro ao db ao banco de dados"}), 500
    except Exception as e:
        print(f"Erro ao processar feedback: {e}", flush=True)
        return jsonify(e), 500




if __name__ == '__main__':
    app.run(debug=True)
