import collections
import operator

alphabet = "abcdefghijklmnopqrstuvwxyz"
key = {}
ciphertext = "hlfiusvsaqfpfpwaryxewdudwbrvxvrthapcjlhrlalbkwfeecmlpfvuyimxqpiovczogidthjgdhrlifyxkwhuigkullqqqhltvyzckbseelxrpikavbrxmysirovgipszwxpiwyauszeuiqhglxesombmhuepeyplvxoethjysytwfydbxndutimvhtzjzzazwiigktqzqpsfpeijyuklfrgnpfeckohuevmwnoiihvogamphbdseiymsogvasyfzvthckoueifegzoqbvrmhyysqembrvxvnecpirnmihwttwtmaooirmyoqbzylszwqembrvxvnqcklalsxpkthswzhnmewtfvxohsbrlmycwfrchjkthtifrhhyxpmxvrorbrlthdcdghxvjlllnsiekckfhbzoyifijeuklsfpxgnlfigkuegiapljgvlphwlpnpcquagyuayopoadhjrpneihvtkivfcomgnsmvtyajwfnlivnywfxzrthtwppbvhzeyvtxxbtwoekeypfvahrpimsrckbcghxwycybboadfiysiaqqnlecpyizswagiitafbavntlskqnembvavgtfhqqhuizlytgbbctemxtdyxigfohrfdczibghbwndgvaiosmmyfnbncepbwyzfxvroaepbtneiduiesxzjeqqnlyptflfavpamsyslleguifwjwzrxcahbwxhiolwdubiywsqiyrthxmpmeqdghxvjtmkwhuigkxflmzwfigknyneqgvfmljjvrbyaepmylfjwggaeprphfvhuebvipaomsfofiytgbwfbtaiwnbbzwfhoiwjhbifyymljdujmtreemsrmqwknrwwysylksnnpmysgbbvrrxrthcpgchrbrxffxzqvtrskebbuoahtxyzypjsytxhwzoklplwaewgypigvnwmfycptsfbrgtcuizsrflgtxgbzqrsnvwzoklgvtpmysbbzghryvnrbqibqlxjyebbaheexxxeuhmmbupeypltifqimwjinomardhaseitvwftaiglnqmflwaiwpneihaoupjxiimwfwtwmpxygknvxwfyxzwcyewfdmlbmnrsplnnbxnsjhhywdjomjvonwbplbwigoywnrbqwtyaghqzihihghxgwzqaacswtxjcaxhsesmljcy"

# taken from previous attempt at this
freq_dict = { "A": .08167, "B": .01492, "C": .02782, "D": .04253, "E": .12702, "F": .02228,
"G": .02015, "H": .06094, "I": .06996, "J": .00153, "K": .00772, "L": .04025,
"M": .02406, "N": .06749, "O": .07507, "P": .01929, "Q": .00095, "R": .05987,
"S": .06327, "T": .09056, "U": .02758, "V": .00978, "W": .02360, "X": .00150,
"Y": .01974, "Z": .00074 }


def v_incidence(input, key_length):
    texts = [""] * key_length

    for x in range(key_length):
        texts[x] = input[x::key_length]

    texts_counts = [0.0] * key_length
    for x in range(key_length):
        texts_counts[x] = collections.Counter(texts[x])


    for x in range(key_length):
        count = 0
        for letter in texts_counts[x]:
            count += texts_counts[x][letter]
        for letter in texts_counts[x]:
            texts_counts[x][letter] = float(texts_counts[x][letter] / (1.0 * count))


    overall_sum = 0
    for x in range(key_length):


        count = 0
        sum = 0
        diff = 0

        for letter in texts_counts[x]:
            count += 1
            sum += texts_counts[x][letter]

        mean = sum / count

        for letter in texts_counts[x]:
            diff += pow(texts_counts[x][letter] - mean, 2)
        overall_sum += (diff / count)
    return overall_sum / key_length

def v_frequency(input, key_length):
    possible_key = ""
    # get individual letter frequencies for given key length
    texts = [""] * key_length
    for x in range(key_length):
        texts[x] = input[x::key_length]

    texts_counts = [0.0] * key_length
    for x in range(key_length):
        texts_counts[x] = collections.Counter(texts[x])

    for x in range(key_length):
        count = 0
        for letter in texts_counts[x]:
            count += texts_counts[x][letter]
        for letter in texts_counts[x]:
            texts_counts[x][letter] = float(texts_counts[x][letter] / (1.0 * count))
    # assume that the most common letter maps to e for each letter in key and add the guess onto possible key
    for x in range(key_length):
        sorted_freqs = sorted(texts_counts[x].items(), key=operator.itemgetter(1), reverse=True)
        guess = sorted_freqs[0][0]
        print(sorted_freqs)
        possible_key += alphabet[(alphabet.find(guess.lower()) - alphabet.find("e")) % len(alphabet)]
    return possible_key

def vigenere_decrypt(input, key):
    output = ""
    key_ind = 0
    for letter in input:
        letter_num = alphabet.find(letter) - alphabet.find(key[key_ind])
        letter_num %= len(alphabet)
        output += alphabet[letter_num]

        key_ind += 1
        if key_ind >= len(key):
            key_ind = 0
    return output


for i in range(2, 27):
    print(str(i).zfill(2) + ':' + str(v_incidence(ciphertext, i)))

# it seems like a key length of 10 is most likely since it has the highest value and is the GCD of other high values (20)


possible_key = v_frequency(ciphertext, 10)
print(possible_key)
plaintext = vigenere_decrypt(ciphertext, possible_key)
print(ciphertext)
print(possible_key * 150)
print(plaintext)

# onate is clearly correct, I se a place where it says mcpurse, im going to try changing that to mypurse
print()
possible_key = 'ulhxionate'
plaintext = vigenere_decrypt(ciphertext, possible_key)
print(ciphertext)
print(possible_key * 150)
print(plaintext)

# i see a place howlonrpeecisely and im going to try to make it say howlongprecisely
print()
possible_key = 'fluxionate'
plaintext = vigenere_decrypt(ciphertext, possible_key)
print(ciphertext)
print(possible_key * 150)
print(plaintext)

#that seems to be the correct key
print()
print(possible_key)



