import os
import streamlit as st
import pandas as pd

from langchain.llms import OpenAI
import json
from langchain.embeddings import OpenAIEmbeddings
from db import config
import openai

db = config


def main():
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    st.header("Ask your CSV 📄")
    documents = st.file_uploader("Upload your file(s)", accept_multiple_files=True)
    opciones = ["Gerente logístico", "Asistente logístico"]
    selected = st.selectbox("Elige la manera en que quieres que responda: ",options=opciones)
    user_question = st.text_input("Ask a question about logistics: ")

    # embeddigns = OpenAIEmbeddings(openai_api_key=OpenAI.api_key)
    
    if documents: 
        for file in documents:
            documentName = str(file.name)
            extension = os.path.splitext(documentName)

            if extension[1] == '.csv':
                csv_data_fragment = pd.read_excel(file)
                json_string = csv_data_fragment.to_json(orient="index")
                parsed_json= json.loads(json_string)
                for i in parsed_json:
                    try:
                        data = parsed_json[f'{i}']
                        prueba = parsed_json['15']
                        db.insertOneDocument(data)
                    except: print("p")

            elif extension[1] in [".xlsx", ".xls"]:
                
                excel_data_fragment = pd.read_excel(file)
                json_string = excel_data_fragment.to_json(orient="index").lower()
                print(json_string)
                parsed_json= json.loads(json_string)
                for i in parsed_json:
                    try:
                        data = parsed_json[f'{i}']
                        db.insertOneDocument(data)
                
                    except: print("p")
    
    if user_question is not None and user_question != "":
            st.spinner("In progress")
            if selected == "Gerente logístico" or selected == opciones[0]:
                    user_question += "Indica la respuesta de manera gerencial, dando recomendacion de acuerdo a la pregunta realizada., si solicita información puntual de solo una orden de compra o número de embarque recomiéndale que elija la opción de Asistente logístico. La información enviada está en formato JSON, por lo que relaciona la información a través de las etiquetas JSON."
            if selected == "Asistente logístico" or selected == opciones[1]:
                    user_question += "Responder como Asistente de Logistica, indicar respuestas claras y completas, incluyendo todo detalle, si solicita información general que incluye la búsqueda de varias ordenes de compra recomiéndale que elija la opción de gerente. relaciona la información a través de la etiqueta JSON de números, es decir, en un solo diccionario está la información"



if __name__ == "__main__":
    main()

# python -m streamlit run main.py
#que información tienes acerca del pedido 4700088934