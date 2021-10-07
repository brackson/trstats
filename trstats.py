#!/usr/bin/env python3
# PEP-8 compliant

# Author: Brandon Jackson
# Class: CSCI4760 Computer Networks, Miao
# Date: 1 Oct 2021
# Assignment: Programming Assignment 1: Traceroute Latency Statistics

import argparse
import json
import os
import pathlib
import re
from statistics import mean, median
import sys
import tempfile
import time


class Trstats:
    def __init__(self, runs, run_delay, max_hops, output, target, test, debug):
        self.num_runs = runs
        self.run_delay = run_delay
        self.max_hops = max_hops
        self.output = output
        self.target = target
        self.test = test
        self.debug = debug

        self.return_list = []
        # increment self.num_ran each time we traceroute until num_runs
        self.num_ran = 0

        if(self.test == "no"):
            for _ in range(self.num_runs):
                self.get_traceroute_output()
                time.sleep(self.run_delay)
        else:
            # grab all text files in ./{self.test} directory
            tr_files = []

            with os.scandir(f"{pathlib.Path().resolve()}/{self.test}") as it:
                for entry in it:
                    if entry.name.endswith(".txt") and entry.is_file():
                        self.get_traceroute_output(tr_file_path=entry.path)
                        time.sleep(self.run_delay)

        if debug:
            with open('output_debug.json', 'w') as outfile:
                json.dump(self.return_list, outfile)

        # all finished, lets remove all_results[] from each hop dict entry
        # and round avg (and median for some reason?)
        for hop_entry in self.return_list:
            hop_entry.pop("all_results")
            hop_entry["avg"] = round(hop_entry["avg"], 3)
            hop_entry["med"] = round(hop_entry["avg"], 3)

        with open(self.output, 'w') as outfile:
            json.dump(self.return_list, outfile)

    def get_traceroute_output(self, tr_file_path=None):

        if tr_file_path is None:
            # create tempfile
            temp = tempfile.NamedTemporaryFile()
            cmd = f"traceroute {self.target} -m {self.max_hops} > {temp.name}"
            os.system(cmd)
            tr_file_name = temp.name
        else:
            tr_file_name = tr_file_path

        for line in open(tr_file_name, "r"):
            # check if it's a blank line; skip if so
            if line == "\n":
                continue

            # remove trailing newline
            line = line.rstrip()

            self.build_hop_dict(line)

        self.num_ran += 1

    def build_hop_dict(self, hop_line):
        # we skip if line contains "traceroute to" (indicates first info msg)
        if "traceroute to" in hop_line:
            return 0

        # we skip if we find an asterisk (which indicates timeout)
        if "*" in hop_line:
            return 0

        # the next 2 sections use different regex patterns bc regex is hard :(
        # use regex to grab the hop #, destination system and destination IP
        info_pattern = "^\s*(\d*)\s*([^\s]+)\s*([^\s]+)"
        info = re.findall(info_pattern, hop_line)

        # use another regex to grab the three time stats given
        stats_pattern = "\S*\s(?=ms)"
        stats = re.findall(stats_pattern, hop_line)

        # convert strings in stats[] to floats
        for i in range(len(stats)):
            stats[i] = float(stats[i])

        stats_average = mean(stats)
        stats_median = median(stats)

        if self.num_ran == 0:
            stat_dict = {
                "all_results": stats,
                "avg": stats_average,
                "hop": int(info[0][0]),
                "hosts": [info[0][1], info[0][2]],
                "max": max(stats),
                "med": stats_median,
                "min": min(stats)
            }

            self.return_list.append(stat_dict)
        else:
            # find dict in return_list[] that matches our hop
            original_dict = next((d for d in self.return_list
                                  if d.get("hop") == int(info[0][0])), None)

            # if it hasn't been put into the return_list on the first try, skip
            if original_dict is None:
                return

            original_dict["all_results"] += stats
            original_dict["avg"] = mean(original_dict["all_results"])
            original_dict["max"] = max(original_dict["all_results"])
            original_dict["med"] = median(original_dict["all_results"])
            original_dict["min"] = min(original_dict["all_results"])


def main():
    parser = argparse.ArgumentParser(description="Run traceroute multiple times\
        towards a given target host")

    parser.add_argument("-n", "--num_runs", metavar="NUM_RUNS",
                        help="Number of times traceroute will run",
                        type=int, default=1)

    parser.add_argument("-d", "--run_delay", metavar="RUN_DELAY",
                        help="Number of seconds to wait between two\
                        consecutive runs", type=float, default=0)

    parser.add_argument("-m", "--max_hops", metavar="MAX_HOPS",
                        help="Max number of hopes that traceroute will probe",
                        type=int, default=30)

    parser.add_argument("-o", "--output", metavar="OUTPUT",
                        help="Path and name (without extension) of the .json\
                        output file", type=str, default="output.json")

    parser.add_argument("-t", "--target", metavar="TARGET",
                        help="A target domain name or IP address",
                        type=str, default="www.google.com")

    parser.add_argument("--test", metavar="TEST_DIR",
                        help="Directory containing num_runs text files, each of\
                        which contains the output of a traceroute run. If\
                        present, this will override all other options and\
                        traceroute will not be invoked. Statistics will be\
                        computed over the traceroute output stored in the text\
                        files only.", type=str, default="no")

    parser.add_argument("--debug",
                        help="Enable to create an output_debug.json file with\
                        an all_results[] list in each hop stat dictionary that\
                        contains all the hop latency data used in calculating\
                        the avg, min, med, and max keys.", action="store_true")

    args = parser.parse_args()

    trstats = Trstats(args.num_runs, args.run_delay, args.max_hops,
                      args.output, args.target, args.test, args.debug)

    return 0

if __name__ == '__main__':
    sys.exit(main())
