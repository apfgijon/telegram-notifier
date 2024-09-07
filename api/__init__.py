import threading
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import FileResponse
import uvicorn
from starlette.status import HTTP_404_NOT_FOUND
from config import Iconfig
from model import IDB

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class MessageTagSchema(BaseModel):
    id: int
    typ: str
    tag: str

    class Config:
        from_attributes = True

class ChannelSchema(BaseModel):
    id: int
    chat_id: int
    name: str
    img_id: Optional[str]
    img: Optional[str]
    selected: bool

    class Config:
        from_attributes = True

class MessageSchema(BaseModel):
    id: int
    content: str
    message_id: int
    date: datetime
    chat_id: int
    analysis: List[MessageTagSchema]
    channel: ChannelSchema

    class Config:
        from_attributes = True


class SetChannelSelect(BaseModel):
    selected: bool
    
class FastAPIAPP:
    
    def __init__(self, config: Iconfig, db: IDB):
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )
        self.db = db
        self.config = config
        self.config = config
        self.active_connections = set()
        self.app.get("/api/get_channels")(self.get_channels)
        self.app.get("/api/get_messages")(self.get_messages)
        self.app.get("/api/get_channel_image/{channel_id}")(self.get_channel_image)
        self.app.post("/api/set_channel_select/{channel_id}")(self.set_channel_select)
        self.app.websocket("/updates")(self.updates)
        self.should_exit = threading.Event()
        self.server = None
    
    def run(self):
        config = uvicorn.Config(self.app, host=self.config.getenv("HOST"), port=int(self.config.getenv("PORT")))
        self.server = uvicorn.Server(config)
        self.server.run()

    def stop(self):
        if self.server:
            self.should_exit.set()
            self.server.should_exit = True

    async def get_channels(self):
        try:
            channels = self.db.get_channels()
            return channels
        except:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Image not found")

    async def get_messages(self):
        try:
            messages = self.db.get_messages()
            return messages
        except:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Image not found")

    async def get_channel_image(self, channel_id: int):
        try:
            img_path = self.db.get_channel_img_path(channel_id)
            return FileResponse(img_path)
        except:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Image not found")

    async def set_channel_select(self, channel_id: int, channelSelect: SetChannelSelect):
        try:
            self.db.set_channel_selected(channel_id, channelSelect.selected)
            return {"status": "ok"}
        except:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Couldnt find channel")
        
    async def updates(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        try:
            while True:
                # Keep the connection alive
                await websocket.receive_text()
        except Exception:
            self.active_connections.remove(websocket)

    async def send_message(self, message):
        message_data = MessageSchema.model_validate(message)
        json_compatible_item_data = jsonable_encoder(message_data)
        for connection in self.active_connections:
            await connection.send_json(json_compatible_item_data)
    
    async def send_message_to_clients(self, message):
        try:
            if message:
                await self.send_message(message)
                return {"status": "Message sent"}
            return {"status": "Message not found"}
        except:
            import traceback
            traceback.print_exc()
