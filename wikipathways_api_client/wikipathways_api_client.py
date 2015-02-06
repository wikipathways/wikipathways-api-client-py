import requests
import getpass
from lxml import etree as ET
import base64

class WikipathwaysApiClient(object):
    """Returns :class:`WikipathwaysApiClient` object.
    :param identifier: WikiPathways ID for the new :class:`WikipathwaysApiClient` object.
    """


    api_to_standard_term_mappings = {
        'id': 'identifier',
        'ids': 'identifiers',
        'pwId': 'identifier',
        'revision': 'version',
        'graphId': 'elementIdentifiers',
        'color': 'colors',
        'fileType': 'fileFormat',
        'species': 'organism',
        'url': 'webPage',
        'codes': 'systemCodes'
    }


    def __init__(self, base_iri=None):
        if base_iri is None:
            base_iri = 'http://www.wikipathways.org/wpi/webservicetest/'
        self.base_iri = base_iri

        # define namespaces
        self.NAMESPACES = {'ns1':'http://www.wso2.org/php/xsd','ns2':'http://www.wikipathways.org/webservice/'}


    def __convert_standard_terms_to_api_terms(self, input_params):
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


    def __convert_api_terms_to_standard_terms(self, input_object):
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


    def create_pathway(self):
        ###
        # author: msk (mkutmon@gmail.com)
        ###

        # login
        pswd = getpass.getpass('Password:')
        auth = {'name' : username , 'pass' : pswd}
        r_login = requests.get('http://test2.wikipathways.org/wpi/webservicetest/?method=login&format=xml', params=auth)
        dom = ET.fromstring(r_login.text)

        authentication = ''
        for node in dom.findall('ns1:auth', namespaces):
                authentication = node.text

        # read gpml file
        f = open(gpml_file, 'r')
        gpml = f.read()

        # create pathway
        update_params = {'auth' : username+'-'+authentication, 'gpml': gpml}
        re = requests.post('http://test2.wikipathways.org/wpi/webservicetest/?method=createPathway&format=xml', params=update_params)
        print re.text


    def get_colored_pathway(self, input_params):
        request_params = self.__convert_standard_terms_to_api_terms(input_params)
        response = requests.get(self.base_iri + 'getColoredPathway', params=request_params)
        dom = ET.fromstring(response.text)
        node = dom.find('ns1:data', self.NAMESPACES)
        file = base64.b64decode(node.text) ### decode this file
        return file


    def get_pathway_as(self, input_params):
        request_params = self.__convert_standard_terms_to_api_terms(input_params)
        response = requests.get(self.base_iri + 'getPathwayAs', params=request_params)
        dom = ET.fromstring(response.text)
        node = dom.find('ns1:data', self.NAMESPACES)
        response_string = base64.b64decode(node.text) ### decode this file
        if request_params['fileType'] == 'gpml' or request_params['fileType'] == 'biopax' or request_params['fileType'] == 'svg':
            response = ET.fromstring(response_string)
        else:
            response = response_string
        return response


    def get_pathway_info(self, identifier, **kwargs):
        """Sends a GET request. Returns :dict:`info` object.
        :param identifier: WikiPathways ID
        :param \*\*kwargs: Optional arguments that ``get_pathway_info`` takes.
        """

        #kwargs.setdefault('allow_redirects', True)

        request_params = {'pwId' : identifier}
        response = requests.get(self.base_iri + '?method=getPathwayInfo&format=xml', params=request_params)
        dom = ET.fromstring(response.text)

        info_api_terms = {}
        for node in dom.findall('ns1:pathwayInfo', self.NAMESPACES):
            for attribute in node:
                info_api_terms[ET.QName(attribute).localname] = attribute.text
        info = self.__convert_api_terms_to_standard_terms(info_api_terms)
        return info


    def find_pathways_by_text(self, input_params):
        """Sends a GET request. Returns list of dictionary references.
        :param input_params
        :param input_params['query']: Text to search for
        :param [input_params['organism']]: Limit to organism with given name
        """

        request_params = self.__convert_standard_terms_to_api_terms(input_params)
        response = requests.get(self.base_iri + '?method=findPathwaysByText&format=xml', params=request_params)
        dom = ET.fromstring(response.text)

        pathways_api_terms = {}
        for node in dom.findall('ns1:result', self.NAMESPACES):
            for child in node:
                pathways_api_terms[ET.QName(child).localname] = child.text
        pathways = self.__convert_api_terms_to_standard_terms(pathways_api_terms)
        return pathways


    def find_pathways_by_xref(self, input_params):
        """Sends a GET request. Returns list of dictionary references.
        :param input_params
        :param input_params['systemCodes']: List of one or more BridgeDb system codes
        :param [input_params['identifiers']]: List of one or more entity reference identifiers
        """

        request_params = self.__convert_standard_terms_to_api_terms(input_params)
        response = requests.get(self.base_iri + '?method=findPathwaysByXref&format=xml', params=request_params)
        dom = ET.fromstring(response.text)

        pathways_api_terms = {}
        for node in dom.findall('ns1:result', self.NAMESPACES):
            for child in node:
                pathways_api_terms[ET.QName(child).localname] = child.text
        pathways = self.__convert_api_terms_to_standard_terms(pathways_api_terms)
        return pathways


    def list_organisms(self):
        """Sends a GET request. Returns :list:`organisms` object, each an organism name as a string.
        """
        response = requests.get(self.base_iri + 'listOrganisms')
        dom = ET.fromstring(response.text)

        organisms = []
        for node in dom:
            organisms.append(node.text)

        return organisms


    # list pathways
    def list_pathways(self, organism):
        request_params = {'organism': organism}
        response = requests.get(self.base_iri + 'listPathways', params=request_params)
        dom = ET.fromstring(response.text)

        pathways = []
        for pathway_node in dom.findall('ns1:pathways', self.NAMESPACES):
            pathway_using_api_terms = {}
            for child_node in pathway_node:
                pathway_using_api_terms[ET.QName(child_node).localname] = child_node.text
            pathway = self.__convert_api_terms_to_standard_terms(pathway_using_api_terms)
            pathways.append(pathway)

        return pathways
