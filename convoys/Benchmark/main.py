import re


def tprint(list):
    time = 195
    CoB = 7500
    cost = 1230
    s1 = 1320
    s2 = 0
    s3 = 360
    s4 = 1440
    c1_Rsend = 11
    c1_Rgather = 60
    c1_Rtransfer = 6
    c1_Rreceive = 2
    c1_transfer = 360
    c1_receive = 120
    c2_Rsend = 17
    c2_Rgather = 61
    c2_Rtransfer = 2
    c2_Rreceive = 6
    c2_transfer = 120
    c2_receive = 360

    original_string = "\\begin{table}[]\n	\\centering\n		\\begin{minipage}[b]{\\textwidth}\n		\\resizebox{" \
                      "\\textwidth}{!}{%\n			\\begin{tabular}{|llllllll|}\n				\\hline\n			" \
                      "		&		&		&		&	\\multicolumn{4}{c|}{\\cellcolor[HTML]{" \
                      "ABCDEF}Stationdata}\\\\\n				\\rowcolor[HTML]{ABCDEF}\n					&	" \
                      "Time	&	CostofBandwidth	&	Cora:cost	&	1	&	2	&	3	&	4\\\\\n				" \
                      "Base	&	195	&	7500	&	1230	&	1320	&	0	&	360	&	1440\\\\\n				" \
                      "\\rowcolor[HTML]{EFEFEF}\n				Result	&	_time	&	_CoB	&	_cost	&	_s1	" \
                      "&	_s2	&	_s3	&	_s4\\\\\n				Diff(\\%)	&	_timediff	&	_CoBdiff	&	" \
                      "_costdiff	&	_s1diff	&	_s2diff	&	_s3diff	&	_s4diff\\\\\\hline\n			\\end{" \
                      "tabular}}\n	\\end{minipage}\n	\\newline\n	\\vspace{-0.25em}\n	\\newline\n	\\begin{minipage}[" \
                      "]{\\textwidth}\n		\\resizebox{\\textwidth}{!}{%\n			\\begin{tabular}{|lllllll|}\n	" \
                      "		\\hline\n			\\rowcolor[HTML]{ABCDEF}\n				&	\\multicolumn{3}{c}{" \
                      "\\cellcolor[HTML]{ABCDEF}Convoy1}	&	\\multicolumn{3}{c|}{\\cellcolor[HTML]{" \
                      "ABCDEF}Convoy2}\\\\\n			\\rowcolor[HTML]{ABCDEF}\n				&	Base	&	" \
                      "Result	&	Diff(\\%)	&	Base	&	Result	&	Diff(\\%)\\\\\n			" \
                      "Runs:send\\_data	&	11	&	c1_send_data	&	c1_send_datadiff	&	17	&	" \
                      "c2_send_data	&	c2_send_datadiff\\\\\n			\\rowcolor[HTML]{EFEFEF}\n			" \
                      "Runs:gather\\_new\\_data	&	60	&	c1_gather	&	c1_gatherdiff	&	61	&	c2_gather	" \
                      "&	c2_gatherdiff\\\\\n			Runs:transfer	&	6	&	c1_Rtransfer	&	" \
                      "c1_Rtransferdiff	&	2	&	c2_Rtransfer	&	c2_Rtransferdiff\\\\\n			\\rowcolor[" \
                      "HTML]{EFEFEF}\n			Runs:receive	&	2	&	c1_Rreceive	&	c1_Rreceivediff	&	6	" \
                      "&	c2_Rreceive	&	c2_Rreceivediff\\\\\n			Transfer	&	360	&	c1_Transfer	&	" \
                      "c1_Transferdiff	&	120	&	c2_Transfer	&	c2_Transferdiff\\\\\n			\\rowcolor[HTML]{" \
                      "EFEFEF}\n			Receive	&	120	&	c1_Receive	&	c1_Receivediff	&	360	&	" \
                      "c2_Receive	&	c2_Receivediff\\\\\\hline\n		\\end{tabular}}\n	\\end{minipage}\n	" \
                      "\\caption{Mycaption}\n	\\label{my-label}\n\\end{table} "
    original_string = original_string.replace("_time\t", list[0].split("=")[1])
    original_string = original_string.replace("_timediff\t", str(int(list[0].split("=")[1]) * 100 / time))
    return original_string


if __name__ == '__main__':
    nbr_list = [2, 4, 6, 8, 10, 15, 16, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 143]
    with open("test", "r") as data_file:
        var_list = []
        for line in reversed(list(data_file)):
            if (line[:9] == 'TotalTime'):
                vars = line.split(' ')
                for i, var in enumerate(vars):
                    if i in nbr_list:
                        var_list.append(var)
                break
        for i, var in enumerate(var_list):
            print(i, var)
        print(tprint(var_list))
