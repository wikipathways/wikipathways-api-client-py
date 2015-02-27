###
# Test script for new WikiPathways webservice API
# author: msk (mkutmon@gmail.com)
###

import requests
import getpass
from lxml import etree as ET

##################################
# variables

username = 'Mkutmon'
gpml_file = 'test.gpml'
wp_id = 'WP4'
basis_url = 'http://pvjs.wikipathways.org/wpi/webservicetest/'
description = 'test update webservice function'

# update revision!!
revision = "78846"

##################################

# define namespaces
namespaces = {'ns1':'http://www.wso2.org/php/xsd','ns2':'http://www.wikipathways.org/webservice'}

# login
password = getpass.getpass('Password:')
auth = {'name' : username , 'pass' : password}
r_login = requests.get(basis_url + 'login', params=auth)
dom = ET.fromstring(r_login.text)

authentication = ''
for node in dom.findall('ns1:auth', namespaces):
	authentication = node.text

# read gpml file
f = open(gpml_file, 'r')
gpml = f.read()

# update pathway
update_params = {'pwId': wp_id, 'description' : description, 'gpml' : gpml, 'revision' : revision, 'auth' : authentication, 'username': username}
requests.post(basis_url + 'updatePathway', params=update_params)
