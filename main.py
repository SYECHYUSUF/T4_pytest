"""
main.py - FastAPI Microservice with JWT Authentication, RBAC, and Task CRUD
===========================================================================
Teknologi :  FastAPI, python-jose (JWT), passlib (bcrypt), python-multipart
Database   :  In-memory dictionary (mock, tanpa database nyata)
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Konfigurasi JWT
# ---------------------------------------------------------------------------
SECRET_KEY = "supersecretkey_ganti_di_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ---------------------------------------------------------------------------
# Inisialisasi Aplikasi
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Microservice API",
    description="FastAPI Microservice: JWT Auth + RBAC + Task CRUD",
    version="1.0.0",
)

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ---------------------------------------------------------------------------
# Mock Database (in-memory)
# ---------------------------------------------------------------------------
# Format: { "username": {"username": str, "hashed_password": str, "role": str} }
fake_users_db: dict = {}

# Format: { id: {"id": int, "title": str, "description": str, "owner": str} }
fake_tasks_db: dict = {}
task_id_counter: int = 1  # Auto-increment sederhana


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------
class UserRegister(BaseModel):
    username: str
    password: str
    role: str = "user"  # default role adalah 'user'


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class TaskCreate(BaseModel):
    title: str
    description: str = ""


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    owner: str


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency: hanya izinkan role 'admin'."""
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied",
        )
    return current_user


# ---------------------------------------------------------------------------
# AUTH Endpoints
# ---------------------------------------------------------------------------
@app.post("/register", status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register(user: UserRegister):
    """Registrasi pengguna baru."""
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if user.role not in ("admin", "user"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Role must be 'admin' or 'user'",
        )
    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hash_password(user.password),
        "role": user.role,
    }
    return {"message": "User registered successfully", "username": user.username, "role": user.role}


@app.post("/login", response_model=Token, tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login dan dapatkan JWT access token."""
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer"}


# ---------------------------------------------------------------------------
# TASK CRUD Endpoints
# ---------------------------------------------------------------------------
@app.get("/tasks", response_model=List[TaskOut], tags=["Tasks"])
def get_tasks(current_user: dict = Depends(get_current_user)):
    """Ambil semua tasks. Dapat diakses oleh 'admin' maupun 'user'."""
    return list(fake_tasks_db.values())


@app.get("/tasks/{task_id}", response_model=TaskOut, tags=["Tasks"])
def get_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Ambil task berdasarkan ID. Dapat diakses oleh 'admin' maupun 'user'."""
    task = fake_tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: TaskCreate, current_user: dict = Depends(require_admin)):
    """Buat task baru. Hanya bisa diakses oleh 'admin'."""
    global task_id_counter
    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description,
        "owner": current_user["username"],
    }
    fake_tasks_db[task_id_counter] = new_task
    task_id_counter += 1
    return new_task


@app.put("/tasks/{task_id}", response_model=TaskOut, tags=["Tasks"])
def update_task(task_id: int, task: TaskUpdate, current_user: dict = Depends(require_admin)):
    """Update task. Hanya bisa diakses oleh 'admin'."""
    existing = fake_tasks_db.get(task_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.title is not None:
        existing["title"] = task.title
    if task.description is not None:
        existing["description"] = task.description
    fake_tasks_db[task_id] = existing
    return existing


@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int, current_user: dict = Depends(require_admin)):
    """Hapus task. Hanya bisa diakses oleh 'admin'."""
    if task_id not in fake_tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    del fake_tasks_db[task_id]
    return {"message": f"Task {task_id} deleted successfully"}
