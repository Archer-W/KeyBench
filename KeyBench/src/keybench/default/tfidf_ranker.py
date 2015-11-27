#!/usr/bin/env python
# -*- encoding utf-8 -*-

import math
from keybench.ranker import RankerC
from keybench.default.util import document_frequencies
from keybench.default.util import n_to_m_grams

class TFIDFRanker(RankerC):
  """
  Component performing keyphrase candidate ranking based on the TF-IDF weight of
  their words.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               document_frequencies,
               nb_documents,
               scoring_function=None):
    """
    Constructor of the component.

    @param  name:                         The name of the component.
    @type   name:                         C{string}
    @param  is_lazy:                      True if the component must load
                                          previous data, False if data must be
                                          computed tought they have already been
                                          computed.
    @type   is_lazy:                      C{bool}
    @param  lazy_directory:               The directory used to store previously
                                          computed data.
    @type   lazy_directory:               C{string}
    @param  debug:                        True if the component is in debug
                                          mode, else False. When the component
                                          is in debug mode, it will output each
                                          step of its processing.
    @type   debug:                        C{bool}
    TODO
    TODO
    TODO
    TODO
    @param  scoring_function:             Function that gives a score to a
                                          candidate according to its words.
    @type   scoring_function:             C{function(expression, word_weights,
                                          tag_separator): float}
    """

    super(TFIDFRanker, self).__init__(name, is_lazy, lazy_directory, debug)

    self.set_document_frequencies(document_frequencies)
    self.set_nb_documents(nb_documents)
    self.set_scoring_function(scoring_function)

  def document_frequencies(self):
    """
    """

    return self._document_frequencies

  def set_document_frequencies(self, document_frequencies):
    """
    """

    self._document_frequencies = document_frequencies

  def nb_documents(self):
    """
    """

    return self._nb_documents

  def set_nb_documents(self, nb_documents):
    """
    """
    
    self._nb_documents = nb_documents

  def scoring_function(self):
    """
    Getter of the function used to compute the scores of the multi-word
    expression, based on the single words TF-IDF weight.

    @return:  The function that gives a score to a candidate according to its
              words.
    @rtype:   C{function(expression, word_weights, tag_separator): float}
    """

    return self._scoring_function

  def set_scoring_function(self, scoring_function):
    """
    Setter of the function used to compute the scores of the multi-word
    expression, based on the single words TF-IDF weight.

    @param  scoring_function: The new function that gives a score to a candidate
                              according to its words.
    @type   scoring_function: C{function(expression, word_weights,
                              tag_separator): float}
    """

    self._scoring_function = scoring_function

  def weighting(self, pre_processed_file, candidates, clusters):
    """
    Takes a pre-processed text (list of POS-tagged sentences) and give a weight
    to its keyphrase candidates.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The keyphrase candidates.
    @type     candidates:         C{list(string)}
    @param    clusters:           The clustered candidates.
    @type     clusters:           C{list(list(string))}

    @return:  A dictionary of terms as key and weight as value.
    @rtype:   C{dict(string, float)}
    """

    weighted_candidates = {}

    # scoring function (WARNING: idfs must be extracted for words)
    if self.scoring_function() != None:
      doc_len = len(pre_processed_file.full_text_words())
      word_counts = {}
      weighted_words = {}

      # get the words counts
      for w in pre_processed_file.full_text_words():
        # no tags in the weights
        w = w.lower().rsplit(pre_processed_file.tag_separator(), 1)[0]

        if not word_counts.has_key(w):
          word_counts[w] = 0.0
        word_counts[w] += 1.0

      # compute only the needed words' tf*idf
      for c in candidates:
        for w in c.split():
          # no tags in the weights
          w = w.lower().rsplit(pre_processed_file.tag_separator(), 1)[0]

          if not weighted_words.has_key(w):
            tf = word_counts[w] / doc_len
            try:
              idf = -math.log((self.document_frequencies()[w] + 1.0) / (self.nb_documents() + 1.0), 2)
            except:
              idf = -math.log(1.0 / (self.nb_documents() + 1.0), 2)
            weighted_words[w] = tf * idf

      # compute the candidate scores
      for c in candidates:
        weighted_candidates[c] = self.scoring_function()(c,
                                                         weighted_words,
                                                         pre_processed_file.tag_separator())
    # no scoring function (WARNING: idfs must be extracted for candidates)
    else:
      doc_len = len(pre_processed_file.full_text_words())
      sentences = pre_processed_file.full_text()
      term_counts = {}
      max_candidate_length = 0

      # compute the maximum length of a candidate
      for candidate in candidates:
        max_candidate_length = max(max_candidate_length, len(candidate.split()))

      # count all possible terms occurrences
      for sentence in sentences:
        for term in n_to_m_grams(sentence.split(), 1, max_candidate_length):
          normalized_term = ""

          for word in term.split():
            if normalized_term != "":
              normalized_term += " "
            normalized_term += word.lower().rsplit(pre_processed_file.tag_separator(), 1)[0]

          if not term_counts.has_key(normalized_term):
            term_counts[normalized_term] = 0.0
          term_counts[normalized_term] += 1.0

      # compute TF-IDFs
      for candidate in candidates:
        untagged_candidate = ""

        for word in candidate.split():
          if untagged_candidate != "":
            untagged_candidate += " "
          untagged_candidate += word.rsplit(pre_processed_file.tag_separator(), 1)[0]

        tf = term_counts[untagged_candidate] / doc_len
        try:
          idf = -math.log((self.document_frequencies()[untagged_candidate] + 1.0) / (self.nb_documents() + 1.0), 2)
        except:
          idf = -math.log(1.0 / (self.nb_documents() + 1.0), 2)
        weighted_candidates[candidate] = tf * idf

    return weighted_candidates

  def ordering(self, weights, clusters):
    """
    Takes the weighted candidates of the analysed text and ordered them such as
    the first ones have the highest weight.

    @param    weights:  A dictionary of weighted candidates.
    @type     weights:  C{dict(string, float)}
    @param    clusters: The clustered candidates.
    @type     clusters: C{list(list(string))}

    @return:  A ordered list of weighted terms.
    @rtype:   C{list(tuple(string, float))}
    """

    return sorted(weights.items(), key=lambda row: row[1], reverse=True)

