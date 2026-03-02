"""
Global Error Handler for FastAPI with Sentry Integration
Catches all unhandled exceptions and logs them to Sentry
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback

try:
    import sentry_sdk
    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False

async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler that catches all unhandled exceptions
    """
    
    # Log to Sentry if available
    if SENTRY_AVAILABLE:
        sentry_sdk.capture_exception(exc)
    
    # Log to console
    print(f"❌ Unhandled Exception: {type(exc).__name__}")
    print(f"   Path: {request.url.path}")
    print(f"   Error: {str(exc)}")
    print(f"   Traceback: {traceback.format_exc()}")
    
    # Return user-friendly error
    if request.url.path.startswith("/api/"):
        # API endpoints return JSON
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Our team has been notified.",
                "path": request.url.path
            }
        )
    else:
        # Web pages return HTML
        return HTMLResponse(
            content=f"""
            <html>
                <head>
                    <title>Error - MINORE BARBERSHOP</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            text-align: center;
                            padding: 50px;
                            background: #1d1a1c;
                            color: #fbcc93;
                        }}
                        .error-box {{
                            background: #2a2a2a;
                            padding: 2rem;
                            border-radius: 8px;
                            max-width: 500px;
                            margin: 0 auto;
                        }}
                        .btn {{
                            background: #fbcc93;
                            color: #1d1a1c;
                            padding: 0.75rem 1.5rem;
                            border-radius: 4px;
                            text-decoration: none;
                            display: inline-block;
                            margin-top: 1rem;
                        }}
                    </style>
                </head>
                <body>
                    <div class="error-box">
                        <h1>⚠️ Oops! Something went wrong</h1>
                        <p>We're sorry, but an unexpected error occurred.</p>
                        <p>Our team has been automatically notified and will fix this soon.</p>
                        <a href="/" class="btn">← Back to Home</a>
                    </div>
                </body>
            </html>
            """,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors (bad request data)
    """
    
    # Log validation errors to Sentry with lower severity
    if SENTRY_AVAILABLE:
        sentry_sdk.capture_message(
            f"Validation error: {exc.errors()}",
            level="warning"
        )
    
    print(f"⚠️ Validation Error: {exc.errors()}")
    
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation error",
                "details": exc.errors()
            }
        )
    else:
        return HTMLResponse(
            content=f"""
            <html>
                <head>
                    <title>Invalid Request - MINORE BARBERSHOP</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            text-align: center;
                            padding: 50px;
                            background: #1d1a1c;
                            color: #fbcc93;
                        }}
                    </style>
                </head>
                <body>
                    <h1>⚠️ Invalid Request</h1>
                    <p>The data you submitted is invalid. Please check and try again.</p>
                    <a href="javascript:history.back()">← Go Back</a>
                </body>
            </html>
            """,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions (404, 403, etc.)
    """
    
    # Only log 500 errors to Sentry
    if exc.status_code >= 500 and SENTRY_AVAILABLE:
        sentry_sdk.capture_exception(exc)
    
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code
            }
        )
    else:
        if exc.status_code == 404:
            return HTMLResponse(
                content=f"""
                <html>
                    <head>
                        <title>Page Not Found - MINORE BARBERSHOP</title>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                text-align: center;
                                padding: 50px;
                                background: #1d1a1c;
                                color: #fbcc93;
                            }}
                            .btn {{
                                background: #fbcc93;
                                color: #1d1a1c;
                                padding: 0.75rem 1.5rem;
                                border-radius: 4px;
                                text-decoration: none;
                                display: inline-block;
                                margin-top: 1rem;
                            }}
                        </style>
                    </head>
                    <body>
                        <h1>404 - Page Not Found</h1>
                        <p>The page you're looking for doesn't exist.</p>
                        <a href="/" class="btn">← Back to Home</a>
                    </body>
                </html>
                """,
                status_code=404
            )
        else:
            return HTMLResponse(
                content=f"""
                <html>
                    <head>
                        <title>Error {exc.status_code} - MINORE BARBERSHOP</title>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                text-align: center;
                                padding: 50px;
                                background: #1d1a1c;
                                color: #fbcc93;
                            }}
                        </style>
                    </head>
                    <body>
                        <h1>Error {exc.status_code}</h1>
                        <p>{exc.detail}</p>
                        <a href="/">← Back to Home</a>
                    </body>
                </html>
                """,
                status_code=exc.status_code
            )

def register_error_handlers(app):
    """
    Register all error handlers with the FastAPI app
    """
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    
    print("✅ Global error handlers registered")
