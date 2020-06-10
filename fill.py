#!/usr/bin/env python2
# -*- coding: iso-8859-1 -*-

import csv
import io
import sys

COLUMN_C = "TIMES FIVE"
COLUMN_D = "PLUS THOUSAND"

def compute_new_data(old_row):
  return [float(old_row[0]) * 5, float(old_row[1]) + 1000]

reader = csv.reader(sys.stdin)
output_stream = io.TextIOWrapper(sys.stdout.buffer, newline="")
writer = csv.writer(output_stream)
old_names = next(reader)

writer.writerow(old_names + [COLUMN_C, COLUMN_D])
for old_row in reader:
  node_label = old_row[0]
  new_row = compute_new_data(old_row[1:])
  writer.writerow(old_row + new_row)
