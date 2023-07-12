import pynetbox
from pyzabbix import ZabbixAPI
from Host import *
NETBOX_IPV6_P = 0
NETBOX_IPV4_P = 1
NETBOX_NAME_P = 2
SHODA_P = 3
ZABBIX_NAME_P = 4
ZABBIX_IPV4_P = 5
ZABBIX_IPV6_P = 6

def loadNbRoles(nb):
    nb_roles = []
    for role in list(nb.dcim.device_roles.all()):
        nb_roles.append(str(role.slug))
    return nb_roles        

def omitRoles(nb_roles,role_omit):
    nb_roles_c = nb_roles
    for role in nb_roles:
        for n in role_omit:
            if role == n:
                nb_roles_c.remove(n)
    nb_roles = nb_roles_c
    return nb_roles

def loadNbHosts(nb,netbox_hosts,nb_roles):
    for host in list(nb.dcim.devices.filter(role = nb_roles)):
        netbox_hosts.append(Host(host.name))
    for ip in list(nb.ipam.ip_addresses.all()):
        for host in netbox_hosts:
            if ip.assigned_object_type == 'dcim.interface' and str(ip.assigned_object) != "None" and ip.assigned_object.device.display == host.getName():
                if len(str(ip)) <= 18:
                    host.setIp(ip)
                if len(str(ip)) > 18:
                    host.setIpv6(ip)
    return netbox_hosts

def loadZbHosts(zb,zabbix_hosts):
    for host in list(zb.host.get(output="extend")):
        zabbix_hosts.append(Host(host['host']))
        for zhost in zabbix_hosts:
            if zhost.getName() == host['host']:
                zhost.setId(host['hostid'])
    for ip in list(zb.hostinterface.get(output=["ip",'hostid'], selectedHosts = ["host"])):
        for host in zabbix_hosts:
            if (host.getId() == ip['hostid']):
                host.setIp(ip['ip'])
    return zabbix_hosts
                
def writeHeader(ws):
    header = ['Ipv6 address','Ipv4 address','Netbox device','Shoda','Zabbix device','Ipv4 address','Ipv6 address']
    for index,s in enumerate(header):
        ws.cell(row=1,column=1+index).value = s
        
def writeNetbox(ws,netbox_hosts,zabbix_hosts):
    row_p = 2
    column_p = 1
    zhost_c = zabbix_hosts
    for host in netbox_hosts:
        ws.cell(row=row_p,column=column_p + NETBOX_IPV6_P).value = host.getIpv6()
        ws.cell(row=row_p,column=column_p + NETBOX_IPV4_P).value = host.getIpv4()
        ws.cell(row=row_p,column=column_p + NETBOX_NAME_P).value = host.getName()
        for zhost in zabbix_hosts:
            nbipv4 = str(host.getIpv4()).split("/")[0]
            if  str(nbipv4) != "" and str(nbipv4).__eq__(str(zhost.getIpv4())) or str(zhost.getName()).__contains__(host.getName()) or str(host.getName()).__contains__(zhost.getName()) :
                dict_conditions={"Podle ipv4":str(nbipv4).__eq__(str(zhost.getIpv4())),"Podle nb jmena":str(zhost.getName()).__contains__(host.getName()) ,"Podle zb jmena":str(host.getName()).__contains__(zhost.getName())}
                ws.cell(row = row_p, column=column_p + ZABBIX_NAME_P).value = zhost.getName()    
                ws.cell(row=row_p,column=column_p + ZABBIX_IPV4_P).value = zhost.getIpv4()
                ws.cell(row=row_p,column=column_p + ZABBIX_IPV6_P).value = zhost.getIpv6()
                zhost_c.remove(zhost)
                ws.cell(row=row_p,column=column_p + SHODA_P).value = str(dict_conditions)
        row_p = row_p + 1
        
def writeZabbix(ws,netbox_hosts,zabbix_hosts):
    row_next = len(netbox_hosts)
    column_p = 1
    row_p = 2 + row_next    
    for host in zabbix_hosts:
        ws.cell(row=row_p,column=column_p + ZABBIX_NAME_P).value = host.getName()    
        ws.cell(row=row_p,column=column_p + ZABBIX_IPV4_P).value = host.getIpv4()
        ws.cell(row=row_p,column=column_p + ZABBIX_IPV6_P).value = host.getIpv6()
        row_p = row_p + 1  