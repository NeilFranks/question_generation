from pipelines import pipeline

# load the trained doctor model
nlp = pipeline("e2e-qg", model="t5-doctor")

# read in the list of every symptom in the dataset
raw_symptoms = []
with open("CSE576_all_symptoms.txt", 'r') as f:
    symptoms = f.readlines()

# remove newline symbol from all symptoms
symptoms = [symptom.rstrip('\n') for symptom in symptoms]

# generate a sentence for each symptom; write results to a .tsv file
with open("CSE576_doctor_all_outputs.tsv", 'w', encoding="utf-8") as f:
    f.write("symptoms\tsentences\n")
    for symptom in symptoms:
        sentences = nlp(symptom)
        if len(sentences) > 1:
            raise Exception("length")

        sentence = sentences[0]
        if sentence.strip == "":
            raise Exception("empty")

        f.write("%s\t%s\n" % (symptom, sentence))
