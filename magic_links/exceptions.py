

class MagicLinkException(Exception):
    def __str__(self):
        return '{e.__class__.__name__}: {e.__doc__}'.format(e=self)


class UserInactiveException(MagicLinkException):
    "User is not active."
    pass


class UserNotFoundException(MagicLinkException):
    "No user is associated with this email."
    pass


class BadRequestException(MagicLinkException):
    pass


class TokenAllocationException(MagicLinkException):
    "Could not allocate token."
    pass


class InvalidKeyException(MagicLinkException):
    "Invalid key provided."
    pass


class UnhandledException(MagicLinkException):
    pass
