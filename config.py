import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't35T!K3y53CR3T??'
