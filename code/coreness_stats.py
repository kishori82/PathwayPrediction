#!/usr/bin/python
# File created on 27 Jan 2012.
from __future__ import division

__author__ = "Kishori M Konwar"
__copyright__ = "Copyright 2013, MetaPathways"
__credits__ = ["r"]
__version__ = "1.0"
__maintainer__ = "Kishori M Konwar"
__status__ = "Release"

try:
     import os, re, glob, operator
     from os import makedirs, sys, remove, rename
     from sys import path
     from optparse import OptionParser

except:
     print """ Could not load some user defined  module functions"""
     print """ Make sure your typed 'source MetaPathwaysrc'"""
     print """ """
     sys.exit(3)


usage= sys.argv[0] + """ -f input_folder  -o <output file>"""

parser = None
def createParser():
    global parser
    epilog = """
     this code computes the coreness of each pathways, i.e., for each pathway what is the 
     percentage of samples it is present in"""

    epilog = re.sub(r'[ \t\f\v]+',' ', epilog)

    parser = OptionParser(usage=usage, epilog=epilog)

    parser.add_option("-f", "--input_folder", dest="input_folder",
                      help='the input fasta filename [REQUIRED]')




def main(argv, errorlogger = None, runstatslogger = None): 
    global parser
    global errorcode

    (opts, args) = parser.parse_args(argv)

    files =  glob.glob(opts.input_folder + "/*.txt")

    N = len(files)
    pathways ={}
    for file in files:
       with open(file, 'r') as fr:
          for line in fr:
             pwy = line.strip()
             if len(pwy)==0 or len(pwy) > 40:
                 continue

             if not pwy in  pathways:
                 pathways[pwy]=0

             pathways[pwy]= pathways[pwy] + 1 


    sorted_pathways = sorted(pathways.items(), key=operator.itemgetter(1), reverse=True) 

    i = 1
    for key, value in sorted_pathways:
       print "%d\t%s\t%d" %(i, key, value/N*100)
       i = i+ 1
    #for key, value in sorted_pathways.iteritems():
    #    print key, value
     

    

# the main function of metapaths
if __name__ == "__main__":
    createParser()
    main(sys.argv[1:])

