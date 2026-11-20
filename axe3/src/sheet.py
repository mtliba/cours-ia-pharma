import sys, glob
from PIL import Image
n = sys.argv[1]; sel = sys.argv[2:] 
fs = sorted(glob.glob(f"../test/{n}/s*.png"))
if sel: fs = [f for f in fs if any(f.endswith(f"s{int(x):02d}.png") for x in sel)]
cols = 3 if len(fs) > 4 else 2; w = 960 if cols == 2 else 640; h = w * 9 // 16
rows = (len(fs) + cols - 1) // cols
im = Image.new("RGB", (cols * w + (cols + 1) * 6, rows * h + (rows + 1) * 6), "#444")
for i, f in enumerate(fs):
    t = Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS)
    im.paste(t, (6 + (i % cols) * (w + 6), 6 + (i // cols) * (h + 6)))
out = f"../test/{n}_sheet{'_' + '_'.join(sel) if sel else ''}.png"; im.save(out); print(out)
