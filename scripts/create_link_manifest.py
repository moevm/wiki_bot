import requests
from bs4 import BeautifulSoup, Tag
from typing import List
import re
import json
import argparse


ALLOW_DOMAINS = [
    "se.moevm.info/",
    "docs.google.com/spreadsheets",
    "docs.google.com/document"
]

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
}


def filter_url(url: str):
    for domain in ALLOW_DOMAINS:
            if re.match(f"https://{domain}", url) is not None:
                return True
    return False


def get_html(url: str) -> str:
    req = requests.get(url, headers=headers, verify=False)
    return req.text


def get_subjects_from_course(start_url: str, level_node: Tag, num_course: int):
    list_of_subjects = []
    for tag in level_node.find_all("a"):
        if filter_url(start_url + tag['href']):
            list_of_subjects.append({
                "url": start_url + tag['href'],
                "human_name": tag.string,
                "subject": tag.string,
                "title": tag["title"],
                "num_course": num_course
            })
    
    return list_of_subjects


def parse_subjects(start_url: str):
    html = get_html(start_url)
    soup = BeautifulSoup(html, "lxml")

    first_course = soup.find_all("li", {"class": "level1 node"})
    other_courses = soup.find_all("li", {"class": "level2 node"})

    list_of_subjects_with_courses = get_subjects_from_course(start_url, first_course[0], 1)

    for i in range(len(other_courses)):
        # already have first course and indexing in real world starts with 1
        list_of_subjects_with_courses.extend(get_subjects_from_course(start_url, other_courses[i], i + 2))
    
    return list_of_subjects_with_courses


def parse_links_from_url(url: str, num_course: int, subject_name: str):
    html = get_html(url)
    soup = BeautifulSoup(html, "lxml")

    links = list(filter(
        lambda x: filter_url(x['href']), 
        soup.find_all("a")
    ))

    result = []
    for link in links:
        result.append({
            "url": link['href'],
            "title": link["title"],
            "human_name": link.string,
            "subject": subject_name,
            "num_course": num_course
        })

    return result


def create_link_manifest(start_url: str):

    link_index = []
    list_of_subjects = parse_subjects(start_url)
    link_index.extend(list_of_subjects)
    
    for subject in list_of_subjects:
        link_index.extend(
            parse_links_from_url(subject['url'], subject['num_course'], subject['subject'])
            )
    
    return link_index


def main(start_url: str, manifest_path: str):
    assert manifest_path.endswith(".json") 
    link_index = create_link_manifest(start_url)
    json.dump(link_index, open(manifest_path, 'w'), ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-url', type=str, help='default url', default="https://se.moevm.info") 
    parser.add_argument('--result-manifest-path', type=str, help='path for save result manifest')
    args = parser.parse_args()
    main(args.start_url, args.result_manifest_path)
