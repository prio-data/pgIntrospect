import fire
import os   
import re
import csv  
from collections import namedtuple

VsRow = namedtuple("VariableSheetRow", "genfunction group variable_name download_link ready hash in_bibtex")


def defns(repodir,out="./authorative_variable_names.csv"):
    lines = []
    for fname in os.listdir(os.path.join(repodir,"R")):
        if not ".R" in fname:
            continue
        pth = os.path.join(repodir,"R",fname)
        with open(pth) as f:
            lines += f.readlines()
        
        pt = "^gen_[a-z]+ ?<- ?function\(input_folder\)"
        defnlines = [fnln[0] for fnln in [re.search(pt,ln) for ln in lines] if fnln]

    rows = []
    for ln in defnlines:
        rows.append({
            "genfunction": re.search("^[^ ]+(?= )",ln)[0],
            "group": "",
            "variable_name": re.search("(?<=_)[a-z]+(?= )",ln)[0],
            "download_link": "",
            "ready": "T",
            "hash": "",
            "in_bibtex": "",
        })
        

    with open(out,"w") as f:
        wr = csv.DictWriter(f,fieldnames=rows[0].keys())
        wr.writeheader()
        wr.writerows(rows)

if __name__ == "__main__":
    fire.Fire(defns)
