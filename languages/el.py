# -*- coding: utf-8 -*-
# $Id: el.py boukeas $
# Author: George Boukeas <boukeas@gmail.com>
# Copyright: This module has been placed in the public domain.

# New language mappings are welcome.  Before doing a new translation, please
# read <http://docutils.sf.net/docs/howto/i18n.html>.  Two files must be
# translated for each language: one in docutils/languages, the other in
# docutils/parsers/rst/languages.

"""
Greek-language mappings for language-dependent features of Docutils.
"""

__docformat__ = 'reStructuredText'

labels = {
      # fixed: language-dependent
      'author': 'Συγγραφέας',
      'authors': 'Συγγραφείς',
      'organization': 'Οργανισμός',
      'address': 'Διεύθυνση',
      'contact': 'Επικοινωνία',
      'version': 'Έκδοση',
      'revision': 'Αναθεώρηση',
      'status': 'Κατάσταση',
      'date': 'Ημερομηνία',
      'copyright': 'Πνευματικά Δικαιώματα',
      'dedication': 'Αφιέρωση',
      'abstract': 'Περίληψη',
      'attention': 'Προσοχή!',
      'caution': 'Προειδοποίηση!',
      'danger': '!ΚΙΝΔΥΝΟΣ!',
      'error': 'Σφάλμα',
      'hint': 'Υπόδειξη',
      'important': 'Σημαντικό',
      'note': 'Σημείωση',
      'tip': 'Συμβουλή',
      'warning': 'Προειδοποίηση',
      'contents': 'Περιεχόμενα',
      # extentions for websheets
      'solution': 'Λύση'}
"""Mapping of node class name to label text."""

bibliographic_fields = {
      # language-dependent: fixed
      'author': 'συγγραφέας',
      'authors': 'συγγραφείς',
      'organization': 'οργανισμός',
      'address': 'διεύθυνση',
      'contact': 'επικοινωνία',
      'version': 'έκδοση',
      'revision': 'αναθεώρηση',
      'status': 'κατάσταση',
      'date': 'ημερομηνία',
      'copyright': 'πνευματικά δικαιώματα',
      'dedication': 'αφιέρωση',
      'abstract': 'περίληψη'}
"""English (lowcased) to canonical name mapping for bibliographic fields."""

author_separators = [',', '·']
"""List of separator strings for the 'Authors' bibliographic field. Tried in
order."""
