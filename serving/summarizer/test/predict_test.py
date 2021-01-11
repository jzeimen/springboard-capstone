import unittest
from  predict import Predictor
import os
class TestPredictorMethods(unittest.TestCase):
    def setUp(self):
        self.predictor = Predictor()
        test_dir = os.path.dirname(os.path.realpath(__file__))
        self.predictor.init(os.path.join(test_dir,'..','..','model'))


    def test_split_article(self):
        """ Test that we correctly split the article up.
        """
        sentences = ['This is the first sentence.',
        'The quick brown fox jumps over the lazy dog.',
        'Some other third sentence can go here.']
        article = " ".join(sentences)
        actual = self.predictor.split_sentences(article)
        self.assertListEqual(sentences, actual)

    def test_make_mask(self):
        """ The model will need to know what actual sentences are and which are not.
            This mask is fed into the layers that need to know. The article can only be 
            30 sentences long. 
        """
        sents = ['1','2','3']
        expected = [True] * 3 + [False] * 27
        actual = self.predictor.make_mask(sents)
        self.assertListEqual(expected, actual)


    def test_padding(self):
        """ The deep learning model needs a fixed length of input,
            The padding insures that we have at least 30 strings as input
            even when we don't have that many sentences.
        """
        sents = ['1','2','3']
        sents_expected = sents + [''] * 27
        sents_actual = self.predictor.pad_sents(sents)
        self.assertListEqual(sents_expected, sents_actual)



    def test_predict(self):
        """ This will run through the whole prediction, the actual prediction will 
        return different results if hte modle file is changed, but we can at least make
        sure that it returns 3 sentences like expected."""
        article = 'After a long race the tortoise ended up beating the hare.'\
                ' The race happened last weekend.'\
                ' The hare was originally the favorite but after taking a 5 hour nap the tortoise had time to catch up.'\
                ' The hare could not belive he was beaten like that.'\
                ' The tortoise claimed that he could beat the hare in any race.'
        predictions = self.predictor.predict(article)
        sents = self.predictor.split_sentences(predictions)
        self.assertEqual(len(sents), 3)