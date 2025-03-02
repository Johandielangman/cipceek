# CIPCeek

Selenium Docs: https://selenium-python.readthedocs.io
Sqlalchemy: https://docs.sqlalchemy.org/en/20/
Loguru: https://loguru.readthedocs.io/en/stable/overview.html


```python
logger.add("file.log", format="{extra[ip]} {extra[user]} {message}")
context_logger = logger.bind(ip="192.168.0.1", user="someone")
context_logger.info("Contextualize your logger easily")
```