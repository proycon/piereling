#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Service Configuration File (Template) --
#       by Maarten van Gompel (proycon)
#       Centre for Language and Speech Technology / Language Machines
#       Radboud University Nijmegen
#
#       https://proycon.github.io/clam
#
#       Licensed under GPLv3
#
###############################################################

#Consult the CLAM manual for extensive documentation

#If we run on Python 2.7, behave as much as Python 3 as possible
from __future__ import print_function, unicode_literals, division, absolute_import

from clam.common.parameters import BooleanParameter, StringParameter, ChoiceParameter, IntegerParameter, StaticParameter
from clam.common.formats import FoLiAXMLFormat, PlainTextFormat, MSWordFormat, HTMLFormat, PDFFormat
from clam.common.converters import *
from clam.common.viewers import FLATViewer, FoLiAViewer
from clam.common.data import Profile, InputTemplate, OutputTemplate, loadconfig, CLAMMetaData, SetMetaField
from clam.common.digestauth import pwhash
import clam
import sys
import os

REQUIRE_VERSION = 3.0

CLAMDIR = clam.__path__[0] #directory where CLAM is installed, detected automatically
WEBSERVICEDIR = os.path.dirname(os.path.abspath(__file__)) #directory where this webservice is installed, detected automatically

# ======== GENERAL INFORMATION ===========

# General information concerning your system.


#The System ID, a short alphanumeric identifier for internal use only
SYSTEM_ID = "piereling"
#System name, the way the system is presented to the world
SYSTEM_NAME = "Piereling"

#An informative description for this system (this should be fairly short, about one paragraph, and may not contain HTML)
SYSTEM_DESCRIPTION = "Piereling can convert a wide variety of document formats to FoLiA XML, and from FoLiA XML to various formats. Data conversions such as these provide the groundwork for Natural Language Processing pipelines. It relies on numerous specialised conversion tools in combination with notable third-party tools such as pandoc."

#A version label of the underlying tool and/or this CLAM wrapper
#(If you can derive this dynamically then that is strongly recommended!)
SYSTEM_VERSION = "0.2"

#The author(s) of the underlying tool and/or this CLAM wrapper
#(If you can derive this dynamically then that is strongly recommended!)
SYSTEM_AUTHOR = "Maarten van Gompel"

SYSTEM_AFFILIATION = "Centre for Language and Speech Technology, Radboud University"

#How to reach the authors?
SYSTEM_EMAIL = "proycon@anaproy.nl"

SYSTEM_LICENSE = "GNU Public License v3"

SYSTEM_URL = "https://github.com/proycon/piereling"

SYSTEM_COVER_URL = "https://raw.githubusercontent.com/proycon/piereling/master/logo.png"

FLATURL = None

#This invokes the automatic loader, do not change it;
#it will try to find a file named $system_id.$hostname.yml or just $hostname.yml, where $hostname
#is the auto-detected hostname of this system. Alternatively, it tries a static $system_id.config.yml or just config.yml .
#You can also set an environment variable CONFIGFILE to specify the exact file to load at run-time.
#It will look in several paths including the current working directory and the path this settings script is loaded from.
#Such an external configuration file simply defines variables that will be imported here. If it fails to find
#a configuration file, an exception will be raised.
loadconfig(__name__)



#Amount of free memory required prior to starting a new process (in MB!), Free Memory + Cached (without swap!). Set to 0 to disable this check (not recommended)
REQUIREMEMORY = 10

#Maximum load average at which processes are still started (first number reported by 'uptime'). Set to 0 to disable this check (not recommended)
#MAXLOADAVG = 4.0

#Minimum amount of free diskspace in MB. Set to 0 to disable this check (not recommended)
#DISK = '/dev/sda1' #set this to the disk where ROOT is on
#MINDISKSPACE = 10

#The amount of diskspace a user may use (in MB), this is a soft quota which can be exceeded, but creation of new projects is blocked until usage drops below the quota again
#USERQUOTA = 100

