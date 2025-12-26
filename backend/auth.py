import bcrypt
from utils.database import create_user, get_user_by_email
def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against the stored hash.
    """
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def register_user(name: str, email: str, password: str) -> dict:
    """
    Registers a new user.
    Returns a dict with success status and message.
    """

    # Backend validation (never trust frontend)
    if not name or not email or not password:
        return {"success": False, "message": "All fields are required."}

    if len(password) < 8:
        return {"success": False, "message": "Password must be at least 8 characters long."}

    # Check if user already exists
    existing_user = get_user_by_email(email)
    if existing_user:
        return {"success": False, "message": "User already exists"}

    # Hash password
    password_hash = hash_password(password)

    # Create user in database
    success = create_user(name, email, password_hash)

    if success:
        return {"success": True, "message": "Registration successful."}
    else:
        return {"success": False, "message": "Registration failed."}
    
def login_user(email: str, password: str) -> dict:
    """
    Logs in a user.
    Returns a dict with success status and user data.
    """

    user = get_user_by_email(email)

    # Security best practice: generic error message
    if not user:
        return {"success": False, "message": "Invalid email or password."}

    if not verify_password(password, user["password_hash"]):
        return {"success": False, "message": "Invalid email or password."}

    # Successful login
    return {
        "success": True,
        "user": {
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }