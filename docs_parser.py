import logging
import json

from scripts.create_link_manifest import create_link_manifest
from scripts.parse_htmls import parse_htmls
from parse_proc.split_page import to_blocktext

logger = logging.getLogger(__name__)


class DocsParser:
    def __init__(self, config):
        self.config = config
        if self.config["use_preload_htmls"]:
            logger.info(f"using preload htmls with manifest {self.config['preload_manifest']}")
            manifest = json.load(open(self.config["preload_manifest"], "r", encoding="utf-8"))
        else:
            manifest = self._parse_data()
        
        self.splitted_docs = {}
        for doc in manifest:
            self.splitted_docs[doc["url"]] = {
                "text_samples": to_blocktext(doc["path_to_file"]),
                "url": doc["url"], 
                "num_course": doc["num_course"],
                "subject": doc["subject"]
            }

    def _parse_data(self):
        logger.info(f'start parsing structure with base url = {self.config["start_url"]}')
        links_manifest = create_link_manifest(self.config["start_url"])
        logger.info("finish parsing structure")

        logger.info(f'start parsing htmls, saving to dir {self.config["dir_with_htmls"]}')
        manifest = parse_htmls(links_manifest, self.config["dir_with_htmls"])
        logger.info("finish parsing htmls")

        return manifest
    
    def get_docs(self):
        return self.splitted_docs