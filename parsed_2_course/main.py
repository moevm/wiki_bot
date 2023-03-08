import requests
from bs4 import BeautifulSoup
import json
import csv

url_pr_1 = "https://se.moevm.info/doku.php/courses:programming:start"
url_inf_1 = "https://se.moevm.info/doku.php/courses:informatics:start"
url_oop_2 = "https://se.moevm.info/doku.php/courses:object_oriented_programming:start"
url_aisd_2 = "https://se.moevm.info/doku.php/courses:algorithms_structures:start"
url_piaa_2 = "https://se.moevm.info/doku.php/courses:algorithms_building_and_analysis:start"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
}


def get_html(url: str) -> str:
    req = requests.get(url, headers=headers, verify=False)
    return req.text


def write_to_file(filename: str, src: str) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        file.write(src)
    file.close()


def read_from_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        src = file.read()
    file.close()
    return src


def edit_html_a_tags(src: str) -> str:
    src.replace('<a href="/doku.php', '<a href="https://se.moevm.info/doku.php').replace('<a href="/lib',
                                                                                         '<a href="https://se.moevm.info/lib')
    return src


def get_all_links_from_html(filename: str, step: int, csvfile: str):
    src = read_from_file(filename)
    soup = BeautifulSoup(src, "lxml")
    all_links = soup.find_all("a")
    number_of_htmls = len(all_links)
    count = 0
    m = []
    for link in all_links:
        try:
            if not count:
                mode = "w"
            else:
                mode = "a"

            link_text_raw = link.text.strip()
            link_url_raw = link.get("href").strip()
            link_text = " ".join(link_text_raw.split())
            link_url = " ".join(link_url_raw.split())
            print(link_text)
            count += 1
            if not step:
                link_content = get_html(link_url)
                write_to_file(str(count) + ".html", link_content)

            if count <= number_of_htmls:
                link_content_name = str(count) + ".html"
                link_content = read_from_file(str(count) + ".html")
            else:
                link_content_name = ""
            with open(csvfile, mode=mode, encoding='utf-8') as w_file:
                file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
                file_writer.writerow([link_text, link_url, link_content_name])
            w_file.close()
        except Exception as ex:
            print(ex)


def main():
    # src = get_html(url_piaa_2)
    # write_to_file("2_3.html", src)
    # src =read_from_file("2_3.html")
    # s1 = src.replace('"/doku.php', '"https://se.moevm.info/doku.php').replace('"/lib',
    #                                                                                      '"https://se.moevm.info/lib')
    get_all_links_from_html("2_3.html", 0, "links_piaa_2.csv")

# src = get_html(url_oop_2)
# write_to_file("2_1.html", src)
# get_all_links_from_html("index.html", 1, 26, "links_pr_1.csv")
# src = get_html(url_inf_1)
# write_to_file("1_2.html", src)
# src = read_from_file("1_2.html")
# s1 = src.replace('<a href="/doku.php', '<a href="https://se.moevm.info/doku.php').replace('<a href="/lib',
#                                                                                      '<a href="https://se.moevm.info/lib')
# print(s1)
# write_to_file("1_2.html", s1)
# get_all_links_from_html("1_2.html", 0, 100, "links_inf_1.csv")
# src = read_from_file("2_1.html")
# s1 = src.replace('<a href="/doku.php', '<a href="https://se.moevm.info/doku.php').replace('<a href="/lib',


if __name__ == "__main__":
    main()
