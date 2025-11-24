import configparser
import json
from flask import Flask, jsonify
import os

app = Flask(__name__)

CONFIG_FILE = "config.ini"
DB_FILE = "database.json"


def parse_config():
    """Read and parse the configuration file, return dictionary."""
    config = configparser.ConfigParser()


    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file '{CONFIG_FILE}' not found.")

    try:
        config.read(CONFIG_FILE)
        result = {}

    
        for section in config.sections():
            result[section] = {}
            for key, value in config.items(section):
                result[section][key] = value

        return result

    except Exception as e:
        raise Exception(f"Error reading config file: {e}")


def save_to_db(data):
    """Save parsed configuration as JSON."""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise Exception(f"Error writing to database.json: {e}")


@app.route("/config", methods=["GET"])
def get_config():
    """GET API to fetch stored JSON configuration."""
    if not os.path.exists(DB_FILE):
        return jsonify({"error": "database.json not found"}), 404

    with open(DB_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == "__main__":
    print("Reading and parsing configuration file...")

    try:
        data = parse_config()
        save_to_db(data)
        print("Configuration File Parser Results:")
        print(json.dumps(data, indent=4))
        print("\nData saved successfully to database.json")

    except Exception as error:
        print(f"Error: {error}")

    print("Starting Flask server on http://127.0.0.1:5000/config")
    app.run(debug=True)
