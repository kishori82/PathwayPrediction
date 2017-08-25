#!/usr/bin/python

from __future__ import division

__author__ = "Kishori M Konwar"
__copyright__ = "Copyright 2013, MetaPathways"
__credits__ = [""]
__version__ = "1.0"
__maintainer__ = "Kishori M Konwar"
__status__ = "Release"

try:
   import subprocess
   import sys
   from os import makedirs, sys, listdir, environ, path
   import re 
   import inspect
   import time
   from optparse import OptionParser
   import shutil 
   from metapaths_utils import printf, eprintf, fprintf
   from sysutil import getstatusoutput, pathDelim
except:
   print """ Could not load some user defined  module functions"""
   print """ Make sure your typed \"source MetaPathwaysrc\""""
   print """ """
   sys.exit(3)

SSH = ''
SCP = ''
PATHDELIM = pathDelim()
WIN_RSA_KEY_ARGS = ["-i", 'executables' + PATHDELIM + 'win' + PATHDELIM + 'bit64' + PATHDELIM + 'win_rsa.ppk', '-batch']


cmd_folder = path.abspath(path.split(inspect.getfile( inspect.currentframe() ))[0])

#config = load_config()
metapaths_config = """template_config.txt""";

script_info={}
script_info['script_usage'] = []
usage= """./remote_blast_qsub.py --sample-name sample_name --faa-file file  """
parser = OptionParser(usage)
parser.add_option("--sample-name", dest="sample_name",  help='submitting blast files')

parser.add_option("--faa-file", dest="faa_files",  help='submitting amino acid files')

parser.add_option("--database-files", dest="database_files",  action='append', default=['metacyc-v4-2011-07-03', 'cog-2007-10-30'],
               help='database file namess')

parser.add_option("--dbnames", dest="dbnames",  action='append', default =['metacyc', 'cog'],
               help='db namess')

parser.add_option("--run-type", dest="run_type",  default=['overlay'], choices=['overlay', 'overwrite'],
               help='redo')

parser.add_option("--batch-size", dest="batch_size", default=500,  type='int', help='number of sequences in a batch (in a file)')
parser.add_option("--max-parallel-jobs", dest="max_parallel_jobs", default= 300, type='int',  help='maximum number of parallel jobs')
 
parser.add_option( "--algorithm", dest="algorithm", choices = ['BLAST', 'LAST'], default = "BLAST",
                  help='the algorithm used for computing homology [DEFAULT: BLAST]')


#database_files = ['metacyc-v4-2011-07-03', 'cog-2007-10-30','refseq_protein', 'kegg-pep-2011-06-18' ]  


#def fprintf(file, fmt, *args):
#    file.write(fmt % args)
  
#def printf(fmt, *args):
#    sys.stdout.write(fmt % args)

def  isValid(opts):
    
    if not hasattr(opts,'sample_name'):
       return False

    if not hasattr(opts,'user') or not hasattr(opts,'server'):
       return False

    if opts.sample_name:
       return True 
    return False


_user = ''
_server =''

def  setUserServer(user, server):
    global _user,_server

    _user = user
    _server = server


def  getUserServer():
    global _user, _server
    return ( _user, _server)
    #return ( 'kishori', 'glacier.westgrid.ca' )
    #return ( 'kishori', 'shangri-la' )
# checks if the supplied arguments are adequate

def  check_if_server_is_up(user, server):
    user, server = getUserServer()

    args = [SSH, user+'@'+server]  
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args += ['echo','hello']
   # print ' '.join(args)
    p = create_a_process(args)  
    result = p.communicate()

    if result[0].strip()=='hello':
       return True
    else:
       return False

def  remove_sample_dir(sample_name):
    user, server = getUserServer()
    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py','--home-dir', '\'\'', '--remove-sample-dir', sample_name]
    #print ' '.join(args)
    p = create_a_process(args)  
    result = p.communicate()
    #p.stdin.write('lovlee81')
    if result[0].strip()=='':
       return True
    else:
       return False


def check_if_sample_folder_exists(sample_name ):
    user, server = getUserServer()
   # args = [SSH, user+'@'+server, 'python', 'daemon.py','--home-dir', '\'\'', '--does-sample-dir-exist', sample_name]
    #print ' '.join(args)
    
    args = [SSH, user+'@'+server]  
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args += ['python', 'daemon.py','--home-dir', '\'\'', '--does-sample-dir-exist', sample_name]
    
    p = create_a_process(args)  
    result = p.communicate()[0].strip()
    if result=='yes':
       return True
    else:
       return False

def is_complete(sample_name,dbname):
    user, server = getUserServer()
    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py','--home-dir', '\'\'', '--is-complete',\
              sample_name, '--dbname', dbname ]
    #print ' '.join(args)
    p = create_a_process(args)  
    result = p.communicate()
    if result[0].strip()=='yes':
       return True
    else:
       return False


