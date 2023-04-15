# wiki_bot


## Запуск скриптов парсинга

Чтобы получить список всех ссылок с интересующими нас html-ками, надо запустить скрипт:
```
python create_link_manifest.py --result-manifest_path=manifest_only_links.json
```

Чтобы спарсить полученные html-ки надо запустить следующий скрипт:
```
python parse_htmls.py --links-manifest-path manifest_only_links.json --result-manifest-path result.json --path-to-dir-with-htmls data/
```