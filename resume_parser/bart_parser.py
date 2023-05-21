from transformers import BartConfig, BartTokenizer, BartForConditionalGeneration
import json
import re

class BartParser:
    def __init__(self, model_path):
        self.tokenizer = BartTokenizer.from_pretrained(model_path, local_files_only=True)
        self.config = BartConfig.from_pretrained(model_path, local_files_only=True)
        self.model = BartForConditionalGeneration.from_pretrained(model_path, local_files_only=True, config=self.config)
        self.section_keys = ['personal_details', 'professional_summary', 'employment_history', 'education', 'skills']
        print("[BART Parser] Resume parser model loaded..")
    
    def parse(self, raw_text):
        input_ids = self.tokenizer(raw_text, return_tensors="pt").input_ids
        output_ids = self.model.generate(input_ids, min_length=100, max_new_tokens=1000)
        raw_json = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        json_data, sections = self.fix(raw_json)
        output = self.convert(json_data, sections)
        return output
    
    def fix(self, raw_json):
        raw_json = re.sub(r'\n', '', raw_json)
        raw_json = re.sub(r'\" +| +\"', '\"', raw_json)
        remaining_sections = self.section_keys
        while raw_json != "" and len(remaining_sections) != 0:
            try:
                json_data = json.loads(raw_json)
                return json_data, remaining_sections
            except:
                last_section = remaining_sections[-1]
                remaining_sections = remaining_sections[:-1]
                last_section_index = raw_json.find(last_section)
                if last_section_index == -1:
                    continue
                raw_json = raw_json[:last_section_index]
                last_comma_index = raw_json.rfind(',')
                if last_comma_index == -1:
                    continue
                raw_json = raw_json[:last_comma_index]
                raw_json += '}'


        return "", []
    
    def convert(self, json_data, sections):
        result = {}
        all_keys = json_data.keys()
        if 'employment_history' in all_keys or 'education' in all_keys or 'skills' in all_keys:
            result['complex_sections'] = {}
        for section in sections:
            sub_json_data = json_data[section]
            if section == 'personal_details':
                result['personal_details'] = self.convert_personal_details(sub_json_data)
            elif section == 'professional_summary':
                result['professional_summary'] = self.convert_professional_summary(sub_json_data)
            elif section == 'employment_history':
                result['complex_sections'][len(result['complex_sections'])] = self.convert_employment_history(sub_json_data)
            elif section == 'education':
                result['complex_sections'][len(result['complex_sections'])] = self.convert_education(sub_json_data)
            elif section == 'skills':
                result['complex_sections'][len(result['complex_sections'])] = self.convert_skills(sub_json_data)    

        return result
    
    def convert_personal_details(self, json_data):
        all_keys = json_data.keys()
        result = {}
        result['header'] = 'Personal Details'
        result['position'] = 1
        if 'first_name' in all_keys:
            result['first_name'] = json_data['first_name']
        if 'last_name' in all_keys:
            result['last_name'] = json_data['last_name']
        if 'job_title' in all_keys:
            result['job_title'] = json_data['job_title']
        if 'address' in all_keys:
            result['address'] = json_data['address']
        if 'email' in all_keys:
            result['email'] = json_data['email']
        # if 'phone' in all_keys:
        #     result['phone'] = json_data['phone']
        return result

    def convert_professional_summary(self, json_data):
        result = {}
        result['header'] = 'Professional Summary'
        result['position'] = 2
        result['content'] = json_data
        return result

    def convert_employment_history(self, json_data):
        result = {}
        result['header'] = 'Employment History'
        result['position'] = 3
        result['section_type'] = 'employment_histories'
        result['employment_histories'] = {}
        for i, sub_json_data in enumerate(json_data):
            sub_result = {}
            all_keys = sub_json_data.keys()
            sub_result['position'] = i + 1
            if 'job_title' in all_keys:
                sub_result['job_title'] = sub_json_data['job_title']
            if 'employer' in all_keys:
                sub_result['employer'] = sub_json_data['employer']
            # if 'start_date' in all_keys:
            #     sub_result['start_date'] = sub_json_data['start_date']
            # if 'end_date' in all_keys:
            #     sub_result['end_date'] = sub_json_data['end_date']
            if 'description' in all_keys:
                sub_result['description'] = sub_json_data['description']
            result['employment_histories'][i] = sub_result
        return result
    
    def convert_education(self, json_data):
        result = {}
        result['header'] = 'Education'
        result['position'] = 4
        result['section_type'] = 'educations'
        result['educations'] = {}
        for i, sub_json_data in enumerate(json_data):
            sub_result = {}
            all_keys = sub_json_data.keys()
            sub_result['position'] = i + 1
            if 'school' in all_keys:
                sub_result['school'] = sub_json_data['school']
            if 'degree' in all_keys:
                sub_result['degree'] = sub_json_data['degree']
            # if 'start_date' in all_keys:
            #     sub_result['start_date'] = sub_json_data['start_date']
            # if 'end_date' in all_keys:
            #     sub_result['end_date'] = sub_json_data['end_date']
            if 'description' in all_keys:
                sub_result['description'] = sub_json_data['description']
            result['educations'][i] = sub_result
        return result
    
    def convert_skills(self, json_data):
        result = {}
        result['header'] = 'Skill'
        result['position'] = 5
        result['section_type'] = 'skills'
        result['skills'] = {}
        for i, sub_json_data in enumerate(json_data):
            sub_result = {}
            sub_result['position'] = i + 1
            sub_result['name'] = sub_json_data
            sub_result['level'] = 'beginner'
            result['skills'][i] = sub_result
        return result

