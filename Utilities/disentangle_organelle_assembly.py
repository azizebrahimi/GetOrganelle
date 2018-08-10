#!/usr/bin/env python
# coding: utf8
import time
import os
import sys
from optparse import OptionParser
path_of_this_script = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(path_of_this_script, ".."))
from Library.assembly_parser import *
from Library.seq_parser import *
path_of_this_script = os.path.split(os.path.realpath(__file__))[0]


def disentangle_circular_assembly(fastg_file, tab_file, prefix, weight_factor, depth_factor,
                                  display=True, keep_temp=False):
    time_a = time.time()
    if display:
        sys.stdout.write("Reading " + fastg_file + " ..\n")
    input_graph = Assembly(fastg_file)
    time_b = time.time()
    if display:
        sys.stdout.write("\n>>> Parsing input fastg file finished: " + str(round(time_b - time_a, 4)) + "s\n")
    temp_graph = prefix + ".temp.fastg" if keep_temp else None
    idealized_graph = input_graph.find_target_graph(tab_file, weight_factor=weight_factor, depth_factor=depth_factor,
                                                    temp_graph=temp_graph, display=display)["graph"]
    time_c = time.time()
    if display:
        sys.stdout.write("\n\n>>> Detecting target graph finished: " + str(round(time_c - time_b, 4)) + "s\n")
    # should add making one-step-inversion pairs for paths,
    # which would be used to identify existence of a certain isomer using mapping information
    count_path = 0
    for this_path in idealized_graph.get_all_circular_paths():
        count_path += 1
        open(prefix + "." + str(count_path) + ".path_sequence.fasta", "w").\
            write(idealized_graph.export_path(this_path).fasta_str())
    time_d = time.time()
    if display:
        sys.stdout.write("\n\n>>> Solving and unfolding graph finished: " + str(round(time_d - time_c, 4)) + "s\n")
    idealized_graph.write_to_file(prefix + ".selected_graph.fastg")


def get_options():
    parser = OptionParser("disentangle_organelle_assembly.py -g input.fastg -t input.tab -o output_dir")
    parser.add_option("-g", dest="fastg_file",
                      help="input fastg format file.")
    parser.add_option("-t", dest="tab_file",
                      help="input tab format file produced by slim_fastg.py.")
    parser.add_option("-o", dest="output_directory",
                      help="output directory.")
    parser.add_option("--depth-f", dest="depth_factor", type=float, default=None,
                      help="depth factor for excluding non-target contigs. Default: auto")
    parser.add_option("--weight-f", dest="weight_factor", type=float, default=100.0,
                      help="weight factor for excluding non-target contigs. Default:%default")
    parser.add_option("--silent", dest="silent", default=False, action="store_true")
    parser.add_option("--keep-temp", dest="keep_temp_graph", default=False, action="store_true",
                      help="for debug.")
    options, argv = parser.parse_args()
    if (options.fastg_file is None) or (options.tab_file is None) or (options.output_directory is None):
        parser.print_help()
        sys.stdout.write("Insufficient arguments!\n")
        sys.exit()
    else:
        return options, argv


def main():
    time0 = time.time()
    options, argv = get_options()
    if not options.silent:
        sys.stdout.write("\nThis is a script for extracting circular organelle genome from assembly result (fastg). "
                         "\nBy jinjianjun@mail.kib.ac.cn\n\n")
    if options.output_directory and not os.path.exists(options.output_directory):
        os.mkdir(options.output_directory)
    disentangle_circular_assembly(options.fastg_file, options.tab_file,
                                  os.path.join(options.output_directory, "target"),
                                  weight_factor=options.weight_factor, depth_factor=options.depth_factor,
                                  display=not options.silent, keep_temp=options.keep_temp_graph)
    if not options.silent:
        sys.stdout.write('\nTotal cost: ' + str(round(time.time() - time0, 4)) + 's\n\n')


if __name__ == '__main__':
    main()


"""Copyright 2018 Jianjun Jin"""
