SuperChat - Unified Conversational Assistant 💬✈️🛒🎬

SuperChat is a single chat assistant that brings together three different services: Aviasales (flights), Birmarket (shopping), and CinemaPlus (movie tickets).

Instead of opening three different apps or switching between different tabs, you can just ask everything in one chat window. The assistant figures out what you are asking for and gets the right data automatically.

💡 What This Project Does

Single Chat Window: You don't need to select a mode or click switches. Just type what you need.

Smart Intent Routing: Automatically detects whether your message is about booking a flight, buying a product, or checking cinema showtimes.

Clean Repository Layer: All local JSON data access is cleanly isolated inside repositories.py (ProductRepository, CinemaRepository, FlightRepository). This makes it super easy to swap local mock data with real REST APIs in Phase 2.

Strict Dataset Adherence: Only uses official entries from the local mock JSON datasets without hallucinating fake items or prices.

Multilingual UI & Multimodal Layout: Basic sidebar support for language context and voice/image search uploads.

📁 Project Structure

super/
├── app.py              # Main Streamlit UI and chat routing logic
├── repositories.py     # Clean data access layer loading JSON files
├── requirements.txt    # Project dependencies
├── flights.json        # Official mock flight dataset
├── products.json       # Official mock shopping dataset
├── movies.json         # Official mock movie list
├── cinemas.json        # Official mock cinema venues
└── showtimes.json      # Official mock movie showtimes


🚀 How to Run the App

Prerequisites

Make sure you have Python 3.10+ installed on your computer.

Quick Start (Single Command Setup)

Clone the repository:

git clone https://github.com/your-username/super.git
cd super


Install the required package:

pip install -r requirements.txt


Launch the app:

streamlit run app.py


The application will automatically open in your browser at http://localhost:8501.

🧪 Testing Sample Queries

You can try typing any of these directly into the chat:

Shopping: "Show me laptops" or "Do you have wireless headphones?"

Flights: "Flights to Istanbul" or "Find me a flight to Moscow"

Cinema: "What is playing tonight?" or "Show me Orbit Zero"

🛠️ Built With

Python 3.11

Streamlit

Python standard libraries (json, urllib.parse)
