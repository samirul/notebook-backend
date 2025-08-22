import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
def send_rate_limit_error_note_send_notification(instance, path,  user_id):
        async_to_sync(channel_layer.group_send)(
            f"{os.environ.get("CHANNEL_ROOM_GROUP")}_{user_id}",{
                "type": "send_notification_rate_limited",
                'notification': f"Max tries exceed {path}, Try again after {str(instance)} seconds."
            }
        )