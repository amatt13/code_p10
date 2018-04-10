#Created by Anders!
import subprocess
import argparse
import os
import datetime
import re

my_location = os.path.dirname(os.path.realpath(__file__)) + "/"
linux = 'linux'

class Exp:
    def __init__(self, price: int, time: int, data: list, clocks: list, delays: list, runs: list):
        self.price = price
        self.time = time
        self.data = data
        self.clocks = clocks
        self.delays = delays
        self.runs = runs

    def comp_price(self, price):
        return (int(price)/self.price) * 100

    def comp_time(self, time):
        return (time/self.time) * 100

    def comp_data(self, data: list):
        result = []
        for i, d in enumerate(data):
            try:
                result.append(int(d)/int(self.data[i]) * 100)
            except ZeroDivisionError:
                result.append(0)
        return result

    def comp_clocks(self, clock, index: int):
        result = []
        try:
            return int(clock)/int(self.clocks[index].split("\t")[1]) * 100
        except ZeroDivisionError:
            return 0

    def comp_delays(self, delay, index: int):
        if int(delay) == 0 and int(self.delays[index].split("\t")[1]) == 0:
            return 100
        try:
            return int(delay)/int(self.delays[index].split("\t")[1]) * 100
        except ZeroDivisionError:
            return "inf"

    def comp_runs(self, run, index: int):
        if int(run) == 0 and int(self.runs[index].split("\t")[1]) == 0:
            return 100
        try:
            return int(run)/int(self.runs[index].split("\t")[1]) * 100
        except ZeroDivisionError:
            return "inf"

def linux_machine(OS_name: str):
    return OS_name == linux


def get_clocks():
    results = []
    clocks = re.findall("( p[0-9]+.idle[<=]+[0-9]+| p[0-9]+.wait[<=]+[0-9]+| p[0-9]+.work[<=]+[0-9]+| p[0-9]+.slew[<=]+[0-9]+)", line)
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

