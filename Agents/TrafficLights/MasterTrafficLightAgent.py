import time
from datetime import datetime, timedelta
from typing import Optional

from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message


def get_inverse_status(status):
    if status == "red":
        return "green"
    else:
        return "red"


class MasterTrafficLightAgent(Agent):
    def __init__(self, jid, password, environment, x, y, size, angle, right_traffic_jid, left_traffic_jid, front_traffic_jid):
        super().__init__(jid, password)
        self.environment = environment

        self.x = x
        self.y = y
        self.size = size
        self.angle = angle

        self.right_traffic_jid = right_traffic_jid
        self.left_traffic_jid = left_traffic_jid
        self.front_traffic_jid = front_traffic_jid

        self.traffic_light = self.environment.add_traffic_light(jid, x, y, size, angle, "red")

        self.environment.update_light_status(self.jid, self.traffic_light, "red")

    async def setup(self):
        class PeriodicBehav(PeriodicBehaviour):
            async def run(self):
                # Muda o seu estado periodicamente
                if self.agent.environment.get_light_status(self.agent.jid) == "red":
                    time.sleep(4)
                    self.agent.environment.update_light_status(self.agent.jid, self.agent.traffic_light, "green")
                    self.agent.environment.add_traffic_light(self.agent.jid, self.agent.x, self.agent.y, self.agent.size, self.agent.angle, "green")
                else:
                    self.agent.environment.update_light_status(self.agent.jid, self.agent.traffic_light, "yellow")
                    self.agent.environment.add_traffic_light(self.agent.jid, self.agent.x, self.agent.y, self.agent.size, self.agent.angle, "yellow")

                    # time.sleep(2)

                    self.agent.environment.update_light_status(self.agent.jid, self.agent.traffic_light, "red")
                    self.agent.environment.add_traffic_light(self.agent.jid, self.agent.x, self.agent.y, self.agent.size, self.agent.angle, "red")

                # Informa os outros semáforos associados a este master para trocarem de estado
                if self.agent.left_traffic_jid is not None:
                    await self.send_communication(self.agent.left_traffic_jid, get_inverse_status(self.agent.environment.get_light_status(self.agent.jid)))

                if self.agent.right_traffic_jid is not None:
                    await self.send_communication(self.agent.right_traffic_jid, get_inverse_status(self.agent.environment.get_light_status(self.agent.jid)))

                if self.agent.front_traffic_jid is not None:
                    await self.send_communication(self.agent.front_traffic_jid, self.agent.environment.get_light_status(self.agent.jid))

            async def on_end(self):
                # stop agent from behaviour
                await self.agent.stop()

            async def send_communication(self, jid, status):
                msg = Message(to=str(jid))
                msg.set_metadata("status", status)
                msg.body = "Change your status"

                await self.send(msg)

        start_at = datetime.now() + timedelta(seconds=2)
        period = PeriodicBehav(period=10, start_at=start_at)
        self.add_behaviour(period)
