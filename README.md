ZABBIX CREATE ITEMS FROM CSV
=======================

Work in progess
----------------

CSV format as below
--------------------

|Module_name|oid_name|oid|datatype|start|end|description|
|-----------|:------:|:------:|:------:|:------:|:------:|---------|
|Voip_Destination|status|1.3.6.1.2.1.2.2.18.0|STRING|0|1000|Some Description|
|Voip_Destination|flags|1.3.6.1.2.1.2.2.18.1|STRING|0|1000|Some Description|
|Voip_Destination|Type|1.3.6.1.2.1.2.2.18.2|STRING|0|1000|Some Description|

``` 
Module_name,oid_name,oid,datatype,start,end,description
Voip_Destination,status,1.3.6.1.2.1.2.2.18.0,STRING,0,1000,Some Description
Voip_Destination,flags,1.3.6.1.2.1.2.2.18.1,STRING,0,1000,Some Description
Voip_Destination,Type,1.3.6.1.2.1.2.2.18.2,STRING,0,1000,Some Description
```

Code Usage :
---------------

```python
import zabbix_items_from_csv
from xml.etree import ElementTree

#-----------------------
# Limit reading to first 10 Lines.
#-----------------------
complete_list_dict_device_1 =  zabbix_items_from_csv.reader_csv_file('oid_list_with_range_processed.csv', 10)
xml_tree_device_1 = zabbix_items_from_csv.\
                            generate_items_xml_file_complete(complete_list_dict_device_1,
                                                            'BLR-DEVICE_1', 'BLR-DEVICE_1',
                                                            '10.12.51.11', 'DEVICE_1')
zabbix_items_from_csv.xml_pretty_me('BLR-DEVICE_1.xml', ElementTree.tostring(xml_tree_device_1))
#-----------------------
xml_tree_device_1 = zabbix_items_from_csv.\
                            generate_items_xml_file_complete(complete_list_dict_device_1,
                                                            'CHN-DEVICE_1', 'CHN-DEVICE_1',
                                                            '10.12.51.11', 'DEVICE_1')
zabbix_items_from_csv.xml_pretty_me('CHN-DEVICE_1.xml', ElementTree.tostring(xml_tree_device_1))


#-----------------------
# Read all the lines from the csv file.
#-----------------------
complete_list_dict_device_2 =  zabbix_items_from_csv.reader_csv_file('oid_list_with_range_processed.csv')
xml_tree_device_2 = zabbix_items_from_csv.\
                            generate_items_xml_file_complete(complete_list_dict_device_2,
                                                             'BLR-DEVICE_2', 'BLR-DEVICE_2',
                                                             '12.12.54.66', 'DEVICE_2')
zabbix_items_from_csv.xml_pretty_me('BLR-DEVICE_2.xml', ElementTree.tostring(xml_tree_device_2))
#-----------------------
xml_tree_device_2 = zabbix_items_from_csv.\
                            generate_items_xml_file_complete(complete_list_dict_device_2,
                                                             'CHN-DEVICE_2', 'CHN-DEVICE_2',
                                                             '12.12.52.74', 'DEVICE_2')
zabbix_items_from_csv.xml_pretty_me('CHN-DEVICE_2.xml', ElementTree.tostring(xml_tree_device_2))
```    


USAGE
--------------------------------------------

     1. To Generate xml import file.
     --------------------------------------------
     python zabbix_items_from_csv.py <export_csv> <host_name> <host_group_name> <host_interface_name> <host_application_name>
     	example: python zabbix_items_from_csv.py oid_list_with_range_processed.csv GGSN-1-LONDON GGSN-GROUP 127.0.0.1 GGSN-APP-OIDS

     Parameter Information
     --------------------------------------------
     <csv_file_to_process>  : Is the csv file in format mentioned in the README.md file.
     <host_name>            : Host name as given in Zabbix server.
     <host_group_name>      : Host Group which the host belongs to, as in Zabbix server.
     <host_interface_ip>    : SNMP Interface configured on Zabbix server. (Assuming Single Interface in Configured)
     <host_application_name>: Application Name in the Zabbix Server. (To organize all items being imported)
     --------------------------------------------