#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import codecs
from candidate_extractors import NounAndADJRExtractor
from candidate_extractors import ExpandedCoreWordExtractor
from candidate_extractors import POSBoundaryBasedCandidateExtractor
from candidate_extractors import POSSequenceExtractor
from candidate_extractors import FromTerminologyExtractor
from candidate_extractors import NPChunkExtractor
from candidate_extractors import STFilteredNGramExtractor
from candidate_extractors import PatternMatchingExtractor
from candidate_extractors import CLARIT96Extractor
from candidate_extractors import CLARIT96_LEXATOM_TAG
from candidate_extractors import train_clarit
from candidate_clusterers import StemOverlapHierarchicalClusterer
from candidate_clusterers import TermVariantClusterer
from candidate_clusterers import LINKAGE_STRATEGY
from evaluators import StandardPRFMEvaluator
from keybench import KeyphraseExtractor
from keybench import KeyBenchWorker
from keybench.default import FakeClusterer
from keybench.default.util import document_frequencies
from keybench.default.util import n_to_m_grams
from keybench.default import TFIDFRanker
from multiprocessing import Queue
from pre_processors import FrenchPreProcessor
from pre_processors import EnglishPreProcessor
from rankers import TextRankRanker
from rankers import KEARanker
from rankers import ORDERING_CRITERIA
from rankers import train_kea
from selectors import UnredundantTextRankSelector
from selectors import UnredundantTopKSelector
from selectors import UnredundantWholeSelector
from graph_based_ranking import TextRankStrategy
from graph_based_ranking import SingleRankStrategy
from graph_based_ranking import TopicRankStrategy
from graph_based_ranking import CompleteGraphStrategy
from util import INISTFileRep
from util import DEFTFileRep
from util import InspecFileRep
from util import PlainTextFileRep
from util import SemEvalFileRep
from util import DUCFileRep
from util import term_scoring
from util import WikiNewsFileRep
from util import bonsai_tokenization
from util import french_stemmed_adjr
from util import french_adjr_stem_ending_counts
from util import english_stemmed_adjr
from util import english_adjr_stem_ending_counts
from nltk.stem import PorterStemmer
from nltk.stem.snowball import FrenchStemmer
from nltk.tokenize.treebank import TreebankWordTokenizer
from os import makedirs
from os import path
from os import listdir
from topicrank_pp import TopicRankPPRanker
from topicrank_pp import add_topicrankpp_graphs_and_models

################################################################################

RUNS_DIR = "results_october_2015_test" # directory used to save informations

##### corpora information ######################################################

CORPORA_DIR = path.join(path.dirname(sys.argv[0]), "..", "res", "corpora")

DEFT_CORPUS_DIR = path.join(CORPORA_DIR, "deft_2012", "test_t2")
DEFT_CORPUS_DOCS = path.join(DEFT_CORPUS_DIR, "documents")
DEFT_CORPUS_REFS = path.join(DEFT_CORPUS_DIR, "ref_test_t2")
DEFT_CORPUS_TERM_SUITE_TERMINOLOGY = path.join(DEFT_CORPUS_DIR, "term_suite_terminology_t2")
DEFT_CORPUS_TERM_SUITE_CLUSTERS = path.join(DEFT_CORPUS_DIR, "term_suite_clusters_t2")
DEFT_CORPUS_ACABIT_TERMINOLOGY = path.join(DEFT_CORPUS_DIR, "acabit_terminology_t2")
DEFT_CORPUS_TRAIN_DOCS = path.join(DEFT_CORPUS_DIR, "train")
DEFT_CORPUS_DOCS_EXTENSION = ".xml"

WIKINEWS_CORPUS_DIR = path.join(CORPORA_DIR, "wikinews_2012")
WIKINEWS_CORPUS_DOCS = path.join(WIKINEWS_CORPUS_DIR, "documents")
WIKINEWS_CORPUS_REFS = path.join(WIKINEWS_CORPUS_DIR, "ref")
WIKINEWS_CORPUS_DOCS_EXTENSION = ".html"

SEMEVAL_CORPUS_DIR = path.join(CORPORA_DIR, "semeval_2010")
SEMEVAL_CORPUS_DOCS = path.join(SEMEVAL_CORPUS_DIR, "documents")
SEMEVAL_CORPUS_REFS = path.join(SEMEVAL_CORPUS_DIR,
                                "ref_modified_stem_combined")
SEMEVAL_CORPUS_TERM_SUITE_TERMINOLOGY = path.join(SEMEVAL_CORPUS_DIR, "term_suite_terminology")
SEMEVAL_CORPUS_TERM_SUITE_CLUSTERS = path.join(SEMEVAL_CORPUS_DIR, "term_suite_clusters")
SEMEVAL_CORPUS_ACABIT_TERMINOLOGY = path.join(SEMEVAL_CORPUS_DIR, "acabit_terminology")
SEMEVAL_CORPUS_TRAIN_DOCS = path.join(SEMEVAL_CORPUS_DIR, "train")
SEMEVAL_CORPUS_DOCS_EXTENSION = ".txt"
SEMEVAL_CORPUS_TRAIN_GRAPH = path.join(SEMEVAL_CORPUS_DIR,
                                       "train_model",
                                       "model_intra_bi_occ.pickle")
SEMEVAL_CORPUS_TRAIN_MODEL = path.join(SEMEVAL_CORPUS_DIR,
                                       "train_model",
                                       "model_extra.pickle")

DUC_CORPUS_DIR = path.join(CORPORA_DIR, "duc_2001")
#DUC_CORPUS_DOCS = path.join(DUC_CORPUS_DIR, "documents")
DUC_CORPUS_DOCS = path.join(DUC_CORPUS_DIR, "full")
#DUC_CORPUS_REFS = path.join(DUC_CORPUS_DIR, "ref")
DUC_CORPUS_REFS = path.join(DUC_CORPUS_DIR, "ref_full")
DUC_CORPUS_TERM_SUITE_TERMINOLOGY = path.join(DUC_CORPUS_DIR, "term_suite_terminology")
DUC_CORPUS_TERM_SUITE_CLUSTERS = path.join(DUC_CORPUS_DIR, "term_suite_clusters")
DUC_CORPUS_ACABIT_TERMINOLOGY = path.join(DUC_CORPUS_DIR, "acabit_terminology")
DUC_CORPUS_TRAIN_DOCS = path.join(DUC_CORPUS_DIR, "train")
DUC_CORPUS_DOCS_EXTENSION = ".xml"
DUC_CORPUS_TRAIN_GRAPH = path.join(DUC_CORPUS_DIR,
                                   "train_model",
                                   "model_intra_bi_occ.pickle")
DUC_CORPUS_TRAIN_MODEL = path.join(DUC_CORPUS_DIR,
                                   "train_model",
                                   "model_extra.pickle")

INSPEC_CORPUS_DIR = path.join(CORPORA_DIR, "inspec")
INSPEC_CORPUS_DOCS = path.join(INSPEC_CORPUS_DIR, "documents")
INSPEC_CORPUS_REFS = path.join(INSPEC_CORPUS_DIR, "ref_contr")
INSPEC_CORPUS_TRAIN_DOCS = path.join(INSPEC_CORPUS_DIR, "train")
INSPEC_CORPUS_DOCS_EXTENSION = ".abstr"
INSPEC_CORPUS_TRAIN_GRAPH = path.join(INSPEC_CORPUS_DIR,
                                      "train_model",
                                      "model_intra_bi_occ.pickle")