def consolidate(sample_name, dbname):
    user, server = getUserServer()
    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    
    args = args + ['python', 'daemon.py','--home-dir', '\'\'', '--consolidate',\
              sample_name, '--dbname', dbname ]
    #print ' '.join(args)
    p = create_a_process(args)  
    result = p.communicate()
    if result[0].strip()=='yes':
       return True
    else:
       return False



def create_sample_folder(sample_name ):
    user, server = getUserServer()

    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py','--home-dir', '\'\'', '--create-sample-dir', sample_name]
    p = create_a_process(args)  
    result = p.communicate()[0].strip()
    if result=='yes':
       return True
    else:
       return False

def does_file_exist(file):
    user, server = getUserServer()
    args = [SSH, user+'@'+server] 
    #print ' '.join(args)
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py','--home-dir', '\'\'', '--does-file-exist', file]
    
    p = create_a_process(args)  
    result = p.communicate()[0].strip()
    if result=='yes':
       return True
    else:
       return False

def does_file_patt_exist(file):
    user, server = getUserServer()
    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py','--home-dir', '\'\'', '--does-file-patt-exist', file]
    #print ' '.join(args)
    p = create_a_process(args)  
    result = p.communicate()[0].strip()
    if result=='yes':
       return True
    else:
       return False

def format_database(database, algorithm):
    user, server = getUserServer()
    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py','--home-dir', '\'\'', '--format-database', database, '--algorithm', algorithm]
    p = create_a_process(args)  
    result = p.communicate()[0].strip()
    if result=='yes':
       return True
    else:
       return False

def number_of_completed(sample):
    user, server = getUserServer()
    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py',  '--get-number-of-completed',  sample]
    #print ' '.join(args)
    p = create_a_process(args)  
    result = p.communicate()
    #print result[0].strip()
    if result[1].strip()=='':
      try:
        return int(result[0].strip())
      except:
        return 0
    else:
       return 0


def number_of_samples(sample):
    user, server = getUserServer()
    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py',  '--get-number-of-samples',  sample]
    #print ' '.join(args)
    p = create_a_process(args)  
    result = p.communicate()
    #print result
    if result[1].strip()=='':
      try:
        return int(result[0].strip())
      except:
        return 0
    else:
       return 0


def printError(result):
    if len(result[1].strip())>0:
      print "Remote Execution Error:"
      print "<-----------------------"
      for line in result:
         print "    " + line
      print "----------------------->"
   
def printResponse(result):
    if len(result[0].strip())>0:
      print "Remote Execution Response:"
      print "<======================="
      for line in result:
         print "    " + line
      print "=======================>"
   


def split_into_batches(file, database_files,  dbnames, size):
    user, server = getUserServer()
    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py','--home-dir', '\'\'', '--split-into-batches', file, '--batch-size', str(size)]

    for database_file,dbname  in zip(database_files, dbnames):
       args.append('--dbnames')
       args.append(dbname)
       args.append('--database-files')
       args.append(database_file)

    p = create_a_process(args)  
    result = p.communicate()
    #print ' '.join(args)
    printError(result)
    #printResponse(result)
    if result[1].strip()!='':
      return "could not split into batches"
    else:
       return result[0].strip()

def number_of_sequences_in_file(file):
    user, server = getUserServer()
    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py','--home-dir', '\'\'', '--number-of-sequences-in-file', file]
    p = create_a_process(args)  
    result = p.communicate()
    if result[1].strip()!='':
      return "could not count no of sequences"
    else:
       return result[0].strip()

def copy_file(source, target):
    user, server = getUserServer()
    if PATHDELIM=='\\':
        args = [SCP] + WIN_RSA_KEY_ARGS + [source, user+'@'+server+':'+ target]
    else:
        args = [SCP, source , user+'@'+server+':~/'+ target]
        
    p = create_a_process(args)  
    result = p.communicate()[0].strip()
    if result=='':
       return True
    else:
       return False
     
def copy_file_back(source, target):
    user, server = getUserServer()
    if PATHDELIM=='\\':
       args = [SCP] + WIN_RSA_KEY_ARGS + [user+'@'+server+':'+ source, target]
    else: 
       args = [SCP, user+'@'+server+':~/'+ source, target]

    #print ' '.join(args)
    p = create_a_process(args)  
    result = p.communicate()[0].strip()
    if result=='':
       return True
    else:
       return False

def copy_daemon_script():
    user, server = getUserServer()
    
    if PATHDELIM=='\\':
        args = [SCP] + WIN_RSA_KEY_ARGS + ['daemon.py', user+'@'+server+':']
    else:
        args = [SCP,'daemon.py',  user+'@'+server+':~/']
    
    p = create_a_process(args)  
    result = p.communicate()[1].strip()
    if result=='':
       return True
    else:
       return False
     
