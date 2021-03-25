import numpy as np
cad='lfdkjddsfkajlsñlsjadkjfsdakjs'
pos = np.where(np.array(list(cad)) == 'a')[0]
print(pos)