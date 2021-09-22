# Movie_Recommendation_Engine
#### Movie_Recommendation_Engine based on the IMDB Movies Dataset

##### This IMDB Dataset contains the following columns having respective values for each movie in the dataset: 'index', 'budget', 'genres', 'homepage', 'id', 'keywords','original_language', 'original_title', 'overview', 'popularity', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title', 'vote_average', 'vote_count', 'cast', 'crew', 'director'.

##### I combined some main columns into a single feature. And than used that sinle Feature to find the similarity scores for all the movies.

##### In this project I used the CountVectorizer() method from "sklearn.feature_extraction.text" module. This method returns the sparse type of matrix with 'm' number of rows and 'n' number of columns, which shows the number of occurences of each unique word(present in complete dataset) in each row.
##### After getting the parse matrix from the CountVectorizer() method, I passesd that matrix to the 'cosine_similarity' method of sklearn, this method gives the similarity score of data in each row with all the other rows, by this we get the similarity score of each unique movie with every other movie.
