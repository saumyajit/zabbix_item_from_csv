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

    complete_list_dict_device_1 =  reader_csv_file('oid_list_with_range_processed.csv', 10)
    xml_tree_device_1 = generate_items_xml_file_complete(complete_list_dict_device_1, 'BLR-DEVICE_1', 'BLR-DEVICE_1', '10.12.51.11', 'DEVICE_1')
    xml_pretty_me('BLR-DEVICE_1.xml', ElementTree.tostring(xml_tree_device_1))

    xml_tree_device_1 = generate_items_xml_file_complete(complete_list_dict_device_1, 'CHN-DEVICE_1', 'CHN-DEVICE_1', '10.12.51.11', 'DEVICE_1')
    xml_pretty_me('CHN-DEVICE_1.xml', ElementTree.tostring(xml_tree_device_1))

    complete_list_dict_device_2 =  reader_csv_file('oid_list_with_range_processed.csv')
    xml_tree_device_2 = generate_items_xml_file_complete(complete_list_dict_device_2, 'BLR-DEVICE_2', 'BLR-DEVICE_2', '12.12.54.66', 'DEVICE_2')
    xml_pretty_me('BLR-DEVICE_2.xml', ElementTree.tostring(xml_tree_device_2))

    xml_tree_device_2 = generate_items_xml_file_complete(complete_list_dict_device_2, 'CHN-DEVICE_2', 'CHN-DEVICE_2', '12.12.52.74', 'DEVICE_2')
    xml_pretty_me('CHN-DEVICE_2.xml', ElementTree.tostring(xml_tree_device_2))