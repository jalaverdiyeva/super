# SuperChat 💬

Hey! This is my individual project submission for **SuperChat**, a unified conversational assistant combining Aviasales (flights), a Shopping Assistant (Birmarket e-commerce), and CinemaPlus (cinema) into a single chat window[cite: 3].

---

## 🚀 Project Overview
Instead of forcing users to switch between multiple apps, SuperChat allows users to talk about flights, products, and movies in any order within one chat interface[cite: 3]. The system automatically routes incoming messages to the correct domain, preserves session context, and reads data strictly from the official Phase 1 JSON mock dataset[cite: 4, 5, 14].

---

## 📂 Project Structure
Here is how my code files are organized:
- `app.py`: Main Streamlit web app handling the chat UI, message history state, and keyword routing.
- `repositories.py`: Data access layer containing `FlightRepository`, `ProductRepository`, and `CinemaRepository` classes that parse the local JSON files[cite: 14].
- `requirements.txt`: Contains project dependencies (`streamlit`)[cite: 11].
- `flights.json`, `products.json`, `movies.json`, `cinemas.json`, `showtimes.json`: The official mock dataset files[cite: 16].

---

## 🛠️ How to Run Locally

1. **Clone or download** this repository.
2. **Open your terminal** in the project directory and create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate



Install dependencies:

Bash
pip install -r requirements.txt
Run the Streamlit application using a single command:

Bash
streamlit run app.py
Open the local URL (http://localhost:8501) in your web browser.

💡 Example Test Queries
Flights: "Find a flight to Istanbul" or "Flights to Dubai"

Shopping: "Wireless Headphones", "Laptop 15 Pro", or "Smartphone X5"

Cinema: "Orbit Zero", "Smile 2", or "sci-fi movies"
