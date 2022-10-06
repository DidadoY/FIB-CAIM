import matplotlib.pyplot as plt
import math
import os
from scipy.optimize import curve_fit

def read_file(fileName):
    f = open(fileName, "r")
    return f

def read_words(f):
    words = {""}
    total_words = 0
    currentWord = ''
    for line in f:
        for w in line:
            if((w >= 'A' and w < 'Z') or (w >= 'a' and w <= 'z')):
                currentWord += w
            else:
                if currentWord != '' and currentWord.isalpha():
                    words.add(currentWord)
                    total_words += 1
                    currentWord = ''
    return words, total_words

def obtain_all_words(ndocs):
	pth = "../documents/novels/"

	content = os.listdir(pth)

	words = {""}
	total_words = 0
	for c in content[:-ndocs]:
		file = read_file(pth+c)
		d,tot = read_words(file)
		total_words += tot
		words = words.union(d)
	
	return words, total_words

heapLaw = lambda N, k, beta : k*(N**beta)
logMath = lambda x : math.log(x,10)

ndocs = [1,13, 18, 27, 30, 32]

x = []
y = []
for i in ndocs:
	words, total_words = obtain_all_words(i)
	x.append(total_words)
	y.append(len(words))

popt, _ = curve_fit(heapLaw, x, y, bounds=([1, 0.1],[200, 1.0]))
	
logx = list(map(logMath, x))
logy = list(map(logMath, y))

plt.plot(logx, logy, "g", label="data")
plt.plot(list(map(logMath, x)), list(map(logMath,heapLaw(x, *popt))), "k--", label="fit")
plt.xlabel("log(total)")
plt.ylabel("log(different)")
plt.show()

plt.plot(x, y, "g", label="data")
plt.plot(x, heapLaw(x, *popt), "k--", label="fit")
plt.xlabel("total")
plt.ylabel("different")
plt.show()
