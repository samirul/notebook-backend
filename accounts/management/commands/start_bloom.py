import os
from django.core.management.base import BaseCommand
from accounts.bloom_filter import RedisBloomFilter

redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_db = os.environ.get('REDIS_DB')
redis_bloom_key = os.environ.get('REDIS_BLOOM_KEY')


class Command(BaseCommand):
    help = "Start the bloom filter"

    def handle(self, *args, **kwargs):
        try:
            RedisBloomFilter(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                key=redis_bloom_key
            )

            self.stdout.write(self.style.SUCCESS('Bloom filter started successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error starting bloom filter: {e}'))
