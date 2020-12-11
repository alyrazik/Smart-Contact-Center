import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from gensim import matutils
import scipy.sparse

def model_from_text(col):
    """ 
    :param 
    col a series of text. Typically a column in pandas dataframe.
    :return: 
    corpus is the term-document matrix in the gensim format
    id2word is dictionary of the all terms and their respective location in the term-document matrix
    """
    cv = CountVectorizer(max_df=0.1)  # for topic modeling.
    # Create document term matrix
    data_cv = cv.fit_transform(col)
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_dtm.reset_index()
    tdm = data_dtm.transpose()
    sparse_counts = scipy.sparse.csr_matrix(tdm)
    corpus = matutils.Sparse2Corpus(sparse_counts)
    id2word = dict((v, k) for k, v in cv.vocabulary_.items())
    return corpus, id2word