INSPEC_CORPUS_TRAIN_MODEL = path.join(INSPEC_CORPUS_DIR,
                                      "train_model",
                                      "model_extra.pickle")

INIST_CORPUS_DIR = path.join(CORPORA_DIR, "inist")
INIST_CORPUS_DOCS_EXTENSION = ".xml"
INIST_LINGUISTIQUE_CORPUS_DOCS = path.join(INIST_CORPUS_DIR,
                                           "linguistique",
                                           "test")
                                           #"dev")
#INIST_LINGUISTIQUE_CORPUS_DOCS = path.join(INIST_CORPUS_DIR,
#                                           "linguistique",
#                                           "train")
INIST_LINGUISTIQUE_CORPUS_TRAIN_DOCS = path.join(INIST_CORPUS_DIR,
                                                 "linguistique",
                                                 "train")
INIST_LINGUISTIQUE_CORPUS_REFS = path.join(INIST_CORPUS_DIR,
                                          "linguistique",
                                          "ref")
                                          #"ref_dev")
#INIST_LINGUISTIQUE_CORPUS_REFS = path.join(INIST_CORPUS_DIR,
#                                          "linguistique",
#                                          "ref_train")
INIST_LINGUISTIQUE_CORPUS_TRAIN_GRAPH = path.join(INIST_CORPUS_DIR,
                                                  "linguistique",
                                                  "train_model",
                                                  "model_intra_bi_occ.pickle")
INIST_LINGUISTIQUE_CORPUS_TRAIN_MODEL = path.join(INIST_CORPUS_DIR,
                                                  "linguistique",
                                                  "train_model",
                                                  "model_extra.pickle")
INIST_LINGUISTIQUE_CORPUS_TERM_SUITE_TERMINOLOGY = path.join(INIST_CORPUS_DIR, "linguistique", "termsuite_terminology.tsv")
INIST_LINGUISTIQUE_CORPUS_TERM_SUITE_CLUSTERS = path.join(INIST_CORPUS_DIR, "linguistique", "termsuite_clusters.tsv")
#-------------------------------------------------------------------------------
INIST_ARCHEOLOGIE_CORPUS_DOCS = path.join(INIST_CORPUS_DIR,
                                           "archeologie",
                                           "test")
                                           #"dev")
#INIST_ARCHEOLOGIE_CORPUS_DOCS = path.join(INIST_CORPUS_DIR,
#                                           "archeologie",
#                                           "train")
INIST_ARCHEOLOGIE_CORPUS_TRAIN_DOCS = path.join(INIST_CORPUS_DIR,
                                                 "archeologie",
                                                 "train")
INIST_ARCHEOLOGIE_CORPUS_REFS = path.join(INIST_CORPUS_DIR,
                                          "archeologie",
                                          "ref")
                                          #"ref_dev")
#INIST_ARCHEOLOGIE_CORPUS_REFS = path.join(INIST_CORPUS_DIR,
#                                          "archeologie",
#                                          "ref_train")
INIST_ARCHEOLOGIE_CORPUS_TRAIN_GRAPH = path.join(INIST_CORPUS_DIR,
                                                  "archeologie",
                                                  "train_model",
                                                  "model_intra_bi_occ.pickle")
INIST_ARCHEOLOGIE_CORPUS_TRAIN_MODEL = path.join(INIST_CORPUS_DIR,
                                                  "archeologie",
                                                  "train_model",
                                                  "model_extra.pickle")
INIST_ARCHEOLOGIE_CORPUS_TERM_SUITE_TERMINOLOGY = path.join(INIST_CORPUS_DIR, "archeologie", "termsuite_terminology.tsv")
INIST_ARCHEOLOGIE_CORPUS_TERM_SUITE_CLUSTERS = path.join(INIST_CORPUS_DIR, "archeologie", "termsuite_clusters.tsv")
#-------------------------------------------------------------------------------
INIST_CHIMIE_CORPUS_DOCS = path.join(INIST_CORPUS_DIR,
                                           "chimie",
                                           "test")
#INIST_CHIMIE_CORPUS_DOCS = path.join(INIST_CORPUS_DIR,
#                                           "chimie",
#                                           "train")
INIST_CHIMIE_CORPUS_TRAIN_DOCS = path.join(INIST_CORPUS_DIR,
                                                 "chimie",
                                                 "train")
INIST_CHIMIE_CORPUS_REFS = path.join(INIST_CORPUS_DIR,
                                          "chimie",
                                          "ref")
#INIST_CHIMIE_CORPUS_REFS = path.join(INIST_CORPUS_DIR,
#                                          "chimie",
#                                          "ref_train")
INIST_CHIMIE_CORPUS_TRAIN_GRAPH = path.join(INIST_CORPUS_DIR,
                                                  "chimie",
                                                  "train_model",
                                                  "model_intra_bi_occ.pickle")
INIST_CHIMIE_CORPUS_TRAIN_MODEL = path.join(INIST_CORPUS_DIR,
                                                  "chimie",
                                                  "train_model",
                                                  "model_extra.pickle")
INIST_CHIMIE_CORPUS_TERM_SUITE_TERMINOLOGY = path.join(INIST_CORPUS_DIR, "chimie", "termsuite_terminology.tsv")
INIST_CHIMIE_CORPUS_TERM_SUITE_CLUSTERS = path.join(INIST_CORPUS_DIR, "chimie", "termsuite_clusters.tsv")
#-------------------------------------------------------------------------------
INIST_SCIENCES_DE_L_INFORMATION_CORPUS_DOCS = path.join(INIST_CORPUS_DIR,
                                           "sciences_de_l_information",
                                           "test")
                                           #"dev")
#INIST_SCIENCES_DE_L_INFORMATION_CORPUS_DOCS = path.join(INIST_CORPUS_DIR,
#                                           "sciences_de_l_information",
#                                           "train")
INIST_SCIENCES_DE_L_INFORMATION_CORPUS_TRAIN_DOCS = path.join(INIST_CORPUS_DIR,
                                                 "sciences_de_l_information",
                                                 "train")
INIST_SCIENCES_DE_L_INFORMATION_CORPUS_REFS = path.join(INIST_CORPUS_DIR,
                                          "sciences_de_l_information",
                                          "ref")
                                          #"ref_dev")
#INIST_SCIENCES_DE_L_INFORMATION_CORPUS_REFS = path.join(INIST_CORPUS_DIR,
#                                          "sciences_de_l_information",
#                                          "ref_train")
INIST_SCIENCES_DE_L_INFORMATION_CORPUS_TRAIN_GRAPH = path.join(INIST_CORPUS_DIR,
                                                  "sciences_de_l_information",
                                                  "train_model",
                                                  "model_intra_bi_occ.pickle")
INIST_SCIENCES_DE_L_INFORMATION_CORPUS_TRAIN_MODEL = path.join(INIST_CORPUS_DIR,
                                                  "sciences_de_l_information",
                                                  "train_model",
                                                  "model_extra.pickle")
