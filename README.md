# ROC-HPL(MXP) sweeper utility

## Setup
this repo is managed with `uv`, to start the virtual environment simply run
`
  uv sync
`

## To Run

1. Build Roc-HPL and/or Roc-HPL  
2. specify the proper path for where HPL/HPL-MXP are built
3. run `uv run main.py`

```
HPL_Sweep Object
  hpl_path: path for where HPL was built
  executable: mpi script used to run HPL
  log_file: file to serialize csv to after sweep is performed (file extention not needed)
  linen: index in stdout where gflops is outputted
  N: N parameter for hpl runs
  log_url (optional): if there is an ntfy instance you can log state in there
```
