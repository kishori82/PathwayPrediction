#!/usr/bin/python

from __future__ import division
try:
     import sys, traceback, re
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

    lca_min_score = 50   # an LCA parameter for min score for a hit to be considered
    lca_top_percent = 10    # an LCA param to confine the hits to within the top hits score upto the top_percent% 
    lca_min_support = 5   # a minimum number of reads in the sample to consider a taxon to be present
    results_dictionary = None
    tax_dbname = 'refseq'

    megan_map = {} # hash between NCBI ID and taxonomic name name
    
    accession_to_taxon_map = {} # hash between gi and taxon name

    # initialize with the ncbi tree file 
    def __init__(self, filename):
        # a readable taxon name to numeric string id map as ncbi
        self.name_to_id={}

        # a readable taxon ncbi tax id to name map
        self.id_to_name={}

        # this is the tree structure in a id to parent map, you can traverse it to go to the root
        self.taxid_to_ptaxid = {}

        self.idno = 0

        self.loadtreefile(filename)
            #print filename,  len(self.taxid_to_ptaxid.keys())

    def load_accession_to_taxon_map(self, accession_to_taxon_file):
        with open(accession_to_taxon_file) as file:
            for line in file:
                fields = line.split("\t")
                fields = map(str.strip, fields)
                self.accession_to_taxon_map[ fields[1] ] = fields[0]


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
        taxonomy_file = open(filename, 'r')
        lines = taxonomy_file.readlines()
        taxonomy_file.close()

        self.name_to_id['root'] = str(self.idno)
        self.id_to_name[str(self.idno)] = 'root'

        self.idno += 1

        for line in lines:
            if self.begin_pattern.search(line):
                continue

            name =  self.name_pattern.search(line)

            if  name==None:
                continue

            taxpart = re.sub(self.name_pattern, '', line)

            fields =  [ x.strip()  for x in taxpart.rstrip().split(';')]

            if len(fields) ==0:
                continue

            for field in fields:
              if field  in self.name_to_id:
                  continue
              self.name_to_id[field] = str(self.idno)
              self.id_to_name[str(self.idno)] = field
              self.idno += 1
            

            previd = self.name_to_id['root']
            for field in fields:
               cid = self.name_to_id[field]

               if not cid in self.taxid_to_ptaxid:
                   self.taxid_to_ptaxid[cid] = [previd, 0, 0]

               previd = cid
            #print  self.taxid_to_ptaxid

            # the taxid to ptax map has for each taxid a corresponding 3-tuple
            # the first location is the pid, the second is used as a counter for
            # lca while a search is traversed up the tree and the third is used for
            # the min support
            #self.taxid_to_ptaxid[str(fields[1])] = [ str(fields[2]), 0, 0]


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
