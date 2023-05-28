from transformers import AutoTokenizer, AutoModelForPreTraining
import torch
import torch.nn.functional as F
from docs_parser import DocsParser
from hyperpyyaml import load_hyperpyyaml


def mean_pooling(model_output, attention_mask):
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(model_output.size()).float()
    sum_embeddings = torch.sum(model_output * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


class AnsweringModel:
    
    def __init__(self, path_to_config):
        with open(path_to_config) as fin:
            self.config = load_hyperpyyaml(fin)

        self.tokenizer = AutoTokenizer.from_pretrained(self.config["hf_model_name"]) 
        self.model = AutoModelForPreTraining.from_pretrained(self.config["hf_model_name"])
        self.model = self.model.to(self.config["device"]) 
    
    def build_vector_spaces(self):
        
        parser = DocsParser(self.config)
        splitted_docs = parser.get_docs()

        self.spaces = {}
        unique_keys = list(set([i['num_course'] for i in splitted_docs]))
        for key in unique_keys:
            self.spaces = [key]

        for doc in splitted_docs:
            encoded_input = self.tokenizer(doc["text_samples"], padding=True, truncation=True, max_length=512, return_tensors='pt').to(model.device)

            #Compute token embeddings
            with torch.no_grad():
                model_output = self.model(**encoded_input, output_hidden_states=True).hidden_states[-1]

            sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
            sentence_embeddings = torch.mean(sentence_embeddings, axis=0)

            self.spaces[doc["num_course"]].append({
                "url": doc["url"],
                "emb": sentence_embeddings
                })
            

    def get_answer(self, question: str, num_course: int, subject: str):
        encoded_input = self.tokenizer([question], padding=True, truncation=True, max_length=512, return_tensors='pt').to(model.device)
        
        #Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input, output_hidden_states=True).hidden_states[-1]

        question_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
        question_embeddings = torch.mean(question_embeddings, axis=0)

        key = num_course
        vector_space = self.spaces[key]
        max_cos_sim = -1
        doc_link = ""
        for doc in vector_space:
            sim = F.cos_sim(question_embeddings.unsqueeze(0), doc["emb"].unsqueeze(0))
            
            if sim > max_cos_sim:
                max_cos_sim, doc_link = sim, doc["url"]

        if max_cos_sim > self.config["rubbish_threshold"]:
            return f"Попробуйте посмотреть здесь {doc_link}"
        else:
            return "Боюсь, я не могу ответить на этот вопрос"
        