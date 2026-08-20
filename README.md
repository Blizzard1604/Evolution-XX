# 🏰 Evolution-XX - Siedler Simulation

Eine text-basierte Strategiesimulation im Stil von "Die Siedler". Baue dein Reich auf, verwalte Ressourcen und wirtschaft, während du deine Population versorgst!

## 🎮 Features

- **Ressourcensystem**: Holz, Stein, Getreide, Mehl, Essen, Gold, Eisen
- **Gebäude**: Verschiedene Produktionsstätten (Sägewerk, Steinbruch, Farm, Mühle, Mine, Schmiede)
- **Arbeiter**: Stelle Arbeiter an und verwalte die Arbeitskräfte
- **Produktion**: Automatische Ressourcenproduktion basierend auf Arbeitern
- **Nahrungs-Management**: Versorge deine Population mit Essen
- **Wachstum**: Die Population wächst bei guter Versorgung
- **Zufallsereignisse**: Gelegentliche Bonusbelohnungen

## 🚀 Spielstart

```bash
python main.py
```

## 📋 Befehle

### Gebäude bauen
```
build <typ> <x> <y>
```
**Verfügbare Gebäudetypen:**
- `warehouse` - Lagerhaus (Startgebäude)
- `lumbermill` - Sägewerk (produziert Holz)
- `quarry` - Steinbruch (produziert Stein)
- `farm` - Bauernhof (produziert Getreide)
- `mill` - Mühle (verarbeitet Getreide zu Mehl)
- `mine` - Mine (produziert Eisenerz)
- `blacksmith` - Schmiede (verarbeitet Eisenerz zu Eisen)
- `barracks` - Kaserne (Militär)

**Beispiel:**
```
build lumbermill 5 5
```

### Arbeiter einstellen
```
hire <typ> [building_id]
```
**Verfügbare Arbeitertypen:**
- `lumberjack` - Holzfäller
- `stonemason` - Steinmetz
- `farmer` - Bauer
- `miller` - Müller
- `miner` - Bergmann
- `smith` - Schmied
- `soldier` - Soldat

**Beispiel:**
```
hire lumberjack 0
```

### Spielkontrolle
- `next` - Nächsten Turn durchführen
- `status` - Spielstand anzeigen
- `help` - Hilfe anzeigen
- `quit` - Spiel beenden

## 🎯 Spielmechaniken

### Ressourcen
- **Produktion**: Arbeiter in Gebäuden produzieren automatisch Ressourcen
- **Verarbeitung**: Manche Gebäude verwandeln Rohstoffe in fertige Produkte
  - Mühle: Getreide → Mehl
  - Schmiede: Eisenerz → Eisen

### Population
- **Verbrauch**: Jeder Einwohner benötigt 1 Essen pro Turn
- **Wachstum**: Bei ausreichend Essen besteht eine 30% Chance für Wachstum
- **Maximale Größe**: 50 Einwohner

### Wirtschaft
- **Schatzkammer**: Gelegentliche Bonusbelohnungen (10% Chance pro Turn)
- **Ressourcenverwaltung**: Alle Ressourcen sind begrenzt

## 💡 Tipps zum Spielen

1. **Prioritäten setzen**:
   - Starte mit Sägewerk und Steinbruch für Rohstoffe
   - Baue schnell eine Farm auf für Nahrungsversorgung
   - Erweitere dann zu spezialisierteren Gebäuden

2. **Arbeitskräfte**:
   - Verteile Arbeiter sinnvoll auf Gebäude
   - Versorge deine Arbeiter mit Essen!
   - Arbeitslose Arbeiter kosten keine Ressourcen, bringen aber nichts

3. **Nahrungskette**:
   - Farm produziert Getreide
   - Mühle verarbeitet Getreide zu Mehl
   - Mehl wird zu Essen für deine Population

4. **Langfristige Strategie**:
   - Baue Lagerhäuser zur Speicherung auf
   - Investiere in Spezialisierung (Minen für Metal)
   - Balanciere zwischen Wachstum und Ressourcen

## 📊 Beispiel-Spielverlauf

```
> build farm 3 3
✅ Bauernhof gebaut an (3, 3)

> hire farmer 1
✅ Bauer eingestellt (ID: 0)

> next
▶️  Turn 1 verarbeitet...
📊 Produktion:
  Bauernhof: 2 Getreide
✅ Population versorgt: 11/11 Essen

> build mill 4 3
✅ Mühle gebaut an (4, 3)

> hire miller 2
✅ Müller eingestellt (ID: 1)

> next
▶️  Turn 2 verarbeitet...
📊 Produktion:
  Bauernhof: 2 Getreide
  Mühle: 1 Mehl
✅ Population versorgt: 11/11 Essen
```

## 🔧 Technologie

- **Python 3.x**
- Datenklassen für Verwaltung
- Enums für Typsicherheit
- Text-basierte Benutzeroberfläche

## 📝 Lizenz

Frei verwendbar für Bildungszwecke
