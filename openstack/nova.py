#!/usr/bin/env python
# -*- coding:utf-8 -*-
from auth import nova_client
from port import change_portsecurity_false
import multiprocessing
import time

def _res(success, **kwargs):
	kwargs['Success'] = 'True' if success else 'False'
	return kwargs

def image_list():
	image_list = []
	images = nova_client.images.list()
	for image in images:
		image_list.append(image)
	return image_list

def flavor_list():
	flavor_list = []
	flavors = nova_client.flavors.list()
	for flavor in flavors:
		flavor_list.append(flavor)
	return flavor_list

def nic_list():
	nic_list = []
	nics = nova_client.networks.list()
	for nic in nics:
		nic_list.append(nic)
	return nic_list

def az_list():
	az_list = []
	azs = nova_client.availability_zones.list()
	for az in azs:
		az_list.append(az)
	return az_list

def start_a_instance(name,image,flavor,nic,az,param = None):
	server  = nova_client.servers.create(name = name , image = image, flavor = flavor, nics = [{'net-id':nic}], availability_zone = az)
	while(nova_client.servers.get(server).status == 'BUILD'):
		time.sleep(1)
		print 'building ...' + name + ' ' + server.status
	if(nova_client.servers.get(server).status == 'ERROR'):
		server.delete()
		print  'build '+ name + ' error and delete'
		return _res(False,Reason = 'Build instance:%s error and delete.' % name)
	else:
		print 'Create instance:' + name + '  successfully' 
	return _res(True,Reason = 'Create instance:%s successfully.' % name)

def start_a_router(name,image,flavor,az, *nic):
	network_list = []
	for net in nic:
		network_list.append({'net-id':net})
	server = nova_client.servers.create(name = name, image = image, flavor = flavor, nics = network_list, availability_zone = az)
	while(nova_client.servers.get(server).status == 'BUILD'):
                time.sleep(1)
                print 'building ...' + name + server.status
        if(nova_client.servers.get(server).status == 'ERROR'):
                server.delete()
                print 'build '+ name + ' error and delete'
                return _res(False,Reason = 'Build instance:%s error and delete.' % name)
        else:
                print 'Create instance:' + name + '  successfully'
	macs = []
	for k,v in nova_client.servers.get(server).addresses.items():
		macs.append(v[0].get('OS-EXT-IPS-MAC:mac_addr'))
	for mac in macs:
		change_portsecurity_false(mac)
    return _res(True,Reason = 'Create router:%s successfully.' % name)
		
def start_many_instance(count, image, flavor, nic, az, param = None):
	pool = multiprocessing.Pool(processes = 10)
	if count  > 250:
		print 'Too large count.'
		return 
	for i in range(count):
		random_date = '%.20f' % time.time()
		ins_name = 'JN' + random_date.translate(None, '.')	
		pool.apply_async(start_a_instance,[ins_name, image, flavor, nic, az])
	pool.close()
	pool.join()
	print 'Create successfully.'
