Piereling
===========

.. image:: https://travis-ci.com/proycon/piereling.svg?branch=master
    :target: https://travis-ci.com/proycon/piereling

.. image:: http://applejack.science.ru.nl/lamabadge.php/piereling
   :target: http://applejack.science.ru.nl/languagemachines/

.. image:: https://www.repostatus.org/badges/latest/active.svg
   :alt: Project Status: Active – The project has reached a stable, usable state and is being actively developed.
   :target: https://www.repostatus.org/#active

.. image:: https://img.shields.io/pypi/v/piereling
   :alt: Latest release in the Python Package Index
   :target: https://pypi.org/project/piereling/

.. image:: https://raw.githubusercontent.com/proycon/piereling/master/logo.png
   :alt: Piereling Logo
   :align: center
   :scale: 40%

**Piereling** is a webservice and web-application to convert between a
variety of document formats and to and from the `Format for Linguistic
Annotation <https://proycon.github.io/folia>`__ (FoLiA). It is intended
to be used in Natural Language Processing pipelines. Piereling itself
does not actually implement the convertors but relies on numerous other
specialised conversion tools in combination with notable third-party
tools such as `pandoc <https://pandoc.org>`__ to accomplish its goals.

*Piereling* is the word for earthworm in Limburgish dialect. Data
conversion forms the *groundwork* for linguistic annotation, and thse
little worms, eating the input file on one end and secreting a
conversion on its outer end, perform that job.

We use `FoLiA <https://proycon.github.io/proycon>`__ as our pivot format
so you will mostly encounter conversions from or to FoLiA. FoLiA is a
format for Linguistic Annotation that also incorporates elaborate
document structure and mark-up facilities. Another important
intermediate format used in many of our conversions through pandoc is
`ReStructuredText <http://docutils.sourceforge.net/rst.html>`__, a
lightweight markup format. Although, Pandoc support a huge number of
conversions between all its supported document formats, it is beyond the
scope of his project to offer those in the webservice.

Available Conversions
---------------------

Conversions to FoLiA
~~~~~~~~~~~~~~~~~~~~

From Document and Markup Formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  from **plain text**; uses ``txt2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  In addition to an attempted extraction of text structure
      (paragraphs) by detecting blank lines, it also supports
      one-sentence-per-line and one-paragraph-per-line styles.
   -  If you can deliver your input as ReStructuredText or Markdown then
      this is is strongly preferred if you want to preserve structure
      and markup, as these formats resolve a lot of ambiguity inherent
      in unspecified plain text.
   -  Information loss: None

-  from **ReStructuredText**; using ``rst2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Minimal to None (almost all rst structures are
      supported)

-  from **Markdown**; via ReStructuredText using
   `pandoc <https://pandoc.org>`__ and then ``rst2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Minimal to None (most markdown structures are
      supported; exceptions are mathematical formula)

-  from **HTML**; via ReStructuredText using
   `pandoc <https://pandoc.org>`__ and then ``rst2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Some; complex layout, complex tables, and
      imagery will generally get lost. Should only be used for
      semantically clean and simple HTML rather than complex
      presentational HTML from the web.

-  from **Word** (Office Open XML, docx); via ReStructuredText using
   `pandoc <https://pandoc.org>`__ and then ``rst2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Some; complex layout, complex tables, and
      imagery will generally get lost.
   -  Note that the Word 2007 DOC format from up until 2007 is not
      supported, only the modern DOCX variant.

-  from **OpenDocument Text** (LibreOffice, odt); via ReStructuredText
   using `pandoc <https://pandoc.org>`__ and then ``rst2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Some; complex layout, complex tables, and
      imagery will generally get lost.

-  from **EPUB**; via ReStructuredText using
   `pandoc <https://pandoc.org>`__ and then ``rst2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Some; complex layout, complex tables, and
      imagery will generally get lost.

-  from **LaTeX**; via ReStructuredText using
   `pandoc <https://pandoc.org>`__ and then ``rst2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Some to considerable; complex layout, complex
      tables, custom packages, math, and imagery will generally get
      lost.

-  from **MediaWiki** (as used by Wikipedia); via ReStructuredText using
   `pandoc <https://pandoc.org>`__ and then ``rst2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Some; complex layout, complex tables. Wikipedia
      specific elements.

-  from **DocBook**; via ReStructuredText using
   `pandoc <https://pandoc.org>`__ and then ``rst2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Unknown

