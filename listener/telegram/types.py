from enum import Enum
from typing import List, Any, Optional

from utils.convert import DictToObject


class AuthorSignature(str, Enum):
    JUAN_HERNÁNDEZ = "Juan Hernández"


class CaptionType(str, Enum):
    FORMATTED_TEXT = "formattedText"


class Caption:
    type: CaptionType
    text: str
    entities: List[Any]

    def __init__(self, type: CaptionType, text: str, entities: List[Any]) -> None:
        self.type = type
        self.text = text
        self.entities = entities


class Minithumbnail:
    type: str
    width: int
    height: int
    data: str

    def __init__(self, type: str, width: int, height: int, data: str) -> None:
        self.type = type
        self.width = width
        self.height = height
        self.data = data


class LocalType(str, Enum):
    LOCAL_FILE = "localFile"


class Local:
    type: LocalType
    path: str
    can_be_downloaded: bool
    can_be_deleted: bool
    is_downloading_active: bool
    is_downloading_completed: bool
    download_offset: int
    downloaded_prefix_size: int
    downloaded_size: int

    def __init__(self, type: LocalType, path: str, can_be_downloaded: bool, can_be_deleted: bool, is_downloading_active: bool, is_downloading_completed: bool, download_offset: int, downloaded_prefix_size: int, downloaded_size: int) -> None:
        self.type = type
        self.path = path
        self.can_be_downloaded = can_be_downloaded
        self.can_be_deleted = can_be_deleted
        self.is_downloading_active = is_downloading_active
        self.is_downloading_completed = is_downloading_completed
        self.download_offset = download_offset
        self.downloaded_prefix_size = downloaded_prefix_size
        self.downloaded_size = downloaded_size


class RemoteType(str, Enum):
    REMOTE_FILE = "remoteFile"


class Remote:
    type: RemoteType
    id: str
    unique_id: str
    is_uploading_active: bool
    is_uploading_completed: bool
    uploaded_size: int

    def __init__(self, type: RemoteType, id: str, unique_id: str, is_uploading_active: bool, is_uploading_completed: bool, uploaded_size: int) -> None:
        self.type = type
        self.id = id
        self.unique_id = unique_id
        self.is_uploading_active = is_uploading_active
        self.is_uploading_completed = is_uploading_completed
        self.uploaded_size = uploaded_size


class VideoType(str, Enum):
    FILE = "file"


class FileClass:
    type: VideoType
    id: int
    size: int
    expected_size: int
    local: Local
    remote: Remote

    def __init__(self, type: VideoType, id: int, size: int, expected_size: int, local: Local, remote: Remote) -> None:
        self.type = type
        self.id = id
        self.size = size
        self.expected_size = expected_size
        self.local = local
        self.remote = remote


class TypeEnum(str, Enum):
    M = "m"
    X = "x"
    Y = "y"


class SizeType(str, Enum):
    PHOTO_SIZE = "photoSize"


class Size:
    type: SizeType
    size_type: TypeEnum
    photo: FileClass
    width: int
    height: int
    progressive_sizes: List[int]

    def __init__(self, type: SizeType, size_type: TypeEnum, photo: FileClass, width: int, height: int, progressive_sizes: List[int]) -> None:
        self.type = type
        self.size_type = size_type
        self.photo = photo
        self.width = width
        self.height = height
        self.progressive_sizes = progressive_sizes


class Photo:
    type: str
    has_stickers: bool
    minithumbnail: Minithumbnail
    sizes: List[Size]

    def __init__(self, type: str, has_stickers: bool, minithumbnail: Minithumbnail, sizes: List[Size]) -> None:
        self.type = type
        self.has_stickers = has_stickers
        self.minithumbnail = minithumbnail
        self.sizes = sizes


class ContentType(str, Enum):
    MESSAGE_PHOTO = "messagePhoto"
    MESSAGE_TEXT = "messageText"
    MESSAGE_VIDEO = "messageVideo"


class Format:
    type: str

    def __init__(self, type: str) -> None:
        self.type = type


class Thumbnail:
    type: str
    format: Format
    width: int
    height: int
    file: FileClass

    def __init__(self, type: str, format: Format, width: int, height: int, file: FileClass) -> None:
        self.type = type
        self.format = format
        self.width = width
        self.height = height
        self.file = file