INIST_SCIENCES_DE_L_INFORMATION_CORPUS_TERM_SUITE_TERMINOLOGY = path.join(INIST_CORPUS_DIR, "sciences_de_l_information", "termsuite_terminology.tsv")
INIST_SCIENCES_DE_L_INFORMATION_CORPUS_TERM_SUITE_CLUSTERS = path.join(INIST_CORPUS_DIR, "sciences_de_l_information", "termsuite_clusters.tsv")

FRENCH_LA = "fr"
FRENCH_STOP_WORDS_FILEPATH = path.join(CORPORA_DIR, "french_unine_stop_words")
ENGLISH_LA = "en"
ENGLISH_STOP_WORDS_FILEPATH = path.join(CORPORA_DIR, "english_unine_stop_words")

##### execution configurations #################################################

LAZY_PRE_PROCESSING = True
LAZY_CANDIDATE_EXTRACTION = True
LAZY_CANDIDATE_CLUSTERING = True
LAZY_RANKING = False
LAZY_SELECTION = False

##### runs possibilities #######################################################

# corpora names
DEFT_CO = "deft"
WIKINEWS_CO = "wikinews"
SEMEVAL_CO = "semeval"
DUC_CO = "duc"
INSPEC_CO = "inspec"
LINGUISTIQUE_CO = "inist_linguistique"
ARCHEOLOGIE_CO = "inist_archeologie"
CHIMIE_CO = "inist_chimie"
SCIENCES_DE_L_INFORMATION_CO = "inist_sciences_de_l_information"

# method names
TFIDF_ME = "tfidf"
TEXTRANK_ME = "textrank"
SINGLERANK_ME = "singlerank"
COMPLETERANK_ME = "completerank"
TOPICRANK_S_ME = "topicrank_s"
TOPICRANK_ME = "topicrank"
KEA_ME = "kea"
TOPICRANK_PP_ME = "topicrank_pp" # TODO

# candidate names
ST_FILTERED_NGRAM_CA = "st_filtered_ngram"
NP_CHUNK_CA = "np_chunk"
LONGEST_NOUN_PHRASE_CA = "longest_noun_phrase"
BEST_PATTERN_CA = "best_pattern"
CLARIT96_CA = "clarit96"
TERM_SUITE_TERMINOLOGY_CA = "term_suite"
ACABIT_TERMINOLOGY_CA = "acabit"
POS_BOUNDARY_BASED_CA = "pos_boundaries"
CORE_WORD_BASED_CA = "core_words"
NOUN_AND_ADJR_CA = "nouns_and_adjr"

# clustering names
NO_CLUSTER_CC = "no_cluster"
HIERARCHICAL_CLUSTER_CC = "hierarchical"
TERM_VARIANT_CLUSTER_CC = "term_variant_cluster"

# scoring names
SUM_SC = "sum"
WEIGHT_SC = "weight"

# selection names
WHOLE_SE = "whole"
TOP_K_SE = "top_k"
TEXTRANK_SE = "textrank"

##### runs #####################################################################

#CORPORA_RU = [LINGUISTIQUE_CO, ARCHEOLOGIE_CO, SCIENCES_DE_L_INFORMATION_CO, CHIMIE_CO]
CORPORA_RU = [DUC_CO]#LINGUISTIQUE_CO, SCIENCES_DE_L_INFORMATION_CO, ARCHEOLOGIE_CO]
METHODS_RU = [TOPICRANK_PP_ME]
NUMBERS_RU = [1, 2, 3, 4, 5, 6, 7, 8, 9] # Lambdat_k
LENGTHS_RU = [1, 2, 3, 4, 5, 6, 7, 8, 9] # Lambda_t
CANDIDATES_RU = [LONGEST_NOUN_PHRASE_CA]
CLUSTERING_RU = [HIERARCHICAL_CLUSTER_CC]
SCORINGS_RU = [WEIGHT_SC]
SELECTIONS_RU = [WHOLE_SE]

# used for the noun phrases extraction
NOUN_TAGS = ["nn", "nns", "nnp", "nnps", "nc", "npp"]
ADJ_TAGS = ["jj", "adj"]
VERB_TAGS = ["vb", "vbd", "vbg", "vbn", "vbp", "vbz", "v", "vimp", "vinf", "vpp", "vpr", "vs"]
# used for tokens filtering in ****Rank methods
TEXTRANK_TAGS = ["nn", "nns", "nnp", "nnps", "jj", "nc", "npp", "adj"]
# rules for NP chunking
english_np_chunk_rules = "{(<nnps|nnp>+)|(<jj>+<nns|nn>)|(<nns|nn>+)}"
french_np_chunk_rules = "{(<npp>+)|(<adj>?<nc><adj>+)|(<adj><nc>)|(<nc>+)}"
# rules for pattern matching
tagged_word_pattern = "([^ ]+\\/%s( |$))" # WARNING space or end line delimiter is in the pattern
english_lnp_tags = "(jj|nnps|nnp|nns|nn)"
french_lnp_tags = "(adj|npp|nc)"
english_n_tags = "(nnps|nnp|nns|nn)"
french_n_tags = "(npp|nc)"
english_a_tags = "(jj)"
french_a_tags = "(adj)"
french_p_tags = "(p)"
french_d_tags = "(det)"
english_lnp_patterns = ["%s+"%(tagged_word_pattern%english_lnp_tags)]
french_lnp_patterns = ["%s+"%(tagged_word_pattern%french_lnp_tags)]
english_na_patterns = ["%s?%s+"%(tagged_word_pattern%english_a_tags,
                                 tagged_word_pattern%english_n_tags)]
french_na_patterns = ["%s+%s?"%(tagged_word_pattern%french_n_tags,
                                tagged_word_pattern%french_a_tags)]#,
                      #"%s((%s%s)|(%s))?%s"%(tagged_word_pattern%french_n_tags,
                      #             tagged_word_pattern%french_p_tags,
                      #             tagged_word_pattern%french_d_tags,
                      #             tagged_word_pattern%"(p+d)",
                      #             tagged_word_pattern%french_n_tags)]
# rules for CLARIT'96 subcompounding
english_clarit_np_patterns = english_lnp_patterns
french_clarit_np_patterns = french_lnp_patterns
english_clarit_lexatom_patterns = [
  "%s%s"%(tagged_word_pattern%("(nnps|nnp|nns|nn|%s)"%CLARIT96_LEXATOM_TAG),
          tagged_word_pattern%("(nnps|nnp|nns|nn|%s)"%CLARIT96_LEXATOM_TAG)),
  "%s%s"%(tagged_word_pattern%"(jjr|jjs|jj)",
          tagged_word_pattern%("(nnps|nnp|nns|nn|%s)"%CLARIT96_LEXATOM_TAG))
]
french_clarit_lexatom_patterns = [
  "%s%s"%(tagged_word_pattern%("(nc|npp|%s)"%CLARIT96_LEXATOM_TAG),
          tagged_word_pattern%"(adj)")
]
english_clarit_special_patterns = [
  "%s%s"%(tagged_word_pattern%"(rbr|rbs|rb)",
          tagged_word_pattern%"(rbr|rbs|rb|jjr|jjs|jj|vbg|vbn)")
]
french_clarit_special_patterns = [
  "%s%s"%(tagged_word_pattern%"(advwh|adv|adjwh|adj|vpp|vpr)",
          tagged_word_pattern%"(advwh|adv|adjwh|adj|vpp|vpr)")
]
english_clarit_impossible_patterns = [
  "%s%s"%(tagged_word_pattern%"(nnps|nnp|nns|nn|vpp|vpr)",
          tagged_word_pattern%"(rbr|rbs|rb|jjr|jjs|jj)"),
  "%s%s"%(tagged_word_pattern%"(jjr|jjs|jj)",
          tagged_word_pattern%"(jjr|jjs|jj)")
]
french_clarit_impossible_patterns = [
  "%s%s"%(tagged_word_pattern%"(advwh|adv)",
          tagged_word_pattern%"(npp|nc)"),
  "%s%s"%(tagged_word_pattern%"(adjwh|adj)",
          tagged_word_pattern%"(advwh|adv|adjwh|adj)")]
