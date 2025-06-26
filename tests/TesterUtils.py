def single_line(outfile, width=80):
    print(80*"-", file=outfile)

def double_line(outfile, width=80):
    print(80*"=", file=outfile)

def single_line_centered(s, outfile, width=80):
    l = int((width - len(s))/2)
    print((l-1)*"-", s, (width - l -1 - len(s))*"-", file=outfile)

def double_line_centered(s, outfile, width=80):
    l = int((width - len(s))/2)
    print((l-1)*"=", s, (width - l -1 - len(s))*"=", file=outfile)

def blank_line(outfile):
    print("", file=outfile)
