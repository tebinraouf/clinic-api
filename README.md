# clinic-api
A Python API written in Flask

# How to run
- Development
    ```python
    FLASK_APP=app.py FLASK_DEBUG=1 python3 -m flask run
    ```
- Production
    ```python
    python3 waitress_server.py
    ```