import os
import sys
import argparse
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import ocrolib
from shutil import copyfile

parser = argparse.ArgumentParser()

parser.add_argument("files", nargs="+", help="input files")
parser.add_argument("--folds", type=int, default=5, help="number of folds")
parser.add_argument("--output", type=str, default="Data", help="output folder")

args = parser.parse_args()

line_candidates = args.files
number_of_folds = args.folds
output_dir = args.output

assert(number_of_folds > 1)
assert(not os.path.isdir(output_dir))

lines = []

for line in sorted(line_candidates):
    base, ext = ocrolib.allsplitext(line)

    if ext.endswith(".png"):
        gt = base + ".gt.txt"
        if os.path.isfile(gt):
            lines.append((base, ext))

assert(len(lines) >= number_of_folds)

output_dir = os.path.join(output_dir, "Folds")

for i in range(0, number_of_folds):
    if not os.path.exists(os.path.join(output_dir,str(i))):
        os.makedirs(os.path.join(output_dir,str(i)))

print(lines)

for i, line in enumerate(lines):
    fold = i%number_of_folds
    base, ext = line
    copyfile(base + ext, os.path.join(output_dir, str(fold), str(fold) + "__" + os.path.basename(base) + ext))
    copyfile(base + ".gt.txt", os.path.join(output_dir, str(fold), str(fold) + "__" + os.path.basename(base) + ".gt.txt"))