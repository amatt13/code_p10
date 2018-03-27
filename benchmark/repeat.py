import sys

if __name__ == '__main__':
    string = sys.argv[1]
    n = sys.argv[2]
    print("Repeating ''{0}'' {1} times".format(string, n))
    result = ""
    i = 0 
    while i < int(n):
        result += string
        i += 1
    print(result)
