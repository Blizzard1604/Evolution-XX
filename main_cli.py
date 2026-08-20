"""
🏰 EVOLUTION-XX - Terminal Mode
Klassisches text-basiertes Siedler-Simulation Spiel
"""

from game_engine import Game, WorkerType, BuildingType
import sys

def main():
    print("\n" + "="*60)
    print("  🏰 WILLKOMMEN BEI EVOLUTION-XX 🏰")
    print("  Terminal Mode")
    print("="*60)
    
    game = Game()
    print(game.get_status())
    print(get_help())
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0]
            
            if cmd == "quit":
                print("Auf Wiedersehen! 👋")
                break
            
            elif cmd == "help":
                print(get_help())
            
            elif cmd == "status":
                print_status(game)
            
            elif cmd == "next":
                result = game.next_turn()
                print(f"\n▶️  Turn {game.turn} verarbeitet...")
                if result["production"]:
                    print("📊 Produktion:")
                    for bid, prod in result["production"].items():
                        building = game.buildings[bid]
                        prod_str = ", ".join([f"{v} {k}" for k, v in prod.items()])
                        print(f"  {building.building_type}: {prod_str}")
                status = "✅" if result["fed"] else "⚠️"
                print(f"{status} Population versorgt: {result['food_amount']}/{game.population} Essen")
                print_status(game)
            
            elif cmd == "build":
                if len(parts) < 4:
                    print("❌ Verwendung: build <typ> <x> <y>")
                    continue
                
                building_name = parts[1].upper()
                try:
                    x, y = int(parts[2]), int(parts[3])
                    success, message, _ = game.add_building(building_name, x, y)
                    if success:
                        print(f"✅ {message}")
                    else:
                        print(f"❌ {message}")
                except (KeyError, ValueError):
                    print(f"❌ Unbekannter Gebäudetyp oder ungültige Koordinaten")
                    print(f"Verfügbare Gebäude: WAREHOUSE, LUMBERMILL, MILL, FARM, MINE, QUARRY, BARRACKS, BLACKSMITH")
            
            elif cmd == "hire":
                if len(parts) < 2:
                    print("❌ Verwendung: hire <typ> [building_id]")
                    continue
                
                worker_name = parts[1].upper()
                try:
                    building_id = int(parts[2]) if len(parts) > 2 else None
                    success, message = game.hire_worker(worker_name, building_id)
                    if success:
                        print(f"✅ {message}")
                    else:
                        print(f"❌ {message}")
                except (KeyError, ValueError):
                    print(f"❌ Unbekannter Arbeitertyp oder ungültige Building ID")
                    print(f"Verfügbare Arbeiter: LUMBERJACK, STONEMASON, FARMER, MILLER, MINER, SMITH, SOLDIER")
            
            elif cmd == "fire":
                if len(parts) < 2:
                    print("❌ Verwendung: fire <worker_id>")
                    continue
                
                try:
                    worker_id = int(parts[1])
                    success, message = game.fire_worker(worker_id)
                    if success:
                        print(f"✅ {message}")
                    else:
                        print(f"❌ {message}")
                except ValueError:
                    print("❌ Ungültige Worker ID")
            
            elif cmd == "list":
                if len(parts) < 2:
                    print("❌ Verwendung: list buildings | workers")
                    continue
                
                if parts[1] == "buildings":
                    print("\n🏠 GEBÄUDE:")
                    for building_id, building in game.buildings.items():
                        print(f"  [{building_id}] {building.building_type} at ({building.x},{building.y}) - {building.workers} Arbeiter")
                
                elif parts[1] == "workers":
                    print("\n👷 ARBEITER:")
                    for worker_id, (wtype, bid) in game.workers.items():
                        building = game.buildings.get(bid) if bid else None
                        loc = f"in {building.building_type}" if building else "arbeitslos"
                        print(f"  [{worker_id}] {wtype} {loc}")
            
            else:
                print("❌ Befehl nicht erkannt. Schreib 'help' für Hilfe.")
        
        except KeyboardInterrupt:
            print("\n\nSpiel unterbrochen. Auf Wiedersehen! 👋")
            break
        except Exception as e:
            print(f"❌ Fehler: {e}")

def print_status(game):
    status = f"\n{'='*60}\n"
    status += f"TURN {game.turn} | Population: {game.population}/{game.max_population} | Schatzkammer: {game.treasury}💰\n"
    status += f"{'='*60}\n"
    
    status += "📦 RESSOURCEN:\n"
    for resource_type, amount in game.resources.items():
        status += f"  {resource_type}: {amount}\n"
    
    status += f"\n🏠 GEBÄUDE ({len(game.buildings)}):\n"
    for building_id, building in game.buildings.items():
        status += f"  [{building_id}] {building.building_type} at ({building.x},{building.y}) - {building.workers} Arbeiter\n"
    
    status += f"\n👷 ARBEITER ({len(game.workers)}):\n"
    if not game.workers:
        status += "  Keine\n"
    else:
        for worker_id, (wtype, bid) in list(game.workers.items())[:10]:
            building = game.buildings.get(bid) if bid else None
            loc = f"in {building.building_type}" if building else "arbeitslos"
            status += f"  [{worker_id}] {wtype} {loc}\n"
        if len(game.workers) > 10:
            status += f"  ... und {len(game.workers) - 10} weitere\n"
    
    print(status)

def get_help():
    help_text = """
🎮 SIEDLER SIMULATION - BEFEHLE:
  
  🏗️  BAUEN:
    build <type> <x> <y>  - Gebäude bauen
    Typen: warehouse, lumbermill, quarry, farm, mill, mine, blacksmith, barracks
    
  👷 ARBEITER:
    hire <type> [building_id]  - Arbeiter einstellen
    Typen: lumberjack, stonemason, farmer, miller, miner, smith, soldier
    
    fire <worker_id>  - Arbeiter entlassen
    
  📋 LISTE:
    list buildings  - Alle Gebäude anzeigen
    list workers    - Alle Arbeiter anzeigen
    
  ⏭️  SPIEL:
    next    - Nächster Turn
    status  - Spielstand anzeigen
    
  ❓ HILFE:
    help  - Diese Hilfe anzeigen
    quit  - Spiel beenden
"""
    return help_text

if __name__ == "__main__":
    main()
