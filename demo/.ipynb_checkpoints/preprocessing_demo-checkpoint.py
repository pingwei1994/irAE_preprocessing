import sys
sys.path.append('../src')

import pandas as pd
import mention_extraction.extract_mentions as eim
import mention_extraction.drug_ici_config
import json



def preprocessing():
    config_file_json = "drug_symptom_dicts.json"
    def load_config(config_file_json):
        with open(config_file_json, 'r') as f:
            config = json.load(f)
        return config
    config = load_config(config_file_json)
    notes = pd.read_csv(f'../data/{config['ehr_file_name']}')
    drug_mentions = eim.extract_ici_mentions(notes, config['drug_dict'])
    symptom_mentions = eim.extract_symptom_mentions(notes, config['symptom_dict'])
    symptom_mentions[['report_id', 'standard_symptom', 'matched_variant',
       'start_index', 'variant_length', 'theword',
       'symptom_adjacent']].to_csv('../data/symptom_mentions.csv', index=False)
    drug_mentions[['report_id', 'standard_drug', 'matched_variant', 'start_index',
       'variant_length', 'theword', 'drug_adjacent']].to_csv('../data/drug_mentions.csv', index=False)
    drug_part = drug_mentions.groupby(['report_id', 'notes', 'standard_drug'], as_index=False).agg({'drug_adjacent':list})
    symptom_part = symptom_mentions.groupby(['report_id', 'notes', 'standard_symptom'], as_index=False).agg({'symptom_adjacent':list})
    final_data = drug_part.merge(symptom_part, on=['report_id', 'notes'], how='inner')
    final_data = final_data.merge(notes[['report_id','patient_index']], on = 'report_id', how='inner')
    final_data.to_csv('../data/final_data.csv', index=False)
        


if __name__ == "__main__":
    preprocessing()






