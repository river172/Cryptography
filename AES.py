import sys
from BitVector import *
import warnings

warnings.filterwarnings(action='ignore')

AES_modulus = BitVector(bitstring='100011011')
key_words = []


def get_key(actual_key):
    key = keysize = None
    keysize = 256
    key = actual_key
    key = key.strip()
    key += '0' * (keysize//8 - len(key)) if len(key) < keysize//8 else key[:keysize//8]  
    key_bv = BitVector( textstring = key )
    return keysize,key_bv

def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant


def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable


def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))


def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words


def ShiftLeft(list,num):
           for x in range(num):
            g=list[0]
            list.pop(0)
            list.append(g)

def MixCol(list):
    columns = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
    n=8
    final = BitVector(intVal=0,size=8)
    
    for j in range(4):
        count = 0
        for i in range(4):
            first = BitVector(intVal=columns[i][0],size=8)
            answer1 = list[0][j].gf_multiply_modular(first,AES_modulus,n)
           


            second = BitVector(intVal=columns[i][1],size=8)
            answer2 = list[1][j].gf_multiply_modular(second,AES_modulus,n)

            third = BitVector(intVal=columns[i][2],size=8)
            answer3 = list[2][j].gf_multiply_modular(third,AES_modulus,n)

            fourth = BitVector(intVal=columns[i][3],size=8)
            answer4 = list[3][j].gf_multiply_modular(fourth,AES_modulus,n)

            final += answer1^answer2^answer3^answer4

            
            count = count +1
    
    return final 
def encrypt(MessageFile,round_keys,subBytesTable,outFile):
    

    bv = BitVector(filename = MessageFile)
    
    statearray = [[0 for  x in range(4)] for x in range(4)]    
    statearray_sub = [[0 for  x in range(4)] for x in range(4)]
    
    #encryption begins
    
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file( 128)
        if bitvec.length() != 128:
            bitvec.pad_from_right(128 - bitvec.length())
        if bitvec.length() > 0:
             words =round_keys[0]
          
             words = words.strip()
             words_bitvec = BitVector(hexstring = words )
             xor_bitvec = bitvec ^ words_bitvec  
             for i in range(4):
                for j in range(4):
                    statearray[j][i] = xor_bitvec[32*i + 8*j:32*i + 8*(j+1)]
             
             for x in range(14):
                
            
                #subBytes step
                for i in range(4):
                    for j in range(4):
                        num =  int(statearray[j][i])
                        
                        statearray_sub[j][i]= BitVector(intVal = subBytesTable[num],size = 8)
                
                #shift rows
                ShiftLeft(statearray_sub[1],1)
                ShiftLeft(statearray_sub[2],2)
                ShiftLeft(statearray_sub[3],3)
                
                    
                 
                #Mix Columns
                if x <13:
                    bitvec = MixCol(statearray_sub)
                    bitvec = bitvec[8:len(bitvec)]
                if x == 13:
                    bitvec=BitVector(size=0)
                    for i in range(4):
                        for j in range(4):
                            bitvec+=statearray_sub[j][i]

                   
                    
                          
                #add round key
                words2 =round_keys[x+1]
                words_bitvec2 = BitVector(hexstring = words2 )
                final_bit =bitvec^words_bitvec2
                
               
               
                for i in range(4):
                    for j in range(4):
                        statearray[j][i] = final_bit[32*i + 8*j:32*i + 8*(j+1)]
                
              
        
                    
        outFile.write(final_bit.get_bitvector_in_hex())

  
def invShiftLeft(list,num):
        for x in range(num):
            g=list[len(list)-1]
            list.pop(len(list)-1)
            list.insert(0,g)

            
            
