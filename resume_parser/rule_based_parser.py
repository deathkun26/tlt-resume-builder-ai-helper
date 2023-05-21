import numpy as np
import re

class RuleBasedParser:
    def parse(self, raw_text):
        result = {}
        result['complex_sections'] = {}
        text = raw_text
        text = self._remove_endline_with_space(text)
        text = self._mark_triple_endline(text, " triple_endline ")
        text = self._replace_endline(text, "\n")

        # sort by priority
        section_headers = {
            'personal_details': ['personal details', 'contacts', 'contact'],
            'professional_summary': ['about me', 'professional summary', 'summary'],
            'employment_history': ['employment history', 'work experience', 'experience work'],
            'education': ['education'],
            'skills': ['skills', 'skill', 'expertise'],
            'name': ['triple_endline'],
            'another': ['references']
        }
        personal_details_section_headers = section_headers['personal_details']
        professional_summary_section_headers = section_headers['professional_summary']
        employment_history_section_headers = section_headers['employment_history']
        education_section_headers = section_headers['education']
        skills_section_headers = section_headers['skills']
        name_section_headers = section_headers['name']
        another_section_headers = section_headers['another']

        all_header_positions = []

        personal_details_section_header_positions = self._find_header_position(text, 'personal_details', personal_details_section_headers)
        all_header_positions += personal_details_section_header_positions

        professional_summary_section_header_positions = self._find_header_position(text, 'professional_summary', professional_summary_section_headers)
        all_header_positions += professional_summary_section_header_positions

        employment_history_section_header_positions = self._find_header_position(text, 'employment_history', employment_history_section_headers)
        all_header_positions += employment_history_section_header_positions

        education_section_header_positions = self._find_header_position(text, 'education', education_section_headers)
        all_header_positions += education_section_header_positions

        skills_section_header_positions = self._find_header_position(text, 'skills', skills_section_headers)
        all_header_positions += skills_section_header_positions

        name_section_header_positions = self._find_header_position(text, 'name', name_section_headers)
        all_header_positions += name_section_header_positions

        another_section_header_positions = self._find_header_position(text, 'another', another_section_headers)
        all_header_positions += another_section_header_positions

        all_header_positions_sorted = self._sort_list_tuple(all_header_positions)

        sections = {}
        previous_start, previous_end, previous_header_type = all_header_positions_sorted[0]
        counter = 0
        for (start, end, header_type) in all_header_positions_sorted:
            if start == previous_start:
                continue
            # print(previous_header_type, ":", previous_start, " -> ", start)
            sections[counter] = (previous_header_type, (previous_start, previous_end), text[previous_start: start])
            counter += 1
            previous_start = start
            previous_end = end
            previous_header_type = header_type
        sections[counter] = (previous_header_type, (previous_start, previous_end), text[previous_start:])
        # print(previous_header_type, ":", previous_start, " -> ", len(text))
        counter += 1

        # print("\n -------------------------- \n ")
        # for i in range(counter): 
        #     print("Section", str(i)+":", sections[i][0], '->')
        #     print("Section position:", sections[i][1][0], "->", sections[i][1][1])
        #     print(sections[i][2].replace('\\n', '\n').replace('triple_endline ', ''))
        #     print("\n -------------------------- \n ")

        section_counter = {}

        for i in range(counter):
            section = sections[i]
            # print(section)
            header_type, header_position, content = section
            
            if header_type == 'name':
                parsed_content = self._parse_name_and_job(header_position, content)
                if parsed_content == "":
                    continue
                if header_type in section_counter.keys():
                    continue
                name_split = parsed_content['name'].split(' ')
                result['personal_details'] = {
                    'position': 1,
                    'last_name': ' '.join(name_split[1:]),
                    'first_name': name_split[0],
                    'job_title': parsed_content['job']
                }
            elif header_type == 'professional_summary':
                parsed_content = self._parse_summary(header_position, content) 
                if parsed_content == "":
                    continue
                if header_type in section_counter.keys():
                    continue
                result['professional_summary'] = {
                    'position': 2,
                    'header': 'Professional Summary',
                    'content': parsed_content
                }
            elif header_type == 'employment_history':
                parsed_content = self._parse_employment(header_position, content) 
                if parsed_content == "":
                    continue
                if header_type in section_counter.keys():
                    for i in result['complex_sections'].keys():
                        if result['complex_sections'][i]['section_type'] == 'employment_histories':
                            current_len = len(result['complex_sections'][i]['employment_histories'])
                            result['complex_sections'][i]['employment_histories'][current_len] = {
                                "position": current_len + 1,
                                "description": parsed_content,
                            }
                            break
                else:
                    result['complex_sections'][len(result['complex_sections'])] = {
                        "position": 3,
                        "header": "Employment History",
                        "section_type": "employment_histories",
                        "employment_histories": {
                            0: {
                                "position": 1,
                                "description": parsed_content,
                            }
                        },
                    }
            elif header_type == 'education':
                parsed_content = self._parse_education(header_position, content) 
                if parsed_content == "":
                    continue
                if header_type in section_counter.keys():
                    for i in result['complex_sections'].keys():
                        if result['complex_sections'][i]['section_type'] == 'educations':
                            current_len = len(result['complex_sections'][i]['educations'])
                            result['complex_sections'][i]['educations'][current_len] = {
                                "position": current_len + 1,
                                "description": parsed_content,
                            }
                            break
                else:
                    result['complex_sections'][len(result['complex_sections'])] = {
                        "position": 4,
                        "header": "Education",
                        "section_type": "educations",
                        "educations": {
                            0: {
                                "position": 1,
                                "description": parsed_content,
                            }
                        },
                    }
            elif header_type == 'skills':
                parsed_content = self._parse_skills(header_position, content)
                if parsed_content == "":
                    continue
                if header_type in section_counter.keys():
                    continue
                skills = {}
                for i, skill in enumerate(parsed_content):
                    skills[i] = {
                        'position': i + 1,
                        'name': skill,
                        'level': 'beginner'
                    }
                result['complex_sections'][len(result['complex_sections'])] = {
                    "position": 5,
                    "header": "Skill",
                    "section_type": "skills",
                    "skills": skills,
                }
            elif header_type == 'personal_details':
                parsed_content = ""
            else:
                parsed_content = ""
            
            if header_type in section_counter.keys():
                section_counter[header_type] += 1
            else: 
                section_counter[header_type] = 1
            # if parsed_content != "":
            #     print(header_type, ":", parsed_content)
        return result

    def _remove_endline_with_space(self, text):
        return re.sub(r'\n( )*', '\n', text)
    
    def _mark_triple_endline(self, text, mark):
        return re.sub(r'\n\n(\n)+', mark, text)
    
    def _replace_endline(self, text, mark):
        return text.replace("\n", mark)
    
    def _find_header_position(self, text, header_type, headers):
        # print(headers)
        lower_text = text.lower()
        indices = []
        start_positions = []
        for header in headers: 
            indices_object = re.finditer(pattern=header, string=lower_text)
            positions = [(index.start(), index.end()) for index in indices_object]
            for position in positions:
                exist = False
                for start_position in start_positions:
                    if (position[0] == start_position):
                        exist = True
                    break
                if not exist:
                    start_positions += [position[0]]
                    indices += [(position[0], position[1], header_type)]
        # print(indices)
        return indices
    
    def _first(self, n):  
        return n[0]    
        
    # function to sort the tuple     
    def _sort_list_tuple(self, list_of_tuples):  
        return sorted(list_of_tuples, key = self._first) 

    def _parse_summary(self, header_position, text):
        text = self._remove_header(header_position, text)
        text = re.sub(r'\n+', ' ', text) # remove \n
        text = re.sub(r'^ *', '', text) # remove space begin text
        return text 
    
    def _parse_name_and_job(self, header_position, text):
        text = self._remove_header(header_position, text)
        split = list(filter(bool, text.split('\n\n')))
        if len(split) == 0:
            return ""
        if len(split) == 2:
            name = split[0]
            name = re.sub(r'\n+', ' ', name)
            job = split[1]
            job = re.sub(r'\n+', ' ', job)
            return {'name': name, 'job': job}
        return ""

    def _parse_education(self, header_position, text):
        text = self._remove_header(header_position, text)
        return text
    
    def _parse_employment(self, header_position, text):
        text = self._remove_header(header_position, text)
        return text
    
    def _parse_skills(self, header_position, text):
        text = self._remove_header(header_position, text)
        split = list(filter(bool, text.split('\n')))
        if len(split) == 0:
            return ""
        return split
    
    def _has_numbers(self, inputString):
        return bool(re.search(r'\d', inputString))
    
    def _extract_duration(self, text):
        split_chars = ['-']
        regex = r'(\d\d/\d\d\d\d) - (\d\d/\d\d\d\d)|(\d\d/\d\d\d\d)-(\d\d/\d\d\d\d)|(\d\d\d\d) - (\d\d\d\d)|(\d\d\d\d)-(\d\d\d\d)|(\d\d/\d\d\d\d)|(\d\d\d\d)'
        # regex = r'(\d\d/\d\d\d\d)-(\d\d/\d\d\d\d)|(\d\d\d\d)-(\d\d\d\d)|(\d\d/\d\d\d\d)|(\d\d\d\d)'
        matched = re.search(regex, text)
        date_matched = "" if matched == None else matched.group() 
        position = None if matched == None else matched.span()
        split = []
        for split_char in split_chars:
            split = list(filter(bool, date_matched.split(split_char)))
            if len(split) != 0:
                break
        if len(split) == 2:
            return position, {'start': split[0], 'end': split[1]}
        elif len(split) == 1:
            return  position, {'start': split[0]}
        else:
            return None, "cant extract duration"
        
    def _remove_header(self, header_position, text):
        start, end = header_position
        text = text[end - start:]
        text = re.sub(r'^ *', '', text) # remove space begin text
        return text