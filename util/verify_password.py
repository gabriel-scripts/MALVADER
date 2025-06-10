import hashlib

from fastapi import HTTPException

async def verify_password(user_hashed_password, input_password):
    input_password_hashed = hashlib.md5(input_password.encode()).hexdigest()

    if user_hashed_password != input_password_hashed:
        raise HTTPException(status_code=400, detail="Invalid password")