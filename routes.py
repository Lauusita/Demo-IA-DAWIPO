from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import pymongo
import openai
from db import config
import pandas as pd
import json
import os


db = config
app = Flask(__name__) 

@app.route("/search", methods=["POST"])
def search():

    res = request.get_data()
    try:    
            if (res==None or res==""):
                execute = "digite prompt"
                return execute
            else:
                prompt = f"""Translate the following natural language query (sometimes it could be a json, list, whatever)  into a MongoDB query using the method find() and giving just the filter as a dictionary (everything is sent in lower case), example, DO NOT give me: db.collection.find(), just give me the list, example: ("pedido" (EVERYTHING IN LOWER CASE) : 356783 (it is important to take care about how the information is sent, if there are just numbers, the data type at the moment to filter as dict is a number NOT A STRING, example, if i sent you "el pedido 39666", you will treat the number 39666 (and whatever number) as an int), the same if it has letters (string). If someone wants de mongo id, please sent the dict as _id) the collection name's is collection: {res}. Please try to predict when someone make a mistake, example, if they write ?pido or pwdido try to predict the correct word, take this as keys to predict words ['_id', '_rownum', 'columna1', 'soc', 'pedido', 'incoterm', 'ciudad incoterm', 'via', 'paisorigen (bl)', 'aduanasalida (fact)', 'aduanallegada (fact)', 'via fra ', 'incoterm fra ', 'region origen', 'país origen fra ', 'ciudad origen fra ', 'ciudad destino fra', 'fecha est ent prov (**)', 'fecha real entr prov', 'factura (el tipo de dato de la factura es String)', 'fecha factura', 'doc transporte', 'sede bl', 'cont - carga s', 'serie nacionalización ', 'fecha etd', 'fecha embarque', 'fecha eta', 'fecha real llegada ', 'fecha levante / liberación', 'fecha max devolución cont ', 'naviera bl', 'embarcador manejo ', 'ee', 'fecha ee', 'rp', 'fecha rp', 'doc contable', 'fecha doc contable', 'cantidad ped', 'terminal arribo', 'gestor front op', 'cordimpo_ped', 'desc.coordinadora', 'anaimpo_ped', 'desc.analista', 'cod.agenciaaduana', 'desc.agenciaaduana', 'observacion_coordinador', 'filtro_proyectos', 'contar ', 'semana entrega proveedor', 'año entrega proveedor', 'semana despacho', 'año despacho', 'clave', 'nombre carpeta documentos ', 'sigla gestor '] and put it logic, example, if someone give you dame informacion de la ciudad del pedido 57676, do not send that ciudad: 57676 bc it has not sense. if the user ask you a question in other language different of spanish, answer them in the same language as the question"""
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                string_mongo = str(response.choices[0].message.content).strip()
                print(string_mongo)

                result = db.db.collection.find(eval(string_mongo))
                list_result = list(result)
                
                str_response_result = str(list_result)
                
                template = f"Transforma el siguiente string: {str_response_result} en un párrafo coherente que presente la información de manera clara y concisa respecto a lo que se te pregunte. Asegúrate de incluir todos los detalles importantes y utilizar un lenguaje fácil de entender. Trata de precedir fechas de llegada, salida, por qué hay retraso, etc, y no solamente fechas sino otro tipo de datos que puedan ser predecibles; trata de dar más información que logres deducir de la información proporcionada. Ten muy en cuenta qué se te está preguntando, si hay 3 o más datos reconoce cuál de los datos es por el cual se está preguntando y cuáles datos se complementan el uno con el otro."

                openai_response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages= [{"role": "system", "content": template}, {"role": "user", "content": str(res)}]
                )   
                final_response = openai_response.choices[0].message.content
                print(openai_response)
                
    except pymongo.errors.ConnectionFailure as error:
        err = f'Please ensure that you are writing properly the information {response, error}'
        return err

    
    return final_response

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
            for i in parsed_json:
                try:
                    data = parsed_json[f'{i}']
                    db.insertOneDocument(data)
                    return "Files successfully added to the database."
                except:
                    return "The data couldn't be added to the database."
        else:
            return jsonify(error="Unsupported file format")
    except Exception as e:
        return jsonify(error=str(e))
    
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)

    # {pedido: [ 4700088934, 4700083159, 4700085940] } Also, the user can make a question in english, you will have to translate