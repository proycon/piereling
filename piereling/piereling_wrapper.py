#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- CLAM Wrapper script Template --
#       by Maarten van Gompel (proycon)
#       https://proycon.github.io/clam
#       Centre for Language and Speech Technology
#       Radboud University Nijmegen
#
#       (adapt or remove this header for your own code)
#
#       Licensed under GPLv3
#
###############################################################

#This is a template wrapper which you can use a basis for writing your own
#system wrapper script. The system wrapper script is called by CLAM, it's job it
#to call your actual tool.

#This script will be called by CLAM and will run with the current working directory set to the specified project directory

#This wrapper script uses Python and the CLAM Data API.
#We make use of the XML settings file that CLAM outputs, rather than
#passing all parameters on the command line.


#If we run on Python 2.7, behave as much as Python 3 as possible
from __future__ import print_function, unicode_literals, division, absolute_import

#import some general python modules:
import sys
import os
import shutil

#import CLAM-specific modules. The CLAM API makes a lot of stuff easily accessible.
import clam.common.data
import clam.common.status

import folia.main as folia

#When the wrapper is started, the current working directory corresponds to the project directory, input files are in input/ , output files should go in output/ .

#make a shortcut to the shellsafe() function
shellsafe = clam.common.data.shellsafe

#this script takes three arguments from CLAM: $DATAFILE $STATUSFILE $OUTPUTDIRECTORY
#(as configured at COMMAND= in the service configuration file, there you can
#reconfigure which arguments are passed and in what order.
datafile = sys.argv[1]
statusfile = sys.argv[2]
outputdir = sys.argv[3]

#If you make use of CUSTOM_FORMATS, you need to import your service configuration file here and set clam.common.data.CUSTOM_FORMATS
#Moreover, you can import any other settings from your service configuration file as well:

from piereling import CUSTOM_FORMATS
clam.common.data.CUSTOM_FORMATS = CUSTOM_FORMATS

#Obtain all data from the CLAM system (passed in $DATAFILE (clam.xml)), always pass CUSTOM_FORMATS as second argument if you make use of it!
clamdata = clam.common.data.getclamdata(datafile)

#You now have access to all data. A few properties at your disposition now are:
# clamdata.system_id , clamdata.project, clamdata.user, clamdata.status , clamdata.parameters, clamdata.inputformats, clamdata.outputformats , clamdata.input , clamdata.output

clam.common.status.write(statusfile, "Starting...")


def run(cmd):
    print("Running " + cmd, file=sys.stderr)
    logfile = os.path.join(outputdir, "lastcommand.log")
    r = os.system(cmd + " 2> " + shellsafe(logfile))
    with open(logfile,'r',encoding='utf-8') as f:
        print(f.read(), file=sys.stderr)
    os.unlink(logfile)
    if r != 0:
        clam.common.status.write(statusfile, "Failure running " + cmd.split(' ')[0],100) # status update
        sys.exit(2)


#=========================================================================================================================

# Below are some examples of how to access the input files and expected output
# files. Choose and adapt one of examples A, B or C.

#-- EXAMPLE A: Iterate over the program --

# The 'program' describes exactly what output files will/should be generated on the
# basis of what input files. It is the concretisation of the profiles and is the
# most elegant method to set up your wrapper.


