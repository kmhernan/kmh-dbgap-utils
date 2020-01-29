"""Module containing pheno_dict and variable_report XML parsers.
These should yield dictionaries of parsed records.
"""
from kmh_dbgap_utils.logger import Logger


class PhenoDictParser:
    def __init__(self, etree):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self._item_iter = etree.iter('variable')

    @staticmethod
    def columns():
        return ['variable_id', 'name', 'type', 'description',
                'value', 'unit', 'logical_min', 'logical_max',
                'coll_interval', 'comment']

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self._item_iter)
        curr = {
          'variable_id': None,
          'name': [],
          'description': [],
          'type': [],
          'value': [],
          'unit': [],
          'logical_min': [],
          'logical_max': [],
          'coll_interval': [],
          'comment': []
        }
        iid = item.get('id')
        curr['variable_id'] = iid
        for child in item:
            if not child.tag:
                continue
            if child.tag == 'value':
                code = child.get('code')
                if code is not None and code != '':
                    curr['value'].append([code, child.text])
                else:
                    curr['value'].append([child.text])

            elif child.tag in ('name', 'description', 'type',
                               'unit', 'logical_min', 'logical_max',
                               'coll_interval', 'comment'):
                curr[child.tag].append(child.text)
            else:
                self.logger.warn("Ignoring {0} - {1} - {2}".format(
                                 child.tag, child.attrib, child.text))

        record = self._format_record(curr)
        return record

    def _format_record(self, record):
        record['name'] = record['name'][0] 
        record['type'] = "; ".join([i for i in record['type']
                                    if i is not None])
        record['description'] = "; ".join(record['description'])
        record['value'] = "; ".join(["=".join(i) for i in record['value']])
        record['unit'] = "; ".join(record["unit"])
        record['logical_min'] = "; ".join(record["logical_min"])
        record['logical_max'] = "; ".join(record["logical_max"])
        record['coll_interval'] = "; ".join(record["coll_interval"])
        record['comment'] = "; ".join(record["comment"])
        return record

class VariableReportParser:
    def __init__(self, etree):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self._item_iter = etree.iter('variable')

    @staticmethod
    def columns():
        return ['variable_id', 'name', 'calculated_type', 'reported_type',
                'description', 'enum_counts']

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self._item_iter)
        desc = item.find('description').text.strip()

        enum_stats = []
        for _enum in item.findall('total/stats/enum'):
            code = _enum.get('code', 'NA')
            count = _enum.get('count', 'NA')
            enum_val = _enum.text if _enum.text is not None else "NA"
            rec = " ".join([code, '-', enum_val, ':', count])
            enum_stats.append(rec)

        if enum_stats:
            record = {
                'variable_id': item.get('id', 'NA'),
                'name': item.get('var_name', 'NA'), 
                'calculated_type': item.get('calculated_type', 'NA'),
                'reported_type': item.get('reported_type', 'NA'),
                'description': desc,
                'enum_counts': "; ".join(enum_stats)  
            }
            return record
