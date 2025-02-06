############# NFS server side configuratuons #####################

Install nfs-server:
# apt install nfs-server nfs-kernel-server -y

Check the status:
# systemctl status nfs-server

If you want to use firewalld, then add the ports from the output of the below command to firewalld:
# ss -tlpn | grep mount
# firewall-cmd --add-service={nfs,mountd,rpc-bind} --permanent

Add folders to export:
# mkdir /data/rabbit-prod
# vi /etc/exports
    /data/rabbit-prod 10.0.6.0/24(rw,sync,no_subtree_check,no_root_squash,no_all_squash,insecure)
# showmount -e localhost
# chown -R nobody:nogroup /data
# chmod -R 777 /data
# exportfs -avr
# systemctl restart nfs-server

############# Cluster configuration ###########################

Install nfs-client on all nodes:
# apt install nfs-common -y

Verify that nfs server is reachable:
# showmount -e <ip-of-nfs-server>

Create storage class:
# kubectl apply -f storageclass.yaml

Create pv:
# kubectl apply -f nfs-pv.yaml

Change the ns here:
# kubectl apply -f cluster-operator.yml

Check if the components are healthy in the rabbitmq-system namespace:
# kubectl get all -o wide -n <namespace>

Create RabbitMQ: Replace the rabbitmqcluster.yaml and change the ns in rabbitmqcluster.yaml
# git clone https://github.com/pavan-kumar-99/medium-manifests.git -b rabbitmq
# cp rabbitmqcluster.yaml medium-manifests/
# cd medium-manifests
# kubectl apply -f rabbitmqcluster.yaml

Default username and pass for this deployment is 'guest'

If you want to export rabbitmq configuratons to another deployment:
# kubectl -n <namespace> exec -it <name-of-rabbit-pod> -- /bin/bash
Inside the container go to the /tmp:
# cd /tmp
# rabbitmqctl export_definitions rabbit-config.txt

Then import inside the another pod:
# rabbitmqctl import_definitions rabbit-config.txt
