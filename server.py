from concurrent import futures
import logging
import grpc
import huggingface_hub
import settings
import cv2
import base64
import os
import pytesseract
import numpy as np
import json
from pdf2image import convert_from_path
from summary_generator.gpt2_generator import GPT2Generator
from summary_generator.gramformer import GrammarCorrect
from resume_parser.bart_parser import BartParser
from resume_parser.rule_based_parser import RuleBasedParser
from resume_parser.chat_gpt_parser import ChatGPTParser
from protos import resume_builder_ai_service_pb2, resume_builder_ai_service_pb2_grpc

import platform
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class ResumeAIServiceServicer(resume_builder_ai_service_pb2_grpc.ResumeAIServiceServicer):
    def __init__(self, hf_auth_token, summary_model_path, resume_parser_model_path):
        # huggingface_hub.login(token=hf_auth_token)
        self.summary_generator = GPT2Generator(summary_model_path)
        if(settings.enable_gramformer):
            self.grammar_correct = GrammarCorrect()
        self.bart_resume_parser = BartParser(resume_parser_model_path)
        self.rule_based_resume_parser = RuleBasedParser()
        self.chat_gpt_resume_parser = ChatGPTParser()

    def ParseResume(self, request, context):
        # TODO
        # request: ParseResumeRequest
        # response: ParseResumeResponse
        logging.info("parsing resume ...")
        bytes = base64.b64decode(request.base64data)
        filename = request.filename
        filetype = request.filetype
        filepath = os.path.join("temp", f"{filename}.{filetype}")
        parsetype = request.parsetype

        with open(filepath, 'wb') as f:
            f.write(bytes)
            f.close()
        
        
        if filetype == "pdf":
            raw_text = self.pdf_to_text(filepath)
        else:
            raw_text = self.image_to_text(filepath)   

        result = self.bart_resume_parser.parse(raw_text)

        os.remove(filepath)
        split = filepath.split('.')
        os.remove(''.join(split[:-1]) + '_scaled' + "." + split[-1])     
        return resume_builder_ai_service_pb2.ParseResumeResponse(result=json.dumps(result))


    def SuggestionSummary(self, request, context):
        logging.info("suggesting summary ...")
        generated = self.summary_generator.generate_sequences(request.input)
        if(settings.enable_gramformer):
            generated = self.grammar_correct.correct(generated)
        generated = '|'.join(generated)
        return resume_builder_ai_service_pb2.SuggestionSummaryResponse(output=generated)
    
    def image_to_text(self, image_path):
        image_root = cv2.imread(image_path)
        image_size = (1414, 2000)
        image = cv2.resize(image_root, image_size, interpolation= cv2.INTER_LINEAR)
        split = image_path.split('.')
        cv2.imwrite(''.join(split[:-1]) + "_scaled" + "." + split[-1], image)
        np_array = np.array(image, dtype=np.uint8)
        text = pytesseract.image_to_string(np_array)
        return text
    
    def pdf_to_text(self, pdf_file):
        image = convert_from_path(pdf_file)[0]
        split = pdf_file.split('.')
        image_path = ''.join(split[:-1]) + '.png'
        image.save(image_path)
        return self.image_to_text(image_path) 
    
def serve():
    logging.info("Server starting ...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=32))
    server.add_insecure_port(f'[::]:{settings.service_port}')
    resume_builder_ai_service_pb2_grpc.add_ResumeAIServiceServicer_to_server(
        ResumeAIServiceServicer(
            settings.hf_auth_token,
            settings.summary_model_path,
            settings.resume_parser_model_path
        ),
        server
    )
    server.start()
    print("tesseract_version", pytesseract.get_tesseract_version().base_version)
    logging.info(f"Started server on port {settings.service_port}")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    serve()