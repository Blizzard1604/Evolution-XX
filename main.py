"""
🏰 EVOLUTION-XX - Siedler Simulation

ZWEI SPIELMODI:

1. 🖥️  WEB-GUI (empfohlen):
   $ python app.py
   Dann öffne: http://localhost:5000
   
   Moderne, interaktive Benutzeroberfläche mit:
   - Visuelle Karte mit Gebäuden
   - Ressourcen-Management
   - Arbeiter-Verwaltung
   - Einfache Click-Bedienung

2. 💻 TERMINAL-MODE:
   $ python main_cli.py
   
   Text-basierte Bedienung mit Befehlen

Für die Web-GUI starten:
"""

import sys

if __name__ == "__main__":
    print(__doc__)
    print("Starting web server...")
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)
