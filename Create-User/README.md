Create a private key and csr
# openssl genrsa -out username.key 2048
# openssl req -new -key username.key -out username.csr -subj "/CN=username"
Create a certificate signing request
# kubectl create -f csr_template.yaml
# kubectl get csr
# kubectl certificate approve username-csr
Verify that the request is approved
# kubectl get csr
Extract user's certificate
# kubectl get csr username-csr -o jsonpath='{.status.certificate}' | base64 --decode > username.crt
Copy the existing kubeconfig file, rename it, then replace the values with values for username user. (You must change client-certificate-data, client-key-data and context parts)
# cp ~/.kube/config username.kubeconfig
Create a role
# kubectl apply -f username-cluster-role.yaml -f username-role-binding.yaml
Verify the permissions are correct
# kubectl --kubeconfig=username.kubeconfig get pods -n <namespace>
