import csv

"""
Certain sentences appear multiple times in the data
We should de-dup these entries. 
"""


def dedup_entries(path_to_file):
    entries = {}
    sentences = set([])
    with open(path_to_file, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)  # skip first line, which is just the name of the columns
        for row in reader:
            symptom = row[0]
            sentence = row[1]
            if sentence not in sentences:
                sentences.add(sentence)
                if symptom in entries.keys():
                    entries[symptom].add(sentence)
                else:
                    entries[symptom] = set([sentence])

    with open(path_to_file, "w", encoding="utf-8") as f:
        f.write("symptoms\tsentences\n")
        for symptom in entries.keys():
            for sentence in list(entries[symptom]):
                f.write("%s\t%s\n" % (symptom, sentence))


dedup_entries("data\doctor\doctor_train.tsv")
dedup_entries("data\doctor\doctor_test.tsv")
dedup_entries("data\patient\patient_train.tsv")
dedup_entries("data\patient\patient_test.tsv")
