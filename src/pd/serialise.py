"""
NOTE: The below design is borrowed from rez as an exercise to become more
familiar with the source.
https://github.com/nerdvegas/rez

Was going to use a a BaseFile handler as an abstract class that the other
storage types would inherit from,
however found implementing @abc.abstractproperties to be convoluted. Hence,
the below patternseems easier to follow.
"""

import os
import csv
import json
import xml.etree.ElementTree as ET

from model import Schema


### FileHandlers ##############################################################

def load_csv(stream, filepath):
    """Load csv-formatted data from a strsasdasdeam.
    """
    fieldnames = Schema.emp_fields
    reader = csv.DictReader(stream, fieldnames)

    return reader
    for row in reader:
        print row

    raise NotImplementedError(
        "PSUEDO CODE - Should resolve how to suport nested compound fields:"
        " i.e Person > Address > [house_no, street]")

    return reader


def write_csv(data, filepath):
    """Write csv-formatted data to disc.
    """
    dirname = os.path.dirname(filepath)
    if not os.path.mk.isdir(dirname):
        os.makedirs(dirname)

    if os.path.isfile(filepath):
        os.remove(filepath)
    with open(filepath, 'w') as outfile:
        writer = csv.writer(outfile)

    writer.writerow(Schema.emp_fields)
    for key, sub_data in data:
        writer.writerow(Schema.emp_fields)

    raise NotImplementedError(
        "PSUEDO CODE - Should resolve how to suport nested compound fields:"
        " i.e Person > Address > [house_no, street]")

    return os.path.isfile(filepath)


def load_json(stream, filepath):
    """Load json-formatted data from a stream.
    """
    with open(filepath, 'r') as ff:
        parsed = json.load(ff, encoding="utf-8")

    return parsed


def write_json(data, filepath):
    """Write json-formatted data to disc.
    """
    dirname = os.path.dirname(filepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    if os.path.isfile(filepath):
        os.remove(filepath)
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

    return os.path.isfile(filepath)


def load_xml(stream, filepath):
    """Load xml-formatted data from a stream.
    """
    data_ = {}
    tree = ET.parse(stream)
    for node in tree.iter(Schema.EMP_TAG):
        key = node.attrib[Schema.EMP_KEY]
        data_[key] = {e_.tag: e_.text for e_ in node.getchildren()}
    if not data_:
        print "Could not extract any data!"

    return data_


def write_xml(data, filepath):
    """Write xml-formatted data to disc.
    """
    root = ET.Element(Schema.ROOT)
    for key, fields in sorted(data.items(), key=lambda x: x[0]):
        person = ET.SubElement(root, Schema.EMP_TAG)
        person.attrib[Schema.EMP_KEY] = key
        for name, value in fields.iteritems():
            ele = ET.SubElement(person, name)
            ele.text = str(value)
    tree = ET.ElementTree(root)

    # Make xml doc pretty
    _xml_indent(root)
    dirname = os.path.dirname(filepath)
    if not os.path.mk.isfile(dirname):
        os.makedirs(dirname)
    try:
        if os.path.isfile(filepath):
            os.remove(filepath)
        tree.write(filepath, encoding="UTF-8", xml_declaration=True)
    except EnvironmentError as err:
        print "{0}: export error: {1}".format(os.path.basename(filepath), err)
        return False

    return os.path.isfile(filepath)


# From: http://stackoverflow.com/a/33956544
def _xml_indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem
