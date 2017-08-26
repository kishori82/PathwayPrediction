#!/usr/bin/python

from __future__ import division
try:
     import sys, traceback, re, gzip
     import math
except:
     print """ Could not load some user defined  module functions"""
     print """ Make sure your typed \'source RiboCensusrc\'"""
     print """ """
     print traceback.print_exc(10)
     sys.exit(3)


def copyList(a, b): 
    [ b.append(x) for x in a ] 

class NCBITREE:
    begin_pattern = re.compile("#")
    name_pattern = re.compile(r'>(\S+)')

    results_dictionary = None

    megan_map = {} # hash between NCBI ID and taxonomic name name
    
    accession_to_taxon_map = {} # hash between gi and taxon name

    idno=0

    # initialize with the ncbi tree file 
    def __init__(self, filename):
        # a readable taxon name to numeric string id map as ncbi
        self.name_to_id={}

        # a readable taxon ncbi tax id to name map
        self.id_to_name={}

        # this is the tree structure in a id to parent map, you can traverse it to go to the root
        self.taxid_to_ptaxid = {}

        self.loadtreefile(filename)
        print filename,  len(self.taxid_to_ptaxid.keys())


    def get_preferred_taxonomy(self, ncbi_id):
        ncbi_id = str(ncbi_id)

        if ncbi_id in self.megan_map:
            exp_lin = self.get_lineage(ncbi_id)
            exp_lin.reverse()
            name ='';
            for lid in exp_lin:
                if lid in self.id_to_name:
                   name += self.id_to_name[lid]+ ';';

            # decommison old format
            #return self.megan_map[ncbi_id] + " (" + str(ncbi_id) + ")"

            return name + " (" + str(ncbi_id) + ")"
        # think about this
        return None



    def loadtreefile(self, filename):
        taxonomy_file = gzip.open(filename, 'r')
        lines = taxonomy_file.readlines()
        taxonomy_file.close()


        for line in lines:
            if self.begin_pattern.search(line):
                continue
            fields =  [ x.strip()  for x in line.rstrip().split('\t')]
            if len(fields) !=3:
                continue
            if str(fields[0]) not in self.id_to_name:
                self.name_to_id[str(fields[0])] = str(fields[1])
            self.id_to_name[str(fields[1])] = str(fields[0])
            # the taxid to ptax map has for each taxid a corresponding 3-tuple
            # the first location is the pid, the second is used as a counter for
            # lca while a search is traversed up the tree and the third is used for
            # the min support
            self.taxid_to_ptaxid[str(fields[1])] = [ str(fields[2]), 0, 0]

    def setParameters(self, min_score, top_percent, min_support):
        self.lca_min_score = min_score
        self.lca_top_percent =top_percent
        self.lca_min_support = min_support
         
    def sizeTaxnames(self ):
         return len(self.name_to_id)


    def sizeTaxids(self):
         return len(self.taxid_to_ptaxid)

    def get_a_Valid_ID(self, name):
        if name in self.name_to_id:
           return  self.name_to_id[name]
        return -1

    # given a taxon name it returns the correcponding unique ncbi tax id
    def translateNameToID(self, name):
        if not name in self.name_to_id:
            return None
        return self.name_to_id[name]

    # given a taxon id to taxon name map
    def translateIdToName(self, id):
        if not id in self.id_to_name:
            return None
        return self.id_to_name[id]

    # given a name it returns the parents name
    def getParentName(self, name):
        if not name in  self.name_to_id:
            return None
        id = self.name_to_id[name]
        pid = self.getParentTaxId(id)
        return self.translateIdToName( pid )


    # given a ncbi tax id returns the parents tax id
    def getParentTaxId(self, ID):
        if not ID in self.taxid_to_ptaxid:
            return None
        return self.taxid_to_ptaxid[ID][0]


    # need to call this to clear the counts of reads at every node      
    def clear_cells(self, IDs):
        limit = len(IDs)
        for id in IDs:
            tid = id
            while( tid in self.taxid_to_ptaxid and tid !='0' ):
                #if self.taxid_to_ptaxid[tid][1]==0:
                #   return  self.id_to_name[tid]
                self.taxid_to_ptaxid[tid][1]=0
                tid = self.taxid_to_ptaxid[tid][0]


    # used for optimization
    def set_results_dictionary(self, results_dictionary):
        self.results_dictionary= results_dictionary

    # monotonicly decreasing function of depth of divergence d
    def step_cost(self, d):
        return 1 / math.pow(2,d)

    # given an ID gets the lineage
    def get_lineage(self, id):
        tid = str(id)
        lineage = []
        lineage.append(tid)
        while( tid in self.taxid_to_ptaxid and tid !='1' ):
            lineage.append(self.taxid_to_ptaxid[tid][0])
            tid = self.taxid_to_ptaxid[tid][0]
        return lineage

def fprintf(file, fmt, *args):
   file.write(fmt % args)
   
   

def printf(fmt, *args):
   sys.stdout.write(fmt % args)
   sys.stdout.flush()
 
def eprintf(fmt, *args):
   sys.stderr.write(fmt % args)
   sys.stderr.flush()
