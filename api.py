#py -m pip install pyzabbix
from pyzabbix import ZabbixAPI
import apiMethods as am
import pynetbox
from Host import *
import re
import openpyxl
#netsystem netbox e2c49da4d7d74a73b5fe3d96f9e8af828dfde965 https://netbox-netsys.netsystem.local/
#netsystem zabbix e7d696fd89678e947d9623018602d2d21419791a2140dd457ce2894a4da3c818 http://192.168.200.133/
#docker netbox 0123456789abcdef0123456789abcdef01234567 http://192.168.56.101:8000
#docker zabbix a7d0127f869816066cbb6d206b6c2a211ddc3d4d3f686e33cdaadc8a3808be26

#Zabbix api connection
zb = ZabbixAPI("http://192.168.200.133/")
zb.login(api_token='e7d696fd89678e947d9623018602d2d21419791a2140dd457ce2894a4da3c818')
#Netbox api connection
nb = pynetbox.api('https://netbox-netsys.netsystem.local/'
                  ,token='e2c49da4d7d74a73b5fe3d96f9e8af828dfde965')
#SSL verification false
nb.http_session.verify = False
wb = openpyxl.Workbook()
ws = wb.active
netbox_hosts = []
nb_hosts = []
zabbix_hosts = []
#Loading roles from netbox
nb_roles = am.loadNbRoles(nb)
print("Netbox role")
print(nb_roles)
print("Zadejte nazev, ktery nechcete vypsat(oddelene mezerou)")
line = "wall-box organizer patch-panel"# input()
user_roles = []
user_roles = line.split()
#User choosing roles to work with
nb_roles = am.omitRoles(nb_roles,user_roles)
#Loading zabbix and netbox devices
netbox_hosts = am.loadNbHosts(nb,netbox_hosts,nb_roles)
zabbix_hosts = am.loadZbHosts(zb,zabbix_hosts)

#Writing informations to excel
list.sort(netbox_hosts,key=lambda x: x.name)            
list.sort(zabbix_hosts,key=lambda x: x.name)            

am.writeHeader(ws)
am.writeNetbox(ws,netbox_hosts,zabbix_hosts)
am.writeZabbix(ws,netbox_hosts,zabbix_hosts)

#Auto adjusting columns
for column_cells in ws.columns:
    length = max(len(str(cell.value)) for cell in column_cells)
    ws.column_dimensions[column_cells[0].column_letter].width = length
wb.save('summary.xlsx')

#For debugging
# for host in netbox_hosts:
#     print(host)
# for host in zabbix_hosts:
#     print(host)
