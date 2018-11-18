from webthing import (Action, Event, Property, SingleThing, Thing, Value,
        WebThingServer)
from sense_hat import SenseHat
import logging
import datetime
import uuid
import time


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


sense = SenseHat()
sense.rotation = 90
temp = sense.get_temperature()

sense.show_message("Hello World")
sense.show_message("Temp: " +  str(temp))


#class SenseHatWebThing:
#    """A Web Thing enable Raspberry PI SenseHat"""
#
#    #def __init__(self):
#    pass


class HelloAction(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, 'hello', input_=input_)

    def perform_action(self):
        sense.show_message("hello")
        self.thing.set_property('text', self.input['text'])
	
def make_thing():
    thing = Thing('Sense Hat', type_='Sense Hat', description= 'A Web Thing Enable Raspberry PI Sense Hat')
    thing.add_property(
            Property(thing, 
                    'on',
                    Value(True),
                    metadata={
                        '@type': 'OnOffProperty',
                        'label': 'On/Off',
                        'type': 'boolean',
                        'description': 'Whether the Sense Hat is turned on',
                    }))
    thing.add_available_action(
        'Hello',
        {
            'label': 'Hello',
            'description': 'Make the sense hat say hello',
            'input': {
                'type': 'object',
                'required': [
                    'text',
                    ],
                'properties': {
                    'text': {
                        'type': 'string',
                        },
                    },
                },
            },
        HelloAction)

    return thing

def run_server():
    thing = make_thing()
    server = WebThingServer(SingleThing(thing), port=8888)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stoping the server')
        server.stop()
        logging.info('done')



if __name__=='__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
