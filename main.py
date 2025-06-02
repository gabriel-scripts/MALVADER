import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dao.config.database import get_async_session
from services import handleRegister, handleLogin

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

@app.post("/register")
async def register_endpoint(form_data: dict, session: AsyncSession = Depends(get_async_session)):
    return await handleRegister(form_data, session)

@app.post('/login')
async def login_endpoint(data: dict, otp, session: AsyncSession = Depends(get_async_session)):
    return await handleLogin(data, otp, session)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)