# 📚 Book Recommendation System

A simple and efficient web application that recommends books based on user input.  
Built with **Flask (Python)** and a clean **HTML/CSS/JS** frontend.  
Live Demo → **https://book-recommendation-system-ptbh.onrender.com**

---

## 🚀 Features
- Enter any book name and get similar book recommendations  
- Displays:
  - Book title  
  - Cover image  
  - Average rating  
  - Quick Google search link  
- Frontend + Backend deployed together on Render (single URL)

---

## 🛠 Tech Stack
- **Backend:** Flask, Pandas, NumPy  
- **Model:** Pickle (trained recommendation model)  
- **Frontend:** HTML, CSS, JavaScript  
- **Deployment:** Render Web Service  

---

## 📂 Project Structure
backend/
app.py
frontend/
index.html
script.js
styles.css
model/
model.pkl
data/
requirements.txt
.gitignore
README.md

---

## ▶️ Running Locally

### 1. Clone the Repository

git clone https://github.com/sowmiyasoundar/Book_Recommendation_System.git
cd Book_Recommendation_System

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Start the Server
python backend/app.py
Now open: http://127.0.0.1:5000

## Deployment (Render)
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app

The app automatically serves the frontend and backend on the same domain.

## How It Works
User enters a book name

Flask backend loads the trained model and book data

Model finds similar books

Frontend displays results with images and ratings

## Contact
Maintained by Sowmiyasoundar
GitHub: https://github.com/sowmiyasoundar
