import csv

"""
Patient shouldn't be asking questions, according to Mihir and Man:
    'Patients should generate sentences, but there are lots of generated questions there.'
"""


def remove_questions(path_to_file):
    entries = {}
    with open(path_to_file, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)  # skip first line, which is just the name of the columns
        for row in reader:
            symptom = row[0]
            sentence = row[1]
            if "?" not in sentence:
                if symptom in entries.keys():
                    entries[symptom].append(sentence)
                else:
                    entries[symptom] = [sentence]

    with open(path_to_file, "w", encoding="utf-8") as f:
        f.write("symptoms\tsentences\n")
        for symptom in entries.keys():
            for sentence in entries[symptom]:
                f.write("%s\t%s\n" % (symptom, sentence))


remove_questions("data\patient\patient_train.tsv")
remove_questions("data\patient\patient_test.tsv")
