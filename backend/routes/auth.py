from fastapi import APIRouter, HTTPException, status
from schemas import RegisterUser, LoginUser, TokenResponse
from auth import hash_password, verify_password, create_access_token
from database import users_collection

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterUser):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = {
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_pw,
        "bio": user.bio,
        "skills_offered": user.skills_offered,
        "skills_wanted": user.skills_wanted,
    }

    users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
def login_user(credentials: LoginUser):
    user = users_collection.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user["email"]})
    return TokenResponse(access_token=access_token)
