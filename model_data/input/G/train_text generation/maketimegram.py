filedata = open('timestamps.txt', 'r')
timestamps = filedata.readlines()
outlines = []
# Kunnen we <timestamp> vertrekken?
for timestamp in timestamps:
    if(timestamp.strip() != ""):
        outlines.append("kunnen we "+timestamp.strip()+" vertrekken")

# Kan je nog even wachten tot <timestamp>?
for timestamp in timestamps:
    if(timestamp.strip() != ""):
        outlines.append("kan je nog even wachten tot "+timestamp.strip())

with open('timestamp_grammar.txt', mode='wt', encoding='utf-8') as myfile:
    myfile.write('\n'.join(outlines))
