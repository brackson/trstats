# TRStats

## Summary
This was a Python assignment for my Computer Networking class. It performs traceroute statistics for a given host. It is PEP-8 compliant. It outputs statistics to a output.json file that contains the format:

```
{
  "avg": 1.123,         # average time of pings
  "hop": 1,             # hop number (omits if * is ever returned)
  "hosts": [            # destination system, destination IP
    "gateway",
    "(128.192.101.129)"
  ],
  "max": 1.123,         # maximum ping
  "med": 1.123,         # median ping
  "min": 1.123          # minimum ping
}, ...
```



## Usage
```
python3 trstats.py [-h] [-n NUM_RUNS] [-d RUN_DELAY] [-m MAX_HOPS] [-o OUTPUT]
                  [-t TARGET] [--test TEST_DIR] [--debug]

Run traceroute multiple times towards a given target host

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_RUNS, --num_runs NUM_RUNS
                        Number of times traceroute will run (default=1)
  -d RUN_DELAY, --run_delay RUN_DELAY
                        Number of seconds to wait between two consecutive runs (default=0)
  -m MAX_HOPS, --max_hops MAX_HOPS
                        Max number of hops that traceroute will probe (default=30)
  -o OUTPUT, --output OUTPUT
                        Path and name (without extension) of the .json output
                        file (default="output.json")
  -t TARGET, --target TARGET
                        A target domain name or IP address (default=www.google.com)
  --test TEST_DIR       Directory containing num_runs text files, each of
                        which contains the output of a traceroute run. If
                        present, this will override all other options and
                        traceroute will not be invoked. Statistics will be
                        computed over the traceroute output stored in the text
                        files only.
  --debug               Enable to create an output_debug.json file with an
                        all_results[] list in each hop stat dictionary that
                        contains all the hop latency data used in calculating
                        the avg, min, med, and max keys. (default=False)

```

## Example
```
$ python3 trstats.py -t www.bing.com -n 2

$ cat output.json
[
  {
    "avg": 1.304,
    "hop": 1,
    "hosts": [
      "gateway",
      "(128.192.101.129)"
    ],
    "max": 1.772,
    "med": 1.304,
    "min": 0.811
  },
    ...
  {
    "avg": 18.493,
    "hop": 16,
    "hosts": [
      "ae55-0.icr02.bl20.ntwk.msn.net",
      "(104.44.238.133)"
    ],
    "max": 19.013,
    "med": 18.493,
    "min": 17.799
  }
]
```
