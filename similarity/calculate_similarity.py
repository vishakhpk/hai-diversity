from evaluate import load
import sys
import pickle

bertscore = load("bertscore")
rouge = load("rouge")
# bleurt = load("bleurt", module_type="metric")
bleu = load("bleu")

obj = pickle.load(open(sys.argv[1], "rb"))

predictions = [item[0] for item in obj]
references = [item[1] for item in obj]

bs_results = bertscore.compute(predictions=predictions, references=references, lang="en", model_type="microsoft/deberta-base-mnli", batch_size = 64)
pickle.dump(bs_results, open("bs_"+sys.argv[1], "wb"))
print("Finished bertscore")
rouge_results = rouge.compute(predictions=predictions, references=references, use_aggregator=False)
pickle.dump(rouge_results, open("rouge_"+sys.argv[1], "wb"))
print("Finished rouge")
#bleurt_results = bleurt.compute(predictions=predictions, references=references, checkpoint="BLEURT-20")
#pickle.dump(bleurt_results, open("bleurt_"+sys.argv[1], "wb"))
bleu_results = {}
bleu_results['bleu'] = []
for i in range(len(predictions)):
    try:
        bleu_score = bleu.compute(predictions=[predictions[i]], references=[references[i]])
        bleu_results['bleu'].append(bleu_score['bleu'])
    except:
        print("Failed at ", i)
pickle.dump(bleu_results, open("bleu_"+sys.argv[1], "wb"))
