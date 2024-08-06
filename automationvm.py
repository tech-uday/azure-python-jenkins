import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

def create_vm(subscription_id, resource_group_name, vm_name, location, username, password, image_publisher, image_offer, image_sku, vnet_name, subnet_name):
    """Creates a virtual machine in Azure within an existing VNet.

    Args:
        subscription_id: Your Azure subscription ID.
        resource_group_name: The name of the resource group.
        vm_name: The name of the virtual machine.
        location: The location of the resources.
        username: The username for the VM.
        password: The password for the VM.
        image_publisher: The publisher of the image.
        image_offer: The offer of the image.
        image_sku: The SKU of the image.
        vnet_name: The name of the existing virtual network.
        subnet_name: The name of the existing subnet.
    """

    # Authenticate to Azure
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)

    # Get existing virtual network and subnet
    vnet = network_client.virtual_networks.get(resource_group_name, vnet_name)
    subnet = network_client.subnets.get(resource_group_name, vnet_name, subnet_name)

    # Create network interface
    nic_params = {
        'ip_configurations': [{
            'name': 'primary',
            'subnet': {'id': subnet.id}
        }]
    }
    nic = network_client.network_interfaces.begin_create_or_update(resource_group_name, 'myNic', nic_params)

    # Create virtual machine
    vm_params = {
        'location': location,
        'hardware_profile': {'vm_size': 'Standard_D2s_v3'},
        'storage_profile': {
            'image_reference': {
                'publisher': image_publisher,
                'offer': image_offer,
                'sku': image_sku,
                'version': 'latest'
            },
            'os_disk': {
                'name': 'myOSDisk',
                'caching': 'ReadWrite',
                'create_option': 'FromImage'
            }
        },
        'network_profile': {
            'network_interfaces': [{
                'id': nic.id
            }]
        },
        'os_profile': {
            'computer_name': vm_name,
            'admin_username': username,
            'admin_password': password
        }
    }
    vm = compute_client.virtual_machines.begin_create_or_update(resource_group_name, vm_name, vm_params)
    vm.result()

# Replace placeholders with your actual values
subscription_id = "4411374d-a972-4fef-8ba5-41a59e110cf3"
resource_group_name = "Testing"
vm_name = "myVMautomation"
location = "centralindia"
username = "azureuser"
password = "password@123"
image_publisher = "Canonical"
image_offer = "UbuntuServer"
image_sku = "18.04-LTS"
vnet_name = "first-vnet"
subnet_name = "default"

create_vm(subscription_id, resource_group_name, vm_name, location, username, password, image_publisher, image_offer, image_sku, vnet_name, subnet_name)
