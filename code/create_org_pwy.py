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
     import random

except:
     print """ Could not load some user defined  module functions"""
     print """ Make sure your typed 'source MetaPathwaysrc'"""
     print """ """
     sys.exit(3)


usage= sys.argv[0] + """ -i input_file -n ncbi_tree  -o <output file>"""

def fprintf(file, fmt, *args):
   file.write(fmt % args)
   
def printf(fmt, *args):
   sys.stdout.write(fmt % args)
   sys.stdout.flush()
 
parser = None
def createParser():
    global parser
    epilog = """
     this code computes the coreness of each pathways, i.e., for each pathway what is the 
     percentage of samples it is present in"""

    epilog = re.sub(r'[ \t\f\v]+',' ', epilog)

    parser = OptionParser(usage=usage, epilog=epilog)

    parser.add_option("-l", "--list", dest="orglist",
                      help='the organism list [REQUIRED]')

    parser.add_option("-p", "--pathways", dest="pathways",
                      help='the pathways [REQUIRED]')

    parser.add_option("-o", "--output_file", dest="output_file",
                      help='the output file [REQUIRED]')




def main(argv, errorlogger = None, runstatslogger = None): 
    global parser

    (opts, args) = parser.parse_args(argv)

    orglist = [] 
    with open(opts.orglist, 'r') as fin:
       for line in fin:
          line = line.strip()
          if not line:
             continue
          orglist.append(line)

    pathways = []
    with open(opts.pathways, 'r') as fin:
       for line in fin:
          line = line.strip()
          if not line:
             continue
          fields = [ x.strip() for x in line.split('\t') ]
          pathways.append(fields[1])

    for org in orglist:
       printf("%s", org)

       for pathway in pathways:
         if random.random() < 0.9:
          printf("\t%s", pathway)

       printf("\n");
       

# the main function of metapaths
if __name__ == "__main__":
    createParser()
    main(sys.argv[1:])

