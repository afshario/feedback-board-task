from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from config import SECRET_KEY,ALGORITHM

security = HTTPBearer()


def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
      token = credentials.credentials

      try:
            payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
            )

            return payload

      except JWTError as e: 
            raise HTTPException(
                  status_code=status.HTTP_401_UNAUTHORIZED,
                  detail=f"Invalid token: {str(e)}"
            )
      except Exception:
            raise HTTPException(
                  status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="Invalid token"
            )