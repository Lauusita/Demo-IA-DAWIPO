from flask import Flask, request, jsonify, render_template 
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pymongo
import openai
from db import config
import pandas as pd
import json
import os


db = config
app = Flask(__name__) 

CORS(app)
@app.route('/')
def index():
    return render_template('index.html') 


@app.route("/searchjuan", methods=["POST"])
def searchJuan():

    res = request.get_data().decode('utf-8')

    loader_json_res = json.loads(res)
    
    prompt= loader_json_res.get('match', {}).get('resolvedInput', "")
    parameters = loader_json_res.get('match', {}).get('parameters', {})

    returned_json = {'prompt': prompt, **parameters}
    string_returned_json = str(returned_json)
    
    try:    
            if (res==None or res==""):
                execute = "digite prompt"
                return execute
            else:
                prompt = f"""Translate the following JSON (sometimes natural language query, whatever)  into a MongoDB query using the method find() and giving just the filter as a dictionary (everything is sent in lower case), example, DO NOT give me: db.collection.find(), just give me the list, example: ("pedido" (EVERYTHING IN LOWER CASE) : 356783 (it is important to take care about how the information is sent, if there are just numbers, the data type at the moment to filter as dict is a number NOT A STRING, example, if i sent you "el pedido 39666", you will treat the number 39666 (and whatever number) as an int), the same if it has letters (string). If someone wants de mongo id, please sent the dict as _id) the collection name's is collection: {string_returned_json}. Please try to predict when someone make a mistake, example, if they write ?pido or pwdido try to predict the correct word, take this as keys to predict words ['_id', '_rownum', 'columna1', 'soc', 'pedido', 'incoterm', 'ciudad incoterm', 'via', 'paisorigen (bl)', 'aduanasalida (fact)', 'aduanallegada (fact)', 'via fra ', 'incoterm fra ', 'region origen', 'país origen fra ', 'ciudad origen fra ', 'ciudad destino fra', 'fecha est ent prov (**)', 'fecha real entr prov', 'factura (el tipo de dato de la factura es String)', 'fecha factura', 'doc transporte', 'sede bl', 'cont - carga s', 'serie nacionalización ', 'fecha etd', 'fecha embarque', 'fecha eta', 'fecha real llegada ', 'fecha levante / liberación', 'fecha max devolución cont ', 'naviera bl', 'embarcador manejo ', 'ee', 'fecha ee', 'rp', 'fecha rp', 'doc contable', 'fecha doc contable', 'cantidad ped', 'terminal arribo', 'gestor front op', 'cordimpo_ped', 'desc.coordinadora', 'anaimpo_ped', 'desc.analista', 'cod.agenciaaduana', 'desc.agenciaaduana', 'observacion_coordinador', 'filtro_proyectos', 'contar ', 'semana entrega proveedor', 'año entrega proveedor', 'semana despacho', 'año despacho', 'clave', 'nombre carpeta documentos ', 'sigla gestor '] and put it logic, example, if someone give you dame informacion de la ciudad del pedido xxx, do not send that ciudad: 57676 bc it has not sense. if the user ask you a question in other language different of spanish, answer them in the same language as the question"""
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature= 0
                )
                
                string_mongo = str(response.choices[0].message.content).strip()
                print(string_mongo)
        
                result = db.db.collection.find(eval(string_mongo),{'_id': False})
                list_result = list(result)

    except pymongo.errors.ConnectionFailure as error:
        err = f'Please ensure that you are writing properly the information { error}'
        return err
    return jsonify(list_result)
    

@app.route('/search', methods=['POST'])
def searchLucho():
    res = request.get_data().decode('utf-8')

    loader_json_res = json.loads(res)
    
    string_returned_json = str(loader_json_res)
    
    try:    
            if (res==None or res==""):
                execute = "digite prompt"
                return execute
            else:
                prompt = f"""Translate the following JSON (sometimes natural language query, whatever)  into a MongoDB query using the method find() and giving just the filter as a dictionary (everything is sent in lower case), example, DO NOT give me: db.collection.find(), just give me the list, example: ("pedido" (EVERYTHING IN LOWER CASE) : 356783 (it is important to take care about how the information is sent, if there are just numbers, the data type at the moment to filter as dict is a number NOT A STRING, example, if i sent you "el pedido 39666", you will treat the number 39666 (and whatever number) as an int), the same if it has letters (string). If someone wants de mongo id, please sent the dict as _id) the collection name's is collection: {string_returned_json}. Please try to predict when someone make a mistake, example, if they write ?pido or pwdido try to predict the correct word, take this as keys to predict words ['_id', '_rownum', 'columna1', 'soc', 'pedido', 'incoterm', 'ciudad incoterm', 'via', 'paisorigen (bl)', 'aduanasalida (fact)', 'aduanallegada (fact)', 'via fra ', 'incoterm fra ', 'region origen', 'país origen fra ', 'ciudad origen fra ', 'ciudad destino fra', 'fecha est ent prov (**)', 'fecha real entr prov', 'factura (el tipo de dato de la factura es String)', 'fecha factura', 'doc transporte', 'sede bl', 'cont - carga s', 'serie nacionalización ', 'fecha etd', 'fecha embarque', 'fecha eta', 'fecha real llegada ', 'fecha levante / liberación', 'fecha max devolución cont ', 'naviera bl', 'embarcador manejo ', 'ee', 'fecha ee', 'rp', 'fecha rp', 'doc contable', 'fecha doc contable', 'cantidad ped', 'terminal arribo', 'gestor front op', 'cordimpo_ped', 'desc.coordinadora', 'anaimpo_ped', 'desc.analista', 'cod.agenciaaduana', 'desc.agenciaaduana', 'observacion_coordinador', 'filtro_proyectos', 'contar ', 'semana entrega proveedor', 'año entrega proveedor', 'semana despacho', 'año despacho', 'clave', 'nombre carpeta documentos ', 'sigla gestor '] and put it logic, example, if someone give you dame informacion de la ciudad del pedido xxx, do not send that ciudad: 57676 bc it has not sense. if the user ask you a question in other language different of spanish, answer them in the same language as the question"""
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature= 0
                )
                
                string_mongo = str(response.choices[0].message.content).strip()
                print(string_mongo)
        
                result = db.db.collection.find(eval(string_mongo),{'_id': False})
                list_result = list(result)

    except pymongo.errors.ConnectionFailure as error:
        err = f'Please ensure that you are writing properly the information { error}'
        return err
    return jsonify(list_result)


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
    app.run(host='0.0.0.0',port=5000)
