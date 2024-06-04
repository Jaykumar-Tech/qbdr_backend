import time, datetime
import asyncio
from decouple import config

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from tools import get_user_id, send_email

from .repository import UserRepo
from app.auth.auth_bearer import JWTBearer, UserRoleBearer
from app.auth.auth_handler import signJWT, generateJWT, decode_token, decode_email_verify_JWT
from app.email_verify.repository import EmailVerifyRepo

from . import schema as userSchema

router = APIRouter()

@router.get("/admin/users", dependencies=[Depends(JWTBearer()), Depends(UserRoleBearer())], tags=["Admin", "User"])
async def get_all_user(db: Session = Depends(get_db)):
    """Get all user list

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    
    db_all_users = await UserRepo.get_all_user_table(db)
    user_count = len(db_all_users)
    active_user_count = await UserRepo.get_active_user_count(db)
    return {
        "user_count": user_count,
        "active_user_count": active_user_count,
        "user_data": db_all_users
    }

@router.get("/admin/users/{req_type}", dependencies=[Depends(JWTBearer()), Depends(UserRoleBearer())], tags=["Admin", "User"])
async def get_specific_users(req_type: str, db: Session=Depends(get_db)):
    result = None
    if req_type == "active_accounts":
        result = await UserRepo.get_active_user_table(db)
    else:
        result = await UserRepo.get_all_user_table(db)
    return {
        "user_data": result
    }
    
@router.post("/admin/users", dependencies=[Depends(JWTBearer()), Depends(UserRoleBearer())], tags=["Admin", "User"])
async def create_new_user(request: Request, db: Session=Depends(get_db)):
    request_data = await request.json()
    user_data = request_data["user_data"]
    db_user = await UserRepo.fetch_by_email(db, email=user_data['email'])
    if db_user:
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà!")
    db_user = await UserRepo.fetch_by_username(db, username=user_data['full_name'])
    if db_user:
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur existe déjà!")

    result = await UserRepo.create(db, user_data)
    if result == False:
        raise HTTPException(status_code=400, detail="Échec de la création de l'utilisateur !")
    
    payload = {
        "user_id": result.id,
        "email": result.email,
        "full_name": result.full_name,
        "time": time.time()
    }
    token = generateJWT(payload)

    add_token = await UserRepo.add_forgot_password_token(db, result.id, token)
    if add_token == False:
        raise HTTPException(status_code=400, detail="Échec de l'ajout du jeton.")
    
    welcome_msg = f"""
    <html>
        <body>
            <h2>Bonjour {result.full_name}</h2>
            <p>Reeact vous invite à rejoindre votre interface d’analyse via le lien ci dessous :</p>
            <p><a href="{config("SITE_URL")}/forgot-password?token={token}">Reset Password!</a></p>
            <p>Voici votre identifiant de connexion :</p>
            <p>{result.email}</p>x
            <img src="{config("SITE_URL")}/static/logoblue.png" alt="Reeact"></img>
        </body>
    </html>
    """
    await send_email(result.email, "Bienvenue sur Reeact!", welcome_msg)
    
    return result
    
@router.get("/admin/user/{user_id}", dependencies=[Depends(JWTBearer()), Depends(UserRoleBearer())], tags=["Admin", "User"])
async def get_user_by_id(user_id: int, db: Session=Depends(get_db)):
    user = await UserRepo.get_user_by_id(db, user_id)
    return {
        "user_data": user,
    }

@router.post("/admin/activate_user", dependencies=[Depends(JWTBearer()), Depends(UserRoleBearer())], tags=["Admin", "User"])
async def activate_user(request: Request, db: Session=Depends(get_db)):
    req_data = await request.json()
    user_id = req_data['user_id']
    is_activate = req_data['activated']
    if user_id == None or is_activate == None:
        raise HTTPException(status_code=403, detail="Erreur de données de demande !")
    res = await UserRepo.activate_user(db, user_id, is_activate)
    if res == False:
        raise HTTPException(status_code=403, detail="DB Error!")
    return {
        "result": True
    }

@router.get("/admin/setting", dependencies=[Depends(JWTBearer()), Depends(UserRoleBearer())], tags=["Admin", "User"])
async def get_my_user_data(request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    result = await UserRepo.get_user_by_id(db, user_id)
    return result

@router.post("/admin/setting", dependencies=[Depends(JWTBearer()), Depends(UserRoleBearer())], tags=["Admin", "User"])
async def update_my_user_data(user_data: userSchema.UserUpdate, request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    user_data.role = 0
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

@router.get("/admin/statistics/", dependencies=[Depends(JWTBearer()), Depends(UserRoleBearer())], tags=["Admin", "Statistics"])
async def get_statistics(db: Session=Depends(get_db)):
    cur_date = datetime.datetime.now()
    cur_month = cur_date.month
    cur_year = cur_date.year
    pre_month = cur_month - 1 if cur_month != 1 else 12
    pre_year = cur_year if cur_month != 1 else cur_year - 1
    pre1_month = pre_month - 1 if pre_month != 1 else 12
    pre1_year = pre_year if pre_month != 1 else pre_year - 1
    pre_month_acc = await UserRepo.get_monthly_acc_count(db, pre_year, pre_month)
    pre1_month_acc = await UserRepo.get_monthly_acc_count(db, pre1_year, pre1_month)
    acc_count = await UserRepo.get_daily_acc_data(db)
    statistics_data = {
        "cur_month_acc": pre_month_acc,
        "pre_month_acc": pre1_month_acc,
        "acc_count": acc_count
    }
    return statistics_data

@router.post("/user/signup", tags=["User"])
async def create_user(user_request: Request, db: Session = Depends(get_db)):
    """
        Create a User and store it in the database
    """
    request_data = await user_request.json()
    user_data = request_data['user_data']
    
    email_verify_token = request_data["email_verify_token"] if "email_verify_token" in request_data else None
    if email_verify_token == None:
        raise HTTPException(status_code=400, detail="No Email Verify Token.")
    email_verify_payload = decode_email_verify_JWT(email_verify_token)
    if email_verify_payload == False:
        raise HTTPException(status_code=400, detail="Invalid Token!")
    if user_data["email"] != email_verify_payload["email"]:
        raise HTTPException(status_code=400, detail="Token doesn't match.")
    verify_result = await EmailVerifyRepo.check_verify_code(db, email_verify_payload["email"], email_verify_payload["verify_code"])
    if verify_result != True:
        raise HTTPException(status_code=400, detail=verify_result)
    
    db_user = await UserRepo.fetch_by_email(db, email=user_data['email'])
    if db_user:
        raise HTTPException(status_code=400, detail="L'email existe déjà!")
    db_user = await UserRepo.fetch_by_username(db, username=user_data['full_name'])
    if db_user:
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur existe déjà!")
    user_data["email_verified"] = True
    user_data["payment_verified"] = False
    
    created_user = await UserRepo.create(db=db, user=user_data)
    
    print("user created on db and stripe!")
    # await EmailVerifyRepo.delete(db, created_user.email)
    
    jwt = signJWT(created_user.id, user_data['email'], created_user.role, created_user.subscription_at)
    welcome_msg = f"""
    <html>
        <body>
            <h2>Bonjour {created_user.full_name}</h2>
            <p>Nous sommes ravis de vous accueillir en tant que nouvel utilisateur de la plateforme Reeact!</p>
            <p>Nous sommes impatients de travailler avec vous et de vous offrir le meilleur service possible.</p>
            <p>Si vous avez des questions ou des besoins spécifiques, n'hésitez pas à nous contacter.</p>
            <p>Bonne analyse!<br/>L’équipe Reeact</p>
            <img src="{config("SITE_URL")}/static/logoblue.png" alt="Reeact"></img>
        </body>
    </html>
    """
    print(welcome_msg)
    await send_email(created_user.email, "Bienvenue sur Reeact!", welcome_msg)
    print("welcome message sent!")
    admin_maile_content = f"""
    <html>
        <body>
            <h2>Bonjour!</h2>
            <p>Un nouvel utilisateur s’est inscrit sur votre plateforme, voici les informations d’inscriptions :</p>
            <p>{created_user.full_name}</p>
            <p>{created_user.email}</p>
            <p>Merci!<br/>L’équipe Reeact</p>
            <img src="{config("SITE_URL")}/static/logoblue.png" alt="Reeact"></img>
        </body>
    </html>
    """
    print(admin_maile_content)
    admin_list = await UserRepo.get_admins_data(db)
    for admin in admin_list:
        await send_email(admin.email, "Nouveau utilisateur", admin_maile_content)
    print("send emails to admins completed!")
    return {
        "user": created_user,
        "jwt": jwt,
    }

@router.post("/user/login", tags=["User"])
async def login(user_request: userSchema.UserLogin, db: Session = Depends(get_db)):
    """
        Login User with Email and Password
    """
    db_user = await UserRepo.fetch_by_email_password(db, email=user_request.email, password=user_request.password)
    if db_user:
        jwt = signJWT(db_user.id, db_user.email, db_user.role, db_user.subscription_at)
        return {
            "user": db_user,
            "jwt": jwt
        }
    else:
        raise HTTPException(status_code=400, detail=db_user)

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

@router.get("/user/dashboard", dependencies=[Depends(JWTBearer())], tags=["Dashboard"])
async def get_dashboard_data(request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    return {
        "reputation_score": ""
    }
    
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
