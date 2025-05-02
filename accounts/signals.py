from django.core.signals import request_started
from django.dispatch import receiver
from .bloom_filter import add_or_check_usernames_in_bloom_filter

_loaded = False
@receiver(request_started)
def load_bloom_filter_once(sender, **kwargs):
    global _loaded
    if not _loaded:
        add_or_check_usernames_in_bloom_filter()
        _loaded = True