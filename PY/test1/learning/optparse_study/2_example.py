from optparse import OptionParser

usage = "myprog[ -f <filename>][-s <xyz>] arg1[,arg2..]"
optParser = OptionParser(usage)
optParser.add_option("-f","--file",action = "store",type="string",dest = "fileName")
optParser.add_option("-v","--vison", action="store_false", dest="verbose",default='None',
                  help="make lots of noise [default]")
fakeArgs = ['-f','file.txt','-v','good luck to you', 'arg2', 'arge']
options, args = optParser.parse_args(fakeArgs)
print(options.fileName)
print(options.verbose)
print(options)
print(args)
print(optParser.print_help())