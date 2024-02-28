from rest_framework import serializers
from .models import Group, Message


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'group_member', 'newest_message_time']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'part_of_group', 'sender', 'message', 'created_at']