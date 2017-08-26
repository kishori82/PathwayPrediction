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


usage= sys.argv[0] + """ -i input_file -n ncbi_tree  -o <output file>"""

parser = None
def createParser():
    global parser
    epilog = """
     this code computes the coreness of each pathways, i.e., for each pathway what is the 
     percentage of samples it is present in"""

    epilog = re.sub(r'[ \t\f\v]+',' ', epilog)

    parser = OptionParser(usage=usage, epilog=epilog)

    parser.add_option("-i", "--input_file", dest="input_file",
                      help='the input file [REQUIRED]')

    parser.add_option("-n", "--ncbi_file", dest="ncbi_file",
                      help='the ncbi file [REQUIRED]')

    parser.add_option("-o", "--output_file", dest="output_file",
                      help='the output file [REQUIRED]')




def main(argv, errorlogger = None, runstatslogger = None): 
    global parser

    (opts, args) = parser.parse_args(argv)

    ncbi_orgs={}
    with open(opts.ncbi_file, 'r') as fn:
       for line in fn:
           line = line.strip()
           if len(line)==0:
             continue

           fields = [ x.strip() for x in line.split('\t') ]
           ncbi_orgs[fields[0].lower()] = fields[0]

    print '#orgs in ncbi tree',  len(ncbi_orgs)
    prokaryotes={}
    with open(opts.input_file, 'r') as fn:
       for line in fn:
           line = line.strip()
           if len(line)==0:
             continue
           fields = [ x.strip() for x in line.split('\t') ]
           prokaryotes[fields[0].lower()]= fields[20]
    print "#orgs in prokaryotes ", len(prokaryotes)

    total = 0
    hits = 0
    for prok in prokaryotes:
       total += 1
       if prok in ncbi_orgs: 
         hits += 1
         print prok, prokaryotes[prok]

    print "#total ", total, "#hits", hits
          
      

    

# the main function of metapaths
if __name__ == "__main__":
    createParser()
    main(sys.argv[1:])

