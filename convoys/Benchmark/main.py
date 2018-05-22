import re

s1C = 2
s2C = 5
s3C = 3
s4C = 2

def tprint(list):
    time = 195
    cost = 1575
    s1 = 720
    s2 = 360
    s3 = 240
    s4 = 720
    CoB = int((s1*s1C)+(s2*s2C)+(s3*s3C)+(s4*s4C))
    ratio = round(int((s1*s1C)+(s2*s2C)+(s3*s3C)+(s4*s4C))/int(s1+s2+s3+s4), 3)
    c1_Rsend = 18
    c1_Rgather = 45
    c1_Rtransfer = 2
    c1_Rreceive = 4
    c1_transfer = 120
    c1_receive = 180
    c1_storage = 650
    c2_Rsend = 19
    c2_Rgather = 47
    c2_Rtransfer = 4
    c2_Rreceive = 2
    c2_transfer = 180
    c2_receive = 120
    c2_storage = 830

    #input
    itime = round(int(list[0].split("=")[1]),2)
    icost = round(int(list[19].split("=")[1]),2)
    is1 = round(int(list[1].split("=")[1]),2)
    is2 = round(int(list[2].split("=")[1]),2)
    is3 = round(int(list[3].split("=")[1]),2)
    is4 = round(int(list[4].split("=")[1]),2)
    iCoB = round(int((is1*s1C)+(is2*s2C)+(is3*s3C)+(is4*s4C)), 2)
    iratio = round(int((is1*s1C)+(is2*s2C)+(is3*s3C)+(is4*s4C))/int(is1+is2+is3+is4), 3)
    ic1_Rsend = round(int(list[8].split("=")[1]),2)
    ic1_Rgather = round(int(list[7].split("=")[1]),2)
    ic1_Rtransfer = round(int(list[9].split("=")[1]),2)
    ic1_Rreceive = round(int(list[10].split("=")[1]),2)
    ic1_transfer = round(int(list[17].split("=")[1]),2)
    ic1_receive = round(int(list[15].split("=")[1]),2)
    ic1_storage = round(int(list[5].split("=")[1]),2)
    ic2_Rsend = round(int(list[12].split("=")[1]),2)
    ic2_Rgather = round(int(list[11].split("=")[1]),2)
    ic2_Rtransfer = round(int(list[13].split("=")[1]),2)
    ic2_Rreceive = round(int(list[14].split("=")[1]),2)
    ic2_transfer = round(int(list[18].split("=")[1]),2)
    ic2_receive = round(int(list[16].split("=")[1]),2)
    ic2_storage = round(int(list[6].split("=")[1]),2)

    original_string = "\\begin{table}[]\n	\\centering\n	\\begin{minipage}[b]{\\textwidth}\n		\\resizebox{\\textwidth}{!}{" \
           "%\n			\\begin{tabular}{|llllllllll|}\n				\\hline\n				&		&		&		" \
           "&   &	\\multicolumn{5}{c|}{\\cellcolor[HTML]{ABCDEF}Station data}\\\\\n				\\rowcolor[HTML]{" \
           "ABCDEF}\n				&	Time	&	Cost of Bandwidth   &   CoB:ratio	&	Cora: cost	&	1	&	2	&	3	&	" \
           "4	&	Total\\\\\n				Base	&	195	&	5400	&    2.647   &	1575	&	720	&	360	&	240	&	" \
           "720	&	2040\\\\\n				\\rowcolor[HTML]{EFEFEF}\n				Result	&	_time	&	" \
           "_CoB	&  _CoBR\t   &	_cost	&	_s1	&	_s2	&	_s3	&	_s4	&	_total\t\\\\\n				Diff (\\%)	&	" \
           "_timediff	&	_CoBdiff	&   _CoBRdiff\t    &	_costdiff	&	_s1diff	&	_s2diff	&	_s3diff	&	_s4diff	&	" \
           "_totaldiff\t\\\\\\hline\n		\\end{tabular}}\n	\\end{minipage}\n	\\newline\n	\\vspace{-0.25em}\n	" \
           "\\newline\n	\\begin{minipage}[]{\\textwidth}\n		\\resizebox{\\textwidth}{!}{%\n			\\begin{" \
           "tabular}{|lllllll|}\n				\\hline\n				\\rowcolor[HTML]{ABCDEF}\n				&	" \
           "\\multicolumn{3}{c}{\\cellcolor[HTML]{ABCDEF}Convoy1}	&	\\multicolumn{3}{c|}{\\cellcolor[HTML]{" \
           "ABCDEF}Convoy2}\\\\\n				\\rowcolor[HTML]{ABCDEF}\n				&	Base	&	Result	&	" \
           "Diff (\\%)	&	Base	&	Result	&	Diff (\\%)\\\\\n				Runs:send\\_data	&	18	&	" \
           "c1_send_data	&	c1_send_datadiff	&	19	&	c2_send_data	&	c2_send_datadiff	\\\\\n		" \
           "		\\rowcolor[HTML]{EFEFEF}\n				Runs:gather\\_new\\_data	&	45	&	c1_gather	&	" \
           "c1_gatherdiff	&	47	&	c2_gather	&	c2_gatherdiff	\\\\\n				Runs:transfer	&	2	" \
           "&	c1_Rtransfer	&	c1_Rtransferdiff	&	4	&	c2_Rtransfer	&	c2_Rtransferdiff	\\\\\n	" \
           "			\\rowcolor[HTML]{EFEFEF}\n				Runs:receive	&	4	&	c1_Rreceive	&	" \
           "c1_Rreceivediff	&	2	&	c2_Rreceive	&	c2_Rreceivediff	\\\\\n				Transfer	&	120	&	" \
           "c1_Transfer	&	c1_Transferdiff	&	180	&	c2_Transfer	&	c2_Transferdiff	\\\\\n				" \
           "\\rowcolor[HTML]{EFEFEF}\n				Receive	&	180	&	c1_Receive	&	c1_Receivediff	&	120	&	" \
           "c2_Receive	&	c2_Receivediff	\\\\\n				Storage	&	650	&	c1_storage	&	c1_storagediff	" \
           "&	830	&	c2_storage	&	c2_storagediff	\\\\\\hline\n		\\end{tabular}}\n	\\end{minipage}\n	" \
           "\\caption{Mycaption}\n	\\label{my-label}\n\\end{table} "
    original_string = original_string.replace("_time\t", str(itime))
    original_string = original_string.replace("_timediff\t", str(round(itime * 100 / time,1)))
    original_string = original_string.replace("_CoB\t", str(iCoB))
    original_string = original_string.replace("_CoBdiff\t", str(round(iCoB * 100 / CoB,1)))
    original_string = original_string.replace("_CoBR\t", str(iratio))
    original_string = original_string.replace("_CoBRdiff\t", str(round(iratio * 100 / ratio,1)))
    original_string = original_string.replace("_cost\t", str(icost))
    original_string = original_string.replace("_costdiff\t", str(round(icost * 100 / cost,1)))
    original_string = original_string.replace("_s1\t", str(is1))
    original_string = original_string.replace("_s1diff\t", str(round(is1 * 100 / s1,1)))
    original_string = original_string.replace("_s2\t", str(is2))
    original_string = original_string.replace("_s2diff\t", str(round(is2 * 100 / s2,1)))
    original_string = original_string.replace("_s3\t", str(is3))
    original_string = original_string.replace("_s3diff\t", str(round(is3 * 100 / s3,1)))
    original_string = original_string.replace("_s4\t", str(is4))
    original_string = original_string.replace("_s4diff\t", str(round(is4 * 100 / s4,1)))
    original_string = original_string.replace("_total\t", str(is1+is2+is3+is4))
    original_string = original_string.replace("_totaldiff\t", str(round((is1+is2+is3+is4) * 100 / (s1+s2+s3+s4),1)))
    original_string = original_string.replace("c1_send_data\t", str(ic1_Rsend))
    original_string = original_string.replace("c1_send_datadiff\t", str(round(ic1_Rsend * 100 / c1_Rsend,1)))
    original_string = original_string.replace("c2_send_data\t", str(ic2_Rsend))
    original_string = original_string.replace("c2_send_datadiff\t", str(round(ic2_Rsend * 100 / c2_Rsend,1)))
    original_string = original_string.replace("c1_gather\t", str(ic1_Rgather))
    original_string = original_string.replace("c1_gatherdiff\t", str(round(ic1_Rgather * 100 / c1_Rgather,1)))
    original_string = original_string.replace("c2_gather\t", str(ic2_Rgather))
    original_string = original_string.replace("c2_gatherdiff\t", str(round(ic2_Rgather * 100 / c2_Rgather,1)))
    original_string = original_string.replace("c1_Rtransfer\t", str(ic1_Rtransfer))
    if (c1_Rtransfer == 0):
        original_string = original_string.replace("c1_Rtransferdiff\t","0")
    else:
        original_string = original_string.replace("c1_Rtransferdiff\t", str(round(ic1_Rtransfer * 100 / c1_Rtransfer,1)))
    original_string = original_string.replace("c2_Rtransfer\t", str(ic2_Rtransfer))
    original_string = original_string.replace("c2_Rtransferdiff\t", str(round(ic2_Rtransfer * 100 / c2_Rtransfer,1)))
    original_string = original_string.replace("c1_Rreceive\t", str(ic1_Rreceive))
    original_string = original_string.replace("c1_Rreceivediff\t", str(round(ic1_Rreceive * 100 / c1_Rreceive,1)))
    original_string = original_string.replace("c2_Rreceive\t", str(ic2_Rreceive))
    if (c2_Rreceive == 0):
        original_string = original_string.replace("c2_Rreceivediff\t","0")
    else:
        original_string = original_string.replace("c2_Rreceivediff\t", str(round(ic2_Rreceive * 100 / c2_Rreceive,1)))
    original_string = original_string.replace("c1_Transfer\t", str(ic1_transfer))
    if (c1_transfer == 0):
        original_string = original_string.replace("c1_Transferdiff\t","0")
    else:
        original_string = original_string.replace("c1_Transferdiff\t", str(round(ic1_transfer * 100 / c1_transfer,1)))
    original_string = original_string.replace("c2_Transfer\t", str(ic2_transfer))
    original_string = original_string.replace("c2_Transferdiff\t", str(round(ic2_transfer * 100 / c2_transfer,1)))
    original_string = original_string.replace("c1_Receive\t", str(ic1_receive))
    original_string = original_string.replace("c1_Receivediff\t", str(round(ic1_receive * 100 / c1_receive,1)))
    original_string = original_string.replace("c2_Receive\t", str(ic2_receive))
    if (c2_receive == 0):
        original_string = original_string.replace("c2_Receivediff\t","0")
    else:
        original_string = original_string.replace("c2_Receivediff\t", str(round(ic2_receive * 100 / c2_receive,1)))
    original_string = original_string.replace("c1_storage\t", str(ic1_storage))
    original_string = original_string.replace("c1_storagediff\t", str(round(ic1_storage * 100 / c1_storage,1)))
    original_string = original_string.replace("c2_storage\t", str(ic2_storage))
    original_string = original_string.replace("c2_storagediff\t", str(round(ic2_storage * 100 / c2_storage,1)))
    return original_string


if __name__ == '__main__':
    nbr_list = [2, 4, 6, 8, 10, 15, 16, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 143]
    with open("test", "r") as data_file:
        var_list = []
        for line in reversed(list(data_file)):
            if (line[:9] == 'TotalTime'):
                vars = line.split(' ')
                for i, var in enumerate(vars):
                    #print(i, var)
                    if i in nbr_list:
                        var_list.append(var)
                break
        for i, var in enumerate(var_list):
            pass#print(i, var)
        print(tprint(var_list))
