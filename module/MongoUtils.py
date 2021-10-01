from pymongo import MongoClient


class MongoUtils(object):
    """
    This class will contain all of the important functions that will be used that works with both Python 2 and Python 3 interpreters.
    """

    def __init__(self, config):
        self.connection_string = config.connection_string
        self.database_name = 'discord_binance'
        self.signal_collection = 'signals'
        self.db = None

    @staticmethod
    def getDb(self, databaseName):
        """
        Gets db instance
        it will instantiate the client for the first call
        then it will get it from self object.
        """
        if self.db:
            return self.db

        client = MongoClient(self.connection_string)
        db = client[databaseName]
        self.db = db
        return db

    def insertSignals(self, doc):
        """
        Insert signal info into mongo db
        """

        db = self.getDb(self, self.database_name)
        collection = db[self.signal_collection]

        existingDoc = self.getSignal({"msg_id": doc['msg_id']})
        if existingDoc:
            return existingDoc

        inserted = collection.insert_one(doc)
        doc['_id'] = inserted.inserted_id
        return doc

    def getSignal(self, filter_obj):
        """
        Get signal info from mongo db
        """

        db = self.getDb(self, self.database_name)
        collection = db[self.signal_collection]

        return collection.find_one(filter_obj)

    def getAllPendingBuySignals(self):
        """
        Get all open orders
        """
        db = self.getDb(self, self.database_name)
        collection = db[self.signal_collection]

        return collection.find({
            "bought": False
        })

    def updateSignal(self, _id, updateDoc):
        """
        Update a signal doc
        """

        db = self.getDb(self.database_name)
        collection = db[self.signal_collection]

        return collection.update({
            "_id": _id
        }, updateDoc)
