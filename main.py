from src.parse import parse_excel_files
from src.generate_web import generate_static_data

def main():
    # 1. Parse data
    parse_excel_files("data", "resultados_porra.csv", "resultados_reales.csv")
    
    # 2. Generate web
    generate_static_data()


if __name__ == "__main__":
    main()
