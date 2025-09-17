import streamlit as st
import requests
from uuid import UUID

API_URL = "http://localhost:8000" 

st.title("Cinema Seat Reservation System")

def get_movies():
    return requests.get(f"{API_URL}/movies").json()

def get_seats(movie_id):
    return requests.get(f"{API_URL}/movies/{movie_id}/seats").json()

def reserve_seat(movie_id, row, number, user_name):
    payload = {
        "row": row,
        "number": number,
        "user_name": user_name
    }
    return requests.post(f"{API_URL}/movies/{movie_id}/reserve", json=payload).json()

def get_reservations():
    return requests.get(f"{API_URL}/reservations").json()

def get_reservation_by_id(reservation_id):
    return requests.get(f"{API_URL}/reservations/{reservation_id}").json()

def cancel_reservation(reservation_id):
    return requests.delete(f"{API_URL}/reservations/{reservation_id}").json()

def add_movie(movie_id, title, duration_minutes):
    payload = {
        "id": movie_id,
        "title": title,
        "duration_minutes": duration_minutes
    }
    return requests.post(f"{API_URL}/movies", json=payload).json()
menu = st.sidebar.radio("Menu", [
    "Reserve Seat", 
    "View All Reservations", 
    "Search Reservation", 
    "Cancel Reservation", 
    "Add Movie"
])

if menu == "Reserve Seat":
    st.header("Reserve a Seat")

    movies = get_movies()
    if not movies or "detail" in movies:
        st.warning("No movies available. Please add movies to the backend first.")
    else:
        movie = st.selectbox("Select Movie", movies, format_func=lambda m: f"{m['title']} ({m['duration_minutes']} min)")
        user_name = st.text_input("Your Name")
        row = st.number_input("Row (1-5)", min_value=1, max_value=5)
        number = st.number_input("Seat Number (1-10)", min_value=1, max_value=10)

        if st.button("Reserve"):
            if not user_name.strip():
                st.error("Please enter your name.")
            else:
                res = reserve_seat(movie_id=movie["id"], row=row, number=number, user_name=user_name)
                if "reservation_id" in res:
                    st.success(f"Reservation successful! Reservation ID: {res['reservation_id']}")
                else:
                    st.error(f"{res.get('detail', 'Reservation failed')}")
elif menu == "View All Reservations":
    st.header("All Reservations")
    reservations = get_reservations()
    if not reservations:
        st.info("No reservations found.")
    else:
        for r in reservations:
            st.markdown(f"""
                - Reservation ID:`{r['id']}`
                - Movie:`{r['movie_title']}`
                - Seat:Row `{r['row']}`, Number `{r['number']}`
                - Reserved By:`{r['user_name']}`
                ---
            """)
elif menu == "Search Reservation":
    st.header("Search Reservation by ID")
    input_id = st.text_input("Enter Reservation ID")

    if st.button("Search"):
        try:
            uuid_obj = UUID(input_id, version=4)
            res = get_reservation_by_id(uuid_obj)
            st.success(" Reservation Found:")
            st.json(res)
        except ValueError:
            st.error("Invalid UUID format.")
        except Exception:
            st.error(" Reservation not found.")

elif menu == "Cancel Reservation":
    st.header("Cancel Reservation")
    input_id = st.text_input("Enter Reservation ID to Cancel")

    if st.button("Cancel Reservation"):
        try:
            uuid_obj = UUID(input_id, version=4)
            res = cancel_reservation(uuid_obj)
            if "message" in res:
                st.success(res["message"])
            else:
                st.error(res.get("detail", "Unknown error"))
        except ValueError:
            st.error(" Invalid UUID format.")
        except Exception:
            st.error(" Reservation not found or already cancelled.")
elif menu == "Add Movie":
    st.header("Add a New Movie")

    movie_id = st.number_input(" Movie ID", min_value=1, step=1)
    title = st.text_input(" Title")
    duration = st.number_input(" Duration (in minutes)", min_value=1, step=1)

    if st.button("Add Movie"):
        if not title.strip():
            st.error(" Please enter a title for the movie.")
        else:
            response = add_movie(movie_id, title.strip(), duration)
            if "movie_id" in response:
                st.success(f" Movie '{title}' added successfully!")
            else:
                st.error(response.get("detail", " Failed to add movie."))
