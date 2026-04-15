from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from http import HTTPStatus

from ..config.env import Settings, get_settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=get_settings().token_endpoint,
)

OAuth2Scheme = Annotated[str, Depends(oauth2_scheme)]


def get_decode_user_token(token: OAuth2Scheme, settings: Settings):
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.secret, 
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            headers={
                'WWW-Authenticate': 'Bearer',
                'error': 'invalid_token',
                'error_description': 'The access token expired',
                'Cache-Control': 'no-store',
                'Pragma': 'no-cache'
            },
            detail={
                'error': 'invalid_token',
                'error_description': 'The access token expired'
            }
        )
    
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            headers={
                'WWW-Authenticate': 'Bearer',
                'error': 'invalid_token',
                'error_description': 'The access token is invalid',
                'Cache-Control': 'no-store',
                'Pragma': 'no-cache'
            },
            detail={
                'error': 'invalid_token',
                'error_description': 'The access token is invalid'
            }
        )
    
    return UUID(payload.sub)

DecodeUserToken = Annotated[UUID, Depends(get_decode_user_token)]
