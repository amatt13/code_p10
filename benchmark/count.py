import sys

if __name__ == '__main__':
    string = sys.argv[1]
    n = sys.argv[2]
    print("Replacing X and counting {0} times".format(n))
    result = ""
    i = 0 
    while i < int(n):
        result += string.replace("X", str(i)) + "\n"
        i += 1
    print(result)
