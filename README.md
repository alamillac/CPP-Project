# CPP-Project
Rebuild DNA sequence using MiniZinc

## Run
To run the code you just have to run the python file **project.py**. In linux this could be done with `./project.py` or `python project.py`

## Config
In the file project.cfg you can set some variables to run the code.

* **mzn_path:** is the path where the MiniZinc command (**mzn-g12fd**) resides. This command is used in the code to load and run the MiniZinc model.

* **skip_mzn_command:** This can be set as **true** or **false**. And indicate if the MiniZinc model should be executed if a previous solution was already found. All the solutions are saved in **data_models**. So if the file *data_models/D2000-3.txt* exist and *skip_mzn_command=true* then the command `mzn-g12fd DNA_model.mzn data_processed/D2000-3.dzn` won't be executed. This is just to save time in models that were previously found.

* **not_process:** This is a list of files to skip. ex: **D3000** says that all the files starting with D3000 will be ignored. In this example *D3000-3.txt* and *D3000-1.txt* will be ignored.
