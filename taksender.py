#!/usr/bin/env python3

import asyncio
import xml.etree.ElementTree as ET

from configparser import ConfigParser

import pytak
import socket
from time import sleep



class MySerializer(pytak.QueueWorker):
    """
    Defines how you process or generate your Cursor on Target Events.
    From there it adds the CoT Events to a queue for TX to a COT_URL.
    """

    async def handle_data(self, data):
        """Handle pre-CoT data, serialize to CoT Event, then puts on queue."""
        event = data
        await self.put_queue(event)

    async def run(self, number_of_iterations=-1):
        """Run the loop for processing or generating pre-CoT data."""
        while 1:
            data = gen_cot()
            await self.handle_data(data)
            await asyncio.sleep(10)

def gen_cot():
    """Generate CoT Event."""
    root = ET.Element("event")
    root.set("version", "2.0")
    root.set("type", "a-n-A-M-A")  # insert your type of marker
    root.set("uid", "Tetris")
    root.set("how", "m-g") 
    root.set("time", pytak.cot_time())
    root.set("start", pytak.cot_time())
    root.set(
        "stale", pytak.cot_time(600)
    )  # time difference in seconds from 'start' when stale initiates

    pt_attr = {
        "lat": "60.120809",  # set your lat (this loc points to Central Park NY)
        "lon": "24.417518",  # set your long (this loc points to Central Park NY)
        "hae": "0",
        "ce": "10",
        "le": "10",
    }
    
    ET.SubElement(root, "point", attrib=pt_attr)

    contact_attr = {
        "callsign": "Tetris",
        "endpoint": "192.168.68.102_4242_udp",
    }

    detail = ET.SubElement(root, "detail")
    ET.SubElement(detail, "contact", attrib=contact_attr)

    return ET.tostring(root)


async def main():
    """Main definition of your program, sets config params and
    adds your serializer to the asyncio task list.
    """
    config = ConfigParser()
    config["mycottool"] = {"COT_URL": "udp://239.2.3.1:6969"}
    config = config["mycottool"]
    print (config["COT_URL"])
    # Initializes worker queues and tasks.
    clitool = pytak.CLITool(config)
    await clitool.setup()

    # Add your serializer to the asyncio task list.
    clitool.add_tasks(set([MySerializer(clitool.tx_queue, config)]))

    # Start all tasks.
    await clitool.run()


if __name__ == "__main__":
    asyncio.run(main())
