from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from magic_links.constants import MESSAGE_MAGIC_LINKS_SENT
from magic_links.serializers import (
    MagicLinkEmailSerializer, 
    MagicLinkTokenSerializer
)
from magic_links.services import (
    authenticate_token,
    send_magic_link,
)


class RequestMagicLink(APIView):

    parser_classes = (JSONParser, FormParser,)
    permission_classes = (AllowAny,)
    serializer_class = MagicLinkEmailSerializer
    
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:                
                send_magic_link(
                    email=serializer.validated_data['email'],
                    go_next=serializer.validated_data.get('next'),
                    request_source=serializer.validated_data.get('source')
                )
            except Exception as e:
                return Response({ 'error': str(e) }, status=status.HTTP_400_BAD_REQUEST)

            return Response({ 'detail': MESSAGE_MAGIC_LINKS_SENT }, status=status.HTTP_200_OK)

        else:
            return Response({ 'error': serializer.error_messages }, status=status.HTTP_400_BAD_REQUEST)


class AuthenticateToken(APIView):
    
    parser_classes = (JSONParser, FormParser,)
    permission_classes = (AllowAny,)
    serializer_class = MagicLinkTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            try:
                token = authenticate_token(
                    email=serializer.validated_data['email'], 
                    callback_token=serializer.validated_data['token']
                )
            except Exception as e:
                return Response({ 'error': str(e) }, status=status.HTTP_400_BAD_REQUEST)

            return Response({ 'token': token.key }, status=status.HTTP_200_OK)

        else:
            return Response({ 'error': serializer.error_messages }, status=status.HTTP_400_BAD_REQUEST)
