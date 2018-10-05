# sd2018b Exam 1
**Icesi University**  
**Course:** Distributed Systems 
**Professor:** Daniel Barragán C.  
**Subject:** Infrastructure automation  
**Email:** daniel.barragan at correo.icesi.edu.co  
**Student:** Alejandro Bueno C.  
**Student ID:** A00335472  
**Git URL:** https://github.com/abc1196/sd2018b-exam1.git  

### Goals to achieve
* Develop the automatic provisioning of an infrastructure
* Diagnose and execute the needed actions to achieve a stable infrastructure  

### Used technologies
* Vagrant
* CentOS7 Box
* Github Repository
* Python3
* Python3 Libraries: Flask, Fabric
* Ngrok  

### Infrastructure diagram  
The desired infrastructure to deploy consists in four virtual machines (VM) with the following settings:  
* CentOS DHCP Server (192.168.180.10): must deliver an IP address to the other VM's. The network address is **192.168.180.0/24** with gateway **192.168.130.1** (the University's gateway). Also, it assigns an static IP addres to the YUM Mirror Server (192.168.180.40).  
* CentOS CI Server (dhcp): this VM has a Flask application with and endpoint using RESTful architecture best practices. The endpoint has the following logic:   
  * A Webhook attached to a Pull Request triggers the endpoint.  
  * The endpoint reads the Pull Request content and searchs for the packages.json file.  
  * Via SSH, the endpoint runs the required commands to update the YUM Mirror Server dependencies.
  * The endpoint return the packages.json content.
* CentOS YUM Mirror Server (192.168.180.40): contains the required dependencies to use in the infrastructure. These dependencies are obtained via a JSON file (packages.json) located at the root of this repository.
* CentOS YUM Client (dhcp): it has its dependencies repolist attached to the YUM Mirror Server.  
* Github Webhook: this webhook triggers when a Pull Request event is created. It calls the CI Server's endpoint.  

![][1]
**Figure 1**. Deploy Diagram  

### Deployment  
After you clone the repository, execute the following commands:  

| Command | Description   |
|---|---|
| vagrant up dhcp_server | Provision the dhcp server first. You should do this to avoid provisioning the other VM's without a valid IP address |  
| vagrant up | Provision the rest of the VM's |  
 
Now, with a tool like **tmux**, create a session with two terminals (Ctrl +A, Shift +2). In both of them, run the next command:  

| Command | Description   |
|---|---|
| vagrant ssh ci_server | Access the CI Server VM |  

In the first terminal, you will start the Flask application. Flask was used because its simple to create and the application will run only one endpoint. A framework like Swagger can be used to build more extensive RESTful APIs. Execute the following commands:  

| Command | Description   |
|---|---|
| sudo su | Login as root |  
| cd | Get in the root dir |
| cd .. | Get in the / dir in root |  
| cd exam1 | Go to the Flask app dir |
| source exam1/bin/activate | Start the Flask virtual environment |
| export FLASK_APP=exam1.py | Export the file exam1.py as a environment variable to run the application |
| flask run | Run the application | 

In the second terminal, you will run ngrok to make the Flask application public. You have to do this to attach the endpoint to the Github's Webhook. Run these commands:  

| Command | Description   |
|---|---|
| sudo su | Login as root |  
| cd | Get in the root dir |
| cd .. | Get in the / dir in root |  
| cd ngrok | Go to the Flask app dir |
| ./ngrok http | Start the ngrok tunnel to make public the application |  

Finally, let's create the Github webhook. In the repository, go to *Settings -> Webhooks*. Add a webhook and put in the Payload URL the URL that ngrok provides with the endpoint. The application endpoint is located at */abc/exam1/api/v1/packages*. So, for example, the resulting Payload URL will look like this:  

```
http://XXXXXXXX.ngrok.io/abc/exam1/api/v1/packages
```
Where XXXXXXXX is the URL ngrok provides each time we run the ngrok command.


### References  
* https://docs.chef.io/  
* https://github.com/ICESI/ds-vagrant/tree/master/centos7/05_chef_load_balancer_example
* https://developer.github.com/v3/guides/building-a-ci-server/
* http://www.fabfile.org/
* http://flask.pocoo.org/  
* https://connexion.readthedocs.io/en/latest/  

[1]: images/01_deploy_diagrampng.png
