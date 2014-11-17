import math, shutil, re, fileinput, os

NUMBER_WORDS = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "fourty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety"
    }

def changeFile(src): #replace problem
    shutil.copy(src, "temp.txt")
    f = open(src, 'r+')
    txt = f.read()
    for word in txt.split():
        try:
            written = translate(int(word))
            txt = txt.replace(word, written)
        except ValueError:
            #print "ValueError for %s" % word
            pass

    temp = open("temp.txt", 'r+')
    temp.write(txt)
    os.remove(src)
    os.rename("temp.txt", src)

def translate(num):
    if type(num) is not int:
        return "Not a number"
    if num > 9999:
        return "Cannot print this number"
    words = []
    ones = num % 10
    tens = num % 100
    hundreds = math.floor(num/100) % 10
    thousands = math.floor(num/1000)

    if thousands:
        words.append(translate(thousands))
        words.append("thousand")
        #if not hundreds and tens:
        #    words.append("and")
    if hundreds:
        words.append(NUMBER_WORDS[hundreds])
        words.append('hundred')
        #if tens:
        #    words.append('and')
    if tens:
        if tens < 20 or ones == 0:
            words.append(NUMBER_WORDS[tens])
        else:
            words.append(NUMBER_WORDS[tens - ones])
            words.append(NUMBER_WORDS[ones])

    if num >= 21 and num <= 99:
        return '-'.join(words)
    
    else:
        return ' '.join(words)

def main():
    changeFile("numbers.txt")

if __name__ == "__main__":
    main()
