#!/usr/bin/env python3
import os
import subprocess
import sys
from subprocess import PIPE
sys.path.append("checker")

import dfa
import dfa_equivalence


POINTS_PER_TEST = 5
SRCFILE = "main.py"
TESTDIR = "tests"
TEST_TIMEOUT = 8  # seconds


def run_test(test):
    # Ensure out directory exists
    test_out = os.path.join(TESTDIR, "out")
    os.makedirs(test_out, exist_ok=True)

    infile = os.path.join(TESTDIR, "in", test)
    outfile = os.path.join(test_out, test)
    reffile = os.path.join(TESTDIR, "ref", test)

    cmd = "python3 '{}' '{}' '{}'".format(SRCFILE, infile, outfile)
    timeout_cmd = "timeout -k {0} {0} {1}".format(TEST_TIMEOUT, cmd)
    cp = subprocess.run(timeout_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    if cp.returncode == 124:
        return 0

    with open(outfile, "r") as fin:
        out_text = fin.read()

    out_dfa = dfa.parse_dfa(out_text)

    try:
        with open(reffile, "r") as fin:
            ref_text = fin.read()
    except FileNotFoundError:
        print("No ref file for test {}".format(test))
        return False

    ref_dfa = dfa.parse_dfa(ref_text)

    return dfa_equivalence.language_eq(out_dfa, ref_dfa)


if __name__ == "__main__":
    if not (os.path.isfile(SRCFILE) and os.access(SRCFILE, os.R_OK)):
        sys.stderr.write("{} unavailable or unreadable!\n".format(SRCFILE))
        sys.exit(1)

    tests = os.listdir(os.path.join(TESTDIR, "in"))
    nr_tests = len(tests)
    total = 0
    max_points = nr_tests * POINTS_PER_TEST

    header = " Running tests: "
    # This number is computed by summing the numbers in {} and the count of
    # characters outside of {} in...
    print("{:=^73}".format(header))
    print("{} {: <25} {: >20} {: >8} {: >8}\n".format("TEST #  ", "NAME", "",
                                                      "STATUS", "POINTS"))
    for i, test in enumerate(tests):
        passed = run_test(test)
        crt_points = POINTS_PER_TEST if passed else 0
        total += crt_points
        str_status = "PASSED" if passed else "FAILED"
        str_points = "[{}/{}]".format(crt_points, POINTS_PER_TEST)
        # ... this print
        print("{: >6} - {: <25} {:.>20} {: >8} {: >8}".format(i + 1, test, "",
                                                              str_status,
                                                              str_points))

    print("\nTOTAL: {}/{}\n".format(total, max_points))
