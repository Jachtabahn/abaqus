# What is Abaqus?

[Abaqus](https://en.wikipedia.org/wiki/Abaqus) is a software suite for finite element analysis and computer-aided engineering. It is used for
* modeling of mechanical components,
* analysis of mechanical components,
* visualizing the finite element analysis result.

The Abaqus products use the open-source scripting language Python for scripting and customization. And in this article we will see, how we can write Python scripts to customize Abaqus.

# Output databases

The standard Abaqus workflow looks like this: ![](abaqus-workflow.png)

Now, let's look at a `job.odb` output file. This file represents an **output database**. This output database contains the following things:
* Steps
* Frames
* Field Outputs

An output database can have several steps. Each step is named like `Example-Step`. Each step consists of many frames. The frames are numbered like `0,1,2,3`. Each frame has several field outputs. Each field output has a name and list of numbers. The numbers are usually rational numbers with many digits after the comma.

Now, our job is to extract all field outputs from a specific frame from a specific step from a given output database. Let's write a Python script to do that.

# Field outputs

We will proceed in three steps. First, we will read out all field outputs, that we can find, and write them into a CSV file. CSV means comma-separated values. So we will just write all the numbers from the field output as a comma-separated list of values into a file. We also put the name of the field output into this file. That's it.

Second, we will *enrich* this CSV file with additional lists of numbers. We will compute these new lists from the numbers, that are already there. This computation can be very complex and can involve differentiating or integrating some complex function with the numbers, that are already there, as its parameters. Then, a new **enriched** CSV file is created, containing the old number lists **plus** the new number lists.

Third, we will read this **enriched** CSV file once again to add the new number lists as new field outputs to our output database.

## 1. Extracting field outputs

```
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
```

## 2. Enriching information

```
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
```

## 3. Creating new field outputs

```
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
```
