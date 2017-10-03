# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component.hooks import getSite
from collections import OrderedDict

import os
import tempfile
import shutil
import re
import unicodecsv as csv
from Products.CMFPlone.utils import safe_unicode
from plone import api
from smtplib import SMTPException, SMTPRecipientsRefused
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


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
            {\Large\bfseries{%s}\par}
            \vskip2em
            {%s\par}
            \vskip2em
            {\large{\selectfont{\sc{\bfseries %s}}\par}}
            \par}}
        \end{minipage}
        \hspace*{\fill}

        \vskip3em

        {
        \noindent{
        \doublespacing
        %s
        }}

        \noindent
        {\singlespacing
        \vfill

        \hspace*{\fill}
        \begin{minipage}[l]{2.25in}
            {\centering
            {\onehalfspacing
                  \sigskip \signature{}{%s\\ %s\\ %s}
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
        uids = []
        self.form = self.request.form

        if self.request.form:
            formkeys = self.request.form.keys()
            if 'certificatebox' in formkeys:
                if type(self.request.form['certificatebox']) == str:
                    uids = [self.request.form['certificatebox']]
                else:
                    uids = self.request.form['certificatebox']

            if not uids:
                return self.index()

            if 'email_option' in formkeys:
                self.send_email(uids)
                # api.portal.show_message((u'Sended!'), self.request, type=u'info')
                return self.index()

            if 'getcertificates' in formkeys:
                apps = self.dataforcertificate(uids)

                if apps:
                    pdfdata = self.createPDF2(apps)
                    if not pdfdata:
                        return self.index()
                    self.request.response.setHeader(
                        "Content-Disposition",
                        "attachment; filename=%s.pdf" %
                        'certificates'
                    )

            if 'getbadges' in formkeys:
                apps = self.dataforbadge(uids)
                if apps:
                    pdfdata = self.createBadgePDF(apps)
                    if not pdfdata:
                        return self.index()
                    self.request.response.setHeader(
                        "Content-Disposition",
                        "attachment; filename=%s.pdf" %
                        'badges'
                    )

            pdffile = pdfdata[0]
            new_file = open(pdffile, "rb")

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

    def urltoworkshop(self):
        return self.context.absolute_url()

    def participants(self):

        participants = {}
        if self.context.portal_type == 'Workshop':
            myview = self.context.unrestrictedTraverse('view')
            participants = myview.participantsWithcolumnOrder(['Confirmed',])

        return participants



    def dataforcertificate(self, uids):
        certificates = self.getInstanceCertificate()
        if not certificates:
            return []

        certificate = certificates[0]

        # this dictionary is static, change for generic
        fields_certificate = OrderedDict()
        fields_certificate['subheader'] = certificate.subheader
        fields_certificate['preamble'] = certificate.preamble
        fields_certificate['participantdata'] = certificate.participantdata
        fields_certificate['bodydescription'] = certificate.bodydescription
        fields_certificate['signaturename'] = certificate.signaturename
        fields_certificate['signatureappointment'] = certificate.signatureappointment
        fields_certificate['signatureinst'] = certificate.signatureinst

        apps = []
        for uid in uids:
            brain = self.catalog.searchResults(
                portal_type='Participant',
                UID=uid,
            )
            if brain:
                obj = brain[0].getObject()
                lparticipant = []
                for cvalue in fields_certificate.values():
                    lparticipant.append(self.parseValue(obj, cvalue))

                apps.append(lparticipant)

        return apps

    def dataforbadge(self, uids):
        apps = []
        for uid in uids:
            brain = self.catalog.searchResults(
                portal_type='Participant',
                UID=uid,
            )
            if brain:
                obj = brain[0].getObject()
                lparticipant = []
                name = obj.firstname + ' ' + obj.lastname
                lparticipant.append(name)
                lparticipant.append(obj.affiliation)
                lparticipant.append(self.context.title)
                apps.append(lparticipant)

        return apps


    def parseValue(self, obj, field_value):

        listvalues = field_value.split(' ')
        regex = re.compile('[^a-zA-Z]')

        participant_fields = {}

        exclude_names = []
        # exclude_names = (
        #     'IBasic.title',
        #     'IBasic.description',
        #     'description',
        #     'title'
        # )

        viewitem = obj.unrestrictedTraverse('view')
        viewitem.update()

        default_widgets = viewitem.widgets.values()

        for widget in default_widgets:
            if widget.__name__ not in exclude_names:
                participant_fields[widget.name.split('.')[-1]] = widget.value

        groups = viewitem.groups
        for group in groups:
            widgetsg = group.widgets.values()
            for widget in widgetsg:
                participant_fields[widget.name.split('.')[-1]] = widget.value

        # for workshops
        workshop_fields = {}
        viewitem = self.context.unrestrictedTraverse('view')
        viewitem.update()

        default_widgets = viewitem.widgets.values()

        for widget in default_widgets:
            if widget.__name__ not in exclude_names:
                workshop_fields[widget.name.split('.')[-1]] = widget.value

        groups = viewitem.groups
        for group in groups:
            widgetsg = group.widgets.values()
            for widget in widgetsg:
                workshop_fields[widget.name.split('.')[-1]] = widget.value

        newListvalues = []

        for value in listvalues:
            newvalue = value

            if '$Participant:' in value:
                vsplit = value.split(':')
                if len(vsplit) >= 2:
                    vfield = vsplit[1]
                    field_name = regex.sub('', vfield)
                    if field_name in participant_fields.keys():
                        newvalue = value.replace('$Participant:' + field_name, participant_fields[field_name])

            if '$Workshop:' in value:
                vsplit = value.split(':')
                if len(vsplit) >= 2:
                    vfield = vsplit[1]
                    field_name = regex.sub('', vfield)
                    if field_name in workshop_fields.keys():
                        newvalue = value.replace('$Workshop:' + field_name, workshop_fields[field_name])

            if '$fancyDate' in value:
                newvalue = value.replace('$fancyDate', self.fancyDate(workshop_fields['start_date'], workshop_fields['end_date']))

            newListvalues.append(safe_unicode(newvalue))

        return ' '.join(newListvalues)

    def fancyDate(self, start_date, end_date):

        month_name = {
            '01': 'January',
            '02': 'February',
            '03': 'March',
            '04': 'April',
            '05': 'May',
            '06': 'June',
            '07': 'July',
            '08': 'August',
            '09': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December',
        }

        sdate = start_date.split('-')
        edate = end_date.split('-')

        syear = sdate[0]
        smonth = sdate[1]
        sday = sdate[2]
        eyear = edate[0]
        emonth = edate[1]
        eday = edate[2]

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
                participant[0],  # 'subheader'
                participant[1],  # 'preamble'
                participant[2],  # 'participantdata'
                participant[3],  # 'bodydescription'
                participant[4],  # 'signaturename'
                participant[5],  # 'signatureappointment'
                participant[6],  # 'signatureinst'

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

    def getInstanceCertificate(self):

        certificates = [item for item in self.context.values() if item.portal_type == 'Certificate']
        if not certificates:
            bcertificates = self.catalog.searchResults(portal_type='Certificate',)
            if bcertificates:
                certificates = [bcertificates[0].getObject()]
        return certificates

    def createPDF2(self, participants):

        # \subheader, \preamble, \participantdata,
        # \bodydescription, \signaturename,
        # \signatureappointment, \signatureinst

        certificates = self.getInstanceCertificate()
        if not certificates:
            return None

        certificate = certificates[0]
        uidtemplate = certificate.ctemplate
        brain = self.catalog.searchResults(portal_type='Folder', UID=uidtemplate,)

        if brain:
            folder_template = brain[0].getObject()
            images = [item for item in folder_template.values() if item.portal_type == 'Image']
            texfiles = [item for item in folder_template.values() if item.portal_type == 'File']
        try:
            image = images[0]
            texfile = texfiles[0]
            imagesg = images[-1]
        except Exception:
            # return None
            raise Exception("No hay archivos de template")

        try:
            tempdir = tempfile.mkdtemp()
        except Exception:
            # return None
            raise Exception("No se pudo crear el temporal")

        #  For cvs file
        headers = [
            'subheader',
            'preamble',
            'participantdata',
            'bodydescription',
            'signaturename',
            'signatureappointment',
            'signatureinst',
        ]

        try:
            cvsfile_path = os.path.join(tempdir, 'namelist.csv')
            csvfile = open(cvsfile_path, 'wb')
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(headers)
            for participant in participants:
                writer.writerow([s.encode('utf8') for s in participant])

            csvfile.close()

            image_path = os.path.join(tempdir, 'header.png')
            image_os = open(image_path, 'wb')
            image_os.write(image.image.data)
            image_os.close()

            image_path = os.path.join(tempdir, 'sg.png')
            image_sg = open(image_path, 'wb')
            image_sg.write(imagesg.image.data)
            image_sg.close()

            title_plan = "%s.tex" % ('certificates')
            file_path = os.path.join(tempdir, title_plan)
            file_os = open(file_path, 'wb')
            file_os.write(texfile.file.data)
            file_os.close()
            os.system("cd {0}; pdflatex -interaction=nonstopmode {1}".format(tempdir, file_path))
            # applied double pdflatex for draft
            # os.system("cd {0}; pdflatex -interaction=nonstopmode {1}".format(tempdir, file_path))
        except Exception:
            # return None
            raise Exception("No se pudo ejecutar el latex")

        pdfname = file_path.replace('.tex', '.pdf')
        # os.system("cp {0} ~/Desktop".format(pdfname))
        return (pdfname, tempdir)

    def createBadgePDF(self, participants):

        # \name, \affiliation, \workshop,
        certificates = self.getInstanceCertificate()
        if not certificates:
            return None

        certificate = certificates[0]
        uidtemplate = certificate.ctemplate
        brain = self.catalog.searchResults(portal_type='Folder', UID=uidtemplate,)

        if brain:
            folder_template = brain[0].getObject()
            images = [item for item in folder_template.values() if item.portal_type == 'Image']
            texfiles = [item for item in folder_template.values() if item.portal_type == 'File']
        try:
            image = images[1]
            texfile = texfiles[1]
        except Exception:
            return None

        try:
            tempdir = tempfile.mkdtemp()
        except Exception:
            return None

        #  For cvs file
        headers = [
            'Name',
            'Affiliation',
            'Workshop',
        ]

        try:
            cvsfile_path = os.path.join(tempdir, 'names.csv')
            csvfile = open(cvsfile_path, 'wb')
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(headers)
            for participant in participants:
                # writer.writerow([s.encode('utf8') for s in participant])
                allvaluesp = []
                for vpr in participant:
                    if vpr:
                        allvaluesp.append(vpr.encode('utf8'))
                    else:
                        allvaluesp.append('')

                writer.writerow(allvaluesp)


            csvfile.close()

            image_path = os.path.join(tempdir, 'header-small.png')
            image_os = open(image_path, 'wb')
            image_os.write(image.image.data)
            image_os.close()

            title_plan = "%s.tex" % ('badges')
            file_path = os.path.join(tempdir, title_plan)
            file_os = open(file_path, 'wb')
            file_os.write(texfile.file.data)
            file_os.close()
            os.system("cd {0}; xelatex -interaction=nonstopmode {1}".format(tempdir, file_path))
        except Exception:
            return None

        pdfname = file_path.replace('.tex', '.pdf')
        # os.system("cp {0} ~/Desktop".format(pdfname))
        return (pdfname, tempdir)

    def send_email(self, participants):
        for uiditem in participants:
            brains = self.catalog.searchResults(portal_type='Participant', UID=uiditem,)
            if brains:
                obj = brains[0].getObject()
                data = self.dataforcertificate([uiditem])
                pdfdata = self.createPDF2(data)
                participant_email = obj.email
                participant_name = obj.firstname + ' ' + obj.lastname
                workshop_title = self.context.title

                if not pdfdata:
                    continue

                mail_text = 'Dear %s:' % (participant_name)
                mail_text += u'\n Please find attached your certificate of '
                mail_text += workshop_title
                mail_text += u'.\n\n\n\n'
                mail_text += u' Best regards, \n'
                mail_text += u'Claudia Arias Cao Romero \n'
                mail_text += u'Conference Program Coordinator \n'
                mail_text += u'Casa Matemática Oaxaca \n'

                pdffile = open(pdfdata[0], "rb")
                pdf = MIMEApplication(pdffile.read(), _subtype='pdf')
                pdf.add_header('content-disposition', 'attachment', filename='certificate.pdf')
                text = MIMEText(mail_text, _charset='UTF-8')
                message = MIMEMultipart(_subparts=(text, pdf))

                participant_email += ', cmo-birs@im.unam.mx'
                try:
                    api.portal.send_email(
                        recipient=participant_email,
                        sender='cmo-birs@im.unam.mx',
                        subject=workshop_title + ' Certificate',
                        body=message,
                    )
                except SMTPRecipientsRefused:
                    # Don't disclose email address on failure
                    raise SMTPRecipientsRefused('Recipient address rejected by server')

                pdffile.close()
                obj.certificatesended = u'Yes'

            try:
                shutil.rmtree(pdfdata[1])  # remove tempdir
            except:
                pass

        return True

    def tableContentInformation(self):

        information = OrderedDict()
        viewitem = self.context.unrestrictedTraverse('view')
        viewitem.update()
        default_widgets = viewitem.widgets.values()
        exclude_names = ['press_release', 'description']

        for widget in default_widgets:
            if widget.__name__ not in exclude_names:
                information[widget.label] = widget.value
        return information
