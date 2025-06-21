 # Commands for tests:


```
pytest test/test_validate_register.py
pytest test/test_otp.py
pytest test/test_password.py
```

```
pytest test/EXAMPLE.py
```

## Covarege:

```
pytest --cov=. --cov-report=term --capture=tee-sys
```

### HTML:

```
pytest --cov=. --cov-report=html --capture=tee-sys
```