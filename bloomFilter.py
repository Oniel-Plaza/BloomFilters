import array
import math
import csv
import sys

p = 0.0000001

def makeBitArray(bitSize, fill = 0):
    intSize = bitSize >> 5                   # number of 32 bit integers
    if (bitSize & 31):                      # if bitSize != (32 * n) add
        intSize += 1                        #    a record for stragglers
    if fill == 1:
        fill = 4294967295                                 # all bits set
    else:
        fill = 0                                      # all bits cleared

    bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return(bitArray)

  # testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return(array_name[record])

# clearBit() returns an integer with the bit at 'bit_num' cleared.
def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return(array_name[record])

# toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return(array_name[record])

# Tests the bit arrays and prints the results
def generateResults(f, f1 ,f2, k, m):
    n = len(f2) # size of the second file
    for i in range(0, n):
        # uses the same hashing as for the bit setting
        h = int(hash(str(f2[i]) + str(k)) % m) 
        
        #Tests the bits and if it is not 0, it means that it's probably in the DB
        if testBit(f, h) != 0:
            print(f2[i] + ",Probably in the DB")
        # Else, it is not in the DB
        else:
            print(f2[i] + ",Not in the DB")
                 
                 
# Creates a list of string for every input line  
def readCSV(f):
    file = open(f)
    type(file)
    reader = csv.reader(file)
    next(reader)
    rows = []
    for row in reader:
        rows.append(row[0])
    file.close()
    return rows


def makeBloom(f1, f2):
    file1 = readCSV(f1) # creates a list with all input lines of the first file
    file2 = readCSV(f2) # creates a list with all input lines of the second file
    n = len(file1) # represents how many lines of input the first file has
    m = int(math.ceil(n * math.log(p) / math.log(1 / math.pow(2, math.log(2)))))
    k = int(round((m / n) * math.log(2))) 
    filter = makeBitArray(m) # creates a BloomFilter that is represented as a bit array
    
    # Iterates over the elements in the first input file
    for i in range (0,n):
        # creates the hashing number by using 'k' as the string constant
        h = hash(file1[i] + str(k)) % m
        # sets the bit in  the bloom filter to one at the hashing index
        setBit(filter,h)
        
    # This function will print the results of the bit testing 
    generateResults(filter, file1, file2, k, m)
    
    
if len(sys.argv) > 1:
    makeBloom(sys.argv[1], sys.argv[2])
            