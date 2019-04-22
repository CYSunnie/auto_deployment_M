#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from openstack.auth import nova_client
from openstack import nova
from openstack import network
from topology import read_xml
import time

class Network(object):
	def __init__(self):
		pass

	def deploy_network(self):
		network_info = read_xml.get_network_info()
		for net in network_info:
			network_name = net[0]
			network_ip = net[1]
			network.create_network(network_name,network_ip)
			print 'Create network %s' % network_name
		return True

	def delete_network(self):
		pass

class Node(object):
	def __init__(self):
		pass

	def deploy_router_node(self):
		router_info = read_xml.get_router_info()
		for router in router_info:
			router_name = router[0]
			router_image_name = router[1]
			router_flavor = router[2]
			router_network_list = router[3]
			router_az = router[4]
			for image in nova_client.images.list():
                                if image.name == router_image_name:
                                        image_id = image.id
                        for flavor in nova_client.flavors.list():
                                if flavor.name == router_flavor:
                                        flavor_id = flavor.id
			net_list = []
			for router_net in router_network_list:
				for net in nova_client.networks.list():
					if net.human_id == router_net:
						net_list.append(net.id)
			for ava in nova_client.availability_zones.list():
				if ava.hosts.keys()[0] == router_az:
					az_zoneName = ava.zoneName
			nova.start_a_router(router_name, image_id, flavor_id, az_zoneName, *net_list)	

	def deploy_instance_node(self):
		instance_info = read_xml.get_instance_info()
		for instance in instance_info:
			instance_name = instance[0]
			instance_image_name = instance[1]
			instance_flavor = instance[2]
			instance_network = instance[3]
			instance_az = instance[4]
			for image in nova_client.images.list():
				if image.name == instance_image_name:
					image_id = image.id
			for flavor in nova_client.flavors.list():
				if flavor.name == instance_flavor:
					flavor_id = flavor.id
			for net in nova_client.networks.list():
				if net.human_id == instance_network:
					net_id = net.id
			for ava in nova_client.availability_zones.list():
				if ava.hosts.keys()[0] == instance_az:
					az_zoneName = ava.zoneName
			nova.start_a_instance(instance_name, image_id, flavor_id, net_id, az_zoneName)
	def deploy_many_instance_nodes(self):
		pass
		

if __name__ == '__main__':
	mynetwork = Network()
	mynode = Node()
	if mynetwork.deploy_network():
		mynode.deploy_router_node()
		mynode.deploy_instance_node()
