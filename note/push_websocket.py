import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

def created_category_note_send_notification(instance, user_id):
        async_to_sync(channel_layer.group_send)(
            f"{os.environ.get("CHANNEL_ROOM_GROUP")}_{user_id}",{
                "type": "send_notification_created_category",
                'notification': f"{str(instance)} category is created successfully."
            }
        )

def created_category_error_note_send_notification(error, user_id):
        async_to_sync(channel_layer.group_send)(
            f"{os.environ.get("CHANNEL_ROOM_GROUP")}_{user_id}",{
                "type": "send_notification_created_category_error",
                'notification': error
            }
        )