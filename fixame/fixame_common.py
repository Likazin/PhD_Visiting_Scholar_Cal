import os
import logging
import sys

__author__ = "Livia Moura"
__copyright__ = "Copyright 2021"
__maintainer__ = "Livia Moura, Rohan Sachdeva"
__email__ = "liviam.moura@gmail.com, rohansach@berkeley.edu"
__status__ = "Development"


def common_validate(**kwargs):
    '''
    *common args*
    fasta:          fasta file for genome|metagenome [.fasta|.fa|.fna]
    output_dir:     output directory where it'll created a fixame_[date] folder
    bins:           folder cointaining bins [.fasta|.fa|.fna]
    #r12:            Interlaced SYNCED forward and reverse paired-end reads
    r1:             Forward paired-end reads
    r2:             Reverse paired-end reads
    '''
    
    if kwargs.get('fasta') and kwargs.get('bins'):
        logging.info('Checking chosen mode [genome/metagenome|bin]')
        logging.error("If you want to curate --bins, do not set --fasta, and vice-versa")
        sys.exit()
        
    if not os.path.exists(kwargs.get('output_dir')):
        logging.info('Checking output folder')
        logging.error("The given path {} does not exist!".format(kwargs.get('output_dir')))
        sys.exit()
    
    if (kwargs.get('minid') < 0.76) or (kwargs.get('minid') > 1.00):
        logging.info('Checking minimum identify for the first alignment')
        logging.error("Please, verify if -minid is >= 0.76 and <= 1.00 ")
        sys.exit()

    if (kwargs.get('num_mismatch') < 0) or (kwargs.get('num_mismatch') > 5):
        logging.info('Checking number of mismatches allowed for the filtering reads')
        logging.error("-num_mismatch must be 0>=x>=5")
        sys.exit()
    
    method = 0
    if kwargs.get('fasta'):
        if os.path.isfile(kwargs.get('fasta')):
            logging.info('Checking if fasta file exists')
        else:
            logging.error('There is no fasta file {}'.format(kwargs.get('fasta')))
            sys.exit()
        
        if not os.path.splitext(kwargs.get('fasta'))[1][1:].strip().lower() in ("fasta","fa","fna"): 
            logging.error('The fasta file should be [.fasta|.fa|.fna]')
            sys.exit()


    if kwargs.get('bins'):
        if not os.path.exists(kwargs.get('bins')):
            logging.info('Checking bins folder')
            logging.error("The given path for the bins {} does not exist!".format(kwargs.get('bins')))
            sys.exit()
        method = 1    
    
    return method


def logging_config(workdir):
    '''Configure the logging'''
    log_file = os.path.join(workdir, "fixame.log")
    log_formatter = logging.Formatter("[%(levelname)s] %(asctime)s %(message)s")
    root_logger = logging.getLogger()
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(log_formatter)
    root_logger.addHandler(ch)
    root_logger.propagate = False


def script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
