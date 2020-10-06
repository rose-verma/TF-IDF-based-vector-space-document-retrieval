import math
import matplotlib.pyplot as plt

# reading data
ground_truth = 0
path = "E:\IIITD\Semester 2\IR\Assignments\Assignment 3\IR-assignment-3-data.txt"
file = open(path, "r").read().split("\n")[:-1]
data = []
c75 = []
for row in file:
    tmp = row.split(" ")[:-1]
    rel = int(tmp[0])
    qid = int(tmp[1].split(":")[1])
    if qid!=4:
        continue
    tmp = tmp[2:]
    dat = {}
    for val in tmp:
        val = val.split(":")
        val[0]=int(val[0])
        dat[val[0]]=float(val[1])
    data.append((rel, qid, dat))
    if rel>0:
        c75.append((1, dat[75]))
        ground_truth+=1
    else:
        c75.append((0, dat[75]))

print("Total URLs: ", len(data))

urls = []
for row in data:
    urls.append((row[0], row[2]))

#print(len(urls))
#print(urls[0])

size = len(urls)
sections = dict()
output = []
maximum = 0
for score in urls:
    sc = score[0] 
    if sc>maximum:
        maximum=sc
    if sc in sections:
        sections[sc].append(score[1])
    else:
        sections[sc]=[score[1]]

# finding total possible files
total = 1
for count in sections:
    total*=len(sections[count])
    
print("Total max dcg URL files possible: ", total)
print("Sample file: ")

# computing idcg and printing max dcg file
i = maximum
j = 0
idcg = 0
idcg_50 = 0
while i>=0:
    for row in sections[i]:
        print(j, row)
        j+=1
        den = math.log(j, 2)
        if den == 0:
            den = 1
        idcg+=i/den
        if j<=50:
            idcg_50+=i/den
    i-=1

print("-----------------------------------------------------------")

def findDCG(lis, lim=False):
    j = 0
    dcg = 0
    for row in lis:
        j+=1
        if lim==True and j==50:
            return dcg
        den = math.log(j, 2)
        if den == 0:
            den = 1
        dcg+=row[0]/den
    return dcg

ndcg_50 = findDCG(urls, lim=True)/idcg_50 
ndcg = findDCG(urls)/idcg
print("ndcg at 50: ",ndcg_50)
print("ndcg for whole dataset : ",ndcg)

c75 = sorted(c75, key=lambda x: x[1], reverse=True)
c75 = [val[0] for val in c75]

tpfp = 1
precision = []
recall = []
tp = 0
for i in c75:
    precision.append(tp/tpfp)
    recall.append(tp/ground_truth)
    if i == 1:
        tp += 1
    tpfp += 1

plt.xlabel('Precision')
plt.ylabel('Recall')
plt.title('Precision-Recall Curve')
plt.plot(recall, precision)
plt.show()
