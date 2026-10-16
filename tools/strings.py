import re, glob, os
sp = os.path.dirname(os.path.abspath(__file__))
pat = re.compile(r'"((?:[^"\\\n]|\\.){3,}?)"|`((?:[^`\\]|\\.){3,}?)`')
out = []
files = [os.path.join(sp, "main.js")] + sorted(glob.glob(os.path.join(sp, "chunks", "*.js")))
for f in files:
    if "index-DNarD217" in f:
        continue
    s = open(f, encoding="utf8").read()
    keep = []
    for a, b in pat.findall(s):
        t = a or b
        if re.search(r'[A-Za-z]{3,}[ ,.][A-Za-z]{2,}', t) and not re.fullmatch(r'[a-z0-9\-\[\]:/ .%()#,&>~_!=*+@]+', t):
            keep.append(t)
    out.append("\n######## " + os.path.basename(f) + "\n" + "\n".join(dict.fromkeys(keep)))
open(os.path.join(sp, "strings.txt"), "w", encoding="utf8").write("\n".join(out))
