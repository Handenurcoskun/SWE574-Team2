
# Run on Local Local Environment

1.	Docker should be installed on your local machine. https://www.docker.com/products/docker-desktop/
2.	Extract the 0.9 tagged release file that is available in my github page, and the USB that I provide.
3.	In the project root directory, where the Dockerfile resides, run docker-compose up command.
4.	From Docker Desktop or terminal screen, see that both web application and mysql database containers are running. From terminal, docker ps command can be used.
5.	If a problem encountered about listening to the 3306 or 8000 ports while starting the containers, kill the other applications that listens to those ports. 
6.	From your web browser, go to http://127.0.0.1:8000 link.

# Run on AWS Cloud Environment

1.	Create an EC2 Linux instance on AWS:
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html
2.	Connect the EC2 instance using one of the methods described here:
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstances.html
3.	Install docker on the Linux EC2 instance: https://docs.docker.com/engine/install/ubuntu/
4.	Transfer the project folder to the EC2 instance: https://asf.alaska.edu/how-to/data-recipes/moving-files-into-and-out-of-an-aws-ec2-instance-windows/
5.	Run docker-compose up command in EC2 under the project folder.
6.	Set inbound and outbound security rules, so that the application can be reached over the internet: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html
