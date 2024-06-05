import time
from decouple import config

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from tools import get_user_id, send_email

from .repository import UserRepo
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT, generateJWT, decode_token

from . import schema as userSchema

router = APIRouter()

@router.post("/user/signup", tags=["User"])
async def create_user(user_request: userSchema.UserCreate, db: Session = Depends(get_db)):
    """
        Create a User and store it in the database
    """
    
    db_user = await UserRepo.fetch_by_email(db, email=user_request.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists!")
    db_user = await UserRepo.fetch_by_username(db, username=user_request.full_name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists!")
    
    try:
        created_user = await UserRepo.create(db=db, user=user_request)
        print("user created successfully!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    jwt = signJWT(created_user.to_dict())

    return {
        "user": created_user,
        "jwt": jwt,
    }

@router.post("/user/login", tags=["User"])
async def login(user_request: userSchema.UserLogin, db: Session = Depends(get_db)):
    """
        Login User with Email and Password
    """
    try:
        db_user = await UserRepo.fetch_by_email_password(db, email=user_request.email, password=user_request.password)
        jwt = signJWT(db_user.to_dict())
        return {
            "user": db_user,
            "jwt": jwt
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/password_forgot/{email}", tags=["User"])
async def password_forgot(email: str, db: Session=Depends(get_db)):
    email_confirm = await UserRepo.fetch_by_email(db, email)
    if not email_confirm:
        raise HTTPException(status_code=403, detail="L'utilisateur n'existe pas.")
    payload = {
        "user_id": email_confirm.id,
        "email": email,
        "full_name": email_confirm.full_name,
        "time": time.time()
    }
    token = generateJWT(payload)
    email_body = f"""
    <html>
        <body>
            <p>Bonjour!</p>
            <p>Si cette demande ne vous appartient pas, veuillez ignorer ce message.</p>
            <p>S'il vous plaît allez à <a href="{config("SITE_URL")}/forgot-password?token={token}">réinitialiser le mot de passe</a>.</p>
            <p>Veuillez saisir le code du site !</p>
        </body>
    </html>
    """
    add_token = await UserRepo.add_forgot_password_token(db, email_confirm.id, token)
    if add_token == False:
        raise HTTPException(status_code=400, detail="Échec de l'ajout du jeton.")
    send_result = await send_email(email, "Réinitialiser le mot de passe!", email_body)
    if send_result == False:
        raise HTTPException(status_code=400, detail="E-mail non envoyé !")
    return "Email sent successfully!"

@router.post("/password_forgot", tags=["User"])
async def check_password_forgot_token(request: Request, db: Session=Depends(get_db)):
    req_data = await request.json()
    token = req_data["token"]
    check_token = await UserRepo.check_password_forgot_token(db, token)
    if check_token == False:
        raise HTTPException(status_code=403, detail="jeton invalide")
    return True

@router.post("/change_password", tags=["user"])
async def change_password(request: Request, db: Session=Depends(get_db)):
    req_data = await request.json()
    token = req_data["token"]
    password = req_data["password"]
    payload = decode_token(token)
    
    check_token = await UserRepo.check_password_forgot_token(db, token)
    if check_token == False:
        raise HTTPException(status_code=403, detail="jeton invalide")
    
    user_id = payload["user_id"] if "user_id" in payload else None
    if user_id == None:
        raise HTTPException(status_code=403, detail="jeton invalide")
    user = userSchema.UserUpdate(forgot_password_token=" ",
                                password=password,
                                email=payload["email"],
                                full_name=payload["full_name"])
    change_password = await UserRepo.update_user_by_id(db, user, user_id)
    if change_password == False:
        raise HTTPException(status_code=403, detail="Échec de la mise à jour du mot de passe.")
    return "Password updated successfully."
    
@router.get("/user/setting", dependencies=[Depends(JWTBearer())], tags=["User"])
async def get_user_profile(request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    user_data = await UserRepo.get_user_by_id(db, user_id)
    if user_data == False:
        HTTPException(status_code=403, detail="Database Error!")
    return {
        "user_data": user_data
    }

@router.post("/user/setting", dependencies=[Depends(JWTBearer())], tags=["User"])
async def update_my_user_data(user_data: userSchema.UserUpdate, request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    token = user_data.forgot_password_token
    origin_user_data = await UserRepo.get_user_by_id(db, user_id)
    if origin_user_data.full_name != user_data.full_name:
        check_username = await UserRepo.fetch_by_username(db, user_data.full_name)
        if check_username:
            raise HTTPException(status_code=403, detail="Nom d'utilisateur existe déjà.")
    if origin_user_data.email != user_data.email:
        check_email = await UserRepo.fetch_by_email(db, user_data.email)
        if check_email:
            raise HTTPException(status_code=403, detail="L'e-mail existe déjà.")
        check_token = await UserRepo.check_password_forgot_token(db, token)
        if check_token == False:
            raise HTTPException(status_code=403, detail="jeton invalide")
    result = await UserRepo.update_user_by_id(db, user_data, user_id)
    return result

@router.put("/user/update/{user_id}", dependencies=[Depends(JWTBearer())], tags=["User"])
async def update_user(user_id: int, user_request: userSchema.UserUpdate, db: Session = Depends(get_db)):
    """
        Update User with id
    """
    
    db_user = await UserRepo.update_user_by_id(db, user=user_request, id=user_id)
    if db_user != "User not exist to update":
        return {
            "updated_user": db_user
        }
    return {
        "status": db_user
    }
