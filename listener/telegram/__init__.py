from collections import namedtuple
from enum import Enum
import json
import sys
from ctypes import *
from typing import Callable
from config import Iconfig
from listener.telegram.types import TelegramMessage
from model import IDB
from .. import Listener, SocialMediaMessage


class EventReceiverCode(str, Enum):
    updateAuthorizationState = "updateAuthorizationState"
    updateNewMessage = "updateNewMessage"
    
    authorizationStateClosed = "authorizationStateClosed"
    authorizationStateWaitTdlibParameters = "authorizationStateWaitTdlibParameters"
    authorizationStateWaitPhoneNumber = "authorizationStateWaitPhoneNumber"
    authorizationStateWaitCode = "authorizationStateWaitCode"
    authorizationStateReady = "authorizationStateReady"
    
    foundChatMessages = "foundChatMessages"
    error = "error"
    chat = "chat"
    file = "file"
    updateNewChat = "updateNewChat"
    updateChatPosition = "updateChatPosition"
    updateChatAddedToList = "updateChatAddedToList"
    updateFile = "updateFile"

class EventSenderCode(str, Enum):
    setTdlibParameters = "setTdlibParameters"
    setAuthenticationPhoneNumber = "setAuthenticationPhoneNumber"
    authorizationStateWaitCode = "authorizationStateWaitCode"
    
    searchChatMessages = "searchChatMessages"
    checkAuthenticationCode = "checkAuthenticationCode"
    supergroupFullInfo = "supergroupFullInfo"
    getChat = "getChat"
    getChats = "getChats"
    getRemoteFile = "getRemoteFile"
    downloadFile = "downloadFile"

