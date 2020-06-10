#!/usr/bin/env python2
# -*- coding: iso-8859-1 -*-

import csv
import io
import odbAccess

ODB_PATH = "Z:\\database.odb"
ODB_STEP = "Example-Step"
COLUMN_A_NAME = "A"
COLUMN_B_NAME = "B"
ODB_FRAME = -1
CSV_PATH = "Z:\\extracted.csv"

odb = odbAccess.openOdb(ODB_PATH)
frame = odb.steps[ODB_STEP].frames[ODB_FRAME]

# Access two field outputs of the given output database.
A_values = frame.fieldOutputs[COLUMN_A_NAME].values
B_values = frame.fieldOutputs[COLUMN_B_NAME].values
assert len(A_values) == len(B_values)

# Open an output CSV file and write those two field outputs into it.
with open(CSV_PATH, "wb") as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['Node label'] + [COLUMN_A_NAME, COLUMN_B_NAME])
  for i in range(len(A_values)):
    assert A_values[i].nodeLabel == B_values[i].nodeLabel
    field_outputs = [A_values[i].data, B_values[i].data]
    writer.writerow([node_label] + field_outputs)

odb.close()
