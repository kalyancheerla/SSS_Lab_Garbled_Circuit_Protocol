# Setup for Lab assignment
1. Have a working k8's cluster with atleast 1 node.
   (Simply just install rancher-desktop which installs wsl, docker, k8's, kubectl & properly configures them)
2. Setting-up kafka
    * Create a separate namespace - `kubectl create namespace kafka-production`
    * Deploy strimzi crds - `kubectl create -f https://strimzi.io/install/latest?namespace=kafka-production -n kafka-production`
    * Check for strimzi operator for kafka to come up - `kubectl get pods -n kafka-production`
    * Now deploy 1 kafka and zookeeper instances using `kafka-zookeeper.yaml`
    * `kubectl apply -f kafka-zookeeper.yaml`
    * Check for kafka and zookeeper pods to come up - `kubectl get pods -n kafka-production`
    * Done with kafka setup. (with a way config is - we can observe the topic operator pod as well)
3. Now lets add some content into our kafka using our producer pod.
    * Build the producer image - `docker build -t producer .` (cd into producer folder)
    * Also, build the consumer image - `docker build -t consumer .` (cd into consumer folder)
    * Check for both the images in docker images - `docker images`
    * Now lets run our consumer pod interactively to observe the producer's messages.
    * Running consumer - `kubectl run consumer --rm --tty -i --image consumer:latest --image-pull-policy Never --restart Never --namespace kafka-production --command -- python /app/consumer.py kafka-cluster-kafka-bootstrap.kafka-production.svc.cluster.local:9092 chat`
    * Here, few important things are namespace, broker-address and topic.
    * For the broker-address, it is <name-of-the-kafka-cluster>-kafka-bootstrap.<namespace>.svc.cluster.local and port 9092.
    * For the topic, it could be anything.
    * Running producer - `kubectl run producer --rm --tty -i --image producer:latest --image-pull-policy Never --restart Never --namespace kafka-production --command -- python /app/producer.py kafka-cluster-kafka-bootstrap.kafka-production.svc.cluster.local:9092 chat`
    * To run producer, open another terminal and see them side-by-side for better understanding.
    * As we ran our producer interactively, we can observe 5 JSON messages being sent to the kafka broker.
    * Also, as consumer is started before the producer, we can observe these messages as well.
    * The producer should gracefully exit and remove itself, but for the consumer pod - we need to kill it by pressing CTRL-c (as many times as reqd.).
4. Build and deploy your malicious-pod and figure-out on how to sniff the data from kafka.

