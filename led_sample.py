import max7219.led as segment
 
#saves the values of all segment displays (max 8)
digValues = [0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000]
 
def display(dig, value):
    values = {}
    values['0'] = 0b01111110
    values['1'] = 0b00001100
    values['2'] = 0b10110110
    values['3'] = 0b10011110
    values['4'] = 0b11001100
    values['5'] = 0b11011010
    values['6'] = 0b11111010
    values['7'] = 0b00001110
    values['8'] = 0b11111110
    values['9'] = 0b11011110
    values[-1]  = 0b00000000 #empty sign
    values[' '] = 0b00000000
    values['A'] = 0b11101110
    values['b'] = 0b11111000
    values['C'] = 0b01110010
    values['d'] = 0b10111100
    values['E'] = 0b11110010
    values['F'] = 0b11100010
    values['G'] = 0b01111010
    values['H'] = 0b11101100
    values['I'] = 0b01100000
    values['J'] = 0b00011100
    values['K'] = 0b11101010
    values['L'] = 0b01110000
    values['O'] = 0b01111110
    values['P'] = 0b11100110
    values['q'] = 0b11001110
    values['r'] = 0b10100000
    values['S'] = 0b11011010
    values['t'] = 0b11110000
    values['U'] = 0b01111100
    values['-'] = 0b10000000
    values['_'] = 0b00010000
 
    bPosition = 0b00000001
 
    if dig < 1:
        bPosition = bPosition<<dig-1
 
    #go through all segment displays
    for x in range(8):
        if (values[value]) & (1 << x) :
            digValues[x] |= bPosition
        else:
            digValues[x] = (0b11111111 ^ bPosition) & digValues[x]
            #Senden
            segment.send_byte(x, digValues[x])
 
def showvalue(value):
    n = [char for char in str(value)]
    #fill all unused ads with the empty character
    n = ([-1]*8 + n)[-8:]
    n.reverse()
    index = 7
    for i in n:
        display(index, i)
        index = index -1
 
def main():
    segment.init()
    segment.clear()
    while True:
        x = str(input('Bitte Wert eingeben: '))
        showvalue(x)
 
if __name__ == "__main__":
    main()
