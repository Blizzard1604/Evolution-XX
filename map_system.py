"""
🗺️ Hierarchisches Map-System mit 3 Ebenen:
1. Weltkarte - Regionen
2. Regionen - Gebiete
3. Gebiete - Gebäude
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import random

class TerrainType(Enum):
    """Gelände-Typen für Gebiete (detailliert)"""
    GRASSLAND = "Grasland"      # 🌱 - gut für Bauernhöfe
    FOREST = "Wald"              # 🌲 - gut für Holz
    MOUNTAIN = "Berg"            # ⛰️ - gut für Minen
    SAND = "Sand"                # 🏜️ - Wüstensand
    RIVER = "Fluss"              # 🌊 - Wasser (nur Gebiet-Level)
    LAKE = "See"                 # 💧 - Wasser (nur Gebiet-Level)
    SWAMP = "Sumpf"              # 🌿 - schlecht

class WorldTerrainType(Enum):
    """Gelände-Typen für die Weltkarte (Biome) - dynamisch auswählbar"""
    MOUNTAINS = "Gebirge"        # ⛰️ - hohe Berge
    FOREST = "Waldland"          # 🌲 - dichte Wälder
    PLAINS = "Ebene"             # 🌾 - flaches Land
    COAST = "Küste"              # 🏖️ - Küstenlinie
    SEA = "Meer"                 # 🌊 - offenes Meer
    ISLANDS = "Inseln"           # ⛱️ - Inselgruppen
    SWAMP = "Sumpf"              # 🌿 - Sumpfgebiet
    DESERT = "Wüste"             # 🏜️ - Wüsteland
    RIVER_DELTA = "Flussdelta"   # 🏞️ - Flussmündung

@dataclass
class Gebiet:
    """Ein einzelnes Gebiet in einer Region - hier werden Gebäude gebaut"""
    id: int
    name: str
    x: int  # Position in der Region (0-9)
    y: int
    terrain_type: TerrainType
    buildings: Dict[int, 'Building'] = field(default_factory=dict)
    resources: Dict[str, int] = field(default_factory=lambda: {
        "WOOD": 0, "STONE": 0, "WHEAT": 0, "FLOUR": 0, 
        "FOOD": 0, "GOLD": 0, "IRON": 0, "IRON_ORE": 0
    })
    population: int = 0
    workers: Dict[int, Tuple[str, Optional[int]]] = field(default_factory=dict)
    
    def get_emoji(self) -> str:
        """Emoji für Terrain-Typ"""
        emojis = {
            TerrainType.GRASSLAND: "🌱",
            TerrainType.FOREST: "🌲",
            TerrainType.MOUNTAIN: "⛰️",
            TerrainType.SAND: "🏜️",
            TerrainType.RIVER: "🌊",
            TerrainType.LAKE: "💧",
            TerrainType.SWAMP: "🌿",
        }
        return emojis.get(self.terrain_type, "?")
    
    def get_bonus_resources(self) -> dict:
        """Welche Ressourcen sind in diesem Gelände besser erreichbar?"""
        bonuses = {
            TerrainType.GRASSLAND: {"WHEAT": 1.5},
            TerrainType.FOREST: {"WOOD": 1.5},
            TerrainType.MOUNTAIN: {"STONE": 1.5, "IRON_ORE": 1.5},
            TerrainType.SAND: {},  # Sand hat keine Boni
            TerrainType.RIVER: {"FOOD": 1.3},
            TerrainType.LAKE: {"FOOD": 1.5},
            TerrainType.SWAMP: {},
        }
        return bonuses.get(self.terrain_type, {})

@dataclass
class Building:
    """Ein Gebäude in einem Gebiet"""
    id: int
    building_type: str
    gebiet_id: int
    x: int  # Position im Gebiet (0-4)
    y: int
    workers: int = 0
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.building_type,
            "gebiet_id": self.gebiet_id,
            "x": self.x,
            "y": self.y,
            "workers": self.workers,
        }

@dataclass
class Region:
    """Eine Region mit mehreren Gebieten"""
    id: int
    name: str
    x: int  # Position auf Weltkarte (0-4)
    y: int
    world_terrain: 'WorldTerrainType' = None  # Terrain der Weltkarte (Parent)
    gebiete: Dict[int, Gebiet] = field(default_factory=dict)
    gebiet_counter: int = 0
    
    def __post_init__(self):
        """Generiere Gebiete für diese Region"""
        if not self.gebiete:
            self.generate_gebiete()
    
    def generate_gebiete(self):
        """Erstelle 25 Gebiete (5x5 Grid) mit Terrainen basierend auf World-Terrain"""
        # Basiere die Terrainen auf dem World-Terrain dieser Region
        if self.world_terrain == WorldTerrainType.MOUNTAINS:
            # Bergige Region - viele Berge
            terrains = [
                TerrainType.MOUNTAIN, TerrainType.MOUNTAIN, TerrainType.MOUNTAIN, TerrainType.GRASSLAND, TerrainType.MOUNTAIN,
                TerrainType.MOUNTAIN, TerrainType.GRASSLAND, TerrainType.MOUNTAIN, TerrainType.FOREST, TerrainType.MOUNTAIN,
                TerrainType.GRASSLAND, TerrainType.MOUNTAIN, TerrainType.MOUNTAIN, TerrainType.MOUNTAIN, TerrainType.GRASSLAND,
                TerrainType.MOUNTAIN, TerrainType.FOREST, TerrainType.GRASSLAND, TerrainType.MOUNTAIN, TerrainType.MOUNTAIN,
                TerrainType.GRASSLAND, TerrainType.MOUNTAIN, TerrainType.MOUNTAIN, TerrainType.GRASSLAND, TerrainType.MOUNTAIN,
            ]
        elif self.world_terrain == WorldTerrainType.FOREST:
            # Waldige Region - viele Wälder
            terrains = [
                TerrainType.FOREST, TerrainType.FOREST, TerrainType.FOREST, TerrainType.FOREST, TerrainType.GRASSLAND,
                TerrainType.FOREST, TerrainType.GRASSLAND, TerrainType.FOREST, TerrainType.FOREST, TerrainType.FOREST,
                TerrainType.FOREST, TerrainType.FOREST, TerrainType.SWAMP, TerrainType.FOREST, TerrainType.GRASSLAND,
                TerrainType.GRASSLAND, TerrainType.FOREST, TerrainType.FOREST, TerrainType.FOREST, TerrainType.FOREST,
                TerrainType.FOREST, TerrainType.GRASSLAND, TerrainType.FOREST, TerrainType.FOREST, TerrainType.FOREST,
            ]
        elif self.world_terrain == WorldTerrainType.PLAINS:
            # Ebene Region - viel Grasland
            terrains = [
                TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND,
                TerrainType.GRASSLAND, TerrainType.FOREST, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND,
                TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.RIVER, TerrainType.GRASSLAND,
                TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.FOREST,
                TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.FOREST, TerrainType.GRASSLAND, TerrainType.GRASSLAND,
            ]
        elif self.world_terrain == WorldTerrainType.COAST:
            # Küstenregion - mix mit Wasser und Land
            terrains = [
                TerrainType.GRASSLAND, TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.LAKE, TerrainType.GRASSLAND,
                TerrainType.RIVER, TerrainType.GRASSLAND, TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.FOREST,
                TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.RIVER, TerrainType.GRASSLAND,
                TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.FOREST, TerrainType.GRASSLAND, TerrainType.LAKE,
                TerrainType.GRASSLAND, TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.LAKE, TerrainType.GRASSLAND,
            ]
        elif self.world_terrain == WorldTerrainType.SEA:
            # Meer-Region - hauptsächlich Wasser (kann nicht besiedelt werden)
            terrains = [
                TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE,
                TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE,
                TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE,
                TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE,
                TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE, TerrainType.LAKE,
            ]
        elif self.world_terrain == WorldTerrainType.ISLANDS:
            # Inseln - kleine Landflecken in Wasser
            terrains = [
                TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.LAKE,
                TerrainType.FOREST, TerrainType.LAKE, TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.FOREST,
                TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.LAKE, TerrainType.LAKE, TerrainType.GRASSLAND,
                TerrainType.GRASSLAND, TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.LAKE, TerrainType.LAKE,
                TerrainType.LAKE, TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.FOREST, TerrainType.LAKE,
            ]
        elif self.world_terrain == WorldTerrainType.SWAMP:
            # Sumpf-Region - mooriges Land
            terrains = [
                TerrainType.SWAMP, TerrainType.SWAMP, TerrainType.LAKE, TerrainType.SWAMP, TerrainType.SWAMP,
                TerrainType.SWAMP, TerrainType.LAKE, TerrainType.SWAMP, TerrainType.SWAMP, TerrainType.GRASSLAND,
                TerrainType.LAKE, TerrainType.SWAMP, TerrainType.SWAMP, TerrainType.SWAMP, TerrainType.LAKE,
                TerrainType.SWAMP, TerrainType.SWAMP, TerrainType.GRASSLAND, TerrainType.SWAMP, TerrainType.SWAMP,
                TerrainType.LAKE, TerrainType.SWAMP, TerrainType.SWAMP, TerrainType.LAKE, TerrainType.SWAMP,
            ]
        elif self.world_terrain == WorldTerrainType.DESERT:
            # Wüste - viel Sand mit gelegentlichen Flüssen und seltenen Oasen
            terrains = [
                TerrainType.SAND, TerrainType.SAND, TerrainType.SAND, TerrainType.SAND, TerrainType.SAND,
                TerrainType.SAND, TerrainType.SAND, TerrainType.SAND, TerrainType.SAND, TerrainType.LAKE,
                TerrainType.SAND, TerrainType.SAND, TerrainType.SAND, TerrainType.SAND, TerrainType.SAND,
                TerrainType.SAND, TerrainType.RIVER, TerrainType.SAND, TerrainType.SAND, TerrainType.SAND,
                TerrainType.SAND, TerrainType.SAND, TerrainType.SAND, TerrainType.RIVER, TerrainType.SAND,
            ]
        elif self.world_terrain == WorldTerrainType.RIVER_DELTA:
            # Flussdelta - Wasser und Land durcheinander
            terrains = [
                TerrainType.GRASSLAND, TerrainType.RIVER, TerrainType.GRASSLAND, TerrainType.RIVER, TerrainType.GRASSLAND,
                TerrainType.RIVER, TerrainType.GRASSLAND, TerrainType.RIVER, TerrainType.GRASSLAND, TerrainType.GRASSLAND,
                TerrainType.GRASSLAND, TerrainType.RIVER, TerrainType.GRASSLAND, TerrainType.RIVER, TerrainType.GRASSLAND,
                TerrainType.RIVER, TerrainType.GRASSLAND, TerrainType.LAKE, TerrainType.GRASSLAND, TerrainType.RIVER,
                TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.RIVER, TerrainType.GRASSLAND, TerrainType.GRASSLAND,
            ]
        else:  # PLAINS fallback
            terrains = [
                TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND,
                TerrainType.GRASSLAND, TerrainType.FOREST, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND,
                TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.RIVER, TerrainType.GRASSLAND,
                TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.FOREST,
                TerrainType.GRASSLAND, TerrainType.GRASSLAND, TerrainType.FOREST, TerrainType.GRASSLAND, TerrainType.GRASSLAND,
            ]
        
        random.shuffle(terrains)
        
        idx = 0
        for y in range(5):
            for x in range(5):
                gebiet = Gebiet(
                    id=self.gebiet_counter,
                    name=f"{self.name}-Gebiet-{self.gebiet_counter + 1}",
                    x=x,
                    y=y,
                    terrain_type=terrains[idx]
                )
                self.gebiete[self.gebiet_counter] = gebiet
                self.gebiet_counter += 1
                idx += 1
    
    def get_gebiet(self, gebiet_id: int) -> Optional[Gebiet]:
        return self.gebiete.get(gebiet_id)
    
    def get_all_gebiete(self) -> List[Gebiet]:
        return list(self.gebiete.values())
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "gebiete_count": len(self.gebiete),
        }

@dataclass
class Weltkarte:
    """Die Weltkarte mit Regionen und World-Terrainen"""
    width: int = 5
    height: int = 5
    regionen: Dict[int, Region] = field(default_factory=dict)
    region_counter: int = 0
    world_terrain: Dict[Tuple[int, int], WorldTerrainType] = field(default_factory=dict)
    
    # Biom-Kompatibilität: Welche Biome können nebeneinander liegen
    BIOME_COMPATIBLE = {
        WorldTerrainType.MOUNTAINS: [
            WorldTerrainType.MOUNTAINS, WorldTerrainType.PLAINS, 
            WorldTerrainType.FOREST, WorldTerrainType.COAST
        ],
        WorldTerrainType.FOREST: [
            WorldTerrainType.FOREST, WorldTerrainType.PLAINS, 
            WorldTerrainType.MOUNTAINS, WorldTerrainType.SWAMP
        ],
        WorldTerrainType.PLAINS: [
            WorldTerrainType.PLAINS, WorldTerrainType.FOREST, 
            WorldTerrainType.MOUNTAINS, WorldTerrainType.DESERT, 
            WorldTerrainType.COAST, WorldTerrainType.RIVER_DELTA
        ],
        WorldTerrainType.COAST: [
            WorldTerrainType.COAST, WorldTerrainType.SEA, 
            WorldTerrainType.ISLANDS, WorldTerrainType.PLAINS, 
            WorldTerrainType.MOUNTAINS, WorldTerrainType.RIVER_DELTA
        ],
        WorldTerrainType.SEA: [
            WorldTerrainType.SEA, WorldTerrainType.COAST, 
            WorldTerrainType.ISLANDS
        ],
        WorldTerrainType.ISLANDS: [
            WorldTerrainType.ISLANDS, WorldTerrainType.SEA, 
            WorldTerrainType.COAST
        ],
        WorldTerrainType.SWAMP: [
            WorldTerrainType.SWAMP, WorldTerrainType.FOREST, 
            WorldTerrainType.PLAINS, WorldTerrainType.RIVER_DELTA
        ],
        WorldTerrainType.DESERT: [
            WorldTerrainType.DESERT, WorldTerrainType.PLAINS, 
            WorldTerrainType.RIVER_DELTA
        ],
        WorldTerrainType.RIVER_DELTA: [
            WorldTerrainType.RIVER_DELTA, WorldTerrainType.PLAINS, 
            WorldTerrainType.COAST, WorldTerrainType.SWAMP, WorldTerrainType.DESERT
        ],
    }
    
    def __post_init__(self):
        """Generiere Regionen und World-Terrainen für die Weltkarte"""
        if not self.world_terrain:
            self.generate_world_terrain()
        if not self.regionen:
            self.generate_regionen()
    
    def get_compatible_biomes(self, terrain: WorldTerrainType) -> list:
        """Hole kompatible Biome für ein gegebenes Terrain"""
        return self.BIOME_COMPATIBLE.get(terrain, list(WorldTerrainType))
    
    def get_neighbors(self, x: int, y: int) -> Dict[str, Optional[WorldTerrainType]]:
        """Hole alle Nachbarn einer Position"""
        neighbors = {
            'north': self.world_terrain.get((x, y - 1)) if y > 0 else None,
            'south': self.world_terrain.get((x, y + 1)) if y < self.height - 1 else None,
            'west': self.world_terrain.get((x - 1, y)) if x > 0 else None,
            'east': self.world_terrain.get((x + 1, y)) if x < self.width - 1 else None,
        }
        return neighbors
    
    def generate_world_terrain(self):
        """Generiere natürliche, kohärente Weltkarte mit echten Küstenlinien"""
        
        # PHASE 1: Erstelle Landmassen und Meere (ohne Küste)
        self._generate_base_continents()
        
        # PHASE 2: Glätte die Landmassen/Meere
        self._smooth_terrain_iterations(2)
        
        # PHASE 3: Generiere detaillierte Biome auf Landmassen
        self._expand_land_biomes()
        
        # PHASE 4: Glätte nochmal
        self._smooth_terrain_iterations(1)
        
        # PHASE 5: Generiere Küstenlinien automatisch
        self._generate_coastlines()
    
    def _generate_base_continents(self):
        """Erstelle grobe Kontinentale Struktur"""
        # Perlin-ähnliche Generierung für Kontinente
        # Verwende einfache Regel: basierend auf Position Cluster bilden
        for y in range(self.height):
            for x in range(self.width):
                # Erzeuge "Inseln" von Land und Wasser
                distance_from_center = abs(x - self.width // 2) + abs(y - self.height // 2)
                
                # Innerer Bereich = eher Land, Ränder = eher Meer
                if distance_from_center <= 3:
                    # Kontinentales Zentrum - hauptsächlich Land
                    if random.random() < 0.85:
                        base = random.choice([WorldTerrainType.PLAINS, WorldTerrainType.FOREST, WorldTerrainType.MOUNTAINS])
                    else:
                        base = WorldTerrainType.SEA
                elif distance_from_center <= 4:
                    # Grenzbereich - gemischt
                    base = random.choice([
                        WorldTerrainType.PLAINS, WorldTerrainType.SEA, 
                        WorldTerrainType.ISLANDS, WorldTerrainType.FOREST
                    ])
                else:
                    # Rand = hauptsächlich Wasser
                    base = random.choice([WorldTerrainType.SEA, WorldTerrainType.ISLANDS])
                
                self.world_terrain[(x, y)] = base
    
    def _smooth_terrain_iterations(self, iterations: int):
        """Glätte die Terrains über mehrere Iterationen"""
        for iteration in range(iterations):
            new_terrain = dict(self.world_terrain)
            
            for y in range(self.height):
                for x in range(self.width):
                    current = self.world_terrain[(x, y)]
                    neighbors = self.get_neighbors(x, y)
                    neighbor_terrains = [t for t in neighbors.values() if t is not None]
                    
                    if neighbor_terrains:
                        # Finde häufigsten Nachbar-Typ
                        most_common = max(set(neighbor_terrains), key=neighbor_terrains.count)
                        
                        # Wenn aktuell nicht kompatibel, ersetze es
                        compatible = self.get_compatible_biomes(most_common)
                        
                        if current not in compatible:
                            new_terrain[(x, y)] = most_common
            
            self.world_terrain = new_terrain
    
    def _expand_land_biomes(self):
        """Ersetze einfache Land-Typen durch detaillierte Biome"""
        for y in range(self.height):
            for x in range(self.width):
                current = self.world_terrain[(x, y)]
                
                # Ersetze einfache Plains/Forest durch spezialisierte Biome
                if current in [WorldTerrainType.PLAINS, WorldTerrainType.FOREST]:
                    # Basierend auf Nachbarn detailliertes Biom wählen
                    neighbors = self.get_neighbors(x, y)
                    neighbor_terrains = [t for t in neighbors.values() if t is not None]
                    
                    has_mountain = WorldTerrainType.MOUNTAINS in neighbor_terrains
                    has_water = WorldTerrainType.SEA in neighbor_terrains or WorldTerrainType.ISLANDS in neighbor_terrains
                    
                    if current == WorldTerrainType.PLAINS:
                        if has_mountain and random.random() < 0.4:
                            self.world_terrain[(x, y)] = WorldTerrainType.MOUNTAINS
                        elif has_water and random.random() < 0.3:
                            self.world_terrain[(x, y)] = random.choice([WorldTerrainType.RIVER_DELTA, WorldTerrainType.SWAMP])
                        elif random.random() < 0.4:
                            self.world_terrain[(x, y)] = WorldTerrainType.DESERT
                    
                    elif current == WorldTerrainType.FOREST:
                        if has_mountain and random.random() < 0.5:
                            self.world_terrain[(x, y)] = WorldTerrainType.MOUNTAINS
                        elif random.random() < 0.3:
                            self.world_terrain[(x, y)] = WorldTerrainType.SWAMP
    
    def _generate_coastlines(self):
        """Generiere Küsten automatisch an Grenzen zwischen Land und Meer"""
        for y in range(self.height):
            for x in range(self.width):
                current = self.world_terrain[(x, y)]
                neighbors = self.get_neighbors(x, y)
                neighbor_terrains = [t for t in neighbors.values() if t is not None]
                
                # Landen neben Wasser = Küste
                is_land = current in [
                    WorldTerrainType.PLAINS, WorldTerrainType.FOREST, 
                    WorldTerrainType.MOUNTAINS, WorldTerrainType.DESERT,
                    WorldTerrainType.SWAMP, WorldTerrainType.RIVER_DELTA
                ]
                
                has_sea_neighbor = WorldTerrainType.SEA in neighbor_terrains
                
                # Wenn Land neben Meer liegt, mache es zur Küste
                if is_land and has_sea_neighbor:
                    self.world_terrain[(x, y)] = WorldTerrainType.COAST
                
                # Insel-Muster: kleine Land-Inseln in Wasser
                elif current == WorldTerrainType.ISLANDS:
                    # Bleibe Island
                    pass
    
    
    def _smooth_isolated_biomes(self):
        """Glätte isolierte Biome, die nicht zu ihren Nachbarn passen"""
        for y in range(self.height):
            for x in range(self.width):
                current = self.world_terrain[(x, y)]
                neighbors = self.get_neighbors(x, y)
                neighbor_terrains = [t for t in neighbors.values() if t is not None]
                
                # Wenn zu viele Nachbarn inkompatibel sind, ändere das aktuelle Terrain
                incompatible_count = 0
                for neighbor in neighbor_terrains:
                    if current not in self.get_compatible_biomes(neighbor):
                        incompatible_count += 1
                
                if incompatible_count >= 3:  # Zu isoliert
                    compatible = []
                    for neighbor in neighbor_terrains:
                        compatible.extend(self.get_compatible_biomes(neighbor))
                    
                    if compatible:
                        # Wähle das häufigste kompatible Terrain
                        self.world_terrain[(x, y)] = max(set(compatible), 
                                                         key=compatible.count)
    
    def get_world_terrain(self, x: int, y: int) -> WorldTerrainType:
        """Hole Terrain für eine Position auf der Weltkarte"""
        return self.world_terrain.get((x, y), WorldTerrainType.PLAINS)
    
    def get_world_terrain_emoji(self, terrain: WorldTerrainType) -> str:
        """Emoji für World-Terrain"""
        emojis = {
            WorldTerrainType.MOUNTAINS: "⛰️",
            WorldTerrainType.FOREST: "🌲",
            WorldTerrainType.PLAINS: "🌾",
            WorldTerrainType.COAST: "🏖️",
            WorldTerrainType.SEA: "🌊",
            WorldTerrainType.ISLANDS: "⛱️",
            WorldTerrainType.SWAMP: "🌿",
            WorldTerrainType.DESERT: "🏜️",
            WorldTerrainType.RIVER_DELTA: "🏞️",
        }
        return emojis.get(terrain, "?")
    
    def get_region_name_for_biome(self, biome: WorldTerrainType) -> str:
        """Generiere einen Region-Namen basierend auf dem Biom"""
        biome_names = {
            WorldTerrainType.MOUNTAINS: [
                "Gebirgskette", "Berghöhe", "Felsenreich", "Schattengipfel", "Kristallspitzen"
            ],
            WorldTerrainType.FOREST: [
                "Urwald", "Waldgeflüster", "Baumreich", "Grüne Tiefe", "Waldmark"
            ],
            WorldTerrainType.PLAINS: [
                "Ebenenland", "Grasflur", "Flachland", "Wiesenmark", "Offenland"
            ],
            WorldTerrainType.COAST: [
                "Küstenzone", "Strandmark", "Buchtland", "Küstenwacht", "Salzküste"
            ],
            WorldTerrainType.SEA: [
                "Meerzone", "Tiefe See", "Gewässer", "Meeresbereich", "Ozeanmark"
            ],
            WorldTerrainType.ISLANDS: [
                "Inselgruppe", "Archipel", "Inselwelt", "Inselvolk", "Eilandkette"
            ],
            WorldTerrainType.SWAMP: [
                "Sumpfland", "Moorgebiet", "Feuchtland", "Schilfmark", "Paludal"
            ],
            WorldTerrainType.DESERT: [
                "Wüstenland", "Sandsee", "Trockenzone", "Dürrereich", "Sandmark"
            ],
            WorldTerrainType.RIVER_DELTA: [
                "Flussdelta", "Deltamark", "Flussebene", "Wasserlabyrinth", "Deltazone"
            ],
        }
        
        names = biome_names.get(biome, ["Unbekannte Region"])
        return random.choice(names)
    
    def generate_regionen(self):
        """Erstelle Regionen für die ganze Welt (5x5 Grid) mit zufälligen Biomen"""
        for y in range(self.height):
            for x in range(self.width):
                world_terrain = self.get_world_terrain(x, y)
                region_name = self.get_region_name_for_biome(world_terrain)
                
                region = Region(
                    id=self.region_counter,
                    name=region_name,
                    x=x,
                    y=y,
                    world_terrain=world_terrain
                )
                self.regionen[self.region_counter] = region
                self.region_counter += 1
    
    def get_region(self, region_id: int) -> Optional[Region]:
        return self.regionen.get(region_id)
    
    def get_all_regionen(self) -> List[Region]:
        return list(self.regionen.values())
    
    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "regionen_count": len(self.regionen),
            "regionen": [r.to_dict() for r in self.get_all_regionen()]
        }

# ==================== Game State Management ====================

class MapNavigator:
    """Verwaltet Navigation zwischen den 3 Ebenen"""
    
    def __init__(self):
        self.weltkarte = Weltkarte()
        self.current_level = "world"  # "world", "region", "gebiet"
        self.current_region_id: Optional[int] = None
        self.current_gebiet_id: Optional[int] = None
    
    def goto_weltkarte(self):
        """Zur Weltkarte"""
        self.current_level = "world"
        self.current_region_id = None
        self.current_gebiet_id = None
        return self.get_weltkarte_state()
    
    def goto_region(self, region_id: int):
        """Zu einer Region"""
        if region_id not in self.weltkarte.regionen:
            return {"error": f"Region {region_id} nicht gefunden"}
        
        self.current_level = "region"
        self.current_region_id = region_id
        self.current_gebiet_id = None
        return self.get_region_state()
    
    def goto_gebiet(self, gebiet_id: int):
        """Zu einem Gebiet"""
        if self.current_region_id is None:
            return {"error": "Zunächst eine Region auswählen"}
        
        region = self.weltkarte.get_region(self.current_region_id)
        if gebiet_id not in region.gebiete:
            return {"error": f"Gebiet {gebiet_id} nicht gefunden"}
        
        self.current_level = "gebiet"
        self.current_gebiet_id = gebiet_id
        return self.get_gebiet_state()
    
    def get_weltkarte_state(self) -> dict:
        """State für Weltkarten-Ansicht mit World-Terrainen"""
        regionen_data = []
        for region in self.weltkarte.get_all_regionen():
            terrain_emoji = self.weltkarte.get_world_terrain_emoji(region.world_terrain)
            regionen_data.append({
                "id": region.id,
                "name": region.name,
                "x": region.x,
                "y": region.y,
                "world_terrain": region.world_terrain.name,
                "world_terrain_name": region.world_terrain.value,
                "emoji": terrain_emoji,
                "gebiete_count": len(region.gebiete),
            })
        
        return {
            "level": "world",
            "width": self.weltkarte.width,
            "height": self.weltkarte.height,
            "regionen": regionen_data,
        }
    
    def get_region_state(self) -> dict:
        """State für Regions-Ansicht"""
        if self.current_region_id is None:
            return {"error": "Keine Region ausgewählt"}
        
        region = self.weltkarte.get_region(self.current_region_id)
        gebiete_data = []
        for gebiet in region.get_all_gebiete():
            gebiete_data.append({
                "id": gebiet.id,
                "name": gebiet.name,
                "x": gebiet.x,
                "y": gebiet.y,
                "terrain": gebiet.terrain_type.name,
                "terrain_name": gebiet.terrain_type.value,
                "emoji": gebiet.get_emoji(),
                "buildings_count": len(gebiet.buildings),
            })
        
        return {
            "level": "region",
            "region_id": region.id,
            "region_name": region.name,
            "width": 5,
            "height": 5,
            "gebiete": gebiete_data,
        }
    
    def get_gebiet_state(self) -> dict:
        """State für Gebiets-Ansicht (wo Gebäude gebaut werden)"""
        if self.current_region_id is None or self.current_gebiet_id is None:
            return {"error": "Keine Region oder Gebiet ausgewählt"}
        
        region = self.weltkarte.get_region(self.current_region_id)
        gebiet = region.get_gebiet(self.current_gebiet_id)
        
        buildings_data = [b.to_dict() for b in gebiet.buildings.values()]
        
        return {
            "level": "gebiet",
            "region_id": region.id,
            "region_name": region.name,
            "gebiet_id": gebiet.id,
            "gebiet_name": gebiet.name,
            "terrain": gebiet.terrain_type.name,
            "terrain_name": gebiet.terrain_type.value,
            "emoji": gebiet.get_emoji(),
            "width": 5,
            "height": 5,
            "buildings": buildings_data,
            "resources": gebiet.resources,
            "population": gebiet.population,
            "workers_count": len(gebiet.workers),
        }
    
    def get_current_state(self) -> dict:
        """Hole aktuellen State basierend auf aktueller Ebene"""
        if self.current_level == "world":
            return self.get_weltkarte_state()
        elif self.current_level == "region":
            return self.get_region_state()
        elif self.current_level == "gebiet":
            return self.get_gebiet_state()
        else:
            return {"error": "Unbekannte Ebene"}
