import requests
import getpass
from lxml import etree as ET
import base64

class WikipathwaysApiClient(object):
    """Returns :class:`WikipathwaysApiClient` object.
    :param identifier: WikiPathways ID for the new :class:`WikipathwaysApiClient` object.
    """


    def invert_dict(dictionary):
        return dict((v, k) for k, v in dictionary.iteritems())


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

    english_name_to_iri_mappings = {
            'African malaria mosquito': 'http://identifiers.org/taxonomy/7165',
            'beet': 'http://identifiers.org/taxonomy/161934',
            'thale cress': 'http://identifiers.org/taxonomy/3702',
            'cattle': 'http://identifiers.org/taxonomy/9913',
            'roundworm': 'http://identifiers.org/taxonomy/6239',
            'dog': 'http://identifiers.org/taxonomy/9615',
            'sea vase': 'http://identifiers.org/taxonomy/7719',
            'zebrafish': 'http://identifiers.org/taxonomy/7955',
            'fruit fly': 'http://identifiers.org/taxonomy/7227',
            'Escherichia coli': 'http://identifiers.org/taxonomy/562',
            'horse': 'http://identifiers.org/taxonomy/9796',
            'chicken': 'http://identifiers.org/taxonomy/9031',
            'soybean': 'http://identifiers.org/taxonomy/3847',
            'human': 'http://identifiers.org/taxonomy/9606',
            'barley': 'http://identifiers.org/taxonomy/4513',
            'Rhesus monkey': 'http://identifiers.org/taxonomy/9544',
            'mouse': 'http://identifiers.org/taxonomy/10090',
            'platypus': 'http://identifiers.org/taxonomy/9258',
            'long-grained rice': 'http://identifiers.org/taxonomy/39946',
            'rice': 'http://identifiers.org/taxonomy/4530',
            'black cottonwood': 'http://identifiers.org/taxonomy/3694',
            'chimpanzee': 'http://identifiers.org/taxonomy/9598',
            'Norway rat': 'http://identifiers.org/taxonomy/10116',
            'baker\'s yeast': 'http://identifiers.org/taxonomy/4932',
            'tomato': 'http://identifiers.org/taxonomy/4081',
            'pig': 'http://identifiers.org/taxonomy/9823',
            'wine grape': 'http://identifiers.org/taxonomy/29760',
            'western clawed frog': 'http://identifiers.org/taxonomy/8364',
            'maize': 'http://identifiers.org/taxonomy/4577'
    }

    iri_to_english_name_mappings = invert_dict(english_name_to_iri_mappings)


    latin_name_to_iri_mappings = {
            'Anopheles gambiae': 'http://identifiers.org/taxonomy/7165',
            'Arabidopsis thaliana': 'http://identifiers.org/taxonomy/3702',
            'Aspergillus niger': 'http://identifiers.org/taxonomy/5061',
            'Bacillus subtilis': 'http://identifiers.org/taxonomy/1423',
            'Beta vulgaris': 'http://identifiers.org/taxonomy/161934',
            'Bos taurus': 'http://identifiers.org/taxonomy/9913',
            'Caenorhabditis elegans': 'http://identifiers.org/taxonomy/6239',
            'Canis familiaris': 'http://identifiers.org/taxonomy/9615',
            'Ciona intestinalis': 'http://identifiers.org/taxonomy/7719',
            'Ruminiclostridium thermocellum': 'http://identifiers.org/taxonomy/1515',
            'Clostridium thermocellum': 'http://identifiers.org/taxonomy/1515',
            'Danio rerio': 'http://identifiers.org/taxonomy/7955',
            'Drosophila melanogaster': 'http://identifiers.org/taxonomy/7227',
            'Escherichia coli': 'http://identifiers.org/taxonomy/562',
            'Equus caballus': 'http://identifiers.org/taxonomy/9796',
            'Gallus gallus': 'http://identifiers.org/taxonomy/9031',
            'Gibberella zeae': 'http://identifiers.org/taxonomy/5518',
            'Glycine max': 'http://identifiers.org/taxonomy/3847',
            'Homo sapiens': 'http://identifiers.org/taxonomy/9606',
            'Hordeum vulgare': 'http://identifiers.org/taxonomy/4513',
            'Macaca mulatta': 'http://identifiers.org/taxonomy/9544',
            'Mus musculus': 'http://identifiers.org/taxonomy/10090',
            'Mycobacterium tuberculosis': 'http://identifiers.org/taxonomy/1773',
            'Ornithorhynchus anatinus': 'http://identifiers.org/taxonomy/9258',
            'Oryza indica': 'http://identifiers.org/taxonomy/39946',
            'Oryza sativa': 'http://identifiers.org/taxonomy/4530',
            'Oryza sativa Indica Group': 'http://identifiers.org/taxonomy/39946',
            'Populus trichocarpa': 'http://identifiers.org/taxonomy/3694',
            'Pan troglodytes': 'http://identifiers.org/taxonomy/9598',
            'Rattus norvegicus': 'http://identifiers.org/taxonomy/10116',
            'Saccharomyces cerevisiae': 'http://identifiers.org/taxonomy/4932',
            'Solanum lycopersicum': 'http://identifiers.org/taxonomy/4081',
            'Sus scrofa': 'http://identifiers.org/taxonomy/9823',
            'Vitis vinifera': 'http://identifiers.org/taxonomy/29760',
            'Xenopus tropicalis': 'http://identifiers.org/taxonomy/8364',
            'Zea mays': 'http://identifiers.org/taxonomy/4577'
    }


    def __init__(self, base_iri=None):
        if base_iri is None:
            base_iri = 'http://webservice.wikipathways.org/'
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


    def __convert_organism_string_to_dict(self, organism_string):
        if hasattr(self, 'organism_dicts'):
            organism_dicts = self.organism_dicts
        else:
            organism_dicts = self.organism_dicts = self.list_organisms()

        for organism_dict in organism_dicts:
            if organism_dict['@id'] == organism_string:
                return organism_dict
            elif organism_dict['name']['la'] == organism_string:
                return organism_dict
            elif organism_dict['name'].get('en') and organism_dict['name']['en'] == organism_string:
                return organism_dict


    def create_pathway(self):
        ###
        # author: msk (mkutmon@gmail.com)
        ###

        # login
        pswd = getpass.getpass('Password:')
        auth = {'name' : username , 'pass' : pswd}
        r_login = requests.get(self.base_iri + 'login', params=auth)
        dom = ET.fromstring(r_login.text)

        authentication = ''
        for node in dom.findall('ns1:auth', namespaces):
                authentication = node.text

        # read gpml file
        f = open(gpml_file, 'r')
        gpml = f.read()

        # create pathway
        update_params = {'auth' : username+'-'+authentication, 'gpml': gpml}
        re = requests.post(self.base_iri + 'createPathway', params=update_params)
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
        response = requests.get(self.base_iri + 'getPathwayInfo', params=request_params)
        dom = ET.fromstring(response.text)

        info_api_terms = {}
        for node in dom.findall('ns1:pathwayInfo', self.NAMESPACES):
            for attribute in node:
                info_api_terms[ET.QName(attribute).localname] = attribute.text
        info = self.__convert_api_terms_to_standard_terms(info_api_terms)

        if info.get('organism') and isinstance(info['organism'], basestring):
            info['organism'] = self.__convert_organism_string_to_dict(info['organism'])

        return info


    def find_pathways_by_text(self, input_params):
        """Sends a GET request. Returns list of dictionary references.
        :param input_params
        :param input_params['query']: Text to search for
        :param [input_params['organism']]: Limit to organism with given name
        """

        request_params = self.__convert_standard_terms_to_api_terms(input_params)
        response = requests.get(self.base_iri + 'findPathwaysByText', params=request_params)
        dom = ET.fromstring(response.text)

        pathways = []
        for node in dom.findall('ns1:result', self.NAMESPACES):
            pathway_using_api_terms = {}
            for child in node:
                pathway_using_api_terms[ET.QName(child).localname] = child.text
                #print pathways_api_terms
            pathway = self.__convert_api_terms_to_standard_terms(pathway_using_api_terms)
            pathways.append(pathway)
        return pathways


    def find_pathways_by_xref(self, input_params):
        """Sends a GET request. Returns list of dictionary references.
        :param input_params
        :param input_params['systemCodes']: List of one or more BridgeDb system codes
        :param [input_params['identifiers']]: List of one or more entity reference identifiers
        """

        request_params = self.__convert_standard_terms_to_api_terms(input_params)
        response = requests.get(self.base_iri + 'findPathwaysByXref', params=request_params)
        dom = ET.fromstring(response.text)

        pathways = []
        for resultNode in dom.findall('ns1:result', self.NAMESPACES):
            pathway_using_api_terms = {}
            pathway_using_api_terms['fields'] = []
            for childNode in resultNode:
                if ET.QName(childNode).localname != 'fields':
                    pathway_using_api_terms[ET.QName(childNode).localname] = childNode.text
                elif ET.QName(childNode).localname == 'fields':
                    field = {}
                    for fieldChildNode in childNode:
                        #TODO standardize names & values from fieldChildNode.text
                        field[ET.QName(fieldChildNode).localname] = fieldChildNode.text
                    pathway_using_api_terms['fields'].append(field)
            pathway = self.__convert_api_terms_to_standard_terms(pathway_using_api_terms)
            pathways.append(pathway)
        return pathways


    def list_organisms(self):
        """Sends a GET request. Returns :list:`organisms` object, each an organism as a dict,
        with the IRI, Latin name and English name (when available).
        """
        response = requests.get(self.base_iri + 'listOrganisms')
        dom = ET.fromstring(response.text)

        organisms = []
        for node in dom:
            organism = {}
            organism['@context'] = [
              {
                'name': {
                  '@id': 'biopax:name',
                  '@container': '@language'
                },
                'Organism': 'http://identifiers.org/snomedct/410607006'
              }
            ]
            organism['@type'] = 'Organism'
            organism['name'] = {}
            organism['name']['la'] = latin_name = node.text
            organism['@id'] = self.latin_name_to_iri_mappings[latin_name]
            english_name = self.iri_to_english_name_mappings.get(organism['@id'])
            if english_name != None:
                organism['name']['en'] = english_name
            organisms.append(organism)

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
