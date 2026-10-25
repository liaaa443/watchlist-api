from pydantic import BaseModel, Field, field_validator

class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=50)
    release_year: int = Field(ge=1888, le=2100)
    rating: float = Field(ge=0, le=10)
    is_favorite: bool = True

    @field_validator("title", "genre")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field tidak boleh hanya berisi spasi")
        return value.strip()


class MovieUpdate(MovieCreate):
    pass


class MovieResponse(MovieCreate):
    id: int
