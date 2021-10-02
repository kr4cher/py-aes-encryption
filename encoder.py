from staticVars import *

class AESEncoder(object):

    def addRoundKey(self, matrix, key):
        newMatrix = []
        for i in range(len(matrix)):
            newMatrix += [[]]
            for j in range(len(matrix[i])):
                stateBin = self.clearBin(matrix[i][j])
                keyBin = self.clearBin(key[i][j])
                newBin = ''
                for k in range(len(stateBin)):
                    newBin += str(int(stateBin[k]) ^ int(keyBin[k]))
                newMatrix[i] += [int(newBin, 2)]
        return newMatrix
    
    
    def subBytes(self, matrix, sBox):
        newMatrix = []
        for i in range(len(matrix)):
            newMatrix += [[]]
            for j in range(len(matrix[i])):
                newMatrix[i] += [sBox[matrix[i][j]]]
        return newMatrix
    
    
    def shiftRows(self, matrix):
        newMatrix = [[matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3]],
                     [matrix[1][1], matrix[1][2], matrix[1][3], matrix[1][0]],
                     [matrix[2][2], matrix[2][3], matrix[2][0], matrix[2][1]],
                     [matrix[3][3], matrix[3][0], matrix[3][1], matrix[3][2]]]
        return newMatrix
    
    
    def mixColumns(self, matrix, GRKoerper=GRKoerper):
        newMatrix = []
        for i in range(len(matrix)):
            newMatrix += [[]]
            for j in range(len(matrix[i])):
                newMatrix[i] += [[]]
    
        polynom = '100011011'
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                binProdukte = []
                for k in range(len(matrix[i])):
                    binProdukt = self.binaerMultiplikation(bin(matrix[k][i])[2:], bin(GRKoerper[j][k])[2:])  # Spalte i der matrix multipliziert mit Reihe i des GRKoerpers
                    if int(binProdukt, 2) > 255:
                        newBin = ''
                        for l in range(len(polynom)):
                            newBin += str(int(binProdukt[l]) ^ int(polynom[l]))  # XOR-Verknuepfung
                        binProdukt = newBin
                    binProdukte += [binProdukt]
                newMatrix[j][i] = int(self.binaerAddition(binProdukte), 2)
        return newMatrix
    
    
    def expandKey(self, key, roundNumber, sBox=sBox, rconMatrix=rconMatrix):
        newMatrix = []
        for i in range(len(key)):
            newMatrix += [[]]
            for j in range(len(key[i])):
                newMatrix[i] += [[]]
                
        # fuer erste Spalte der newMatrix
        letzteSpalte = []
        for i in range(len(key)):
            letzteSpalte += [key[i][len(key) - 1]]
        # RotWord
        spalte = self.rotWord(letzteSpalte)
        # SubBytes
        nSpalte = []
        for i in range(len(spalte)):
            nSpalte += [sBox[spalte[i]]]
        spalte = nSpalte
        nSpalte = []
        for i in range(len(spalte)):
            binZahlen = [self.clearBin(spalte[i]), self.clearBin(key[i][0]), self.clearBin(rconMatrix[i][roundNumber])]
            newMatrix[i][0] = int(self.binaerAddition(binZahlen), 2)
        
        # fuer restliche Spalten
        for i in range(1, len(key)):
            for j in range(len(key)):
                binZahlen = [self.clearBin(key[j][i]), self.clearBin(newMatrix[j][i - 1])]
                newMatrix[j][i] = int(self.binaerAddition(binZahlen), 2)
                
        return newMatrix
    
    
    def encode(self, matrix, key):
        # Verschluesselung
        
        matrix = self.addRoundKey(matrix, key)
        
        for i in range(9):
            matrix = self.subBytes(matrix, sBox)
            matrix = self.shiftRows(matrix)
            matrix = self.mixColumns(matrix, GRKoerper)
            key = self.expandKey(key, i, sBox, rconMatrix)
            matrix = self.addRoundKey(matrix, key)
            
##             print(20 * '-')
##             print('Round', i + 1, end='\n\n')
##             self.printMatrix(matrix)
          
        matrix = self.subBytes(matrix, sBox)
        matrix = self.shiftRows(matrix)
        key = self.expandKey(key, 9, sBox, rconMatrix)
        matrix = self.addRoundKey(matrix, key)
        
        print(20 * '-')
        print('Round 10:', end='\n\n')
        self.printMatrix(matrix)
        print('Key:')
        self.printMatrix(key)
        
        return matrix
    
    
    #=================#
    # Hilfsfunktionen #
    #=================#
    
    def clearBin(self, number):
        # return: String mit 8-stelliger Binaerzahl
        return bin(number)[2:].zfill(8)
    
    
    def printMatrix(self, matrix, end='\n', sep=' '):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                hexZahl = hex(matrix[i][j])
                if len(hexZahl) == 3:
                    hexZahl = hexZahl[:2] + '0' + hexZahl[2:]
                if i == len(matrix) - 1:
                    if j == len(matrix[i]) - 1:
                        print(hexZahl)
                    else:
                        print(hexZahl, end=sep)
                else:
                    if j == len(matrix[i]) - 1:
                        print(hexZahl)
                    else:
                        print(hexZahl, end=sep)
        print(end=end)
    
    
    def binaerMultiplikation(self, bin1, bin2):
        # Parameter: 2 Binaerzalen als String; len(bin1)<=8, len(bin2)<=2
        # return:    Binaerprodukt als String mit Laenge 8
        bin1 = bin1.zfill(8)
        bin2 = bin2.zfill(2)
            
        if bin2 == '00':
            produkt = '00000000'
        elif bin2 == '01':
            return bin1
        else:
            produkt = ''
            teilProdukt = []
            
            for i in range(2):
                teilProdukt += ['']
                for j in range(8):
                    teilProdukt[i] += bin1[j] * int(bin2[i])
            
            teilProdukt[0] += '0'
            teilProdukt[1] = teilProdukt[1].zfill(len(teilProdukt[0]))
            for i in range(len(teilProdukt[0])):
                produkt += str(int(teilProdukt[0][i]) ^ int(teilProdukt[1][i]))
        
        return produkt
    
    
    def binaerAddition(self, binZahlen):
        # XOR-Verknüpfung
        summe = ''
        laenge = 0
        for zahl in binZahlen:
            if len(zahl) > laenge:
                laenge = len(zahl)
        
        for i in range(laenge):
            bit = 0
            for j in range(len(binZahlen)):
                if len(binZahlen[j]) < laenge:
                    binZahlen[j] = binZahlen[j].zfill(laenge)
                bit ^= int(binZahlen[j][i])
            summe += str(bit)
            
        return summe
    
    
    def rotWord(self, spalte):
        helpVar = spalte[0]
        for i in range(len(spalte) - 1):
            spalte[i] = spalte[i + 1]
        spalte[len(spalte) - 1] = helpVar
        return spalte