english_pos_boundaries = {
  "cc": ["for", "or", "and"],
  "dt": [],
  "ex": [],
  "fw": [],
  "in": ["of"],
  "jjr": [],
  "jjs": [],
  "ls": [],
  "md": [],
  "pdt": [],
  "pos": [],
  "prp": [],
  "prp$": [],
  "rb": [],
  "rbr": [],
  "rbs": [],
  "rp": [],
  "to": [],
  "uh": [],
  "vb": [],
  "vbd": [],
  "vbg": [],
  "vbn": [],
  "vbp": [],
  "vbz": [],
  "wdt": [],
  "wp": [],
  "wp$": [],
  "wrb": [],
  #"cd": [],
  #"sym": [],
  "''": [],
  "``": [],
  "\"": [],
  ")": [],
  "(": [],
  "]": [],
  "[": [],
  "}": [],
  "{": [],
  ",": [],
  ":": [],
  "...": [],
  ".": [],
  "!": [],
  "?": [],
  "punct": []
}
# TODO
french_pos_boundaries = {
}

################################################################################

def extract_stop_words(stop_words_filepath):
  st_file = codecs.open(stop_words_filepath, "r", "utf-8")
  stop_words = st_file.read().split("\n")

  st_file.close()

  for i, st in enumerate(stop_words):
    stop_words[i] = st.replace("\r", "")

  stop_words.append(",")
  stop_words.append(".")
  stop_words.append("!")
  stop_words.append("?")
  # NEWLY ADDED
  stop_words.append("]")
  stop_words.append("[")
  stop_words.append("=")
  stop_words.append("..")
  stop_words.append("...")
  stop_words.append(";")
  stop_words.append("(")
  stop_words.append(")")
  stop_words.append(":")

  return stop_words

def english_tokenization(term):
  word_tokenizer = TreebankWordTokenizer()
  tokenized_term = ""

  for word in word_tokenizer.tokenize(term):
    if tokenized_term != "":
      tokenized_term += " "
    tokenized_term += word

  return tokenized_term

def is_french_adjr(word): # TODO change adjr tests
  stemmer = FrenchStemmer()
  # suffixes with gender and number flexions
  suffixes = [
    u"ain", u"ains", u"aine", u"aines",
    u"aire", u"aires",
    u"al", u"aux", u"als", u"ale", u"ales",
    u"el", u"els", u"elle", u"elles",
    u"esque", u"esques",
    u"estre", u"estres",
    u"eux", u"euse", u"euses",
    u"é", u"és", u"ée", u"ées",
    u"ien", u"iens", u"ienne", u"iennes",
    u"ier", u"iers", u"ière", u"ières",
    u"if", u"ifs", u"ive", u"ives",
    u"il", u"ils",
    u"in", u"ins", u"ine", u"ines",
    u"ique", u"iques",
    u"ois", u"oise", u"oises"
  ]
  stem = stemmer.stem(word)
  stem_ending = ""
  if word.replace(u"é", "e").replace(u"è", "e").startswith(stem.replace(u"é", "e").replace(u"è", "e")):
    stem_ending = word.replace(u"é", "e").replace(u"è", "e").split(stem.replace(u"é", "e").replace(u"è", "e"), 1)[1]

  if stem in french_stemmed_adjr:
    return True
  for suffix in suffixes:
    if word[-len(suffix):] == suffix:
      return True
  # TODO change adjr tests
  #if stem_ending in french_adjr_stem_ending_counts:
  #  return True
  return False

def is_english_adjr(word): # TODO change adjr tests
  stemmer = PorterStemmer()
  suffixes = [
    u"al",
    u"ant",
    u"ary",
    u"ic",
    u"ous",
    u"ive"
  ]
  stem = stemmer.stem(word)
  stem_ending = ""
  if word.startswith(stem):
    stem_ending = word.split(stem, 1)[1]

  if stem in english_stemmed_adjr:
    return True
  for suffix in suffixes:
    if word[-len(suffix):] == suffix:
      return True
  # TODO change adjr tests
  #if stem_ending in english_adjr_stem_ending_counts:
  #  return True
  return False

def learn_tag_sequences(train_docs,
                        ext,
                        pre_processor,
                        tokenize):
  tag_sequences = {}

  # FIXME not needed when candidates are extracted
  for filename in listdir(train_docs):
    if filename.rfind(ext) >= 0 \
       and len(filename) - filename.rfind(ext) == len(ext):
      filepath = path.join(train_docs, filename)
      keyphrase_path = path.join(train_docs, filename.replace(ext, ".key"))
      pre_processed_file = pre_processor.pre_process_file(filepath)
      sentences = pre_processed_file.full_text()
      keyphrase_file = codecs.open(keyphrase_path,
                                   "r",
                                   pre_processed_file.encoding())
      keyphrases = keyphrase_file.read().split(";")
      tokenized_keyphrases = {}

      # tokenize keyphrases
      for keyphrase in keyphrases:
        tokenized_keyphrases[tokenize(keyphrase.lower().strip())] = True

      # parse n-grams
      for sentence in sentences:
        sentence = sentence.strip()

        for tagged_candidate in n_to_m_grams(sentence.split(), 1, len(sentence.split())):
          untagged_candidate = ""
          tag_sequence = ""

          for wt in tagged_candidate.split():
            if untagged_candidate != "":
              untagged_candidate += " "
            untagged_candidate += wt.rsplit(pre_processed_file.tag_separator(),
                                            1)[0]

            if tag_sequence != "":
              tag_sequence += " "
            tag_sequence += wt.rsplit(pre_processed_file.tag_separator(), 1)[1]

          # add tag sequence if it is a keyphrase
          if untagged_candidate in tokenized_keyphrases:
            tag_sequences[tag_sequence] = True

      keyphrase_file.close()

  return tag_sequences

################################################################################
# Main
################################################################################

