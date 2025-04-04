from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from schemas.auth import LoginRequest, LoginSuccessResponse, LoginFailedResponse
from security import verify_password, create_access_token
from database import get_db

router = APIRouter()

@router.post("/login", 
    response_model=LoginSuccessResponse,
    responses={
        401: { "model": LoginFailedResponse },
    }
)
async def login(
    request: LoginRequest, 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {
        "token": access_token,
        "message": "Login successful"
    }
