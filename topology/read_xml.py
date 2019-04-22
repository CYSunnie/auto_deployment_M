#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from xml.etree import ElementTree as ET


#tree = ET.parse('/root/python/auto_deployment/topology/topo.xml')
tree = ET.parse('./topo.xml')
root = tree.getroot()

def get_network_info():
	networkInfo_node = root.find('networkInfo')
	network_nodes = networkInfo_node.findall('network')

	networks = []
	for net in network_nodes:
		networks.append([net.find('name').text, net.find('networkIp').text])
	return networks

def get_router_info():
	routerInfo_node = root.find('routerInfo')
	router_nodes = routerInfo_node.findall('router')
	routers = []
	for router in router_nodes:
		networknames = []
		for networkname in router.findall('networkname'):
			networknames.append(networkname.text)
		routers.append([router.find('name').text, router.find('image').text, router.find('flavor').text, networknames, router.find('az').text])
	return routers

def get_instance_info():
	instanceInfo_node = root.find('instanceInfo')
	instance_nodes = instanceInfo_node.findall('instance')
	instances = []
	for instance in instance_nodes:
		instances.append([instance.find('name').text, instance.find('image').text, instance.find('flavor').text, instance.find('networkname').text, instance.find('az').text])
	return instances

if __name__ == '__main__':
	print get_network_info()
	print get_router_info()
	print get_instance_info()