def submit_job(sample_name, memory, walltime, algorithm):
    user, server = getUserServer()
    args = [SSH, user+'@'+server]
    if PATHDELIM =='\\':
        args = args + WIN_RSA_KEY_ARGS
    args = args + ['python', 'daemon.py','--home-dir', '\'\'', '--submit-job',\
           sample_name, '--memory',  memory, '--walltime', walltime,  '--algorithm', algorithm ]
    #print ' '.join(args)
    p = create_a_process(args)  
    result = p.communicate()
    #print result
    if result[1].strip()=='':
       return True
    else:
       return False

def get_number_of_running_jobs():
    user, server = getUserServer()
    args = [SSH, user+'@'+server, 'python', 'daemon.py','--home-dir', '\'\'', '--get-number-of-running-jobs', user]
    p = create_a_process(args)  
    result = p.communicate()
    if result[1].strip()=='':
       try:
          return  int(result[0].strip())
       except:
          return 0
    else:
       return 0


#def retrieve_results(sample_name, dbname):

def create_a_process(args):
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p


class empty(object):
    pass

def blastgrid(argv):

    opts = empty()
    for key, value in argv.items():
        setattr(opts, key, value)
          
    if not isValid(opts):
       print usage
       sys.exit(0)

    global SSH
    global SCP
    if PATHDELIM=='/':
       SSH = 'ssh'
       SCP = 'scp'
    else:
       SSH = 'executables' + PATHDELIM + 'win' + PATHDELIM + 'bit64' + PATHDELIM + 'plink'
       SCP = 'executables' + PATHDELIM + 'win' + PATHDELIM + 'bit64' + PATHDELIM + 'pscp'

    setUserServer(opts.user, opts.server)
 
    user, server  = getUserServer()


    print ""
    if not check_if_server_is_up(user, server):
       print "     Server " + server + " is not  working"
       return
    else:
       print "     Server " + server + " is working "

    if  copy_daemon_script():
        print "     Successfully copied daemon script"
    else:
        print "     Failed to  copy daemon script"
        sys.exit(0)
        
    # Check if MetaPathways folder is present
    print '     \'MetaPathways\''
    if  check_if_sample_folder_exists('MetaPathways'):
        print "                 found"
    else:
        print "                 NOT found"
        if create_sample_folder('MetaPathways'):
           print "                 just created!"
        else:
           print "                 couldn't create!"

    # create MetaPathways/databases folder
    print "     \'MetaPathways/databases\'"
    if check_if_sample_folder_exists('MetaPathways/databases'):
        print "                 found"
    else: 
        print "                 NOT found"
        if  create_sample_folder('MetaPathways/databases'):
           print "                 just created"
        else:
           print "                 couldn't create!"


    # create MetaPathways/executables folder
    print "     \'MetaPathways/executables\'"
    if check_if_sample_folder_exists('MetaPathways/executables'):
        print "                 found"
    else: 
        print "                 NOT found"
        if  create_sample_folder('MetaPathways/executables'):
           print "                 just created"
        else:
           print "                 couldn't create!"


    MetaPathways='MetaPathways/'
    #Make sure B/LASP is installed
    if opts.algorithm == 'LAST': 
       target = MetaPathways + 'executables/lastal' 
       source = 'executables' + PATHDELIM + 'linux' + PATHDELIM + 'bit64' + PATHDELIM + 'lastal'
    if opts.algorithm == 'BLAST': 
       target = MetaPathways + 'executables/blastp' 
       source = 'executables' + PATHDELIM + 'linux' + PATHDELIM + 'bit64' +PATHDELIM + 'blastp'
    print '     ' + target
    if does_file_exist(target):
        print "                 found"
    else:
       print "                 NOT found"
       #detect architecture code 
       if  copy_file(source, target ):
           print "                 just copied"
       else:
           print "                 couldn't copy!"

    #Make sure FORMATDB is installed
    if opts.algorithm == 'LAST': 
       target = MetaPathways + 'executables/lastdb' 
       source = 'executables' + PATHDELIM + 'linux' + PATHDELIM + 'bit64' + PATHDELIM + 'lastdb'
    if opts.algorithm == 'BLAST': 
       target = MetaPathways + 'executables/formatdb' 
       source = 'executables' + PATHDELIM + 'linux' + PATHDELIM + 'bit64' + PATHDELIM + 'formatdb'
    print '     ' + target
    if does_file_exist(target):
        print "                 found"
    else:
       print "                 NOT found"
       #detect architecture code 
       if  copy_file(source, target ):
           print "                 just copied"
       else:
           print "                 couldn't copy!"

    #for each database upload and format if necessary
    for database_file, dbname, in zip(opts.database_files, opts.dbnames):
       #Make sure DATABASESES are installed
       target = MetaPathways + 'databases' + '/' + database_file 
       print '     ' + target
       if does_file_exist(target):
          print "                 found"
       else:
          print "                 NOT found"
          source = 'blastDB' +  PATHDELIM + database_file
          if  copy_file(source, target ):
             print "                 just copied "
          else:
             print "                 couldn't copy!"

       #Make sure DATABASESES are formatted
       if opts.algorithm == 'LAST': 
          target1 = target+ '*ssp' 
       if opts.algorithm == 'BLAST': 
          target1 = target+ '*psq' 
     
       if does_file_patt_exist(target1):
          print "                 already formatted"
       else:
          print "                 NOT formatted"
          if  format_database(target, opts.algorithm):
             print "                 just formatted"
          else:
             print "                 couldn't format!"
   

    sample_name = re.sub(r'^.*/', '', opts.sample_name)
    sample_name = re.sub(r'^.*[\\]', '', sample_name)
    #sample_name = re.sub(r'^.*[\\]', '', opts.sample_name)

    if opts.run_type=='overwrite':
       print "Removing old sample folder"
       remove_sample_dir(MetaPathways + sample_name)
   
    #create the sample folder MetaPathways/sample
    print "     Sample Folder " + sample_name
    if  check_if_sample_folder_exists(MetaPathways + sample_name):
       print "                 found"
    else:
       print "                 NOT found"
       if create_sample_folder(MetaPathways + sample_name):
          print "                 created!"
       else:
          print "                 NOT created!"
       

    # create MetaPathways/sample/.qstatdir
    folder = MetaPathways + sample_name + PATHDELIM + '.qstatdir'
    print '     ' + folder
    if check_if_sample_folder_exists(folder):
       print "                 found"
    else: 
        print "                 NOT found"
        if  create_sample_folder(folder):
          print "                 created!"
        else:
          print "             NOT created!"



    # copy the faa file to remote head
    source = opts.sample_name + PATHDELIM + 'orf_prediction' + PATHDELIM + sample_name + '.qced.faa'
    target = MetaPathways + sample_name + '/' + sample_name + '.qced.faa'
    print '     ' + target
    if does_file_exist(target):
       print "                 found"
    else:
       print "                 NOT found"
       if  copy_file(source, target ):
           print "                 copied"
       else:
           print "                 couldn't copy!"

   
    fileName = MetaPathways + sample_name +'/' + sample_name + '.qced.faa'
    #print "Number of sequences " +   number_of_sequences_in_file(fileName)

    # now split into batches 
    split_into_batches(fileName, opts.database_files, opts.dbnames, opts.batch_size)

    numsamples = number_of_samples(sample_name)
    print '     Number of sequence files created :' + str(numsamples)
    
    print "\n"
