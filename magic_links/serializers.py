from rest_framework import serializers


class MagicLinkEmailSerializer(serializers.Serializer):
    email 	= serializers.EmailField()
    source 	= serializers.CharField(default='default')
    next 	= serializers.CharField(required=False)


class MagicLinkTokenSerializer(serializers.Serializer):
    email 	= serializers.EmailField()
    token 	= serializers.CharField()
