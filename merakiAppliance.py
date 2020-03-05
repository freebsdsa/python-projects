#!/usr/bin/python3

import meraki
import os

####
MERAKI_API_KEY = os.getenv('MERAKI_API_KEY')
MERAKI_ORG_ID = os.getenv('MERAKI_ORG_ID')
####

dashboard = meraki.DashboardAPI(
    api_key=MERAKI_API_KEY,
    base_url='https://api-mp.meraki.com/api/v0/',
    print_console=False,
    output_log=False,
    simulate=False,
    maximum_retries=3
)

org_id = MERAKI_ORG_ID

####

inventory = dashboard.organizations.getOrganizationInventory(org_id)
appliances = [device for device in inventory if device['model'][:2] in ('MX') and device['networkId'] is not None]

for net in appliances:
    isStaticIP = ''
    serial = net['serial']
    net_id = net['networkId']
    name = net['name']
    model = net['model']
    mac = net['mac']
    network = dashboard.networks.getNetwork(net_id)
    net_name = network['name']

    uplinks = dashboard.devices.getNetworkDeviceUplink(net_id, serial)
    uplinks_info = dict.fromkeys(['WAN1', 'WAN2'])
    uplinks_info['WAN1'] = dict.fromkeys(['interface', 'status', 'ip', 'publicIp'])
    uplinks_info['WAN2'] = dict.fromkeys(['interface', 'status', 'ip', 'publicIp'])
    uplinks_info['Cellular'] = dict.fromkeys(['interface', 'status', 'ip', 'publicIp'])
    for uplink in uplinks:
        uplinks_info['WAN1']['status'] = ''
        uplinks_info['WAN2']['status'] = ''
        interface = uplink['interface']
        interface = interface.replace(" ", "")
        if uplink['interface'] == 'WAN 1':
            for key in uplink.keys():
                uplinks_info['WAN1'][key] = uplink[key]
            status = uplinks_info['WAN1']['status']
            interface_ip = uplinks_info['WAN1']['ip']
            public_ip = uplinks_info['WAN1']['publicIp']
            try:
                uplinks_info['WAN1']['usingStaticIp']
                isStaticIP = uplinks_info['WAN1']['usingStaticIp']
            except:
                isStaticIP = 'Unknown'
            isStaticIP = str(isStaticIP)
            getLatency = dashboard.devices.getNetworkDeviceLossAndLatencyHistory(net_id, serial, '8.8.8.8', timespan='300', uplink='wan1')
            try:
                latency = str(getLatency[0]['latencyMs'])
            except:
                latency = 'Unknown'
            try:
                packetLoss = str(getLatency[0]['lossPercent'])
            except:
                latency = 'Unknown'

            print("{'serial' = '"+serial+"', 'networkId' = '"+net_id+"', 'networkName' = '"+net_name+"', 'deviceName' = '"+name+"', 'deviceModel' = '"+model+"', 'deviceMac' = '"+mac+"', 'interfaceStatus' = '"+status+"', 'interfaceName' = '"+interface+"', 'interfaceIp' = '"+interface_ip+"', 'interfacePublicIp' = '"+public_ip+"', 'interfaceStatic' = '"+isStaticIP+"', 'latency' = '"+latency+"', 'packetLoss' = '"+packetLoss+"'}")

        elif uplink['interface'] == 'WAN 2':
            for key in uplink.keys():
                uplinks_info['WAN2'][key] = uplink[key]
            status = uplinks_info['WAN2']['status']
            interface_ip = uplinks_info['WAN2']['ip']
            public_ip = uplinks_info['WAN2']['publicIp']
            try:
                uplinks_info['WAN2']['usingStaticIp']
                isStaticIP = uplinks_info['WAN2']['usingStaticIp']
            except:
                isStaticIP = 'Unknown'
            isStaticIP = str(isStaticIP)
            getLatency = dashboard.devices.getNetworkDeviceLossAndLatencyHistory(net_id, serial, '8.8.8.8', timespan='300', uplink='wan2')
            try:
                latency = str(getLatency[0]['latencyMs'])
            except:
                latency = 'Unknown'
            try:
                packetLoss = str(getLatency[0]['lossPercent'])
            except:
                latency = 'Unknown'

            print("{'serial' = '"+serial+"', 'networkId' = '"+net_id+"', 'networkName' = '"+net_name+"', 'deviceName' = '"+name+"', 'deviceModel' = '"+model+"', 'deviceMac' = '"+mac+"', 'interfaceStatus' = '"+status+"', 'interfaceName' = '"+interface+"', 'interfaceIp' = '"+interface_ip+"', 'interfacePublicIp' = '"+public_ip+"', 'interfaceStatic' = '"+isStaticIP+"', 'latency' = '"+latency+"', 'packetLoss' = '"+packetLoss+"'}")

exit()
