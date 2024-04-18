test = "https://kisswood.eu/farawaypain/kumo-desu-ga-nani-ka-chapitre-300/"[:-1]
numChap = test[test.find('chapitre')+9:].replace('-','.')
print(numChap)

numChap = {0:6,1:5,2:3}

for i in range(numChap.__len__()-1,-1,-1):
    print(numChap[i])

print([7,8]+[4])