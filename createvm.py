import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

def create_vm(subscription_id, resource_group_name, vm_name, location, username, password, image_publisher, image_offer, image_sku, vnet_name, subnet_name, public_ip_name, vm_size="Standard_D2s_v3"):
    """Creates a virtual machine in Azure.

    Args:
        subscription_id (str): Your Azure subscription ID.
        resource_group_name (str): The name of the resource group.
        vm_name (str): The name of the virtual machine.
        location (str): The location of the resources.
        username (str): The username for the VM.
        password (str): The password for the VM.
        image_publisher (str): The publisher of the image.
        image_offer (str): The offer of the image.
        image_sku (str): The SKU of the image.
        vnet_name (str): The name of the virtual network.
        subnet_name (str): The name of the subnet.
        public_ip_name (str): The name of the public IP address.
        vm_size (str, optional): The size of the VM. Defaults to "Standard_D2s_v3".
    """

    # Authenticate to Azure
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Create resource group if it doesn't exist
    resource_group_params = {'location': location}
    resource_client.resource_groups.create_or_update(resource_group_name, resource_group_params)

    # Create virtual network
    vnet_params = {
        'address_space': {'address_prefixes': ['10.0.0.0/16']},
        'location': location
    }
    vnet = network_client.virtual_networks.create_or_update(resource_group_name, vnet_name, vnet_params)

    # Create subnet
    subnet_params = {
        'address_prefix': '10.0.0.0/24'
    }
    subnet = network_client.subnets.create_or_update(resource_group_name, vnet_name, subnet_name, subnet_params)

    # Create public IP
    public_ip_params = {
        'location': location,
        'public_ip_allocation_method': 'Static'
    }
    public_ip = network_client.public_ip_addresses.create_or_update(resource_group_name, public_ip_name, public_ip_params)

    # Create network interface
    nic_params = {
        'ip_configurations': [{
            'name': 'primary',
            'subnet': {'id': subnet.id},
            'public_ip_address': {'id': public_ip.id}
        }]
    }
    nic = network_client.network_interfaces.create_or_update(resource_group_name, 'myNic', nic_params)

    # Create virtual machine
    vm_params = {
        'location': location,
        'hardware_profile': {'vm_size': vm_size},
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
vm_name = "myVM"
location = "centralindia"
username = "azureuser"
password = "password@123"
image_publisher = "Canonical"
image_offer = "UbuntuServer"
image_sku = "18.04-LTS"
vnet_name = "myVnet"
subnet_name = "default"
public_ip_name = "myPublicIP"

create_vm(subscription_id, resource_group_name, vm_name, location, username, password, image_publisher, image_offer, image_sku, vnet_name, subnet_name, public_ip_name)
