import os
import argparse
import Voting
import re

parser = argparse.ArgumentParser()

parser.add_argument("input_dirs", nargs="+",
                    help="dirs containing dirs with the output of the different voters: *.txt and *.llocsExt")

args = parser.parse_args()
input_dirs = args.input_dirs


def load_llocs(link):
    file = open(link, "r")
    data = file.read()

    if data.endswith("\n"):
        data = data[:-1]
    rows = data.split("\n")

    #llocs can start or end with whitespace
    while(rows[0].startswith(" ")):
        rows.pop(0)

    while(rows[-1].startswith(" ")):
        rows.pop(-1)

    line_llocs = []
    llocs_string = ""

    last_space = False

    for i, row in enumerate(rows):
        cols = row.split("\t")

        #assert(len(cols) == 5)
        #TODO
        if len(cols) == 5:
            char = cols[0]

            #if char == u'\u0303':
            #    continue

            prob = cols[3]
            llocs = {char : float(prob)}

            alts = cols[4].split("||")

            for alt in alts:
                alt = alt.split("__")
                if len(alt) == 2:
                    llocs[alt[0]] = float(alt[1])

            #get rid of two or more whitespaces in a row
            if last_space and char == " ":
                line_llocs[-1].update({" ": 100.0})
                continue

            if char == " ":
                last_space = True
            else:
                last_space = False

            llocs_string += char
            line_llocs.append(llocs)

    return llocs_string, line_llocs


def init_ocr_result(folder, ocr_file):
    ocr_file = os.path.join(folder, ocr_file)
    llocs_file = ocr_file.replace(".txt", ".extLlocs")

    if os.path.exists(llocs_file):
        file = open(ocr_file, "r")
        ocr = file.read().strip()

        llocs_string, line_llocs = load_llocs(llocs_file)

        return ocr, llocs_string, line_llocs


def find_voters_with_most_frequent_legth(sync, voters):
    lengths = {}

    for i, voter in enumerate(voters):
        length = sync.length(i)

        if length in lengths:
            lengths[length] += 1
        else:
            lengths[length] = 1

    most_freq_length = -1
    occurrences = 0

    for length in lengths.keys():
        if lengths[length] < occurrences:
            continue
        elif lengths[length] == occurrences:
            if length < most_freq_length:
                most_freq_length = length
                occurrences = lengths[length]
        else:
            most_freq_length = length
            occurrences = lengths[length]

    #print(most_freq_length)

    actual_voters = []

    for i, voter in enumerate(voters):
        if sync.length(i) == most_freq_length:
            actual_voters.append(i)

    return actual_voters, most_freq_length


def add_llocs(sum, new):
    for char in new:
        if char in sum:
            sum[char] += new[char]
        else:
            sum[char] = new[char]


def get_most_likely_char(sum):
    return max(sum, key=lambda key: sum[key])


all = 0
skipped = 0


def perform_conf_vote(voters):
    global all
    global skipped

    results = [voter[1] for voter in voters]

    synclist = Voting.synchronize(results)

    final_result = ""

    for sync in synclist:
        #print(sync)
        actual_voters, most_freq_length = find_voters_with_most_frequent_legth(sync, voters)

        if len(actual_voters) == 1:
            final_result += voters[actual_voters[0]][1][sync.start(actual_voters[0]):sync.stop(actual_voters[0]) + 1]
        else:
            for i in range(most_freq_length):
                sum = {}

                for idx, voter in enumerate(actual_voters):
                    new_llocs = voters[voter][2][sync.start(idx) + i:sync.start(idx) + i + 1]
                    all += 1

                    if len(new_llocs) == 0:
                        continue
                    add_llocs(sum, new_llocs[0])

                if len(sum) > 0:
                    final_result += get_most_likely_char(sum)
                else:
                    skipped += 1

    return final_result


def process_dir(fold_dirs, ocr):
    global all
    global skipped

    print(ocr)
    results = []

    first_result = init_ocr_result(fold_dirs[0], ocr)

    if (first_result != None):
        results.append(first_result)

        for f in fold_dirs[1:]:
            result = init_ocr_result(f, ocr)

            if (result != None):
                results.append(result)

    # TODO
    if len(results) > 2:
        final_result = perform_conf_vote(results)
        re.sub("\s+", " ", final_result)

        return final_result
    else:
        print("Fail...")


for dir in input_dirs:
    fold_dirs = []

    for fold_dir in os.listdir(dir):
        fold_dir = os.path.join(dir, fold_dir)

        if os.path.isdir(fold_dir) and not fold_dir.endswith("Voted"):
            fold_dirs.append(fold_dir)

    output_folder = os.path.join(dir, "Voted")

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    ocr_outputs = [txt for txt in os.listdir(fold_dirs[0])
                   if txt.endswith(".txt") and not txt.endswith(".gt.txt")]

    for ocr in ocr_outputs:
        final_result = process_dir(fold_dirs, ocr)

        if final_result != None:
            text_file = open(os.path.join(dir, "Voted", ocr), "w")
            text_file.write(final_result)
            text_file.close()

print("Skipped/Processed: %s/%s" % (skipped, all))