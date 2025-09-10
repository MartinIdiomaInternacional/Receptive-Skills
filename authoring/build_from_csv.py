
import csv, json, sys, os
from pathlib import Path

# Usage: python build_from_csv.py <authoring_dir> <content_dir_root>
# Example: python build_from_csv.py ./authoring ./content

LEVELS = ["A1","A2","B1","B1+","B2","B2+","C1","C2"]

def ensure_dirs(root):
    for sec in ["grammar","listening","reading"]:
        Path(root, sec).mkdir(parents=True, exist_ok=True)

def irt_block(a,b,c):
    return {"model":"3PL","a":float(a or 1.0),"b":float(b or 0.0),"c":float(c or 0.2)}

def write_json(paths, data_by_level):
    for lvl, items in data_by_level.items():
        outp = Path(paths[lvl])
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

def build_grammar(csv_path, out_root):
    by_level = {lvl: [] for lvl in LEVELS}
    with open(csv_path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(row for row in f if not row.startswith('#'))
        for row in r:
            if row.get("section","").strip() != "grammar": continue
            lvl = row["level"].strip()
            if lvl not in by_level: continue
            tags = [t.strip() for t in (row.get("tags","") or "").split(";") if t.strip()]
            item = {
                "id": row["id"].strip(),
                "type": row.get("type","mcq").strip(),
                "prompt": row["prompt"].strip(),
                "options": [row.get("option_0",""),row.get("option_1",""),row.get("option_2",""),row.get("option_3","")],
                "answer_index": int(row["answer_index"]),
                "rationale": row.get("rationale",""),
                "irt": irt_block(row.get("irt_a","1.0"), row.get("irt_b","0.0"), row.get("irt_c","0.2")),
                "tags": tags
            }
            if row.get("anchor","").lower()=="true": item["anchor"]=True
            if row.get("pretest","").lower()=="true": item["pretest"]=True
            by_level[lvl].append(item)
    paths = {lvl: Path(out_root, "grammar", f"{lvl}.json") for lvl in LEVELS}
    write_json(paths, by_level)

def build_listening(csv_path, out_root):
    by_level = {lvl: [] for lvl in LEVELS}
    carry = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(row for row in f if not row.startswith('#'))
        for row in r:
            if row.get("section","").strip() != "listening": continue
            lvl = row["level"].strip()
            if lvl not in by_level: continue
            tid = row["testlet_id"].strip()
            if tid not in carry:
                carry[tid] = {
                    "testlet_id": tid,
                    "audio_url": row["audio_url"].strip(),
                    "items": [],
                    "tags": []
                }
                if row.get("anchor","").lower()=="true": carry[tid]["anchor"]=True
                if row.get("pretest","").lower()=="true": carry[tid]["pretest"]=True
            tags = [t.strip() for t in (row.get("tags","") or "").split(";") if t.strip()]
            carry[tid]["tags"] = list(sorted(set(carry[tid]["tags"]+tags)))
            item = {
                "id": row["id"].strip(),
                "type": row.get("type","mcq").strip(),
                "prompt": row["prompt"].strip(),
                "options": [row.get("option_0",""),row.get("option_1",""),row.get("option_2",""),row.get("option_3","")],
                "answer_index": int(row["answer_index"]),
                "rationale": row.get("rationale",""),
                "irt": irt_block(row.get("irt_a","1.0"), row.get("irt_b","0.0"), row.get("irt_c","0.2")),
                "tags": tags
            }
            carry[tid]["items"].append(item)
            # assign to level
            by_level[lvl].append(carry[tid])
    paths = {lvl: Path(out_root, "listening", f"{lvl}.json") for lvl in LEVELS}
    write_json(paths, by_level)

def build_reading(csv_path, out_root):
    by_level = {lvl: [] for lvl in LEVELS}
    carry = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(row for row in f if not row.startswith('#'))
        for row in r:
            if row.get("section","").strip() != "reading": continue
            lvl = row["level"].strip()
            if lvl not in by_level: continue
            tid = row["testlet_id"].strip()
            if tid not in carry:
                carry[tid] = {
                    "testlet_id": tid,
                    "passage": row["passage"].strip(),
                    "items": [],
                    "tags": []
                }
                if row.get("anchor","").lower()=="true": carry[tid]["anchor"]=True
                if row.get("pretest","").lower()=="true": carry[tid]["pretest"]=True
            tags = [t.strip() for t in (row.get("tags","") or "").split(";") if t.strip()]
            carry[tid]["tags"] = list(sorted(set(carry[tid]["tags"]+tags)))
            item = {
                "id": row["id"].strip(),
                "type": row.get("type","mcq").strip(),
                "prompt": row["prompt"].strip(),
                "options": [row.get("option_0",""),row.get("option_1",""),row.get("option_2",""),row.get("option_3","")],
                "answer_index": int(row["answer_index"]),
                "rationale": row.get("rationale",""),
                "irt": irt_block(row.get("irt_a","1.0"), row.get("irt_b","0.0"), row.get("irt_c","0.2")),
                "tags": tags
            }
            carry[tid]["items"].append(item)
            by_level[lvl].append(carry[tid])
    paths = {lvl: Path(out_root, "reading", f"{lvl}.json") for lvl in LEVELS}
    write_json(paths, by_level)

def main():
    if len(sys.argv) < 3:
        print("Usage: python build_from_csv.py <authoring_dir> <content_dir_root>")
        sys.exit(1)
    author = Path(sys.argv[1])
    outroot = Path(sys.argv[2])
    ensure_dirs(outroot)
    build_grammar(author / "grammar.csv", outroot)
    build_listening(author / "listening.csv", outroot)
    build_reading(author / "reading.csv", outroot)
    print("Built JSON banks to:", outroot)

if __name__ == "__main__":
    main()
