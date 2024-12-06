This page explains how to build a docker image from python image with terraform installed and simple python api exposed.
To test the api working the simple java code is included. Create simple main.tf file inside the container.
Don't forget to add access key and the secret key to the configuration file.
Enter the container terminal of the java app, create a file with the java code. compile it, and run.

# docker build -f Dockerfile . -t ghcr.io/tda-centre/terraform:1.3
# docker push

# javac TerraformExecutor.java
# java TerraformExecutor

Adjust the service name and the commands in the TerraformExecutor.java file
Also, K8S definition files are given to create deployment from the image.
