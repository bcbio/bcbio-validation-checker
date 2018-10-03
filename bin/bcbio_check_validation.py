#!/use/bin/env python
"""Check validations outputs, ensuring that outputs match expected.

Ensures consistency between bcbio runs against reference materials,
ensuring outputs are within range of tolerance.
"""
import csv
import json
import sys

def main(base_output, *cur_outputs):
    # use first grading summary when scattered analysis, could be smarter about picking
    # if we have some logic about what to use with multiple
    cur_output = cur_outputs[0]
    threshold = 0.0025  # 0.25% different relative to initial output
    base_vals = _validation_to_vals(base_output)
    cur_vals = _validation_to_vals(cur_output)
    allowed = _get_allowed_differences(base_vals, threshold)
    results = {"Steps": {}}
    details = []
    for k, base_v in base_vals.items():
        if base_v > 0:
            cur_v = cur_vals.get(k, 0)
            k_allowed = allowed[tuple(k[:3])]
            diff = abs(cur_v - base_v)
            result = diff < k_allowed
            results["Steps"]["_".join(list(k))] = result
            details.append(list(k) + [base_v, cur_v, diff, k_allowed, result])
    results["Overall"] = all(results["Steps"].values())

    with open("results.json", "w") as out_handle:
        json.dump(results, out_handle, indent=4)
    with open("log.txt", "w") as out_handle:
        writer = csv.writer(out_handle, dialect="excel-tab")
        writer.writerow(["sample", "caller", "vartype", "metric", "expected",
                         "found", "diff", "allowed_diff", "passes"])
        for d in details:
            writer.writerow(d)

def _get_allowed_differences(vals, threshold):
    """Retrieve allowed number of changes relative to TP counts.
    """
    allowed = {}
    for (sample, caller, vartype, metric), count in vals.items():
        if metric == "tp":
            allowed[(sample, caller, vartype)] = int(count * threshold)
    return allowed

def _validation_to_vals(val_output):
    out = {}
    with open(val_output) as in_handle:
        reader = csv.reader(in_handle)
        header = reader.next()
        for val in (dict(zip(header, xs)) for xs in reader):
            curkey = (val["sample"], val["caller"], val["vtype"], val["metric"])
            out[curkey] = int(val["value"])
    return out

if __name__ == "__main__":
    if len(sys.argv[1:]) < 2:
        print("Incorrect arguments, expect at least two inputs")
        print("Usage:")
        print("  bcbio_check_validations.py truth.csv tocheck.csv")
        sys.exit()
    main(*sys.argv[1:])
