import random
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from map_system import MapNavigator, Gebiet, Building

# ==================== Enums ====================
class ResourceType(Enum):
    # Grundrohstoffe
    WOOD = "Holz"
    STONE = "Stein"
    SAND = "Sand"
    WATER = "Wasser"
    CLAY = "Lehm"
    
    # Landwirtschaftliche Produkte    
    WHEAT = "Getreide"
    VEGETABLES = "Gemüse"
    FRUITS = "Obst"

    # Tierische Produkte
    MEAT = "Fleisch"
    LEATHER = "Leder"
    FISH = "Fisch"
    
    #Nutztiere
    HORSE = "Pferd"
    DONKEY = "Esel"

    # Bergbau
    IRON_ORE = "Eisenerz"
    GOLD_ORE = "Golderz"
    COAL = "Kohle"
    COPPER_ORE = "Kupfererz"
    SILVER_ORE = "Silbererz"
    SALT = "Salz"

    # Verarbeitete Baumaterialien
    PLANKS = "Bretter"
    BRICKS = "Ziegel"
    GLASS = "Glas"
    
    # Verarbeitete Nahrungsmittel
    FLOUR = "Mehl"
    BREAD = "Brot"
    WURST = "Wurst"

    # Verarbeitete Metalle
    IRON = "Eisen"
    STEEL = "Stahl"
    SILVER = "Silber"
    COPPER = "Kupfer"

    #Metallprodukte
    TOOLS = "Werkzeuge"

    #Militärprodukte
    SWORD = "Schwert"
    BOW = "Bogen"
    ARROW = "Pfeil"
    SPEER = "Speer"
    SHIELD = "Schild"
    IRON_ARMOR = "Eisenrüstung"
    LETHER_ARMOR = "Leder-Rüstung"

    # Handel
    GOLD = "Gold"
    
class BuildingType(Enum):
    # Grundversorgung
    WELL = "Brunnen"
    PIT = "Grube" # Sand und Lehm

    # Landwirtschaftliche Gebäude
    FARM = "Bauernhof"
    HUNTERHUT = "Jagdhaus"

    # Tierhaltung
    PIG_FARM = "Schweinezucht"
    HORSE_FARM = "Pferdezucht"
    DONKEY_FARM = "Eselzucht"

    # Fischerei
    FISHING_HUT = "Fischerhütte"

    # Bergbau
    IRON_MINE = "Eisenmine"
    GOLD_MINE = "Goldmine"
    COAL_MINE = "Kohlemine"
    COPPER_MINE = "Kupfermine"
    SILVER_MINE = "Silbermine"
    SALT_MINE = "Salzmine"

    # Holzverarbeitung
    FORESTER = "Förster"
    WOODCUTTER = "Holzfällerhütte"
    SAWMILL = "Sägewerk"
    CHARCOAL_BURNING = "Köhlerei"

    # Verarbeitete Baumaterialien
    BRICKWORKS = "Ziegelbrennerei"
    GLASSWORKS = "Glashütte"

    # Verarbeitete Nahrungsmittel
    MILL = "Mühle"
    BAKERY = "Bäckerei"
    BUTCHER = "Metzgerei"

    # Metallverarbeitung
    SMELTER = "Schmelzofen"
    TOOL_SMITH = "Werkzeugschmiede"
    WEAPON_SMITH = "Waffenschmiede"

    # Militärprodukte
    WEAPON_WORKSHOP = "Waffenwerkstatt"
    ARMORY = "Rüstungsschmiede"

    # Lagerung
    WAREHOUSE = "Lagerhaus"

    # Wohnen
    HOUSE = "Haus"

    # Bildung
    SCHOOL = "Schule"
    UNIVERSITY = "Universität"

    # Gesellschaft
    MARKET = "Marktplatz"
    TAVERN = "Taverne"

    # Militär
    BARRACKS = "Kaserne"
    TRAINING_GROUND = "Trainingsgelände"
    GUARD_TOWER = "Wachturm"

    # Infrastruktur
    ROAD = "Straße"

