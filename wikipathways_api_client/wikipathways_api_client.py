import requests
from lxml import etree as ET
import base64

class WikipathwaysApiClient(object):
    """Returns :class:`WikipathwaysApiClient` object.
    :param identifier: WikiPathways ID for the new :class:`WikipathwaysApiClient` object.
    """

    api_to_standard_term_mappings = {
        'id': 'identifier',
        'pwId': 'identifier',
        'revision': 'version',
        'graphId': 'element_identifiers',
        'color': 'colors',
        'fileType': 'FileFormat',
        'species': 'organism',
        'url': 'webPage'
    }

    def __init__(self, base_iri=None):
        if base_iri is None:
            base_iri = 'http://webservice.wikipathways.org/'
        self.base_iri = base_iri

        # define namespaces
        self.NAMESPACES = {'ns1':'http://www.wso2.org/php/xsd','ns2':'http://www.wikipathways.org/webservice/'}

    def convert_standard_terms_to_api_terms(self, input_params):
        terms_to_convert = self.api_to_standard_term_mappings
        standard_terms = terms_to_convert.values()
        api_terms = terms_to_convert.keys()

        request_params = {}
        for key, value in input_params.iteritems():
            if (key in standard_terms):
                def get_api_term(candidate_api_term):
                    return self.api_to_standard_term_mappings[candidate_api_term] == key

                api_term = filter(get_api_term, api_terms)[0]
                request_params[api_term] = input_params[key]
            else:
                request_params[key] = input_params[key]

        return request_params

    def convert_api_terms_to_standard_terms(self, input_object):
        terms_to_convert = self.api_to_standard_term_mappings
        standard_terms = terms_to_convert.values()
        api_terms = terms_to_convert.keys()

        output_object = {}
        for key, value in input_object.iteritems():
            if (key in api_terms):
                api_term = terms_to_convert[key]
                output_object[api_term] = input_object[key]
            else:
                output_object[key] = input_object[key]

        return output_object

    def get_pathway_info(self, identifier, **kwargs):
        """Sends a GET request. Returns :dict:`info` object.
        :param identifier: WikiPathways ID
        :param \*\*kwargs: Optional arguments that ``get_pathway_info`` takes.
        """

        #kwargs.setdefault('allow_redirects', True)

        request_params = {'pwId' : identifier}
        response = requests.get(self.base_iri + 'getPathwayInfo', params=request_params)
        dom = ET.fromstring(response.text)

        info_api_terms = {}
        for node in dom.findall('ns1:pathwayInfo', self.NAMESPACES):
            for attribute in node:
                info_api_terms[ET.QName(attribute).localname] = attribute.text
        info = self.convert_api_terms_to_standard_terms(info_api_terms)
        return info

    # list organisms
    def list_organisms(self):
        response = requests.get(self.base_iri + 'listOrganisms')
        dom = ET.fromstring(response.text)

        organisms = []
        for node in dom:
            organisms.append(node.text)

        return organisms

    def get_colored_pathway(self, input_params):
        request_params = self.convert_standard_terms_to_api_terms(input_params)
        response = requests.get(self.base_iri + 'getColoredPathway', params=request_params)
        dom = ET.fromstring(response.text)
        node = dom.find('ns1:data', self.NAMESPACES)
        file = base64.b64decode(node.text) ### decode this file
        return file

    def get_pathway_as(self, input_params):
        request_params = self.convert_standard_terms_to_api_terms(input_params)
        response = requests.get(self.base_iri + 'getPathwayAs', params=request_params)
        dom = ET.fromstring(response.text)
        node = dom.find('ns1:data', self.NAMESPACES)
        response_string = base64.b64decode(node.text) ### decode this file
        if request_params['fileType'] == 'gpml' or request_params['fileType'] == 'biopax' or request_params['fileType'] == 'svg':
            response = ET.fromstring(response_string)
        else:
            response = response_string
        return response

    # list pathways
    def list_pathways(self, organism):
        request_params = {'organism': organism}
        response = requests.get(self.base_iri + 'listPathways', params=request_params)
        dom = ET.fromstring(response.text)

        pathways = []
        for pathway_node in dom.findall('ns1:pathways', self.NAMESPACES):
            pathway_api_terms = {}
            for attribute in pathway_node:
                pathway_api_terms[ET.QName(attribute).localname] = attribute.text
            pathway = self.convert_api_terms_to_standard_terms(pathway_api_terms)
            pathways.append(pathway)

        return pathways
