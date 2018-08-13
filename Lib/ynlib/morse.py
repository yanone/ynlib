morseAlphabet ={
    "A" : ".-",
    "B" : "-...",
    "C" : "-.-.",
    "D" : "-..",
    "E" : ".",
    "F" : "..-.",
    "G" : "--.",
    "H" : "....",
    "I" : "..",
    "J" : ".---",
    "K" : "-.-",
    "L" : ".-..",
    "M" : "--",
    "N" : "-.",
    "O" : "---",
    "P" : ".--.",
    "Q" : "--.-",
    "R" : ".-.",
    "S" : "...",
    "T" : "-",
    "U" : "..-",
    "V" : "...-",
    "W" : ".--",
    "X" : "-..-",
    "Y" : "-.--",
    "Z" : "--..",
    " " : "/",

    "1" : ".----",
    "2" : "..---",
    "3" : "...--",
    "4" : "....-",
    "5" : ".....",
    "6" : "-....",
    "7" : "--...",
    "8" : "---..",
    "9" : "----.",
    "0" : "-----",

    "." : ".-.-.-",
    "," : "--..--",
    ":" : "---...",
    "?" : "..--..",
    "'" : ".----.",
    "-" : "-....-",
    "/" : "-..-.",
    "@" : ".--.-.",
    "=" : "-...-",

    }

inverseMorseAlphabet=dict((v,k) for (k,v) in morseAlphabet.items())


testCode = ".... . .-.. .-.. --- / -.. .- .. .-.. -.-- / .--. .-. --- --. .-. .- -- -- . .-. / --. --- --- -.. / .-.. ..- -.-. -.- / --- -. / - .... . / -.-. .... .- .-.. .-.. . -. --. . ... / - --- -.. .- -.-- "

# parse a morse code string positionInString is the starting point for decoding
def decodeMorse(code, positionInString = 0):
    
    if positionInString < len(code):
        morseLetter = ""
        for key,char in enumerate(code[positionInString:]):
            if char == " ":
                positionInString = key + positionInString + 1
                letter = inverseMorseAlphabet[morseLetter]
                return letter + decodeMorse(code, positionInString)
            
            else:
                morseLetter += char
    else:
        return ""
    

#encode a message in morse code, spaces between words are represented by '/'
def encodeToMorse(message):
    encodedMessage = ""
    for char in message[:]:
        if char.upper() in morseAlphabet:
            encodedMessage += morseAlphabet[char.upper()] + " "
            
    return encodedMessage.strip()


def encodeToTiming(code):
    codes = []
    for word in code.split(' '):
        wordcodes = []
        for char in word:
            if char == '-':
                wordcodes.append('===')
            elif char == '.':
                wordcodes.append('=')
            elif char == '/':
                wordcodes.append('.')
        codes.append('.'.join(wordcodes))
    return '...'.join(codes)


if __name__ == '__main__':
    morse = encodeToMorse('I love you.')
    timing = encodeToTiming(morse)

    print morse
    print timing
