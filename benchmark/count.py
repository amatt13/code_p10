import sys

if __name__ == '__main__':
    string = sys.argv[1]
    n = sys.argv[2]
    print("Replacing X and counting {0} times".format(n))
    result = ""
    print("\n".join(string.replace("X", str(x)) for x in range(0, int(n))))
