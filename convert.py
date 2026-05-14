with open("readme.md", "r") as input, open("result.txt", "w") as output:
    for line in input:
        start = line[:3]
        end = line[-2:]
        if line.find("png") > 0:
            name = line[3:-3]
            print(name)
            output.write(f'<img src="{name}" align="center">\n')
        else:
            output.write(line)

    