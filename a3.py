# coding: utf-8

# # Assignment 3:  Recommendation systems
#
# Here we'll implement a content-based recommendation algorithm.
# It will use the list of genres for a movie as the content.
# The data come from the MovieLens project: http://grouplens.org/datasets/movielens/

# Please only use these imports.
from collections import Counter, defaultdict
import math
import numpy as np
import os
import pandas as pd
import re
from scipy.sparse import csr_matrix
import urllib.request
import zipfile

def download_data():
    """ DONE. Download and unzip data.
    """
    url = 'https://www.dropbox.com/s/h9ubx22ftdkyvd5/ml-latest-small.zip?dl=1'
    urllib.request.urlretrieve(url, 'ml-latest-small.zip')
    zfile = zipfile.ZipFile('ml-latest-small.zip')
    zfile.extractall()
    zfile.close()


def tokenize_string(my_string):
    """ DONE. You should use this in your tokenize function.
    """
    return re.findall('[\w\-]+', my_string.lower())


def tokenize(movies):
    """
    Append a new column to the movies DataFrame with header 'tokens'.
    This will contain a list of strings, one per token, extracted
    from the 'genre' field of each movie. Use the tokenize_string method above.
    Note: you may modify the movies parameter directly; no need to make
    a new copy.
    Params:
      movies...The movies DataFrame
    Returns:
      The movies DataFrame, augmented to include a new column called 'tokens'.
    >>> movies = pd.DataFrame([[123, 'Horror|Romance'], [456, 'Sci-Fi']], columns=['movieId', 'genres'])
    >>> movies = tokenize(movies)
    >>> movies['tokens'].tolist()
    [['horror', 'romance'], ['sci-fi']]
    """
    ###TODO
    pass
    t1 = []
    t2 = []
    for row in movies["genres"]:
        t1 = tokenize_string(row)
        t3 = []
        for t in t1:
            if (t not in t3):
                t3.append(t)
        t2.append(t3)
    movies["tokens"] = t2
    return movies

def featurize(movies):
    """
    Append a new column to the movies DataFrame with header 'features'.
    Each row will contain a csr_matrix of shape (1, num_features). Each
    entry in this matrix will contain the tf-idf value of the term, as
    defined in class:
    tfidf(i, d) := tf(i, d) / max_k tf(k, d) * log10(N/df(i))
    where:
    i is a term
    d is a document (movie)
    tf(i, d) is the frequency of term i in document d
    max_k tf(k, d) is the maximum frequency of any term in document d
    N is the number of documents (movies)
    df(i) is the number of unique documents containing term i
    Params:
      movies...The movies DataFrame
    Returns:
      A tuple containing:
      - The movies DataFrame, which has been modified to include a column named 'features'.
      - The vocab, a dict from term to int. Make sure the vocab is sorted alphabetically as in a2 (e.g., {'aardvark': 0, 'boy': 1, ...})
    """
    ###TODO
    pass
    v_set = set()
    film = {}
    temp_dict = defaultdict(int)
    # N
    film_num = movies.shape
    num_films = film_num[0]
    movies["features"] = ""

    for index, row in movies.iterrows():
        # movie ID --> (num_features,Counter(tokens))
        film[row["movieId"]] = (len(set(row["tokens"])), Counter(row["tokens"]), index)
        # Building Vocab
        for tok in row["tokens"]:
            temp_dict[tok] += 1
            v_set |= {tok}

    vocab = {}
    i = 0
    for t in sorted(v_set):
        vocab[t] = i
        i += 1

    for movie in sorted(film):
        # max_k = movie_dic[movie][1].most_common()
        max_k = film[movie][1].most_common(1)[0][1]
        data = []
        column = []
        # Improve here
        tup = film[movie]
        for term in tup[1]:
            tf_id = tup[1][term]
            df_i = temp_dict[term]
            tf_idf = (tf_id / max_k) * math.log((num_films / df_i), 10)
            data.append(tf_idf)
            column.append(vocab[term])
        rows = [0] * len(column)
        temp = csr_matrix((data, (rows, column)), shape=(1, len(vocab)))
        index = tup[2]
        movies.set_value(index=index, col="features", value=temp)

    return (movies, vocab)