def invMixCol(list):
    columns = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
    n=8
    final = BitVector(intVal=0,size=8)
    
    for j in range(4):
        count = 0
        for i in range(4):
            first = BitVector(intVal=columns[i][0],size=8)
            answer1 = list[0][j].gf_multiply_modular(first,AES_modulus,n)
           


            second = BitVector(intVal=columns[i][1],size=8)
            answer2 = list[1][j].gf_multiply_modular(second,AES_modulus,n)

            third = BitVector(intVal=columns[i][2],size=8)
            answer3 = list[2][j].gf_multiply_modular(third,AES_modulus,n)

            fourth = BitVector(intVal=columns[i][3],size=8)
            answer4 = list[3][j].gf_multiply_modular(fourth,AES_modulus,n)

            final += answer1^answer2^answer3^answer4

            
            count = count +1
    
    return final           
            
    


def decrypt(Message,round_keys,subBytesTable,outFile):
    

    bv = BitVector(hexstring = Message)
    
    statearray = [[0 for  x in range(4)] for x in range(4)]    
    statearray_sub = [[0 for  x in range(4)] for x in range(4)]  
    round_keys.reverse()
    #encryption begins
    
    for i in range(bv.length()// 128):
        bitvec = bv[i*128:i*128+128]
        
      
        if bitvec.length() > 0:
            words =round_keys[0]
            words = words.strip()
            words_bitvec = BitVector(hexstring = words )
            xor_bitvec = bitvec ^ words_bitvec
            for i in range(4):
                for j in range(4):
                    statearray[j][i] = xor_bitvec[32*i + 8*j:32*i + 8*(j+1)]

             
            for x in range(14):
                #setup
               
                #shift rows
                invShiftLeft(statearray[1],1)
                invShiftLeft(statearray[2],2)
                invShiftLeft(statearray[3],3)


                #INVERSEsubBytes step
                for i in range(4):
                    for j in range(4):
                        num =  int(statearray[j][i])
                        index = invSubBytesTable.index(num)
                        statearray_sub[j][i]= BitVector(intVal = invSubBytesTable[num],size = 8)
                #addkey
                before_key=BitVector(intVal=0,size=8)
                for i in range(4):
                    for j in range(4):
                        before_key += statearray_sub[j][i]
                before_key=before_key[8:len(before_key)]
                words2 =round_keys[x+1]
                words_bitvec2 = BitVector(hexstring = words2 )
                before_key = before_key^words_bitvec2

                for i in range(4):
                    for j in range(4):
                        statearray_sub[j][i] = before_key[32*i + 8*j:32*i + 8*(j+1)]
                
                #Mix Column
                if x < 13:
                    bitvec = invMixCol(statearray_sub)
                    bitvec = bitvec[8:len(bitvec)]
                    

                    for i in range(4):
                        for j in range(4):
                            statearray[j][i] = bitvec[32*i + 8*j:32*i + 8*(j+1)]
                if x == 13:
                    bitvec = BitVector(size=0)
                    for i in range(4):
                        for j in range(4):
                            bitvec+=statearray_sub[j][i]

                  
            outFile.write(bitvec.get_bitvector_in_ascii())






subBytesTable = []                                                  # for encryption
invSubBytesTable = []                                               # for decryption
genTables()
with open(sys.argv[3], 'r') as f:
    key_from_file = f.read()
keysize, key_bv = get_key(key_from_file)

key_words = gen_key_schedule_256(key_bv)
key_schedule = []

for word_index,word in enumerate(key_words):
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i*8:i*8+8].intValue())
        key_schedule.append(keyword_in_ints)
num_rounds = None
num_rounds = 14
round_keys = [None for i in range(num_rounds+1)]
for i in range(num_rounds+1):
    round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3]).get_bitvector_in_hex()


#Get message
if sys.argv[1][1] == 'e':   
    messageFile = sys.argv[2]
    outFile = sys.argv[4]
    outF = open(outFile,"w")
    encrypt(messageFile,round_keys,subBytesTable,outF)

if sys.argv[1][1] == 'd':   
    messageFile = sys.argv[2]
    messageF = open(messageFile,"r",encoding='utf-8')
    message = messageF.read()
   
    outFile = sys.argv[4]
    outF = open(outFile,"w",encoding='utf-8')
    decrypt(message,round_keys,subBytesTable,outF)


   




