import os
import redis
from rest_framework.exceptions import Throttled
from .rate_push_websocket  import send_rate_limit_error_note_send_notification

redis_client = redis.StrictRedis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    db=os.environ.get('REDIS_DB'),
    decode_responses=True
)


def rate_limiter(max_requests: int, time_window: int):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            client_id = request.user.id if request.user.is_authenticated else request.META.get('REMOTE_ADDR')
            endpoint = request.path
            redis_key = f"redis_key_rate_limit:{client_id}:{endpoint}"
            current_requests = redis_client.get(name=redis_key)

            if current_requests is None:
                redis_client.set(name=redis_key, value=1, ex=time_window)
            elif int(current_requests) < max_requests:
                redis_client.incr(name=redis_key)
            else:
                retry_after_as_timeout = redis_client.ttl(name=redis_key)
                send_rate_limit_error_note_send_notification(
                    instance=retry_after_as_timeout,
                    path=endpoint,
                    user_id=request.user.id
                )
                raise Throttled(detail=f"Max tries exceed, Try again after {retry_after_as_timeout} seconds.")
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator







