from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load KNN model
with open("../model/model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]
book_titles = data["book_titles"]
book_matrix = data["book_matrix"]

# Load books & ratings datasets
books_df = pd.read_csv("../data/books.csv", low_memory=False, encoding="latin-1")
ratings_df = pd.read_csv("../data/ratings.csv", low_memory=False)

# Calculate average rating per book
avg_ratings = ratings_df.groupby("ISBN")["Book-Rating"].mean().to_dict()
title_to_isbn = dict(zip(books_df["Book-Title"], books_df["ISBN"]))

@app.route("/recommend", methods=["GET"])
def recommend():
    query = request.args.get("book", "").strip()
    if not query:
        return jsonify({"error": "No book provided"}), 400

    # Case-insensitive substring search in book titles
    matches = [title for title in book_titles if query.lower() in title.lower()]

    if matches:
        book_name = matches[0]
        index = book_titles.index(book_name)
        distances, indices = model.kneighbors([book_matrix[index]], n_neighbors=6)
        recommended_titles = [book_titles[i] for i in indices[0][1:]]  # skip input book

        recommendations = []
        for title in recommended_titles:
            isbn = title_to_isbn.get(title, "")
            image_url = (
                f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
                if isbn else "https://via.placeholder.com/120x180.png?text=No+Image"
            )
            rating = round(avg_ratings.get(isbn, 0), 1) if isbn else 0
            google_link = f"https://www.google.com/search?q={title.replace(' ', '+')}"
            recommendations.append({
                "title": title,
                "image": image_url,
                "rating": rating,
                "link": google_link
            })
    else:
        # Book not found → show user input only
        book_name = query
        recommendations = [{
            "title": query,
            "image": "https://via.placeholder.com/120x180.png?text=No+Image",
            "rating": 0,
            "link": f"https://www.google.com/search?q={query.replace(' ', '+')}"
        }]

    return jsonify({
        "input_book": book_name,
        "recommendations": recommendations
    })


@app.route("/")
def home():
    return jsonify({"message": "Book Recommender API running!"})

if __name__ == "__main__":
    app.run(debug=True)
