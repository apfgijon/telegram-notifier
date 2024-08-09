from typing import Callable

class Listener():
    def listen(self, callback: Callable[[str], None]) -> None:
        pass