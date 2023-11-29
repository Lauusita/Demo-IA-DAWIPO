import pymongo

MONGO_TIMEOUT= 1000
MONGO_URI= "mongodb+srv://laura_manolo:P0nedera@registromanolo.9xu303a.mongodb.net/"
MONGODB = "test_database"
MONGOCOL = "Registro_embarque"

try:
    cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeOutMS= MONGO_TIMEOUT)
    cliente.server_info()
    
    print('la conexión fue exitosa')

    db = cliente.test_database
    database = cliente[MONGODB]
    collection = database[MONGOCOL]
    
    print(database['Registro_embarque'])

    def insertOneDocument(document):
        try:
            db.collection.insert_one(document)
        except pymongo.errors.ConnectionFailure as error:
            print('Error para añadir información '+ error)

    def insertManyDocuments(documents):
        try:
            db.collection.insert_many(documents)                
        except pymongo.errors.ConnectionFailure as error:
            print('Error para añadir información' + error)

    

        
except pymongo.errors.ConnectionFailure as error:
    print('Error conectar al servidor '+ error)
