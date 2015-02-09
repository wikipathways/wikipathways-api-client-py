from wikipathways_api_client import WikipathwaysApiClient

def main():
    wikipathways_api_client_instance = WikipathwaysApiClient()

    '''
    '''
    # Get pathway info
    info = wikipathways_api_client_instance.get_pathway_info('WP274')
    print info

    '''
    # Get organisms
    organisms = wikipathways_api_client_instance.list_organisms()
    print organisms
    '''

    '''
    # Get colored pathway
    file = wikipathways_api_client_instance.get_colored_pathway({
        'identifier': 'WP2062',
        'version': 0,
        'elementIdentifiers': ["ffffff90","ffffffe5"],
        'colors': ["0000ff","0000ff"],
        'fileFormat': 'svg' ### png, pdf
    })
    print file
    '''

    '''
    # Get pathway with desired file format
    file = wikipathways_api_client_instance.get_pathway_as({
        'identifier': 'WP2062',
        'version': 0,
        'fileFormat': 'gpml'
    })
    print file
    '''

    '''
    pathways_all = wikipathways_api_client_instance.list_pathways(organism = 'Homo sapiens')
    print pathways_all
    '''

    '''
    # findPathwaysByText
    pathways_by_text = wikipathways_api_client_instance.find_pathways_by_text({
            'query': 'apoptosis'
        })
    print pathways_by_text 
    '''

    '''
    # findPathwaysByXref
    pathways_by_xref = wikipathways_api_client_instance.find_pathways_by_xref({
        'systemCodes': 'X',
        'identifiers': '201746_at'
    })
    print pathways_by_xref 
    '''

if __name__ == '__main__':
    main()
