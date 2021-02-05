import pytz
from datetime import datetime
from simple_settings import settings
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import AutoReconnect, PyMongoError
from utilities.logger import Logger

logger = Logger().get_logger()


class MongoUtil(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoUtil, cls).__new__(cls)
            cls.mongo_client = MongoUtil.create_mongo_connection()
        return cls._instance

    @staticmethod
    def create_mongo_connection():
        host = settings.MONGO_HOST
        port = settings.MONGO_PORT
        username = settings.MONGO_USERNAME
        password = settings.MONGO_PASSWORD
        authsource = settings.MONGO_DEFAULT_DATABASE
        try:
            if password:
                mongo_client = MongoClient(host=host, port=port,
                                           username=username,
                                           password=password,
                                           authSource=authsource
                                           )
            else:
                # for local testing
                mongo_client = MongoClient(host=host, port=port)
            # to check mongo connection.
            mongo_client.server_info()
            logger.info("Mongo connection established")
        except (AutoReconnect, PyMongoError) as e:
            logger.error(f"Error connecting to Mongo {e}")
            raise e
        return mongo_client

    def get_mongo_client(self):
        return self.mongo_client

    def get_collection(self, collection_name, database=settings.MONGO_DEFAULT_DATABASE):
        '''
        :param collection_name: collection name
        :param database: database name
        :return: Collection object of the specified collection name.
        '''
        try:
            mongo_client = self.get_mongo_client()
            database_instance = Database(mongo_client, database)
            collection = Collection(database=database_instance, name=collection_name)
            return collection
        except (PyMongoError, Exception) as e:
            logger.error(f"Error connecting to collection {collection_name}  error = {e}")
            raise e

    def upsert_query_results(self, user, query):

        try:
            user_collection = MongoUtil().get_collection(collection_name=settings.USER_DATA_COLLECTION)
            timezone = pytz.timezone('Asia/Calcutta')

            updated_documents = user_collection.update_many(
                filter={"user": user, "query": query},
                update={'$set': {"user": user, "query": query, "last_updated_time": datetime.now(timezone)}},
                upsert=True)
            logger.info(
                f"updated result acknowledged = {updated_documents.acknowledged} "
                f"matched_count = {updated_documents.matched_count} "
                f"updated_count = {updated_documents.modified_count}")
        except Exception as e:
            logger.exception(f"Error in upserting data in Mongo for user = {user}  error = {str(e)}")
            raise e

    def fetch_recent_result(self, user, query):
        '''
        :param user: user for which recent result are being fetched
        :param query: query string for recent searches
        :return: keywords for recent searches matching query.
        '''
        try:
            user_collection = MongoUtil().get_collection(collection_name=settings.USER_DATA_COLLECTION)
            results = list(user_collection.find(filter={"query": {'$regex': query, '$options': 'i'}}))
            keywords = "\n".join(list(map(lambda x: x.get("query"), results)))
            return keywords
        except Exception as e:
            logger.exception(f"Error in fetching data in Mongo for user = {user}  error = {str(e)}")
            raise e