# setup toolbar
    #toolbar_width = 100

    #sys.stdout.flush()
    #sys.stdout.write("\b"*(toolbar_width)) # return to start of line, after '['
    prevLen = 0 


    completed_dictionary ={}

    LIMIT = 100000
    iter = 0
    for i in xrange(LIMIT):
#       time.sleep(3) # do real work here
       iter = i
       completedsamples = number_of_completed(sample_name)
       current = int((completedsamples*100)/numsamples)
       number_running_jobs=get_number_of_running_jobs()

       if int(number_running_jobs) < int(opts.max_parallel_jobs):
          for database_file, dbname in zip(opts.database_files, opts.dbnames):
            # print "submitting "
             submit_job(sample_name, opts.mem, opts.walltime, opts.algorithm)
      
       # check if it is complete
       completed_count = 0
       for database_file, dbname in zip(opts.database_files, opts.dbnames):
            if not dbname in completed_dictionary and  is_complete(sample_name, dbname):
              if not consolidate(sample_name, dbname):
                   print "Consolidation failed! for database " + dbname
              else: # successful consolidation 
                   completed_dictionary[dbname] = True 
                   print "Consolidated results for search against database : " + dbname


       statString=  str(completedsamples) + '/' + str(numsamples) + '  (' + str(current) + '%)'
       sys.stdout.write("\b"*(prevLen)) # return to start of line, after '['
       sys.stdout.write(statString) # return to start of line, after '['
       sys.stdout.flush()
       prevLen = len(statString)

       if len(opts.database_files) == len(completed_dictionary):
          break
    sys.stdout.write("\n")

    if iter==LIMIT-1:
       print "WARNING: Max Time Exceeded \n Please restart the script to monitor/submit  jobs"


    for dbname in opts.dbnames: 
       target = opts.sample_name +  PATHDELIM + 'blast_results' + PATHDELIM 
       source = MetaPathways + sample_name + '/' + sample_name + '.' + dbname +'.blastout'
       copy_file_back(source, target)

    #print "Completed calculation!"

