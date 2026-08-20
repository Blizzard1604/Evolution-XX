from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from game_engine import Game
import json

app = Flask(__name__)
CORS(app)

# Global game instance
game = None

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/game/init', methods=['POST'])
def init_game():
    """Initialize a new game"""
    global game
    game = Game()
    return jsonify(game.get_state())

@app.route('/api/game/state', methods=['GET'])
def get_state():
    """Get current game state"""
    if game is None:
        return jsonify({"error": "Game not initialized"}), 400
    return jsonify(game.get_state())

# ==================== Navigation ====================

@app.route('/api/map/goto_world', methods=['POST'])
def goto_world():
    """Go to world map"""
    if game is None:
        return jsonify({"error": "Game not initialized"}), 400
    
    result = game.goto_world()
    return jsonify(result)

@app.route('/api/map/goto_region', methods=['POST'])
def goto_region():
    """Go to a region"""
    if game is None:
        return jsonify({"error": "Game not initialized"}), 400
    
    data = request.json
    region_id = data.get('region_id')
    
    result = game.goto_region(region_id)
    return jsonify(result)

@app.route('/api/map/goto_gebiet', methods=['POST'])
def goto_gebiet():
    """Go to a gebiet"""
    if game is None:
        return jsonify({"error": "Game not initialized"}), 400
    
    data = request.json
    gebiet_id = data.get('gebiet_id')
    
    result = game.goto_gebiet(gebiet_id)
    return jsonify(result)

# ==================== Building Management ====================

@app.route('/api/building/build', methods=['POST'])
def build_building():
    """Build a new building"""
    if game is None:
        return jsonify({"error": "Game not initialized"}), 400
    
    data = request.json
    building_type = data.get('type')
    x = data.get('x')
    y = data.get('y')
    
    success, message = game.add_building(building_type, x, y)
    return jsonify({
        "success": success,
        "message": message,
        "state": game.get_state()
    })

@app.route('/api/worker/hire', methods=['POST'])
def hire_worker():
    """Hire a new worker"""
    if game is None:
        return jsonify({"error": "Game not initialized"}), 400
    
    data = request.json
    worker_type = data.get('type')
    gebiet_id = data.get('gebiet_id')
    
    success, message = game.hire_worker(worker_type, gebiet_id)
    return jsonify({
        "success": success,
        "message": message,
        "state": game.get_state()
    })

@app.route('/api/game/next', methods=['POST'])
def next_turn():
    """Process next turn"""
    if game is None:
        return jsonify({"error": "Game not initialized"}), 400
    
    result = game.next_turn()
    return jsonify({
        "turn_result": result,
        "state": game.get_state()
    })

@app.route('/api/resources/costs', methods=['GET'])
def get_building_costs():
    """Get building costs"""
    building_type = request.args.get('type')
    
    if not building_type:
        all_costs = {}
        for btype in ["WAREHOUSE", "LUMBERMILL", "MILL", "FARM", "MINE", "QUARRY", "BARRACKS", "BLACKSMITH"]:
            all_costs[btype] = Game.get_building_costs(btype)
        return jsonify(all_costs)
    
    costs = Game.get_building_costs(building_type)
    return jsonify(costs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
