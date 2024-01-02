import numpy as np
lista = [('cosa', 2), ('t', 3)]
modulo = lambda x : np.sqrt(np.sum(np.square(x)))
weights =  [x[1] for x in lista]
finalMod = modulo(weights)
    

normalized = list(map(lambda x : (x[0], x[1]/finalMod), lista))

print(normalized)