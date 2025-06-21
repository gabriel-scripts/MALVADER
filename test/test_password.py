import pytest
from fastapi import HTTPException
from services.validadeData import is_password_strong

@pytest.mark.anyio
async def test_validate_password_success():
    password = "G@NSDWMNamwdn291-/"
    try:
        resultado = await is_password_strong(password)
        assert resultado is None  # Função não retorna nada se for válida
    except HTTPException:
        pytest.fail("validate_data should not raise HTTPException for valid data")

@pytest.mark.anyio
async def test_validate_password_length():
    password = "Short1!"
    with pytest.raises(HTTPException) as excinfo:
        await is_password_strong(password)
    assert "password need 12 caracteres length" in str(excinfo.value)

@pytest.mark.anyio
async def test_validate_password_uppercase():
    password = "lowercase@1234"
    with pytest.raises(HTTPException) as excinfo:
        await is_password_strong(password)
    assert "password need at least one UPPERCASE" in str(excinfo.value)

@pytest.mark.anyio
async def test_validate_password_downcase():
    password = "UPPERCASE@1234"
    with pytest.raises(HTTPException) as excinfo:
        await is_password_strong(password)
    assert "password need at least one DOWNCASE" in str(excinfo.value)

@pytest.mark.anyio
async def test_validate_password_number():
    password = "NoNumber@Passw"
    with pytest.raises(HTTPException) as excinfo:
        await is_password_strong(password)
    assert "password need at least one number" in str(excinfo.value)

@pytest.mark.anyio
async def test_validate_password_special():
    password = "NoSpecial1234A"
    with pytest.raises(HTTPException) as excinfo:
        await is_password_strong(password)
    assert "password need at least one special caracterer" in str(excinfo.value)