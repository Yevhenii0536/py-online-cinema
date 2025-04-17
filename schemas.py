from pydantic import BaseModel, EmailStr


class MovieBase(BaseModel):
    title: str
    genre: str
    price: float


class FilmCreate(MovieBase):
    pass


class FilmRead(MovieBase):
    id: int

    class Config:
        from_attributes = True


class FilmUpdate(MovieBase):
    pass


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str