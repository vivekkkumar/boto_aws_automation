from src.ec2.VPC import vpc
from src.ec2.EC2 import ec2
from src.clientLocator import EC2Client

def main():

    ec2_client = EC2Client().get_client()
    myvpc = vpc(ec2_client)

    response = myvpc.create_vpc()

    # using inbuilt str magic method
    print ('VPC created' + str(response))

    vpc_name = 'Boto3-VPC'

    # check documentation for actual value in the dictionary
    vpc_id = response['Vpc']['VpcId']

    myvpc.add_name_tag(vpc_id, vpc_name)

    igw_obj = myvpc.create_internet_gateway()

    # more information on the off documentation
    igw_id = igw_obj['InternetGateway']['InternetGatewayId']

    myvpc.attach_igw_to_vpc(vpc_id, igw_id)

    public_subnet_response = myvpc.create_subnet(vpc_id, '10.0.1.0/24')

    public_subnet_id = public_subnet_response['Subnet']['SubnetId']

    print ("subnet created for vpc {} with id {}".format(vpc_id, str(public_subnet_response)))

    myvpc.add_name_tag(public_subnet_id, 'Boto3-Public-Subnet')

    ''' In order for a subnet to be communicated from outside, an Internet Gateway is needed along with a routing table'''

    route_table_response = myvpc.create_public_route_table(vpc_id)

    rtbl_id = route_table_response['RouteTable']['RouteTableId']

    myvpc.create_igw_route_on_public_route_table(rtbl_id, igw_id)

    # Associate public subnet with the route table

    myvpc.associate_subnet_with_route_table(public_subnet_id, rtbl_id)

    # Allow auto assign public ip address for subnet

    myvpc.allow_auto_assign_ip_address_for_subnet(public_subnet_id)

    # create a private subnet

    private_subnet_response = myvpc.create_subnet(vpc_id, cidr_block='10.0.2.0/24')

    private_subnet_id = private_subnet_response['Subnet']['SubnetId']

    # not associating or attaching to route table since this is a private subnet
    print ("created private subnet {} for vpc{}".format(private_subnet_id, vpc_id))

    # add name tag to the subnet

    myvpc.add_name_tag(private_subnet_id, 'Boto3-Private-Subnet')

    # EC2 instance

    ec2obj = ec2(ec2_client)

    # Create a key pair

    key_pair_name = 'Boto3-key-pair'

    ec2_key_pair_resp =  ec2obj.create_key_pair(key_pair_name)

    print ("Created Key pair with name {} and key pair response {}".format(key_pair_name, str(ec2_key_pair_resp)))

    # Create a security group

    public_security_group = 'Boto-public-sg'
    pub_sg_response = ec2obj.create_security_group(public_security_group, "Public Security group for public subnet", vpc_id)

    pub_sg_response_id = pub_sg_response['GroupId']
    # add public access to security group

    ec2obj.add_inbound_rule_sg(pub_sg_response_id)

    print ('Added public access rule to security group {}'.format(public_security_group))

    # starting script can start any application, commands to start a service or run a web app

    user_data = """#!/bin/bash
                    yum update -y
                    yum install httpd24 -y
                    service httpd start
                    chkconfig httpd on
                    echo "<html><body><h1> Hello from Boto3 </h1></body></html>" > /var/www/html/index.html"""

    # launch public EC2 instance

    ec2obj.launch_ec2_instance('ami-0d2692b6acea72ee6', key_pair_name, 1, 1, pub_sg_response_id, public_subnet_id , user_data)

    print ("Launching public ec2 instance using AMI ami-0d2692b6acea72ee6")

    # adding another security group

    private_security_group_name = "Boto3-private-sg"
    private_security_group_description = 'Private security group for priveta subnet'
    private_security_group_response = ec2obj.create_security_group(private_security_group_name, private_security_group_description, vpc_id)

    private_security_group_id = private_security_group_response['GroupId']

    # add rule to private security group

    ec2obj.add_inbound_rule_sg(private_security_group_id)

    # launch a private EC2 instance

    ec2obj.launch_ec2_instance('ami-0d2692b6acea72ee6', key_pair_name,1, 1, private_security_group_id, private_subnet_id, "")

if __name__ == '__main__':
    main()