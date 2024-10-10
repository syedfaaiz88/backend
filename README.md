# API Documentation

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
      "username": "sohaibfazal68",
      "email": "bcsf19m010@pucit.edu.pk",
      "phone_number": "03334461447",
      "address": "Lahore",
      "date_of_birth": "2001-10-25",
      "gender": 1,
      "bio": "SQA Engineer @ Bigentities",
      "first_name": "Sohaib",
      "last_name": "Fazal",
      "date_joined": "2024-08-29T21:24:19.457513Z",
      "is_verified": true
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

### 5. Logout

**Endpoint:** `api/logout/`
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
  "new_password": "xxx",
  "again_new_password": "xxx",
  "old_password": "xxxx"
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
  "first_name": "xxx",
  "last_name": "xxx",
  "user_name": "xxx",
  "address": "xxx",
  "bio": "xxx"
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
    "username": "sohaibfazal68",
    "email": "bcsf19m010@pucit.edu.pk",
    "phone_number": "03334461447",
    "address": "Lahore",
    "date_of_birth": "2001-10-25",
    "gender": 1,
    "bio": "SQA Engineer @ Bigentities",
    "first_name": "Sohaib",
    "last_name": "Fazal",
    "date_joined": "2024-08-29T21:24:19.457513Z",
    "is_verified": true
  },
  "hasResult": true
}
```
