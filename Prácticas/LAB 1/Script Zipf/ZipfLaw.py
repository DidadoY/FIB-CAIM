import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import sys

def filter(text):
    filefiltered = open('newFile.txt', 'w')
    lines = text.readlines()
    for i in range(0, len(lines)):
        freq = lines[i].split(', ')
        word = freq[1].split('\n')
        if (word[0].isalpha()):
            filefiltered.write(str(freq[0]))
            filefiltered.write(", ")
            filefiltered.write(str(word[0]))
            filefiltered.write("\n")
            
            frequencies.append(int(freq[0]))

    filefiltered.close()
    return filefiltered

zipfLaw = lambda rank, a, b, c : c/((rank+b)**a)
logMath = lambda x : math.log(x, 10)

frequencies = []

file = open('../documents/file20news.txt', 'r')
newfile = filter(file)
frequencies.sort(reverse=True)

ranks = range(1, len(frequencies)+1)

popt, _ = curve_fit(zipfLaw, ranks, frequencies, bounds=([0.01, 0.0, 0.0],[1.5, 10000, 1000000]))

print(popt)

plt.plot(ranks, frequencies, "g", label="data")
plt.plot(ranks, zipfLaw(ranks, *popt), "k--", label="fit")
plt.xlabel("ranks")
plt.ylabel("frequencies")
plt.show()

logFrequencies = list(map(logMath, frequencies))
logRanks = list(map(logMath, ranks))

plt.plot(logRanks, logFrequencies, "g", label="data")
plt.plot(logRanks, list(map(logMath,zipfLaw(ranks, *popt))), "k--", label="fit")
plt.xlabel("log(ranks)")
plt.ylabel("log(frequencies)")
plt.show()
