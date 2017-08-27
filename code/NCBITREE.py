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

        self.org_pathways={}

    def loadtreefile(self, filename):
        with gzip.open(filename, 'r') as fin:
          lines = fin.readlines()

        #this simply creates the tree
        for line in lines:
              if self.begin_pattern.search(line):
                  continue
              fields =  [ x.strip()  for x in line.rstrip().split('\t')]
              if len(fields) !=3:
                  continue
              if str(fields[0]) not in self.id_to_name:
                  self.name_to_id[str(fields[0]).lower()] = str(fields[1])
  
              self.id_to_name[str(fields[1])] = str(fields[0])
  
              # the taxid to ptax map has for each taxid a corresponding 3-tuple   [ x, y , z ]
              # x : pid,  parent id
              # y : a flag
              # z : a counter
              # u : {id1, id2,...idn} set of children as a dictionary the values are flag
  
              self.taxid_to_ptaxid[str(fields[1])] = [ str(fields[2]), 0, 0, {}]
         
        #this is a code where each children introuduces itself in the parent's hash 
        for line in lines:
              if self.begin_pattern.search(line):
                  continue
              fields =  [ x.strip()  for x in line.rstrip().split('\t')]
              if len(fields) !=3:
                  continue

              sid = str(fields[1])

              while sid!='1':
                 pid = self.taxid_to_ptaxid[sid][0]
                 if sid in self.taxid_to_ptaxid[pid][3]:
                    break

                 self.taxid_to_ptaxid[pid][3][sid] = 0
                 sid = pid
                 

    def get_root(self):
         sid = None
         for tid, pid in  self.taxid_to_ptaxid.iteritems():
            sid = tid

         while sid!='1':
             pid = self.taxid_to_ptaxid[sid][0]
             sid = pid

         return sid


    def print_tree(self, rid, depth=0, limit=1000000):
        print '\t'*depth, self.id_to_name[rid]
        cids = self.taxid_to_ptaxid[rid][3].keys()
        ctr = 0
        for cid in cids:
          self.print_tree(cid, depth=depth+1, limit = limit)
          ctr += 1
          if ctr > limit:
             break



    # return the taxonomy linears from and id, e.g., 56 would return Bacteria;ProteoBacteria;Gammaproteobacteria;Some Species name
    def get_full_taxonomy(self, ncbi_id):
        ncbi_id = str(ncbi_id)

        if ncbi_id in self.megan_map:
            exp_lin = self.get_lineage(ncbi_id)
            exp_lin.reverse()
            name ='';
            for lid in exp_lin:
                if lid in self.id_to_name:
                   name += self.id_to_name[lid]+ ';';
            return name + " (" + str(ncbi_id) + ")"
        # think about this
        return None

    # get the number of taxon ids
    def numTaxnames(self ):
         return len(self.name_to_id)


    # get the number of unique taxon ids
    def numTaxids(self):
         return len(self.taxid_to_ptaxid)

    # given a tax name tet the id
    def get_ID(self, name):
        if name in self.name_to_id:
           return  self.name_to_id[name]
        return None

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


    # internal function need to call this to clear the counts of reads at every node      
    def _clear_cells(self, IDs):
        limit = len(IDs)
        for id in IDs:
            tid = id
            while( tid in self.taxid_to_ptaxid and tid !='0' ):
                #if self.taxid_to_ptaxid[tid][1]==0:
                #   return  self.id_to_name[tid]
                self.taxid_to_ptaxid[tid][1]=0
                tid = self.taxid_to_ptaxid[tid][0]


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
 
    def add_org_pathways(self, name, pathways):
       name = name.lower()
       if name in self.name_to_id:
          id = self.name_to_id[name]
          self.org_pathways[name] = pathways


def fprintf(file, fmt, *args):
   file.write(fmt % args)
   
def printf(fmt, *args):
   sys.stdout.write(fmt % args)
   sys.stdout.flush()
 
def eprintf(fmt, *args):
   sys.stderr.write(fmt % args)
   sys.stderr.flush()
