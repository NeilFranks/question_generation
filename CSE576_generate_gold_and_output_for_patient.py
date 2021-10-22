import random
import csv
from pipelines import pipeline

# load the trained patient model
nlp = pipeline("e2e-qg", model="t5-patient")

# Gather every gold sentence for each symptom, from train and test .tsv files
gold_dict = {}

with open('data/patient/patient_test.tsv', encoding="utf-8") as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)  # skip first line, which is just the name of the columns
    for row in reader:
        symptom = row[0]
        gold_sentence = row[1]
        if symptom in gold_dict.keys():
            gold_dict[symptom].append(gold_sentence)
        else:
            gold_dict[symptom] = [gold_sentence]

print("%s symptoms" % len(gold_dict.keys()))

# generate a .tsv file associating one symptom to one gold sentence
with open("CSE576_gold_and_generated_for_patient.tsv", 'w', encoding="utf-8") as f:
    f.write("symptoms\tgold sentences\tgenerated sentences\n")
    for symptom in gold_dict.keys():
        gold_sentence = random.choice(gold_dict[symptom])
        if gold_sentence.strip == "":
            raise Exception("empty")

        generated_sentences = nlp(symptom)
        if len(generated_sentences) > 1:
            raise Exception("length")

        generated_sentence = generated_sentences[0]
        if generated_sentence.strip == "":
            raise Exception("empty")

        f.write("%s\t%s\t%s\n" % (symptom, gold_sentence, generated_sentence))
