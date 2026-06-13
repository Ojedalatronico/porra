# World Cup 2026 Betting Pool (Porra)

This project parses participant predictions from Excel files, fetches real results from an API, calculates points, and displays them in a web dashboard.

## Structure
- `src/parse.py`: Logic for parsing Excel files and fetching API data.
- `src/app.py`: Streamlit web application.
- `data/`: Folder containing Excel files and generated CSVs.

## How to use

1. **Install dependencies**:
   ```bash
   pip install openpyxl requests streamlit pandas
   ```

2. **Parse data**:
   Run the parser to update `resultados_porra.csv` based on the latest Excel files and API results.
   ```bash
   python main.py
   ```

3. **Automation**:
   This project is set to update automatically every hour via GitHub Actions. It will:
   - Synchronize matches with the live API.
   - Recalculate points for all participants.
   - Regenerate the `index.html` dashboard.

To deploy the dashboard, simply enable **GitHub Pages** in your repository settings and point it to the `index.html` in the root (main branch).