class WorkerType(Enum):

    # Freie Arbeitskräfte
    FREE_WORKER = "Freier Arbeiter"

    # Grundberufe
    LUMBERJACK = "Holzfäller"
    FORESTER = "Förster"
    STONEMASON = "Steinmetz"
    WORKER = "Arbeiter"
    CRAFTSMAN = "Handwerker"

    # Nahrungsversorgung
    FARMER = "Bauer"
    MILLER = "Müller"
    COOK = "Koch"
    BREEDER = "Züchter"
    FISHERMAN = "Fischer"
    HUNTER = "Jäger"

    # Bergbau und Metallverarbeitung
    MINER = "Bergmann"
    SMITH = "Schmied"
    CHARCOAL_BURNER = "Köhler"

    # Bau und Gelände
    BUILDER = "Bauarbeiter"
    PLANNER = "Planierer"

    # Militär
    SOLDIER = "Soldat"
    ARCHER = "Bogenschütze"
    CAVALRY = "Kavallerist"

    # Handel und Transport
    MERCHANT = "Händler"
    CARRIER = "Träger"

    # Bildung und Verwaltung
    SCHOLAR = "Gelehrter"

# ==================== Data Classes ====================
@dataclass
class Building:
    id: int
    building_type: str
    x: int
    y: int
    workers: int = 0
    storage: Dict[str, int] = None
    production_rate: float = 1.0
    
    def __post_init__(self):
        if self.storage is None:
            self.storage = defaultdict(int)

