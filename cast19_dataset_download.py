import ir_datasets
import csv
import os
from tqdm import tqdm

dataset = ir_datasets.load("trec-cast/v1/2019")

data_path = 'datasets/cast'
os.makedirs(data_path, exist_ok=True)
os.chdir(data_path)

print(f"Current directory {os.getcwd()}")
#with open('cast19_qrel.tsv', 'w', newline='') as f:
    # Iterate over the qrels
#    writer = csv.writer(f, delimiter='\t')
#    for qrel in dataset.qrels_iter():
#        writer.writerow(list(qrel))



with open("trec_cast_2019.tsv", "w", encoding="utf-8") as file:
    # Iterate over the dataset and write each document
    for doc in tqdm(dataset.docs_iter()):
        # Replace tabs and newlines in the text to avoid formatting issues
        text_cleaned = doc.text.replace("\t", " ").replace("\n", " ")
        file.write(f"{doc.doc_id}\t{text_cleaned}\n")

print("Dataset saved to trec_cast_2019.tsv")


with open("trec_cast_2019.qrels", "w", encoding="utf-8") as file:
    # Iterate over the qrels and write them in TREC format
    # Format: <topic_id> <iteration> <doc_id> <relevance>
    for qrel in tqdm(dataset.qrels_iter()):
        file.write(f"{qrel.query_id} 0 {qrel.doc_id} {qrel.relevance}\n")

print("Qrels saved to trec_cast_2019.qrels")