#The secret key is used internally for cryptographically signing session data, in production environments, you'll want to set this to a persistent value. If not set it will be randomly generated.
#SECRET_KEY = 'mysecret'

#Allow Asynchronous HTTP requests from **web browsers** in following domains (sets Access-Control-Allow-Origin HTTP headers), by default this is unrestricted
#ALLOW_ORIGIN = "*"

# ======== WEB-APPLICATION STYLING =============

#Choose a style (has to be defined as a CSS file in clam/style/ ). You can copy, rename and adapt it to make your own style
STYLE = 'classic'

# ======== ENABLED FORMATS ===========

#In CUSTOM_FORMATS you can specify a list of Python classes corresponding to extra formats.
#You can define the classes first, and then put them in CUSTOM_FORMATS, as shown in this example:

class TEIXMLFormat(CLAMMetaData):
    attributes = {}
    name = "TEI P5 XML"
    mimetype = 'text/tei+xml'

class ReStructuredTextFormat(CLAMMetaData):
    attributes = {'encoding': StaticParameter('encoding','Encoding',value='utf-8')}
    name = "ReStructuredText"
    mimetype = 'text/rst'

class MarkdownFormat(CLAMMetaData):
    attributes = {'encoding': StaticParameter('encoding','Encoding',value='utf-8')}
    name = "Markdown Text"
    mimetype = 'text/markdown'

class CONLLuFormat(CLAMMetaData):
    attributes = {'encoding': StaticParameter('encoding','Encoding',value='utf-8')}
    name = "CONLL-U"
    mimetype = 'text/plain'

class AlpinoXMLFormat(CLAMMetaData):
    attributes = {'encoding': StaticParameter('encoding','Encoding',value='utf-8')}
    name = "Alpino XML"
    mimetype = 'text/alpino+xml'

class NAFXMLFormat(CLAMMetaData):
    attributes = {'encoding': StaticParameter('encoding','Encoding',value='utf-8')}
    name = "NAF XML"
    mimetype = 'text/naf+xml'

class EPUBFormat(CLAMMetaData):
    name = "EPUB"
    mimetype = 'application/epub+zip'

class LaTeXFormat(CLAMMetaData):
    attributes = {'encoding': StaticParameter('encoding','Encoding',value='utf-8')}
    name = "LaTeX"
    mimetype = 'application/x-latex'

class DocBookXMLFormat(CLAMMetaData):
    name = "DocBook XML"
    mimetype = 'application/docbook+xml'

CUSTOM_FORMATS = [ TEIXMLFormat, ReStructuredTextFormat, MarkdownFormat, CONLLuFormat, AlpinoXMLFormat, NAFXMLFormat, EPUBFormat, LaTeXFormat, DocBookXMLFormat ]

# ======== ENABLED VIEWERS ===========

#In CUSTOM_VIEWERS you can specify a list of Python classes corresponding to extra formats.
#You can define the classes first, and then put them in CUSTOM_VIEWERS, as shown in this example:

# CUSTOM_VIEWERS = [ MyXMLViewer ]

# ======= INTERFACE OPTIONS ===========

#Here you can specify additional interface options (space separated list), see the documentation for all allowed options
#INTERFACEOPTIONS = "inputfromweb" #allow CLAM to download its input from a user-specified url
INTERFACEOPTIONS = "centercover,coverheight100"

# ======== PREINSTALLED DATA ===========

#INPUTSOURCES = [
#    InputSource(id='sampledocs',label='Sample texts',path=ROOT+'/inputsources/sampledata',defaultmetadata=PlainTextFormat(None, encoding='utf-8') ),
#]

# ======== PROFILE DEFINITIONS ===========

#Define your profiles here. This is required for the project paradigm, but can be set to an empty list if you only use the action paradigm.

