from wikipathways_api_client import WikipathwaysApiClient

def main():
    wikipathways_api_client_instance = WikipathwaysApiClient()

    '''
    # Get pathway info
    info = wikipathways_api_client_instance.get_pathway_info('WP274')
    print info
    '''

    '''
    # Get organisms
    organisms = wikipathways_api_client_instance.list_organisms()
    print organisms
    '''

    '''
    # Get colored pathway
    kwargs = {
        'identifier': 'WP2062',
        'version': 0,
        'element_identifiers': ["ffffff90","ffffffe5"],
        'colors': ["#0000FF","#0000FF"],
        'file_format': 'image/svg+xml'
    }
    file = wikipathways_api_client_instance.get_colored_pathway(**kwargs)
    print file
    '''

    '''
    # Get pathway with desired file format
    kwargs = {
        'identifier': 'WP2062',
        'version': 0,
        'file_format': 'application/gpml+xml'
    }
    file = wikipathways_api_client_instance.get_pathway_as(**kwargs)
    print file
    '''

    '''
    pathways_all = wikipathways_api_client_instance.list_pathways(organism = 'Homo sapiens')
    print pathways_all
    '''

    '''
    # findPathwaysByText
    kwargs = {
        'query': 'apoptosis',
        'organism': 'http://identifiers.org/taxonomy/9606'
    }
    pathways_by_text = wikipathways_api_client_instance.find_pathways_by_text(**kwargs)
    print pathways_by_text 
    '''

    '''
    # findPathwaysByXref
    #kwargs = {
    #    'system_codes': ['X', 'L'],
    #    'identifiers': ['201746_at', '7040']
    #}
    kwargs = {
        '@id': [
            'http://identifiers.org/ncbigene/7040',
            'http://identifiers.org/affy.probeset/201746_at'
        ]
    }
    pathways_by_xref = wikipathways_api_client_instance.find_pathways_by_xref(**kwargs)
    print pathways_by_xref 
    '''

if __name__ == '__main__':
    main()
