## Steps to calculate pairwise similarity scores

1. Create a pickle file consisting of a list of all pairs of summaries of the essays. This file consumes the three JSONL files for each of the essay setups with summaries and outputs a pickled list of summary pairs, keypoint\_pairs.pkl. 
```
python3 create_lists.py
```

2. Calculate the similarity between each of the pairs in keypoint\_pairs.pkl and store these in separate pickle files.
```
python3 calculate_similarity.py keypoint_pairs.pkl
```
