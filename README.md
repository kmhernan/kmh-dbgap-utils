# kmh-dbgap-utils
Some helpers for dealing with dbgap xmls.

## Install

1. `git clone git@github.com:kmhernan/kmh-dbgap-utils.git`
2. `pip install kmh-dbgap-utils`

You should be on `python>=3.5` and it is recommended to install within a virtual environment. Only standard libraries are
used.

## Usage

### Download data dictionary XMLs and create TSV

```
$ kmh-dbgap-utils extractdatadict --help
2020-01-28 19:34:24,281 - kmh-dbgap-utils.main - INFO - ---------------------------------------------------------------------------
2020-01-28 19:34:24,281 - kmh-dbgap-utils.main - INFO - Program Args: kmh-dbgap-utils extractdatadict --help
2020-01-28 19:34:24,281 - kmh-dbgap-utils.main - INFO - Date/time: 2020-01-28 19:34:24.281374
2020-01-28 19:34:24,281 - kmh-dbgap-utils.main - INFO - ---------------------------------------------------------------------------
2020-01-28 19:34:24,281 - kmh-dbgap-utils.main - INFO - ---------------------------------------------------------------------------
usage: KMH dbGap Helpers extractdatadict [-h] --phs PHS --outdir OUTDIR

Download phenotype dictionaries and make TSV.

optional arguments:
  -h, --help       show this help message and exit
  --phs PHS        phsid of the project you want to extract
  --outdir OUTDIR  The directory to put results in
 ```
  
 ### Download variable report XMLs and create TSV
 
 ```
 $ kmh-dbgap-utils extractvariablereport --help
2020-01-28 19:35:27,726 - kmh-dbgap-utils.main - INFO - ---------------------------------------------------------------------------
2020-01-28 19:35:27,726 - kmh-dbgap-utils.main - INFO - Program Args: kmh-dbgap-utils extractvariablereport --help
2020-01-28 19:35:27,726 - kmh-dbgap-utils.main - INFO - Date/time: 2020-01-28 19:35:27.726958
2020-01-28 19:35:27,727 - kmh-dbgap-utils.main - INFO - ---------------------------------------------------------------------------
2020-01-28 19:35:27,727 - kmh-dbgap-utils.main - INFO - ---------------------------------------------------------------------------
usage: KMH dbGap Helpers extractvariablereport [-h] --phs PHS --outdir OUTDIR

Download variable reports and make TSV.

optional arguments:
  -h, --help       show this help message and exit
  --phs PHS        phsid of the project you want to extract
  --outdir OUTDIR  The directory to put results in
  ```
  
  **Note** Currently I only extract variable reports for enumerated valued. Will do others in future.
