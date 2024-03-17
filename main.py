# from flask import Flask, request, render_template, jsonify
# from flask_cors import CORS
# import subprocess

# # Para instalar os pacotes use pip install -r requirements.txt

# app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/execute', methods=['POST'])
# def execute():
#     data = request.get_json()
#     code = data['code']
    
#     try:
#         result = subprocess.run(['python', '-c', code], capture_output=True, text=True)
#         output = result.stdout.strip()
#         return jsonify({'output': output})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# if __name__ == '__main__':
#     app.run(debug=False)


from flask import Flask, request, render_template, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    app.run(host='0.0.0.0', port=5000)