def train_test_split(ratings):
    """DONE.
    Returns a random split of the ratings matrix into a training and testing set.
    """
    test = set(range(len(ratings))[::1000])
    train = sorted(set(range(len(ratings))) - test)
    test = sorted(test)
    return ratings.iloc[train], ratings.iloc[test]


def cosine_sim(a, b):
    """
    Compute the cosine similarity between two 1-d csr_matrices.
    Each matrix represents the tf-idf feature vector of a movie.
    Params:
      a...A csr_matrix with shape (1, number_features)
      b...A csr_matrix with shape (1, number_features)
    Returns:
      The cosine similarity, defined as: dot(a, b) / ||a|| * ||b||
      where ||a|| indicates the Euclidean norm (aka L2 norm) of vector a.
    """
    ###TODO
    pass

    num = np.dot(a.toarray(),b.toarray().T)
    norm_ab =np.linalg.norm(a.toarray()) * np.linalg.norm(b.toarray())
    return num[0][0]/norm_ab



def make_predictions(movies, ratings_train, ratings_test):
    """
    Using the ratings in ratings_train, predict the ratings for each
    row in ratings_test.
    To predict the rating of user u for movie i: Compute the weighted average
    rating for every other movie that u has rated.  Restrict this weighted
    average to movies that have a positive cosine similarity with movie
    i. The weight for movie m corresponds to the cosine similarity between m
    and i.
    If there are no other movies with positive cosine similarity to use in the
    prediction, use the mean rating of the target user in ratings_train as the
    prediction.
    Params:
      movies..........The movies DataFrame.
      ratings_train...The subset of ratings used for making predictions. These are the "historical" data.
      ratings_test....The subset of ratings that need to predicted. These are the "future" data.
    Returns:
      A numpy array containing one predicted rating for each element of ratings_test.
    """
    ###TODO
    pass

    # Index(['userId', 'movieId', 'rating', 'timestamp'], dtype='object')
    ratings_test_copy = ratings_test.copy(deep=True)

    ud = defaultdict(list)
    md = defaultdict(list)

    for index,row in ratings_train.iterrows():
        ud[row["userId"]].append((row["movieId"],row["rating"]))
        md[row["userId"]].append(row["rating"])

    #mean rating for userId
    for user in md:
        md[user] = sum(md[user])/len(md[user])

    for index,row in ratings_test.iterrows():
        mov_rated_x = ud[row["userId"]]
        norm_sum = 0.0
        r_temp = movies.loc[movies["movieId"] == row["movieId"],"features"].iloc[0]
        # print(r_temp)
        va = r_temp
        s = 0.0
        weighted_avg = 0.0
        count_pos = 0
        for mov in mov_rated_x:
            # row containing this movie in movies df
            row_mov_movies = movies.loc[movies["movieId"] == mov[0],"features"].iloc[0]
            # print(row_mov_movies)
            vb = row_mov_movies
            s_a_b = cosine_sim(va,vb)
            if(s_a_b >0):
                s += s_a_b * mov[1]
                norm_sum += s_a_b
                count_pos +=1
        if(count_pos >0):
            w = s/norm_sum
        elif(count_pos==0):
            w = md[row["userId"]]

        # print(weighted_avg)
        ratings_test_copy.set_value(index=index,col="rating",value=w)

    ex = ratings_test_copy["rating"].values

    return ex

def mean_absolute_error(predictions, ratings_test):
    """DONE.
    Return the mean absolute error of the predictions.
    """

    return np.abs(predictions - np.array(ratings_test.rating)).mean()


def main():
    download_data()
    path = 'ml-latest-small'
    ratings = pd.read_csv(path + os.path.sep + 'ratings.csv')
    movies = pd.read_csv(path + os.path.sep + 'movies.csv')
    movies = tokenize(movies)
    movies, vocab = featurize(movies)
    print('vocab:')
    print(sorted(vocab.items())[:10])
    ratings_train, ratings_test = train_test_split(ratings)
    print('%d training ratings; %d testing ratings' % (len(ratings_train), len(ratings_test)))
    predictions = make_predictions(movies, ratings_train, ratings_test)
    print('error=%f' % mean_absolute_error(predictions, ratings_test))
    print(predictions[:10])


if __name__ == '__main__':
    main()