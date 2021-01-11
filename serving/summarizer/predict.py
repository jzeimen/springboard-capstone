import tensorflow as tf
import spacy
import pandas as pd
from rouge_score import rouge_scorer

MAX_ARTICLE_LENGTH = 30

class Predictor():
    def __init__(self):
        self.model = None
        self.nlp = None

    def init(self, model_file_override=None):
        """If the model is not loaded the model, do so now."""
        if self.model is None:
            model_file = "model"
            if model_file_override is not None:
                model_file = model_file_override
            self.model = tf.keras.models.load_model(model_file)
            self.nlp = spacy.load('en_core_web_sm')

    def predict(self, article, n=3):
        """Given the article, return the top n sentences that summarize it"""
        self.init()
        sentences = self.split_sentences(article)
        return self.predict_top_sents(sentences, n=n)

    def split_sentences(self, article):
        return [str(i) for i in list(self.nlp(article, disable=['tagger', 'ner']).sents)]


    def score_sentences(self, sentences):
        sentences = sentences[:MAX_ARTICLE_LENGTH]
        sentences = self.pad_sents(sentences)
        mask = self.make_mask(sentences)
        scores = self.model({"article_sentences":tf.constant([sentences]*MAX_ARTICLE_LENGTH), 
                "sent":tf.constant(sentences), 
                "mask": tf.constant([mask]*MAX_ARTICLE_LENGTH)})
        scores = scores.numpy().squeeze()
        return scores, sentences

    def predict_top_sents(self, sentences, n=1):
        scores, sentences = self.score_sentences(sentences)
        df = pd.DataFrame({'score': scores, 'sentence': sentences})
        return " ".join(df.nlargest(n,'score').sort_index()['sentence'].values.tolist())

    # If the article is less than MAX_ARTICLE_LENGTH, we need to pad and mask the empty sentences.
    @classmethod
    def make_mask(cls, sents):
        length = len(sents)
        return ([True] * length) +([False] * (MAX_ARTICLE_LENGTH-length))

    # Just use empty strings to pad
    @classmethod
    def pad_sents(cls, sents):
        length = len(sents)
        if not isinstance(sents, list):
            sents = sents.tolist()
        return sents + [""] * (MAX_ARTICLE_LENGTH-length)

