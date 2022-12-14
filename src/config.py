# type:ignore[assignment]
from pydantic import BaseSettings, Field


class Config(BaseSettings):
    ADMIN_ID:  int = ...
    ADMIN_UN: str = ...
    GROUP_ID: int = ...
    API_TOKEN: str = ...
    TECH_LINK: str = ...
    BONUS_LINK: str = ...
    POSTGRES_DB: str = ...
    POSTGRES_USER: str = ...
    POSTGRES_PASSWORD: str = ...
    DB_HOST: str = ...
    DB_PORT: int = ...
    REDIS_HOST: str = ...
    REDIS_PORT: int = ...
    REDIS_DB: int = ...
    postgres_dsl = {'dbname': POSTGRES_DB,
                    'user': POSTGRES_USER,
                    'password': POSTGRES_PASSWORD,
                    'host': DB_HOST,
                    'port': DB_PORT}
    class Config:
        case_sensitive = False
        env_file = ".env"


# class Config(BaseSettings):
#     ADMIN_ID:  int = ...
#     ADMIN_UN: str = ...
#     GROUP_ID: int = ...
#     API_TOKEN: str = ...
#     TECH_LINK: str = ...
#     BONUS_LINK: str = ...
#     DB_PATH: str = ...
#     link: str = Field('t.me/annapurna_mp_bot', env='link')
#
#     class Config:
#         case_sensitive = False


settings = Config()


# ['_conf', '_values', '__module__', '__annotations__', '__doc__', 'message_id', 'from_user', 'sender_chat', 'date',
#  'chat', 'forward_from', 'forward_from_chat', 'forward_from_message_id', 'forward_signature', 'forward_date',
#  'is_automatic_forward', 'reply_to_message', 'via_bot', 'edit_date', 'has_protected_content', 'media_group_id',
#  'author_signature', 'forward_sender_name', 'text', 'entities', 'caption_entities', 'audio', 'document', 'animation',
#  'game', 'photo', 'sticker', 'video', 'voice', 'video_note', 'caption', 'contact', 'location', 'venue', 'poll', 'dice',
#  'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
#  'supergroup_chat_created', 'channel_chat_created', 'message_auto_delete_timer_changed', 'migrate_to_chat_id',
#  'migrate_from_chat_id', 'pinned_message', 'invoice', 'successful_payment', 'connected_website', 'passport_data',
#  'proximity_alert_triggered', 'voice_chat_scheduled', 'voice_chat_started', 'voice_chat_ended',
#  'voice_chat_participants_invited', 'reply_markup', 'web_app_data', 'video_chat_scheduled', 'video_chat_started',
#  'video_chat_ended', 'video_chat_participants_invited', 'content_type', 'is_forward', 'is_command', 'get_full_command',
#  'get_command', 'get_args', 'parse_entities', 'from_id', 'md_text', 'html_text', 'url', 'link', 'answer',
#  'answer_photo', 'answer_audio', 'answer_animation', 'answer_document', 'answer_video', 'answer_voice',
#  'answer_video_note', 'answer_media_group', 'answer_location', 'answer_venue', 'answer_contact', 'answer_sticker',
#  'answer_poll', 'answer_dice', 'answer_chat_action', 'reply', 'reply_photo', 'reply_audio', 'reply_animation',
#  'reply_document', 'reply_video', 'reply_voice', 'reply_video_note', 'reply_media_group', 'reply_location',
#  'reply_venue', 'reply_contact', 'reply_poll', 'reply_sticker', 'reply_dice', 'forward', 'edit_text', 'edit_caption',
#  'edit_media', 'edit_reply_markup', 'delete_reply_markup', 'edit_live_location', 'stop_live_location', 'delete', 'pin',
#  'unpin', 'send_copy', 'copy_to', '__int__', '_ContextInstanceMixin__context_instance', '_props', '_aliases',
#  '__init__', 'conf', 'props', 'props_aliases', 'values', 'telegram_types', 'to_object', 'bot', 'to_python', 'clean',
#  'as_json', 'create', '__str__', '__repr__', '__getitem__', '__setitem__', '__contains__', '__iter__', 'iter_keys',
#  'iter_values', '__hash__', '__eq__', '__init_subclass__', 'get_current', 'set_current', '__dict__', '__weakref__',
#  '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__ne__', '__gt__', '__ge__', '__new__',
 # '__reduce_ex__', '__reduce__', '__subclasshook__', '__format__', '__sizeof__', '__dir__', '__class__']