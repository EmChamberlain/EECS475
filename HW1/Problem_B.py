from collections import Counter
import string

def decrypt(key, ciphertext):
    s_out = ""
    for char in ciphertext:
        s_out += str(key[char])
    return s_out




alphabet = "abcdefghijklmnopqrstuvwxyz"
key = {}
ciphertext = "emglosudcgdncuswysfhnsfcykdpumlwgyicoxysipjckqpkugkmgolicgincgacksnisacykzsckxecjckshysxcgoidpkzcnkshicgiwygkkgkgoldsilkgoiusigledspwzugfzccndgyysfuszcnxeojncgyeoweupxezgacgnfglknsacigoiyckxcjuciuzcfzccndgyysfeuekuzcsocfzccnciaczejncshfzejzegmxcyhcjumgkucy"

for char in alphabet:
    key[char] = '?'


# looking for e/a
counter = Counter(ciphertext)
for char, count in counter.most_common():
    print(char, count)


# looking for th
collected = [ciphertext[i:i+2] for i in range(len(ciphertext)-3)]
counter = Counter(collected)
for s, count in counter.most_common():
    if count >= 4:
        print(s + ':' + str(count))

# looking for the
collected = [ciphertext[i:i+3] for i in range(len(ciphertext)-4)]
counter = Counter(collected)
for s, count in counter.most_common():
    if count >= 2:
        print(s + ':' + str(count))

# e = c, h = z, t = f

key['c'] = 'e'
key['u'] = 't'
key['z'] = 'h'

key['g'] = 'a'
key['o'] = 'n'
key['i'] = 'd'

key['f'] = 'w'
key['n'] = 'l'

key['a'] = 'v'
key['e'] = 'i'
key['j'] = 'c'

key['w'] = 'g'

key['y'] = 'r'

key['k'] = 's'
key['x'] = 'p'

key['s'] = 'o'
key['p'] = 'u'

key['d'] = 'b'

key['h'] = 'f'

key['l'] = 'y'

key['q'] = 'j'
key['m'] = 'm'

for char in alphabet:








decrypted = decrypt(key, ciphertext)

print(ciphertext)
print(decrypted)





