"# API Documentation

## Endpoints

### 1. Signup

**Endpoint:** `api/signup/`
**Method:** POST

**Request:**
```json 
{
    "username": "faaiz88",
    "email": "faaiz290302@gmail.com",
    "password": "#Trigonometry1",
    "first_name": "Syed Faizan",
    "last_name": "Hussain",
    "date_of_birth": "1990-01-01",
    "gender": 1,
    "phone_number": "1234567890",
    "address": "123 Example St, City, Country"
}
```

**Response:**
```json
{
    "status": true,
    "message": "Verification email sent to faaiz290302@gmail.com. Please verify your account.",
    "errorCode": null,
    "result": {
        "username": "faaiz88",
        "email": "faaiz290302@gmail.com",
        "first_name": "Syed Faizan",
        "last_name": "Hussain",
        "date_of_birth": "1990-01-01",
        "gender": 1,
        "phone_number": "1234567890",
        "address": "123 Example St, City, Country"
    },
    "hasResult": true
}
```

### 2. Login

**Endpoint:** `api/login/`
**Method:** POST

**Request:**
```json
{
    "email": "faaiz290302@gmail.com",
    "password": "#Trigonometry1"
}
```

**Response:**
```json
{    
    "status": true,
    "message": "Login successful.",
    "errorCode": null,
    "result": {
        "user": {
            "username": "faaiz88",
            "email": "faaiz290302@gmail.com",
            "first_name": "Syed Faizan",
            "last_name": "Hussain",
            "date_of_birth": "1990-01-01",
            "gender": 1,
            "phone_number": "1234567890",
            "address": "123 Example St, City, Country"
        },
        "tokens": {
            "access": "xxx",
            "refresh": "xxx"
        }
    },
    "hasResult": true
}
```

### 3. Verify Email

**Endpoint:** `api/verify-email/<token>`
**Method:** GET

**Response:**
```json
{
    "status": true,
    "message": "Email verified successfully.",
    "errorCode": null,
    "result": null,
    "hasResult": false
}
```

### 4. Refresh Token

**Endpoint:** `api/refresh/token`
**Method:** POST

**Request:**
```json
{
    "refresh": "xxx"
}
```

**Response:**
```json
{
  "status": true,
  "message": "Token refreshed successfully.",
  "errorCode": "",
  "errors": null,
  "result": {
    "access": "xxx"
  },
  "hasResult": true
}
```
