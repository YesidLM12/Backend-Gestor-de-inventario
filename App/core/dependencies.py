
from fastapi import HTTPException, Request, status
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


def get_current_user_from_request(request: Request):
    """Get the current user from the request"""

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    
    token = auth_header.split(' ')[1]

    try:

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        role = payload.get('role')

        if not username or not role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

        return {"username": username, "role": role}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')