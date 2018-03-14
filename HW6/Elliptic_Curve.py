def modInverse(a, m) :
    a = a % m
    for x in range(1, m) :
        if ((a * x) % m == 1) :
            return x
    return 1

multi = 7

a = 1
b = 6
p = 11

x = 2
y = 7

xf = 5
yf = 2
for i in range(multi - 2):
    inv = modInverse(( xf - x )% p, p)
    lam = ( (yf - y)*(inv) ) % p
    x_temp = (lam**2 - x - xf) % p
    y_temp = (lam*(x - x_temp) - y) % p
    xf = x_temp
    yf = y_temp
print((xf, yf))
