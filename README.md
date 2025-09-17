# 🎬 Cinema Seat Reservation System

A Python-based cinema seat booking system with a **FastAPI backend** and a **Streamlit frontend**.  
Users can browse movies, view available seats, and make reservations in real-time.

---

## 🚀 Features
- FastAPI backend for movie and seat management.
- RESTful APIs for seat reservations.
- Streamlit-based user interface for easy seat booking.
- Seat status updates (reserved / available).
- Unique reservation IDs for each booking.

---

## 🛠️ Tech Stack
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Data Models:** Pydantic
- **API Communication:** Requests

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cinema-seat-reservation.git
   cd cinema-seat-reservation
2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
3. Install dependencies:
pip install -r requirements.txt
4. ▶️ Usage
Start the FastAPI backend:
uvicorn main:app --reload
The API will be available at: http://127.0.0.1:8000
5. Run the Streamlit frontend:
streamlit run gui.py
6. Access the UI at: http://localhost:8501
7. 📖 API Endpoints
GET /movies → Get list of movies
GET /movies/{movie_id}/seats → Get seats for a movie
POST /movies/{movie_id}/reserve → Reserve a seat
8. 📜 License
This project is licensed under the MIT License – feel free to use and modify.
9. 👤 Author
Developed by Zeerak Khan
