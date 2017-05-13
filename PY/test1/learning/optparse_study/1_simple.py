from optparse import OptionParser

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="filename",
                      help="read data from FILENAME")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    fakeArgs = ['-f', 'file.txt', '-v','']
    (options, args) = parser.parse_args(fakeArgs)
    print(parser.print_help())
    if len(args) != 1:
        parser.error("incorrect number of arguments ddddddd")
    if options.verbose:
        print("reading %s..." % options.filename)


if __name__ == "__main__":
    main()