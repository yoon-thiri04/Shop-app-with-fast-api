import os
from dotenv import load_dotenv

load_dotenv()

class MongoConfig:
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME= os.getenv("MONGO_DB_NAME")