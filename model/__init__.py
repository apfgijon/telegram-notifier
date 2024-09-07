from sqlite3 import IntegrityError
from typing import Union
from sqlalchemy import Boolean, create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from listener import SocialMediaMessage
from sqlalchemy.orm import selectinload

class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    message_id = Column(Integer, unique=True)
    date = Column(DateTime)
    chat_id = Column(Integer, ForeignKey('channel.id'), unique=False)
    analysis = relationship("MessageTag", back_populates="message", uselist=True)
    channel = relationship("Channel", back_populates="messages", uselist=False)

class MessageTag(Base):
    __tablename__ = 'message_tag'

    id = Column(Integer, primary_key=True)
    typ = Column(String)
    tag = Column(String)
    message_id = Column(Integer, ForeignKey('message.id'))
    message = relationship("Message", back_populates="analysis")
    

class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    name = Column(String)
    img_id = Column(String, nullable=True)
    img = Column(String, nullable=True)
    selected = Column(Boolean, default=False)
    messages = relationship("Message", back_populates="channel")
    
    
class IDB():
    def save_message(self, new_message: SocialMediaMessage, chat_id:int) -> Union[Message, None]:
        pass
    def save_message_tag(self, message: Message, typ:str, tag:str):
        pass
    def save_channel(self, chat_id: int, name: str, photo_id: str = None):
        pass
    def img_channel(self, img_id: str, path: str):
        pass
    def get_channel_messages(self, chat_id: int):
        pass
    def get_channels(self):
        pass
    def get_messages(self):
        pass
    def get_channel_img_path(self, chat_id: int):
        pass
    def set_channel_selected(self, chat_id: int, selected: bool):
        pass
    def get_full_message(self, message_id: int):
        pass
        

class SQLAlchemyDB(IDB):
    
    def __init__(self):
        engine = create_engine('sqlite:///messages.db')
        
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def save_message_tag(self, message: Message, typ:str, tag:str):
        instance = MessageTag(
            message= message,
            typ= typ,
            tag= tag,
        )
        self.session.add(instance)
        self.session.commit()
    def save_message(self, new_message: SocialMediaMessage) -> Union[Message, None]:
        channel = self.session.query(Channel).filter_by(chat_id=new_message.chat_id).first()
        if channel:
            there_is_not_message = self.session.query(Message).filter_by(message_id=new_message.message_id).first() is None
            if there_is_not_message:
                message = Message(
                    message_id=new_message.message_id,
                    content=new_message.message_content,
                    channel=channel,
                    date=datetime.fromtimestamp(new_message.date),
                    )
                try:
                    self.session.add(message)
                    self.session.commit()
                    return message
                except:
                    pass
        return None
        
    def save_channel(self, chat_id: int, name: str, photo_id: str = None):
        instance = self.session.query(Channel).filter_by(chat_id=chat_id).first()
        if instance:
            instance.name = name
            if photo_id:
                instance.img_id = photo_id
        else:
            channel = Channel(
                chat_id=chat_id,
                name=name,
                )
            if photo_id: 
                channel.img_id = photo_id
            self.session.add(channel)
        
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def img_channel(self, img_id: str, path: str):
        instance = self.session.query(Channel).filter_by(img_id=img_id).first()
        if instance:
            instance.img = path
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()

    def get_channel_messages(self, chat_id: int):
        instance = self.session.query(Channel).filter_by(id=chat_id).first()
        return instance.messages

    def get_channels(self):
        instance = self.session.query(Channel).all()
        return list(map(lambda ch: Channel(
            id = ch.id,
            chat_id = ch.chat_id,
            name = ch.name,
            img_id = ch.img_id,
            img = ch.img.split("\\")[-1],
            selected = ch.selected
            ),instance))

    def get_messages(self):
        instance = self.session.query(Message).join(Channel) \
                .filter(Channel.selected == True).options(selectinload(Message.analysis), selectinload(Message.channel)).all()
        return instance
    
    def get_channel_img_path(self, chat_id: int):
        instance = self.session.query(Channel).filter_by(id=chat_id).first()
        return instance.img

    def set_channel_selected(self, chat_id: int, selected: bool):
        instance = self.session.query(Channel).filter_by(id=chat_id).first()
        if instance:
            instance.selected = selected
            self.session.commit()
    
    def get_full_message(self, message_id: int):
        instance = self.session.query(Message).join(Channel) \
                .filter(Message.id == message_id) \
                .options(selectinload(Message.analysis), selectinload(Message.channel)).first()
        return instance