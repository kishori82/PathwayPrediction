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
     import os, re, glob, operator, sys, gzip, random
     from NCBITREE import NCBITREE
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

    parser.add_option("-a", "--annot_filee", dest="annot_file",
                      help='the annotation file [REQUIRED]')

    parser.add_option("-s", "--sample", dest="sample_file",
                      help='the sample file with annotaiton [REQUIRED]')


def removeHTMLtag(line):
    line = re.sub(r'<[a-zA-Z]+>', '', line)
    line = re.sub(r'<\/[a-zA-Z]+>', '', line)
    return line
    
htmlSymbol= re.compile(r'&([a-z]+);')
def modifyHTMLsymbol(line):

    res = htmlSymbol.search(line)
    while  res:
      symbol =  res.group(1) 
      line = line.replace("&" + symbol +";",symbol, 100)
      res = htmlSymbol.search(line)

    return line

def main(argv, errorlogger = None, runstatslogger = None): 
    global parser

    (opts, args) = parser.parse_args(argv)


    
    common_name = re.compile(r'COMMON-NAME - (.*)$')
    synonym = re.compile(r'SYNONYMS - (.*)$')

    annotations = {}
    c = 1
    with open(opts.annot_file, 'r' ) as fin:
      for line in fin:
         annot=None
         res = common_name.search(line) 
         if res:
            annot = removeHTMLtag(res.group(1))
            annot =  modifyHTMLsymbol(annot)
       
         res1 = synonym.search(line) 
         if res1:
            annot = removeHTMLtag(res1.group(1))
            annot =  modifyHTMLsymbol(annot)

         if annot:
             annotid = "ANOT-" + str(c)
             c += 1
             annotations[annotid] = annot

    indexes ={}
    for annotid in annotations:
      fields = [ x.strip() for x in annotations[annotid].split(' ') ]
      for field in fields:  
         if not  field in indexes:
            indexes[field] = []
         indexes[field].append(annotid)

    
    with open(opts.sample_file, 'r' ) as fin:
      for line in fin:
        fields = [ x.strip() for x in line.split(' ') ]
          

         


# the main function of metapaths
if __name__ == "__main__":
    createParser()
    main(sys.argv[1:])

