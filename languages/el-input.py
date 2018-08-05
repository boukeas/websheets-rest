# -*- coding: utf-8 -*-
# $Id: el.py boukeas $
# Author: George Boukeas <boukeas@gmail.com>
# Copyright: This module has been placed in the public domain.

# New language mappings are welcome.  Before doing a new translation, please
# read <http://docutils.sf.net/docs/howto/i18n.html>.  Two files must be
# translated for each language: one in docutils/languages, the other in
# docutils/parsers/rst/languages.

"""
Greek-language mappings for language-dependent features of
reStructuredText.
"""

__docformat__ = 'reStructuredText'


directives = {
      # language-dependent: fixed
      'attention': 'προσοχή',
      'caution': 'προειδοποίηση',
      'code': 'κώδικας',
      'code-block': 'ενότητα-κώδικα',
      'sourcecode': 'πηγαίος-κώδικας',
      'danger': 'κίνδυνος',
      'error': 'σφάλμα',
      'hint': 'υπόδειξη',
      'important': 'σημαντικό',
      'note': 'σημείωση',
      'tip': 'υπόδειξη',
      'warning': 'προειδοποίηση',
      'admonition': 'επισήμανση',
      'sidebar': 'πλευρική-στήλη',
      'topic': 'θέμα',
      'line-block': 'μορφοποιημένο-λεκτικό',
      'parsed-literal': 'επεξεργασμένο-λεκτικό',
      'rubric': 'ρουμπρίκα',
      'epigraph': 'επιγραφή',
      'highlights': 'βασικά-στοιχεία',
      'pull-quote': 'παράθεση',
      'compound': 'σύνθετη',
      'container': 'δοχείο',
      #'questions': 'ερωτήσεις',
      'table': 'πίνακας',
      'csv-table': 'csv-πίνακας',
      'list-table': 'πίνακας-λιστών',
      #'qa': 'ερωταπαντήσεις',
      #'faq': 'συχνές-ερωτήσεις',
      'meta': 'μεταδεδομένα',
      'math': 'μαθηματικά',
      #'imagemap': 'εικονοχάρτης',
      'image': 'εικόνα',
      'figure': 'σχήμα',
      'include': 'συμπερίληψη',
      'raw': 'ακατέργαστο',
      'replace': 'αντικατάσταση',
      'unicode': 'unicode',
      'date': 'ημερομηνία',
      'class': 'κλάση',
      'role': 'ρόλος',
      'default-role': 'προεπιλεγμένος-ρόλος',
      'title': 'τίτλος',
      'contents': 'περιεχόμενα',
      'sectnum': 'αρίθμηση-ενοτήτων',
      'section-numbering': 'αρίθμηση-ενοτήτων',
      'header': 'κεφαλίδα',
      'footer': 'υποσέλιδο',
      #'footnotes': 'υποσημειώσεις',
      #'citations': 'παραπομπές',
      'target-notes': 'σημειώσεις-στόχου',
      'restructuredtext-test-directive': 'δοκιμαστική-οδηγία-restructuredtext'}
"""English name to registered (in directives/__init__.py) directive name
mapping."""

roles = {
    # language-dependent: fixed
    'abbreviation': 'συντομογραφία',
    'ab': 'συντομογραφία',
    'acronym': 'ακρωνύμιο',
    'ac': 'ακρωνύμιο',
    'code': 'κώδικας',
    'index': 'ευρετήριο',
    'i': 'ευρετήριο',
    'subscript': 'δείκτης',
    'sub': 'δείκτης',
    'superscript': 'εκθέτης',
    'sup': 'εκθέτης',
    'title-reference': 'αναφορά-τίτλου',
    'title': 'αναφορά-τίτλου',
    't': 'αναφορά-τίτλου',
    'pep-reference': 'αναφορά-pep',
    'pep': 'αναφορά-pep',
    'rfc-reference': 'αναφορά-rfc',
    'rfc': 'αναφορά-rfc',
    'emphasis': 'έμφαση',
    'strong': 'ισχυρό',
    'literal': 'λεκτικό',
    'math': 'μαθηματικά',
    'named-reference': 'επώνυμη-αναφορά',
    'anonymous-reference': 'ανώνυμη-αναφορά',
    'footnote-reference': 'αναφορά-υποσημείωσης',
    'citation-reference': 'αναφορά-παραπομπής',
    'substitution-reference': 'αναφορά-αντικατάστασης',
    'target': 'στόχος',
    'uri-reference': 'αναφορά-uri',
    'uri': 'αναφορά-uri',
    'url': 'αναφορά-uri',
    'raw': 'ακατέργαστο',}
"""Mapping of English role names to canonical role names for interpreted text.
"""
