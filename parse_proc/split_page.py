from bs4 import BeautifulSoup
from bs4.element import Tag

from transformers import AutoTokenizer

maxLen_tensor = 512

tokenizer = AutoTokenizer.from_pretrained("cointegrated/LaBSE-en-ru")

blocks = ["span", "li", "a", "ol", "tr", "p", "h1", "h2", "h3", "h4", "h5"]


def _extract_blocks(parent_tag):
    extracted_blocks = []
    for tag in parent_tag:
        if tag.name in blocks:
            extracted_blocks.append([tag, tag.name])
            continue
        if isinstance(tag, Tag):
            if len(tag.contents) > 0:
                inner_blocks = _extract_blocks(tag)
                if len(inner_blocks) > 0:
                    extracted_blocks.extend(inner_blocks)
    return extracted_blocks


# сгруппируем текст по заголовкам
def sum_block_h(blocks):
    h_blocks = []
    txt_block = ""
    activate = False
    for block in blocks:
        if not activate and 'h' in block[1]:
            activate = True
        if activate and 'h' in block[1]:
            h_blocks.append(txt_block)
            txt_block = ""
        elif tokenizer(txt_block + " " + block[0].get_text().strip(), padding=True, max_length=None,
                       return_tensors='pt')['input_ids'].shape[-1] > maxLen_tensor:
            h_blocks.append(txt_block)
            txt_block = ""
        txt_block += " " + block[0].get_text().strip()
    if txt_block:
        h_blocks.append(txt_block)
    return h_blocks


# функция, которая получает на вход страницу html и возвращает список блоков
def to_blocktext(html_text):
    soup = BeautifulSoup(html_text, features="lxml")
    extracted_blocks = _extract_blocks(soup.body)

    grouped_text = sum_block_h(extracted_blocks)
    extracted_blocks_texts = []
    text_block = ""

    for i in range(len(grouped_text)):
        if tokenizer(text_block + grouped_text[i], padding=True, max_length=None,
                     return_tensors='pt')['input_ids'].shape[-1] > maxLen_tensor:
            extracted_blocks_texts.append(text_block)
            text_block = ""

        text_block += grouped_text[i]

    if text_block:
        extracted_blocks_texts.append(text_block)

    if grouped_text[-1] not in extracted_blocks_texts[-1]:
        extracted_blocks_texts.append(text_block)

    return extracted_blocks_texts


def main(path_to_html: str = ""): 
    if not path_to_html:
        print("Пропиши путь к файлу")
        return
    with open(path_to_html, 'r', encoding="utf8") as f:
        txt = f.read()

    list_of_blocks = to_blocktext(txt)
    
    return list_of_blocks


if __name__ == "__main__":
    main()
