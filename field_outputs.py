#!/usr/bin/env python2
# -*- coding: iso-8859-1 -*-

import csv
import io
import odbAccess

ODB_PATH = "Z:\\database.odb"
ODB_STEP = "Example-Step"
ODB_FRAME = -1
ODB_INSTANCE = "EXAMPLE-INSTANCE"
CSV_PATH = "Z:\\enriched.csv"

odb = odbAccess.openOdb(ODB_PATH)
frame = odb.steps[ODB_STEP].frames[ODB_FRAME]
instance = odb.rootAssembly.instances[ODB_INSTANCE]

# Read the enriched CSV.
csvfile = open(CSV_PATH)
reader = csv.reader(csvfile)
names = next(reader)
csv_data = [[] for _ in names]
for row in reader:
  for i in range(len(row)):
    if i == 0:
      csv_data[i].append(int(row[i]))
    else:
      csv_data[i].append((float(row[i]),))
csvfile.close()

# For each new list of numbers, add a new field output.
for i, name in enumerate(names):
  if i == 0: continue
  if name in frame.fieldOutputs.keys(): continue

  new_field_output = frame.FieldOutput(name=name, description=name, type=odbAccess.SCALAR)
  new_field_output.addData(
    position = odbAccess.NODAL,
    instance = instance,
    labels = csv_data[0],
    data = csv_data[i])

odb.save()
odb.close()
