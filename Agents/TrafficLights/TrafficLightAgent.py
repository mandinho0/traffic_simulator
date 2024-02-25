import asyncio
from datetime import datetime, timedelta

from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour


class TrafficLightAgent(Agent):
    def __init__(self, jid, password, environment, tl_coordinates, front_tl_coordinates, left_tl_coordinates,
                 right_tl_coordinates):

        super().__init__(jid, password)
        self.environment = environment
        self.main_status = "green"

        # Guarda as coordenadas de todos os semaforos
        self.tl_coordinates = tl_coordinates
        self.front_tl_coordinates = front_tl_coordinates
        self.left_tl_coordinates = left_tl_coordinates
        self.right_tl_coordinates = right_tl_coordinates

        # Inicializa todos os semaforos como null
        self.tl = None
        self.front_tl = None
        self.left_tl = None
        self.right_tl = None

        self.initialize_trafficlights(jid, tl_coordinates, front_tl_coordinates, left_tl_coordinates,
                                      right_tl_coordinates)

    async def setup(self):
        class PeriodicBehav(PeriodicBehaviour):
            async def run(self):
                # Muda o seu estado periodicamente
                if self.agent.main_status == "red":
                    self.agent.main_status = "green"
                    asyncio.create_task(self.atualiza_tl_NOK(self.agent.left_tl, str(self.agent.jid) + "_3", self.agent.left_tl_coordinates))
                    asyncio.create_task(self.atualiza_tl_NOK(self.agent.right_tl, str(self.agent.jid) + "_4", self.agent.right_tl_coordinates))
                    await asyncio.sleep(4)
                    asyncio.create_task(self.atualiza_tl_OK(self.agent.tl, str(self.agent.jid) + "_1", self.agent.tl_coordinates))
                    asyncio.create_task(self.atualiza_tl_OK(self.agent.front_tl, str(self.agent.jid) + "_2", self.agent.front_tl_coordinates))
                else:
                    self.agent.main_status = "red"
                    asyncio.create_task(self.atualiza_tl_NOK(self.agent.tl, str(self.agent.jid) + "_1", self.agent.tl_coordinates))
                    asyncio.create_task(self.atualiza_tl_NOK(self.agent.front_tl, str(self.agent.jid) + "_2", self.agent.front_tl_coordinates))
                    await asyncio.sleep(4)
                    asyncio.create_task(self.atualiza_tl_OK(self.agent.left_tl, str(self.agent.jid) + "_3", self.agent.left_tl_coordinates))
                    asyncio.create_task(self.atualiza_tl_OK(self.agent.right_tl, str(self.agent.jid) + "_4", self.agent.right_tl_coordinates))

            async def atualiza_tl_OK(self, agent, jid, coordinates):
                if agent is not None:
                    self.agent.environment.update_light_status(jid, agent, "green")

            async def atualiza_tl_NOK(self, agent, jid, coordinates):
                if agent is not None:
                    self.agent.environment.update_light_status(jid, agent, "yellow")

                    #await asyncio.sleep(2)

                    self.agent.environment.update_light_status(jid, agent, "red")

            async def on_end(self):
                # stop agent from behaviour
                await self.agent.stop()

        start_at = datetime.now() + timedelta(seconds=2)
        period = PeriodicBehav(period=20, start_at=start_at)
        self.add_behaviour(period)

    def initialize_trafficlights(self, jid, tl_coordinates, front_tl_coordinates, left_tl_coordinates,
                                 right_tl_coordinates):

        self.tl = self.environment.add_traffic_light(jid + "_1", tl_coordinates.x, tl_coordinates.y,
                                                     tl_coordinates.size, tl_coordinates.angle, "green")

        if front_tl_coordinates is not None:
            self.front_tl = self.environment.add_traffic_light(jid + "_2", front_tl_coordinates.x, front_tl_coordinates.y,
                                                               front_tl_coordinates.size, front_tl_coordinates.angle,
                                                               "green")

        if left_tl_coordinates is not None:
            self.left_tl = self.environment.add_traffic_light(jid + "_3", left_tl_coordinates.x, left_tl_coordinates.y,
                                                              left_tl_coordinates.size, left_tl_coordinates.angle,
                                                              "red")

        if right_tl_coordinates is not None:
            self.right_tl = self.environment.add_traffic_light(jid + "_4", right_tl_coordinates.x, right_tl_coordinates.y,
                                                               right_tl_coordinates.size, right_tl_coordinates.angle,
                                                               "red")
