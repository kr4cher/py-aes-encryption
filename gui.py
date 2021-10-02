from tkinter import Tk, Text, Button
from tkinter.constants import DISABLED, END, NORMAL
from encoder import AESEncoder
from staticVars import keyMatrix

class GUI():
    
    def __init__(self):
        self.encoder = AESEncoder()

        self.tk = Tk()
        self.tk.title('AES-Verschluesselung')
        self.tk.geometry('1280x720')
        
        self.enterText = Text(master=self.tk, width=50, height=10)
        self.enterText.grid(row=0, column=0, padx=50, pady=50)
        
        self.arrowLabel = Button(master=self.tk, text='Verschluesseln -->', command=self.encode)
        self.arrowLabel.grid(row=0, column=1, pady=100)
        
        self.outputText = Text(master=self.tk, width=50, height=10, state=DISABLED)
        self.outputText.grid(row=0, column=2, padx=50, pady=50)
        
        self.tk.mainloop()
        
    def encode(self):
        text = self.enterText.get('1.0', 'end-1c')
        matrizen = [[[]]]
        matrixInd = 0
        rowInd = 0
        
        if text != '':
            for sign in text:
                matrizen[matrixInd][rowInd] += [ord(sign)]
                if len(matrizen[matrixInd][rowInd]) >= 4:
                    matrizen[matrixInd] += [[]]
                    rowInd += 1
                    if rowInd >= 4:
                        matrizen += [[[]]]
                        matrixInd += 1
                        rowInd = 0
            
            full = (rowInd == 0 and len(matrizen[len(matrizen) - 1][0]) == 4)
            while not full:
                matrizen[matrixInd][rowInd] += [0]
                if len(matrizen[matrixInd][rowInd]) >= 4:
                    matrizen[matrixInd] += [[]]
                    rowInd += 1
                    if rowInd >= 4:
                        full = True
                        
            output = []
            for matrix in matrizen:
                newMatrix = self.encoder.encode(matrix, keyMatrix)
                output += [newMatrix]
            
            self.outputText.config(state=NORMAL)
            self.outputText.delete('1.0', END)
            self.outputText.insert('1.0', self.formatMatrizen(output))
            self.outputText.config(state=DISABLED)
        else:
            self.outputText.config(state=NORMAL)
            self.outputText.delete('1.0', END)
            self.outputText.config(state=DISABLED)
        
        
    def formatMatrizen(self, matrizen):
        returnValue = ''
        for matrix in matrizen:
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    hexZahl = hex(matrix[i][j])
                    if len(hexZahl) == 3:
                        hexZahl = hexZahl[:2] + '0' + hexZahl[2:]
                    if j == len(matrix[i]) - 1:
                        returnValue += hexZahl + '\n'
                    else:
                        returnValue += hexZahl + ' '
            returnValue += '\n'
        return returnValue


gui = GUI()
