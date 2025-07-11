############# NFS server side configuratuons #####################

Install nfs-server:
# apt install nfs-server nfs-kernel-server -y

Check the status:
# systemctl status nfs-server

If you want to use firewalld, then add the ports from the output of the below command to firewalld:
# ss -tlpn | grep mount
# firewall-cmd --add-service={nfs,mountd,rpc-bind} --permanent

Add folders to export:
# mkdir /data
# vi /etc/exports
    /data/rabbit-prod <source-subnet-which-we-want-to-have-access-to-our-nfs-server>/24(rw,sync,no_subtree_check,no_root_squash,no_all_squash,insecure)
# chown -R nobody:nogroup /data
# chmod -R 777 /data
# exportfs -avr
# systemctl restart nfs-server
# showmount -e localhost

############# Cluster configuration ###########################

Install nfs-client on all nodes:
# apt install nfs-common -y

Verify that nfs server is reachable:
# showmount -e <ip-of-nfs-server>

Add helm repo for nfs provisioner (below commands will also install storageclass name nfs-client for us)
# helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
# helm install nfs-subdir-external-provisioner --create-namespace --namespace nfs nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=<ip-of-nfs-server> \
    --set nfs.path=/data

Create a test pvc to see if it works:
# cat << EOF > test-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 100Mi
  storageClassName: nfs-client
EOF
