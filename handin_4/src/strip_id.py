import sys

with open(sys.argv[1]) as data, open(sys.argv[2], 'w') as savefile:
    for line in data:
        if line[0:10] == "@attribute" and line [11:13] != "ID":
            savefile.write(line)
        else:
            newline = line.split(',')[1:]
            for i in range(len(newline)):
                savefile.write(newline[i])
                if i != len(newline) - 1:
                    savefile.write(',')
        savefile.write('\n')
