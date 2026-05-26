from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)

class AppException(Exception):
    def __init__(self, status_code: int, error_code: str, message: str, details: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details or {}

class CredentialsMismatchException(AppException):
    def __init__(self, message: str = "Invalid email or password.", details: dict = None):
        super().__init__(
            status_code=401,
            error_code="CREDENTIALS_MISMATCH",
            message=message,
            details=details
        )

class ResourceNotFoundException(AppException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
            message=message,
            details=details
        )

class CrisisAlertTriggered(AppException):
    def __init__(self, message: str = "Crisis trigger detected.", details: dict = None):
        super().__init__(
            status_code=403,
            error_code="CRISIS_ALERT",
            message=message,
            details=details
        )

class ValidationFailedException(AppException):
    def __init__(self, message: str = "Validation failed.", details: dict = None):
        super().__init__(
            status_code=422,
            error_code="VALIDATION_FAILED",
            message=message,
            details=details
        )

class ForbiddenException(AppException):
    def __init__(self, message: str = "Access forbidden.", details: dict = None):
        super().__init__(
            status_code=403,
            error_code="FORBIDDEN",
            message=message,
            details=details
        )

def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        details = {}
        for error in exc.errors():
            loc = " -> ".join([str(x) for x in error.get("loc", [])])
            details[loc] = error.get("msg", "Invalid value")
            
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error_code": "VALIDATION_FAILED",
                "message": "Input validation failed.",
                "details": details
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled server exception occurred")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred.",
                "details": {}
            }
        )
