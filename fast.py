import datetime
import time

#time.time

start = time.time()

for i in range(50):
    if i%2 == 0:
        print(f"{i} is an even number")
else:
        print(f"{i} is an odd number")
    

end = time.time()

print(end-start)
