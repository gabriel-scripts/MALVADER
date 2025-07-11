from fastapi import HTTPException

from util.verify_password import verify_password
from util.send_otp import send_otp
from util.generate.generate_otp import generate_otp

from dao.repository.UserRepository import UserRepository
from dao.repository.FuncionarioRepository import FuncionarioRepository

from fastapi import BackgroundTasks

async def handleLogin(login_data, session, background_tasks: BackgroundTasks):
    login_dict = login_data.dict()

    user_db = UserRepository(session)
    funcionario_db = FuncionarioRepository(session)

    user = await user_db.find_by_cpf(login_dict["cpf"])        
    if not user:
        raise HTTPException(status_code=400, detail="User not exists")

    if user.tipo_usuario == 'funcionario':
        if not login_dict["codigo_funcionario"]:
            raise HTTPException(status_code=400, detail="Funcionario code connot be null")

        codigo = funcionario_db.find_by_codigo(login_dict["codigo_funcionario"])
        if not codigo:
            raise HTTPException(status_code=400, detail="Funcionario not exists")
        
    await verify_password(user.senha_hash, login_dict["senha"], user.id_usuario, session)
    otp = await generate_otp(session, user.id_usuario)
    if not otp:
        raise HTTPException(status_code=400, detail="error to generate OTP")
    
    background_tasks.add_task(send_otp, user.email, otp)