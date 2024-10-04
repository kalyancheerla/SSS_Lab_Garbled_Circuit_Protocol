# Task 1 - Setup
* Check if rancher desktop is running properly or not, if not launch the rancher desktop.
* Attach a screenshot of rancher desktop running properly and also one for Cluster dashboard with the pods (cluster-\>nodes-\>click-on-node).
* Open powershell and verify if the kubernetes node was running or not, by using
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
* Command - `kubectl run bot1 --rm --tty -i --image chatbot:latest --image-pull-policy Never --restart Never --namespace kafka-production --command -- python /app/main.py <Your-EUID> <SomeRandomChatRoomNameYouChoose>`
* Lets understand the above command, as we need to run a second instance of it. Here, we are using `kubectl` to `run` a pod named `bot1` with flags set to remove it automatically, open a interactive shell, using the image `chatbot:latest` which we built previosuly using docker and other flags set not to pull image from online and not to restart the pod. Also, requesting to create the pod in the `kafka-production` namespace and overwrite the command that pod runs with our python command where you have to specify your EUID and other details.
* Now open another terminal, deploy another kubernetes pod named bot2 with all other flags and details retaining same but using your partner's EUID and the same chat room id that you had used above. Now you can chat with eachother on these terminals.
* Now you can send messages in the two terminals with each other, so lets simulate a chat instance between you and your partner exchanging greetings (also, send at least 5 messages from each side for better simulation purposes).
* Now send some secret details like a fake username (Your-EUID+Your-Partners-EUID) and a fake password (Your-FullName+Your-Partners-FullName) in one of your chats.
* As these messages traverse between you and your partner through kafka and the kafka instance created here stores them.
* Now you are tasked to retrieve these details but you should not create any more pods in the `kafka-production` namespace.

# Task 3 - Deploy your malicious-pod
* To do the retrieval, we will create a malicious flask pod (deployed in test-pipeline namespace) which takes some details and helps in retriving our chats.
* For building the chatbot use `docker build -t chatbot .` (cd into appropriate dir).
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
