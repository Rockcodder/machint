a = ["I", "X", "C", "M", "X̅"]
b = ["V", "L", "D", "V̅"]


def toRom(num : int, pos : int):
    num = int(num)
    if(num>0 and num<4):
        print(a[pos-1]*num, end="")
    elif(num == 4):
        print(a[pos-1]+b[pos-1], end="")
    elif(num>4 and num<9):
        num -= 5
        print(b[pos-1]+a[pos-1]*num, end="")
    elif(num == 9):
        print(a[pos-1]+a[pos], end="")

def main():
    num = input("Enter number: ")
    print("Number in Roman numerals is: ", end="")
    for i in range(0, len(num)):
        toRom(num[i], len(num) - i)
    print()
main()