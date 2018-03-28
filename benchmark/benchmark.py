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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Benchmark tool for UPPAAL models')
    parser.add_argument('-o', type=str, required=False, help='OS name')
    parser.add_argument('-i', type=int, required=False, help='Number of iterations to run', default=1)
    parser.add_argument('--write', action='store_true', required=False, help='Write results to a file (set --t to get a trace)')
    parser.add_argument('--t', action='store_true', required=False, help='Generate and show some trace')
    parser.add_argument('--s', action='store_true', required=False, help='Reduces output')
    args = parser.parse_args()

    OS = args.o
    if args.o is None:
        OS = linux
    write = args.write
    t = y = s = q = ""

    if args.t:
        t = "-t0"
        y = "-y"
    if args.s:
        s = "-s"
        q = "-q"

    time_measurements = []
    my_location_windows = my_location.replace("/", "\\")
    
    with open('results', 'w') as results:
        for model in os.listdir(os.getcwd()):
            i = 0    
            try:
                if model.split('.')[1] == 'xml':
                    results.write(model + "\n")
                    times = []
                    with open(my_location + "benchmark_trace", 'w') as trace_file:
                        while i < args.i:
                            i += 1
                            output = None
                            if write:
                                output = trace_file
                            p1 = None
                            print("Current model:{0}".format(model))
                            start = datetime.datetime.now()
                            if linux_machine(OS):
                                subprocess.Popen([my_location + "./verifyta", my_location + model, my_location + "classic.q",
                                                  "-o1", t, y], stdout=output, stderr=output).wait()
                            else:
                                subprocess.Popen(my_location_windows + "verifyta.exe -o1 " + t + " " + s + " " + q + " "  + y  + " " + my_location_windows + model + " " + my_location_windows + "classic.q", stdout=output, stderr=output).wait()
                            end = datetime.datetime.now()
                            time = end - start
                            total_seconds = time.total_seconds()
                            times.append(total_seconds)
                            results.write(str(i) + ": " + str(times[-1]) + "\n")
                            print("Done:{0}".format(model))
                    with open('benchmark_trace', 'r') as trace:
                        for line in reversed(list(trace)):
                            t_time = re.findall("(t_time[>=]+[0-9]+)", line)
                            if t_time:
                                results.write("data_earth: " + re.findall("(data_earth\=[0-9]+)", line)[0].split('=')[1])
                                results.write("\ndata_storage: " + re.findall("(data_gathered\=[0-9]+)", line)[0].split('=')[1])
                                results.write('\ndata_internal: ' + re.findall("(data_internal\=[0-9]+)", line)[0].split('=')[1] + "\n")
                                for clock in get_clocks():
                                    results.write("{0}\t{1}\n".format(clock[0], clock[1]))
                                for i in range(0, 3):
                                    items = get_delays(i)
                                    for item in items:
                                        results.write(item + "\n")
                                for i in range(0, 3):
                                    items = get_runs(i)
                                    for item in items:
                                        results.write(item + "\n")
                                break
                        results.write("\n\n")
                        trace.seek(0)
                        trace.truncate()
            except IndexError as e:
                    pass
    for times in time_measurements:
        print("Average time: " + str(sum(times) / len(times)))