def main(argv):
  runs = [
    # documents directory,
    # documents extension,
    # pre-processor,
    # candidate extractor,
    # candidate clusterer,
    # ranker,
    # selector,
    # evaluator
  ]

  ##### runs' creation #########################################################

  # lazy loading of idfs
  for corpus in CORPORA_RU:
    for method in METHODS_RU:
      for number in NUMBERS_RU:
        for length in LENGTHS_RU:
          docs = None
          ext = None
          term_suite_terms = None
          term_suite_clusters = None
          acabit_terms = None
          train_docs = None
          refs = None
          stop_words = None
          stemmer = None
          ref_stemmer = None
          tokenize = None
          pre_processor = None
          language = None
          dfs = None
          nb_documents = None
          np_chunk_rules = None
          lnp_patterns = None
          na_patterns = None
          is_adjr_function = None
          clarit_np_patterns = None
          clarit_lexatom_patterns = None
          clarit_special_patterns = None
          clarit_impossible_patterns = None
          pos_boundaries = None
          domain_graph_filepath = None
          domain_model_filepath = None

          if corpus == DEFT_CO:
            docs = DEFT_CORPUS_DOCS
            ext = DEFT_CORPUS_DOCS_EXTENSION
            term_suite_terms = DEFT_CORPUS_TERM_SUITE_TERMINOLOGY
            term_suite_clusters = DEFT_CORPUS_TERM_SUITE_CLUSTERS
            acabit_terms = DEFT_CORPUS_ACABIT_TERMINOLOGY
            train_docs = DEFT_CORPUS_TRAIN_DOCS
            refs = DEFT_CORPUS_REFS
            stop_words = extract_stop_words(FRENCH_STOP_WORDS_FILEPATH)
            stemmer = FrenchStemmer()
            ref_stemmer = stemmer
            tokenize = bonsai_tokenization
            pre_processor = FrenchPreProcessor("%s_pre_processor"%corpus,
                                               LAZY_PRE_PROCESSING,
                                               RUNS_DIR,
                                               True,
                                               DEFTFileRep())
            language = FRENCH_LA
            np_chunk_rules = french_np_chunk_rules
            lnp_patterns = french_lnp_patterns
            na_patterns = french_na_patterns
            is_adjr_function = is_french_adjr
            clarit_np_patterns = french_clarit_np_patterns
            clarit_lexatom_patterns = french_clarit_lexatom_patterns
            clarit_special_patterns = french_clarit_special_patterns
            clarit_impossible_patterns = french_clarit_impossible_patterns
            pos_boundaries = french_pos_boundaries
          else:
            if corpus == WIKINEWS_CO:
              docs = WIKINEWS_CORPUS_DOCS
              train_docs = docs # FIXME
              ext = WIKINEWS_CORPUS_DOCS_EXTENSION
              refs = WIKINEWS_CORPUS_REFS
              stop_words = extract_stop_words(FRENCH_STOP_WORDS_FILEPATH)
              stemmer = FrenchStemmer()
              ref_stemmer = stemmer
              tokenize = bonsai_tokenization
              pre_processor = FrenchPreProcessor("%s_pre_processor"%corpus,
                                                 LAZY_PRE_PROCESSING,
                                                 RUNS_DIR,
                                                 True,
                                                 WikiNewsFileRep())
              language = FRENCH_LA
              np_chunk_rules = french_np_chunk_rules
              lnp_patterns = french_lnp_patterns
              na_patterns = french_na_patterns
              is_adjr_function = is_french_adjr
              clarit_np_patterns = french_clarit_np_patterns
              clarit_lexatom_patterns = french_clarit_lexatom_patterns
              clarit_special_patterns = french_clarit_special_patterns
              clarit_impossible_patterns = french_clarit_impossible_patterns
              pos_boundaries = french_pos_boundaries
            else:
              if corpus == SEMEVAL_CO:
                docs = SEMEVAL_CORPUS_DOCS
                ext = SEMEVAL_CORPUS_DOCS_EXTENSION
                term_suite_terms = SEMEVAL_CORPUS_TERM_SUITE_TERMINOLOGY
                term_suite_clusters = SEMEVAL_CORPUS_TERM_SUITE_CLUSTERS
                acabit_terms = SEMEVAL_CORPUS_ACABIT_TERMINOLOGY
                train_docs = SEMEVAL_CORPUS_TRAIN_DOCS
                refs = SEMEVAL_CORPUS_REFS
                stop_words = extract_stop_words(ENGLISH_STOP_WORDS_FILEPATH)
                stemmer = PorterStemmer()
                ref_stemmer = None
                tokenize = english_tokenization
                pre_processor = EnglishPreProcessor("%s_pre_processor"%corpus,
                                                    LAZY_PRE_PROCESSING,
                                                    RUNS_DIR,
                                                    True,
                                                    "/",
                                                    SemEvalFileRep())
                language = ENGLISH_LA
                np_chunk_rules = english_np_chunk_rules
                lnp_patterns = english_lnp_patterns
                na_patterns = english_na_patterns
                is_adjr_function = is_english_adjr
                clarit_np_patterns = english_clarit_np_patterns
                clarit_lexatom_patterns = english_clarit_lexatom_patterns
                clarit_special_patterns = english_clarit_special_patterns
                clarit_impossible_patterns = english_clarit_impossible_patterns
                pos_boundaries = english_pos_boundaries
                domain_graph_filepath = SEMEVAL_CORPUS_TRAIN_GRAPH
                domain_model_filepath = SEMEVAL_CORPUS_TRAIN_MODEL
                domain_graph_filepath_c = path.join(path.split(SEMEVAL_CORPUS_TRAIN_GRAPH)[0],
                                                    "c",
                                                    path.split(SEMEVAL_CORPUS_TRAIN_GRAPH)[1])
                domain_model_filepath_c = path.join(path.split(SEMEVAL_CORPUS_TRAIN_MODEL)[0],
                                                    "c",
                                                    path.split(SEMEVAL_CORPUS_TRAIN_MODEL)[1])
                domain_graph_filepath_h = path.join(path.split(SEMEVAL_CORPUS_TRAIN_GRAPH)[0],
                                                    "h",
                                                    path.split(SEMEVAL_CORPUS_TRAIN_GRAPH)[1])
                domain_model_filepath_h = path.join(path.split(SEMEVAL_CORPUS_TRAIN_MODEL)[0],
                                                    "h",
                                                    path.split(SEMEVAL_CORPUS_TRAIN_MODEL)[1])
                domain_graph_filepath_i = path.join(path.split(SEMEVAL_CORPUS_TRAIN_GRAPH)[0],
                                                    "i",
                                                    path.split(SEMEVAL_CORPUS_TRAIN_GRAPH)[1])
                domain_model_filepath_i = path.join(path.split(SEMEVAL_CORPUS_TRAIN_MODEL)[0],
                                                    "i",
                                                    path.split(SEMEVAL_CORPUS_TRAIN_MODEL)[1])
                domain_graph_filepath_j = path.join(path.split(SEMEVAL_CORPUS_TRAIN_GRAPH)[0],
                                                    "j",
                                                    path.split(SEMEVAL_CORPUS_TRAIN_GRAPH)[1])
                domain_model_filepath_j = path.join(path.split(SEMEVAL_CORPUS_TRAIN_MODEL)[0],
                                                    "j",
                                                    path.split(SEMEVAL_CORPUS_TRAIN_MODEL)[1])
              else:
                if corpus == DUC_CO:
                  docs = DUC_CORPUS_DOCS
                  ext = DUC_CORPUS_DOCS_EXTENSION
                  term_suite_terms = DUC_CORPUS_TERM_SUITE_TERMINOLOGY
                  term_suite_clusters = DUC_CORPUS_TERM_SUITE_CLUSTERS
                  acabit_terms = DUC_CORPUS_ACABIT_TERMINOLOGY
                  train_docs = DUC_CORPUS_TRAIN_DOCS
                  refs = DUC_CORPUS_REFS
                  stop_words = extract_stop_words(ENGLISH_STOP_WORDS_FILEPATH)
                  stemmer = PorterStemmer()
                  ref_stemmer = PorterStemmer()
                  tokenize = english_tokenization
                  pre_processor = EnglishPreProcessor("%s_pre_processor"%corpus,
                                                      LAZY_PRE_PROCESSING,
                                                      RUNS_DIR,
                                                      True,
                                                      "/",
                                                      DUCFileRep())
                  language = ENGLISH_LA
                  np_chunk_rules = english_np_chunk_rules
                  lnp_patterns = english_lnp_patterns
                  na_patterns = english_na_patterns
                  is_adjr_function = is_english_adjr
                  clarit_np_patterns = english_clarit_np_patterns
                  clarit_lexatom_patterns = english_clarit_lexatom_patterns
                  clarit_special_patterns = english_clarit_special_patterns
                  clarit_impossible_patterns = english_clarit_impossible_patterns
                  pos_boundaries = english_pos_boundaries
                  domain_graph_filepath = DUC_CORPUS_TRAIN_GRAPH
                  domain_model_filepath = DUC_CORPUS_TRAIN_MODEL
                else:
                  if corpus == INSPEC_CO:
                    docs = INSPEC_CORPUS_DOCS
                    ext = INSPEC_CORPUS_DOCS_EXTENSION
                    train_docs = INSPEC_CORPUS_TRAIN_DOCS
                    refs = INSPEC_CORPUS_REFS
                    stop_words = extract_stop_words(ENGLISH_STOP_WORDS_FILEPATH)
                    stemmer = PorterStemmer()
                    ref_stemmer = stemmer
                    tokenize = english_tokenization
                    pre_processor = EnglishPreProcessor("%s_pre_processor"%corpus,
                                                        LAZY_PRE_PROCESSING,
                                                        RUNS_DIR,
                                                        True,
                                                        "/",
                                                        InspecFileRep())
                    language = ENGLISH_LA
                    np_chunk_rules = english_np_chunk_rules
                    lnp_patterns = english_lnp_patterns
                    na_patterns = english_na_patterns
                    is_adjr_function = is_english_adjr
                    clarit_np_patterns = english_clarit_np_patterns
                    clarit_lexatom_patterns = english_clarit_lexatom_patterns
                    clarit_special_patterns = english_clarit_special_patterns
                    clarit_impossible_patterns = english_clarit_impossible_patterns
                    pos_boundaries = english_pos_boundaries
                    domain_graph_filepath = INSPEC_CORPUS_TRAIN_GRAPH
                    domain_model_filepath = INSPEC_CORPUS_TRAIN_MODEL
                  elif corpus == LINGUISTIQUE_CO:
                    docs = INIST_LINGUISTIQUE_CORPUS_DOCS
                    ext = INIST_CORPUS_DOCS_EXTENSION
                    train_docs = INIST_LINGUISTIQUE_CORPUS_TRAIN_DOCS
                    refs = INIST_LINGUISTIQUE_CORPUS_REFS
                    term_suite_terms = INIST_LINGUISTIQUE_CORPUS_TERM_SUITE_TERMINOLOGY
                    term_suite_clusters = INIST_LINGUISTIQUE_CORPUS_TERM_SUITE_CLUSTERS
                    stop_words = extract_stop_words(FRENCH_STOP_WORDS_FILEPATH)
                    stemmer = FrenchStemmer()
                    ref_stemmer = stemmer
                    tokenize = bonsai_tokenization
                    pre_processor = FrenchPreProcessor("%s_pre_processor"%corpus,
                                                       LAZY_PRE_PROCESSING,
                                                       RUNS_DIR,
                                                       True,
                                                       INISTFileRep())
                    language = FRENCH_LA
                    np_chunk_rules = french_np_chunk_rules
                    lnp_patterns = french_lnp_patterns
                    na_patterns = french_na_patterns
                    is_adjr_function = is_french_adjr
                    domain_graph_filepath = INIST_LINGUISTIQUE_CORPUS_TRAIN_GRAPH
                    domain_model_filepath = INIST_LINGUISTIQUE_CORPUS_TRAIN_MODEL
                  elif corpus == ARCHEOLOGIE_CO:
                    docs = INIST_ARCHEOLOGIE_CORPUS_DOCS
                    ext = INIST_CORPUS_DOCS_EXTENSION
                    train_docs = INIST_ARCHEOLOGIE_CORPUS_TRAIN_DOCS
                    refs = INIST_ARCHEOLOGIE_CORPUS_REFS
                    term_suite_terms = INIST_ARCHEOLOGIE_CORPUS_TERM_SUITE_TERMINOLOGY
                    term_suite_clusters = INIST_ARCHEOLOGIE_CORPUS_TERM_SUITE_CLUSTERS
                    stop_words = extract_stop_words(FRENCH_STOP_WORDS_FILEPATH)
                    stemmer = FrenchStemmer()
                    ref_stemmer = stemmer
                    tokenize = bonsai_tokenization
                    pre_processor = FrenchPreProcessor("%s_pre_processor"%corpus,
                                                       LAZY_PRE_PROCESSING,
                                                       RUNS_DIR,
                                                       True,
                                                       INISTFileRep())
                    language = FRENCH_LA
                    np_chunk_rules = french_np_chunk_rules
                    lnp_patterns = french_lnp_patterns
                    na_patterns = french_na_patterns
                    is_adjr_function = is_french_adjr
                    domain_graph_filepath = INIST_ARCHEOLOGIE_CORPUS_TRAIN_GRAPH
                    domain_model_filepath = INIST_ARCHEOLOGIE_CORPUS_TRAIN_MODEL
                  elif corpus == CHIMIE_CO:
                    docs = INIST_CHIMIE_CORPUS_DOCS
                    ext = INIST_CORPUS_DOCS_EXTENSION
                    train_docs = INIST_CHIMIE_CORPUS_TRAIN_DOCS
                    refs = INIST_CHIMIE_CORPUS_REFS
                    term_suite_terms = INIST_CHIMIE_CORPUS_TERM_SUITE_TERMINOLOGY
                    term_suite_clusters = INIST_CHIMIE_CORPUS_TERM_SUITE_CLUSTERS
                    stop_words = extract_stop_words(FRENCH_STOP_WORDS_FILEPATH)
                    stemmer = FrenchStemmer()
                    ref_stemmer = stemmer
                    tokenize = bonsai_tokenization
                    pre_processor = FrenchPreProcessor("%s_pre_processor"%corpus,
                                                       LAZY_PRE_PROCESSING,
                                                       RUNS_DIR,
                                                       True,
                                                       INISTFileRep())
                    language = FRENCH_LA
                    np_chunk_rules = french_np_chunk_rules
                    lnp_patterns = french_lnp_patterns
                    na_patterns = french_na_patterns
                    is_adjr_function = is_french_adjr
                    domain_graph_filepath = INIST_CHIMIE_CORPUS_TRAIN_GRAPH
                    domain_model_filepath = INIST_CHIMIE_CORPUS_TRAIN_MODEL
                  elif corpus == SCIENCES_DE_L_INFORMATION_CO:
                    docs = INIST_SCIENCES_DE_L_INFORMATION_CORPUS_DOCS
                    ext = INIST_CORPUS_DOCS_EXTENSION
                    train_docs = INIST_SCIENCES_DE_L_INFORMATION_CORPUS_TRAIN_DOCS
                    refs = INIST_SCIENCES_DE_L_INFORMATION_CORPUS_REFS
                    term_suite_terms = INIST_SCIENCES_DE_L_INFORMATION_CORPUS_TERM_SUITE_TERMINOLOGY
                    term_suite_clusters = INIST_SCIENCES_DE_L_INFORMATION_CORPUS_TERM_SUITE_CLUSTERS
                    stop_words = extract_stop_words(FRENCH_STOP_WORDS_FILEPATH)
                    stemmer = FrenchStemmer()
                    ref_stemmer = stemmer
                    tokenize = bonsai_tokenization
                    pre_processor = FrenchPreProcessor("%s_pre_processor"%corpus,
                                                       LAZY_PRE_PROCESSING,
                                                       RUNS_DIR,
                                                       True,
                                                       INISTFileRep())
                    language = FRENCH_LA
                    np_chunk_rules = french_np_chunk_rules
                    lnp_patterns = french_lnp_patterns
                    na_patterns = french_na_patterns
                    is_adjr_function = is_french_adjr
                    domain_graph_filepath = INIST_SCIENCES_DE_L_INFORMATION_CORPUS_TRAIN_GRAPH
                    domain_model_filepath = INIST_SCIENCES_DE_L_INFORMATION_CORPUS_TRAIN_MODEL

          for candidate in CANDIDATES_RU:
            for cluster in CLUSTERING_RU:
              for scoring in SCORINGS_RU:
                for selection in SELECTIONS_RU:
                  run_name = "%s_%s_%d_%d_%s_%s_%s_%s"%(corpus,
                                                        method,
                                                        number,
                                                        length,
                                                        candidate,
                                                        cluster,
                                                        scoring,
                                                        selection)
                  c = None # candidate_extractor
                  cc = None # candidate_clusterer
                  r = None # ranker
                  s = None # selector
                  e = None # evaluator

                  ##### candidate extractor ####################################
                  if candidate == ST_FILTERED_NGRAM_CA:
                      c = STFilteredNGramExtractor(run_name,
                                                   LAZY_CANDIDATE_EXTRACTION,
                                                   RUNS_DIR,
                                                   True,
                                                   length,
                                                   stop_words)
                  else:
                    if candidate == LONGEST_NOUN_PHRASE_CA:
                      c = PatternMatchingExtractor(run_name,
                                                   LAZY_CANDIDATE_EXTRACTION,
                                                   RUNS_DIR,
                                                   True,
                                                   lnp_patterns)
                    else:
                      if candidate == BEST_PATTERN_CA:
                        c = POSSequenceExtractor(run_name,
                                                 LAZY_CANDIDATE_EXTRACTION,
                                                 RUNS_DIR,
                                                 True,
                                                 learn_tag_sequences(train_docs,
                                                                     ext,
                                                                     pre_processor,
                                                                     tokenize),
                                                 stop_words)
                      else:
                        if candidate == NP_CHUNK_CA:
                          c = NPChunkExtractor(run_name,
                                               LAZY_CANDIDATE_EXTRACTION,
                                               RUNS_DIR,
                                               True,
                                               np_chunk_rules)
                        else:
                          if candidate == CLARIT96_CA:
                            c = CLARIT96Extractor(run_name,
                                                  LAZY_CANDIDATE_EXTRACTION,
                                                  RUNS_DIR,
                                                  True,
                                                  clarit_np_patterns,
                                                  clarit_lexatom_patterns,
                                                  clarit_special_patterns,
                                                  clarit_impossible_patterns,
                                                  train_clarit(train_docs,
                                                               ext,
                                                               pre_processor,
                                                               PatternMatchingExtractor(run_name + "_pre",
                                                                                        LAZY_CANDIDATE_EXTRACTION,
                                                                                        RUNS_DIR,
                                                                                        True,
                                                                                        clarit_np_patterns)))
                          else:
                            if candidate == TERM_SUITE_TERMINOLOGY_CA:
                              c = FromTerminologyExtractor(run_name,
                                                           LAZY_CANDIDATE_EXTRACTION,
                                                           RUNS_DIR,
                                                           True,
                                                           term_suite_terms,
                                                           "utf-8", # FIXME
                                                           tokenize)
                            else:
                              if candidate == ACABIT_TERMINOLOGY_CA:
                                c = FromTerminologyExtractor(run_name,
                                                             LAZY_CANDIDATE_EXTRACTION,
                                                             RUNS_DIR,
                                                             True,
                                                             acabit_terms,
                                                             "utf-8", # FIXME
                                                             tokenize)
                              else:
                                if candidate == POS_BOUNDARY_BASED_CA:
                                  c = POSBoundaryBasedCandidateExtractor(run_name,
                                                                         LAZY_CANDIDATE_EXTRACTION,
                                                                         RUNS_DIR,
                                                                         True,
                                                                         pos_boundaries)
                                else:
                                  if candidate == CORE_WORD_BASED_CA:
                                      c = ExpandedCoreWordExtractor(run_name,
                                                                    LAZY_CANDIDATE_EXTRACTION,
                                                                    RUNS_DIR,
                                                                    True,
                                                                    stop_words,
                                                                    VERB_TAGS,
                                                                    stemmer)
                                  else:
                                    if candidate == NOUN_AND_ADJR_CA:
                                      c = NounAndADJRExtractor(run_name,
                                                               LAZY_CANDIDATE_EXTRACTION,
                                                               RUNS_DIR,
                                                               True,
                                                               na_patterns,
                                                               ADJ_TAGS,
                                                               is_adjr_function)
                  ##### candidate clusterer ####################################
                  if cluster == NO_CLUSTER_CC:
                    cc = FakeClusterer(run_name,
                                       LAZY_CANDIDATE_CLUSTERING,
                                       RUNS_DIR,
                                       True)
                  else:
                    if cluster == HIERARCHICAL_CLUSTER_CC:
                      cc = StemOverlapHierarchicalClusterer(run_name,
                                                            LAZY_CANDIDATE_CLUSTERING,
                                                            RUNS_DIR,
                                                            True,
                                                            LINKAGE_STRATEGY.AVERAGE,
                                                            0.25,
                                                            stemmer)
                    else:
                      if cluster == TERM_VARIANT_CLUSTER_CC:
                        cc = TermVariantClusterer(run_name,
                                                  LAZY_CANDIDATE_CLUSTERING,
                                                  RUNS_DIR,
                                                  True,
                                                  term_suite_clusters,
                                                  "utf-8",
                                                  tokenize)
                  ##### scoring ################################################
                  scoring_function = None
                  if scoring == SUM_SC:
                    scoring_function = term_scoring.sum
                  else:
                    if scoring == WEIGHT_SC:
                      if language == FRENCH_LA:
                        scoring_function = term_scoring.normalized_right_significance
                      else:
                        if language == ENGLISH_LA:
                            scoring_function = term_scoring.normalized
                  ##### ranker #################################################
                  if method == TFIDF_ME:
                    ##### DF computation ###################################
                    nb_documents, dfs = document_frequencies(train_docs,
                                                             ext,
                                                             # no candidate
                                                             # means word
                                                             # TF-IDF
                                                             pre_processor)#,
                                                             #c)
                    ############################################################
                    r = TFIDFRanker(run_name,
                                    LAZY_RANKING,
                                    RUNS_DIR,
                                    True,
                                    # no scoring function means n-gram TF-IDF
                                    dfs,
                                    nb_documents,
                                    scoring_function)
                  else:
                    if method == TEXTRANK_ME \
                       or method == SINGLERANK_ME \
                       or method == COMPLETERANK_ME \
                       or method == TOPICRANK_S_ME \
                       or method == TOPICRANK_ME:
                      strategy = None

                      if method == TEXTRANK_ME:
                        strategy = TextRankStrategy(2,
                                                    pre_processor.tag_separator(),
                                                    TEXTRANK_TAGS)
                      else:
                        if method == SINGLERANK_ME:
                          strategy = SingleRankStrategy(10,
                                                        pre_processor.tag_separator(),
                                                        TEXTRANK_TAGS)
                        else:
                          if method == COMPLETERANK_ME:
                            strategy = CompleteGraphStrategy(None,
                                                             pre_processor.tag_separator(),
                                                             TEXTRANK_TAGS)
                          else:
                            if method == TOPICRANK_S_ME \
                               or method == TOPICRANK_ME:
                              if method == TOPICRANK_S_ME:
                                sub_strategy = SingleRankStrategy(10,
                                                                  pre_processor.tag_separator(),
                                                                  TEXTRANK_TAGS)
                              if method == TOPICRANK_ME:
                                sub_strategy = CompleteGraphStrategy(None,
                                                                     pre_processor.tag_separator(),
                                                                     TEXTRANK_TAGS)
                              strategy = TopicRankStrategy(sub_strategy,
                                                           stemmer)
                      r =  TextRankRanker(run_name,
                                          LAZY_RANKING,
                                          RUNS_DIR,
                                          True,
                                          strategy,
                                          scoring_function)
                    elif method == TOPICRANK_PP_ME:
                      add_topicrankpp_graphs_and_models(corpus,
                                                        domain_graph_filepath,
                                                        domain_model_filepath,
                                                        stemmer)
                      if corpus == SEMEVAL_CO:
                        add_topicrankpp_graphs_and_models("%s#C"%(corpus),
                                                          domain_graph_filepath_c,
                                                          domain_model_filepath_c,
                                                          stemmer)
                        add_topicrankpp_graphs_and_models("%s#H"%(corpus),
                                                          domain_graph_filepath_h,
                                                          domain_model_filepath_h,
                                                          stemmer)
                        add_topicrankpp_graphs_and_models("%s#I"%(corpus),
                                                          domain_graph_filepath_i,
                                                          domain_model_filepath_i,
                                                          stemmer)
                        add_topicrankpp_graphs_and_models("%s#J"%(corpus),
                                                          domain_graph_filepath_j,
                                                          domain_model_filepath_j,
                                                          stemmer)
                      if corpus == DUC_CO:
                        train_graph_path = path.split(domain_graph_filepath)[0]
                        train_graph_name = path.split(domain_graph_filepath)[1]
                        train_model_path = path.split(domain_model_filepath)[0]
                        train_model_name = path.split(domain_model_filepath)[1]

                        for document_name in listdir(path.join(train_graph_path, "documents")):
                          graph_filepath = path.join(train_graph_path, "documents", document_name, train_graph_name)
                          model_filepath = path.join(train_model_path, "documents", document_name, train_model_name)
                          print "%s#%s"%(corpus, document_name)
                          print graph_filepath
                          print model_filepath
                          add_topicrankpp_graphs_and_models("%s#%s"%(corpus, document_name),
                                                            graph_filepath,
                                                            model_filepath,
                                                            stemmer)

                      r = TopicRankPPRanker(run_name,
                                            LAZY_RANKING,
                                            RUNS_DIR,
                                            True,
                                            corpus,
                                            False,  # use_proba
                                            False,  # oriented
                                            stemmer,
                                            lambda_k=float(number) / 10.0,
                                            lambda_t=float(length) / 10.0)
                                            #number) # number of controlled
                                            #float("inf"))#number, # number of controlled
                                                    # keyphrases to extract
                                            #recomendation_weight=float(length)/100.0)
                    else:
                      if method == KEA_ME:
                        kea_train_dir = path.join(RUNS_DIR, "kea_models")
                        if not path.exists(kea_train_dir):
                          makedirs(kea_train_dir)
                        # TF-IDFs are computed based on n-gram counts
                        train_nb_documents, train_dfs = document_frequencies(train_docs,
                                                                             ext,
                                                                             pre_processor,
                                                                             c)
                        train_tfidf_ranker = TFIDFRanker(run_name,
                                                         LAZY_RANKING,
                                                         RUNS_DIR,
                                                         True,
                                                         train_dfs,
                                                         train_nb_documents)
                        classifier = train_kea(path.join(kea_train_dir, "kea_model_%s"%run_name),
                                               train_docs,
                                               ext,
                                               ".key",
                                               tokenize,
                                               stemmer,
                                               pre_processor,
                                               c,
                                               cc,
                                               train_tfidf_ranker)
                        r = KEARanker(run_name,
                                      LAZY_RANKING,
                                      RUNS_DIR,
                                      True,
                                      classifier,
                                      train_tfidf_ranker)
                  ##### selector ###############################################
                  if selection == WHOLE_SE:
                    s = UnredundantWholeSelector(run_name,
                                                 LAZY_SELECTION,
                                                 RUNS_DIR,
                                                 True,
                                                 stemmer)
                  else:
                    if selection == TOP_K_SE:
                      s = UnredundantTopKSelector(run_name,
                                                  LAZY_SELECTION,
                                                  RUNS_DIR,
                                                  True,
                                                  number,
                                                  stemmer)
                    else:
                      if selection == TEXTRANK_SE:
                        s = UnredundantTextRankSelector(run_name,
                                                        LAZY_SELECTION,
                                                        RUNS_DIR,
                                                        True,
                                                        number,
                                                        stemmer)
                  ##### evaluator ##############################################
                  e = StandardPRFMEvaluator(run_name,
                                            RUNS_DIR,
                                            True,
                                            refs,
                                            pre_processor.encoding(),
                                            ref_stemmer,
                                            stemmer,
                                            tokenize)

                  runs.append(KeyphraseExtractor(docs,
                                                 ext,
                                                 pre_processor,
                                                 c,
                                                 cc,
                                                 r,
                                                 s,
                                                 e))

  ##### Runs' execution ########################################################

  print "EXECUTION OF %d RUNS..."%len(runs)
  queue = Queue()
  for run in runs:
    queue.put(run)
    KeyBenchWorker(queue).start()

################################################################################
if __name__ == "__main__":
  main(sys.argv)
################################################################################

