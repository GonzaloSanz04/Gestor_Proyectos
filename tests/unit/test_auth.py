from datetime import datetime, UTC, timedelta

import pytest

from src.services.auth import hashear_password, verificar_password, crear_token
from src.config import settings

import jwt


USUARIO_ID = 1
PASSWORD = "mi_contraseña_test"

@pytest.fixture
def payload():
    token = crear_token(USUARIO_ID)
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

@pytest.fixture
def hashed():
    return hashear_password(PASSWORD)

def test_crear_token_verificar_idusuario_correcto(payload):

    assert payload["sub"] == str(USUARIO_ID)

def test_crear_token_rechaza_firma_invalida():

    token = crear_token(USUARIO_ID)
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(token, "x" * 32, algorithms=[settings.jwt_algorithm])

def test_crear_token_verificar_expiration_correcta(payload):

    assert "exp" in payload
    assert payload["exp"] > datetime.now(UTC).timestamp()

def test_crear_token_verificar_exp_no_supera_duracion_configurada(payload):

    limite = datetime.now(UTC).timestamp() + timedelta(minutes=settings.access_token_expire_minutes + 1).total_seconds()
    assert payload["exp"] < limite

def test_token_expirado():

    expired_token = jwt.encode({"sub": str(USUARIO_ID), "exp": datetime.now(UTC) - timedelta(minutes=1)}, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(expired_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

def test_hashear_y_verificar_password_correcto(hashed):

    assert verificar_password(PASSWORD, hashed) is True

def test_hashear_y_verificar_password_incorrecto(hashed):

    assert verificar_password("incorrecta", hashed) is False

def test_hashear_y_verificar_password_multiple(hashed):

    hashed1 = hashear_password(PASSWORD)

    assert hashed1 != hashed

def test_hashear_y_verificar_hash(hashed):

    assert hashed != PASSWORD
