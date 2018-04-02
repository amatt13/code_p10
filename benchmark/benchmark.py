#Created by Anders!
import subprocess
import argparse
import os
import datetime
import re

my_location = os.path.dirname(os.path.realpath(__file__)) + "/"
linux = 'linux'


def linux_machine(OS_name: str):
    return OS_name == linux


def get_clocks():
    results = []
    clocks = re.findall("( p[0-9]+.idle[<=]+[0-9]+| p[0-9]+.wait[<=]+[0-9]+| p[0-9]+.work[<=]+[0-9]+| p[0-9]+.slew[<=]+[0-9]+)", line)
    for c in clocks:
        splits = c.split("<=")
        results.append((splits[0].replace(" ", ""), splits[1]))
    return results


def get_delays(first):
    return re.findall("(delays\["+str(first)+"\]\[[0-9]+\]=[0-9]+)", line)


def get_runs(first):
    return re.findall("(runs\["+str(first)+"\]\[[0-9]+\]=[0-9]+)", line)

def write(text, newline=True):
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
    for model in os.listdir(os.getcwd()):
        i = 0    
        try:
            splits = model.split('.')
            if splits[1] == 'xml':
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
                        write(str(i) + ": " + str(times[-1]))
                        print("Done:{0}".format(model))
                with open('benchmark_trace', 'r') as trace:
                    for line in reversed(list(trace)):
                        t_time = re.findall("(t_time[>=]+[0-9]+)", line)
                        if t_time:
                            earth = re.findall("(data_earth\=[0-9]+)", line)[0].split('=')[1]
                            storage = re.findall("(data_gathered\=[0-9]+)", line)[0].split('=')[1]
                            internal = re.findall("(data_internal\=[0-9]+)", line)[0].split('=')[1]
                            write("data_earth:\t" + earth)
                            write("data_storage:\t" + storage)
                            write('data_internal:\t' + internal)
                            clocks_str = short_name
                            for clock in get_clocks():
                                write("{0}\t{1}".format(clock[0], clock[1]))
                                clocks_str += " & {0}".format(clock[1])
                            clocks_str += " \\\\ \\hline"
                            delays_str = short_name
                            for i in range(0, 3):
                                items = get_delays(i)
                                for item in items:
                                    write(item) # delays[0][1]=15 
                                    delays_str += " & {0}".format(item.split("=")[1])
                            delays_str += " \\\\ \\hline"
                            runs_str = short_name
                            for i in range(0, 3):
                                items = get_runs(i)
                                for item in items:
                                    write(item)
                                    runs_str += " & {0}".format(item.split("=")[1])
                            runs_str += " \\\\ \\hline"
                            print(construct_genral(name=short_name, time=str(total_seconds), earth=earth, gathered=storage, transferred=internal))
                            print(clocks_str)
                            print(delays_str)
                            print(runs_str)
                            break
                    write("\n")
        except IndexError as e:
                pass
    for times in time_measurements:
        print("Average time: " + str(sum(times) / len(times)))



