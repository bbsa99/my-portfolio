# JWT Authentication & Security
## Authentication Flow
### Successful Response
### Token Types
## Security Middleware
### JWT Authentication Middleware (Code Snippet)
### Rate Limiting Middleware
### Rate Limiting Middleware (Code Snippet)
### CORS Configuration
## Password Security
## Security Headers
## OpenTelemetry Security
## Environment Security
## Compliance

### Security Standards

- **OWASP Top 10**: Addressed through input validation, parameterized queries, and security headers
- **GDPR**: User data is pseudonymized, right to be implemented via audit log
- **PCI DSS**: Payment data is not stored; only order references are kept
- **ISO 27001**: Security policies documented and implemented through middleware

### Testing Security

```bash
# Run security-related tests
python -m pytest cloudforge/api_gateway/tests/ -v -k "auth or security"

# Test authentication bypass attempts
# Test rate limiting enforcement
# Test JWT token validation edge cases
# Test CORS configuration
# Test password hashing verification
```

### Security Headers Test

```python
def test_security_headers(client):
    response = client.get("/api/v1/health")
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "Strict-Transport-Security" in response.headers
```

### .env Best Practices

```env
# ❌ Don't commit these to version control
JWT_SECRET_KEY=super-secret-value
POSTGRES_PASSWORD=password123
REDIS_PASSWORD=password123

# ✅ Use environment variables or AWS Parameter Store
JWT_SECRET_KEY=${JWT_SECRET_KEY}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
REDIS_PASSWORD=${REDIS_PASSWORD}
```

### .gitignore

```gitignore
# Environment files
.env
.env.example (remove sensitive values or use placeholder)

# Local development
.DS_Store
*.log
```

### Trace Context Propagation

- Headers are propagated across service boundaries
- **x-b3-traceid**: W3C Trace Context
- **x-b3-spanid**: W3C Span Context
- **x-otp-traceid**: OpenTelemetry Trace ID

### Security Considerations

- Never log sensitive data in trace attributes
- Mask PII (Personally Identifiable Information) in logs
- Use secure headers for OTLP endpoint communication
- Validate OTLP receiver authentication in production

### Middleware Configuration

```python
# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    
    return response
```

### Hashing

- **Algorithm**: Argon2id (recommended) or bcrypt
- **Work factor**: Configurable cost parameter
- **Salt**: Automatically generated per password

```python
# Password hashing example
import argon2

hasher = argon2.PasswordHasher(
    time_cost=15,  # 15 iterations
    memory_cost=64,  # 64 MiB
    parallelism=2,
    hash_len=32,
    type=argon2.Type.IDENTIFIER,
)

# Hash password
hashed = hasher.hash("user-password")

# Verify password
try:
    hasher.verify(hashed, "user-password")
    print("Password verified!")
except argon2.exceptions.VerifyMismatchError:
    print("Password verification failed")
```

```python
# FastAPI CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Rate-Limit-Limit", "X-Rate-Limit-Remaining"],
)
```

```python
# Simplified rate limiting
async def rate_limit_middleware(request, call_next):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    
    current_count = redis.incr(key)
    if current_count == 1:
        redis.expire(key, 60)  # 1 minute TTL
    
    if current_count > 100:  # Default limit
        retry_after = 60  # seconds
        raise RateLimitExceeded(retry_after=retry_after)
    
    response = await call_next(request)
    return response
```

- **Default limit**: 100 requests/minute per IP
- **Auth endpoint limit**: 10 requests/minute for login/register
- **Implementation**: Token bucket algorithm using Redis
- **Response**: 429 Too Many Requests with `Retry-After` header

```python
# Simplified auth middleware
async def auth_middleware(request, call_next):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        request.state.user = None
        return await call_next(request)
    
    token = auth_header.split(" ")[1]
    
    try:
        payload = jwt.decode(
            token,
            options={"verify": True},
            algorithms=["HS256"],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise AuthError("Token payload missing user identity")
        
        request.state.user = await get_user_by_id(user_id)
        if not request.state.user or not request.state.user.is_active:
            raise AuthError("User inactive or not found")
            
    except jwt.ExpiredSignatureError:
        raise AuthError("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthError("Invalid token")
    
    response = await call_next(request)
    return response
```

### JWT Authentication Middleware

Located in `api_gateway/middleware/auth.py`, the middleware:

1. **Extracts token** from `Authorization: Bearer <token>` header
2. **Validates token signature** using JWT_SECRET_KEY
3. **Decodes payload** to extract user identity
4. **Checks expiration** and validates `exp` and `nbf` claims
5. **Attaches user** to request state for downstream use
6. **Returns 401 Unauthorized** for invalid/missing tokens

#### Access Token

- **Duration**: 30 minutes (configurable via JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
- **Purpose**: Short-lived token for API access
- **Usage**: Included in `Authorization: Bearer <token>` header for each request
- **Signing**: HS256 algorithm with JWT_SECRET_KEY

#### Refresh Token

- **Duration**: 7 days (configurable via JWT_REFRESH_TOKEN_EXPIRE_DAYS)
- **Purpose**: Obtain new access tokens without re-authentication
- **Usage**: POST to `/api/v1/auth/refresh` with refresh token
- **Storage**: HttpOnly cookie or secure storage

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800,
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Login Request

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "user-password"
}
```

## Overview

CloudForge implements comprehensive JWT-based authentication and security measures across all microservices. The security architecture covers token-based authentication, password handling, rate limiting, and secure configuration management.
