#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from colorama import init,Fore
import time
from openstack import network
from openstack import nova
from openstack import glance

def start():
	while True:
                choice1 = int(raw_input())
                if choice1 == 1:
                        deploy_network()
			break
                elif choice1 == 2:
                        deploy_node()
			break
                elif choice1 == 3:
                        operate_image()
		elif choice1 == 4:
			print '退出...'
			time.sleep(1)
			exit()
                else:
			print ' 请重新输入：'
			continue
def operate_image():
	print '----------------------------'
        print '|'+ Fore.BLUE + '         网络部署         ' + Fore.BLACK + '|'
        print '----------------------------'
        print '         1.添加镜像'
        print '         2.删除镜像'
        print '         3.返回主界面'
        print '----------------------------'
        print ' 请选择操作：'
	while True:
		choice6 = int(raw_input())
		if choice6 == 1:
			#print glance.image_list
			#for i in glance.image_list:
			#	print getattr(i,'name')
			print Fore.YELLOW + '请输入镜像名：' + Fore.BLACK
			image_name = raw_input()
			print '----------------------------'
			import os
			Path = '/home/images'
			Pathname = []
			for i in os.listdir(Path):
				Pathname.append(i)
			for i,name in enumerate(Pathname):
				print i, '\t', name
			print '----------------------------'
			print Fore.YELLOW + '请选择镜像文件' + Fore.BLACK
			name_index = int(raw_input())
			image_file = 'home/images' + Pathname[name_index]
			print Fore.GREEN + '创建结果：' + Fore.BLACK
			print glance.create_image(image_name,image_file)
			time.sleep(0.5)
			operate_image()
		elif choice6 == 2:
			print Fore.YELLOW + '请输入需要删除的镜像名：' + Fore.BLACK
			image_name = raw_input()
			print Fore.GREEN + '删除结果' + Fore.BLACK
			print glance.delete_image(image_name)
			time.sleep(0.5)
			operate_image()	
			
		elif choice6 == 3:
			main()

		else:
			print Fore.RED + '输入不合法,请重新输入：'
			continue
			
def deploy_network():
	print '----------------------------'
        print '|'+ Fore.BLUE + '         网络部署         ' + Fore.BLACK + '|'
        print '----------------------------'
        print '         1.添加网络'
        print '         2.删除网络'
        print '         3.返回主界面'
        print '----------------------------'
        print ' 请选择操作：'
	while True:
		choice2 = int(raw_input())
		if choice2 == 1:
			print network.net_list
			print Fore.YELLOW + '请输入网络名：' + Fore.BLACK
			network_name = raw_input()
			print Fore.YELLOW + '请输入网络地址:格式(192.168.1.0/24)' + Fore.BLACK
			network_ip = raw_input()
			print Fore.GREEN + '创建结果：' + Fore.BLACK
			print network.create_network(network_name,network_ip)
			time.sleep(0.5)
			deploy_network()

		elif choice2 == 2:
			print Fore.YELLOW + '请输入需要删除的网络名：' + Fore.BLACK
			network_name = raw_input()
			print Fore.GREEN + '删除结果' + Fore.BLACK
			print network.delete_network(network_name)
			time.sleep(0.5)
			deploy_network()	
			
		elif choice2 == 3:
			main()

		else:
			print Fore.RED + '输入不合法,请重新输入：'
			continue
						
def deploy_node():
	print '----------------------------'
        print '|'+ Fore.BLUE + '         节点部署         ' + Fore.BLACK + '|'
        print '----------------------------'
        print '         1.部署路由节点'
        print '         2.部署主机节点'
        print '         3.返回主界面'
        print '----------------------------'
        print ' 请选择操作：'
	while True:
		choice3 = int(raw_input())
		if choice3 ==1:
			deploy_router_node()
			time.sleep(0.5)
			deploy_node()
		elif choice3 == 2:
			deploy_compute_node()
			time.sleep(0.5)
			deploy_node()
		elif choice3 == 3:
			main()
		else:
                        print Fore.RED + '输入不合法,请重新输入：'
                        continue

