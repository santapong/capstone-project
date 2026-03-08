# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-03-08

### Added
- **Centralized Configuration**: Implemented `Pydantic Settings` in `capstone/backend/config.py` for unified environment variable management.
- **Enterprise-Grade Logging**: Standardized logging with configurable levels, paths, and formats.
- **Health Check Endpoint**: Added `/health` endpoint for monitoring application status.
- **Global Error Handling**: Standardized API error responses using a global exception handler in FastAPI.
- **Testing Infrastructure**: 
    - Integrated `pytest`, `pytest-asyncio`, and `httpx`.
    - Added comprehensive fixtures in `tests/conftest.py`.
    - Implemented unit tests for core API endpoints.
- **Code Quality**: Added `ruff.toml` for automated linting and formatting.
- **Structural Integrity**: Added `__init__.py` files across the backend to ensure valid Python packaging.

### Changed
- **Database Layer**: 
    - Refactored `connection.py` to use a singleton engine and standard SQLAlchemy session management.
    - Updated all API routers to use the standardized SQLAlchemy `Session` dependency.
- **API Client**: Centralized frontend API communication in `api_client.js` using Axios and environment-based configuration.
- **README Refactor**: Completely rewritten to reflect the new architecture and provide professional documentation.

### Security
- Removed hardcoded credentials and moved all sensitive parameters to environment variables with validation.
- Configured CORS middleware for cross-origin security.
