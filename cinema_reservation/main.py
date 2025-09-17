from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Tuple, Optional
from uuid import uuid4, UUID

app = FastAPI(title="Zeerak Cinema Seat Reservation System")

class Movie(BaseModel):
    id: int
    title: str
    duration_minutes: int

class Seat(BaseModel):
    row: int
    number: int
    is_reserved: bool = False
    reserved_by: Optional[str] = None
    reservation_id: Optional[UUID] = None

class ReserveRequest(BaseModel):
    row: int
    number: int
    user_name: str

class Reservation(BaseModel):
    id: UUID
    movie_id: int
    movie_title: str
    row: int
    number: int
    user_name: str

ROWS = 5
SEATS_PER_ROW = 10

movies: Dict[int, Movie] = {}
movie_seats: Dict[int, Dict[Tuple[int, int], Seat]] = {}
reservations: Dict[UUID, Reservation] = {}

def create_seat_layout() -> Dict[Tuple[int, int], Seat]:
    return {
        (row, num): Seat(row=row, number=num)
        for row in range(1, ROWS + 1)
        for num in range(1, SEATS_PER_ROW + 1)
    }

def validate_seat_coordinates(row: int, number: int):
    if row < 1 or row > ROWS or number < 1 or number > SEATS_PER_ROW:
        raise HTTPException(status_code=400, detail="Invalid seat coordinates")

@app.get("/")
def root():
    return {"message": "Welcome to the Cinema Seat Reservation System"}
@app.post("/movies", status_code=201)
def create_movie(movie: Movie):
    if movie.id in movies:
        raise HTTPException(status_code=400, detail="Movie ID already exists")
    movies[movie.id] = movie
    movie_seats[movie.id] = create_seat_layout()
    return {"message": f"Movie '{movie.title}' added successfully", "movie_id": movie.id}

@app.get("/movies", response_model=List[Movie])
def list_movies():
    return list(movies.values())

@app.get("/movies/{movie_id}/seats", response_model=List[Seat])
def get_seats_for_movie(movie_id: int):
    if movie_id not in movie_seats:
        raise HTTPException(status_code=404, detail="Movie not found")
    return list(movie_seats[movie_id].values())

@app.get("/movies/{movie_id}/seats/{row}/{number}", response_model=Seat)
def check_seat_status(movie_id: int, row: int, number: int):
    if movie_id not in movie_seats:
        raise HTTPException(status_code=404, detail="Movie not found")
    validate_seat_coordinates(row, number)
    key = (row, number)
    seats = movie_seats[movie_id]
    if key not in seats:
        raise HTTPException(status_code=404, detail="Seat not found")
    return seats[key]
@app.post("/movies/{movie_id}/reserve", status_code=201)
def reserve_seat_for_movie(movie_id: int, request: ReserveRequest):
    if movie_id not in movie_seats:
        raise HTTPException(status_code=404, detail="Movie not found")

    validate_seat_coordinates(request.row, request.number)
    key = (request.row, request.number)
    seats = movie_seats[movie_id]

    if seats[key].is_reserved:
        raise HTTPException(status_code=400, detail="Seat already reserved")
    reservation_id = uuid4()
    seats[key].is_reserved = True
    seats[key].reserved_by = request.user_name
    seats[key].reservation_id = reservation_id

    reservation = Reservation(
        id=reservation_id,
        movie_id=movie_id,
        movie_title=movies[movie_id].title,
        row=request.row,
        number=request.number,
        user_name=request.user_name
    )
    reservations[reservation_id] = reservation

    return {
        "message": f"Seat {request.row}-{request.number} reserved by {request.user_name} for '{movies[movie_id].title}'",
        "reservation_id": reservation_id
    }

@app.get("/reservations", response_model=List[Reservation])
def get_all_reservations():
    return list(reservations.values())

@app.get("/reservations/{reservation_id}", response_model=Reservation)
def get_reservation_by_id(reservation_id: UUID):
    if reservation_id not in reservations:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservations[reservation_id]

@app.delete("/reservations/{reservation_id}")
def cancel_reservation(reservation_id: UUID):
    if reservation_id not in reservations:
        raise HTTPException(status_code=404, detail="Reservation not found")

    reservation = reservations.pop(reservation_id)
    key = (reservation.row, reservation.number)
    seats = movie_seats[reservation.movie_id]

    if key in seats:
        seats[key].is_reserved = False
        seats[key].reserved_by = None
        seats[key].reservation_id = None

    return {"message": f"Reservation {reservation_id} cancelled successfully."}
