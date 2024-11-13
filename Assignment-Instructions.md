# Task 1 - Setup
* Check if k3s is running properly or not, if not set it up using instructions for setup.
* Attach a screenshot of k3s running properly and also one for kuberntes dashboard showing workload status for all namespaces.
    * Use `systemctl status k3s.service` to get k3s service status.
    * Use `kubectl -n kubernetes-dashboard create token student` for getting student user access token.
    * Then use `kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard-kong-proxy 8443:443 --address 0.0.0.0`
      for port forwarding and then use the access token from previous command and visit `https://localhost:8443/#/workloads?namespace=_all`
      to get the screenshot.
    * For accessing kubernetes-dashboard, we need to portforward everytime and the terminal will be occupied with that command.
    * To close it, use ctrl-c and if you want to always access it then leave this command running and use different terminal for other commands.
* Open terminal and verify if the kubernetes setup was running or not, by using
  `kubectl get pods -A` (which prints all the pods present in the kuberntes system).
* Attach a screenshot of the output.
* Now verify, specifically if there are pods running in `kafka-production` namespace, by using
  `kubectl get pods -n kafka-production`.
* Attach a screenshot of the output.
* You should observe, a strimzi operator pod, zookeeper pod, kafka-broker pod, & other in *running state*.
* With this you have a proper kubernetes setup with kafka deployed and running properly.

# Task 2 - Insert Data into kafka
* For this task, lets understand what & how kafka being used in real world.
    * kafka is a distributed, scalable, & fault-tolerant stream processing platform, which works using publish-subscriber model.
    * Producers send data to Kafka topics, and consumers read from those topics independently.
    * Data persists for a configured time, even after it’s consumed by subscribers.
    * kafka is widely used in companies like LinkedIn, Netflix, and Uber for processing large volumes of real-time data and handling event-driven architectures.

```
      Simple architecture diagram of kafka.
      +------------+       +-----------+         +--------------+
      |  Producer  | --->  |  Kafka    | ---->   |  Consumer(s) |
      | (App/Data) |       |  Cluster  |         | (App/Data)   |
      +------------+       +-----------+         +--------------+
                              |    |
                            Zookeeper
                          (Coordination)
```
* Even discord uses it for its messaging services, and we will also run a simple cli-chatbot to do the same.
* Clone the repo, `https://github.com/kalyancheerla/SSS_Lab_K8s_Cross_Namespace_Access_Vulnerability.git`.
* Change directory into cli-chatbot to build it using `docker` by using `docker build -t chatbot .`.
* Verify if it is built successfully or not using `docker image ls`.
* Now lets use the built docker image to deploy a pod running in kubernetes, lets also run it interactively as we need to exchange messages.
* We need to export the docker image and import in k3s to run it as pod, and below are the commands for it.
    * `docker save -o chatbot.tar chatbot:latest` - save the chatbot:latest image as chatbot.tar file.
    * `sudo ctr images import chatbot.tar` - import the chatbot.tar file into k3s ctr images.
    * `sudo ctr images ls | grep chatbot` - verify the import.
* Command - `kubectl run bot1 --rm --tty -i --image chatbot:latest --image-pull-policy Never --restart Never --namespace kafka-production --command -- python /app/main.py <Your-EUID> <SomeRandomChatRoomNameYouChoose>`
* Lets understand the above command, as we need to run a second instance of it. Here, we are using `kubectl` to `run` a pod named `bot1` with flags set to remove it automatically, open a interactive shell, using the image `chatbot:latest` which we built previosuly using docker and other flags set not to pull image from online and not to restart the pod. Also, requesting to create the pod in the `kafka-production` namespace and overwrite the command that pod runs with our python command where you have to specify your EUID and other details.
* Now open another terminal, deploy another kubernetes pod named bot2 with all other flags and details retaining same but using your partner's EUID and the same chat room id that you had used above. Now you can chat with eachother on these terminals.
* Now you can send messages in the two terminals with each other, so lets simulate a chat instance between you and your partner exchanging greetings (also, send at least 5 messages from each side for better simulation purposes).
* Now send some secret details like a fake username (Your-EUID+Your-Partners-EUID) and a fake password (Your-FullName+Your-Partners-FullName) in one of your chats.
* As these messages traverse between you and your partner through kafka and the kafka instance created here stores them.
* Now you are tasked to retrieve these details but you should not create any more pods in the `kafka-production` namespace.

# Task 3 - Deploy your malicious-pod
* To do the retrieval, we will create a malicious flask pod (deployed in test-pipeline namespace) which takes some details and helps in retriving our chats.
* For building the malicious-pod use `docker build -t malicious-pod .` (cd into appropriate dir).
* We need to export the docker image and import in k3s to run it as pod, and below are the commands for it.
    * `docker save -o malicious-pod.tar malicious-pod:latest` - save the malicious-pod:latest image as malicious-pod.tar file.
    * `sudo ctr images import malicious-pod.tar` - import the malicious-pod.tar file into k3s ctr images.
    * `sudo ctr images ls | grep malicious-pod` - verify the import.
* For deploying our flask pod use `kubectl apply -f flask-app.yaml` (file is present in the repo provided).
* We can access the flask app on `localhost:30000`.
* Now you need to understand the flask application and figure-out the details that need to go in the html form.

# Task 4 - Exploit the kafka-cluster to retrieve the messages
* Once all the details were figured-out, provide a screenshot with all these values in the html form.
* Attach a screenshot where the form succeeds in retrieving the info about your chats.
* The screenshot should contain your above messages that you had sent in Task 2.
* Hola! you had successfully exploited the provided kafka system.

# Task 5 - Reflection
* So, what have you done in here?
* Why is a pod deployed in test-pipeline had internal access to a pod deployed in kafka-production namespace?
* Reflect on what you had done in at least 2 paragraphs, explaining the attack.

# Task 6 - Feedback (No points)
* Provide your feedback on the lab, so that we can improve it for future students.
