 # How to run tests:


```
pytest test/test_validate.py
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