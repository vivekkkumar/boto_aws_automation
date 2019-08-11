
Libraries and set of Python files to create a VPC. 

A VPC with public and private subnets. One EC2 instance on the public and one on the private subent.

THe public instance can be accessed through the Internet.

Which deploys a webserver and an index page if the IP is accessed.

In order for this script to work aws-cli has to be have the secret is being added to the client.

testDeployment.py can take all the config and start spinning up the resources.
