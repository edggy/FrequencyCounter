#import bitStream

#11000001110101011
#1
#{1:1}
#

class FreqCounter:
    def __init__(self, stream, maxLen = None):
        self.data = {}
        lastN = []
        self.length = 0
        for i in stream:
            self.length += 1
            lastN.append(i)
            if maxLen and len(lastN) > maxLen:
                lastN = lastN[1:]
            chain = ()
            for char in reversed(lastN):
                chain = (char,) + chain
                if chain not in self.data:
                    self.data[chain] = 1
                else:
                    self.data[chain] += 1
                
                    
    def __getitem__(self, i):
        try:
            return self.data[i]
        except KeyError:
            return 0
        
    def __len__(self):
        return self.length
    
if __name__ == '__main__':
    import math
    from bitStream import BitStream as Bs
    
    bs = Bs(0xddf07d88bcfcd9dbc9564c56900cbc533d9485e6c1195e5299db9b0ec44fe0c2acb63d22d901a5327d67188013edccb403bcd07d4a34a87ef9cd182d0f0be638)
    bs2 = Bs(0b01001001011011100010000001100011011011110110110101110000011101010111010001100101011100100010000001110011011000110110100101100101011011100110001101100101001000000110000101101110011001000010000001101001011011100110011001101111011100100110110101100001011101000110100101101111011011100010000001110100011010000110010101101111011100100111100100101100001000000110000100100000010010000111010101100110011001100110110101100001011011100010000001100011011011110110010001100101001000000110100101110011001000000110000100100000011100000110000101110010011101000110100101100011011101010110110001100001011100100010000001110100011110010111000001100101001000000110111101100110001000000110111101110000011101000110100101101101011000010110110000100000011100000111001001100101011001100110100101111000001000000110001101101111011001000110010100100000011101000110100001100001011101000010000001101001011100110010000001100011011011110110110101101101011011110110111001101100011110010010000001110101011100110110010101100100001000000110011001101111011100100010000001101100011011110111001101110011011011000110010101110011011100110010000001100100011000010111010001100001001000000110001101101111011011010111000001110010011001010111001101110011011010010110111101101110)
    
    countLength = 16
    fc = FreqCounter(bs, countLength)
    
    
    length = 0
    count = 0
    
    avg = [1]
    var = [1]
    
    for i in range(2**countLength):
        tup = tuple([j for j in Bs(i)])
        tup2 = tuple([j for j in reversed(Bs(i))])
        
        freq = fc[tup]
        freq2 = fc[tup2]
        
        if length != len(tup):
            #print '0b' + '0' * length, (len(fc) - count)
            freq = fc[(0,) * length]
            print '0b' + '0' * length, freq
            print
            avg[length] += freq
            var[length] += freq**2
            length = None
            count = 0   
            avg.append(0)
            var.append(0)
        
        if length is None:
            length = len(tup)
            
        
            
        print bin(i), freq
        count += freq
        avg[length] += freq
        var[length] += freq**2
        
        if tup != tup2:
            print '0b' + ''.join(reversed(bin(i)[2:])), freq2
            count += freq2
            avg[length] += freq2
            var[length] += freq2**2
            
    print avg
    avg2 = [1.0*len(fc) / i for n, i in enumerate(avg)]
    print avg2
    print
    print var
    stdev = [1.0*i/j - k**2 for i, j, k in zip(var, avg, avg2)]
    print map(math.sqrt, stdev[1:])