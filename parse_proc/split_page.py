from bs4 import BeautifulSoup
from bs4.element import Tag
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("cointegrated/LaBSE-en-ru")

blocks = ["p", "h1", "h2", "h3", "h4", "h5"]


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
    max_len_of_blocks = max([len(x) for x in [block.get_text().strip() for block in extracted_blocks]])
    extracted_blocks_texts = []
    text_block = ""
    k = 0

    for i in range(len(extracted_blocks) - 1):
        if not text_block and k < 2250 // max_len_of_blocks:
            text_block += " " + extracted_blocks[i].get_text().strip()
            k += 1
            continue
        if len(text_block + " " + extracted_blocks[i + 1].get_text().strip()) > 2250:
            extracted_blocks_texts.append(text_block)
            text_block = ""
            k = 0

        text_block += " " + extracted_blocks[i + 1].get_text().strip()

    if extracted_blocks[-1].get_text().strip() not in extracted_blocks_texts[-1]:
        extracted_blocks_texts.append(extracted_blocks[-1].get_text().strip())

    return extracted_blocks_texts


txt = open('3.html', 'r', encoding="utf8").read()

soup = BeautifulSoup(txt, 'lxml')

list_of_blocks = to_blocktext(txt)
list_of_lens = [len(x) for x in list_of_blocks]
print(list_of_blocks)
print(len(list_of_blocks))

encoded_input = tokenizer(list_of_blocks, padding=True, truncation=True, max_length=64, return_tensors='pt')

print(encoded_input['input_ids'])
