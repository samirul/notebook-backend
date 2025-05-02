from pybloom_live import BloomFilter
from django.contrib.auth import get_user_model

User = get_user_model()
bloom_filter = BloomFilter(capacity=10000000, error_rate=0.001)

def add_or_check_usernames_in_bloom_filter():
    for username in User.objects.values_list('username', flat=True):
        bloom_filter.add(username)