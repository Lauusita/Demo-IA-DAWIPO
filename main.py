import os
import streamlit as st
import pandas as pd
from langchain.chat_models import ChatOpenAI
import openpyxl
from langchain.llms import OpenAI
import json
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain.vectorstores.pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferWindowMemory
from PIL import Image 

import pinecone




def main():

        OpenAI.api_key = os.getenv('OPENAI_API_KEY')
        
        pinecone.init(api_key="5c4ae0f5-57b8-456a-9269-73eb310c4512", environment= os.getenv('PINECONE_ENV'))
        index = pinecone.Index('wipoia')
        st.set_page_config("Dawipo AI", "./assets/favicon.png",layout="centered")

        image = Image.open('./assets/dawipo.png ')
        st.sidebar.image(image, caption='Feel the power of your company Supply Chain Data')

        documents = st.file_uploader("Upload your file(s)", accept_multiple_files=True)

        opciones = ["Gerente logístico", "Asistente logístico"]
        selected = st.selectbox("Elige la manera en que quieres que responda: ",options=opciones)

        user_question = st.text_input("Ask a question about logistics: ")
        
        llm = ChatOpenAI(
                temperature=0,
                model="gpt-3.5-turbo",
                )
        
        embeddigns = OpenAIEmbeddings(openai_api_key=OpenAI.api_key)
        ids = list('abcdefg')
        if documents: 
                for file in documents:
                        documentName = str(file.name)
                        extension = os.path.splitext(documentName)

                        if extension[1] == '.csv':
                                
                                agent = create_csv_agent(
                                        llm,
                                        [file],
                                        verbose=True,
                                        agent_type=AgentType.OPENAI_FUNCTIONS
                                )
                                agent.handle_parsing_errors = True
                                # stringAgent = str(agent.tools[0].locals)
                                lenStringAgent = agent.tools[0].locals
                                
                                print(extension)

                                for i in range(len(lenStringAgent)):
                                        dataFrameSplitted = agent.tools[0].locals[f'df{i+1}']

                                        stringDFcsv = str(dataFrameSplitted)

                                        csvDoc = RecursiveCharacterTextSplitter(chunk_size= 1536)
                                        csv = csvDoc.split_text(stringDFcsv)

                                        Pinecone.from_texts(csv, embeddigns, index_name="wipoia")

                        elif extension[1] in [".xlsx", ".xls"]:

                                
                                excel_data_fragment = pd.read_excel(file, sheet_name="Hoja1")
                                
                                json_string = excel_data_fragment.to_json()
                                parsed_json= json.loads(json_string)
                                parsed_json

                                a = str(parsed_json)
                                print(parsed_json)
                                xlsxDoc = RecursiveCharacterTextSplitter(chunk_size= 1536)
                                xlsx = xlsxDoc.split_text(a)
                                Pinecone.from_texts(xlsx, embeddigns, index_name="wipoia")
        
        
        searchVector = Pinecone.from_existing_index("wipoia", embeddigns)
        print('se ha conectado')
        print(selected)

        
        

        def search(vector, prompt):
                
                llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
                retriever = vector.as_retriever(search_type="similarity")
                
                cadena = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever= retriever)
                a = ConversationBufferWindowMemory()
                run = cadena.run(prompt)
                return run
        
        if user_question is not None and user_question != "":
                st.spinner("In progress")
                if selected == "Gerente logístico" or selected == opciones[0]:
                        user_question += "Indica la respuesta de manera gerencial, , dando recomendacion de acuerdo a la pregunta realizada., si solicita información puntual de solo una orden de compra o número de embarque recomiéndale que elija la opción de Asistente logístico. La información enviada está en formato JSON, por lo que relaciona la información a través de las etiquetas JSON."
                if selected == "Asistente logístico" or selected == opciones[1]:
                        user_question += "Responder como Asistente de Logistica, indicar respuestas claras y completas, incluyendo todo detalle, si solicita información general que incluye la búsqueda de varias ordenes de compra recomiéndale que elija la opción de gerente. relaciona la información a través de la etiqueta JSON de números, es decir, en un solo diccionario está la información"
        
        response = search(searchVector, user_question)
        st.write(response)
        print(response)
        
if __name__ == "__main__":

        main()



# python -m streamlit run <filename.py> 
#que información tienes acerca del pedido 4700088934