"""Helper functions."""
import xml.etree.ElementTree as ET


def load_xml_file(fil):
    """
    Takes the file path and returns an XML object.
    :param fil: XML file path
    :return: XML object
    """
    res = None
    with open(fil, 'rt') as fh:
        dat = fh.read()
        res = ET.fromstring(dat)
    return res
