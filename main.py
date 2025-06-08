import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dao.config.database import get_async_session 
from services.handleRegister import handleRegister
from services.handleLogin import handleLogin
from models.pydantic.Usuario import UsuarioBase

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "funcionando"}

@app.get("/api/getbyid")
def getbyid():
    pass 

@app.post("/api/register")
async def register_endpoint(form_data: UsuarioBase, session: AsyncSession = Depends(get_async_session)):
    await handleRegister(form_data, session)
    return {"[200]", "User saved with success"}

    

@app.post('/api/login')
async def login_endpoint(data: UsuarioBase, session: AsyncSession = Depends( get_async_session )):
    return await handleLogin(data, session)

@app.post('/api/verify-otp')
async def verify_otp(email: str, otp: str):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)