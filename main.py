from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from db import config
import pandas as pd
import pymongo
import openai
import tempfile
import json
import os


db = config
app = Flask(__name__) 
openai.api_key = os.getenv('OPENAI_API_KEY')
CORS(app)
@app.route('/')
def index():
    return render_template('index.html') 


# RUTA MAIN DE FLOWISE SIN IMPLEMENTAR CSV
@app.route('/search', methods=['POST'])
def searchLucho():

    try:
        json_req = request.get_json()
        pedido = json_req.get('pedido')

        result = db.db.prueba.find({'pedido': int(pedido)},{'_id': False})
        
        list_result = list(result)
        if len(list_result) == 0:
            return "El pedido no existe."
        
        string_list = str(list_result[0])

        system_message = json_req.get('system_message')
        llm = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_message}, {"role": "user", "content": string_list} ],
            temperature= 0
        )
            
        a = llm.choices[0].message.content

    except pymongo.errors.ConnectionFailure as error:
        err = f'Please ensure that you are writing properly the information { error}'
        return err
    
    return a

@app.route('/split', methods=['POST'])
def split():
    try:
        json_req = request.get_json()
        pedido = json_req.get('pedido')

        result = db.db.prueba.find({'pedido': int(pedido)},{'_id': False})
        
        list_result = list(result)
        
        datos = json_req.get('datos')
        split_datos = datos.split(',')
        
        a = []
        for i in split_datos:

            item = i.strip()
            for cantidadPos in range(len(list_result)):
                new_results = f"{i}: {list_result[cantidadPos].get(item, 'No encontrado')}"
                new_results.strip()
                a.append(new_results)
        print(a)
        p = json.dumps(a)

        # string_list = str(list_result)
        # result_json = json.loads(string_list)
        
        # result_pedido = list_result
        if len(list_result) == 0:
            return "El pedido no existe."
        
        string_list = str(list_result)

        system_message = json_req.get('system_message')
        llm = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_message}, {"role": "user", "content": p} ],
            temperature= 0
        )
            
        a = llm.choices[0].message.content

    except pymongo.errors.ConnectionFailure as error:
        err = f'Please ensure that you are writing properly the information { error}'
        return err

    return a
# ¡¡NO TOCAR!!
# SUBIR ARCHIVOS A LA BASE DE DATOS (MONGODB)
@app.route('/upload', methods=['POST'])
def uploadFiles():
    
    try:
        if 'file' not in request.files:
            return jsonify(error="No file provided")
        
        res = request.files['file']
        
        filename = secure_filename(res.filename)
        unique_filename = os.path.splitext(filename)[1]

        if unique_filename == '.xlsx' or unique_filename == ".xls":
            
            excel_data_fragment = pd.read_excel(res, engine='openpyxl')
            json_string = excel_data_fragment.to_json(orient="index").lower()
            parsed_json = json.loads(json_string)
            
            complete_data = []
            for i in parsed_json:
                data = parsed_json[f'{i}']
                complete_data.append(data)
                
            try:
                db.db.collection.insert_many(complete_data)
                res = "All files successfully added to the database."
                return res
            except:
                return "The data couldn't be added to the database."
        else:
            return jsonify(error="Unsupported file format")
    except Exception as e:
        return jsonify(error=str(e))
    
    
@app.route('/endpoint', methods=['POST'])
def handle_request():
    data = request.json

    for key, value in data.items():
        print(f"{key}: {value}\n")
    return "si"


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)


#string_data = str(result_data)
        # string_data= string_data.strip('[]')
        # result_data = json.loads(string_data)