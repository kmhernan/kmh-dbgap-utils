"""Module containing constants and basic
navigation utils for dbgap.
"""
import os
from ftplib import FTP

from kmh_dbgap_utils.logger import Logger
from kmh_dbgap_utils.utils import load_xml_file

DBGAP_FTP_SERVER = "ftp.wip.ncbi.nlm.nih.gov"
DBGAP_STUDY_BASE = "/dbgap/studies/%(studyid)s/%(fullid)s"
STUDY_FILE_TEMPLATE = DBGAP_STUDY_BASE + "/GapExchange_%(fullid)s.xml"
STUDY_DIRECTORY_TEMPLATE = DBGAP_STUDY_BASE + "/pheno_variable_summaries"

class DbGapFtp:
    """
    Class for connecting to dbgap FTP with generic
    helper functions.
    """

    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.ftp = FTP(DBGAP_FTP_SERVER)
        self.logger.info("Connecting to dbgap FTP server {0}".format(
                         DBGAP_FTP_SERVER))
        self.ftp.login()

    def get_study_details(self, phs, outdir):
        """
        Gets the study name from the GapExchange file.
        :param phs: the parsed phs dictionary
        :param outdir: path to output directory
        :return: the project name
        """
        ft = STUDY_FILE_TEMPLATE % phs
        tf = os.path.join(outdir, os.path.basename(ft))
        self.logger.info("Getting study details...")
        self.download_file(ft, FileWrapper(tf))
        sname = None
        try:
            obj = load_xml_file(tf)
            res = obj.find('Studies')
            for item in res:
                cfg = item.find('Configuration')
                for child in cfg:
                    if child.tag.lower().startswith('studyname'):
                        if child.text:
                            sname = child.text.strip()
                            break
        finally:
            os.remove(tf)

        return sname

    def download_file(self, fname, target_file):
        """Class adapted from Mayo Clinic's dbgap packages
        https://github.com/crDDI/dbgap/blob/master/dbgap/file_downloader.py
        :param fname: the file to download from ftp
        :param target_file: the `FileWrapper` instance to download to
        """
        self.ftp.retrbinary('RETR ' + fname,
            lambda line: target_file.write(line.decode('utf-8')
                                           if isinstance(line, bytes)
                                           else line))

    @staticmethod
    def parse_phs(phs):
        """
        Parse phs into parts.
        :param phs: phs ID of the study
        :return: dictionary of the phs id parts
        """
        full_dbgapid = phs.split('.')
        dbgapid_parts = full_dbgapid[:3]
        dbgapid = {
            'studyid': dbgapid_parts[0],
            'versionedid': dbgapid_parts[0] + '.' + dbgapid_parts[1],
            'fullid': ".".join(dbgapid_parts)
        }
        return dbgapid

    def iter_study_xmls(self, phs, file_endswith, outdir):
        """
        For every file in the study directory that endswith the provided
        string, download, load XML, and yield object.
        """
        try:
            self.ftp.cwd(STUDY_DIRECTORY_TEMPLATE % phs)
        except Exception:
            self.logger.warn("Can't find " + STUDY_DIRECTORY_TEMPLATE % phs)
            pass

        for f in self.ftp.nlst():
            if f.endswith(file_endswith):
                tf = os.path.join(outdir, f)
                try:
                    self.logger.info("Downloading {0}...".format(f))
                    self.download_file(f, FileWrapper(tf))
                    obj = load_xml_file(tf)
                    yield f, obj

                finally:
                     os.remove(tf)

class FileWrapper:
    """Class adapted from Mayo Clinic's dbgap packages
    https://github.com/crDDI/dbgap/blob/master/dbgap/file_downloader.py
    """
    def __init__(self, fname=None):
        self.file = open(fname, 'w')

    def write(self, txt):
        self.file.write(txt.decode('utf-8') if isinstance(txt, bytes) else txt)

    def read(self):
        return self.file.read()
