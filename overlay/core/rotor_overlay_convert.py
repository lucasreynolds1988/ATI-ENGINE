import os
import csv
import json

def csv_to_txt(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    in_path = os.path.join(overlay, filename)
    out_path = os.path.join(overlay, filename.rsplit('.',1)[0] + ".txt")
    with open(in_path, "r") as csvfile, open(out_path, "w") as txtfile:
        reader = csv.reader(csvfile)
        for row in reader:
            txtfile.write("\t".join(row) + "\n")
    print(f"Converted {filename} to TXT: {os.path.basename(out_path)}")

def txt_to_csv(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    in_path = os.path.join(overlay, filename)
    out_path = os.path.join(overlay, filename.rsplit('.',1)[0] + ".csv")
    with open(in_path, "r") as txtfile, open(out_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for line in txtfile:
            writer.writerow(line.rstrip("\n").split("\t"))
    print(f"Converted {filename} to CSV: {os.path.basename(out_path)}")

def json_to_txt(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    in_path = os.path.join(overlay, filename)
    out_path = os.path.join(overlay, filename.rsplit('.',1)[0] + ".txt")
    with open(in_path, "r") as jsonfile, open(out_path, "w") as txtfile:
        data = json.load(jsonfile)
        if isinstance(data, dict):
            for k, v in data.items():
                txtfile.write(f"{k}: {v}\n")
        elif isinstance(data, list):
            for item in data:
                txtfile.write(str(item) + "\n")
    print(f"Converted {filename} to TXT: {os.path.basename(out_path)}")

def txt_to_json(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    in_path = os.path.join(overlay, filename)
    out_path = os.path.join(overlay, filename.rsplit('.',1)[0] + ".json")
    with open(in_path, "r") as txtfile, open(out_path, "w") as jsonfile:
        lines = [line.rstrip("\n") for line in txtfile]
        try:
            # Try key-value: "key: value"
            obj = {}
            for line in lines:
                if ": " in line:
                    k, v = line.split(": ", 1)
                    obj[k] = v
            if obj:
                json.dump(obj, jsonfile, indent=2)
            else:
                json.dump(lines, jsonfile, indent=2)
        except:
            json.dump(lines, jsonfile, indent=2)
    print(f"Converted {filename} to JSON: {os.path.basename(out_path)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        mode, filename = sys.argv[1], sys.argv[2]
        if mode == "csv2txt":
            csv_to_txt(filename)
        elif mode == "txt2csv":
            txt_to_csv(filename)
        elif mode == "json2txt":
            json_to_txt(filename)
        elif mode == "txt2json":
            txt_to_json(filename)
        else:
            print("Modes: csv2txt | txt2csv | json2txt | txt2json")
    else:
        print("Usage: python rotor_overlay_convert.py <mode> <filename>")
