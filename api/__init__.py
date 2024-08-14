from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import uvicorn
from starlette.status import HTTP_404_NOT_FOUND
from config import Iconfig
from model import IDB

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
        self.app.get("/api/get_channels")(self.get_channels)
        self.app.get("/api/get_messages")(self.get_messages)
        self.app.get("/api/get_channel_image/{channel_id}")(self.get_channel_image)
        self.app.post("/api/set_channel_select/{channel_id}")(self.set_channel_select)
    
    def run(self):
        uvicorn.run(self.app, host=self.config.getenv("HOST"), port=int(self.config.getenv("PORT")))

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