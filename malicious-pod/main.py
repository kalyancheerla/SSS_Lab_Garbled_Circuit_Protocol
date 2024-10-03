from flask import Flask, request, render_template, jsonify
from producer import producer_create
from producer import p_create
from consumer import consumer_create
from consumer import c_create

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('pc-setup-form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    sslchoice = request.form['sslchoice']
    porc = request.form['porc']
    messages = request.form['messages']
    bserver = request.form['bserver']
    clientid = request.form['clientid']
    topic = request.form['topic']
    sprotocol = request.form['sprotocol']
    smechanism = request.form['smechanism']
    suser = request.form['suser']
    spass = request.form['spass']

    if porc == 'p':
        if sslchoice == 'yes':
            producer = producer_create(bserver, clientid, sprotocol, smechanism, suser, spass)
        else:
            producer = producer_create(bserver, clientid)

        producer_consumer_list = p_create(producer, topic, messages)

    else:
        if sslchoice == 'yes':
            consumer = consumer_create(topic, bserver, clientid, sprotocol, smechanism, suser, spass)
        else:
            consumer = consumer_create(topic, bserver, clientid)

        producer_consumer_list = c_create(consumer)

    list_to_str = ' '.join(map(str, producer_consumer_list))

    return list_to_str


@app.route('/api', methods=['POST'])
def api_form_post():
    print("starting api")
    kafka_task = {
        'sslchoice': request.json['sslchoice'],
        'porc': request.json['porc'],
        'messages': request.json['messages'],
        'bserver': request.json['bserver'],
        'clientid': request.json['clientid'],
        'topic': request.json['topic']
        }

    print("about to start creating p or c")
    if kafka_task.get('porc') == 'p':
        if kafka_task.get('sslchoice') == 'yes':
            producer = producer_create(kafka_task.get('bserver'), kafka_task.get('clientid'),
                                       kafka_task.get('sprotocol'), kafka_task.get('smechanism'),
                                       kafka_task.get('suser'), kafka_task.get('spass'))
        else:
            producer = producer_create(kafka_task.get('bserver'), kafka_task.get('clientid'))

        producer_consumer_list = p_create(producer, kafka_task.get('topic'), int(kafka_task.get('messages')))

    else:
        print("Entering consumer")
        if kafka_task.get('sslchoice') == 'yes':
            consumer = consumer_create(kafka_task.get('topic'), kafka_task.get('bserver'), kafka_task.get('clientid'),
                                       kafka_task.get('sprotocol'), kafka_task.get('smechanism'),
                                       kafka_task.get('suser'), kafka_task.get('spass'))
        else:
            print("about to create consumer")
            consumer = consumer_create(kafka_task.get("topic"), kafka_task.get("bserver"), kafka_task.get("clientid"))

        producer_consumer_list = c_create(consumer)

    list_to_str = ' '.join(map(str, producer_consumer_list))

    return list_to_str


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

