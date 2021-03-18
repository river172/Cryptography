import PrimeGenerator 
#GCD Code from https://www.geeksforgeeks.org/gcd-in-python/
#!/usr/bin/env python3.7.7
from BitVector import *
import sys

e = 65537
def computeGCD(x, y): 
  
    if x > y: 
        small = y 
    else: 
        small = x 
    for i in range(1, small+1): 
        if((x % i == 0) and (y % i == 0)): 
            gcd = i 
              
    return gcd 

def keyGen():
    
    num_of_bits_desired = 128                           
    generator = PrimeGenerator.PrimeGenerator( bits = num_of_bits_desired )                 #
    prime = generator.findPrime() 
    prime2 = generator.findPrime()

    PrimeBV = BitVector(intVal = prime)
    Prime2BV= BitVector(intVal = prime2)

    
    check = True
    while(check):

        if(prime == prime2):
            check = False

        if(PrimeBV[0] == 0 | PrimeBV[1] == 0):
            check = False

        if(Prime2BV[0] == 0 | Prime2BV[1] == 0):
            check = False
        if(computeGCD(prime - 1,e) != 1):
            check = False
        if(computeGCD(prime2 - 1,e) != 1):
            check = False
        if(check == True):
            break
        else:
            prime = generator.findPrime() 
            prime2 = generator.findPrime()

            PrimeBV = BitVector(intVal = prime)
            Prime2BV= BitVector(intVal = prime2)
    return prime,prime2

def RSA_encrypt(P,Q,messageFile,outF):
    n = P * Q
    
    bv = BitVector(filename = messageFile)
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file( 128)
        if bitvec.length() != 128:
            bitvec.pad_from_right(128 - bitvec.length())
        if bitvec.length() > 0:
            Padding_left = BitVector(intVal = 0 ,size = 128)
            combined_bv = Padding_left + bitvec
           
            C = pow(int(combined_bv),e,n)
            Final_bv = BitVector(intVal= C, size= 256)
            outF.write(Final_bv.get_bitvector_in_hex())


def RSA_decrypt(P,Q,messageFile,outF):
    n = P * Q
    totient = (P-1)*(Q-1)
    pBit = BitVector(intVal = P, size =256)
    qBit = BitVector(intVal = Q, size = 256)
    Modulus = BitVector(intVal = totient,size = 256)
    BitD = BitVector(intVal = e ,size = 256)
    d = BitD.multiplicative_inverse(Modulus)
    final_string =''
    bv = BitVector(hexstring = messageFile)
    for i in range(bv.length()// 256):
        bitvec = bv[i*256:i*256+256]
        if bitvec.length() > 0:
            vp = pow(int(bitvec),int(d),P)
            vq = pow(int(bitvec),int(d),Q)
            vpBit = BitVector(intVal = vp,size = 256)
            vqBit = BitVector(intVal = vq,size = 256)
            pMI = pBit.multiplicative_inverse(qBit)
            qMI = qBit.multiplicative_inverse(pBit)
            Xp = int(qMI) * int(qBit)
            Xq = int(pMI) * int(pBit)
            CRT = (int(vpBit)*Xp+int(vqBit)*Xq) % n

            CRTbit = BitVector(intVal = CRT,size = 256)
            final = CRTbit[128:256]
        

        final_string = final_string+ final.get_bitvector_in_ascii()
    outF.write(final_string)

            


            


#main function

if(sys.argv[1][1]== 'g'):
    Pfile = sys.argv[2]
    Qfile = sys.argv[3]
    outP = open(Pfile,"w")
    outQ= open(Qfile,"w")
    prime,prime2 = keyGen()
    outP.write(str(prime))
    outQ.write(str(prime2))

if sys.argv[1][1] == 'e':   

    messageFile = sys.argv[2]
    with open(sys.argv[3], 'r') as Pfile:
        P = int(Pfile.read())
    with open(sys.argv[4], 'r') as Qfile:
        Q = int(Qfile.read())
    outFile = sys.argv[5]
    outF = open(outFile,"w")
    RSA_encrypt(P,Q,messageFile,outF)

if sys.argv[1][1] == 'd':   

    messageFile = sys.argv[2]
    messageF = open(messageFile,"r",encoding='utf-8')
    message = messageF.read()
    with open(sys.argv[3], 'r') as Pfile:
        P = int(Pfile.read())
    with open(sys.argv[4], 'r') as Qfile:
        Q = int(Qfile.read())
    outFile = sys.argv[5]
    outF = open(outFile,"w")
    RSA_decrypt(P,Q,message,outF)
  

