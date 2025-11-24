import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import pickle
import warnings
warnings.filterwarnings("ignore")

print("📌 Loading dataset...")

books = pd.read_csv("../data/books.csv", low_memory=False, encoding="latin-1")
ratings = pd.read_csv("../data/ratings.csv", low_memory=False)
users = pd.read_csv("../data/users.csv", low_memory=False)

print("📌 Cleaning and filtering data...")

# Remove users who rated less than 100 books
valid_users = ratings['User-ID'].value_counts()
valid_users = valid_users[valid_users > 100].index
ratings = ratings[ratings['User-ID'].isin(valid_users)]

# Remove books with less than 50 ratings
valid_books = ratings['ISBN'].value_counts()
valid_books = valid_books[valid_books > 50].index
ratings = ratings[ratings['ISBN'].isin(valid_books)]

# Merge books & ratings
book_ratings = ratings.merge(books, on='ISBN')

# Create pivot table (now small)
print("📌 Creating pivot table...")
pivot = book_ratings.pivot_table(index="Book-Title", columns="User-ID", values="Book-Rating").fillna(0)

print("📌 Pivot shape:", pivot.shape)

# KNN model
print("📌 Training KNN model...")
model = NearestNeighbors(metric="cosine", algorithm="brute")
model.fit(pivot.values)

# Save model + index list
print("📌 Saving model...")
with open("model.pkl", "wb") as f:
    pickle.dump(
        {
            "model": model,
            "book_titles": list(pivot.index),
            "book_matrix": pivot.values
        },
        f
    )

print("🎉 Model training completed successfully!")
