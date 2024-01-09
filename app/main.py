from datetime import datetime, timedelta
from typing import Union, List

from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import crud
import apicall

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

SUBJECT = 'sub'
EXPIRATION_TIME = 'exp'

fake_users_db = {
    "yamada": {
        "username": "yamada",
        "full_name": "Yamada Taro",
        "age": 33,
        "height": 172,
        "weight": 65,
        "email": "yamada@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "tanaka": {
        "username": "tanaka",
        "full_name": "Tanaka Hanako",
        "age": 22,
        "height": 165,
        "weight": 53,
        "email": "tanaka@example.com",
        "hashed_password": "$2b$12$1qcPHSRytz4buadEFi8WsO9XS6ZqDD4a3Qqnvz5NjJXZ7ohz/upGG",
        "disabled": False,
    }

}


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

class UserLogin(BaseModel):
    email: str
    password: str

class FileInfo(BaseModel):
    file_name: Union[str, None] = None
    img: Union[bytes, None] = None
    file_id: str | None
    album_id: str | None
    url: str | None
    timestamp: str | None
    
class UserFile(BaseModel):
    user_id: Union[str, None] = None
    file_infos: List[FileInfo]| None
    
class User(BaseModel):
    username: str
    email: Union[str, None] = None
    password: Union[str, None] = None
    user_id: Union[int, None] = None
    disabled: bool | None = False
    
class UserInDB(User):
    hashed_password: str
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

#frontend側のIPを書く
origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_password(plain_password, hashed_password):
    print(plain_password,hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({EXPIRATION_TIME: expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    print("get_current_user")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f'### token = {token},  payload = {payload}')
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError as e:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials, " + str(type(e)),
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    
    info = crud.get_userinfo_by_username(username=username)
    if info == '':
       raise credentials_exception 
    print("##info##")
    print(info)
    user = UserInDB(hashed_password=info['password'],**info)
    
    if user is None:
        raise credentials_exception
    return user
    
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    print(current_user)
    if current_user.disabled:
    #if True:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/file", response_model=UserFile)
async def read_users_file(current_user: User = Depends(get_current_active_user)):
    info = crud.get_userinfo_by_email(email=current_user.email)
    file_infos = crud.get_fileinfo(info['user_id'])
    _infos = []
    for _info in file_infos:
        f = FileInfo(**_info)
        _infos.append(f)
    user_file = UserFile(user_id=str(info['user_id']),file_infos=_infos)
    return user_file

@app.get("/hello")
def hello():
    return {"Hello": "World"}

@app.post("/token",response_model=Token)
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
           
    # パスワードチェック
    hashedpass = crud.get_hashedpasswd(form_data.username)
    if hashedpass == '':
        raise credentials_exception
    
    ret = verify_password(form_data.password,hashedpass)
    
    #ユーザーログイン失敗
    if not ret:
        raise credentials_exception
    
    username = crud.get_username(form_data.username)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={SUBJECT: username}, expires_delta=access_token_expires
    )
    
    return {"token": access_token, "token_type": "bearer"}
   

@app.post("/upload/try")
def upload_file(file_info: FileInfo, current_user: User = Depends(get_current_user)):
    url = apicall.upload_s3(file_info.img)
    print(current_user.user_id,file_info.file_name,url)
    crud.add_file(current_user.user_id,file_info.file_name,url)
    return {"status": "OK"}

@app.post("/signup")
def signup(user: User):
    hash_pass = get_password_hash(user.password)
    crud.add_userinfo(user.username,user.email,hash_pass)
    return {"status": "OK"}

@app.delete("/token", response_model=Token)
def signup():
    return {"token": "access_token", "token_type": "bearer"}
# must mount on root(/) after all path operations, otherwise they will be overrided !
#app.mount("/", StaticFiles(directory="static/dist", html=True), name="html")