PROFILES = [
    Profile(
        InputTemplate('txt2folia_in', PlainTextFormat,"Plain text input for conversion to FoLiA",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            ChoiceParameter(id='style',name='Style',description='The style the text is in, determines whether structure can be extracted.', choices=[('undetermined','Undetermined (no structure will be extracted)'), ('sentenceperline','One sentence per line'),('paragraphperline','One paragraph per line'),('paragraphs', 'Paragraphs separated by a blank line')]),
            extension='.txt',
            multi=True,
        ),
        OutputTemplate('txt2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from plain text',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.txt'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('rst2folia_in', ReStructuredTextFormat,"ReStructuredText Input for conversion to FoLiA",
            extension='.rst',
            multi=True,
        ),
        OutputTemplate('rst2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from ReStructuredText input',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.rst'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('md2folia_in', MarkdownFormat,"Markdown Input for conversion to FoLiA",
            ChoiceParameter(id='flavour',name='Flavour',description='Markdown flavour', choices=[('normal','normal'), ('strict','strict'),('github','github')]),
            extension='.md',
            multi=True,
        ),
        OutputTemplate('md2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from Markdown input',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.md'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('docx2folia_in', MSWordFormat,"MS Word (Office Open XML, docx) input for conversion to FoLiA",
            extension='.docx',
            multi=True,
        ),
        OutputTemplate('docx2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from MS Word input',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.docx'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('odt2folia_in', MSWordFormat,"OpenDocument Text Document (odt) for conversion to FoLiA",
            extension='.odt',
            multi=True,
        ),
        OutputTemplate('odt2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from OpenDocument Text',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.odt'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('epub2folia_in', EPUBFormat,"EPUB for conversion to FoLiA",
            extension='.epub',
            multi=True,
        ),
        OutputTemplate('epub2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from EPUB',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.epub'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('latex2folia_in', LaTeXFormat,"LaTeX source for conversion to FoLiA",
            extension='.tex',
            multi=True,
        ),
        OutputTemplate('latex2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from LaTeX',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.tex'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('mediawiki2folia_in', PlainTextFormat,"MediaWiki Markup (Wikipedia and others) for conversion to FoLiA",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            extension='.txt',
            multi=True,
        ),
        OutputTemplate('mediawiki2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from MediaWiki',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.txt'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('docbook2folia_in', DocBookXMLFormat,"Docbook for conversion to FoLiA",
            extension='.xml',
            multi=True,
        ),
        OutputTemplate('docbook2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from Docbook',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.xml','.dbk'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('html2folia_in', HTMLFormat,"HTML for conversion to FoLiA",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            extension='.html',
            multi=True,
        ),
        OutputTemplate('html2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from HTML',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.html','.htm'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('pdf2folia_in', PDFFormat,"PDF with embedded text (pdf) for conversion to FoLiA",
            extension='.pdf',
            multi=True,
        ),
        OutputTemplate('pdf2folia_out',FoLiAXMLFormat,'FoLiA XML output (untokenised) from PDF',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.pdf'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('conllu2folia_in', CONLLuFormat,"CONLL-U format for conversion to FoLiA",
            multi=True,
        ),
        OutputTemplate('conllu2folia_out',FoLiAXMLFormat,'FoLiA XML output from CONLL-U',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.txt','.conll','.conllu','.tsv','.csv'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('naf2folia_in', NAFXMLFormat,"NAF XML for conversion to FoLiA",
            multi=True,
        ),
        OutputTemplate('naf2folia_out',FoLiAXMLFormat,'FoLiA XML output from NAF',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.naf.xml','.naf','.xml'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('alpino2folia_in', AlpinoXMLFormat,"Alpino XML for conversion to FoLiA",
            extension='.xml',
            multi=True,
        ),
        OutputTemplate('alpino2folia_out',FoLiAXMLFormat,'FoLiA XML output from NAF',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            extension='.folia.xml',
            removeextensions=['.xml'],
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('tei2folia_in', TEIXMLFormat,"TEI P5 XML input for conversion to FoLiA",
            extension='.xml',
            #filename='filename.txt',
            multi=True #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('tei2folia_out',FoLiAXMLFormat,'FoLiA XML output from TEI input',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            removeextensions=['.tei.xml','.xml','.tei'],
            extension='.folia.xml', #set an extension or set a filename:
            multi=True
        ),
    ),
    Profile(
        InputTemplate('folia2txt_in', FoLiAXMLFormat,"FoLiA XML input for conversion to text",
            extension='.folia.xml',
            multi=True,
        ),
        OutputTemplate('folia2txt_out',PlainTextFormat,'Plain text output from FoLiA input',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextensions=['.folia.xml','.xml'],
            extension='.txt',
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('folia2rst_in', FoLiAXMLFormat,"FoLiA XML input for conversion to ReStructuredText",
            extension='.folia.xml',
            multi=True,
        ),
        OutputTemplate('folia2rst_out',ReStructuredTextFormat,'Plain text output from FoLiA input',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextensions=['.folia.xml','.xml'],
            extension='.rst',
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('folia2html_in', FoLiAXMLFormat,"FoLiA XML input for conversion to HTML",
            extension='.folia.xml',
            multi=True,
        ),
        OutputTemplate('folia2html_out',HTMLFormat,'HTML output from FoLiA input',
            removeextensions=['.folia.xml','.xml'],
            extension='.html',
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('foliavalidator_in', FoLiAXMLFormat,"FoLiA XML input for validation",
            extension='.folia.xml',
            multi=True,
        ),
        OutputTemplate('foliavalidator_out',PlainTextFormat,'Validation report from FoLiA input',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextensions=['.folia.xml','.xml'],
            extension='.log',
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('foliaupgrade_in', FoLiAXMLFormat,"FoLiA XML input for upgrade to a newer FoLiA",
            extension='.folia.xml',
            multi=True,
        ),
        OutputTemplate('foliaupgrade_out',FoLiAXMLFormat,'Upgraded FoLiA XML output',
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            FoLiAViewer(),
            multi=True,
        ),
    ),
]

# ======== COMMAND ===========

#The system command for the project paradigm.
#It is recommended you set this to small wrapper
#script around your actual system. Full shell syntax is supported. Using
#absolute paths is preferred. The current working directory will be
#set to the project directory.
#
#You can make use of the following special variables,
#which will be automatically set by CLAM:
#     $INPUTDIRECTORY  - The directory where input files are uploaded.
#     $OUTPUTDIRECTORY - The directory where the system should output
#                        its output files.
#     $TMPDIRECTORY    - The directory where the system should output
#                        its temporary files.
#     $STATUSFILE      - Filename of the .status file where the system
#                        should output status messages.
#     $DATAFILE        - Filename of the clam.xml file describing the
#                        system and chosen configuration.
#     $USERNAME        - The username of the currently logged in user
#                        (set to "anonymous" if there is none)
#     $PARAMETERS      - List of chosen parameters, using the specified flags
#
COMMAND = WEBSERVICEDIR + "/piereling_wrapper.py $DATAFILE $STATUSFILE $OUTPUTDIRECTORY"

#Or for the shell variant:
#COMMAND = WEBSERVICEDIR + "/piereling_wrapper.sh $STATUSFILE $INPUTDIRECTORY $OUTPUTDIRECTORY $PARAMETERS"

#Or if you only use the action paradigm, set COMMAND = None

# ======== PARAMETER DEFINITIONS ===========

#The global parameters (for the project paradigm) are subdivided into several
#groups. In the form of a list of (groupname, parameters) tuples. The parameters
#are a list of instances from common/parameters.py

PARAMETERS =  [
    ("ReStructuredText Parameters", [
        BooleanParameter(id="strip-relative-links",name="Strip relative links",description="Strip relative hyperlinks"),
        BooleanParameter(id="strip-links",name="Strip links",description="Strip all hyperlinks"),
        BooleanParameter(id="strip-style",name="Strip style",description="Strip all text styling (bold, italics etc)"),
        BooleanParameter(id="strip-gaps",name="Strip gaps",description="Strip all gaps (includes verbatim and code blocks)"),
        BooleanParameter(id="strip-raw",name="Strip raw",description="Strip all raw content (do not encode as gaps)"),
        BooleanParameter(id="strip-tables",name="Strip tables",description="Strip tables"),
        BooleanParameter(id="ignore-lineblocks",name="Ignore lineblocks",description="Ignore lineblocks, treat as normal paragraphs."),
    ] ),
    ("Validation Parameters", [
        ChoiceParameter(id="validationmode",name="Validation mode",description="Validation behaviour", choices=[("fail","Fail on validation errors"),("continue","Continue on validation errors")],default="fail"),
        BooleanParameter(id="autodeclare",name="Autodeclare",description="Attempt to automatically declare missing annotations"),
        BooleanParameter(id="deep",name="Deep Validation",description="Do deep validation (verifies tag sets)"),
        BooleanParameter(id="quick",name="Quicker Validation",description="Do quicker validation by skipping the check against the RelaxNG schema"),
        #ChoiceParameter(id="casesensitive",name="Case Sensitivity",description="Enable case sensitive behaviour?", choices=["yes","no"],default="no"),
        #StringParameter(id="author",name="Author",description="Sign output metadata with the specified author name",maxlength=255),
    ] ),
    ("Upgrade Parameters", [
        BooleanParameter(id="fixunassignedprocessor",name="Fix unassigned processor",description="Fixes invalid FoLiA that does not explicitly assign a processor to an annotation when multiple processors are possible (and there is therefore no default). The last processor will be used in this case."),
    ] ),

]


# ======= ACTIONS =============

#The action paradigm is an independent Remote-Procedure-Call mechanism that
#allows you to tie scripts (command=) or Python functions (function=) to URLs.
#It has no notion of projects or files and must respond in real-time. The syntax
#for commands is equal to those of COMMAND above, any file or project specific
#variables are not available though, so there is no $DATAFILE, $STATUSFILE, $INPUTDIRECTORY, $OUTPUTDIRECTORY or $PROJECT.

ACTIONS = [
    #Action(id='multiply',name='Multiply',parameters=[IntegerParameter(id='x',name='Value'),IntegerParameter(id='y',name='Multiplier'), command=sys.path[0] + "/actions/multiply.sh $PARAMETERS" ])
    #Action(id='multiply',name='Multiply',parameters=[IntegerParameter(id='x',name='Value'),IntegerParameter(id='y',name='Multiplier'), function=lambda x,y: x*y ])
]

# ======= FORWARDERS =============

#Global forwarders call a remote service, passing a backlink for the remote service to download an archive of all the output data. The remote service is expected to return a redirect (HTTP 302) . CLAM will insert the backlink where you put $BACKLINK in the url:

#FORWARDERS = [
    #Forwarder(id='otherservice', name="Other service", description="", url="https://my.service.com/grabfrom=$BACKLINK")
#]

# ======== DISPATCHING (ADVANCED! YOU CAN SAFELY SKIP THIS!) ========

#The dispatcher to use (defaults to clamdispatcher.py), you almost never want to change this
#DISPATCHER = 'clamdispatcher.py'

#DISPATCHER_POLLINTERVAL = 30   #interval at which the dispatcher polls for resource consumption (default: 30 secs)
#DISPATCHER_MAXRESMEM = 0    #maximum consumption of resident memory (in megabytes), processes that exceed this will be automatically aborted. (0 = unlimited, default)
#DISPATCHER_MAXTIME = 0      #maximum number of seconds a process may run, it will be aborted if this duration is exceeded.   (0=unlimited, default)
#DISPATCHER_PYTHONPATH = []        #list of extra directories to add to the python path prior to launch of dispatcher

#Run background process on a remote host? Then set the following (leave the lambda in):
#REMOTEHOST = lambda: return 'some.remote.host'
#REMOTEUSER = 'username'

#For this to work, the user under which CLAM runs must have (passwordless) ssh access (use ssh keys) to the remote host using the specified username (ssh REMOTEUSER@REMOTEHOST)
#Moreover, both systems must have access to the same filesystem (ROOT) under the same mountpoint.
