#!/usr/bin/env python2
# -*- coding: iso-8859-1 -*-

import csv
import io
import sys

COLUMN_C = "TIMES FIVE"
COLUMN_D = "PLUS THOUSAND"

# The following can be a complex function, somehow computing two numbers from two numbers.
def compute_new_data(old_row):
  return [float(old_row[0]) * 5, float(old_row[1]) + 1000]

# Open the standard input stream as a CSV file.
reader = csv.reader(sys.stdin)
old_names = next(reader)

# Open the standard output stream as a CSV file.
output_stream = io.TextIOWrapper(sys.stdout.buffer, newline="")
writer = csv.writer(output_stream)

# Read one line of the input CSV file at a time,
# and enrich this line with computations from our above complex function,
# then write the enriched line into the output CSV file.
writer.writerow(old_names + [COLUMN_C, COLUMN_D])
for old_row in reader:
  node_label = old_row[0]
  new_row = compute_new_data(old_row[1:])
  writer.writerow(old_row + new_row)
