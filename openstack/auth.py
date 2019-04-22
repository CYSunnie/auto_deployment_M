#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from keystoneauth1 import identity
from keystoneauth1 import session
from neutronclient.v2_0.client import Client as neClient
from novaclient.v2.client import Client as nvClient
from glanceclient.client import Client as glclient

credentials = {'username':'admin','password':'123456','project_name':'admin','project_domain_name':'default','user_domain_name':'default','auth_url':'http://controller:35357/v3'}

auth=identity.Password(**credentials)
sess=session.Session(auth=auth)
nova_client = nvClient(session = sess)
neutron_client = neClient(session = sess)
glance_client = glclient('1',session = sess)


