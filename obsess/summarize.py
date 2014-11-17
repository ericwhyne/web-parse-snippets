# Modified by Eric Whyne 2014
# Orignal author: Tristan Havelick <tristan@havelick.com> https://github.com/thavelick/summarize/

from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk.data

class SimpleSummarizer:

    def reorder_sentences( self, output_sentences, input ):
        output_sentences.sort( lambda s1, s2:
            input.find(s1) - input.find(s2) )
        return output_sentences

    def get_summarized(self, input, num_sentences,mustinclude):
        # TODO: allow the caller to specify the tokenizer they want
        # TODO: allow the user to specify the sentence tokenizer they want

        tokenizer = RegexpTokenizer('\w+')

        # get the frequency of each word in the input
        base_words = [word.lower()
            for word in tokenizer.tokenize(input)]
        words = [word for word in base_words if word not in stopwords.words()]
        word_frequencies = FreqDist(words)

        # now create a set of the most frequent words
        most_frequent_words = [pair[0] for pair in word_frequencies.items()[:100]]

        # break the input up into sentences.  working_sentences is used
        # for the analysis, but actual_sentences is used in the results
        # so capitalization will be correct.

        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        actual_sentences = sent_detector.tokenize(input)
        working_sentences = [sentence.lower()
            for sentence in actual_sentences]

        mustinclude = mustinclude.lower()

        # iterate over the most frequent words, and add the first sentence
        # that inclues each word to the result.
        output_sentences = []

        for word in most_frequent_words:
            for i in range(0, len(working_sentences)):
                if (mustinclude in working_sentences[i] and word in working_sentences[i] and actual_sentences[i] not in output_sentences):
                    output_sentences.append(actual_sentences[i])
                    break
                if len(output_sentences) >= num_sentences: break
            if len(output_sentences) >= num_sentences: break

        # If we came up empty just find a sentence with our word that must be included
        if len(output_sentences) == 0:
          for i in range(0, len(working_sentences)):
            if mustinclude in working_sentences[i]:
              output_sentences.append(actual_sentences[i])
              break

        # sort the output sentences back to their original order
        return self.reorder_sentences(output_sentences, input)

    def summarize(self, input, num_sentences, mustinclude = " "):
        return " ".join(self.get_summarized(input, num_sentences, mustinclude))
