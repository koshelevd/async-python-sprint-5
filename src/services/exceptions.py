from fastapi import status


class BaseCustomException(Exception):
    """Base class for custom errors"""

    status = status.HTTP_400_BAD_REQUEST
    message = "Not set"
    description = "Bad Request"
    context = None


class BaseSimpleException(BaseCustomException):
    """Base class for simple errors"""

    def __init__(self, context: str | None = None, message: str | None = None):
        self._context = context
        if message:
            self.message = message

    @property
    def context(self):
        return self._context


class BaseFieldException(BaseCustomException):
    """
    Base class for errors related to object fields.
    The context_message attribute can use {field}
    for formatting the field name.
    """

    message = "An error occurred while processing the request body"
    context_message = "Error in fields: {field}"

    def __init__(
        self,
        fields: list,
        message: str | None = None,
        context_message: str | None = None,
    ):
        self.fields = fields
        if message:
            self.message = message
        if context_message:
            self.context_message = context_message

    @property
    def context(self) -> dict:
        return {
            field: self.context_message.format(field=field)
            for field in self.fields
        }


class UniqueValidationException(BaseFieldException):
    """Error caused by violation of unique constant of the object."""

    message = "Field uniqueness violated"
    context_message = "Object with {field} already exists"


class NotFoundValueException(BaseFieldException):
    """Error caused by the inability to find an object."""

    message = "Object not found"
    context_message = "Object not found with {field}"
    status = status.HTTP_404_NOT_FOUND
    description = "Not Found"


class InvalidValueException(BaseFieldException):
    """Error caused by the inability to find an object with field value."""

    status = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Invalid value"
    context_message = "Invalid value: {field}"


class BadRequestException(BaseSimpleException):
    """Bad request error."""

    message = "Bad Request"


class ObjectIsGoneException(BaseSimpleException):
    """Error caused by the deleted status of object."""

    status = status.HTTP_410_GONE
    message = "Object is gone"


class NotAuthorizedException(BaseSimpleException):
    """Not authorized error."""

    status = status.HTTP_401_UNAUTHORIZED
    message = "Not authorized"
