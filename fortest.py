import random
import math

lst = []

for i in range(100):
    lst.append(round(random.uniform(0, 100), 2))

print(lst)
print(sum(lst) / 100)
