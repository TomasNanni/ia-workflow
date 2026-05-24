from app.services import auth as auth_service

def test_password_hashing():
    password = "secret_password"
    hashed = auth_service.get_password_hash(password)
    assert hashed != password
    assert auth_service.verify_password(password, hashed)
    assert not auth_service.verify_password("wrong_password", hashed)

def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = auth_service.create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0
