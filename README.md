# Repository for materials of the HAI Diversity Paper 

We collect argumentative essays from users who write with and without model help using the [CoAuthor](https://coauthor.stanford.edu/) interface. We then formulate metrics to measure if writers produce more similar essays, reducing the diversity at the corpus level. 

## Raw Essay Logs
The CoAuthor interface allows us to record each keystroke of the writing process which allows us to replay each session for subsequent study. The raw logs from the essays collected are present in the directory logs/pilot/. These log files can be used to replay the writing session via CoAuthor. <br/>

Each of these log files is a jsonl which can be consumed by read\_single\_file.py which contains a function to return a dictionary containing the essay text, summary statistics such as the number of model suggestions and model-written fraction of the essay, as well as a mask which maps each character in the essay to the author being either 'U' for user or 'A' for the model. We use these for subsequent analysis. Please note that the raw logs include _all_ essays which were collected including some pilot experiments which did not make it into the final controlled experiment.  

```
python3 read_single_file.py <path to jsonl>
``` 

## Processed Essay Data

In the processed\_data/ folder we also link the essays from the experiment in a set of jsonl files. Each essay item can be read as a JSON and has the following keys
```
(Pdb) obj.keys()
dict_keys(['essay', 'path', 'prompt', 'title', 'summary', 'sentences', 'matched_sents', 'match_scores', 'authorship'])
```
Each key corresponds to the following:
- **essay**: Text of the essay
- **path**: Mapping to the log file indexed from the home directory of this repo
- **prompt**: Full text of the prompt given to the writers
- **title**: Short form version of the prompt given to the writers
- **summary**: Summary of the essay as obtained from GPT3.5. It is stored as a list of key points, each one sentence long. The first item in the list is sometimes an empty sentence which should be ignored. 
- **sentences**: The text of the essay broken up into individual sentences, stored as a list.
- **matched_sents**: The mapping of each key point in the summary to the closest match sentence. Also stored as a list of length equal to the length of the summary where each element of the list is the index of the match among the sentences
- **match_scores**: Rouge scores used to create the mapping
- **authorship**: The mapping of each sentence in the essay to whether it was written by the model or the user. Stored as a list of length equal to the number of sentences, each with either 'U' meaning the sentence was written in majority by the user or 'A' if the majority was by the model

