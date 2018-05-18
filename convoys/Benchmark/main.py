import re
if __name__ == '__main__':
    nbr_list = [2, 4, 6, 8, 10, 15, 16, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 143]
    with open("test", "r") as data_file:
        var_list = []
        for line in reversed(list(data_file)):
            if(line[:9] == 'TotalTime'):
                vars = line.split(' ')
                for i, var in enumerate(vars):
                    if i in nbr_list:
                        var_list.append(var)
                break
        for var in var_list:
            print(var)