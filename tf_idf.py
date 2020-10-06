import os
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import math
import string

#path = 'E:\IIITD\Semester 2\IR\Assignments\Assignment 3\\20_newsgroups\\'
path = 'E:\IIITD\Semester 2\IR\Assignments\Assignment 3\\test\\'
r_path = 'E:\IIITD\Semester 2\IR\Assignments\Assignment 3\\file.txt'
           
corpus = []
# loading data, tokenization 
r_index = 1
reviews = open(r_path, "r").read().split('\n')
temp = []
for review in reviews:
    if review != '':
        temp.append(review.split(' ')[1])
reviews = temp
max_score = 0
for folder in os.listdir(path):
    folder_path = path+folder
    print(folder_path)
    for filename in os.listdir(folder_path):
        cur_path = folder_path+"\\"+filename
        file  = open(cur_path, "r")
        dat = file.read().lower()
        body = word_tokenize(dat)
        auth_score = int(reviews[r_index-1])
        if auth_score>max_score:
            max_score = auth_score
        corpus.append([folder+'/'+filename, body, auth_score])
        r_index += 1
print("Number of documents: ", len(corpus))
print("Data loaded and tokenized")

# lemmatization, punctuation removal and stop word removal
res = []
doc_scores = {}
puncts = set(string.punctuation)
puncts.update(['`','.','',"''",'""','--','``'])
stop_words=set(stopwords.words("english"))
lem = WordNetLemmatizer()
for i in range(len(corpus)):
    temp = []
    for j in range(len(corpus[i][1])):
        word = corpus[i][1][j]
        if word not in stop_words:
            tokens = re.split(r'\s+|[,;.@:-]\s*', word)
            temp_str = ""
            for t in tokens:
                if t not in puncts:
                    temp_str = lem.lemmatize(t)
                    temp.append(temp_str)
            if temp_str != word and temp_str not in puncts:
                temp.append(lem.lemmatize(word))
    res.append([corpus[i][0], temp, corpus[i][2]/max_score])
    doc_scores[corpus[i][0]] = corpus[i][2]/max_score
corpus = res
print("Lemmatized")

# counting frequencies
doc_maxes = dict()
max_tfs = dict()
for i in range(len(corpus)):
    unique = {}
    max_freq = 1
    max_tfs[corpus[i][0]] = 0
    for word in corpus[i][1]:
        if word in unique:
            unique[word]+=1
        else:
            unique[word]=1
        if max_freq<unique[word]:
            max_freq=unique[word]
    corpus[i][1] = unique
    doc_maxes[corpus[i][0]] = max_freq

#creating word base
word_base = set()
for i in range(len(corpus)): 
    word_base |= set(corpus[i][1])
print("Unique words found: ", len(word_base))

# counting termwise tfs and idfs
tf_scores = {}
idf_scores = {}
num_docs = len(corpus)
for term in word_base:
    df = 0
    for doc in corpus:
        flag = False
        if term in doc[1]:
            tf= doc[1][term]
            flag = True
        if flag:
            n_tf_score = tf/len(doc[1])
            tf_score = 1+math.log(tf, 10)
            if tf_score > max_tfs[doc[0]]:
                max_tfs[doc[0]] = tf_score
            tf_scores[(doc[0], term)] = tf_score
            if term in doc[1]:
                df+= 1
            idf_scores[term] = math.log(num_docs/1+df,10)
            #corpus[i][2] = tf_score + math.log(corpus[i][2]/max_score + 1, 10)
print("TFs Counted")

# building inverted index
inverted_index = dict()
for lis in corpus:
    for word in lis[1]:
        score = (lis[2]+(tf_scores[(lis[0], word)]/max_tfs[lis[0]])*idf_scores[word])/2
        if word in inverted_index:
            inverted_index[word][lis[0]]=score
        else:
            inverted_index[word] = {lis[0]:score}
            #inverted_index[word] = [1 , {(lis[2], lis[0])}]
print("Posting Lists Built")

# sorting inverted index
sorted_postings = {}
for term in inverted_index:
    lis = sorted(inverted_index[term].items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    sorted_postings[term] = lis
print("Posting Lists Sorted")

temp = {}
for corp in corpus:
    temp[corp[0]] = corp[1]
corpus = temp

r = 10
champion_lists = dict()
low_lists = dict()
for term in sorted_postings:
    champion_lists[term] = sorted_postings[term][:r]
    low_lists[term] = sorted_postings[term][r:]

#print(len(champion_lists["end"]),champion_lists["end"])
#print(len(low_lists["end"]),low_lists["end"])

while True:
    
    query = input("Enter Query\n")
    if query=="exit":
        break
    query = query.lower()
    for c in string.punctuation:
        query = query.replace(c," ")
    query = word_tokenize(query)
    temp=[]
    for word in query:
        if word not in stop_words:
            temp.append(lem.lemmatize(word))
    query = temp
    print(query)
    
    k = int(input("Enter K\n"))
    
    # computing cosine values
    cosines = {}
    q_scores = {}
    for term in query:
        if term in idf_scores:
            idf = math.log(num_docs/1+idf_scores[term],10)
            tf_idf = idf/len(query)
            q_scores[term] = tf_idf
    
    candidates = set()
    for term in query:
        if term in champion_lists.keys():
            docs = [tups[0] for tups in champion_lists[term]]
            if len(docs) > k:
                docs = docs[:k]
            else:
                docs = docs[:r]
                lows = [tups[0] for tups in low_lists[term]]
                lows = lows[:k-r]
                docs.extend(lows)
            candidates |= set(docs)
    print("Candidates:", candidates)
            
    for doc in candidates:
        num = 0
        den1 = 0
        den2 = 0
        for term in query:
            flag = False
            if term in corpus[doc]:
                num+=q_scores[term]*tf_scores[(doc,term)]/max_tfs[doc]
                #num+=q_scores[term]*inverted_index[term][doc]
                flag = True
            if flag:
                den2+=q_scores[term]**2
        for term in corpus[doc]:
            #den1 += inverted_index[term][doc]**2
            den1 += tf_scores[(doc,term)]/max_tfs[doc]**2
        if den1 == 0 or den2 ==0:
            cos = 0
        else:
            cos = num/(math.sqrt(den1)*math.sqrt(den2)) 
        cosines[doc]=cos
    
    #for doc in cosines:
    #    cosines[doc] = cosines[doc]+doc_scores[doc]
    cosines = sorted(cosines.items(), key = lambda value:(value[1], value[0]), reverse=True)[:k]
    print("\nCosine Similarity based results:\n",[x[0] for x in cosines])            
    