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
ineuron-Big-Data-Assignments/KafkaAssignment1-producer.py-code /
@Soumyapallebothula
Soumyapallebothula Rename KafkaAssignment-producer.py-code to KafkaAssignment1-producer.?
?
Latest commit 961eecd on Oct 3
 History
 1 contributor
173 lines (137 sloc)  5.53 KB

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# A simple example demonstrating use of JSONSerializer.

import argparse
from uuid import uuid4
from six.moves import input
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
#from confluent_kafka.schema_registry import *
import pandas as pd
from typing import List

FILE_PATH = "./restaurant_orders.csv"
columns=['order_number','order_date','item_name','quantity','product_price','total_products']

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


def get_order_instance(file_path):
    df=pd.read_csv(file_path)
    df=df.iloc[:,:]
    #print('Check1:',df.values)
    orders:List[Order]=[]    #list of Car objects
    for data in df.values:
        order=Order(dict(zip(columns,data)))
        #print('check2',dict(zip(columns,data)))
        orders.append(order)
        yield order

def order_to_dict(order:Order, ctx):
    """
    Returns a dict representation of a User instance for serialization.
    Args:
        user (User): User instance.
        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
    Returns:
        dict: Dict populated with user attributes to be serialized.
    """

    # User._address must not be serialized; omit from dict
    return order.record


def delivery_report(err, msg):
    """
    Reports the success or failure of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def main(topic):

    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    #get schema
    #Method-1
    #my_schema = schema_registry_client.get_schema(schema_id=100003).schema_str

    #Method-2
    topic = 'restaurant-take-away-data'
    my_schema = schema_registry_client.get_latest_version(topic+'-value').schema.schema_str  
    #print(my_schema)

    #To serialize the keys
    string_serializer = StringSerializer('utf_8')
    #to serialize json data
    json_serializer = JSONSerializer(my_schema, schema_registry_client, order_to_dict)     #hardcode : schema_str

    producer = Producer(sasl_conf())

    print("Producing user records to topic {}. ^C to exit.".format(topic))
    #while True:
        # Serve on_delivery callbacks from previous calls to produce()
    producer.poll(0.0)
    try:
        i=0
        for order in get_order_instance(file_path=FILE_PATH):

            print(order)
            producer.produce(topic=topic,
              #uuid4() generate random strings
              #everytime we produce a message it needs a key, if hardcode the key then message goes to same partition everytime
                            key=string_serializer(str(uuid4()), order_to_dict),
                            value=json_serializer(order, SerializationContext(topic, MessageField.VALUE)),
                            on_delivery=delivery_report)
            i+=1
#             if i>1:
#               #produce only two records
#               break
    except KeyboardInterrupt:
        pass
    except ValueError:
        print("Invalid input, discarding record...")
        pass

    print("\nFlushing records...")
    #flush the buffer memory
    producer.flush()

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
ineuron-Big-Data-Assignments/KafkaAssignment1-producer.py-code at main ? Soumyapallebothula/ineuron-Big-Data-Assignments ? GitHub