import platform
import psutil
import json
import speedtest
from flask import Flask, jsonify

app = Flask(__name__)

def get_system_info():
    """Retorna as especificações do sistema."""
    system_info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": psutil.cpu_count(logical=True),
        "memory": round(psutil.virtual_memory().total / (1024 ** 3), 2),  # Convert to GB
    }
    return system_info

def get_internet_speed():
    """Retorna a velocidade de download e upload usando speedtest-cli."""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1e6  # Convert to Mbps
        upload_speed = st.upload() / 1e6  # Convert to Mbps
        return {
            "download_speed_mbps": round(download_speed, 2),
            "upload_speed_mbps": round(upload_speed, 2)
        }
    except Exception as e:
        return {"error": f"Erro ao testar velocidade de internet: {str(e)}"}

@app.route('/')
def index():
    """Endpoint principal que retorna informações do sistema e internet."""
    system_info = get_system_info()
    internet_speed = get_internet_speed()
    
    data = {
        "system_info": system_info,
        "internet_speed": internet_speed,
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)