class TelegramListener(Listener):
    def __init__(self, config: Iconfig, database: IDB):
        self.database = database
        self.app_id = config.getenv("APP_ID")
        self.api_hash = config.getenv("API_HASH")
        self.waiting_timeout = config.getenv("WAITING_TIMEOUT")
        tdjson = CDLL(config.getenv("TDJSON_LOCATION"))
        _td_create_client_id = tdjson.td_create_client_id
        _td_create_client_id.restype = c_int
        _td_create_client_id.argtypes = []

        
        log_message_callback_type = CFUNCTYPE(None, c_int, c_char_p)

        _td_set_log_message_callback = tdjson.td_set_log_message_callback
        _td_set_log_message_callback.restype = None
        _td_set_log_message_callback.argtypes = [c_int, log_message_callback_type]
        

        self._td_receive = tdjson.td_receive
        self._td_receive.restype = c_char_p
        self._td_receive.argtypes = [c_double]

        self._td_send = tdjson.td_send
        self._td_send.restype = None
        self._td_send.argtypes = [c_int, c_char_p]

        self._td_execute = tdjson.td_execute
        self._td_execute.restype = c_char_p
        self._td_execute.argtypes = [c_char_p]
        
        log_message_callback_type = CFUNCTYPE(None, c_int, c_char_p)
        
        @log_message_callback_type
        def on_log_message_callback(verbosity_level, message):
            if verbosity_level == 0:
                sys.exit('TDLib fatal error: %r' % message)
                
        _td_set_log_message_callback(1, on_log_message_callback)
        
        self.client_id = _td_create_client_id()
        
        self.connected = False
        self.authenticated= False
        self.chat_id =  -1002192247697
        
    def __td_send(self, query):
        query = json.dumps(query).encode('utf-8')
        self._td_send(self.client_id, query)

    def __td_receive(self):
        result = self._td_receive(int(self.waiting_timeout))
        if result:
            result = json.loads(result.decode('utf-8'))
        return result

    def __td_execute(self, query):
        query = json.dumps(query).encode('utf-8')
        result = self._td_execute(query)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result
    
    def __authenticate(self) -> bool:
        print("Authenticating...")
        while not self.connected:
            event = self.__td_receive()
            if event:
                
                if event['@type'] == EventReceiverCode.updateAuthorizationState:
                    auth_state = event['authorization_state']

                    # if client is closed, we need to destroy it and create new client
                    if auth_state['@type'] == EventReceiverCode.authorizationStateClosed:
                        self.connected = False
                        return False
                    
                    if auth_state['@type'] == EventReceiverCode.authorizationStateWaitTdlibParameters:
                        self.__td_send({'@type': EventSenderCode.setTdlibParameters,
                                'database_directory': 'tdlib',
                                'use_message_database': True,
                                'use_secret_chats': True,
                                'api_id': self.app_id,
                                'api_hash': self.api_hash,
                                'system_language_code': 'en',
                                'device_model': 'Desktop',
                                'application_version': '1.0'})
                    if auth_state['@type'] == EventReceiverCode.authorizationStateWaitPhoneNumber:
                        phone_number = input('Please enter your phone number: ')
                        self.__td_send({'@type': EventSenderCode.setAuthenticationPhoneNumber, 'phone_number': phone_number})
                    
                    if auth_state['@type'] == EventReceiverCode.authorizationStateWaitCode:
                        code = input('Please enter the authentication code you received: ')
                        self.__td_send({'@type': EventSenderCode.checkAuthenticationCode, 'code': code})
                    
                    if auth_state['@type'] == EventReceiverCode.authorizationStateReady:
                    
                        self.connected = True
        return self.connected                        

    def __listen_notification(self, callback: Callable[[SocialMediaMessage], None]):
        print("Ready!")
        while self.connected:
            event = self.__td_receive()
            if event:
                if event['@type'] == EventReceiverCode.updateNewMessage:                    
                    try:
                        message = TelegramMessage(event["message"])
                        
                        callback(SocialMediaMessage(
                                chat_id=message.chat_id,
                                message_id=message.id,
                                message_content=message.content.text.text,
                                date=message.date,
                            ))
                    except:
                        pass
                elif event["@type"] == EventReceiverCode.foundChatMessages:
                    
                    for message in event["messages"]:
                        try:
                            message = TelegramMessage(message)
                            callback(SocialMediaMessage(
                                chat_id=message.chat_id,
                                message_id=message.id,
                                message_content=message.content.text.text,
                                date=message.date,
                            ))
                        except Exception as e:
                            pass
                elif event["@type"] == EventReceiverCode.error:
                    print(f"ERROR: {event}")
                elif event["@type"] == EventReceiverCode.chat:
                    photo = None
                    try:
                        photo= event["photo"]["big"]["remote"]["id"]
                    except:
                        pass
                    
                    self.database.save_channel(event["id"], event["title"], photo)
                    self.__td_send({'@type': EventSenderCode.searchChatMessages, 
                                    'chat_id': event["id"],
                                    'query': "",
                                    'from_message_id': 0,
                                    'offset': 0,
                                    'limit': 20,
                                    })
                        
                    if photo:
                        self.__td_send({'@type': EventSenderCode.getRemoteFile, "remote_file_id": event["photo"]["big"]["remote"]["id"]})
                elif event["@type"] == EventReceiverCode.updateFile:
                    self.database.img_channel(event["file"]["remote"]["id"], event["file"]["local"]["path"])
                    pass
                elif event["@type"] == EventReceiverCode.updateChatPosition:
                    if (event["chat_id"] < 0):
                        self.__td_send({'@type': EventSenderCode.getChat, "chat_id": event["chat_id"]})
                elif event["@type"] == EventReceiverCode.file:
                    self.__td_send({
                        '@type': EventSenderCode.downloadFile, 
                        "file_id": event["id"],
                        "priority": 1,
                        "offset": 0,
                        "limit": 0,
                        "synchronous": True,
                    })
          
                        
    def __init_communication(self):
        self.__td_execute({'@type': 'setLogVerbosityLevel', 'new_verbosity_level': 0, '@extra': 1.01234})
        self.__td_send({'@type': 'getOption', 'name': 'version', '@extra': 1.01234})

    def __receive_base_data(self):
        self.__td_send({'@type': EventSenderCode.getChats, 'limit': 100})
        
    def listen(self, callback: Callable[[str], None]) -> None:

        self.__init_communication()
        if not self.__authenticate():
            return
        
        self.__receive_base_data()

        if not self.__listen_notification(callback):
            return
        else:
            self.listen(callback)
            
            
            
