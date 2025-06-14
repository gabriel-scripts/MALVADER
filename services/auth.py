from datetime import datetime
from fastapi import HTTPException

from dao.repository.UserRepository import UserRepository
from dao.repository.FuncionarioRepository import FuncionarioRepository

from util.jwt.JWT import create_access_token
from util.save_auditoria import save_auditoria

async def auth(auth_input, session):

    auth_dict = auth_input.dict()

    print(auth_input)

    user_db = UserRepository(session)
    user = await user_db.find_by_cpf(auth_dict["cpf"])

    print(user.__dict__)

    if(user.otp_ativo == None):
        raise HTTPException(status_code=400, detail="User with no OTP")
    
    if user.otp_expiracao is None or user.otp_expiracao < datetime.now():
        raise HTTPException(status_code=400, detail="Otp Expiretad")
    
    if(user.otp_ativo != auth_dict["otp"]):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    if user.tipo_usuario == 'cliente':
        data = {
            "id_usuario": user.id_usuario,
            "cpf": user.cpf,
            "email": user.email,
            "tipo_usuario": user.tipo_usuario
        }
        
        auditoria_data = {
            "id_usuario": user.id_usuario,
            "acao": "logar_cliente",
            "data_hora": datetime.now(),
            "detalhes": f"Usuário {user.email} logado com sucesso"
        }

        await save_auditoria(session, auditoria_data)
        codigo = await create_access_token(data)
        return {"cliente": codigo}
    
    if user.tipo_usuario == 'funcionario':

        funcionario_repository = FuncionarioRepository(session)
        funcionario = await funcionario_repository.find_by_codigo(auth_dict["codigo_funcionario"]) 

        if not funcionario:
            raise HTTPException(status_code=400, detail="Funcionario not exists")

        data = {
            "id_usuario": user.id_usuario,
            "email": user.email,
            "codigo_funcionario": funcionario.codigo_funcionario,
            "tipo": user.tipo_usuario,
            "cargo": funcionario.cargo
        }

        auditoria_data = {
            "id_usuario": user.id_usuario,
            "acao": "logar_funcionario",
            "data_hora": datetime.now(),
            "detalhes": f"Usuário {user.email} logado com sucesso"
        }

        await save_auditoria(session, auditoria_data)
        codigo = await create_access_token(data)
        return {"funcionario": codigo}