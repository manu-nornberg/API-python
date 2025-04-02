import sqlite3 
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute(
            """
                CREATE TABLE IF NOT EXISTS LIVROS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    titulo TEXT NOT NULL,  
                    categoria TEXT NOT NULL,  
                    autor TEXT NOT NULL,  
                    imagem_url TEXT NOT NULL  
                )
            """
        )

init_db()

@app.route('/')
def home():
    return "Bem-vindo a API de Livros!"


@app.route('/doar', methods=['POST'])
def doar_livro():
        data = request.get_data(as_text=True)  
        data = data.encode('utf-8') 
        data = json.loads(data)

        if not all(key in data for key in ('titulo', 'categoria', 'autor', 'imagem_url')):
            return jsonify({'error': 'Faltam dados obrigatórios!'}), 400

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO LIVROS (titulo, categoria, autor, imagem_url)
                VALUES (?, ?, ?, ?)
                """, 
                (data['titulo'], data['categoria'], data['autor'], data['imagem_url'])
            )
            conn.commit()

        return jsonify({'message': 'Livro cadastrado com sucesso!'}), 201

@app.route('/livros', methods=['GET'])
def listar_livros():
    try:
        with sqlite3.connect("database.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM LIVROS")
            livros = cursor.fetchall()

        livros_lista = [
            {
                'id': livro['id'],
                'titulo': livro['titulo'],
                'categoria': livro['categoria'],
                'autor': livro['autor'],
                'imagem_url': livro['imagem_url']
            }
            for livro in livros
        ]

        return jsonify(livros_lista)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM LIVROS WHERE id = ?", (id,))
            conn.commit()

        return jsonify({"message": "Livro excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)