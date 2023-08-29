# Repository for materials of the HAI Diversity Paper 

We collect argumentative essays from users who write with and without model help using the [CoAuthor](https://coauthor.stanford.edu/) interface. We then formulate metrics to measure if writers produce more similar essays, reducing the diversity at the corpus level. 

## Raw Essay Logs
The CoAuthor interface allows us to record each keystroke of the writing process which allows us to replay each session for subsequent study. The raw logs from the essays collected are present in the directory raw\_logs/.<br/>
Each of these log files is a jsonl which can be consumed by read\_single\_file.py which contains a function to return a dictionary containing the essay text, summary statistics such as the number of model suggestions and model-written fraction of the essay, as well as a mask which maps each character in the essay to the author being either 'U' for user or 'A' for the model. We use these for subsequent analysis. Please note that the raw logs include _all_ essays which were collected including some pilot experiments which did not make it into the final controlled experiment.  

```
python3 read_single_file.py <path to jsonl>
``` 
