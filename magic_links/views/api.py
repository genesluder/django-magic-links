from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from magic_links.constants import (
    MESSAGE_USER_INACTIVE,
    MESSAGE_USER_NOT_FOUND,
    MESSAGE_EMAIL_REQUIRED,
    MESSAGE_MAGIC_LINKS_SENT,
    MESSAGE_UNKNOWN_ERROR,
    MESSAGE_TOKEN_ALLOCATION_FAILED,
    MESSAGE_INVALID_KEY,
)
from magic_links.settings import api_settings
from magic_links.serializers import (
    MagicLinkEmailSerializer, 
    MagicLinkTokenSerializer
)
from magic_links.services import send_magic_link
from magic_links.utils import (
    authenticate_user, 
    get_user_for_email, 
    validate_credential,
)


class RequestMagicLink(APIView):

    permission_classes = (AllowAny,)
    serializer_class = MagicLinkEmailSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():

            email = serializer.validated_data['email']
            request_source = serializer.validated_data['source']

            user = get_user_for_email(email)

            if user:
                if not user.is_active:
                    return Response({ 'detail': MESSAGE_USER_INACTIVE }, status=status.HTTP_400_BAD_REQUEST)

                success = send_magic_link(user, request_source)

                if success:
                    status_code = status.HTTP_200_OK
                    message = MESSAGE_MAGIC_LINKS_SENT
                else:
                    status_code = status.HTTP_400_BAD_REQUEST
                    message = MESSAGE_UNKNOWN_ERROR

                return Response({ 'detail': message }, status=status_code)

            else:
                return Response({ 'detail': MESSAGE_USER_NOT_FOUND }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({ 'error': serializer.error_messages }, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenFromMagicLinkToken(APIView):
    
    permission_classes = (AllowAny,)
    serializer_class = MagicLinkTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data['email']
            callback_token = serializer.validated_data['token']

            credential = validate_credential(email, callback_token)

            if credential:

                user = credential.user

                if not user.is_active:
                    return Response({ 'detail': MESSAGE_USER_INACTIVE }, status=status.HTTP_400_BAD_REQUEST)

                token = authenticate_user(user)

                if token:
                    return Response({ 'token': token.key }, status=status.HTTP_200_OK)
                else:
                    return Response({ 'detail': MESSAGE_TOKEN_ALLOCATION_FAILED }, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({ 'detail': MESSAGE_INVALID_KEY }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({ 'error': serializer.error_messages }, status=status.HTTP_400_BAD_REQUEST)

        return Response({ 'detail': MESSAGE_UNKNOWN_ERROR }, status=status.HTTP_400_BAD_REQUEST)

