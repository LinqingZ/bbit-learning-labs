import pika
import os

from consumer_interface import mqConsumerInterface

class mqConsumer(mqConsumerInterface):
    def __init__(self, binding_key: str, exchange_name: str, queue_name: str) -> None:
        # super().__init__(binding_key, exchange_name, queue_name)
        # super().setupRMQConnection()
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.setupRMQConnection()
    
    # setupRMQConnection Function: Establish connection to the RabbitMQ service, 
    # declare a queue and exchange, bind the binding key to the queue on the 
    # exchange and finally set up a callback function for receiving messages
    def setupRMQConnection(self) -> None:
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.queue_bind(
            queue= self.queue_name,
            routing_key= self.binding_key,
            exchange=self.exchange_name,
        )
        self.channel.basic_consume(
            self.queue_name, self.on_message_callback, auto_ack=False
        )

    # onMessageCallback: Print the UTF-8 string message and then close the connection.
    def on_message_callback(self, channel, method_frame, header_frame, body) -> None:
        self.channel.basic_ack(method_frame.delivery_tag, False)
        print(body)
    
    # startConsuming: Consumer should start listening for messages from the queue.
    def startConsuming(self) -> None:
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

        
    def __del__(self) -> None:
        self.channel.close()
        self.connection.close()
    

        