for outputfile, outputtemplate_id in clamdata.program.getoutputfiles():
    if outputtemplate_id == "errorlog":
        continue

    clam.common.status.write(statusfile, "Processing " + os.path.basename(str(outputfile)),50) # status update
    #(Use outputtemplate_id to match against output templates)
    #(You can access output metadata using outputfile.metadata[parameter_id])
    outputfilepath = str(outputfile) #example showing how to obtain the path to the file
    #if you expect just a single input file for this output file, you can use this:
    inputfile, inputtemplate = clamdata.program.getinputfile(outputfile)
    inputfilepath = str(inputfile)

    docid = folia.makencname(inputfile.filename.split('.')[0])
    rst2folia_args = [ '--docid=' + shellsafe(docid, '"') ]
    for opt in ("strip-relative-links", "strip-links","strip-style", "strip-gaps", "strip-raw", "strip-tables", "ignore-lineblocks" ):
        if clamdata.get(opt):
            rst2folia_args.append("--" + opt)

    if outputtemplate_id == 'rst2folia_out':
        run("rst2folia " + " ".join(rst2folia_args) + " " + shellsafe(inputfilepath,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'txt2folia_out':
        txt2folia_args = [ '--id=' + shellsafe(docid, '"') ]
        if 'style' in inputfile.metadata:
            style = inputfile.metadata["style"]
            if style == "sentenceperline":
                txt2folia_args.append("--sentenceperline")
            elif style == "paragraphperline":
                txt2folia_args.append("--paragraphperline")
            elif style == "undetermined":
                txt2folia_args.append("--nostructure")
            else:
                txt2folia_args.append("--paragraphs")
        else:
            txt2folia_args.append("--paragraphs")
        run("txt2folia -o '-' " + " ".join(txt2folia_args) + " " + shellsafe(inputfilepath,'"') + " > " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'md2folia_out':
        intermediatefile = outputfilepath.replace('.folia.xml','') + '.rst'
        flavour = 'markdown'
        try:
            if inputfile.metadata['flavour'] == 'github':
                flavour = 'markdown_github'
            elif inputfile.metadata['flavour'] == 'strict':
                flavour = 'markdown_strict'
            elif inputfile.metadata['flavour'] == 'normal':
                flavour = 'markdown'
        except KeyError:
            pass
        run("pandoc --from=markdown --to=rst " + shellsafe(inputfilepath,'"') + " > " + shellsafe(intermediatefile,'"') )
        run("rst2folia " + " ".join(rst2folia_args) + " " + shellsafe(intermediatefile,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'pdf2folia_out':
        intermediatefile = outputfilepath.replace('.folia.xml','') + '.txt'
        run("pdftotext -nopgbrk " + shellsafe(inputfilepath,'"') + " - > " + shellsafe(intermediatefile,'"') )
        run("txt2folia -o '-' --id=" + shellsafe(docid, '"') + " " + shellsafe(intermediatefile,'"') + " > " + shellsafe(outputfilepath,'"') )
        #to be implemented:
        #intermediatefile = outputfilepath.replace('.folia.xml','') + '.pdf2xml.xml'
        #run("pdftohtml -s -i -noframes -stdout -xml " + shellsafe(inputfilepath,'"') + " " + shellsafe(intermediatefile,'"') )
        #run("pdfxml2folia " + shellsafe(intermediatefile,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'docx2folia_out':
        intermediatefile = outputfilepath.replace('.folia.xml','') + '.rst'
        run("pandoc --from=docx --to=rst " + shellsafe(inputfilepath,'"') + " > " + shellsafe(intermediatefile,'"') )
        run("rst2folia " + " ".join(rst2folia_args) + " " + shellsafe(intermediatefile,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'odt2folia_out':
        intermediatefile = outputfilepath.replace('.folia.xml','') + '.rst'
        run("pandoc --from=odt --to=rst " + shellsafe(inputfilepath,'"') + " > " + shellsafe(intermediatefile,'"') )
        run("rst2folia " + " ".join(rst2folia_args) + " " + shellsafe(intermediatefile,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'epub2folia_out':
        intermediatefile = outputfilepath.replace('.folia.xml','') + '.rst'
        run("pandoc --from=epub --to=rst " + shellsafe(inputfilepath,'"') + " > " + shellsafe(intermediatefile,'"') )
        run("rst2folia " + " ".join(rst2folia_args) + " " + shellsafe(intermediatefile,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'latex2folia_out':
        intermediatefile = outputfilepath.replace('.folia.xml','') + '.rst'
        run("pandoc --from=latex --to=rst " + shellsafe(inputfilepath,'"') + " > " + shellsafe(intermediatefile,'"') )
        run("rst2folia " + " ".join(rst2folia_args) + " " + shellsafe(intermediatefile,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'mediawiki2folia_out':
        intermediatefile = outputfilepath.replace('.folia.xml','') + '.rst'
        run("pandoc --from=mediawiki --to=rst " + shellsafe(inputfilepath,'"') + " > " + shellsafe(intermediatefile,'"') )
        run("rst2folia " + " ".join(rst2folia_args) + " " + shellsafe(intermediatefile,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'docbook2folia_out':
        intermediatefile = outputfilepath.replace('.folia.xml','') + '.rst'
        run("pandoc --from=docbook --to=rst " + shellsafe(inputfilepath,'"') + " > " + shellsafe(intermediatefile,'"') )
        run("rst2folia " + " ".join(rst2folia_args) + " " + shellsafe(intermediatefile,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'html2folia_out':
        intermediatefile = outputfilepath.replace('.folia.xml','') + '.rst'
        run("pandoc --from=html --to=rst " + shellsafe(inputfilepath,'"') + " > " + shellsafe(intermediatefile,'"') )
        run("rst2folia " + " ".join(rst2folia_args) + " " + shellsafe(intermediatefile,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'conllu2folia_out':
        run("conllu2folia --id=" + shellsafe(docid, '"') + " --outputfile " + shellsafe(outputfilepath,'"') + " " +  shellsafe(inputfilepath,'"') )

    elif outputtemplate_id == 'alpino2folia_out':
        run("alpino2folia " + shellsafe(inputfilepath,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'tei2folia_out':
        run("tei2folia -o '-' " + shellsafe(inputfilepath,'"') + " > " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'naf2folia_out':
        run("naf2folia " + shellsafe(inputfilepath,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'hocr2folia_out':
        #we can't override the output filename yet
        #run("FoLiA-hocr -O " + shellsafe(outputdir,'"') + " " + shellsafe(intermediatefile,'"')  )
        raise NotImplementedError

    elif outputtemplate_id == 'alto2folia_out':
        #we can't override the output filename yet
        #run("FoLiA-hocr -O " + shellsafe(outputdir,'"') + " " + shellsafe(intermediatefile,'"')  )
        raise NotImplementedError

    elif outputtemplate_id == 'folia2txt_out':
        run("folia2txt " + shellsafe(inputfilepath,'"') + " > " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'folia2rst_out':
        run("folia2rst " + shellsafe(inputfilepath,'"') + " " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'folia2html_out':
        run("folia2html " + shellsafe(inputfilepath,'"') + " > " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'foliavalidator_out':
        validationmode = clamdata.get('validationmode','fail')
        args = []
        if validationmode == "continue":
            args.append( "-i")
        if clamdata.get('autodeclare',False):
            args.append( "-a")
        if clamdata.get('deep',False):
            args.append( "-d")
        if clamdata.get('quick',False):
            args.append( "-q")
        if clamdata.get('fixunassignedprocessor',False):
            args.append( "--fixunassignedprocessor")
        run("foliavalidator " + " ".join(args) + " " + shellsafe(inputfilepath,'"') + " 2> " + shellsafe(outputfilepath,'"') )

    elif outputtemplate_id == 'foliaupgrade_out':
        args = ["--dryrun" ] #we set this so the original file isn't overwritten but we get output on stdout instead
        if clamdata.get('fixunassignedprocessor',False):
            args.append( "--fixunassignedprocessor")
        run("foliaupgrade " + " ".join(args) + " " + shellsafe(inputfilepath,'"') + " > " + shellsafe(outputfilepath,'"') )

clam.common.status.write(statusfile, "Done",100) # status update

sys.exit(0) #non-zero exit codes indicate an error and will be picked up by CLAM as such!
