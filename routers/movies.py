from fastapi import APIRouter, Depends, HTTPException, Response, status

from dependencies.auth import verify_api_key
from schemas.movie import MovieCreate, MovieResponse, MovieUpdate
from services import movie_service

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("", response_model=list[MovieResponse])
def list_movies():
    return movie_service.get_all_movies()


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int):
    try:
        return movie_service.get_movie(movie_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404, detail=str(exc).strip("'")
        ) from exc


@router.post(
    "",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(data: MovieCreate):
    return movie_service.create_movie(data)


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, data: MovieUpdate):
    try:
        return movie_service.update_movie(movie_id, data)
    except KeyError as exc:
        raise HTTPException(
            status_code=404, detail=str(exc).strip("'")
        ) from exc


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):
    try:
        movie_service.delete_movie(movie_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404, detail=str(exc).strip("'")
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
