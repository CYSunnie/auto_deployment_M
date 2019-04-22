#!/usr/bin/env python 

from colorama import init,Fore
from auth import neutron_client

net_list = neutron_client.list_networks()

def _res(success,**kwargs):
        kwargs['Success'] = 'True' if success else 'False'
        return kwargs

def create_network(network_name,network_ip):
	flag_name = False
	for net in net_list['networks']:
		if net['name'] == network_name:
			flag_name = True
		else:
			pass
	if flag_name:
		return _res(False,Reason='Name already exist')	
	else:
		body_sample = {'network':{'name':network_name}}
		netw = neutron_client.create_network(body = body_sample)
		net_dict = netw['network']
		network_id = net_dict['id']
		body_create_subnet = {'subnets':[{'name':'subnet_%s' % network_name,'cidr':network_ip,'ip_version':4,'network_id':network_id}]}
		subnet = neutron_client.create_subnet(body = body_create_subnet)
		#subnet_dict = subnet['subnets']
		return _res(True,Reason = 'Network %s has been created.' % net_dict['name'])

def delete_network(network_name):
	flag_name = False
	for net in net_list['networks']:
		if net['name'] == network_name:
			neutron_client.delete_network(net['id'])
			flag_name = True
		else:
			pass 	
	if flag_name:
		return _res(True,Reason = 'Network %s has been deleted.' % network_name)
	else:
		return _res(False,Reason = 'There is no network:%s in openstack,can not delete.' % network_name)


