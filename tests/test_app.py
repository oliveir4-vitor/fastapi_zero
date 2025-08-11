from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA)
    A: Arrange  - Arranjo
    A: Act      - Executa a coisa (o SUT)
    A: Assert   - Garanta que algo é algo
    """
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!!'}  # Assert


def greet_test():
    client = TestClient(app)

    response = client.get('/greetings')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == '<h1>Olá, mundo!</h1>' in response.text
