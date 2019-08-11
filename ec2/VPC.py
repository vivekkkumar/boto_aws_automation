class vpc:
    def __init__(self, client):
        self._client = client

        # very useful auto complete for boto methods with signature pyboto3 package

        """ :type : pyboto3.ec2 """

    def create_vpc(self):
        '''
        Have to create the VPC first and then the name has to be assigned
        '''
        print('Creating a VPC')
        return self._client.create_vpc(
            CidrBlock='10.0.0.0/16'
        )

    def add_name_tag(self, resource_id, resource_name):
        print ('Adding {} tag to the {} '.format(resource_name, resource_id))
        return self._client.create_tags(
            Resources=[resource_id],
            Tags=[{
                'Key' : 'Name',
                'Value' : resource_name
            }]
        )

    def create_internet_gateway(self):
        print ("creating an InternetGateway")
        return self._client.create_internet_gateway()

    def attach_igw_to_vpc(self, vpc_id, igw_id):
        print ("attaching {} to the vpc {}".format(igw_id, vpc_id))
        return self._client.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )

    def create_subnet(self, vpcid, cidr_block):
        print ("creating subnet for vpc {} with CIDR block {}".format(vpcid, cidr_block))
        return self._client.create_subnet(
            VpcId=vpcid,
            CidrBlock=cidr_block
        )

    def create_public_route_table(self, vpcid):
        print("creating public rout for vpc {}".format(vpcid))
        return self._client.create_route_table(VpcId=vpcid)

    def create_igw_route_on_public_route_table(self, rtbl_id, igwid):
        print("Adding route table entry for  IGW {} with the route table {}".format(igwid, rtbl_id))
        return self._client.create_route(
            RouteTableId=rtbl_id,
            GatewayId=igwid,
            # this is to say any network or any IP can access the resource
            DestinationCidrBlock='0.0.0.0/0'
        )

    def associate_subnet_with_route_table(self, subnet_id, rtbl_id):
        print ("Associating subnet {} with the route table {}".format(subnet_id, rtbl_id) )
        return self._client.associate_route_table(
            SubnetId=subnet_id,
            RouteTableId=rtbl_id
        )

    def allow_auto_assign_ip_address_for_subnet(self, subnet_id):
        '''
        Specify true to indicate that ENIs attached to instances created in the specified subnet should be assigned a public IPv4 address.
        '''
        return self._client.modify_subnet_attribute(
            SubnetId=subnet_id,
            MapPublicIpOnLaunch={'Value' : True}
        )