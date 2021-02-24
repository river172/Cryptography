
#Divide function ideas gotten from https://www.playandlearntocode.com/article/integer-division-algorithm-python-leetcode
#python 3.7.7
def multiply(n, m): 
    add = 0
    tempM = abs(m)
    if m  == 0:
        return 0
    if n == 0:
        return 0
    if m == 1:
        return n
    if n == 1:
        return m
    if m == 2:
        return n<<1
    if n == 2:
        return  m<<1
    

    if m == -1:
        return -n
    if n == -1:
        return -m
    if m == -2:
        return -(n<<1)
    if n == 2:
        return  -(m<<1)
    
    
    else:
        i = tempM- 2
        for x in range(i):
            add = n+ add
        if(m >0):
         return((n<<1)+add)

        if m < 0 :
            return -((n<<1)+add)

def Divide(m, n):
        remainder = n  
        quot = 1
        if m < n:
            return 0
        
        elif m == n:
            return 1

        while m > remainder:
            quot = quot << 1
            remainder = remainder << 1 

        remainder = remainder >> 1
        quot = quot >> 1
        return quot + Divide(m - remainder, n)

import sys

if len(sys.argv) != 3:  
    sys.stderr.write("Usage: %s   <integer>   <modulus>\n" % sys.argv[0]) 
    sys.exit(1) 

NUM, MOD = int(sys.argv[1]), int(sys.argv[2])

def MI(num, mod):
    
    NUM1 = num
    if(num < mod and num < 0):
        num = mod +num
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = Divide(num,mod)
        num, mod = mod, num % mod
        x_new = multiply(x,q)
        y_new = multiply(y,q)
      
        x, x_old = x_old - multiply(x,q),x
        y, y_old = y_old - multiply(y,q), y
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM1, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM1, MOD, MI))

MI(NUM, MOD)