class ContentVideo:
    type: str
    duration: int
    width: int
    height: int
    file_name: str
    mime_type: str
    has_stickers: bool
    supports_streaming: bool
    minithumbnail: Minithumbnail
    thumbnail: Thumbnail
    video: FileClass

    def __init__(self, type: str, duration: int, width: int, height: int, file_name: str, mime_type: str, has_stickers: bool, supports_streaming: bool, minithumbnail: Minithumbnail, thumbnail: Thumbnail, video: FileClass) -> None:
        self.type = type
        self.duration = duration
        self.width = width
        self.height = height
        self.file_name = file_name
        self.mime_type = mime_type
        self.has_stickers = has_stickers
        self.supports_streaming = supports_streaming
        self.minithumbnail = minithumbnail
        self.thumbnail = thumbnail
        self.video = video


class Content:
    type: ContentType
    text: Optional[Caption]
    video: Optional[ContentVideo]
    caption: Optional[Caption]
    show_caption_above_media: Optional[bool]
    has_spoiler: Optional[bool]
    is_secret: Optional[bool]
    photo: Optional[Photo]

    def __init__(self, type: ContentType, text: Optional[Caption], video: Optional[ContentVideo], caption: Optional[Caption], show_caption_above_media: Optional[bool], has_spoiler: Optional[bool], is_secret: Optional[bool], photo: Optional[Photo]) -> None:
        self.type = type
        self.text = text
        self.video = video
        self.caption = caption
        self.show_caption_above_media = show_caption_above_media
        self.has_spoiler = has_spoiler
        self.is_secret = is_secret
        self.photo = photo


class TypeType(str, Enum):
    REACTION_TYPE_EMOJI = "reactionTypeEmoji"


class TypeClass:
    type: TypeType
    emoji: str

    def __init__(self, type: TypeType, emoji: str) -> None:
        self.type = type
        self.emoji = emoji


class ReactionType(str, Enum):
    MESSAGE_REACTION = "messageReaction"


class Reaction:
    type: ReactionType
    reaction_type: TypeClass
    total_count: int
    is_chosen: bool
    recent_sender_ids: List[Any]

    def __init__(self, type: ReactionType, reaction_type: TypeClass, total_count: int, is_chosen: bool, recent_sender_ids: List[Any]) -> None:
        self.type = type
        self.reaction_type = reaction_type
        self.total_count = total_count
        self.is_chosen = is_chosen
        self.recent_sender_ids = recent_sender_ids


class ReactionsType(str, Enum):
    MESSAGE_REACTIONS = "messageReactions"


class Reactions:
    type: ReactionsType
    reactions: List[Reaction]
    are_tags: bool

    def __init__(self, type: ReactionsType, reactions: List[Reaction], are_tags: bool) -> None:
        self.type = type
        self.reactions = reactions
        self.are_tags = are_tags


class RecentReplierIDType(str, Enum):
    MESSAGE_SENDER_USER = "messageSenderUser"


class RecentReplierID:
    type: RecentReplierIDType
    user_id: int

    def __init__(self, type: RecentReplierIDType, user_id: int) -> None:
        self.type = type
        self.user_id = user_id


class ReplyInfoType(str, Enum):
    MESSAGE_REPLY_INFO = "messageReplyInfo"


class ReplyInfo:
    type: ReplyInfoType
    reply_count: int
    recent_replier_ids: List[RecentReplierID]
    last_read_inbox_message_id: int
    last_read_outbox_message_id: int
    last_message_id: int

    def __init__(self, type: ReplyInfoType, reply_count: int, recent_replier_ids: List[RecentReplierID], last_read_inbox_message_id: int, last_read_outbox_message_id: int, last_message_id: int) -> None:
        self.type = type
        self.reply_count = reply_count
        self.recent_replier_ids = recent_replier_ids
        self.last_read_inbox_message_id = last_read_inbox_message_id
        self.last_read_outbox_message_id = last_read_outbox_message_id
        self.last_message_id = last_message_id


