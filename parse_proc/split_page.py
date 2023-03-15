from bs4 import BeautifulSoup
from bs4.element import Tag
from transformers import AutoTokenizer

maxNum_chars = 2250
maxLen_tensor = 512

tokenizer = AutoTokenizer.from_pretrained("cointegrated/LaBSE-en-ru")

blocks = ["ol", "ul", "tr", "p", "h1", "h2", "h3", "h4", "h5"]


def _extract_blocks(parent_tag):
    extracted_blocks = []
    for tag in parent_tag:
        if tag.name in blocks:
            extracted_blocks.append(tag)
            continue
        if isinstance(tag, Tag):
            if len(tag.contents) > 0:
                inner_blocks = _extract_blocks(tag)
                if len(inner_blocks) > 0:
                    extracted_blocks.extend(inner_blocks)
    return extracted_blocks


def to_blocktext(html_text):
    soup = BeautifulSoup(html_text, features="lxml")
    extracted_blocks = _extract_blocks(soup.body)
    encoded_text_blocks = [block.get_text().strip() for block in extracted_blocks]
    encoded_blocks = tokenizer(encoded_text_blocks, padding=True, max_length=None, return_tensors='pt')
    max_len_of_blocks = len(encoded_blocks['input_ids'][0])
    extracted_blocks_texts = []
    text_block = ""
    k = 0

    for i in range(len(extracted_blocks) - 1):
        if not text_block or k < maxLen_tensor // max_len_of_blocks:
            text_block += " " + extracted_blocks[i].get_text().strip()
            k += 1
            continue
        if tokenizer(text_block + " " + extracted_blocks[i + 1].get_text().strip(), padding=True, max_length=None,
                     return_tensors='pt')['input_ids'].shape[-1] > maxLen_tensor:
            extracted_blocks_texts.append(text_block)
            text_block = ""
            k = 0

        text_block += " " + extracted_blocks[i + 1].get_text().strip()

    extracted_blocks_texts.append(text_block)

    if extracted_blocks[-1].get_text().strip() not in extracted_blocks_texts[-1]:
        extracted_blocks_texts.append(extracted_blocks[-1].get_text().strip())

    return extracted_blocks_texts


with open('3.html', 'r', encoding="utf8") as f:
    txt = f.read()

list_of_blocks = to_blocktext(txt)
list_of_lens = [len(x) for x in list_of_blocks]

encoded_input = tokenizer(list_of_blocks, padding=True, max_length=None, return_tensors='pt')
