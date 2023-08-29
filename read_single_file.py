import os
import json
import sys

def find_writing_sessions(dataset_dir):
    paths = [
        os.path.join(dataset_dir, path)
        for path in os.listdir(dataset_dir) 
        if path.endswith('jsonl') and fname in path
    ]
    return paths


def read_writing_session(path):
    events = []
    with open(path, 'r') as f:
        for event in f:
            events.append(json.loads(event))
    return events

def apply_ops(doc, mask, ops, source):
    original_doc = doc
    original_mask = mask

    new_doc = ''
    new_mask = ''
    for i, op in enumerate(ops):

        # Handle retain operation
        if 'retain' in op:
            num_char = op['retain']

            retain_doc = original_doc[:num_char]
            retain_mask = original_mask[:num_char]

            original_doc = original_doc[num_char:]
            original_mask = original_mask[num_char:]

            new_doc = new_doc + retain_doc
            new_mask = new_mask + retain_mask

        # Handle insert operation
        elif 'insert' in op:
            insert_doc = op['insert']

            insert_mask = 'U' * len(insert_doc)  # User
            if source == 'api':
                insert_mask = 'A' * len(insert_doc)  # API

            if isinstance(insert_doc, dict):
                if 'image' in insert_doc:
                    print('Skipping invalid object insertion (image)')
                else:
                    print('Ignore invalid insertions:', op)
                    # Ignore other invalid insertions
                    # Debug if necessary
                    pass
            else:
                new_doc = new_doc + insert_doc
                new_mask = new_mask + insert_mask

        # Handle delete operation
        elif 'delete' in op:
            num_char = op['delete']

            if original_doc:
                original_doc = original_doc[num_char:]
                original_mask = original_mask[num_char:]
            else:
                new_doc = new_doc[:-num_char]
                new_mask = new_mask[:-num_char]

        else:
            # Ignore other operations
            # Debug if necessary
            print('Ignore other operations:', op)
            pass

    final_doc = new_doc + original_doc
    final_mask = new_mask + original_mask
    return final_doc, final_mask

def get_text_and_mask(events, event_id, remove_prompt=True):
    prompt = events[0]['currentDoc'].strip()
    # print("Prompt: ", prompt)

    text = prompt
    mask = 'P' * len(prompt)  # Prompt
    for event in events[:event_id]:
        if 'ops' not in event['textDelta']:
            continue
        ops = event['textDelta']['ops']
        source = event['eventSource']
        text, mask = apply_ops(text, mask, ops, source)

    if remove_prompt:
        if 'P' not in mask:
            print('=' * 80)
            print('Could not find the prompt in the final text')
            print('-' * 80)
            print('Prompt:', prompt)
            print('-' * 80)
            print('Final text:', text)
        else:
            end_index = mask.rindex('P')
            text = text[end_index + 1:]
            mask = mask[end_index + 1:]

    return text, mask

def read_file(path, display=True):
    events =  read_writing_session(path)
    i = len(events) - 1
    text, mask = get_text_and_mask(events, i, remove_prompt=False)
    essay = text.split("\n---\n")[-1]
    prompt = text.split("\n---\n")[0]
    split_idx = len(prompt)
    if display:
        print("Path: ", path)
        print('Text:', len(text), text) 
        print('Mask:', len(mask), mask) 
        print(prompt)
        print(essay)
        print("Count of words: ", len(essay.split()))
    query_total, selected_total = 0, 0
    for event in events:
        if event['eventName'] == "suggestion-get":
            query_total += 1
        if event['eventName'] == "suggestion-select":
            selected_total += 1
    if display:
        print("Total Suggestions: ", query_total)
        print("Total Accepted Suggestions: ", selected_total)
        try:
            print("Accepted Fraction: ", selected_total/query_total)
        except:
            pass
    ai_char_count = mask[split_idx:].count("A")
    h_char_count = mask[split_idx:].count("U")
    if display:
        print(len(text), len(prompt), len(essay), ai_char_count, h_char_count)
        print("AI Written Fraction: ", ai_char_count/len(essay))
        print("User Written Fraction: ", h_char_count/len(essay))
    try:
        acceptance_rate = selected_total/query_total
    except:
        acceptance_rate = 0
    try:
        ai_fraction = ai_char_count/len(essay)
    except:
        ai_fraction = 0
    return {'prompt':prompt, 'essay':essay, 'word_count':len(essay.split()), 'total_queries':query_total, 'total_accepted':selected_total, 'acceptance_rate':acceptance_rate, 'ai_char_count': ai_char_count, 'user_char_count':h_char_count, 'ai_fraction':ai_fraction, 'mask':mask, 'all_text':text}


if __name__ == "__main__":

    path = sys.argv[1]
    print("Reading logs from file: ", path)
    read_file(path, True)
    exit(0)

    essays = []
    events =  read_writing_session(path)
    i = len(events) - 1
    text, mask = get_text_and_mask(events, i, remove_prompt=False)
    essay = text.split("\n---\n")[-1]
    prompt = text.split("\n---\n")[0]
    split_idx = len(prompt)
    print("Path: ", path)
    print('Text:', len(text), text) 
    print('Mask:', len(mask), mask) 
    print(prompt)
    print(essay)
    print("Count of words: ", len(essay.split()))
    query_total, selected_total = 0, 0
    for event in events:
        if event['eventName'] == "suggestion-get":
            query_total += 1
        if event['eventName'] == "suggestion-select":
            selected_total += 1
    print("Total Suggestions: ", query_total)
    print("Total Accepted Suggestions: ", selected_total)
    print("Accepted Fraction: ", selected_total/query_total)
    ai_char_count = mask[split_idx:].count("A")
    h_char_count = mask[split_idx:].count("U")
    print(len(text), len(prompt), len(essay), ai_char_count, h_char_count)
    print("AI Written Fraction: ", ai_char_count/len(essay))
    print("User Written Fraction: ", h_char_count/len(essay))
