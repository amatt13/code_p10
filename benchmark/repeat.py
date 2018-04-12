import sys

if __name__ == '__main__':
    string = sys.argv[1]
    n = sys.argv[2]
    print("Repeating ''{0}'' {1} times".format(string, n))
    print("".join(string for _ in range(0, int(n))))
