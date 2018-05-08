# Created by Anders!
import subprocess
import argparse
import os
import datetime
import re

my_location = os.path.dirname(os.path.realpath(__file__)) + "/"


def linux_machine(OS_name: str):
    return OS_name == linux


def get_clocks():
    results = []
    clocks = re.findall(
        "( p[0-9]+.idle[<=]+[0-9]+| p[0-9]+.wait[<=]+[0-9]+| p[0-9]+.work[<=]+[0-9]+| p[0-9]+.slew[<=]+[0-9]+)", line)
    for c in clocks:
        splits = c.split("<=")
        results.append((splits[0].replace(" ", ""), splits[1]))
    return results


def get_delays():
    return re.findall("(delays\[[0-9]+\]\[[0-9]+\]=[0-9]+)", line)


def get_runs():
    return re.findall("(runs\[[0-9]+\]\[[0-9]+\]=[0-9]+)", line)


def write(text, newline=True):
    text = str(text)
    with open('results', 'a') as results:
        if newline:
            text += "\n"
        results.write(text)


if __name__ == '__main__':
    write(str(datetime.datetime.now()))
    # models
    for model in os.listdir(os.getcwd()):
        i = 0
        count = 0
        splits = model.split('.')
        if len(splits) == 2 and splits[1] == 'xml':
            write(model)
            short_name = splits[0]
            times = []
            with open(my_location + "benchmark_trace", 'w') as trace_file:
                output = trace_file
                p1 = None
                count += 1
                print("{0} - Current model:{1}".format(count, model))
                start = datetime.datetime.now()
                subprocess.Popen(
                    [my_location + "./verifyta", my_location + model, my_location + "classic.q", "-o1", "-t0", "-y", "-q", "-s"],
                    stdout=output, stderr=output).wait()
                end = datetime.datetime.now()
                time = end - start
                total_seconds = time.total_seconds()
                write("{0}".format(total_seconds))
                print("Done:{0}".format(model))
            with open('benchmark_trace', 'r') as trace:
                for line in reversed(list(trace)):
                    t_time = re.findall("(t_time[>=]+[0-9]+)", line)
                    price = re.findall("(band_cost\=[0-9]+)", line)
                    if t_time and price:
                        price = price[0].split('=')[1]
                        write("{0}".format(price))
                        earth = re.findall("(data_earth\=[0-9]+)", line)[0].split('=')[1]
                        storage = re.findall("(data_gathered\=[0-9]+)", line)[0].split('=')[1]
                        internal = re.findall("(data_internal\=[0-9]+)", line)[0].split('=')[1]
                        write(earth)
                        write(storage)
                        write(internal)
                        runs0 = []
                        runs1 = []
                        runs2 = []
                        runs3 = []
                        delays0 = []
                        delays1 = []
                        delays2 = []
                        delays3 = []
                        idles = []
                        waits = []
                        works = []
                        slews = []
                        for i, clock in enumerate(get_clocks()):
                            write("{0}".format(clock[1]))
                            if 'idle' in clock[0]:
                                idles.append(clock[1])
                            elif 'work' in clock[0]:
                                works.append(clock[1])
                            elif 'wait' in clock[0]:
                                waits.append(clock[1])
                            else:
                                slews.append(clock[1])
                        for index, d in enumerate(get_delays()):
                            splits = d.replace("=", "\t").split("\t")
                            name = str(splits[0])
                            d = str(splits[1])
                            write("{0}".format(d))  # delays[0][1]=15
                            if '][0]' in name:
                                delays0.append(d)
                            elif '][1]' in name:
                                delays1.append(d)
                            elif '][2]' in name:
                                delays2.append(d)
                            else:
                                delays3.append(d)
                        for index, r in enumerate(get_runs()):
                            splits = r.replace("=", "\t").split("\t")
                            name = str(splits[0])
                            r = str(splits[1])
                            write("{0}".format(r))
                            if '][0]' in name:
                                runs0.append(r)
                            elif '][1]' in name:
                                runs1.append(r)
                            elif '][2]' in name:
                                runs2.append(r)
                            else:
                                runs3.append(r)
                        print("\t\t\t".join(runs0) + "\n" +
                              "\t\t\t".join(runs1) + "\n" +
                              "\t\t\t".join(runs2) + "\n" +
                              "\t\t\t".join(runs3) + "\n" +
                              "\t\t\t".join(delays0) + "\n" +
                              "\t\t\t".join(delays1) + "\n" +
                              "\t\t\t".join(delays2) + "\n" +
                              "\t\t\t".join(delays3) + "\n" +
                              "\t\t\t".join(idles) + "\n" +
                              "\t\t\t".join(waits) + "\n" +
                              "\t\t\t".join(works) + "\n" +
                              "\t\t\t".join(slews) + "\n" +
                              str(total_seconds) + "\t" + str(price) + "\t" + str(earth) + "\t" + str(storage) + "\t" + str(internal))
                        break
                write("\n")

# r[0][0]			r[1][0]			r[2][]
# r[0][1]			r[1][1]			...
# ...
# d[0][]0 ...
# ...
# idle0			idle1			idle2
# wait..
# work...
# slew...
# time	cost	data_earth	data_gathered	data_trans
