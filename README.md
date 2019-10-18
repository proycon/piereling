[![Language Machines Badge](http://applejack.science.ru.nl/lamabadge.php/piereling)](http://applejack.science.ru.nl/languagemachines/)
[![Build Status](https://travis-ci.org/proycon/piereling.svg?branch=master)](https://travis-ci.org/proycon/piereling)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
# Piereling

**Piereling** is a webservice and web-application to convert between a variety
of document formats and to and from the [Format for Linguistic
Annotation](https://proycon.github.io/folia) (FoLiA). It is intended to be used in
Natural Language Processing pipelines. Piereling itself does not actually
implement the convertors but relies on numerous other specialised conversion
tools in combination with notable third-party tools such as
[pandoc](https://pandoc.org) to accomplish its goals.

*Piereling* is the word for earthworm in Limburgish dialect; see it as a worm,
or rather a whole bunch of worms, eating input an input file on one end and
secreting a conversion on its outer end.

We use FoLiA as our pivot format so you will mostly encounter conversions from
or to FoLiA.  Pandoc support a huge number of other conversions between
document formats, it is beyond the scope of his project to offer those in the webservice.

## Conversions to FoLiA

* from **plain text**; uses ``txt2folia`` from [FoLiA-Tools](https://github.com/proycon/folia-tools).
    * If you can deliver your input as ReStructuredText or Markdown then this is is strongly preferred if you want to preserve structure and markup.
    * Information loss: None
* from **ReStructuredText**; using ``rst2folia`` from [FoLiA-Tools](https://github.com/proycon/folia-tools).
    * Information loss: Minimal to None (almost all rst structures are supported)
* from **Markdown**; via ReStructuredText using [pandoc](https://pandoc.org) and then ``rst2folia`` from [FoLiA-Tools](https://github.com/proycon/folia-tools).
    * Information loss: Minimal to None (most markdown structures are supported; exceptions are mathematical formula)
* from **Word** (Office Open XML, docx); via ReStructuredText using [pandoc](https://pandoc.org) and then ``rst2folia`` from [FoLiA-Tools](https://github.com/proycon/folia-tools).
    * Information loss: Some; complex layout, complex tables, and imagery will generally get lost.
* from **OpenDocument Text** (LibreOffice, odt); via ReStructuredText using [pandoc](https://pandoc.org) and then ``rst2folia`` from [FoLiA-Tools](https://github.com/proycon/folia-tools).
    * Information loss: Some; complex layout, complex tables, and imagery will generally get lost.
* from **TEI P5 XML** (Text Encoding Initiative); uses ``tei2folia`` from [FoLiA-Tools](https://github.com/proycon/folia-tools).
    * TEI is a very extensive and flexible format with many different forms
    * Information loss: Our converter will only work for a certain subset of TEI and may fail on others. Though we support a lot of TEi elements, there is also still a lot that is not covered by the converter.
* from **CONLL-U**; uses ``conllu2folia`` from [FoLiA-Tools](https://github.com/proycon/folia-tools).
    * Information loss: None
* from **Alpino XML**; uses ``alpino2folia`` from [FoLiA-Tools](https://github.com/proycon/folia-tools).
    * Information loss: Minimal to None
* from **PDF**; uses ``pdftotext`` from [Poppler](https://poppler.freedesktop.org) and then ``txt2folia`` from FoLiA-tools.
    * Only works for PDFs with embedded text, not for imagery which would require OCR!
    * Information loss: Considerable. PDF conversion is notoriously difficult, the layout of the document will most probably get lost in the conversion (especially in case of multi-columned output). The markup will get lost too.
* from **hOCR**; uses ``FoLiA-hocr`` from [foliautils](https://github.com/LanguageMachines/foliautils).
    * hOCR is a standard format outputted by OCR systems such as [Tesseract](https://github.com/tesseract-ocr/tesseract).
    * Information loss: Unknown
* from **ALTO**; uses ``FoLiA-alto`` from [foliautils](https://github.com/LanguageMachines/foliautils).
    * ALTO is a tandard ormat for the description of text OCR and layout information of pages for digitized material.
    * Information loss: Unknown

## Conversions from FoLiA

* to **HTML**; this conversion is offered through the default viewer in the web-interface.
    * Information loss: Minimal, but it is offered for presentational purposes rather than focussing on semantics.
* to **plain text**, uses ``folia2txt`` from [FoLiA-Tools](https://github.com/proycon/folia-tools).
    * Information loss: Considerable, as only the text will be outputted and any annotations and markup will be lost.



