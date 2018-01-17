from collections import Counter

alphabet = "abcdefghijklmnopqrstuvwxyz"
ciphertext = "kqerejebcppcjcrkieacuzbkrvpkrbcibqcarbjcvfcupkriofkpacuzqepbkrxpeiieabdkpbcpfcdccafieabdkpbcpfeqpkazbkrhaibkapcciburccdkdccjcidfuixpafferbiczdfkabicbbenefcupjcvkabpcydccdpkbcocperkivkscpicbrkijpkabi"


# taken from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = xgcd(b, n)
    if g == 1:
        return x % n

def decrypt(input, key):
    out_str = ""
    a = mulinv(key[0], 26)
    b = key[1]
    m = 26
    for char in input:
        x = ord(char) - 97
        out_str += alphabet[(a*(x - b)) % 26]
    return out_str

# looking for e/t
counter = Counter(ciphertext)
for char, count in counter.most_common():
    print(char, count, (ord(char) - 97))

print(ord('e') - 97)
print(ord('t') - 97)

# equation one : 2 = (A*4 + B) mod 26
# equation two : 1 = (A*19 + B) mod 26

valid_keys = []
# solving the modular system of equations assuming these two letters are e and t, we can throw out a lot of invalid As
for A in range(26):
    if A % 2 == 0 or A == 13:
        continue
    for B in range(26):
        eqn_one = (2 == (A*4 + B) % 26)
        eqn_two = (1 == (A*19 + B) % 26)
        if eqn_one and eqn_two:
            valid_keys.append((A, B))

print(valid_keys)

# only one valid key, (19, 4)
print(decrypt(ciphertext, valid_keys[0]))
# ...... This is in french........ well I guess I got lucky with E and T being the most common letters still
# you guys are tricky

