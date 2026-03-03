from typing import Annotated
from fastapi import FastAPI, Form
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345admin"

@app.post("/login")
def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    """
    Login endpoint that accepts username and password via form data.
    """
    
    logger.info(f"Login attempt - Username: '{username}', Password: '{password}'")
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        logger.info(f"✅ Successful login for user: {username}")
        return {
            "status": "success",
            "token": "secret_token_12345",
            "message": "Authentication successful"
        }
    else:
        logger.info(f"❌ Failed login attempt for user: {username}")
        return {
            "status": "error",
            "message": "Invalid credentials"
        }

@app.get("/")
def root():
    """Home page with server information"""
    return {
        "message": "Brute-force attack demonstration server",
        "endpoints": {
            "POST /login": "Login endpoint (accepts form data: username, password)"
        },
        "warning": "This server is for educational purposes only!"
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}
