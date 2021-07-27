import sys, os
from hashlib import md5


if len(sys.argv) < 2:
    print('provide image path to run')
    exit()

dup = []
keys = dict()
for f in sys.argv[1:]:
    if os.path.isfile(f):
        with open(f,'rb') as img:
            imgHash = md5(img.read()).hexdigest()
        if imgHash not in keys:
            keys[imgHash] = f
        else:
            os.rename(f,f'data/duplicates/DUPLICATE_{len(dup)}.png')
            dup.append((f,keys[imgHash]))
print('#####################')
print(*dup, sep = '\n')
print('#####################')