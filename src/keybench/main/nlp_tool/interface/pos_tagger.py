# -*- encoding: utf-8 -*-

import exceptions

class KBPOSTaggerI(object):
  """Interface of a tokenized sentence Part-of-Speech tagger.

  Attributes:
    tagset: The C{dict} of tags (C{list} of C{string} tags) associated to a
      grammatical class (see C{KBPOSTaggerI.POSTagKey}).
  """

  ##############################################################################
  class POSTagKey:
    """Part-of-Speech names.

    Part-of-Speech names to use as tagset keys. Those names are generic and
    meant to match multiple tags. However, highly specific class may not be
    given.

    Attributes:
      NOUN: Key used for noun tags.
      PROPER_NOUN: Key used for proper noun tags.
      ADJECTIVE: Key used for adjective tags.
      VERB: Key used for verb tags.
      ADVERB: Key used for adverb tags.
      PRONOUN: Key used for pronoun tags.
      PREPOSITION: Key used for preposition tags.
      DETERMINER: Key used for determiner tags.
      NUMBER: Key used for number tags.
      FOREIGN_WORD: Key used for foreign word tags.
      PUNCTUATION: Key used for punctuation tags.
    """

    NOUN          = "__noun__"
    PROPER_NOUN   = "__proper_noun__"
    ADJECTIVE     = "__adjective__"
    VERB          = "__verb__"
    ADVERB        = "__adverb__"
    COORDINATION  = "__coordination__"
    PRONOUN       = "__pronoun__"
    PREPOSITION   = "__preposition__"
    DETERMINER    = "__determiner__"
    NUMBER        = "__number__"
    FOREIGN_WORD  = "__foreign_word__"
    PUNCTUATION   = "__punctuation__"
  ##############################################################################

  def __init__(self):
    super(KBPOSTaggerI, self).__init__()

    self._tagset = {}

  @property
  def tagset(self):
    return self._tagset

  def tagName(self, pos_tag):
    """Gives the tag name of a given POS tag.

    Args:
      pos_tag: The C{string} POS tag to get the name of.

    Returns:
      The C{string} tag name corresponding to the POS tag.
    """

    for tag, pos_tags in self._tagset.items() :
      if pos_tag in pos_tags:
        return tag

    return None

  def tag(self, tokenized_sentences):
    """POS tags tokenized sentences.

    Args:
      tokenized_sentences: The C{list} of tokenized sentences (C{list}s of
        C{string} words).

    Returns:
      The C{list} of sentences' POS tags. POS tags of one sentence is a C{list}
      of C{string} tags.
    """

    raise exceptions.NotImplementedError()

