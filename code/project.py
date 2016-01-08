#!/usr/bin/env python

from libs import DNARebuild, DataBuild, MiniZinc
import logging
from os import path, walk
import time

logfile = "project.log"

# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                    # datefmt='%m-%d %H:%M',
                    filename=logfile,
                    filemode='a')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)


def skip(skipped_files, current_file):
    result = False
    i = 0
    while not result and i < len(skipped_files):
        if skipped_files[i] in current_file:
            result = True
        i += 1
    return result

if __name__ == "__main__":
    # Dir constants
    dir_raw_data = "data"
    dir_processed = "data_processed"
    dir_models = "data_models"
    dir_results = "results"
    dir_stats = "stats"

    # MiniZinc Model filename
    mzn_model = "DNA_model.mzn"

    not_process = [  # list of files to skip
        "D2000",
        "D3000",
        "D4000",
        "D5000",
        "D6000"
    ]

    # Init base libs
    mznBuild = DataBuild()
    mznCmd = MiniZinc("mzn-g12fd", mzn_model)
    rebuild_mzn = DNARebuild()

    for root, dirs, files in walk(dir_raw_data):
        for raw_filename in files:
            logging.info("File %s found" % raw_filename)
            if skip(not_process, raw_filename):
                logging.info("Skipping file %s" % raw_filename)
            else:
                logging.info("Starting file %s" % raw_filename)
                time.sleep(1)

                # Set namefiles
                raw_file = path.join(root, raw_filename)
                basename = raw_filename.split('.')[0]
                processed_file = path.join(dir_processed, basename + '.dzn')
                modeled_file = path.join(dir_models, basename + '.txt')
                result_file = path.join(dir_results, basename + '.txt')
                stats_file = path.join(dir_stats, basename + '.json')

                # Init process
                mznBuild.clear()
                try:
                    # Build data for MiniZinc model
                    mznBuild.readRawDNAFile(raw_file)
                    mznBuild.writeProcessedDNAFile(processed_file)

                    # Try to execute the MiniZinc model with the processed data
                    mznCmd.init_stats(stats_file)
                    result_mzn = mznCmd.run_and_save(processed_file, modeled_file)

                    # Read data obtained from MiniZinc model
                    model = rebuild_mzn.readModelFromFile(modeled_file)
                    rebuild_mzn.saveResults(model, result_file)
                except:
                    logging.error("Something was wrong with file %s" % raw_file)
                    time.sleep(3)
