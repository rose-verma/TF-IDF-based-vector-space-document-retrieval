# TF-IDF-based-vector-space-document-retrieval


IIITD IR Course Assignment:

Download http://archives.textfiles.com/stories.zip dataset

Implement a CLI tool for:
1. Jaccard Coefficient based document retrieval: For each query, your system will output
top k documents based on jaccard score.
2. Tf-Idf based document retrieval: For each query, your system will output top k
documents based on tf-idf-matching-score. Implement different versions of Tf-Idf based
document retrieval then compare and analyze which performs better and why.
3. Tf-Idf based vector space document retrieval: For each query, your system will output
top k documents based on a cosine similarity between query and document vector.

In addition, ensure that numerical queries work. Example “100 animals”, “50,000 variety of
flowers”, “population of 1 billion” etc.

Give special attention to the terms in the document title and analyze the change in result with
and without attention to terms in title.

Compare and state pros and cons for all the techniques.

Separately,

Download the dictionary from http://www.gwicks.net/dictionaries.htm (UK ENGLISH - 65,000 words)

Take a sentence as input from user. For each non dictionary words present in the sentence
suggest top k words on the basis of minimum edit distance. Cost of operations is defined as:

Insert: 2
Delete: 1
Replace: 3