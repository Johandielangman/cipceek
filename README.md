# CIPCeek

Selenium Docs: https://selenium-python.readthedocs.io
Sqlalchemy: https://docs.sqlalchemy.org/en/20/
Loguru: https://loguru.readthedocs.io/en/stable/overview.html
driver manager: https://pypi.org/project/webdriver-manager/


```python
logger.add("file.log", format="{extra[ip]} {extra[user]} {message}")
context_logger = logger.bind(ip="192.168.0.1", user="someone")
context_logger.info("Contextualize your logger easily")
```


For the downloads folder:

```python
options = webdriver.ChromeOptions() ;
prefs = {"download.default_directory" : "<directory_path>;
#example: prefs = {"download.default_directory" : "C:\Tutorial\down"};
options.add_experimental_option("prefs",prefs);
```