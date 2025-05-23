import os
import duckdb
from backend.models import UserLogin
from backend.logger import log_access, log_failed_login
from fastapi import FastAPI, HTTPException, Depends, Header
from backend.auth import verify_password, create_token, decode_token

app = FastAPI()
duckdb.connect(os.getcwd() + '/database/annotated_ultrasound.duckdb')

def auth_required(authorization: str = Header(...)):

    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise ValueError()

        return decode_token(token)

    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/login")
def login(user: UserLogin):

    with duckdb.connect(os.getcwd() + "/database/annotated_ultrasound.duckdb") as connection:
        result = connection.execute("SELECT password FROM users WHERE username = ?", (user.username,)
    ).fetchone()
        
    if result is None:
        log_failed_login(user.username)
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(user.password, result[0]):
        raise HTTPException(status_code=401, detail="Invalid password")

    log_access(user.username, "/login")
    return {"token": create_token({"sub": user.username})}

@app.get("/secure-data")
def secure_data(token: dict = Depends(auth_required)):

    log_access(token["sub"], "/secure-data")

    return {"message": f"Hello {token['sub']}, your data is safe!"}