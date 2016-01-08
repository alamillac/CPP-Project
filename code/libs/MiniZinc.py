#!/usr/bin/env python

from subprocess import check_output
from os import path
import logging
import timeit
import json


class MiniZinc(object):
    def __init__(self, mz_cmd="mzn-g12fd", model=None):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Setting MiniZinc command")

        self.mz_cmd = mz_cmd
        if model:
            self.load(model)
        else:
            self.model = None

        self.statsfile = None

    def init_stats(self, statsfile):
        self.statsfile = statsfile

    def load(self, filename_model):
        self.model = filename_model

    def run(self, filename):
        if not self.model:
            raise Exception("Not model loaded")

        command = [self.mz_cmd, self.model, filename]
        self.logger.info("Running: '%s'. This could take some time" % " ".join(command))
        try:
            tic = timeit.default_timer()
            result = check_output(command)
            toc = timeit.default_timer()
            exec_time = toc - tic
            self.logger.info("Command executed successfully. It takes %s seconds to complete." % exec_time)

            if self.statsfile:
                self.logger.info("Saving stats in %s." % self.statsfile)
                try:
                    with open(self.statsfile, 'w') as f:
                        json.dump({"processing_time": exec_time}, f)
                    self.logger.info("Stats saved")
                except:
                    self.logger.warn("The stats file %s couldn't be saved" % self.statsfile)
            return result
        except:
            self.logger.error("MiniZin command fail")
            raise

    def run_and_save(self, inputfile, outputfile, skip_if_exist=True):
        if skip_if_exist and path.isfile(outputfile):
            self.logger.warn("Skipping MiniZinc command. The file %s already exist and skip option is True" % outputfile)
            return

        response = self.run(inputfile)
        self.logger.info("Saving data model in %s" % outputfile)
        try:
            with open(outputfile, 'w') as f:
                f.write(response)
            self.logger.info("File %s created successfully" % outputfile)
        except:
            self.logger.error("File %s couldn't be created" % outputfile)
            raise
