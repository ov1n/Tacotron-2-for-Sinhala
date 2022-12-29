""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
from unidecode import unidecode
from .numbers import normalize_numbers


# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\%s.' % x[0]), x[1]) for x in [
  ('පෙ.ව.', 'පෙරවරු'),
  ('ප.ව.', 'පස්වරු'),
  ('බු.ව', 'බුද්ධ වර්ෂ'),
  ('ක්‍රි.ව', 'ක්‍රිස්තු වර්ෂ'),
]]

_rupees_re = re.compile(r'රු.\s*([0-9\.\,]*[0-9]+)')
def _expand_rupees(m):
  match = m.group(1)
  parts = match.split('.')
  if len(parts)>2:
    return "රුපියල්" + match # Unexpected format
  
  rupees = int(parts[0]) if (parts[0]) else 0
  cents = int(parts[0]) if len(parts) > 1 and parts[1] else 0
  default = "යි"

  if rupees and cents:
    rupee_unit = "රුපියල්"
    cent_unit = "සත"

  return "%s %s %s %s" % (rupee_unit, rupees, default,cent_unit, cents)

def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def expand_numbers(text):
  return normalize_numbers(text)


def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
  return unidecode(text)


def basic_cleaners(text):
  '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def transliteration_cleaners(text):
  '''Pipeline for non-English text that transliterates to ASCII.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def english_cleaners(text):
  '''Pipeline for English text, including number and abbreviation expansion.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_numbers(text)
  text = expand_abbreviations(text)
  text = collapse_whitespace(text)
  return text

def return_text(text):
  return text