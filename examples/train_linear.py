"""Small executable scoring example, not a competitive scientific baseline.

python examples/train_linear.py --root . --task B10_Rch --split isotope101 \
    --output /tmp/linear-predictions.csv
nuclearbench score --root . --task B10_Rch --split isotope101 \
    --predictions /tmp/linear-predictions.csv
"""

import argparse
import csv
from pathlib import Path

import numpy as np

from nuclearbench.bank import validate
from nuclearbench.scoring import partition

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, default=Path("."))
parser.add_argument("--task", default="B10_Rch")
parser.add_argument("--split", default="isotope101")
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
validate(args.root)
_, train = partition(args.root, args.task, args.split, "train")
_, test = partition(args.root, args.task, args.split, "test")


def features(rows):
    return np.asarray([[1.0, r["N"], r["Z"]] for r in rows])


coefficients = np.linalg.lstsq(features(train), [r["y"] for r in train], rcond=None)[0]
predictions = features(test) @ coefficients
with args.output.open("w", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["sample_id", "prediction"])
    writer.writerows((row["sample_id"], float(value)) for row, value in zip(test, predictions))
