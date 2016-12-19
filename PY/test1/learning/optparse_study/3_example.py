from optparse import OptionParser
optParser = OptionParser()
optParser.add_option("-n","--number",action = "store",type="int",dest = "intNumber")
optParser.add_option("-v","--version", action="store_false", dest="verbose",default='gggggggg',help="no help")
options, args = optParser.parse_args()
if options.intNumber is not None:  # 当有选项n时，则使用给出的参数值
    # num = options.intNumber
    print(options.intNumber,options.verbose)

else:
    for i in range(1, 5):  # 不给选项n的情况下，默认输出的是1～4
         # num = i
         print(i)
