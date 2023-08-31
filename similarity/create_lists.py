import json
import pickle
import random

all_kp = []
for modifier in ["solo", "instructgpt", "gpt3"]:
    # ip = []
    unique_essays = []
    with open("summaries-essays_"+modifier+".jsonl", 'r') as f:
        for line in f:
            item = json.loads(line.strip())
            try:
                these_kp = ' '.join(item['summary'])
            except:
                print("Missing summary", item)
            if item['essay'] in unique_essays:
                continue
            unique_essays.append(item['essay'])
            all_kp.append(these_kp) #random.sample(these_kp, 100)
        print(len(all_kp))

filtered_kp = []
for kp in all_kp:
    if len(kp) > 0 and kp not in filtered_kp:
        filtered_kp.append(kp)

print("After filtering: ", len(filtered_kp))
op = []
for i, kp in enumerate(filtered_kp):
    for j, other_kp in enumerate(filtered_kp):
        if j > i:
            continue
        if kp!=other_kp:
            op.append((kp, other_kp))

print("All pairs: ", len(op))
op = list(set(op))
print("Unique pairs: ", len(op))

pickle.dump(op, open("keypoint_pairs.pkl", "wb"))
