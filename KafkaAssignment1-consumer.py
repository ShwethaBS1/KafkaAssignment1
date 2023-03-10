Skip to content
Product
Solutions
Open Source
Pricing
Search
Sign in
Sign up
Soumyapallebothula
/
ineuron-Big-Data-Assignments
Public
Code
Issues
Pull requests
Actions
Projects
Security
Insights
ineuron-Big-Data-Assignments/KafkaAssignment1-consumer.py-code
@Soumyapallebothula
Soumyapallebothula Rename KafkaAssignment-consumer.py-code to KafkaAssignment1-consumer.?
?
Latest commit 1402aa4 on Oct 3
 History
 1 contributor
102 lines (78 sloc)  3.38 KB

import argparse
import datetime
import csv

from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
API_KEY = 'U7AMUKXPHFK2OWCS'
ENDPOINT_SCHEMA_URL  = 'https://psrc-8kz20.us-east-2.aws.confluent.cloud'
API_SECRET_KEY = '7YpeRlRpE8F3tHjuXEE+jgPlNKfuUcR0XjM/2zQuWjdvoBGsx3QBjL5ggdEYSrL6'
BOOTSTRAP_SERVER = 'pkc-lzvrd.us-west4.gcp.confluent.cloud:9092'
SECURITY_PROTOCOL = 'SASL_SSL'
SSL_MACHENISM = 'PLAIN'
SCHEMA_REGISTRY_API_KEY = '2BZKDZPGOMN5ZXC4'
SCHEMA_REGISTRY_API_SECRET = 'mUqb34z0+ubS1+srQqttUwflYni7o+742R2JFp1vqz72SwZLd9qPqRxWmPc7xECD'
def sasl_conf():

    sasl_conf = {'sasl.mechanism': SSL_MACHENISM,
                 # Set to SASL_SSL to enable TLS support.
                #  'security.protocol': 'SASL_PLAINTEXT'}
                'bootstrap.servers':BOOTSTRAP_SERVER,
                'security.protocol': SECURITY_PROTOCOL,
                'sasl.username': API_KEY,
                'sasl.password': API_SECRET_KEY
                }
    return sasl_conf
def schema_config():
    return {'url':ENDPOINT_SCHEMA_URL,
    
    'basic.auth.user.info':f"{SCHEMA_REGISTRY_API_KEY}:{SCHEMA_REGISTRY_API_SECRET}"

    }
class Order:   
    def __init__(self,record:dict):
        for k,v in record.items():
            setattr(self,k,v)
        
        self.record=record
   
    @staticmethod
    def dict_to_order(data:dict,ctx):
        return Order(record=data)

    def __str__(self):
        return f"{self.record}"


def main(topic):


    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    my_schema = schema_registry_client.get_schema(schema_id=100003).schema_str

    json_deserializer = JSONDeserializer(my_schema,
                                         from_dict=Order.dict_to_order)

    consumer_conf = sasl_conf()
    consumer_conf.update({
                     'group.id': 'group1',
                     'auto.offset.reset': "earliest"})     #or earliest, latest

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    counter=0
    with open('./output.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['order_number','order_date','item_name','quantity','product_price','total_products'])
        while True:
            try:
                # SIGINT can't be handled when polling, limit timeout to 1 second.
                msg = consumer.poll(1.0)
                if msg is None:
                    continue

                order = json_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))

                if order is not None:
                    counter+=1
                    print(datetime.datetime.now())
                    print("User record {}: order: {}\n"
                          .format(msg.key(), order))

                    #print(type(order.record))
                    #print(order.record.values())
                    rowList = []
                    for col in order.record.values():
                        rowList.append(col)

                    w.writerow(rowList)

                    print('Total messages fetched till now:', counter)
                    
            except KeyboardInterrupt:
                break

    consumer.close()

main("restaurant-take-away-data")
Footer
? 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
ineuron-Big-Data-Assignments/KafkaAssignment1-consumer.py-code at main ? Soumyapallebothula/ineuron-Big-Data-Assignments ? GitHub