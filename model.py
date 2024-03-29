from transformers import AutoTokenizer, AutoModelForPreTraining
import torch
import torch.nn.functional as F
from docs_parser import DocsParser
import logging
from tqdm import tqdm
from typing import Dict


logger = logging.getLogger(__name__)


def mean_pooling(model_output: torch.Tensor, attention_mask: torch.Tensor):
    """Function for mean polling. 
    After model inference your have vector for every token, but we need emb for sentence.
    To solve this, we average token-level emb to one sentence-level emb

    Parameters:
        model_output: Tensor with shape (batch_size, cnt_tokens, emb_dim), assume it is model last_hidden_state
        attention_mask: Tensor with shape (batch_size, cnt_tokens, emb_dim), attention_mask for vectorized texts
    """

    input_mask_expanded = attention_mask.unsqueeze(-1).expand(model_output.size()).float()
    sum_embeddings = torch.sum(model_output * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


class AnsweringModel:
    """Class for answering model

    Attributes:
        config: Config for all app, using for specify model name, device type
    """

    def __init__(self, config: Dict):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(self.config["hf_model_name"])
        self.model = AutoModelForPreTraining.from_pretrained(self.config["hf_model_name"])
        self.model = self.model.to(self.config["device"])
        logger.info("start build vector spaces")
        self.build_vector_spaces()
        logger.info("finish build vector spaces")


    def build_vector_spaces(self):
        """Method, which build vector spaces per every combination (num_course, subject_name).
        Vector spacec using for semantic search(in get_answer), to get nearest docs to user question
        """

        parser = DocsParser(self.config)
        splitted_docs = parser.get_docs()

        self.spaces = {}
        unique_keys = list(set([(splitted_docs[i]['num_course'], splitted_docs[i]['subject']) for i in splitted_docs]))
        for key in unique_keys:
            self.spaces[key] = []

        for doc in tqdm(splitted_docs):
            encoded_input = self.tokenizer(splitted_docs[doc]["text_samples"], padding=True,
                                           truncation=True, max_length=512, return_tensors='pt').to(self.model.device)

            # Compute token embeddings
            with torch.no_grad():
                model_output = self.model(**encoded_input, output_hidden_states=True).hidden_states[-1]

            sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
            sentence_embeddings = torch.mean(sentence_embeddings, axis=0)

            self.spaces[(splitted_docs[doc]["num_course"], splitted_docs[doc]['subject'])].append({
                "url": doc,
                "emb": sentence_embeddings
            })


    def get_answer(self, question: str, num_course: int, subject: str):
        """Method for semantic search nearest to user question doc

        Parameters:
            question: Text of user question
        """

        encoded_input = self.tokenizer([question], padding=True, truncation=True,
                                       max_length=512, return_tensors='pt').to(self.model.device)

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input, output_hidden_states=True).hidden_states[-1]

        question_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
        question_embeddings = torch.mean(question_embeddings, axis=0)

        key = (num_course, subject)
        vector_space = self.spaces[key]
        max_cos_sim = -1
        doc_link = ""
        for doc in vector_space:
            sim = F.cosine_similarity(question_embeddings.unsqueeze(0), doc["emb"].unsqueeze(0))

            if sim > max_cos_sim:
                max_cos_sim, doc_link = sim, doc["url"]
        
        logger.info(f"answer sim for question: {question}, sim = {sim}")
        if max_cos_sim > self.config["rubbish_threshold"]:
            return f"Попробуйте посмотреть здесь {doc_link}"
        else:
            return "Боюсь, я не могу ответить на этот вопрос"