def deploy_compute_node():
	print '----------------------------'
        print '|'+ Fore.BLUE + '         主机节点部署         ' + Fore.BLACK + '|'
        print '----------------------------'
        print '         1.部署单个节点'
        print '         2.部署多个节点'
        print '         3.返回上层界面'
        print '----------------------------'
        print ' 请选择操作：'
	while True:
                choice4 = int(raw_input())
                if choice4 ==1:
                        print '请输入节点名：'
			name = raw_input()

			print ' - - - - - - - '
			for i ,image in enumerate(nova.image_list()):
				print i, '\t', image.name
			print ' - - - - - - -'
			print '请选择镜像号：'
			image_index = int(raw_input())
			image = nova.image_list()[image_index]
	
			print ' - - - - - - - '
			for i , flavor in enumerate(nova.flavor_list()):
				print i ,'\t',flavor.name
			print ' - - - - - - - '
			print '请选择配置大小：'
			flavor_index = int(raw_input())
			flavor = nova.flavor_list()[flavor_index]		
			
			print ' - - - - - - - ' 
                        for i , nic in enumerate(nova.nic_list()):
                                print i ,'\t',nic.human_id       
                        print ' - - - - - - - '
                        print '请选择网络号：'
                        nic_index = int(raw_input())            nic = nova.nic_list()[nic_index]
			
			print ' - - - - - - - '
                        for i , az in enumerate(nova.az_list()):
                                print i ,'\t',az.zoneName
                        print ' - - - - - - - '
                        print '请选择部署域：'
                        az_index = int(raw_input())   
                        az = nova.az_list()[az_index]
			
			nova.start_a_instance(name, image.id, flavor.id, nic.id, az.zoneName)
			break
                elif choice4 == 2:
                        print '请输入需要创建的节点数（小于250）:'
			count = int(raw_input())
			print ' - - - - - - - '
                        for i ,image in enumerate(nova.image_list()):
                                print i, '\t', image.name
                        print ' - - - - - - -'
                        print '请选择镜像号：'
                        image_index = int(raw_input())
                        image = nova.image_list()[image_index]

                        print ' - - - - - - - '
                        for i , flavor in enumerate(nova.flavor_list()):
                                print i ,'\t',flavor.name
                        print ' - - - - - - - '
                        print '请选择配置大小：'
                        flavor_index = int(raw_input())
                        flavor = nova.flavor_list()[flavor_index]

                        print ' - - - - - - - '
                        for i , nic in enumerate(nova.nic_list()):
                                print i ,'\t',nic.human_id
                        print ' - - - - - - - '
                        print '请选择网络号：'
                        nic_index = int(raw_input())
                        nic = nova.nic_list()[nic_index]

                        print ' - - - - - - - '
                        for i , az in enumerate(nova.az_list()):
                                print i ,'\t',az.zoneName
                        print ' - - - - - - - '
                        print '请选择部署域：'
                        az_index = int(raw_input())
                        az = nova.az_list()[az_index]

			nova.start_many_instance(count, image.id, flavor.id, nic.id, az.zoneName)
                        break
                elif choice4 == 3:
                        deploy_node()
		else:
                        print Fore.RED + '输入不合法,请重新输入：'
                        continue

def deploy_router_node():
	print '----------------------------'
        print '|'+ Fore.BLUE + '         路由节点部署         ' + Fore.BLACK + '|'
        print '----------------------------'
        print '         1.部署单个路由节点'
        print '         2.返回上层界面'
        print '----------------------------'
        print ' 请选择操作：'
	while True:
		choice5 = int(raw_input())
		if choice5 == 1:
			print '请输入节点名：'
                        name = raw_input()

                        print ' - - - - - - - '
                        for i ,image in enumerate(nova.image_list()):
                                print i, '\t', image.name
                        print ' - - - - - - -'
                        print '请选择镜像号：'
                        image_index = int(raw_input())
                        image = nova.image_list()[image_index]

                        print ' - - - - - - - '
                        for i , flavor in enumerate(nova.flavor_list()):
                                print i ,'\t',flavor.name
                        print ' - - - - - - - '
                        print '请选择配置大小：'
                        flavor_index = int(raw_input())
                        flavor = nova.flavor_list()[flavor_index]

			net_list = []
			while True:
                        	print ' - - - - - - - '
                        	for i , nic in enumerate(nova.nic_list()):
                                	print i ,'\t',nic.human_id
                        	print ' - - - - - - - '
                        	print '请选择路由器接入网络(输入-1结束)：'
                        	nic_index = int(raw_input())
				if nic_index == -1:
					break
				else:
					nic = nova.nic_list()[nic_index]
					net_list.append(nic.id)

                        print ' - - - - - - - '
                        for i , az in enumerate(nova.az_list()):
                                print i ,'\t',az.zoneName
                        print ' - - - - - - - '
                        print '请选择部署域：'
                        az_index = int(raw_input())
                        az = nova.az_list()[az_index]

			nova.start_a_router(name, image.id, flavor.id, az.zoneName, *net_list)
			break

		elif choice5 == 2:
			deploy_node()
		else:
                        print Fore.RED + '输入不合法,请重新输入：'
                        continue

def main():
	print '------------------------------------'
	print '|'+ Fore.GREEN + '         江南大学网络平台         ' + Fore.BLACK + '|'
	print '------------------------------------'
	print '      	1.网络'
	print '         2.节点'
	print '         3.镜像'
	print '         4.退出'
	print '------------------------------------'
	print ' 请选择操作：'
	
	start()
	


if __name__ == '__main__':
	main()
