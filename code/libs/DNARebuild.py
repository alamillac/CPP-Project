#!/usr/bin/env python

import json
import re
import logging


class DNARebuild(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Setting DNARebuild")

    def readModelFromString(self, model_data_str):
        """Read the data obtained from the MiniZinc model and rebuild the original ADN.
        modelData should has the form:
        {
        "original_DNA_order": [ARRAY],
        "k": [ARRAY]
        }
        ----------"""
        # Here we only need to get the data inside {} and send it to a json parser
        model = {"original_DNA_order": [], "k": []}

        try:
            regModel = re.match(r'{.+}', model_data_str)  # Get all inside {}
            model_json = regModel.group(0)
            model = json.loads(model_json)
            self.logger.info("Model obtained successfully")
        except:
            if "UNSATISFIABLE" in model_data_str:
                self.logger.warn("This model is unsatisfiable")
            else:
                self.logger.error("Something was wrong. The model has not a proper format")
                raise

        return model

    def readModelFromFile(self, filename):
        self.logger.info("Reading data from model in file %s" % filename)
        try:
            with open(filename) as model_file:
                model_data_str = model_file.read()
        except:
            self.logger.error("Something was wrong. The file %s couldn't be opened" % filename)
            raise

        return self.readModelFromString(model_data_str)

    def getResults(self, model, DNA_pieces):
        sorted_DNA_pieces = []
        for i in xrange(len(model["original_DNA_order"])):
            if i < len(model["k"]):
                current_DNA = DNA_pieces[model["original_DNA_order"][i] - 1][:-model["k"][i]]
            else:
                current_DNA = DNA_pieces[model["original_DNA_order"][i] - 1]
            sorted_DNA_pieces.append(current_DNA)
        return ''.join(sorted_DNA_pieces)

    def showResults(self, model, DNA_pieces):
        self.logger.info("Showing results in console")
        print self.getResults(model, DNA_pieces)

    def saveResults(self, model, DNA_pieces, result_filename):
        self.logger.info("Saving results in file %s" % result_filename)
        try:
            result = self.getResults(model, DNA_pieces)
            with open(result_filename, 'w') as result_file:
                result_file.write(result)
            self.logger.info("Results file save successfully")
            self.logger.info("DNA: %s" % result)
        except:
            self.logger.error("Something was wrong saving the file %s" % result_filename)

if __name__ == "__main__":
    rebuild_mzn = DNARebuild()
    model = rebuild_mzn.readModelFromFile("data_models/D200-1.txt")
    rebuild_mzn.showResults(model)
