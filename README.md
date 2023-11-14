
# Langchain Chat-CSV with OpenAI and Pinecone
--

## How it works
This python application reads CSVs documents using an agentExecutor and processes the data, then converts the acquired data to String and split the data into chunks, with the purpose of sending it to a vector database (Pinecone) to make easier the search of information or data using OpenAI LLMs alongside with Langchain Agents in order to answer any questions. 

## Required packages
1. First of all, make sure you have Python and pip previously installed on your system before run the next steps. Additionally, it's neccesary to obtain an OPENAI API Key, Pinecone API key and its respective enviroment. Put those API keys on a `.env` file. Ensure that you won't make them public
2. To install de required packages use the following command: 
``` 
pip install langchain langchain-experimental pinecone streamlit python-dotenv
```


## Usage
To run the application, execture the `main.py` file using streamlit.
```
streamlit run main.py
```
if you are running the application in a different path, execute the path where is located the `main.py`:
``` 
streamlit run /your/path/main.py 
```
