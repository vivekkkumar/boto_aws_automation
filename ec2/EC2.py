

class ec2:
    def __init__(self, client):
        self._client = client

        """ :type : pyboto3.ec2 """

    def create_key_pair(self, key_name):
        print ('Creating Keypair {}'.format(key_name))
        return self._client.create_key_pair(KeyName=key_name)

    def create_security_group(self, group_name, description, vpc_id):
        print ('Creating a security group with name {} for vpc {}'.format(group_name, vpc_id))
        return self._client.create_security_group(
            GroupName=group_name,
            Description= description,
            VpcId=vpc_id
        )

    def add_inbound_rule_sg(self,sg_group_id):

        print("Adding inbound access to security group {}".format(sg_group_id))
        # ingress is for incoming traffic, authorize to allow, revoke to remove the rule.
        # check official doc, below definition allows traffic from all IPs port 80 http and SSH.
        self._client.authorize_security_group_ingress(
            GroupId=sg_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort' : 80,
                    'ToPort' : 80,
                    'IpRanges' : [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )

    def launch_ec2_instance(self, image_ID, key_name, min_count, max_count, security_group_id, subnet_id, user_data):
        print ("Launching EC2 instance of count {} in subnet {}".format(min_count, subnet_id))
        return self._client.run_instances(
            ImageId=image_ID,
            KeyName=key_name,
            MinCount=min_count,
            MaxCount=max_count,
            InstanceType='t2.micro',             # free tier
            SecurityGroupIds=[security_group_id],
            SubnetId=subnet_id,
            UserData=user_data
        )