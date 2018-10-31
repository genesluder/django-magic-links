from rest_framework import serializers


class MagicLinkEmailSerializer(serializers.Serializer):

    email 	= serializers.EmailField()
    source 	= serializers.CharField()


class MagicLinkTokenSerializer(serializers.Serializer):

    email 	= serializers.EmailField()
    token 	= serializers.CharField()

