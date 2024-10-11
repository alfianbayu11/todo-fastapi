# FastAPI To-Do List API

This is a simple To-Do List application backend built using **FastAPI**. The application provides API endpoints to register users, login with JWT authentication, and manage checklists and to-do items.

## Features
- User registration
- User login with JWT authentication
- CRUD operations for checklists
- CRUD operations for items within checklists
- Update item status (done/undone)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/alfianbayu11/todo-fastapi.git
   cd todo-fastapi
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**

   ```python
   from app.database import Base, engine
   Base.metadata.create_all(bind=engine)
   ```

5. **Run the application:**

   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API documentation at:**

   http://127.0.0.1:8000/docs

## API Endpoints

### Authentication
- **POST /register/** - Register a new user.
- **POST /login/** - Login with username and password to obtain a JWT token.

### Checklists
- **GET /checklists/** - Get all checklists for the logged-in user.
- **POST /checklists/** - Create a new checklist.
- **DELETE /checklists/{checklist_id}** - Delete a checklist.

### Checklist Items
- **GET /checklists/{checklist_id}/items** - Get all items for a checklist.
- **POST /checklists/{checklist_id}/items** - Add a new item to a checklist.
- **PUT /checklists/{checklist_id}/items/{item_id}/status** - Update the status of a checklist item (done/undone).
- **DELETE /checklists/{checklist_id}/items/{item_id}** - Delete an item from a checklist.

## JWT Authentication

This project uses JWT (JSON Web Token) for authentication. You need to include the `Authorization: Bearer {token}` header in requests that require authentication.

### Example login request:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

### Response:

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

Use this `access_token` in the `Authorization` header for protected routes:

```makefile
Authorization: Bearer your_jwt_token
```

## Testing the API

You can test the API using tools like **Postman**, **curl**, or **HTTPie**.

### Example requests

#### Register a new user

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/register/' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "user1",
  "email": "user1@example.com",
  "password": "password123"
}'
```

#### Login and get a JWT token

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/login/' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "user1",
  "password": "password123"
}'
```

#### Create a new checklist

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/checklists/' \
  -H 'Authorization: Bearer your_jwt_token' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Daily Tasks"
}'
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

### Testing Tools
- **Postman**: Use this to test the API by sending HTTP requests (POST, GET, PUT, DELETE).
- **curl** or **HTTPie**: CLI tools to interact with API endpoints.
