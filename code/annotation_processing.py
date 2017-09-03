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

    parser.add_option("-d", "--data_folder", dest="data_folder",
                      help='the annotation file [REQUIRED]')

    parser.add_option("-s", "--sample", dest="sample_file",
                      help='the sample file with annotaiton [REQUIRED]')

    parser.add_option("-r", "--reactions", dest="reactions",
                      help='the reactions file with ec number [REQUIRED]')


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


    
    unique_id = re.compile(r'UNIQUE-ID - (.*)$')
    reaction_list = re.compile(r'REACTION-LIST - (.*)$')
    ec_number = re.compile(r'EC-NUMBER - .*(\d+[.]\d+[.]\d+[.]\d+)')
    enzymatic_reaction = re.compile(r'ENZYMATIC-REACTION - (.*)$')

    common_name = re.compile(r'COMMON-NAME - (.*)$')
    synonym = re.compile(r'SYNONYMS - (.*)$')

    # read PATHWAYS and their REACTIONS
    pathways_to_rxns = {}
    rxns_to_pathways = {}
    with open(opts.data_folder + '/pathways.dat', 'r' ) as fin:
      for line in fin:
         line = line.strip()
         resPwy = unique_id.search(line) 
         if resPwy:
            pwy = resPwy.group(1)
            pathways_to_rxns[pwy] = []
       
         resRxn = reaction_list.search(line) 
         if resRxn:
            rxn=resRxn.group(1)
            pathways_to_rxns[pwy].append(rxn)
            if not rxn in rxns_to_pathways:
               rxns_to_pathways[rxn] = []
            rxns_to_pathways[rxn].append(pwy)
       

    # read REACTIONS to ENZREACTIONS
    enzrxn_to_reactions = {}
    ec_to_reactions = {}
    reactions = {}
    with open(opts.data_folder + '/reactions.dat', 'r' ) as fin:
      for line in fin:
         line = line.strip()
         #print line
         resRxn = unique_id.search(line) 
         if resRxn:
            rxn=resRxn.group(1)
            reactions[rxn] = { 'EC': [],  'ENZRXNS':[] }
       
         resEC = ec_number.search(line) 
         if resEC:
            EC=resEC.group(1)
            reactions[rxn]['EC'].append(EC)
            ec_to_reactions[EC] = rxn
       
         resEnzRxn = enzymatic_reaction.search(line) 
         if resEnzRxn:
            enzrxn=resEnzRxn.group(1)
            reactions[rxn]['ENZRXNS'].append(enzrxn)
            enzrxn_to_reactions[enzrxn] = rxn
       

    
    # create ANNOT to the EZNRXN 
    annotation_to_enzrxn = {}
    annotations = {}
    c = 1
    with open(opts.data_folder + '/enzrxns.dat', 'r' ) as fin:
      for line in fin:
         #line = line.lower()
         resEnzRxn = unique_id.search(line) 
         if resEnzRxn:
             enzrxn=resEnzRxn.group(1)

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
             annotations[annotid] = annot.lower()
             annotation_to_enzrxn[annotid] = enzrxn
             #print annotid, annotation_to_enzrxn[annotid] 


    word_to_annotids ={}
    for annotid in annotations:
      fields = [ x.strip() for x in annotations[annotid].split(' ') ]
      for field in fields:  
         if not  field in word_to_annotids:
            word_to_annotids[field] = []
         word_to_annotids[field].append(annotid)


    # keeps track for the reactions
    rxns_in_sample={}
    
    orfCount = 0
    hitCount = 0
    # read the sample annotations and see the matches to the annots
    with gzip.open(opts.sample_file, 'r' ) as fin:
      for line in fin:
        annot_matches={}
        line = line.lower()
        fields = [ x.strip() for x in line.split('\t') ]
        #print "=====>", line
        orfCount += 1

        if fields[1]: 
          ec = fields[1]
          if ec in ec_to_reactions:
             rxn = ec_to_reactions[ec]
             if not rxn in rxns_in_sample:
                 rxns_in_sample[rxn] = 0
             rxns_in_sample[rxn] += 1
             continue

        if len(fields) ==3 and fields[2]: 
           words = [ x.strip() for x in fields[2].split(' ') ]
           for word in words:  
             if word in word_to_annotids:
                for annotid in word_to_annotids[word]:
                  if not annotid in annot_matches:
                     annot_matches[annotid] = 0
                  annot_matches[annotid] += 1

             for annotid in annot_matches:
                if annot_matches[annotid] == len(words) or annot_matches[annotid] >= 2:
                   #print '\t\t',annotations[annotid]
                   #print '\t\t\t', annotation_to_enzrxn[annotid], enzrxn_to_reactions[annotation_to_enzrxn[annotid]]
                   rxn=enzrxn_to_reactions[annotation_to_enzrxn[annotid]]
                   hitCount += 1
                   if not rxn in rxns_in_sample:
                      rxns_in_sample[rxn] = 0

                   rxns_in_sample[rxn] += 1
                   break
           
    # the set of reactions present and their number
    #for rxn, count in rxns_in_sample.iteritems():
    #    print rxn, count

    pwys_in_sample={}

    for rxn, count in rxns_in_sample.iteritems():
      if rxn in rxns_to_pathways:
       pwys = rxns_to_pathways[rxn] 
       for pwy in pwys:
          if not pwy in pwys_in_sample:
            pwys_in_sample[pwy] = 0
          pwys_in_sample[pwy] += 1

    print '# orfs of the sample ', orfCount
    print '# orfs matched with metacyc reactions :', hitCount
    print "# reactions predicted :", len(rxns_in_sample.keys())
    print '# pathways predicted  :', len(pwys_in_sample.keys())
          

    pwy_to_x = {}
    x_to_pwy = {}
    x = 1
    for pwy in pathways_to_rxns:
        pwy_to_x[pwy]='x' + str(x)
        x_to_pwy['x' + str(x)] = pwy
        x +=1

    with open('input.lp', 'w') as  fout:
        fprintf(fout, "Minimize\n") 

        fprintf(fout, "  obj:") 
        for pwy in pwys_in_sample:
            fprintf(fout, " + %s", pwy_to_x[pwy]) 
        fprintf(fout, "\n") 

        # subject to
        fprintf(fout, "Subject To\n") 

        c=1
        for rxn in rxns_in_sample:
           if rxn in rxns_to_pathways:
             c +=1
             fprintf(fout, "  %s: ", 'c' +str(c)) 
             for pwy in rxns_to_pathways[rxn]:
                fprintf(fout, " + %s", pwy_to_x[pwy]) 
             fprintf(fout, " >= 1\n") 

        fprintf(fout, "Bounds\n") 
        # variable types
        fprintf(fout, "Binary\n") 
        for pwy in pwys_in_sample:
            fprintf(fout, "  %s\n", pwy_to_x[pwy]) 

        # End
        fprintf(fout, "End\n") 
        
    command = "glpsol"  + " --lp input.lp -o output.sol >> /dev/null"

    os.system(command)

    try:
       glpout = open('output.sol','r')
    except IOError:
       print """Cannot open \'ouptut.sol\' to read solution"""
       sys.exit(0)
    
    solLines = glpout.readlines()
    glpout.close()

    activity = re.compile(r'Activity')
    sol = re.compile(r'\d+\s([x]\d+)\s+[*]\s+([0-1])')

    count = 0
    i = 1
    for line in solLines:
       line = line.strip()
       if activity.search(line):
           count += 1
       if count < 2:
          continue


       res= sol.search(line)
       if res:
           xpwy=res.group(1)
           result=res.group(2)
           if result=='1':
             print i, x_to_pwy[xpwy]
             i+=1
              

        
       
    
    
       




# the main function of metapaths
if __name__ == "__main__":
    createParser()
    main(sys.argv[1:])
