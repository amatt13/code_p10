import re

s1C = 2
s2C = 5
s3C = 3
s4C = 2


def calc(arg1, arg2, decimals):
    if arg1 == 0 and arg2 != 0:
        return "\\textbf{N/A}"
    elif arg1 > arg2:
        return "\\textbf{" + str(round((((arg1 - arg2) / arg1) * -1) * 100, decimals)) + "}"
    elif arg1 < arg2:
        return "\\textbf{+" + str(round(((arg2 - arg1) / arg1) * 100, decimals)) + "}"
    else:
        return "\\textbf{" + str(0) + "}"


def tprint(list):
    time = 200
    cost = 2600
    s1 = 840
    s2 = 360
    s3 = 420
    s4 = 840
    CoB = int((s1 * s1C) + (s2 * s2C) + (s3 * s3C) + (s4 * s4C))
    ratio = round(int((s1 * s1C) + (s2 * s2C) + (s3 * s3C) + (s4 * s4C)) / int(s1 + s2 + s3 + s4), 3)
    c1_Rsend = 20
    c1_Rgather = 50
    c1_Rtransfer = 6
    c1_Rreceive = 2
    c1_transfer = 360
    c1_receive = 120
    c1_storage = 410
    c2_Rsend = 24
    c2_Rgather = 38
    c2_Rtransfer = 2
    c2_Rreceive = 6
    c2_transfer = 120
    c2_receive = 360
    c2_storage = 530

    # input
    itime = round(int(list[0].split("=")[1]), 2)
    icost = round(int(list[19].split("=")[1]), 2)
    is1 = round(int(list[1].split("=")[1]), 2)
    is2 = round(int(list[2].split("=")[1]), 2)
    is3 = round(int(list[3].split("=")[1]), 2)
    is4 = round(int(list[4].split("=")[1]), 2)
    iCoB = round(int((is1 * s1C) + (is2 * s2C) + (is3 * s3C) + (is4 * s4C)), 2)
    iratio = round(int((is1 * s1C) + (is2 * s2C) + (is3 * s3C) + (is4 * s4C)) / int(is1 + is2 + is3 + is4), 3)
    ic1_Rsend = round(int(list[8].split("=")[1]), 2)
    ic1_Rgather = round(int(list[7].split("=")[1]), 2)
    ic1_Rtransfer = round(int(list[9].split("=")[1]), 2)
    ic1_Rreceive = round(int(list[10].split("=")[1]), 2)
    ic1_transfer = round(int(list[17].split("=")[1]), 2)
    ic1_receive = round(int(list[15].split("=")[1]), 2)
    ic1_storage = round(int(list[5].split("=")[1]), 2)
    ic2_Rsend = round(int(list[12].split("=")[1]), 2)
    ic2_Rgather = round(int(list[11].split("=")[1]), 2)
    ic2_Rtransfer = round(int(list[13].split("=")[1]), 2)
    ic2_Rreceive = round(int(list[14].split("=")[1]), 2)
    ic2_transfer = round(int(list[18].split("=")[1]), 2)
    ic2_receive = round(int(list[16].split("=")[1]), 2)
    ic2_storage = round(int(list[6].split("=")[1]), 2)

    original_string = "\\begin{table}[h]\n	\\centering\n	\\begin{minipage}[b]{\\textwidth}\n		\\resizebox{\\textwidth}{!}{" \
                      "%\n			\\begin{tabular}{|llllllllll|}\n				\\hline\n				&		&		&		" \
                      "&   &	\\multicolumn{5}{c|}{\\cellcolor[HTML]{ABCDEF}Station data}\\\\\n				\\rowcolor[HTML]{" \
                      "ABCDEF}\n				&	Time	&	Cost of Bandwidth   &   CoB:ratio	&	Cora: cost	&	1	&	2	&	3	&	" \
                      "4	&	Total\\\\\n				Base	&	200	&	6420	&    2.61   &	2600	&	840	&	360	&	420	&	" \
                      "840	&	2460\\\\\n				\\rowcolor[HTML]{EFEFEF}\n				Result	&	_time	&	" \
                      "_CoB	&  _CoBR\t   &	_cost	&	_s1	&	_s2	&	_s3	&	_s4	&	_total\t\\\\\n				Diff (\\%)	&	" \
                      "_timediff	&	_CoBdiff	&   _CoBRdiff\t    &	_costdiff	&	_s1diff	&	_s2diff	&	_s3diff	&	_s4diff	&	" \
                      "_totaldiff\t\\\\\\hline\n		\\end{tabular}}\n	\\end{minipage}\n	\\newline\n	\\vspace{-0.25em}\n	" \
                      "\\newline\n	\\begin{minipage}[]{\\textwidth}\n		\\resizebox{\\textwidth}{!}{%\n			\\begin{" \
                      "tabular}{|lllllll|}\n				\\hline\n				\\rowcolor[HTML]{ABCDEF}\n				&	" \
                      "\\multicolumn{3}{c}{\\cellcolor[HTML]{ABCDEF}Convoy1}	&	\\multicolumn{3}{c|}{\\cellcolor[HTML]{" \
                      "ABCDEF}Convoy2}\\\\\n				\\rowcolor[HTML]{ABCDEF}\n				&	Base	&	Result	&	" \
                      "Diff (\\%)	&	Base	&	Result	&	Diff (\\%)\\\\\n				Runs:send\\_data	&	20	&	" \
                      "c1_send_data	&	c1_send_datadiff	&	24	&	c2_send_data	&	c2_send_datadiff	\\\\\n		" \
                      "		\\rowcolor[HTML]{EFEFEF}\n				Runs:gather\\_new\\_data	&	50	&	c1_gather	&	" \
                      "c1_gatherdiff	&	38	&	c2_gather	&	c2_gatherdiff	\\\\\n				Runs:transfer	&	6	" \
                      "&	c1_Rtransfer	&	c1_Rtransferdiff	&	2	&	c2_Rtransfer	&	c2_Rtransferdiff	\\\\\n	" \
                      "			\\rowcolor[HTML]{EFEFEF}\n				Runs:receive	&	2	&	c1_Rreceive	&	" \
                      "c1_Rreceivediff	&	6	&	c2_Rreceive	&	c2_Rreceivediff	\\\\\n				Transfer	&	360	&	" \
                      "c1_Transfer	&	c1_Transferdiff	&	120	&	c2_Transfer	&	c2_Transferdiff	\\\\\n				" \
                      "\\rowcolor[HTML]{EFEFEF}\n				Receive	&	120	&	c1_Receive	&	c1_Receivediff	&	360	&	" \
                      "c2_Receive	&	c2_Receivediff	\\\\\n				Storage	&	410	&	c1_storage	&	c1_storagediff	" \
                      "&	530	&	c2_storage	&	c2_storagediff	\\\\\\hline\n		\\end{tabular}}\n	\\end{minipage}\n	" \
                      "\\caption{Mycaption}\n	\\label{my-label}\n\\end{table} "
    original_string = original_string.replace("_time\t", str(itime))
    original_string = original_string.replace("_timediff\t", calc(time, itime, 1))
    original_string = original_string.replace("_CoB\t", str(iCoB))
    original_string = original_string.replace("_CoBdiff\t", calc(CoB, iCoB, 1))
    original_string = original_string.replace("_CoBR\t", str(iratio))
    original_string = original_string.replace("_CoBRdiff\t", calc(ratio, iratio, 1))
    original_string = original_string.replace("_cost\t", str(icost))
    original_string = original_string.replace("_costdiff\t", calc(cost, icost, 1))
    original_string = original_string.replace("_s1\t", str(is1))
    original_string = original_string.replace("_s1diff\t", calc(s1, is1, 1))
    original_string = original_string.replace("_s2\t", str(is2))
    original_string = original_string.replace("_s2diff\t", calc(s2, is2, 1))
    original_string = original_string.replace("_s3\t", str(is3))
    original_string = original_string.replace("_s3diff\t", calc(s3, is3, 1))
    original_string = original_string.replace("_s4\t", str(is4))
    original_string = original_string.replace("_s4diff\t", calc(s4, is4, 1))
    original_string = original_string.replace("_total\t", str(is1 + is2 + is3 + is4))
    original_string = original_string.replace("_totaldiff\t", calc((s1 + s2 + s3 + s4), (is1 + is2 + is3 + is4), 2))
    original_string = original_string.replace("c1_send_data\t", str(ic1_Rsend))
    original_string = original_string.replace("c1_send_datadiff\t", calc(c1_Rsend, ic1_Rsend, 1))
    original_string = original_string.replace("c2_send_data\t", str(ic2_Rsend))
    original_string = original_string.replace("c2_send_datadiff\t", calc(c2_Rsend, ic2_Rsend, 1))
    original_string = original_string.replace("c1_gather\t", str(ic1_Rgather))
    original_string = original_string.replace("c1_gatherdiff\t", calc(c1_Rgather, ic1_Rgather, 1))
    original_string = original_string.replace("c2_gather\t", str(ic2_Rgather))
    original_string = original_string.replace("c2_gatherdiff\t", calc(c2_Rgather, ic2_Rgather, 1))
    original_string = original_string.replace("c1_Rtransfer\t", str(ic1_Rtransfer))
    original_string = original_string.replace("c1_Rtransferdiff\t", calc(c1_Rtransfer, ic1_Rtransfer, 1))
    original_string = original_string.replace("c2_Rtransfer\t", str(ic2_Rtransfer))
    original_string = original_string.replace("c2_Rtransferdiff\t", calc(c2_Rtransfer, ic2_Rtransfer, 1))
    original_string = original_string.replace("c1_Rreceive\t", str(ic1_Rreceive))
    original_string = original_string.replace("c1_Rreceivediff\t", calc(c1_Rreceive, ic1_Rreceive, 1))
    original_string = original_string.replace("c2_Rreceive\t", str(ic2_Rreceive))
    original_string = original_string.replace("c2_Rreceivediff\t", calc(c2_Rreceive, ic2_Rreceive, 1))
    original_string = original_string.replace("c1_Transfer\t", str(ic1_transfer))
    original_string = original_string.replace("c1_Transferdiff\t", calc(c1_transfer, ic1_transfer, 1))
    original_string = original_string.replace("c2_Transfer\t", str(ic2_transfer))
    original_string = original_string.replace("c2_Transferdiff\t", calc(c2_transfer, ic2_transfer, 1))
    original_string = original_string.replace("c1_Receive\t", str(ic1_receive))
    original_string = original_string.replace("c1_Receivediff\t", calc(c1_receive, ic1_receive, 1))
    original_string = original_string.replace("c2_Receive\t", str(ic2_receive))
    original_string = original_string.replace("c2_Receivediff\t", calc(c2_receive, ic2_receive, 1))
    original_string = original_string.replace("c1_storage\t", str(ic1_storage))
    original_string = original_string.replace("c1_storagediff\t", calc(c1_storage, ic1_storage, 1))
    original_string = original_string.replace("c2_storage\t", str(ic2_storage))
    original_string = original_string.replace("c2_storagediff\t", calc(c2_storage, ic2_storage, 1))
    return original_string


if __name__ == '__main__':
    nbr_list = [0, 4, 6, 8, 10, 15, 16, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 143]
    # nbr_list = [2, 4, 6, 8, 10, 15, 16, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 207]
    with open("test", "r") as data_file:
        var_list = []
        for line in reversed(list(data_file)):
            if (line[:9] == 'TotalTime'):
                vars = line.split(' ')
                for i, var in enumerate(vars):
                    print(i, var)
                    if i in nbr_list:
                        var_list.append(var)
                break
        for i, var in enumerate(var_list):
            print(i, var)
        print(tprint(var_list))
