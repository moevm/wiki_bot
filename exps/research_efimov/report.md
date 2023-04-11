# Мотивация

Была поставлена задача провести исследование по одной или нескольким статей, дабы выяснить возможные модернизации для сегментации текста при помощи machine learning.


## Анализ статьи 

Для исследования была выбрана статья [Transformer over Pre-trained Transformer for Neural Text Segmentation with Enhanced Topic Coherence](https://arxiv.org/pdf/2110.07160.pdf).
Если кратко, то вот, что было в статье:

Первым шагом исследователи описали задачу сегментации текста, которая важна для многих приложений обработки естественного языка. Задача состоит в разделении текста на сегменты, каждый из которых должен содержать информацию об отдельных темах обсуждения.

В статье описывается эксперимент, который показывает преимущества Transformer-модели перед предобученной на большом корпусе текстов BERT-моделью в задаче сегментации текста. Исследователи создали две модели - BERT-SP и Transformer-SP.

BERT-SP модель основана на обучении предварительно обученной BERT-модели для задачи сегментации текста. Transformer-SP модель основана на той же архитектуре, что и BERT-SP, но использует самостоятельно обученные энкодеры.

Эксперимент состоял из трех последовательных шагов: извлечение кластеров, порождение сегментов и оценка коэффициента тематической связности для каждого сегмента. Исследователи провели эксперименты на нескольких наборах данных и сравнили результаты работы двух моделей.


## Результат статьи и вывод: 

В результате эксперимента было показано, что Transformer-SP модель показывает лучшее качество в сегментации текста и улучшении тематической связности в сравнении с BERT-SP моделью. В частности, Transformer-SP модель показала наилучший результат на трех наборах данных, используемых в эксперименте.

Основной вывод статьи заключается в том, что Transformer-модель более эффективна для решения задачи сегментации текста и улучшения тематической связности в сегментах по сравнению с предварительно обученной BERT-моделью. Это может привести к улучшению качества решения более широкого спектра задач обработки естественного языка.

# Целесообразность использования

Если в нескольких словах, то использование такого подхода к сегментации текста - не вариант. Учитывая, что архитектура проекта построена на модели BERT, переписывание на Transformer-SP не имеет абсолютно никакого смысла.