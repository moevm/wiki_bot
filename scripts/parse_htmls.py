import argparse
import requests
from bs4 import BeautifulSoup, Tag
import json
import os
import hashlib
from bs4 import BeautifulSoup, Tag


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
}


def get_html(url: str) -> str:
    req = requests.get(url, headers=headers, verify=False)
    return req.text


def clear_html(html: str):
    soup = BeautifulSoup(html, "lxml")
    page_content = soup.find_all("div", {"class": "page group"})[0]
    toc = page_content.find("div", {"id": "dw__toc"})
    if toc is not None:
        toc.extract()
    return str(page_content)


def main(links_manifest_path: str, result_manifest_path: str, path_to_dir_with_htmls: str):
    path_to_dir_with_htmls =  path_to_dir_with_htmls if path_to_dir_with_htmls.endswith("/") else f"{path_to_dir_with_htmls}/"
    manifest = json.load(open(links_manifest_path, "r"))
    new_manifest = []

    if not os.path.exists(path_to_dir_with_htmls):
        os.makedirs(path_to_dir_with_htmls)

    for item in manifest:
        html = get_html(item['url'])

        if "se.moevm.info" in item["url"]:
            html = clear_html(html)
        html_name = f"{item['num_course']}_{hashlib.md5(html.encode('utf-8')).hexdigest()}.html"
        path_to_save = f"{path_to_dir_with_htmls}{html_name}"
        
        with open(path_to_save, "w", encoding="utf-8") as file:
            file.write(html)
        file.close()

        item['path_to_file'] = path_to_save
        new_manifest.append(item)
    
    json.dump(new_manifest, open(result_manifest_path, 'w'), ensure_ascii=False, indent=4)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--links-manifest-path', type=str, help='path to manifest with links', required=True) 
    parser.add_argument('--result-manifest-path', type=str, help='path for save result manifest', required=True)
    parser.add_argument('--path-to-dir-with-htmls', type=str, help='path for save result htmls', required=True)
    args = parser.parse_args()
    main(args.links_manifest_path, args.result_manifest_path, args.path_to_dir_with_htmls)
