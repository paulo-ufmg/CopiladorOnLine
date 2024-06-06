from flask import Flask, request, render_template, jsonify
import subprocess
from jinja2 import Environment
import re

# Definição da função de filtro
def extrair_nome_da_funcao(entrada):
    padrao = r"def\s+(\w+)\s*\(.*\):"
    match = re.match(padrao, entrada)
    if match:
        return match.group(1)
    else:
        return None

def leiaMetodos(metodos):
    try:
        with open ("metodos.txt", "r",encoding='utf-8') as arq:
            while True:
                line = arq.readline()
                if not line: break #interrompe ao final do arquivo
                if line.strip() == "": continue  # Ignorar linhas em branco
                if line.strip()[0]==";": continue # ignora linhas de comentário

                if(line.strip().startswith('>')): #Identificado novo metodo
                    chave =  line.strip()[1:]
                    metodos[chave] = []
                else:
                    if chave in metodos:
                        metodos[chave].append(line)
    except FileNotFoundError:
        print("Falha ao acessar arquivo!")                        



app = Flask(__name__)

# Registrar a função como um filtro personalizado
app.jinja_env.filters['extrair_nome_da_funcao'] = extrair_nome_da_funcao

@app.route('/')
def index():
    metodos = dict()
    leiaMetodos(metodos)
    return render_template('index.html', metodos=metodos)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    code = data['code']
    
    try:
        result = subprocess.run(['python', '-c', code], capture_output=True, text=True)
        output = result.stdout.strip()
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
