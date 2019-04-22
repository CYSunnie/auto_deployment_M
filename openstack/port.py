#!/usr/bin/env python
# -*- coding:utf-8 -*-

from auth import neutron_client
import re
RE_MAC_ADDRESS = re.compile(r'^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$')

def _validate_mac(mac):
        return RE_MAC_ADDRESS.match(mac) is not None

def _res(success,**kwargs):
        kwargs['Success'] = 'True' if success else 'False'
        return kwargs

def change_portsecurity_false(mac):
        if not _validate_mac(mac):
                return _res(False,Reason = 'invalid MAC address')

        flag = False
        ports_list = neutron_client.list_ports()['ports']
        for port in ports_list:
                if port['mac_address'] == mac:
                        port_id = port['id']
                        flag = True
        if not flag:
                return _res(False,Reason='MAC not exist')

        neutron_client.update_port(port_id, {'port':{'security_groups':None}})
        neutron_client.update_port(port_id, {'port':{'port_security_enabled':'False'}})
	return _res(True,Reason = 'Port security of %s has been set from True to False.' % mac)
