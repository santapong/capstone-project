import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from capstone.backend.api.router import (
    router_chatbot,
    router_dashboard,
    router_document,
)
from capstone.backend.config import settings
from capstone.backend.database.connection import init_db
from capstone.backend.logs.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize database
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    root_path=settings.API_PREFIX if settings.API_PREFIX != "/" else ""
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins from settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

@app.get("/", tags=["Default"])
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Default"])
async def health_check():
    return {"status": "ok", "version": settings.VERSION}

# Include routers
app.include_router(router_chatbot)
app.include_router(router_document)
app.include_router(router_dashboard)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)