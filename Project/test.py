import os
import random
prime = 115792089237316195423570985008687907853269984665640564039457584007913129639747
counter = 0
while True:
    rand = str(random.randint(0, prime))
    with open("test.txt", "w+") as f:
        f.write(rand)
    os.system("./project < test.txt > out.txt")
    with open("out.txt", "r") as f:
        if "Correct!" not in f.read():
            print("*****")
            print(rand)
            print("*****")
            print("Not correct! Check out.txt for more details.")
            exit(-1)
        else:
            counter += 1
            print("Total correct: " + str(counter))
