#!/use/bin/env python
"""Check validations outputs, ensuring that outputs match expected.

Ensures consistency between bcbio runs against reference materials,
ensuring outputs are within range of tolerance.
"""
import csv
import json
import sys

def main(base_output, cur_output):
    threshold = 0.05  # 5% different relative to initial output
    base_vals = _validation_to_vals(base_output)
    cur_vals = _validation_to_vals(cur_output)
    results = {"Steps": {}}
    for k, base_v in base_vals.items():
        if base_v > 0:
            cur_v = cur_vals.get(k, 0)
            change = float(cur_v) / float(base_v)
            result = change > (1.0 - threshold) and change < (1.0 + threshold)
            results["Steps"]["_".join(list(k))] = result
    results["Overall"] = all(results["Steps"].values())

    with open("results.json", "w") as out_handle:
        json.dump(results, out_handle, indent=4)

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
    main(*sys.argv[1:])
