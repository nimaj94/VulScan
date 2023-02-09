import redis
from rest_framework import serializers

from scanner.models import Website


class ScanSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(required=True, allow_blank=False, max_length=255)

    class Meta:
        model = Website
        fields = ['id', 'domain', 'created_at', 'status']

    def create(self, validated_data):
        website = Website.objects.create(**validated_data)
        redis_con = redis.Redis(host='localhost', port=6379, db=0)
        redis_con.rpush("websites", website.domain)
        return website
