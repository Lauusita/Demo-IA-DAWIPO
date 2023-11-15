import os
import streamlit as st
import pandas as pd
from langchain.chat_models import ChatOpenAI

from langchain.llms import OpenAI

from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain.vectorstores.pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
import pinecone



def main():

        OpenAI.api_key = os.getenv('OPENAI_API_KEY')
        
        pinecone.init(api_key="5c4ae0f5-57b8-456a-9269-73eb310c4512", environment= os.getenv('PINECONE_ENV'))

        st.set_page_config(page_title="Ask your CSV 📄")
        st.header("Ask your CSV 📄")

        documents = st.file_uploader("Upload your file(s)", accept_multiple_files=True)
        opciones = ["Gerente logístico", "Asistente logístico"]


        selected = st.selectbox("Elige la manera en que quieres que responda: ",options=opciones)

        user_question = st.text_input("Ask a question about logistics: ")
        
        llm = ChatOpenAI(
                temperature=0,
                model="gpt-3.5-turbo",
                )
        
        embeddigns = OpenAIEmbeddings(openai_api_key=OpenAI.api_key)
        
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
                                        print(dataFrameSplitted)  
                                        stringDFcsv = str(dataFrameSplitted)

                                        csvDoc = RecursiveCharacterTextSplitter(chunk_size= len(stringDFcsv), chunk_overlap=1)
                                        csv = csvDoc.split_text(stringDFcsv)

                                        Pinecone.from_texts(csv, embeddigns, index_name="wipoia")


                        elif extension[1] in [".xlsx", ".xls"]:
                                loader = pd.read_excel(file, engine='openpyxl')
                                stringDFxlsv = str(loader)

                                xlsxDoc = RecursiveCharacterTextSplitter(chunk_size= len(stringDFxlsv), chunk_overlap=1)
                                xlsx = xlsxDoc.split_text(stringDFxlsv)

                                # print(index.describe_index_stats())

                                Pinecone.from_texts(xlsx, embeddigns, index_name="wipoia")
        
        
        searchVector = Pinecone.from_existing_index("wipoia", embeddigns)
        print('se ha conectado')

        print(selected)

        def search(vector, prompt):
                llm = ChatOpenAI(model='gpt-4', temperature=0)
                retriever = searchVector.as_retriever(search_type="similarity")
                
                cadena = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever= retriever)
                run = cadena.run(prompt)
                return run
        
        if user_question is not None and user_question != "":
                st.spinner("In progress")

                if selected == "Gerente logístico" or selected == opciones[0]:
                        user_question += "Indica la respuesta de manera gerencial, , dando recomendacion de acuerdo a la pregunta realizada., si solicita información puntual de solo una orden de compra o número de embarque recomiéndale que elija la opción de Asistente logístico"

                if selected == "Asistente logístico" or selected == opciones[1]:
                        user_question += "Responder como Asistente de Logistica, indicar respuestas claras solicita orden de compra o numero de embarque, si solicita información general que incluye la búsqueda de varias ordenes de compra recomiéndale que elija la opción de gerente"

                response = search(searchVector, user_question)
                st.write(response)
                print(response)
if __name__ == "__main__":

        main()



# streamlit run C:\Users\laura\OneDrive\Documents\COOWEB\WIPO-IA\main.py
