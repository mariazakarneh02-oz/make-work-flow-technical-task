from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.domain.exceptions.user import EmailAlreadyExistsError
from app.presentation.routes.user import router as user_router


app = FastAPI(
    title="Workflow API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)


@app.exception_handler(EmailAlreadyExistsError)
def handle_email_already_exists(
    request: Request,
    exc: EmailAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc),
        },
    )


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }