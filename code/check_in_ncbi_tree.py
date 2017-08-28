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


usage= sys.argv[0] + """ -i input_list  -n ncbi_tree_file  -o <output file>"""

parser = None
def createParser():
    global parser
    epilog = """
     this code computes the coreness of each pathways, i.e., for each pathway what is the 
     percentage of samples it is present in"""

    epilog = re.sub(r'[ \t\f\v]+',' ', epilog)

    parser = OptionParser(usage=usage, epilog=epilog)

    parser.add_option("-i", "--input_list", dest="input_list",
                      help='the input list [REQUIRED]')

    parser.add_option("-n", "--ncbi_tree", dest="ncbi_tree",
                      help='the ncbi tree [REQUIRED]')



def main(argv, errorlogger = None, runstatslogger = None): 
    global parser
    global errorcode

    (opts, args) = parser.parse_args(argv)


    ncbi_taxons={}
    with open(opts.ncbi_tree, 'r') as fin:
       for line in fin:
          if line.strip :
             tax = line.strip().split('\t')[0] 
          else:
             continue
          ncbi_taxons[tax.lower()] = tax


    
    valid =0
    total =0
    with open(opts.input_list, 'r') as fin:
       for line in fin:
          if line.strip :
             tax = line.strip().split('\t')[0] 
             tax = re.sub("\"", "", tax)
          else:
             continue
          total += 1
          if tax.lower() in ncbi_taxons: 
             valid += 1 
             print tax

    print valid, total 

# the main function of metapaths
if __name__ == "__main__":
    createParser()
    main(sys.argv[1:])

