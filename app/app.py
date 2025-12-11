from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory "database"
users_db: Dict[int, dict] = {}

# Pydantic model
class User(BaseModel):
    name: str
    email: str

# Create User
@app.post("/users/{user_id}")
def create_user(user_id: int, user: User):
    if user_id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user_id] = user.dict()
    return {"message": "User created", "user": users_db[user_id]}

# Get User
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

# Update User
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user.dict()
    return {"message": "User updated", "user": users_db[user_id]}

# Delete User
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted"}

# List All Users
@app.get("/users")
def list_users():
    return users_db

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API"}