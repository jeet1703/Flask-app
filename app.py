from flask import Flask, render_template, request
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error

warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the data
df = pd.read_csv('path_to_your_file.csv', header=None)
df.columns = ['user_id', 'prod_id', 'rating', 'timestamp']
df = df.drop('timestamp', axis=1)
df_copy = df.copy(deep=True)

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the recommendation logic
@app.route('/recommend', methods=['POST'])
def recommend():
    # Perform analysis and recommendation logic here
    
    # Finding unique users and products
    unique_users = df['user_id'].nunique()
    unique_products = df['prod_id'].nunique()

    # Top 10 users based on rating
    most_rated = df.groupby('user_id').size().sort_values(ascending=False)[:10]
    
    # Filter users who have given 50 or more ratings
    counts = df['user_id'].value_counts()
    df_final = df[df['user_id'].isin(counts[counts >= 50].index)]
    
    # Create interaction matrix
    final_ratings_matrix = df_final.pivot(index='user_id', columns='prod_id', values='rating').fillna(0)
    given_num_of_ratings = np.count_nonzero(final_ratings_matrix)
    possible_num_of_ratings = final_ratings_matrix.shape[0] * final_ratings_matrix.shape[1]
    
    # Calculate the density of ratings
    density = (given_num_of_ratings / possible_num_of_ratings) * 100
    
    # Calculate average and count of ratings for each product
    average_rating = df_final.groupby('prod_id')['rating'].mean()
    count_rating = df_final.groupby('prod_id')['rating'].count()
    final_rating = pd.DataFrame({'avg_rating': average_rating, 'rating_count': count_rating})
    
    # Sort products based on average ratings and filter for top n
    final_rating = final_rating.sort_values(by='avg_rating', ascending=False)
    
    def top_n_products(final_rating, n, min_interaction):
        recommendations = final_rating[final_rating['rating_count'] > min_interaction]
        recommendations = recommendations.sort_values('avg_rating', ascending=False)
        return recommendations.index[:n]
    
    # Get top 5 products with at least 50 interactions
    top_products = list(top_n_products(final_rating, 5, 50))
    
    return render_template('result.html', 
                            unique_users=unique_users, 
                            unique_products=unique_products, 
                            density=density, 
                            top_products=top_products)

if __name__ == '__main__':
    app.run(debug=True)
