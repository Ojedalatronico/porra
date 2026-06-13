import os
import csv
import json
import pandas as pd
from src.parse import parse_excel_files

def generate_static_data():
    """Generates the main index.html with all data embedded for the static site."""
    csv_path = os.path.join("data", "resultados_porra.csv")
    if not os.path.exists(csv_path):
        print("Error: CSV not found. Running parser first...")
        parse_excel_files("data", "resultados_porra.csv", "resultados_reales.csv")

    df = pd.read_csv(csv_path)
    # Replace NaN for JSON compatibility
    df = df.replace({pd.NA: None, float('nan'): None})
    
    # Pre-calculate data for the frontend
    # 1. Leaderboard
    leaderboard = df.groupby("Participante")["Puntos"].sum().reset_index()
    leaderboard = leaderboard.sort_values(by="Puntos", ascending=False).to_dict(orient="records")
    
    # 2. Results per user
    user_results = {}
    for user in df["Participante"].unique():
        user_results[user] = df[df["Participante"] == user].to_dict(orient="records")

    # 3. List of participants
    participants = sorted(df["Participante"].unique().tolist())

    data_json = {
        "leaderboard": leaderboard,
        "participants": participants,
        "user_results": user_results
    }

    # Generate full single HTML file (or separate if preferred, but single is easier/mobile friendly)
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>World Cup 2026 - Porra</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #1e40af;
            --primary-light: #3b82f6;
            --secondary: #be123c;
            --bg: #f8fafc;
            --card: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --accent: #f59e0b;
        }}

        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.5;
        }}

        header {{
            background: linear-gradient(135deg, var(--primary) 0%, #1e3a8a 100%);
            color: white;
            padding: 2rem 1rem;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }}

        .nav-container {{
            max-width: 600px;
            margin: 1.5rem auto 0;
            display: flex;
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 4px;
        }}

        .nav-btn {{
            flex: 1;
            border: none;
            background: none;
            color: white;
            padding: 0.75rem;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .nav-btn.active {{
            background: white;
            color: var(--primary);
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }}

        main {{
            max-width: 1000px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}

        .card {{
            background: var(--card);
            border-radius: 16px;
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        .section-title {{
            padding: 1.5rem;
            margin: 0;
            font-weight: 800;
            font-size: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid var(--border);
        }}

        .table-wrapper {{ overflow-x: auto; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}

        th {{
            background: #f1f5f9;
            padding: 1rem;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
        }}

        td {{ padding: 1.25rem 1rem; border-bottom: 1px solid var(--border); }}
        
        tr:last-child td {{ border-bottom: none; }}

        /* Leaderboard Specific */
        .rank-badge {{
            display: inline-flex;
            width: 32px;
            height: 32px;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-weight: bold;
            background: #f1f5f9;
        }}
        .rank-1 {{ background: #fef3c7; color: #92400e; }}
        .rank-2 {{ background: #f1f5f9; color: #475569; }}
        .rank-3 {{ background: #ffedd5; color: #9a3412; }}

        /* Selection Controls */
        .controls {{ padding: 1.5rem; background: #f8fafc; border-bottom: 1px solid var(--border); }}
        
        select {{
            width: 100%;
            padding: 0.75rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            font-size: 1rem;
            background-color: white;
            cursor: pointer;
        }}

        .summary-banner {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 1.5rem;
            background: #eff6ff;
            color: var(--primary);
            font-weight: 600;
        }}

        /* Match specific row styling */
        .match-row {{ display: flex; flex-direction: column; gap: 0.25rem; }}
        .team-name {{ font-weight: 600; }}
        .score-pill {{
            background: var(--primary);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
            margin: 0 4px;
        }}
        .points-tag {{
            background: #dcfce7;
            color: #166534;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 700;
        }}

        /* Mobile Adjustments */
        @media (max-width: 640px) {{
            header h1 {{ font-size: 1.5rem; }}
            td, th {{ padding: 0.75rem 0.5rem; font-size: 0.9rem; }}
            .desktop-only {{ display: none; }}
            .nav-container {{ margin: 1rem 1rem 0; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>World Cup 2026 Porra</h1>
        <div class="nav-container">
            <button id="btn-leaderboard" class="nav-btn active" onclick="showSection('leaderboard')">Clasificación</button>
            <button id="btn-individual" class="nav-btn" onclick="showSection('individual')">Mis Puntos</button>
        </div>
    </header>

    <main>
        <!-- Leaderboard -->
        <div id="section-leaderboard" class="card">
            <h2 class="section-title">📊 Clasificación General</h2>
            <div class="table-wrapper">
                <table id="leaderboard-table">
                    <thead>
                        <tr>
                            <th style="width: 60px">#</th>
                            <th>Participante</th>
                            <th style="text-align: right">Puntos</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>

        <!-- Individual -->
        <div id="section-individual" class="card" style="display: none;">
            <h2 class="section-title">👤 Resultados por Persona</h2>
            <div class="controls">
                <select id="user-selector" onchange="renderUser()"></select>
            </div>
            <div id="user-stats" class="summary-banner" style="display: none;">
                <span>Total de Puntos</span>
                <span id="total-pts-val">0</span>
            </div>
            <div class="table-wrapper">
                <table id="user-table">
                    <thead>
                        <tr>
                            <th>Partido</th>
                            <th class="desktop-only">Fase</th>
                            <th style="text-align: center">Puntos</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>
    </main>

    <script>
        const appData = {json.dumps(data_json)};

        function showSection(id) {{
            localStorage.setItem('activeSection', id);
            document.getElementById('section-leaderboard').style.display = id === 'leaderboard' ? 'block' : 'none';
            document.getElementById('section-individual').style.display = id === 'individual' ? 'block' : 'none';
            document.getElementById('btn-leaderboard').className = 'nav-btn' + (id === 'leaderboard' ? ' active' : '');
            document.getElementById('btn-individual').className = 'nav-btn' + (id === 'individual' ? ' active' : '');
            
            if(id === 'leaderboard') renderLeaderboard();
        }}

        function renderLeaderboard() {{
            const tbody = document.querySelector('#leaderboard-table tbody');
            tbody.innerHTML = appData.leaderboard.map((row, idx) => `
                <tr>
                    <td><span class="rank-badge rank-${{idx + 1}}">${{idx + 1}}</span></td>
                    <td style="font-weight: 600">${{row.Participante}}</td>
                    <td style="text-align: right; font-weight: 800; color: var(--primary)">${{row.Puntos}}</td>
                </tr>
            `).join('');
        }

        function initApp() {{
            const select = document.getElementById('user-selector');
            select.innerHTML = '<option value="">Selecciona un participante...</option>' + 
                appData.participants.map(p => `<option value="${{p}}">${{p}}</option>`).join('');
            
            // Restore selection and section from localStorage
            const savedSection = localStorage.getItem('activeSection') || 'leaderboard';
            showSection(savedSection);

            const savedUser = localStorage.getItem('selectedParticipant');
            if (savedUser && appData.participants.includes(savedUser)) {{
                select.value = savedUser;
                renderUser();
            }}
        }}

        function renderUser() {{
            const name = document.getElementById('user-selector').value;
            const container = document.getElementById('user-stats');
            const tbody = document.querySelector('#user-table tbody');
            
            // Save to localStorage
            if (name) {{
                localStorage.setItem('selectedParticipant', name);
            }} else {{
                localStorage.removeItem('selectedParticipant');
            }}

            if(!name) {{
                container.style.display = 'none';
                tbody.innerHTML = '';
                return;
            }}

            const results = appData.user_results[name];
            const total = results.reduce((acc, r) => acc + (r.Puntos || 0), 0);
            
            container.style.display = 'flex';
            document.getElementById('total-pts-val').textContent = total;

            tbody.innerHTML = results.map(r => `
                <tr>
                    <td>
                        <div class="match-row">
                            <span><span class="team-name">${{r.Equipo_Local}}</span> ${{r.Goles_Local ?? '-'}}</span>
                            <span><span class="team-name">${{r.Equipo_Visitante}}</span> ${{r.Goles_Visitante ?? '-'}}</span>
                        </div>
                    </td>
                    <td class="desktop-only" style="color: var(--text-muted); font-size: 0.85rem">${{r.Tipo}}</td>
                    <td style="text-align: center"><span class="points-tag">${{r.Puntos}}</span></td>
                </tr>
            `).join('');
        }}

        window.onload = initApp;
    </script>
</body>
</html>"""
    
    output_path = "index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"Website generated as {output_path}!")

if __name__ == "__main__":
    generate_static_data()
