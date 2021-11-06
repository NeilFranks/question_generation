# Initial setup
Follow the instructions for installing necessary dependencies, found in this repository's main README

# Prepare the data
**You may skip this section if you are already provided a trained model and tokenizer!**

- In the `data` directory, create two new folders: `doctor` and `patient`. 
- In doctor, drop `doctor_train.tsv` and `doctor_test.tsv`. 
- In patient, drop `patient_train.tsv` and `patient_test.tsv`.
- To prepare the doctor datasets, run 

    ```bash
    python prepare_data.py --task=e2e_qg --valid_for_qg_only --model_type=t5 --dataset_path=data/doctor/ --qg_format=highlight_qg_format --max_source_length=512 --max_target_length=32 --train_file_name=doctor/doctor_train_data_e2e_qg_t5.pt --valid_file_name=doctor/doctor_valid_data_e2e_qg_t5.pt
    ```

- To prepare the patient datasets, run 

    ```bash
    python prepare_data.py --task=e2e_qg --valid_for_qg_only --model_type=t5 --dataset_path=data/patient/ --qg_format=highlight_qg_format --max_source_length=512 --max_target_length=32 --train_file_name=patient/patient_train_data_e2e_qg_t5.pt --valid_file_name=patient/patient_valid_data_e2e_qg_t5.pt
    ```

**Notably, this process will also generate a tokenizer, which you will need for training your models and generating output.**

Your file structure should now include:

```bash
├── data
│   ├── doctor
│   │   ├── doctor_test.tsv
│   │   ├── doctor_train_data_e2e_qg_t5.pt
│   │   ├── doctor_train.tsv
│   │   └── doctor_valid_data_e2e_qg_t5.pt
│   └── patient
│       ├── patient_test.tsv
│       ├── patient_train_data_e2e_qg_t5.pt
│       ├── patient_train.tsv
│       └── patient_valid_data_e2e_qg_t5.pt
├── t5_qg_tokenizer
│   ├── added_tokens.json
│   ├── special_tokens_map.json
│   ├── spiece.model
│   └── tokenizer_config.json
```

# Training
**You may skip this section if you are already provided a trained model and tokenizer!**

To train a doctor model, run `python CSE576_train_doctor.py`. The number of epochs is set to 100, but you may change the number of epochs by changing the value associated with `"num_train_epochs"` in `CSE576_train_doctor.py`.
When training is done, you should see a new directory named `t5-doctor`, with the following structure:
```bash
├── t5-doctor
│   ├── checkpoint-XXXXX
│   │   └── ...
│   ├── added_tokens.json
│   ├── config.json
│   ├── eval_results.txt
│   ├── pytorch_model.bin
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── training_args.bin
```

To train a patient model, run `python CSE576_train_patient.py`. The number of epochs is set to 100, but you may change the number of epochs by changing the value associated with `"num_train_epochs"` in `CSE576_train_patient.py`.
When training is done, you should see a new directory named `t5-patient`, with the following structure:
```bash
├── t5-patient
│   ├── checkpoint-XXXXX
│   │   └── ...
│   ├── added_tokens.json
│   ├── config.json
│   ├── eval_results.txt
│   ├── pytorch_model.bin
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── training_args.bin
```

# Using an existing model
To use an existing model, **you must also make use of a tokenizer**. 

Copy/paste the files into the directory so that the file structure includes this structure, encapsulating the necessary tokenizer, and the trained models:
```bash
├── t5_qg_tokenizer
│   ├── added_tokens.json
│   ├── special_tokens_map.json
│   ├── spiece.model
│   └── tokenizer_config.json
├── t5-doctor
│   ├── checkpoint-XXXXX
│   │   └── ...
│   ├── added_tokens.json
│   ├── config.json
│   ├── eval_results.txt
│   ├── pytorch_model.bin
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── training_args.bin
├── t5-patient
│   ├── checkpoint-XXXXX
│   │   └── ...
│   ├── added_tokens.json
│   ├── config.json
│   ├── eval_results.txt
│   ├── pytorch_model.bin
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── training_args.bin
```

# Generating output from models
After the previous steps, you should have your tokenizer and models in the correct place, and generating output should be straight-forward.

In python, you may generate output for the doctor for a symptom (e.g., `sense of hunger`) by running the simple commands:
```python
from pipelines import pipeline
nlp = pipeline("e2e-qg", model="t5-doctor")
print(nlp("sense of hunger"))
```

Similarly, for the patient:
```python
from pipelines import pipeline
nlp = pipeline("e2e-qg", model="t5-patient")
print(nlp("sense of hunger"))
```

To generate outputs for all the given combinations of symptoms, run `python CSE576_generate_gold_and_output_for_doctor.py` for the doctor, and `python CSE576_generate_gold_and_output_for_patient.py` for the patient.

These commands will generate `CSE576_gold_and_generated_for_doctor.tsv` and `CSE576_gold_and_generated_for_patient.tsv`, respectively.

These generated .tsv files can be opened in Excel, and you can view the generated output for every given symtom and combination of symptoms.