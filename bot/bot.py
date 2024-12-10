from sc2.bot_ai import BotAI, Race
from sc2.data import Result

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.buff_id import BuffId
from sc2.ids.upgrade_id import UpgradeId

from sc2.unit import Unit
from sc2.units import Units


class CompetitiveBot(BotAI):
    NAME: str = "SoO_Bot"
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
        # Send workers to gather
        await self.distribute_workers()
        
        # Build Drones  until 16 
        
        if self.supply_workers < 19:
            if self.can_afford(UnitTypeId.DRONE) and self.already_pending(UnitTypeId.DRONE) < 19:
                self.train(UnitTypeId.DRONE)
        
        # Builds Spawning Pool on 12 supply
        if self.supply_used >= 12:
            if (self.structures(UnitTypeId.SPAWNINGPOOL).amount + self.already_pending(UnitTypeId.SPAWNINGPOOL) == 0):   
                if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                    await self.build(UnitTypeId.SPAWNINGPOOL, near=self.townhalls.first)
             # Build queens
            elif (self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) < self.townhalls.amount):
                if self.structures(UnitTypeId.SPAWNINGPOOL).ready:
                    self.train(UnitTypeId.QUEEN)

            # If we have no extractor, build extractor
            if self.structures(UnitTypeId.SPAWNINGPOOL).ready and (self.structures(UnitTypeId.EXTRACTOR).amount + self.already_pending(UnitTypeId.EXTRACTOR) == 0) and self.workers:
                #self.workers.random.build(UnitTypeId.EXTRACTOR, self.vespene_geyser.closest_to(self.townhalls.first))
                await self.build(UnitTypeId.EXTRACTOR, self.vespene_geyser.closest_to(self.townhalls.first))
            
           

        #Build Overlords if supply is low
        if self.supply_left <2 and self.already_pending(UnitTypeId.OVERLORD) == 0:
            self.train(UnitTypeId.OVERLORD)

        #Queen Injecting
        main: Unit = self.townhalls.first
        if self.units(UnitTypeId.QUEEN).ready:
            for queen in self.units(UnitTypeId.QUEEN).idle:
                if queen.energy >= 25 and not main.has_buff(BuffId.QUEENSPAWNLARVATIMER):
                    queen(AbilityId.EFFECT_INJECTLARVA, main)

        # Building Zerglings
        if self.structures(UnitTypeId.SPAWNINGPOOL).ready and self.larva:
            if self.can_afford(UnitTypeId.ZERGLING):
                self.train(UnitTypeId.ZERGLING, self.larva.amount)

        
        # Build Movement Speed upgrade
        if self.already_pending_upgrade(UpgradeId.ZERGLINGMOVEMENTSPEED) == 0:
            if self.structures(UnitTypeId.SPAWNINGPOOL).ready:
                self.research(UpgradeId.ZERGLINGMOVEMENTSPEED)
        
        # Send units to attack when zergling speed is done
        if self.units(UnitTypeId.ZERGLING).ready and self.already_pending_upgrade(UpgradeId.ZERGLINGMOVEMENTSPEED) == 1:
            for zergling in self.units(UnitTypeId.ZERGLING).idle:
                zergling.attack(self.enemy_start_locations[0])

        



