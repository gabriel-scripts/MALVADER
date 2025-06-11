from fastapi import HTTPException

from util.verify_password import verify_password
from util.send_otp import send_otp
from util.generate.generate_otp import generate_otp

from dao.repository.UserRepository import UserRepository

async def handleLogin(login_data, session):
    login_dict = login_data.dict()

    user_db = UserRepository(session)
    user = await user_db.find_by_cpf(login_dict["cpf"])

    if not user:
        raise HTTPException(status_code=400, detail="User not exists")

    try: 
        await verify_password(user.senha_hash, login_dict["senha"])
        otp = await generate_otp(session, user.id_usuario)
        if not otp:
            raise HTTPException(status_code=400, detail="error to generate OTP")
        await send_otp(user.email, otp)
    except Exception as e:
        print(f"erro: {e}")