# -*- encoding: utf-8 -*-

class KBDocument(object):
  """A representation of a document.

  A read-only representation of a document. The document includes content
  information (language, encoding, etc.), segmented text (title, abstract and
  content) and linguistically processed text (sentence segmentation, word
  tokenization and Part-Of-Speech tagging).

  Attributes:
    corpus_name: The C{string} name of the corpus to which the document belongs
      to.
    filepath: The C{string} path of the file containing the document.
    name: The name (identifier) of the document.
    language: The C{string} name of the document's language (see
      C{keybench.main.language_support.KBLanguage}).
    encoding: The C{string} name of the document's encoding.
    title: The title of the document.
    abstract: The abstract of the document.
    content: The content of the document.
    title_sentences: The sentences of the title, as a C{list} of C{string}.
    abstract_sentences: The sentences of the abstract, as a C{list} of
      C{string}.
    content_sentences: The sentences of the content, as a C{list} of C{string}.
    title_sentence_tokens: The tokens of the tile sentences, as a C{list} of
      C{list} of C{string}.
    abstract_sentence_tokens: The tokens of the abstract sentences, as a C{list}
      of C{list} of C{string}.
    content_sentence_tokens: The tokens of the content sentences, as a C{list
      of C{list} of C{string}.
    title_normalized_tokens: The normalized tokens of the title sentences, as a
      C{list} of C{list} of C{string}.
    abstract_normalized_tokens: The normalized tokens of the abstract sentences,
      as a C{list} of C{list} of C{string}.
    content_normalized_tokens: The normalized tokens of the content sentences,
      as a C{list} of C{list} of C{string}.
    title_token_lemmas: The lemmas of the normalized tokens of the title
      sentences, as a C{list} of C{list} of C{string}.
    abstract_token_lemmas: The lemmas of the normalized tokens of the abstract
      sentences, as a C{list} of C{list} of C{string}.
    content_token_lemmas: The lemmas of the normalized tokens of the content
      sentences, as a C{list} of C{list} of C{string}.
    title_token_stems: The stems of the normalized tokens of the title
      sentences, as a C{list} of C{list} of C{string}.
    abstract_token_stems: The stems of the normalized tokens of the abstract
      sentences, as a C{list} of C{list} of C{string}.
    content_token_stems: The stems of the normalized tokens of the content
      sentences, as a C{list} of C{list} of C{string}.
    title_token_pos_tags: The POS tags of the tokens of the title sentences, as
      a C{list} of C{list} of C{string}.
    abstract_token_pos_tags: The POS tags of the tokens of the abstract
      sentences, as a C{list} of C{list} of C{string}.
    content_token_pos_tags: The POS tags of the tokens of the content sentences,
      as a C{list} of C{list} of C{string}.
    full_text: The concatenation of the title, the abstract and the content of
      the document.
    full_text_sentences: The concatenation of the sentences of the title, the
      abstract and the content.
    full_text_sentence_tokens: The concatenation of the tokens of the title, the
      abstract and the content.
    full_text_token_pos_tags: The concatenation of POS tags of the title, the
      abstract and the content.
  """

  def __init__(self,
               corpus_name,
               filepath,
               name,
               language,
               encoding,
               title,
               abstract,
               content,
               title_sentences,
               abstract_sentences,
               content_sentences,
               title_sentence_tokens,
               abstract_sentence_tokens,
               content_sentence_tokens,
               title_normalized_tokens,
               abstract_normalized_tokens,
               content_normalized_tokens,
               title_token_lemmas,
               abstract_token_lemmas,
               content_token_lemmas,
               title_token_stems,
               abstract_token_stems,
               content_token_stems,
               title_token_pos_tags,
               abstract_token_pos_tags,
               content_token_pos_tags):
    super(KBDocument, self).__init__()

    self._corpus_name = corpus_name
    self._filepath = filepath
    self._name = name
    self._language = language
    self._encoding = encoding
    self._title = title
    self._abstract = abstract
    self._content = content
    self._title_sentences = title_sentences
    self._abstract_sentences = abstract_sentences
    self._content_sentences = content_sentences
    self._title_sentence_tokens = title_sentence_tokens
    self._abstract_sentence_tokens = abstract_sentence_tokens
    self._content_sentence_tokens = content_sentence_tokens
    self._title_normalized_tokens = title_normalized_tokens
    self._abstract_normalized_tokens = abstract_normalized_tokens
    self._content_normalized_tokens = content_normalized_tokens
    self._title_token_lemmas = title_token_lemmas
    self._abstract_token_lemmas = abstract_token_lemmas
    self._content_token_lemmas = content_token_lemmas
    self._title_token_stems = title_token_stems
    self._abstract_token_stems = abstract_token_stems
    self._content_token_stems = content_token_stems
    self._title_token_pos_tags = title_token_pos_tags
    self._abstract_token_pos_tags = abstract_token_pos_tags
    self._content_token_pos_tags = content_token_pos_tags

  def __eq__(self, other):
    return self._corpus_name == other._corpus_name \
           and self._filepath == other._filepath \
           and self._name == other._name \
           and self._language == other._language \
           and self._encoding == other._encoding \
           and self._title == other._title \
           and self._abstract == other._abstract \
           and self._content == other._content \
           and self._title_sentences == other._title_sentences \
           and self._abstract_sentences == other._abstract_sentences \
           and self._content_sentences == other._content_sentences \
           and self._title_sentence_tokens == other._title_sentence_tokens \
           and self._abstract_sentence_tokens == other._abstract_sentence_tokens \
           and self._content_sentence_tokens == other._content_sentence_tokens \
           and self._title_normalized_tokens == other._title_normalized_tokens \
           and self._abstract_normalized_tokens == other._abstract_normalized_tokens \
           and self._content_normalized_tokens == other._content_normalized_tokens \
           and self._title_token_lemmas == other._title_token_lemmas \
           and self._abstract_token_lemmas == other._abstract_token_lemmas \
           and self._content_token_lemmas == other._content_token_lemmas \
           and self._title_token_stems == other._title_token_stems \
           and self._abstract_token_stems == other._abstract_token_stems \
           and self._content_token_stems == other._content_token_stems \
           and self._title_token_pos_tags == other._title_token_pos_tags \
           and self._abstract_token_pos_tags == other._abstract_token_pos_tags \
           and self._content_token_pos_tags == other._content_token_pos_tags

  def __ne__(self, other):
    return not self.__eq__(other)

  @property
  def corpus_name(self):
    return self._corpus_name

  @property
  def filepath(self):
    return self._filepath

  @property
  def name(self):
    return self._name

  @property
  def language(self):
    return self._language

  @property
  def encoding(self):
    return self._encoding

  @property
  def title(self):
    return self._title

  @property
  def abstract(self):
    return self._abstract

  @property
  def content(self):
    return self._content

  @property
  def title_sentences(self):
    return self._title_sentences

  @property
  def abstract_sentences(self):
    return self._abstract_sentences

  @property
  def content_sentences(self):
    return self._content_sentences

  @property
  def title_sentence_tokens(self):
    return self._title_sentence_tokens

  @property
  def abstract_sentence_tokens(self):
    return self._abstract_sentence_tokens

  @property
  def content_sentence_tokens(self):
    return self._content_sentence_tokens

  @property
  def title_normalized_tokens(self):
    return self._title_normalized_tokens

  @property
  def abstract_normalized_tokens(self):
    return self._abstract_normalized_tokens

  @property
  def content_normalized_tokens(self):
    return self._content_normalized_tokens

  @property
  def title_token_lemmas(self):
    return self._title_token_lemmas

  @property
  def abstract_token_lemmas(self):
    return self._abstract_token_lemmas

  @property
  def content_token_lemmas(self):
    return self._content_token_lemmas

  @property
  def title_token_stems(self):
    return self._title_token_stems

  @property
  def abstract_token_stems(self):
    return self._abstract_token_stems

  @property
  def content_token_stems(self):
    return self._content_token_stems

  @property
  def title_token_pos_tags(self):
    return self._title_token_pos_tags

  @property
  def abstract_token_pos_tags(self):
    return self._abstract_token_pos_tags

  @property
  def content_token_pos_tags(self):
    return self._content_token_pos_tags

  @property
  def full_text(self):
    return ("%s %s %s"%(self._title, self._abstract, self._content)).strip()

  @property
  def full_text_sentences(self):
    result = []
    
    result.extend(self._title_sentences)
    result.extend(self._abstract_sentences)
    result.extend(self.content_sentences)

    return result

  @property
  def full_text_sentence_tokens(self):
    result = []
    
    result.extend(self._title_sentence_tokens)
    result.extend(self._abstract_sentence_tokens)
    result.extend(self.content_sentence_tokens)

    return result

  @property
  def full_text_normalized_tokens(self):
    result = []
    
    result.extend(self._title_normalized_tokens)
    result.extend(self._abstract_normalized_tokens)
    result.extend(self.content_normalized_tokens)

    return result

  @property
  def full_text_token_lemmas(self):
    result = []
    
    result.extend(self._title_token_lemmas)
    result.extend(self._abstract_token_lemmas)
    result.extend(self.content_token_lemmas)

    return result

  @property
  def full_text_token_stems(self):
    result = []
    
    result.extend(self._title_token_stems)
    result.extend(self._abstract_token_stems)
    result.extend(self.content_token_stems)

    return result

  @property
  def full_text_token_pos_tags(self):
    result = []
    
    result.extend(self._title_token_pos_tags)
    result.extend(self._abstract_token_pos_tags)
    result.extend(self.content_token_pos_tags)

    return result

