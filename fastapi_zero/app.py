from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.schema import Message

from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return Message(message='Olá Mundo!!')


@app.get(
    '/greetings',
    response_class=HTMLResponse
)
def greet():
    return """
    <html>
      <head>
        <title>Ex HTML</title>
      </head>
      <body>
        <h1>Olá, mundo!</h1>
      </body>
    </html>"""
