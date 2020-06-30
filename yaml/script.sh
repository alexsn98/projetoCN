gcloud container clusters resize cloudcomputingcluster --num-nodes=5 --region=europe-west1-d
gcloud config set project cloudcomputingproject-272814
kubectl create -f workloads/country.yaml
kubectl create -f workloads/indicator.yaml
kubectl create -f workloads/serie.yaml
kubectl create -f workloads/spark.yaml
kubectl create deployment frontend --image=alexsn98/frontend_cn:latest
kubectl expose deployment country --type=NodePort --port 80 --target-port 5000
kubectl expose deployment indicator --type=NodePort --port 80 --target-port 5000
kubectl expose deployment serie --type=NodePort --port 80 --target-port 5000
kubectl expose deployment spark --type=NodePort --port 80 --target-port 5000
kubectl expose deployment frontend --type=NodePort --port 80
kubectl create -f ingress/my-ingress.yaml