# ==================== Game Manager ====================
class Game:
    def __init__(self, width: int = 20, height: int = 20, initial_pop: int = 10):
        # Neue Map-Navigation
        self.map_navigator = MapNavigator()
        
        # Globale Spielstatistiken
        self.turn = 0
        self.population = initial_pop  # Globale Population
        self.max_population = 100
        self.treasury = 100
        
        # Globale Ressourcen (Lager)
        self.global_resources = defaultdict(int)
        self.global_resources["WOOD"] = 200
        self.global_resources["STONE"] = 150
        self.global_resources["WHEAT"] = 120
        self.global_resources["FOOD"] = 150
        
        # Building Counter für IDs
        self.building_counter = 0
        self.worker_counter = 0
    
    def get_state(self) -> dict:
        """Hole aktuellen State (inkl. Map-Ebene)"""
        map_state = self.map_navigator.get_current_state()
        
        state = {
            "turn": self.turn,
            "population": self.population,
            "max_population": self.max_population,
            "treasury": self.treasury,
            "global_resources": dict(self.global_resources),
            "map": map_state,
        }
        
        return state
    
    # ==================== Navigation ====================
    def goto_world(self):
        """Gehe zur Weltkarte"""
        self.map_navigator.goto_weltkarte()
        return {
            "success": True,
            "state": self.get_state()
        }
    
    def goto_region(self, region_id: int):
        """Gehe zu einer Region"""
        result = self.map_navigator.goto_region(region_id)
        if "error" in result:
            return {"success": False, "message": result["error"]}
        
        return {
            "success": True,
            "state": self.get_state()
        }
    
    def goto_gebiet(self, gebiet_id: int):
        """Gehe zu einem Gebiet"""
        result = self.map_navigator.goto_gebiet(gebiet_id)
        if "error" in result:
            return {"success": False, "message": result["error"]}
        
        return {
            "success": True,
            "state": self.get_state()
        }
    
    # ==================== Gebäude bauen ====================
    def add_building(self, building_type: str, x: int, y: int) -> Tuple[bool, str]:
        """Baue ein Gebäude im aktuellen Gebiet"""
        if self.map_navigator.current_level != "gebiet":
            return False, "Du bist nicht in einem Gebiet!"
        
        if self.map_navigator.current_region_id is None or self.map_navigator.current_gebiet_id is None:
            return False, "Keine Region/Gebiet ausgewählt!"
        
        # Besorge das Gebiet
        region = self.map_navigator.weltkarte.get_region(self.map_navigator.current_region_id)
        gebiet = region.get_gebiet(self.map_navigator.current_gebiet_id)
        
        # Überprüfe Koordinaten
        if not (0 <= x < 5 and 0 <= y < 5):
            return False, f"Koordinaten außerhalb des Gebiets! (5x5)"
        
        # Überprüfe ob Platz frei
        for b in gebiet.buildings.values():
            if b.x == x and b.y == y:
                return False, "Dieser Platz ist bereits besetzt!"
        
        # Überprüfe Kosten
        costs = self.get_building_costs(building_type)
        for resource, amount in costs.items():
            if self.global_resources[resource] < amount:
                return False, f"Nicht genug {resource}! Benötigt: {amount}, Vorhanden: {self.global_resources[resource]}"
        
        # Deduct costs
        for resource, amount in costs.items():
            self.global_resources[resource] -= amount
        
        # Erstelle Gebäude
        building = Building(
            id=self.building_counter,
            building_type=building_type,
            gebiet_id=self.map_navigator.current_gebiet_id,
            x=x,
            y=y,
        )
        self.building_counter += 1
        gebiet.buildings[building.id] = building
        
        return True, f"✅ {building_type} gebaut an ({x}, {y})"
    
    @staticmethod
    def get_building_costs(building_type: str) -> Dict[str, int]:
        """Baukosten für Gebäudetypen"""
        costs = {
            "WAREHOUSE": {"STONE": 50, "WOOD": 20},
            "LUMBERMILL": {"STONE": 30, "WOOD": 50},
            "MILL": {"STONE": 40, "WOOD": 30},
            "FARM": {"WOOD": 20},
            "MINE": {"STONE": 60, "WOOD": 40},
            "QUARRY": {"WOOD": 30},
            "BARRACKS": {"STONE": 80, "WOOD": 40},
            "BLACKSMITH": {"STONE": 50, "WOOD": 40},
        }
        return costs.get(building_type, {})
    
    # ==================== Arbeiter ====================
    def hire_worker(self, worker_type: str, gebiet_id: Optional[int] = None) -> Tuple[bool, str]:
        """Stelle einen Arbeiter an"""
        if self.population <= 0:
            return False, "Keine Population verfügbar!"
        
        if self.map_navigator.current_level != "gebiet":
            return False, "Du musst in einem Gebiet sein!"
        
        if self.map_navigator.current_region_id is None or self.map_navigator.current_gebiet_id is None:
            return False, "Keine Region/Gebiet ausgewählt!"
        
        region = self.map_navigator.weltkarte.get_region(self.map_navigator.current_region_id)
        gebiet = region.get_gebiet(self.map_navigator.current_gebiet_id)
        
        worker_id = self.worker_counter
        self.worker_counter += 1
        
        gebiet.workers[worker_id] = (worker_type, None)
        gebiet.population += 1
        self.population -= 1
        
        return True, f"✅ {worker_type} eingestellt im Gebiet"
    
    # ==================== Ressourcen ====================
    def produce_resources(self):
        """Verarbeite Produktion in allen Gebieten"""
        production_log = []
        
        # Iteriere über alle Regionen und Gebiete
        for region in self.map_navigator.weltkarte.get_all_regionen():
            for gebiet in region.get_all_gebiete():
                for building in gebiet.buildings.values():
                    if building.workers == 0:
                        continue
                    
                    # Produktionslogik basierend auf Gebäudetyp
                    if building.building_type == "LUMBERMILL":
                        amount = int(building.workers * 2)
                        gebiet.resources["WOOD"] += amount
                        self.global_resources["WOOD"] += amount
                        production_log.append(f"{gebiet.name}: +{amount} Holz")
                    
                    elif building.building_type == "QUARRY":
                        amount = int(building.workers * 2)
                        gebiet.resources["STONE"] += amount
                        self.global_resources["STONE"] += amount
                        production_log.append(f"{gebiet.name}: +{amount} Stein")
                    
                    elif building.building_type == "FARM":
                        amount = int(building.workers * 2)
                        gebiet.resources["WHEAT"] += amount
                        self.global_resources["WHEAT"] += amount
                        production_log.append(f"{gebiet.name}: +{amount} Getreide")
        
        return production_log
    
    def next_turn(self):
        """Verarbeite einen Turn"""
        self.turn += 1
        
        prod_log = self.produce_resources()
        
        # Population versorgen
        food_needed = self.population
        food_available = self.global_resources["FOOD"]
        
        if food_available >= food_needed:
            self.global_resources["FOOD"] -= food_needed
            fed = True
        else:
            starved = food_needed - food_available
            self.population -= min(starved, self.population)
            self.global_resources["FOOD"] = 0
            fed = False
        
        return {
            "turn": self.turn,
            "fed": fed,
            "food_amount": min(food_available, food_needed),
            "production": prod_log
        }
