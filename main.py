import argparse
import threading

from api import FastAPIAPP
from config import Config
from listener import SocialMediaMessage
from listener.telegram import TelegramListener

import ollama

from model import SQLAlchemyDB, IDB

def parse_opts():
    parser = argparse.ArgumentParser(description="Telegram app for process diffusion groups")
    return parser.parse_args()

def callback(db: IDB):
    # I know its attached to telegram...
    def retfunc(message: SocialMediaMessage):
        message_entity = db.save_message(message)
        if message_entity:
            try:
                with open("./system_prompts.txt", "r", encoding='utf-8') as f:
                    
                    prompts = f.read().split("\n\n")
            except:
                import traceback
                traceback.print_exc()
            for prompt in prompts:
                response = ollama.chat(model='llama3.1', messages=[
                    {
                        'role': 'system',
                        'content': f""" {prompt} """,
                    },
                    {
                        'role': 'user',
                        'content': f"""{message.message_content}"""
                    },
                ])
                tag = str(response['message']['content'])
                db.save_message_tag(message_entity, tag.split(" ")[0])
        
    return retfunc

def run_fastapi(app: FastAPIAPP):
    app.run()
    
def bootstrap(opts):
    config = Config()
    db = SQLAlchemyDB()
    listener = TelegramListener(config, db)
    fastapi = FastAPIAPP(config, db)
    fastapi_thread = threading.Thread(target=run_fastapi, args=(fastapi,))
    fastapi_thread.start()
    listener.listen(callback(db))

if __name__ == "__main__":
    opts = parse_opts()
    bootstrap(opts)

