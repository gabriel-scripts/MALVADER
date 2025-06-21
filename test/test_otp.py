import pytest
from fastapi import HTTPException
from util.send_otp import send_otp

@pytest.mark.anyio
async def test_validate_otp_success():
    otp = '1234'
    email = 'gabriel123@gmail.com'
    try:
        resultado = await send_otp(email, otp)
        print(resultado)
    except HTTPException:
        pytest.fail("validate_data should not raise HTTPException for valid data")

@pytest.mark.anyio
async def test_validate_data_success():
    otp = ''
    email = 'gabriel123@gmail.com'
    
    with pytest.raises(HTTPException) as excinfo:
        await send_otp(email, otp)
    assert "OTP cannot be null" in str(excinfo.value)

@pytest.mark.anyio
async def test_validate_data_success():
    otp = '1234'
    email = ''
    
    with pytest.raises(HTTPException) as excinfo:
        await send_otp(email, otp)
    assert "Need a email to send OTP" in str(excinfo.value)