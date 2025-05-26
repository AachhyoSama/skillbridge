from fastapi import APIRouter, HTTPException, Depends
from models.user import User
from schemas import UserPublic, UpdateUser
from database import users_collection
from dependencies.auth import get_current_user

router = APIRouter()


# access my profile
@router.get("/me")
def get_profile(current_user: dict = Depends(get_current_user)):
    current_user["_id"] = str(current_user["_id"])
    return current_user


# update profile
@router.put("/me")
def update_profile(updated: UpdateUser, current_user: dict = Depends(get_current_user)):
    update_data = {k: v for k, v in updated.model_dump().items() if v is not None}
    if update_data:
        users_collection.update_one({"_id": current_user["_id"]}, {"$set": update_data})
    return {"message": "Profile updated successfully!"}


# add skills
@router.post("/me/skills")
def add_skills(skills: dict, current_user: dict = Depends(get_current_user)):
    skills_offered = skills.get("skills_offered", [])
    skills_wanted = skills.get("skills_wanted", [])
    update_query = {}

    if skills_offered:
        update_query["skills_offered"] = {"$each": skills_offered}
    if skills_wanted:
        update_query["skills_wanted"] = {"$each": skills_wanted}

    if update_query:
        users_collection.update_one(
            {"_id": current_user["_id"]}, {"$addToSet": update_query}
        )

    return {"message": "Skills added"}


# remove skills
@router.delete("/me/skills")
def remove_skills(skills: dict, current_user: dict = Depends(get_current_user)):
    skills_offered = skills.get("skills_offered", [])
    skills_wanted = skills.get("skills_wanted", [])
    update_query = {}

    if skills_offered:
        users_collection.update_one(
            {"_id": current_user["_id"]},
            {"$pull": {"skills_offered": {"$in": skills_offered}}},
        )

    if skills_wanted:
        users_collection.update_one(
            {"_id": current_user["_id"]},
            {"$pull": {"skills_wanted": {"$in": skills_wanted}}},
        )

    return {"message": "Skills removed"}


# delete user profile
@router.delete("/me")
def delete_account(current_user: dict = Depends(get_current_user)):
    users_collection.delete_one({"_id": current_user["_id"]})
    return {"message": "User account deleted"}


@router.get("/users", response_model=list[UserPublic])
def get_all_users():
    users = []
    for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(
            UserPublic(
                id=user["_id"],
                email=user["email"],
                username=user["username"],
                bio=user.get("bio", ""),
                skills_offered=user.get("skills_offered", []),
                skills_wanted=user.get("skills_wanted", []),
            )
        )
    return users


@router.get("/users/{email}", response_model=User)
def get_user_by_email(email: str):
    user = users_collection.find_one({"email": email}, {"_id": 0, "hashed_password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)
