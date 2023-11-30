import pymongo
import os

MONGO_TIMEOUT= 1000
MONGODB = "test_database"
MONGOCOL = "registro_embarque"

try:
    cliente = pymongo.MongoClient(os.getenv('URLMONGO'), serverSelectionTimeOutMS= MONGO_TIMEOUT)
    cliente.server_info()
    
    print('la conexión fue exitosa')

    db = cliente.test_database
    database = cliente[MONGODB]
    collection = database[MONGOCOL]
    

    print(db.list_collection_names())
    database2 = cliente[MONGODB]
    registro_embarque = database2['registro_embarque']
    def insertOneDocument(document):
        try:
            db.collection.insert_one(document)
        except pymongo.errors.ConnectionFailure as error:
            print('Error para añadir información ', error)

    def insertManyDocuments(documents):
        try:
            db.prueba.insert_many(documents)                
        except pymongo.errors.ConnectionFailure as error:
            print('Error para añadir información', error)

except pymongo.errors.ConnectionFailure as error:
    print('Error conectar al servidor ', error)
