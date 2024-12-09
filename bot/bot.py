from sc2.bot_ai import BotAI, Race
from sc2.data import Result


from sc2.ids.unit_typeid import UnitTypeId


class CompetitiveBot(BotAI):
    NAME: str = "CompetitiveBot"
    """This bot's name"""

    RACE: Race = Race.Zerg
    """This bot's Starcraft 2 race.
    Options are:
        Race.Terran
        Race.Zerg
        Race.Protoss
        Race.Random
    """
    async def on_start(self):
        """
        This code runs once at the start of the game
        Do things here before the game starts
        """
        print("Game started")


    async def on_step(self, iteration: int):
        
        if self.supply_used >= 12:
            if (
                    self.structures(
                        UnitTypeId.SPAWNINGPOOL).amount
                    + self.already_pending(
                        UnitTypeId.SPAWNINGPOOL)
                    == 0
                ):
            
                if self.can_afford(
                    UnitTypeId.SPAWNINGPOOL
                    ):    
                    await self.build(
                        UnitTypeId.SPAWNINGPOOL, 
                        near=self.townhalls.first
                    )

       
        if self.structures(
            UnitTypeId.SPAWNINGPOOL
            ).ready and self.larva:
            if self.can_afford(UnitTypeId.ZERGLING):
                self.train(
                    UnitTypeId.ZERGLING, 
                    self.larva.amount)

        if self.units(UnitTypeId.ZERGLING).ready:
            for zergling in self.units(
                UnitTypeId.ZERGLING
                ):
                zergling.attack(
                    self.enemy_start_locations[0]
                    )






