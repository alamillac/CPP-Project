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


def compare(file1, file2):
    results = {"names": ['', ''], "chars": [0, 0], "equal": False}
    try:
        with open(file1) as f1:
            text1 = f1.read().strip()

        with open(file2) as f2:
            text2 = f2.read().strip()

        results["names"][0] = file1
        results["names"][1] = file2
        results["chars"][0] = len(text1)
        results["chars"][1] = len(text2)
        results["equal"] = text1 == text2
    except:
        logging.error("Error in function compare")
    return results

if __name__ == "__main__":
    # Dir constants
    dir_raw_data = "data"
    dir_processed = "data_processed"
    dir_models = "data_models"
    dir_results = "results"
    dir_stats = "stats"

    # MiniZinc Model filename
    mzn_models = [
        ("DNA_model.mzn", {"sufix": ""}),
        ("DNA_model_max.mzn", {"sufix": "_max"})
    ]

    not_process = [  # list of files to skip
        # "D2000",
        "D3000",
        "D4000",
        "D5000",
        "D6000"
    ]

    # Init base libs
    mznBuild = DataBuild()
    mznCmd = MiniZinc("mzn-g12fd")
    rebuild_mzn = DNARebuild()

    for root, dirs, files in walk(dir_raw_data):
        for raw_filename in files:
            logging.info("File %s found" % raw_filename)
            if skip(not_process, raw_filename):
                logging.info("Skipping file %s" % raw_filename)
            else:
                logging.info("Starting file %s" % raw_filename)
                time.sleep(0.5)

                # Set namefiles
                raw_file = path.join(root, raw_filename)
                basename = raw_filename.split('.')[0]
                processed_file = path.join(dir_processed, basename + '.dzn')
                modeled_file = path.join(dir_models, basename + '{sufix}.txt')
                result_file = path.join(dir_results, basename + '{sufix}.txt')
                stats_file = path.join(dir_stats, basename + '{sufix}.json')

                # Init process
                mznBuild.clear()
                try:
                    # Build data for MiniZinc model
                    mznBuild.readRawDNAFile(raw_file)
                    mznBuild.writeProcessedDNAFile(processed_file)

                    for mzn_model, mzn_model_sufix in mzn_models:
                        # Try to execute the MiniZinc model with the processed data
                        mznCmd.load(mzn_model)
                        mznCmd.init_stats(stats_file.format(**mzn_model_sufix))
                        result_mzn = mznCmd.run_and_save(processed_file, modeled_file.format(**mzn_model_sufix))

                        # Read data obtained from MiniZinc model
                        model = rebuild_mzn.readModelFromFile(modeled_file.format(**mzn_model_sufix))
                        rebuild_mzn.saveResults(model, mznBuild.DNA_pieces, result_file.format(**mzn_model_sufix))

                    # Compare results
                    diff = compare(result_file.format(**mzn_models[0][1]), result_file.format(**mzn_models[1][1]))
                    logging.info("{} chars in {}, {} chars in {}. Files equal: {}".format(diff["chars"][0], diff["names"][0], diff["chars"][1], diff["names"][1], diff["equal"]))
                except:
                    logging.error("Something was wrong with file %s" % raw_file)
                    time.sleep(3)
