import openai
import time
import sys
import json
import copy
import os

fname = sys.argv[1]

ip = []
with open(fname, 'r') as f:
    for line in f:
        ip.append(json.loads(line.strip()))

op = []
try:
    with open("summaries-"+fname, "r") as f:
        for line in f:
            op.append(json.loads(line.strip()))
except Exception as e:
    print("No pre-existing output for this file: ", e)

openai.api_key = os.getenv("OPENAI_API_KEY")
# breakpoint()

# op = []
prompt = "Summarize this essay into a set of simple bullet points that cover all the information from the essay: "
for item in ip:
    essay = item['essay']
    f = False
    for existing_item in op:
        if existing_item['essay'] == essay:
            f = True
            break
    if f:
        print("Found essay already, skipping")
        continue
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."}, 
            {"role": "user", "content": prompt+essay}]
    )
    summary = completion['choices'][0]['message']['content'].replace("\n", " ")
    op_item = copy.deepcopy(item)
    if "-" in summary:
        op_item['summary'] = summary.split("- ")
    op.append(op_item)
    print(len(op), " now sleeping")
    # breakpoint()
    if len(op) % 10 == 0:
        with open("summaries-"+fname, "w") as f:
            for temp in op:
                f.write(json.dumps(temp)+'\n')
        time.sleep(60)

with open("summaries-"+fname, "w") as f:
    for temp in op:
        f.write(json.dumps(temp)+'\n')
