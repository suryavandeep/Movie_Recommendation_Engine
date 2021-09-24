from flask import Flask,render_template,request,url_for,jsonify,redirect
import requests
import pandas as pd
import numpy as np
import pickle
import bz2
import _pickle as cPickle
import urllib.request,json

#loading the compressed pickle file using 'bz2' module
pickle_data=bz2.BZ2File('compressed_cos_similarity.pkl','rb')
cosine_data=cPickle.load(pickle_data)
#loading the pickled file movie_index.pkl
movie_titles=pickle.load(open('id_title.pkl','rb'))

app=Flask(__name__)

@app.route("/",methods=['POST','GET'])
def imdb():
    return render_template('imdb.html')

@app.route("/movie_title", methods=['POST','GET'])
def movie_title():
    check='none'
    if request.form:
        try:
            title=request.form['title']
            title=title.title()
            match_movies = movie_titles['title'].loc[movie_titles['title'].str.contains(title, case=False)]
            final_title=match_movies.iloc[0]
            index=int(movie_titles['title'].index[movie_titles['title']==final_title][0])
            return recommend(index,title)
        except:
            error_message="Invalid Input, please check and type the correct title of movie"
            check='fail'
            return render_template('imdb.html',message=error_message,check=check)
    else:
        return redirect(url_for('/'))

def recommend(index,title):
    recommend_list=[]
    recommend_id_list=[]
    similarity_list=cosine_data[index]
    tupled_indexlist=list(enumerate(similarity_list))
    sorted_similarity_list=sorted(tupled_indexlist,key=lambda x:x[1],reverse=True)
    for i in sorted_similarity_list[0:10]:
        recommend_list.append(movie_titles['title'][i[0]])
        recommend_id_list.append(movie_titles['id'][i[0]])
    poster_paths=get_poster_path(recommend_id_list)
    check='pass'
    return render_template('imdb.html',recommendations=recommend_list,movie=title,check=check,poster_list=poster_paths,zip=zip)

def get_poster_path(id_list):
    api_key='c1e9f7b4e89d8bd40d73382d0ef6e99a'
    list=id_list
    response_data=[]
    for i in list:
        search_url=f'https://api.themoviedb.org/3/movie/{i}?api_key={api_key}'
        try:
            title_response=urllib.request.urlopen(search_url)
            title_data=title_response.read()
            title_json=json.loads(title_data)
            if "poster_path" in title_json:
                response_data.append(title_json['poster_path'])
        except:
            response_data.append("Image not Available on Server")
    return response_data

if __name__=="__main__":
    app.run(debug=True)