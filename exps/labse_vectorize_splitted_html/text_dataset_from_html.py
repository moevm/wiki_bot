from torch.utils.data import Dataset
import pandas as pd
from typing import Callable


class TextDatasetFromHTML(Dataset):
    """
    Class for dataset with texts, obtained from src html by using split_func,
    which must be specified by user. 
    """
    def __init__(self, path_to_dir: str, path_to_manifest: str, split_func: Callable):
        assert path_to_dir != "", "Please, set path to directory with html"
        assert path_to_manifest != "", "Please, set path to manifest(csv) with files"
        self.path_to_dir = path_to_dir
        self.path_to_manifest = path_to_manifest
        self.manifest = pd.read_csv(path_to_manifest, sep=";", names=["title", "url", "filename"])
        self.manifest = self.manifest.dropna()
        self._split_htmls(split_func)
    
    def _split_htmls(self, split_func: Callable):
        self.text_samples = []
        for row in self.manifest.iterrows():
            row = row[1]
            path_to_file = self.path_to_dir + row['filename']
            current_text_samples = split_func(path_to_file)
            self.text_samples.append({
                "path_to_file": path_to_file,
                "text_samples": current_text_samples,
                "title": row['title']
            })

    def __getitem__(self, ind):
        """Return item with text_sample, path to src file and title of file"""
        assert len(self.text_samples) > 0, "Please, call split_htmls before"
        return self.text_samples[ind]
    
    def __len__(self):
        return len(self.manifest)