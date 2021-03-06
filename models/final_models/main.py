from lxml import objectify, etree
import re
import os

count = 0
currentTransition = ''


class Template(object):
    def __init__(self, name, nodes, transitions):
        self.name = name
        self.nodes = nodes
        self.transitions = transitions


class Name(object):
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name


class Label(object):
    def __init__(self, kind, x, y, code):
        self.kind = kind
        self.x = x
        self.y = y
        self.code = code


class Location(object):
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.Name = None
        self.Label = None
        self.init = False
        self.urgent = False
        self.committed = False


class Transition(object):
    def __init__(self):
        global count, currentTransition
        self.id = currentTransition = 't' + str(count)
        count = count + 1
        self.source = None
        self.target = None
        self.labels = []
        self.nails = []


class Nail(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def colorCodedText(kind, code):
    formatedCode = ''
    for line in code:
        if kind == "select":
            formatedCode = formatedCode + "\\textcolor{select}{" + line + "}\\\\"
        elif kind == "guard":
            formatedCode = formatedCode + "\\textcolor{guard}{" + line + "}\\\\"
        elif kind == "synchronisation":
            formatedCode = formatedCode + "\\textcolor{sync}{" + line + "}\\\\"
        elif kind == "assignment":
            formatedCode = formatedCode + "\\textcolor{update}{" + line + "}\\\\"
        elif kind == "invariant":
            formatedCode = formatedCode + "\\textcolor{invariant}{" + line + "}\\\\"
    return formatedCode

textOffsetX = -10
textOffsetY = -5
nodeOffsetX = 0
nodeOffsetY = 0
nameOffsetX = -20
nameOffsetY = -5

def replace_bools(str):
    return str.replace("\\&amp;","\\&").replace('\\&lt', '<').replace('\\&gt', '>').replace(';=', '=')


def GenerateTikz(name, nodes, transitions):
    f = open(name + ".tex", "w")
    f.write("\\begin{figure}[H]\n\t\\centering\n\t\\begin{tikzpicture}[x=0.02cm,y=0.02cm]\n\t% place nodes\n")
    for l in nodes:
        symbol = ''
        if l.urgent:
            symbol = "$\cup$"
        elif l.committed:
            symbol = "c"
        if l.init:
            f.write("\\node[init] at (" + str(int(l.x) + nodeOffsetX) + ", " + str((int(l.y) + nodeOffsetY) * -1) + ") (" + l.id + ") {" + symbol + "};\n")
        else:
            f.write("\\node[location] at (" + str(int(l.x) + nodeOffsetX) + ", " + str((int(l.y)+nodeOffsetY) * -1) + ") (" + l.id + ") {" + symbol + "};\n")
    f.write("\t% place node labels\n")
    for l in nodes:
        if l.Label is not None:
            code = replace_bools(l.Label.code)
            fragments = code.split("\n")
            code = colorCodedText(l.Label.kind, fragments)
            f.write("\\node[anchor=north west, text width=10cm, font=\\tiny, align=left] at (" + str(int(l.Label.x) + textOffsetX) + "," + str((int(l.Label.y) + textOffsetY)*-1) + ") {\\begin{tabular}{l}" + code + "\\end{tabular}};\n")
        if l.Name is not None:
            f.write("\\node[anchor=north west, text width=10cm, font=\\tiny, align=left] at (" + str(int(l.Name.x) + nameOffsetX) + "," + str((int(l.Name.y) + nameOffsetY)*-1) + ") {\\begin{tabular}{l}" + l.Name.name + "\\end{tabular}};\n")
        f.write("\t% place transition labels\n")
    for t in transitions:
        for ts in t.labels:
            if ts is not None:
                code =  replace_bools(ts.code)
                fragments = code.split("\n")
                code = colorCodedText(ts.kind, fragments)
                f.write("\\node[anchor=north west, text width=10cm, font=\\tiny, align=left] at (" + str(int(ts.x) + textOffsetX) + "," + str((int(ts.y) + textOffsetY) * -1) + ") {\\begin{tabular}{l}" + code + "\\end{tabular}};\n")
    f.write("\t% place transitions\n")
    for t in transitions:
        path = "\draw[->] (" + t.source + ") -- "
        for ns in t.nails:
            path = path + "(" + ns.x + ", " + str(int(ns.y) * -1) + ") -- "
        test = t.target
        path = path + "(" + test + ") {};\n"
        f.write(path)
    f.write("\t\\end{tikzpicture}\n\t\\caption{The " + name.split("_")[-1].replace('_','\\_') + " template}\n\t\\label{fig:t_" + name + "}\n\end{figure}\n")


def my_filter(current_template, template):
    return filter(lambda x: x.name == current_template, templates)


def my_filter_next(current_location, elements):
    return filter(lambda x: x.id == current_location, elements)

def find_fragments(str):
    return re.findall("[^\ ]+", str)[1:]


if __name__ == '__main__':
    inTemplate = inLocation = inTransition = False
    xml = ''
    xmlList = []
    templates = []
    currentTemplate = ''
    currentLocation = ''
    for filename in os.listdir(os.getcwd()):
        if filename.split('.')[1] == 'xml':
            with open(filename) as f:
                for line in f:
                    if line[-2:] == '>\n':
                        xml = xml + line.replace('\t', '').replace('\n', '')
                    else:
                        xml = xml + line.replace('\t', '')
                xml = xml.replace('\n', '!newline!')
                xmlList = xml.split('<')
                for line in xmlList:
                    if line[:8] == 'template':
                        inTemplate = True
                    elif line[:8] == 'location':
                        inLocation = True
                        fragments = line.split(' ')[1:]
                        templateFilter = my_filter(currentTemplate, templates)
                        next(templateFilter).nodes.append(
                            Location(fragments[0][4:][:-1], fragments[1][3:][:-1], fragments[2][3:][:-2]))
                        currentLocation = fragments[0][4:][:-1]
                    elif line[:4] == 'name':
                        if inTemplate:
                            templates.append(Template(filename.split('.')[0] + "_" + line[5:], [], []))
                            currentTemplate = filename.split('.')[0] + "_" + line[5:]
                            inTemplate = False
                        elif inLocation:
                            templateFilter = my_filter(currentTemplate, templates)
                            locationFilter = my_filter_next(currentLocation, next(templateFilter).nodes)
                            fragments = re.findall("[^\ |\>]+", line)[1:]
                            next(locationFilter).Name = Name(fragments[0][3:][:-1], fragments[1][3:][:-1], fragments[2])
                    elif line[:5] == 'label':
                        if inTransition:
                            templateFilter = my_filter(currentTemplate, templates)
                            transitionFilter = my_filter_next(currentTransition, next(templateFilter).transitions)
                            fragments = find_fragments(line.split('>')[0])
                            code = line.split('>')[1].replace("!newline!", "\n").replace("&", "\&").replace("_", "\_")
                            next(transitionFilter).labels.append(
                                Label(fragments[0][6:][:-1], fragments[1][3:][:-1], fragments[2][3:][:-1], code))
                        elif inLocation:
                            templateFilter = my_filter(currentTemplate, templates)
                            locationFilter = my_filter_next(currentLocation, next(templateFilter).nodes)
                            fragments = find_fragments(line.split('>')[0])
                            code = line.split('>')[1].replace("!newline!", "\n").replace("&", "\&").replace("_", "\_")
                            next(locationFilter).Label = Label(fragments[0][6:][:-1], fragments[1][3:][:-1],
                                                               fragments[2][3:][:-1], code)
                    elif line[:9] == 'committed':
                        templateFilter = my_filter(currentTemplate, templates)
                        locationFilter = my_filter_next(currentLocation, next(templateFilter).nodes)
                        next(locationFilter).committed = True
                    elif line[:6] == 'urgent':
                        templateFilter = my_filter(currentTemplate, templates)
                        locationFilter = my_filter_next(currentLocation, next(templateFilter).nodes)
                        next(locationFilter).urgent = True
                    elif line[:10] == 'transition':
                        inTransition = True
                        templateFilter = my_filter(currentTemplate, templates)
                        next(templateFilter).transitions.append(Transition())
                    elif line[:4] == 'nail':
                        fragments = line.split(' ')[1:]
                        templateFilter = my_filter(currentTemplate, templates)
                        transitionFilter = my_filter_next(currentTransition, next(templateFilter).transitions)
                        next(transitionFilter).nails.append(Nail(fragments[0][3:][:-1], fragments[1][3:][:-3]))
                    elif line[:6] == 'source':
                        templateFilter = my_filter(currentTemplate, templates)
                        transitionFilter = my_filter_next(currentTransition, next(templateFilter).transitions)
                        next(transitionFilter).source = line[12:][:-3]
                    elif line[:6] == 'target':
                        templateFilter = my_filter(currentTemplate, templates)
                        transitionFilter = my_filter_next(currentTransition, next(templateFilter).transitions)
                        next(transitionFilter).target = line[12:][:-3]
                    elif line[:4] == 'init':
                        templateFilter = my_filter(currentTemplate, templates)
                        locationFilter = my_filter_next(line[10:][:-3], next(templateFilter).nodes)
                        next(locationFilter).init = True
                    elif line[:1] == '/':
                        if line[1:][:-1] == 'location':
                            inLocation = False
                        elif line[1:][:-1] == 'transition':
                            inTransition = False

    for l in templates:
        print(l.name)
        GenerateTikz(l.name, l.nodes, l.transitions)
