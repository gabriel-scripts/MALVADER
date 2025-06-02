from validadeData import validate_data

async def handleLogin(data, otp):
    try: 
        validate_data(data)
    except Exception as e:
        pass