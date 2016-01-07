#!/usr/bin/env python

import os
import json


class DataBuild(object):
    """Build a data file to be used by a MiniZinc model"""

    def __init__(self, min_k_value=3):
        self.num_nucleotides_in_original_DNA = 0
        self.num_nucleotides = 0
        self.num_DNA_pieces = 0
        self.max_nucleotides_in_DNA = 0
        self.sizes_DNA_pieces = []
        self.DNA_nucleotides = []

        self.DNA_pieces = []  # Original data from raw files

        self.min_k_value = min_k_value

        self.conversion_table = []

    def readRawDNAFile(self, filename):
        """Read a file with all the pieces of DNA to rebuild the original sequence of DNA and save them in memory"""
        with open(filename) as raw_DNA_file:
            self.DNA_pieces = [piece_of_DNA.strip() for piece_of_DNA in raw_DNA_file.readlines()]

        # get the number of nucleotides from filename
        # ex. D2000-1.txt -> 2.000 nucleotides
        basename = os.path.basename(filename)
        self.num_nucleotides_in_original_DNA = int(basename[1:].split('-')[0])

        # get the number of different nucleotides in file
        all_possible_nucleotides = list(set(''.join(self.DNA_pieces)))
        self.num_nucleotides = len(all_possible_nucleotides)

        self.num_DNA_pieces = len(self.DNA_pieces)

        self.sizes_DNA_pieces = [len(piece_of_DNA) for piece_of_DNA in self.DNA_pieces]

        self.max_nucleotides_in_DNA = max(self.sizes_DNA_pieces)

        # iterate in every piece of DNA and fill all the necesary data to build the model
        self.conversion_table = {all_possible_nucleotides[i]: i + 1 for i in xrange(len(all_possible_nucleotides))}
        for piece_of_DNA in self.DNA_pieces:
            row = []
            for idx in xrange(self.max_nucleotides_in_DNA):
                if idx < len(piece_of_DNA):
                    nucleotides = piece_of_DNA[idx]
                    row.append(self.conversion_table[nucleotides])
                else:
                    row.append(0)
            self.DNA_nucleotides.append(row)

    def dumpListToMiniZincFormat(self, pyLisy):
        return json.dumps(pyLisy)

    def dumpArrayToMiniZincFormat(self, array):
        return '[|' + ' | '.join([', '.join([str(element) for element in row]) for row in array]) + '|]'

    def getInMiniZincFormat(self):
        return 'num_nucleotides_in_original_DNA = %d;\n' % self.num_nucleotides_in_original_DNA +\
               'num_nucleotides = %d;\n' % self.num_nucleotides +\
               'num_DNA_pieces = %d;\n' % self.num_DNA_pieces +\
               'max_nucleotides_in_DNA = %d;\n' % self.max_nucleotides_in_DNA +\
               'sizes_DNA_pieces = %s;\n' % self.dumpListToMiniZincFormat(self.sizes_DNA_pieces) +\
               'DNA_nucleotides = %s;\n' % self.dumpArrayToMiniZincFormat(self.DNA_nucleotides) +\
               'min_k_value = %d;\n' % self.min_k_value

    def writeProcessedDNAFile(self, filename):
        """Write the DNA data already processed to be read by the Minizinc model"""
        with open(filename, 'w') as mz_data_file:
            mz_data_file.write(self.getInMiniZincFormat())

if __name__ == "__main__":
    mznBuild = DataBuild()
    mznBuild.readRawDNAFile('data/D200-3.txt')
    print mznBuild.getInMiniZincFormat()
    mznBuild.writeProcessedDNAFile('data_test/D200-3.dzn')

    # mzn-g12fd DNA_model.mzn data_test/D200-3.dzn
