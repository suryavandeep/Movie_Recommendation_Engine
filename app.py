from flask import Flask,render_template,request,url_for,jsonify,redirect
import requests
import pandas as pd
import numpy as np
import pickle
import bz2
import _pickle as cPickle
import traceback

app=Flask(__name__)

@app.route("/",methods=['POST','GET'])
def imdb():
    return render_template('imdb.html')

@app.route("/movie_title", methods=['POST','GET'])
def movie_title():
    try:
        title=request.form['title']
        title=title.title()
        match_movies = movie_titles.loc[movie_titles.str.contains(title, case=False)]
        final_title=match_movies.iloc[0]
        index=int(movie_titles.index[movie_titles==final_title][0])
        return recommend(index)
    except:
        return str(traceback.format_exc())

def recommend(index):
    recommend_list=[]
    similarity_list=cosine_data[index]
    tupled_indexlist=list(enumerate(similarity_list))
    sorted_similarity_list=sorted(tupled_indexlist,key=lambda x:x[1],reverse=True)
    for i in sorted_similarity_list[0:10]:
        recommend_list.append(movie_titles[i[0]])
    recommend_list=np.array(recommend_list).reshape(10,1)
    return render_template('imdb.html',recommendations=recommend_list)

if __name__=="__main__":
    #loading the compressed pickle file using 'bz2' module
    pickle_data=bz2.BZ2File('compressed_cos_similarity.pkl','rb')
    cosine_data=cPickle.load(pickle_data)
    #loading the pickled file movie_index.pkl
    movie_titles=pickle.load(open('movie_index.pkl','rb'))
    app.run(debug=True)