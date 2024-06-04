from os import listdir
import re
import json

results = { "meta" : {}, "data" : [] }
for f in listdir('reward/'):
    item = {}
    item["path_to"] = f'reward/%s' % f
    title = re.sub(r'\.[a-z]*', '', f)
    title = title.replace("_plus", "+")
    title = title.replace("_minus", "-")
    title = title.replace("_", " ")
    item["title"] = title

    for i in range(3):
        results["data"].append(item)


with open('rewards.json', 'w') as f:
    json.dump(results, f, indent=2)
