# -*- encoding: utf-8 -*-

import re

from keybench.main import core
from keybench.main import model
from keybench.main.component import interface

class POSSequenceBasedCandidateExtractor(interface.KBCandidateExtractorI):
  """Pattern matching candidate extractor.

  Candidate extractor providing only textual units that match given
  Part-of-Speech patterns (e.g. r"JJ?NN+"), using the appropriate tag labels
  (see C{keybench.main.nltp_tool.interface.KBPOSTaggerI.POSTagKey}).
  """

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache,
               pos_regexp):
    """Constructor.

    Args:
      name: The C{string} name of the component.
      run_name: The C{string} name of the run for which the component is
        affected to.
      shared: True if the component shares informations with equivalent
        components (same name).
      lazy_mode: True if the component load precomputed data. False, otherwise.
      debug_mode: True if the component can log debug messages. False,
        otherwise.
      root_cache: The root of the cache directory where the cached objects must
        be stored.
      pos_regexp: The regular expression that represents Part-of-Speech patterns.
    """

    super(POSSequenceBasedCandidateExtractor, self).__init__(name,
                                                             run_name,
                                                             shared,
                                                             lazy_mode,
                                                             debug_mode,
                                                             root_cache)

    self._pos_regexp = pos_regexp

  def _candidateExtraction(self, document):
    """Extracts the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be extracted.

    Returns:
      The C{list} of extracted, and filtered, candidates (C{KBTextualUnit}s).
    """

    tokenized_sentences = document.full_text_sentence_tokens
    pos_tagged_sentences = document.full_text_token_pos_tags
    candidates = {}

    # extract sentences' textual units matching POS tag patterns
    for sentence_offset, tokenized_sentence in enumerate(tokenized_sentences):
      pos_tagged_sentence = pos_tagged_sentences[sentence_offset]
      full_pos_tag_sequence = " ".join(pos_tagged_sentence)
      pos_position_to_inner_sentence_position = {}

      # create the map associating the position a POS tag first character to a
      # token position
      pos_character_position_accumulator = 0
      for inner_sentence_position, pos in pos_tagged_sentence:
        pos_position_to_inner_sentence_position[pos_character_position_accumulator] = inner_sentence_position

        pos_character_position_accumulator += len(pos) + 1 # 1 is for the " "

      # find the textual unit matching the POS tag sequence represented by the
      # regexp
      for match in re.finditer(self._pos_regexp, full_pos_tag_sequence):
        start = pos_position_to_inner_sentence_position[match.start()]
        end = start + (match.end() - match.start())

        super(POSSequenceBasedCandidateExtractor, self)._updateCandidateDictionary(candidates,
                                                                                   document,
                                                                                   sentence_offset,
                                                                                   start,
                                                                                   end)

    return candidates.values()

