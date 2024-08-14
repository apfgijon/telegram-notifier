from typing import Callable
from dataclasses import dataclass

@dataclass
class SocialMediaMessage():
    chat_id: int
    message_id: int
    message_content: str
    date: int
    

class Listener():
    def listen(self, callback: Callable[[SocialMediaMessage], None]) -> None:
        pass