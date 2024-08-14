import os
from dotenv import load_dotenv

load_dotenv()

class Iconfig():
    def getenv(self,env_variable:str):
        pass

class Config(Iconfig):

    possible_variables =[
        "API_HASH", 
        "APP_ID", 
        "TDJSON_LOCATION", 
        "WAITING_TIMEOUT", 
        "HOST", 
        "PORT", 
    ]
    def __init__(self) -> None:
        pass

    def getenv(self, env_variable: str):
        if env_variable not in self.possible_variables:
            return ""
        return os.getenv(env_variable)
