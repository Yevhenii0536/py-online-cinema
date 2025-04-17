from pydantic import BaseModel


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
    email: str


class UserCreate(BaseModel):
    password: str


class UserRead(BaseModel):
    id: int

    class Config:
        from_attributes = True