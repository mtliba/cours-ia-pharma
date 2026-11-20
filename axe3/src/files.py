import sys, os, json
n = sys.argv[1]; root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", n)
fs = [{"as": "project/deck.json", "path": f"{root}/project/deck.json"}, {"as": "project/deck.css", "path": f"{root}/project/deck.css"}]
for f in sorted(os.listdir(f"{root}/project/slides")):
    fs.append({"as": f"project/slides/{f}", "path": f"{root}/project/slides/{f}"})
print(json.dumps(fs))
