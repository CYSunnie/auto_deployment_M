#!/usr/bin/env python

from colorama import init,Fore
from auth import glance_client

images = glance_client.images.list()
image_list = list(images)

def _res(success,**kwargs):#respond
        kwargs['Success'] = 'True' if success else 'False'
        return kwargs


def create_image(image_name,image_file):
	flag_name = False
	#print image_list
	for image in image_list:
		if getattr(image,'name') == image_name:
			flag_name = True
		else:
			pass
	if flag_name:
		return _res(False,Reason='Name already exist')	
	else:
		with open(image_file) as fimage:
			glance_client.images.create(name=image_name, is_public=False, disk_format="qcow2", container_format="bare", data=fimage)
		return _res(True,Reason = 'Image %s has been created.' % image_name)
	

def delete_image(image_name):
	flag_delete = False
	for image in image_list:
		if getattr(image,'name') == image_name:
			glance_client.images.delete(getattr(image,'id'))
			flag_delete = True
		else:
			pass 	
	if flag_delete:
		return _res(True,Reason = 'Image %s has been deleted.' %image_name)
	else:
		return _res(False,Reason = 'There is no image:%s in openstack,can not delete.' %image_name)


'''if __name__ == '__main__':
	with open("/home/images/cirros-0.3.4-x86_64-disk.img") as fimage:
		glance_client.images.create(name="cirros22", is_public=False, disk_format="qcow2", container_format="bare", data=fimage)
'''