def construct_genral(name, time, earth, gathered, transferred):
    return "{0} & {1} & {2} & {3} & {4} \\\\ \\hline".format(name, earth, gathered, transferred, time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Benchmark tool for UPPAAL models')
    parser.add_argument('-o', type=str, required=False, help='OS name')
    parser.add_argument('-i', type=int, required=False, help='Number of iterations to run', default=1)
    parser.add_argument('--w', action='store_true', required=False, help='Write results to a file (set --t to get a trace)')
    parser.add_argument('--t', action='store_true', required=False, help='Generate and show some trace')
    parser.add_argument('--s', action='store_true', required=False, help='Reduces output')
    args = parser.parse_args()

    OS = args.o
    if args.o is None:
        OS = linux
    w = args.w
    t = y = s = q = ""

    if args.t:
        t = "-t0"
        y = "-y"
    if args.s:
        s = "-s"
        q = "-q"

    time_measurements = []
    my_location_windows = my_location.replace("/", "\\")
    
    write(str(datetime.datetime.now()))
    # base
    base_time = 0
    base_price = 0
    base_clocks = []
    base_delays = []
    base_runs = []
    base_data = []
    with open(my_location + "/base/base.xml") as base:
        write("base.xml")
        short_name = "base"
        times = []
        with open(my_location + "benchmark_trace", 'w') as trace_file:
            output = None
            if w:
                output = trace_file
            p1 = None
            print("Current model:base.xml")
            start = datetime.datetime.now()
            if linux_machine(OS):
                subprocess.Popen([my_location + "./verifyta", my_location + "/base/base.xml", my_location + "classic.q",
                                  "-o1", t, y], stdout=output, stderr=output).wait()
            else:
                subprocess.Popen(my_location_windows + "verifyta.exe -o1 " + t + " "  + y  + " " + my_location_windows + model + " " + my_location_windows + "classic.q", stdout=output, stderr=output).wait()
            end = datetime.datetime.now()
            time = end - start
            base_time = time.total_seconds()
            times.append(base_time)
            write(str(times[-1]))
            print("Done:base.xml")
        with open('benchmark_trace', 'r') as trace:
            for line in reversed(list(trace)):
                t_time = re.findall("(t_time[>=]+[0-9]+)", line)
                base_price = re.findall("(band_cost\=[0-9]+)", line)
                if t_time and base_price:
                    base_price = base_price[0].split('=')[1]
                    write(base_price)
                    earth = re.findall("(data_earth\=[0-9]+)", line)[0].split('=')[1]
                    storage = re.findall("(data_gathered\=[0-9]+)", line)[0].split('=')[1]
                    internal = re.findall("(data_internal\=[0-9]+)", line)[0].split('=')[1]
                    base_data.append(earth)
                    base_data.append(storage)
                    base_data.append(internal)
                    write(earth)
                    write(storage)
                    write(internal)
                    clocks_str = short_name
                    for clock in get_clocks():
                        clock_rep = "{0}\t{1}".format(clock[0], clock[1])
                        write(clock_rep.split("\t")[1])
                        base_clocks.append(clock_rep)
                        clocks_str += " & {0}".format(clock[1])
                    clocks_str += " \\\\ \\hline"
                    delays_str = short_name
                    for d in get_delays():
                        d = d.replace("=", "\t")
                        write(d.split("\t")[1]) # delays[0][1]=15 
                        base_delays.append(d)
                        delays_str += " & {0}".format(d.split("\t")[1])
                    delays_str += " \\\\ \\hline"
                    runs_str = short_name
                    for r in get_runs():
                        r = r.replace("=", "\t")
                        write(r.split("\t")[1])
                        base_runs.append(r)
                        runs_str += " & {0}".format(r.split("\t")[1])
                    runs_str += " \\\\ \\hline"
                    print(construct_genral(name=short_name, time=str(base_time), earth=earth, gathered=storage, transferred=internal))
                    print(clocks_str)
                    print(delays_str)
                    print(runs_str)
                    break
            write("\n")

    # models
    base_exp = Exp(price=int(base_price), time=base_time, data=base_data, clocks=base_clocks, delays=base_delays, runs=base_runs)
    for model in os.listdir(os.getcwd()):
        i = 0    
        splits = model.split('.')
        if len(splits) == 2 and splits[1] == 'xml':
            write(model)
            short_name = splits[0]
            times = []
            with open(my_location + "benchmark_trace", 'w') as trace_file:
                while i < args.i:
                    i += 1
                    output = None
                    if w:
                        output = trace_file
                    p1 = None
                    print("Current model:{0}".format(model))
                    start = datetime.datetime.now()
                    if linux_machine(OS):
                        subprocess.Popen([my_location + "./verifyta", my_location + model, my_location + "classic.q",
                                          "-o1", t, y], stdout=output, stderr=output).wait()
                    else:
                        subprocess.Popen(my_location_windows + "verifyta.exe -o1 " + t + " "  + y  + " " + my_location_windows + model + " " + my_location_windows + "classic.q", stdout=output, stderr=output).wait()
                    end = datetime.datetime.now()
                    time = end - start
                    total_seconds = time.total_seconds()
                    times.append(total_seconds)
                    write("{0}\t{1}".format(total_seconds, base_exp.comp_time(total_seconds)))
                    print("Done:{0}".format(model))
            with open('benchmark_trace', 'r') as trace:
                for line in reversed(list(trace)):
                    t_time = re.findall("(t_time[>=]+[0-9]+)", line)
                    price = re.findall("(band_cost\=[0-9]+)", line)
                    if t_time and price:
                        price = price[0].split('=')[1]
                        write("{0}\t{1}".format(price, base_exp.comp_price(price)))
                        earth = re.findall("(data_earth\=[0-9]+)", line)[0].split('=')[1]
                        storage = re.findall("(data_gathered\=[0-9]+)", line)[0].split('=')[1]
                        internal = re.findall("(data_internal\=[0-9]+)", line)[0].split('=')[1]
                        d_r = base_exp.comp_data([earth, storage, internal])
                        write(earth + "\t" + str(d_r[0]))
                        write(storage + "\t" + str(d_r[1]))
                        write(internal + "\t" + str(d_r[2]))
                        clocks_str = short_name
                        for i, clock in enumerate(get_clocks()):
                            write("{0}\t{1}".format(clock[1], base_exp.comp_clocks(clock[1], i)))
                            clocks_str += " & {0}".format(clock[1])
                        clocks_str += " \\\\ \\hline"
                        delays_str = short_name
                        for index, d in enumerate(get_delays()):
                            d = d.replace("=", "\t").split("\t")[1]
                            write("{0}\t{1}".format(d, base_exp.comp_delays(d, index))) # delays[0][1]=15 
                            delays_str += " & {0}".format(d)
                        delays_str += " \\\\ \\hline"
                        runs_str = short_name
                        for index, r in enumerate(get_runs()):
                            r = r.replace("=", "\t").split("\t")[1]
                            write("{0}\t{1}".format(r, base_exp.comp_runs(r, index)))
                            runs_str += " & {0}".format(r)
                        runs_str += " \\\\ \\hline"
                        print(construct_genral(name=short_name, time=str(total_seconds), earth=earth, gathered=storage, transferred=internal))
                        print(clocks_str)
                        print(delays_str)
                        print(runs_str)
                        break
                write("\n")
    for times in time_measurements:
        print("Average time: " + str(sum(times) / len(times)))



