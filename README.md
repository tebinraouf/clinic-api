# clinic-api
A Python API written in Flask

# How to run
- Development
    ```python
    FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run
    ```
- Production
    ```python
    python waitress_server.py
    ```