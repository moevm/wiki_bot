from text_dataset_from_html import TextDatasetFromHTML
from typing import Callable, List
import torch


class SearchSpace:
    """
    Class with naive realization of search in vector space.
    Metrics specified by user
    """
    def __init__(self, datasets: List[TextDatasetFromHTML], text_vectorize_func: Callable):
        self.datasets = datasets
        self._build_space(text_vectorize_func)

    def _build_space(self, text_vectorize_func: Callable):
        self.vectorize_func = text_vectorize_func
        self.space = torch.tensor([])
        self.src_files = []
        for dataset in self.datasets:
            for item in dataset:
                for sample in item["text_samples"]:
                    vector = text_vectorize_func(sample)
                    self.space = torch.hstack([self.space, vector.unsqueeze(1)])
                    self.src_files.extend([(item["path_to_file"], item['title'])])
        self.space = torch.transpose(self.space, 0, 1)

    def find_top_nearest(self, text: str, metric: Callable, cnt: int):
        """Return top-k nearest samples and disctace to them"""
        assert len(self.space) > 0, "You need space for search, call build_space before"
        vectotized_text = self.vectorize_func(text)
        distances = torch.tensor([])
        for ind in range(len(self.space)):
            cur_distance = metric(vectotized_text, self.space[ind])
            distances = torch.cat((distances, torch.tensor([cur_distance])))
        values, indices = distances.topk(cnt)
        return values, [self.src_files[i] for i in indices]