<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Multi-Lingual Product Catalog Translator - Copilot Instructions

## Project Overview
This is a Python-based web application that provides AI-powered translation services for e-commerce product catalogs using IndicTrans2 by AI4Bharat. The project consists of a FastAPI backend and a Streamlit frontend.

## Architecture
- **Backend**: FastAPI with IndicTrans2 integration, SQLite database
- **Frontend**: Streamlit web interface
- **ML Model**: IndicTrans2 by AI4Bharat for neural machine translation
- **Database**: SQLite for storing translations and corrections
- **Languages**: Supports 15+ Indian languages plus English

## Key Technologies
- **FastAPI**: High-performance web framework for the backend API
- **Streamlit**: Interactive web interface for users
- **IndicTrans2**: State-of-the-art neural machine translation for Indian languages
- **Pydantic**: Data validation and serialization
- **SQLite**: Lightweight database for development
- **PyTorch/Transformers**: For running the ML models

## Code Style and Conventions
- Follow PEP 8 Python style guidelines
- Use type hints throughout the codebase
- Include comprehensive docstrings for all functions and classes
- Use async/await for I/O operations in FastAPI
- Implement proper error handling and logging
- Use Pydantic models for request/response validation

## Project Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── models.py               # Pydantic data models
├── translation_service.py  # IndicTrans2 integration
├── database.py             # SQLite database operations
└── requirements.txt        # Backend dependencies

frontend/
├── app.py                  # Streamlit application
└── requirements.txt        # Frontend dependencies
```

## Development Guidelines

### Backend Development
- Use FastAPI dependency injection for database connections
- Implement proper HTTP status codes and error responses
- Use background tasks for long-running operations
- Add comprehensive logging for debugging
- Validate all inputs using Pydantic models
- Follow RESTful API design principles

### Frontend Development
- Use Streamlit's component system effectively
- Implement proper error handling for API calls
- Create responsive layouts using columns and containers
- Add loading states for better user experience
- Use caching where appropriate (@st.cache_data)
- Follow Streamlit best practices for session state management

### Database Operations
- Use connection pooling for database access
- Implement proper transaction handling
- Add database indexes for frequently queried columns
- Use parameterized queries to prevent SQL injection
- Implement database migration scripts for schema changes

### ML Integration
- Handle model loading and initialization properly
- Implement proper error handling for translation failures
- Add confidence scoring for translations
- Support batch processing for efficiency
- Implement proper memory management for large models

## Security Considerations
- Validate all user inputs
- Implement rate limiting for API endpoints
- Use proper CORS configuration
- Sanitize database inputs
- Log security-relevant events
- Use environment variables for sensitive configuration

## Testing
- Write unit tests for all business logic
- Add integration tests for API endpoints
- Test error conditions and edge cases
- Use pytest for testing framework
- Mock external dependencies in tests
- Test both success and failure scenarios

## Performance Optimization
- Use async operations for I/O bound tasks
- Implement proper caching strategies
- Optimize database queries
- Use connection pooling
- Implement proper pagination for large datasets
- Monitor memory usage with ML models

## API Design Patterns
- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Implement consistent error response formats
- Use appropriate HTTP status codes
- Version your APIs (/v1/, /v2/)
- Implement proper request/response logging
- Use OpenAPI/Swagger documentation

## Common Patterns in This Codebase
- Translation service uses async methods for model operations
- Database operations use context managers for connection handling
- API endpoints use dependency injection for database access
- Frontend makes HTTP requests to backend APIs
- Error handling uses try/except blocks with proper logging
- Configuration uses environment variables with defaults

## Debugging Tips
- Check FastAPI logs for backend issues
- Use Streamlit's error display for frontend debugging
- Monitor database locks and connection issues
- Check model loading and GPU memory usage
- Verify API endpoint accessibility and CORS settings
- Use FastAPI's interactive docs (/docs) for API testing

## Deployment Considerations
- Use proper environment variables for configuration
- Implement health check endpoints
- Use proper logging configuration for production
- Consider containerization with Docker
- Implement proper database backup strategies
- Monitor application performance and errors
