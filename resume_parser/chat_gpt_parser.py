import json
import openai

openai.api_key = "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"

PARSE_PROMT = "Parse the following resume and extract the following information: {0}. And convert into JSON format with schema: {1}\n\n\"{2}\""

class ChatGPTParser:
    def __init__(self):
        self.sections = "personal details, professional summary, employment history, education, skills"
        schema_filepath = './resume_parser/resume_schema.json'
        schema_file = open(schema_filepath)
        self.resume_schema = json.load(schema_file)
        schema_file.close()
    def parse(self, raw_text):
        completion = openai.ChatCompletion.create(
            model="text-davinci-002",
            messages=[
                {"role": "user", "content": PARSE_PROMT.format(self.sections, self.resume_schema, raw_text)}
            ])
        print(completion.choices[0].message)