class InteractionInfoType(str, Enum):
    MESSAGE_INTERACTION_INFO = "messageInteractionInfo"


class InteractionInfo:
    type: InteractionInfoType
    view_count: int
    forward_count: int
    reply_info: Optional[ReplyInfo]
    reactions: Optional[Reactions]

    def __init__(self, type: InteractionInfoType, view_count: int, forward_count: int, reply_info: Optional[ReplyInfo], reactions: Optional[Reactions]) -> None:
        self.type = type
        self.view_count = view_count
        self.forward_count = forward_count
        self.reply_info = reply_info
        self.reactions = reactions


class ReplyTo:
    type: str
    chat_id: int
    message_id: int
    origin_send_date: int

    def __init__(self, type: str, chat_id: int, message_id: int, origin_send_date: int) -> None:
        self.type = type
        self.chat_id = chat_id
        self.message_id = message_id
        self.origin_send_date = origin_send_date


class SenderIDType(str, Enum):
    MESSAGE_SENDER_CHAT = "messageSenderChat"


class SenderID:
    type: SenderIDType
    chat_id: int

    def __init__(self, type: SenderIDType, chat_id: int) -> None:
        self.type = type
        self.chat_id = chat_id


class MessageType(str, Enum):
    MESSAGE = "message"


class Message:
    type: MessageType
    id: int
    sender_id: SenderID
    chat_id: int
    is_outgoing: bool
    is_pinned: bool
    is_from_offline: bool
    can_be_saved: bool
    has_timestamped_media: bool
    is_channel_post: bool
    is_topic_message: bool
    contains_unread_mention: bool
    date: int
    edit_date: int
    interaction_info: InteractionInfo
    unread_reactions: List[Any]
    message_thread_id: int
    saved_messages_topic_id: int
    self_destruct_in: float
    auto_delete_in: float
    via_bot_user_id: int
    sender_business_bot_user_id: int
    sender_boost_count: int
    author_signature: AuthorSignature
    media_album_id: str
    effect_id: int
    restriction_reason: str
    content: Content
    reply_to: Optional[ReplyTo]

    # def __init__(self, type: MessageType, id: int, sender_id: SenderID, chat_id: int, is_outgoing: bool, is_pinned: bool, is_from_offline: bool, can_be_saved: bool, has_timestamped_media: bool, is_channel_post: bool, is_topic_message: bool, contains_unread_mention: bool, date: int, edit_date: int, interaction_info: InteractionInfo, unread_reactions: List[Any], message_thread_id: int, saved_messages_topic_id: int, self_destruct_in: float, auto_delete_in: float, via_bot_user_id: int, sender_business_bot_user_id: int, sender_boost_count: int, author_signature: AuthorSignature, media_album_id: str, effect_id: int, restriction_reason: str, content: Content, reply_to: Optional[ReplyTo]) -> None:
    #     self.type = type
    #     self.id = id
    #     self.sender_id = sender_id
    #     self.chat_id = chat_id
    #     self.is_outgoing = is_outgoing
    #     self.is_pinned = is_pinned
    #     self.is_from_offline = is_from_offline
    #     self.can_be_saved = can_be_saved
    #     self.has_timestamped_media = has_timestamped_media
    #     self.is_channel_post = is_channel_post
    #     self.is_topic_message = is_topic_message
    #     self.contains_unread_mention = contains_unread_mention
    #     self.date = date
    #     self.edit_date = edit_date
    #     self.interaction_info = interaction_info
    #     self.unread_reactions = unread_reactions
    #     self.message_thread_id = message_thread_id
    #     self.saved_messages_topic_id = saved_messages_topic_id
    #     self.self_destruct_in = self_destruct_in
    #     self.auto_delete_in = auto_delete_in
    #     self.via_bot_user_id = via_bot_user_id
    #     self.sender_business_bot_user_id = sender_business_bot_user_id
    #     self.sender_boost_count = sender_boost_count
    #     self.author_signature = author_signature
    #     self.media_album_id = media_album_id
    #     self.effect_id = effect_id
    #     self.restriction_reason = restriction_reason
    #     self.content = content
    #     self.reply_to = reply_to

class TelegramMessage(DictToObject, Message):
    pass