"""
Subcommand for downloading and extracting dbGap 
phenotype dictionaries to TSV.
"""
import os
from kmh_dbgap_utils.dbgap import DbGapFtp

from kmh_dbgap_utils.subcommands import Subcommand
from kmh_dbgap_utils.logger import Logger
from kmh_dbgap_utils.parsers import PhenoDictParser


class ExtractDataDict(Subcommand):
    @classmethod
    def __add_arguments__(cls, parser):
        """Add the arguments to the parser"""
        # Input group
        parser.add_argument('--phs', type=str, required=True,
                       help="phsid of the project you want to extract")
        parser.add_argument('--outdir', type=str, required=True,
                       help='The directory to put results in')


    @classmethod
    def __get_description__(cls):
        """
        Optionally returns description
        """
        return "Download phenotype dictionaries and make TSV."


    @classmethod
    def main(cls, options): 
        logger = Logger.get_logger(cls.__tool_name__())
        logger.info("Download dbGap phenotype dictionaries.")
        logger.info("PHS: {0}".format(options.phs))

        # Parse phs
        phs = DbGapFtp.parse_phs(options.phs)

        # outputs
        ofile = os.path.join(options.outdir,
                             '{fullid}.data_dict.tsv'.format(**phs))
        logger.info("Extracting outputs to {0}".format(ofile))
        ohead = ['study_phs', 'study_name', 
                 'xml_file'] + PhenoDictParser.columns()

        # dbgap client
        dbgap = DbGapFtp()
        study_name = dbgap.get_study_details(phs, options.outdir) 
        logger.info("Study name: {0}".format(study_name))
        with open(ofile, 'wt') as o:
            o.write('\t'.join(ohead) + '\n')
            for xml_file, dat in dbgap.iter_study_xmls(phs, 'data_dict.xml',
                                                       options.outdir):
                parser = PhenoDictParser(dat)
                for record in parser:
                    row = [phs['fullid'], study_name, xml_file] + [
                           record[i] for i in PhenoDictParser.columns()]
                    o.write('\t'.join(row) + '\n')

        logger.info("Finished")
