import argparse
import threading

from api import FastAPIAPP
from config import Config, Iconfig
from listener import SocialMediaMessage
from listener.telegram import TelegramListener

import ollama

from model import SQLAlchemyDB, IDB
from translator import translate
import asyncio

def parse_opts():
    parser = argparse.ArgumentParser(description="Telegram app for process diffusion groups")
    return parser.parse_args()

def callback(db: IDB, fastapi: FastAPIAPP, config: Iconfig):
    # I know its attached to telegram...
    def retfunc(message: SocialMediaMessage):
        message_entity = db.save_message(message)
        if message_entity:
            try:
                with open("./system_prompts.txt", "r", encoding='utf-8') as f:
                    prompts = []
                    for p in f.read().split("\n\n"):
                        lines = p.split("\n")
                        prompts.append(
                            {
                                "type": lines[0],
                                "prompt": "\n".join(lines[1:]),
                            }
                        )
                    
            except:
                import traceback
                traceback.print_exc()
            for prompt in prompts:
                response = ollama.chat(model='llama3.1', messages=[
                    {
                        'role': 'system',
                        'content': f""" {prompt["prompt"]} """,
                    },
                    {
                        'role': 'user',
                        'content': f"""{message.message_content}"""
                    },
                ])
                tag = str(response['message']['content'])
                db.save_message_tag(message_entity, prompt["type"], tag)
            
            translated_message = translate(message.message_content, config.getenv("LANGUAGE"))
            if translated_message:
                db.save_message_tag(message_entity, "TRANSLATE", translated_message)
            
            message_stored = db.get_full_message(message_entity.id)
            if message_stored.channel.selected:
                asyncio.run(fastapi.send_message_to_clients(message_stored))
        
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
    try:
        listener.listen(callback(db, fastapi, config))
    except KeyboardInterrupt:
        pass
    fastapi.stop()

if __name__ == "__main__":
    opts = parse_opts()
    bootstrap(opts)

