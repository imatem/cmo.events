# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component.hooks import getSite

import os
import tempfile
import shutil


HEADER_LATEX_TEMPLATE = r"""

\documentclass[16pt]{scrartcl}
\usepackage[letterpaper,left=1.5cm,right=1.5cm,top=2cm,bottom=2cm,heightrounded]{geometry}
\usepackage{pdflscape}
\usepackage{setspace}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage[T1]{fontenc}
\usepackage{background}
%\SetBgContents{}
%
\usepackage{datatool} %% for mail merging, and read file
%
\def\signature#1#2{\parbox[b]{1in}{\smash{#1}\vskip12pt}
\hfill \parbox[t]{2.2in}{\shortstack{\vrule width 2.2in height 0.4pt\\\small#2}}}
\def\sigskip{\vskip0.4in plus 0.1in}
        \def\beginskip{\vskip0.5875in plus 0.1in}
% % some colors
\definecolor{cline}{RGB}{229,220,224}
%
\begin{document}

\sloppy
\begin{landscape}
    %\pagecolor{Bisque}
    %
"""

BODY_LATEX_TEMPLATE = r"""
    \pagestyle{empty}
        {
        \linespread{2}\selectfont
        \begin{minipage}[c]{9in}
            \includegraphics[width=1\textwidth]{header}
            \vskip-2.3em
            \noindent\makebox[\linewidth]{\color{cline}{{\rule{\textwidth}{2.5pt}}}}
        \end{minipage}
        \vskip3em

        \noindent
        \hspace*{\fill}
        \begin{minipage}[c]{6.2in}
            {\centering
            {\onehalfspacing
            {\Large\bfseries{CERTIFICATE}\par}
            \vskip2em
            {This is to certify that:\par}
            \vskip2em
            {\large{\selectfont{\sc{\bfseries %s}}\par}}
            \par}}
        \end{minipage}
        \hspace*{\fill}
        
        \vskip3em
        
        {
        \noindent{
        \doublespacing
        has attended the ``%s'' workshop, held from %s, at %s, Oaxaca, Oax. Mexico.
        }}
        
        \noindent
        {\singlespacing
        \vfill
        
        \hspace*{\fill}
        \begin{minipage}[l]{2.25in}
            {\centering
            {\onehalfspacing
                  \sigskip \signature{}{Dr. Jos\'e Seade Kuri\\ Director\\ Casa Matem\'atica Oaxaca }
            \par}}
        \end{minipage}
        \hspace*{\fill}
       
        \vfill
        \pagebreak
        }
    }

"""

FOOTER_LATEX_TEMPLATE = r"""
\end{landscape}
%
\end{document}

"""


class CertificatesView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        apps = []
        self.form = self.request.form
        if self.request.form:
            if 'certificatebox' in self.request.form.keys():
                if type(self.request.form['certificatebox']) == str:
                    uids = [self.request.form['certificatebox']]
                else:
                    uids = self.request.form['certificatebox']
                for uid in uids:
                    brain = self.catalog.searchResults(
                        portal_type='Participant',
                        UID=uid,
                    )
                    if brain:
                        obj = brain[0].getObject()
                        firstname = obj.firstname
                        lastname = obj.lastname
                        name = firstname + ' ' + lastname
                        workshop = self.context.Title() + u''
                        start_date = self.context.start_date
                        end_date = self.context.end_date
                        textdate = self.fancyDate(start_date, end_date) + u''
                        place = u'at Los Laureles'
                        apps.append([name, workshop, textdate, place])
                        # \name=Name,\workshop=Workshop, \edate=Date, \place=place}
        if apps:
            pdfdata = self.createPDF(apps)
            pdffile = pdfdata[0]
            new_file = open(pdffile, "rb")
            self.request.response.setHeader(
                "Content-Disposition",
                "attachment; filename=%s.pdf" %
                'certificates'
            )
            self.request.response.setHeader("Content-Type", "application/pdf")
            # self.request.response.setHeader("Content-Length", len(pdfcontent))
            # self.request.response.setHeader('Last-Modified', DateTime.rfc822(DateTime()))
            # self.request.response.setHeader("Cache-Control", "no-store")
            # self.request.response.setHeader("Pragma", "no-cache")
            self.request.response.write(new_file.read())
            new_file.close()
            try:
                shutil.rmtree(pdfdata[1])  # remove tempdir
            except:
                pass
            return new_file
        return self.index()

    @property
    def catalog(self):
        return getToolByName(getSite(), 'portal_catalog')

    def participants(self):

        participants = {}
        if self.context.portal_type == 'Workshop':
            myview = self.context.unrestrictedTraverse('view')
            participants = myview.participantsWithcolumnOrder()
        return participants

    def fancyDate(self, start_date, end_date):

        month_name = {
            '1': 'January',
            '2': 'February',
            '3': 'March',
            '4': 'April',
            '5': 'May',
            '6': 'June',
            '7': 'July',
            '8': 'Augost',
            '9': 'September',
            '10': 'Octover',
            '11': 'November',
            '12': 'December',
        }

        syear = str(start_date.year)
        smonth = str(start_date.month)
        sday = str(start_date.day)
        eyear = str(end_date.year)
        emonth = str(end_date.month)
        eday = str(end_date.day)

        textdate = u''
        if syear == eyear:
            if smonth == emonth:
                textdate = month_name[smonth] + ' ' + sday + '-' + eday + ', ' + syear

            else:
                textdate = month_name[smonth] + ' ' + sday + '-' + month_name[emonth] + ' ' + eday + ', ' + syear

        else:
            textdate = month_name[smonth] + ' ' + sday + ' ' + syear
            textdate += '-'
            textdate += month_name[emonth] + ' ' + eday + ' ' + eyear + ', '

        return textdate

    def createPDF(self, participants):

        title_plan = "%s.tex" % ('certificates')
        mainTex = u'% !TEX encoding = UTF-8 Unicode\n'
        mainTex += HEADER_LATEX_TEMPLATE

        images = [item for item in getSite().values() if item.portal_type == 'Image']
        image = images[0]

        for participant in participants:

            mainTex += BODY_LATEX_TEMPLATE % (
                participant[0],
                participant[1],
                participant[2],
                participant[3],
            )
        mainTex += FOOTER_LATEX_TEMPLATE
        try:
            fileTex = mainTex.encode('utf-8', 'ignore')
            tempdir = tempfile.mkdtemp()
            file_path = os.path.join(tempdir, title_plan)
            file_os = open(file_path, 'wb')
            file_os.write(fileTex)
            file_os.close()

            image_path = os.path.join(tempdir, 'header.png')
            image_os = open(image_path, 'wb')
            image_os.write(image.image.data)
            image_os.close()

            os.system("cd {0}; pdflatex -interaction=nonstopmode {1}".format(tempdir, file_path))
        except:
            pass

        pdfname = file_path.replace('.tex', '.pdf')
        # os.system("cp {0} ~/Desktop".format(pdfname))
        return (pdfname, tempdir)
