# API Documentation

## Endpoints

### 1. Signup

**Endpoint:** `api/signup/`
**Method:** POST

**Request:**

```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "date_of_birth": "1990-01-01",
  "gender": 1,
  "phone_number": "string",
  "address": "string"
}
```

**Response:**

```json
{
  "status": true,
  "message": "Verification email sent to faaiz290302@gmail.com. Please verify your account.",
  "errorCode": null,
  "result": {
    "username": "string",
    "email": "user@example.com",
    "password": "string",
    "phone_number": "strings",
    "address": "string",
    "date_of_birth": "2019-08-24",
    "gender": 0,
    "bio": "string",
    "first_name": "string",
    "last_name": "string",
    "date_joined": "2019-08-24T14:15:22Z",
    "is_verified": true,
    "profile_picture": "http://example.com"
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
  "email": "user@example.com",
  "password": "string"
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
      "username": "string",
      "email": "user@example.com",
      "password": "string",
      "phone_number": "strings",
      "address": "string",
      "date_of_birth": "2019-08-24",
      "gender": 0,
      "bio": "string",
      "first_name": "string",
      "last_name": "string",
      "date_joined": "2019-08-24T14:15:22Z",
      "is_verified": true,
      "profile_picture": "http://example.com"
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
  "refresh": "string"
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
    "access": "string"
  },
  "hasResult": true
}
```

### 5. Logout

**Endpoint:** `api/logout/`
**Method:** POST

**Request:**

```json
{
  "refresh": "string"
}
```

**Response:**

```json
{
  "status": true,
  "message": "Logout successfully.",
  "errorCode": "",
  "errors": null,
  "result": null,
  "hasResult": false
}
```

### 6. Change Password

**Endpoint:** `api/change-password/`
**Method:** POST

**Request:**

```json
{
  "old_password": "string",
  "new_password": "string",
  "again_new_password": "string"
}
```

**Response:**

```json
{
  "status": true,
  "message": "Password changed successfully.",
  "errorCode": "",
  "errors": null,
  "result": null,
  "hasResult": false
}
```

### 7. Edit Profile Details

**Endpoint:** `api/edit-profile-details/`
**Method:** POST

**Request:**

```json
{
  "first_name": "string",
  "last_name": "string",
  "user_name": "string",
  "address": "string",
  "bio": "string"
}
```

**Response:**

```json
{
  "status": true,
  "message": "Profile updated successfully.",
  "errorCode": "",
  "errors": null,
  "result": {
    "username": "string",
    "email": "user@example.com",
    "password": "string",
    "phone_number": "strings",
    "address": "string",
    "date_of_birth": "2019-08-24",
    "gender": 0,
    "bio": "string",
    "first_name": "string",
    "last_name": "string",
    "date_joined": "2019-08-24T14:15:22Z",
    "is_verified": true,
    "profile_picture": "http://example.com"
  },
  "hasResult": true
}
```

### 8. User Name Availablility

**Endpoint:** `api/is-username-available/`
**Method:** POST

**Request:**

```json
{
  "username": "string"
}
```

**Response:**

```json
{
  "status": true,
  "message": "Username availability check completed.",
  "errorCode": "",
  "errors": null,
  "result": {
      "user_name_availbility": true
  },
  "hasResult": true
}
```
