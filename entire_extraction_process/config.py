PACKAGES = [
    "!pip install spacy",
    "!python -m spacy download en",
    "!pip install allennlp",
    "!pip install allennlp-models",
]
MODEL_URL = "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2020.02.27.tar.gz"