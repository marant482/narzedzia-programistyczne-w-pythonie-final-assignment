import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def load_data(file_path: str, **kwargs) -> pd.DataFrame | None:
    """
    Wczytuje dane z pliku CSV, XLS lub XLSX
    Funkcja wymaga Pythona w wersji 3.10 lub nowszej, ze względu na formułę ***|None

    Args:
        file_path (str): Ścieżka do pliku
        **kwargs: Dodatkowe argumenty dla funkcji wczytujących z pandas

    Returns:
        DataFrame z danymi lub None, jeśli wystąpił błąd
    """

    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path, **kwargs)
            logging.info("Wczytanie pliku CSV zakończone pomyślnie.")
            return df

        elif file_path.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path, **kwargs)
            logging.info("Wczytanie pliku Excel zakończone pomyślnie.")
            return df

        else:
            raise ValueError(f"Nieobsługiwany format pliku, dostępne formaty to CSV, XLS, oraz XLSX")

    except FileNotFoundError:
        logging.error(f"Plik nie został znaleziony pod ścieżką: {file_path}")
        return None

    except Exception as e:
        logging.error(f"Wystąpił błąd podczas przetwarzania pliku {file_path}: {e}")
        return None


if __name__ == '__main__':
    plik_csv = 'data/alkohol.csv'
    plik_xls = 'data/populacja.xls'
    plik_xlsx = 'data/powierzchnie.xlsx'

    print("Test wczytywania CSV")
    df_csv = load_data(plik_csv)
    if df_csv is not None:
        print(df_csv.head())

    print("\nTest wczytywania xls")
    df_xls = load_data(plik_xls)
    if df_xls is not None:
        print(df_xls.head())

    print("\nTest wczytywania xlsx")
    df_xlsx = load_data(plik_xlsx)
    if df_xlsx is not None:
        print(df_xlsx.head())

    print("\nTest nieistniejącego pliku")
    load_data("brakpliku.csv")