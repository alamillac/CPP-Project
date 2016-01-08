#!/usr/bin/env python

import os
import json
import logging


class DataBuild(object):
    """Build a data file to be used by a MiniZinc model"""

    def __init__(self, min_k_value=3):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Setting DataBuild")

        self.min_k_value = min_k_value
        self.clear()

    def clear(self):
        self.num_nucleotides_in_original_DNA = 0
        self.num_nucleotides = 0
        self.num_DNA_pieces = 0
        self.max_nucleotides_in_DNA = 0
        self.sizes_DNA_pieces = []
        self.DNA_nucleotides = []
        self.DNA_nucleotides_inv = []

        self.DNA_pieces = []  # Original data from raw files

        self.conversion_table = []

    def readRawDNAFile(self, filename):
        """Read a file with all the pieces of DNA to rebuild the original sequence of DNA and save them in memory"""
        self.logger.info("Reading raw data from file %s" % filename)
        try:
            with open(filename) as raw_DNA_file:
                self.DNA_pieces = [piece_of_DNA.strip() for piece_of_DNA in raw_DNA_file.readlines()]
        except:
            self.logger.error("Something was wrong. The file %s couldn't be opened" % filename)
            raise

        # get the number of nucleotides from filename
        # ex. D2000-1.txt -> 2.000 nucleotides
        basename = os.path.basename(filename)
        self.num_nucleotides_in_original_DNA = int(basename[1:].split('-')[0])

        # get the number of different nucleotides in file
        all_possible_nucleotides = set(''.join(self.DNA_pieces))
        self.num_nucleotides = len(all_possible_nucleotides)

        self.num_DNA_pieces = len(self.DNA_pieces)

        self.sizes_DNA_pieces = [len(piece_of_DNA) for piece_of_DNA in self.DNA_pieces]

        self.max_nucleotides_in_DNA = max(self.sizes_DNA_pieces)

        # iterate in every piece of DNA and fill all the necesary data to build the model
        list_full_nucleotides = []
        for piece_of_DNA in self.DNA_pieces:
            for idx in xrange(self.max_nucleotides_in_DNA):
                if idx < len(piece_of_DNA):
                    nucleotides = piece_of_DNA[:idx + 1]
                    nucleotides_inv = piece_of_DNA[-(idx + 1):]
                    list_full_nucleotides.append(nucleotides)
                    list_full_nucleotides.append(nucleotides_inv)
        unique_full_nucleotides = list(set(list_full_nucleotides))

        self.conversion_table = {unique_full_nucleotides[i]: str(i + 1) for i in xrange(len(unique_full_nucleotides))}
        for piece_of_DNA in self.DNA_pieces:
            row = []
            row_inv = []
            for idx in xrange(self.max_nucleotides_in_DNA):
                if idx < len(piece_of_DNA):
                    nucleotides = piece_of_DNA[:idx + 1]
                    nucleotides_inv = piece_of_DNA[-(idx + 1):]
                    row.append(self.conversion_table[nucleotides])
                    row_inv.append(self.conversion_table[nucleotides_inv])
                else:
                    row.append('0')
                    row_inv.append('0')
            self.DNA_nucleotides.append(row)
            self.DNA_nucleotides_inv.append(row_inv)

        self.logger.info("File readed successfully")

    def dumpListToMiniZincFormat(self, pyLisy):
        return json.dumps(pyLisy)

    def dumpArrayToMiniZincFormat(self, array):
        return '[|' + ' | '.join([', '.join(row) for row in array]) + '|]'

    def getInMiniZincFormat(self):
        return 'num_nucleotides_in_original_DNA = %d;\n' % self.num_nucleotides_in_original_DNA +\
               'num_nucleotides = %d;\n' % self.num_nucleotides +\
               'num_DNA_pieces = %d;\n' % self.num_DNA_pieces +\
               'max_nucleotides_in_DNA = %d;\n' % self.max_nucleotides_in_DNA +\
               'sizes_DNA_pieces = %s;\n' % self.dumpListToMiniZincFormat(self.sizes_DNA_pieces) +\
               'DNA_nucleotides = %s;\n' % self.dumpArrayToMiniZincFormat(self.DNA_nucleotides) +\
               'DNA_nucleotides_inv = %s;\n' % self.dumpArrayToMiniZincFormat(self.DNA_nucleotides_inv) +\
               'min_k_value = %d;\n' % self.min_k_value

    def writeProcessedDNAFile(self, filename):
        """Write the DNA data already processed to be read by the Minizinc model"""
        self.logger.info("Saving processed data in %s" % filename)
        try:
            with open(filename, 'w') as mz_data_file:
                mz_data_file.write(self.getInMiniZincFormat())
            self.logger.info("Data saved successfully")
        except:
            self.logger.error("Something was wrong. The file %s couldn't be saved" % filename)
            raise

if __name__ == "__main__":
    mznBuild = DataBuild()
    mznBuild.readRawDNAFile('data/D2000-1.txt')
    print mznBuild.getInMiniZincFormat()
    mznBuild.writeProcessedDNAFile('data_processed/D2000-1.dzn')

    # mzn-g12fd DNA_model.mzn data_test/D200-3.dzn