-  from **TEI P5 XML** (Text Encoding Initiative); uses ``tei2folia``
   from `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  TEI is a very extensive and flexible format with many different
      forms
   -  Information loss: Our converter will only work for a certain
      subset of TEI, mostly equivalent to TEI Lite, and may fail on
      others. Though we support a lot of TEI elements, there is also
      still a lot that is not covered by the converter. There will be
      comments in the output for anything that could not be converted
      properly.

-  from **PDF**; uses ``pdftotext`` from
   `Poppler <https://poppler.freedesktop.org>`__ and then ``txt2folia``
   from FoLiA-tools.

   -  Only works for PDFs with embedded text, not for imagery which
      would require OCR!
   -  Information loss: **Considerable!** PDF conversion is notoriously
      difficult, the layout of the document will most probably get lost
      in the conversion (especially in case of multi-columned output).
      The markup will get lost too.
   -  Structural conversion is very inaccurate (i.e. paragraphs will not
      be nicely mapped) and produces ugly FoLiA.
   -  Always avoid this conversion if you can!

-  from **hOCR**; uses ``FoLiA-hocr`` from
   `foliautils <https://github.com/LanguageMachines/foliautils>`__.

   -  hOCR is a standard format outputted by OCR systems such as
      `Tesseract <https://github.com/tesseract-ocr/tesseract>`__.
   -  Information loss: Unknown

-  from **ALTO**; uses ``FoLiA-alto`` from
   `foliautils <https://github.com/LanguageMachines/foliautils>`__.

   -  ALTO is a standard format for the description of text OCR and
      layout information of pages for digitized material.
   -  Information loss: Unknown

From other Linguistic Annotation Formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  from **NAF** (NLP Annotation Format) to FoLiA; uses ``naf2folia``
   from `NAFFoLiAPy <https://github.com/cltl/naffoliapy>`__.

   -  This converter is still in an early and experimental stage.
   -  Information loss: Not all annotation layers are implemented yet.
      Those that are should suffer minimal to no information loss. See
      the `website <https://github.com/cltl/naffoliapy>`__ for details.

-  from **CONLL-U**; uses ``conllu2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: None

-  from **Alpino XML**; uses ``alpino2folia`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Minimal to None

Conversions from FoLiA
~~~~~~~~~~~~~~~~~~~~~~

-  to **plain text**, uses ``folia2txt`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Considerable, as only the text will be outputted
      and any annotations, most structure, and all markup will be lost.
      The text itself, however, will be very accurately converted, in
      either tokenised (if available) or untokenised form.

-  to **HTML**; this conversion is offered through the default viewer in
   the web-interface.

   -  Information loss: Minimal, but information is represented purely
      for presentational purposes rather than focussing on semantics.

-  to **ReStructuredText**, uses ``folia2rst`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.

   -  Information loss: Structure and mark-up will be preserved, but
      annotations will be lost!

Validation & Upgrade
~~~~~~~~~~~~~~~~~~~~

-  FoLiA validation; using ``foliavalidator`` from
   `FoLiA-Tools <https://github.com/proycon/folia-tools>`__.
-  FoLiA upgrade; upgrades an older FoLiA version to a newer one (mostly
   inteneded for FoLiA v1 to FoLiA v2); uses ``foliaupgrade`` from
   `FoLiA-Tools <https://github.com/proycon/foliatools>`__.

Installation
------------

Install using pip (preferably in a Python virtual environment):

``pip install piereling``

Piereling is supplied as part of our
`LaMachine <https://proycon.github.io/LaMachine>`__ distribution, which
includes all dependencies out of the box. If you don’t use this, you
will need to take care of installing certain dependencies yourself in
order for all convertors to work, this includes:

-  `pandoc <https://pandoc.org>`__
-  `foliautils <https://github.com/LanguageMachines/foliautils>`__
-  `poppler-utils <https://poppler.freedesktop.org>`__

For production use, we recommend using uwsgi in combination with a
webserver such as Apache (with mod_uwsgi_proxy), or nginx. A uwsgi
configuration has been generated (``piereling.example.ini``); it is
specific to the host you deploy the webservice on. This in turn loads
the wsgi script (``piereling.wsgi``), which loads your webservice.

Sample configurations for nginx and Apache have been generated as a
starting point, add these to your server and then use the
``./startserver_production.sh`` script to launch CLAM using uwsgi. If
you use LaMachine, all this has already been set up for you.

Usage
-----

Run ``clamservice piereling.piereling`` to start the *development*
server and then navigate your browser to the address printed.

Web
---

Piereling is a RESTful webservice and also provides a web-interface for
human end users (powered by `CLAM <https://proycon.github.io/clam>`__).
If you instead seek to do conversions locally on the command line then
you have no need for Piereling and should simply invoke the
aforementioned conversion tools directly.

A public instance of this webservice is available at ``https://webservices-lst.science.ru.nl/piereling``, register for a
free account at ``https://webservices-lst.science.ru.nl`` first.

Related Tools
-------------

If you want to convert to TEI, or use TEI as a pivot format for
conversions, then you can look at
`OxGarage <https://oxgarage2.tei-c.org/>`__
(`source <https://github.com/TEIC/oxgarage/>`__) and
`OpenConvert <https://github.com/INL/OpenConvert>`__.

