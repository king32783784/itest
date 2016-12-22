import os
import sys
import xml.dom.minidom


class Parsing_XML():
    '''Parsing XML-formatted files for Lart_i'''

    @staticmethod
    def parsing_label_list(labelname, xmlfile):
        '''Parsing Gets the list labels'''
        try:
            xml_dom = xml.dom.minidom.parse(xmlfile)
            xml_label = xml_dom.getElementsByTagName(labelname)
        except IOError:
            print 'Failed to open %s file,Please check it' % xmlfile
            exit(1)
        xml_label_list = []
        for single_label in xml_label:
            xml_label_list.append(single_label.firstChild.data)
        return xml_label_list

    @staticmethod
    def specific_elements(labelname, xmlfile):
        '''Read the specific elements,call the class may need to override
           this function.By default returns a "xml_list" and "xml_dict" a
           dictionary of xml_list specify a label for the list xml_dict
           key for the XML element, the corresponding value for a list of
           corresponding element tag content
        '''
        xml_labels = Parsing_XML.parsing_label_list(labelname, xmlfile)[0].split(' ')
        xml_elements_dict = {}
        for per_label in xml_labels:
            per_xml_label_list = Parsing_XML.parsing_label_list(per_label, xmlfile)
            xml_elements_dict[per_label] = per_xml_label_list
        xml_dict = {'xml_list': xml_labels, 'xml_dict': xml_elements_dict}
        return xml_dict
# case1:parsing Testsetup_sample.xml
#a = Parsing_XML.specific_elements('testtype', 'Setup.xml')
#print a
