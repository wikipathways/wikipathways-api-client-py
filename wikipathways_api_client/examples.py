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
    #fileType = 'png' ### svg, pdf
    file_format = 'svg' ### png, pdf
    wikipathways_id = "WP2062"

    element_identifiers=["ffffff90","ffffffe5"]
    colors = ["0000ff","0000ff"]

    file = wikipathways_api_client_instance.get_colored_pathway({
        'identifier': wikipathways_id,
        'version': 0,
        'elementIdentifiers': element_identifiers,
        'colors': colors,
        'fileFormat': file_format
    })
    print file
    '''

    # Get pathway with desired file format
    file = wikipathways_api_client_instance.get_pathway_as({
        'identifier': 'WP2062',
        'version': 0,
        'FileFormat': 'gpml'
    })
    print file

    '''
    pathways_all = wikipathways_api_client_instance.list_pathways(organism = 'Homo sapiens')
    print pathways_all
    '''

if __name__ == '__main__':
    main()
