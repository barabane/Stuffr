from fastapi import HTTPException


class InvalidHTTPException(HTTPException):
    def __init__(self, status_code: int = None, detail='Ошибка на стороне сервера'):
        super().__init__(status_code=status_code if status_code else 500, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, status_code: int = None, detail='Вы не авторизованы'):
        super().__init__(status_code=status_code if status_code else 401, detail=detail)


class ConflictException(HTTPException):
    def __init__(self, status_code: int = None, detail='Conflict'):
        super().__init__(status_code=status_code if status_code else 409, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, status_code: int = None, detail='Bad request'):
        super().__init__(status_code=status_code if status_code else 402, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, status_code: int = None, detail='Not found'):
        super().__init__(status_code=status_code if status_code else 404, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, status_code: int = None, detail='Forbidden'):
        super().__init__(status_code=status_code if status_code else 403, detail=detail)


class TokenExpiredException(InvalidHTTPException):
    def __init__(self, detail='Время действия токена истекло'):
        super().__init__(detail=detail)


class GetTokenException(InvalidHTTPException):
    def __init__(self, detail='Ошибка при получении токена'):
        super().__init__(detail=detail)


class UserAlreadyExistsException(ConflictException):
    def __init__(self, detail='Пользователь с таким email уже существует'):
        super().__init__(detail=detail)


class UserDoesNotExistsException(NotFoundException):
    def __init__(self, detail='Пользователя с таким email не существует'):
        super().__init__(detail=detail)


class InvalidCredentialsException(BadRequestException):
    def __init__(self, detail='Неправильная почта или пароль'):
        super().__init__(detail=detail)


class UserForbiddenException(ForbiddenException):
    def __init__(self, detail='Недостаточно прав для использования'):
        super().__init__(detail=detail)


class PasswordsNotMatchException(BadRequestException):
    def __init__(self, detail='Пароли не совпадают'):
        super().__init__(detail=detail)


class ChangePasswordException(HTTPException):
    def __init__(self, status_code: int = None, detail='Ошибка при смене пароля'):
        super().__init__(status_code=status_code if status_code else 500, detail=detail)
