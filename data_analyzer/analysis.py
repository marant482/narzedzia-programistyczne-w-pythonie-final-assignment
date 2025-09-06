import pandas as pd
import logging
from typing import Dict, Any, List
from scipy.stats import pearsonr

def oblicz_statystyki(df: pd.DataFrame, columns: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Oblicza i zwraca podstawowe statystyki (min, max, średnia, mediana)
    dla wskazanych kolumn w DataFrame.

    Args:
        df (pd.DataFrame): DataFrame do analizy.
        columns (List[str]): Lista nazw kolumn do obliczenia statystyk.

    Returns:
        Dict[str, Dict[str, Any]]: Słownik, gdzie kluczem jest nazwa kolumny,
                                   a wartością słownik ze statystykami.
    """
    stats = {}
    logging.info("Rozpoczynam obliczanie podstawowych statystyk.")
    for col in columns:
        if col in df.columns:
            # Upewniamy się, że kolumna jest numeryczna przed obliczeniami
            if pd.api.types.is_numeric_dtype(df[col]):
                stats[col] = {
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'średnia': df[col].mean(),
                    'mediana': df[col].median(),
                    'odchylenie_standardowe': df[col].std()
                }
                logging.info(f"Obliczono statystyki dla kolumny: '{col}'.")
            else:
                logging.warning(f"Kolumna '{col}' nie jest typu numerycznego i zostanie pominięta w statystykach.")
        else:
            logging.warning(f"Kolumna '{col}' nie została znaleziona w DataFrame i zostanie pominięta.")
    return stats


def testuj_korelacje(df: pd.DataFrame, col1: str, col2: str, poziom_istotnosci: float = 0.05) -> Dict[str, Any]:
    """
    Przeprowadza test hipotezy o korelacji Pearsona między dwiema kolumnami.

    Args:
        df (pd.DataFrame): DataFrame zawierający dane.
        col1 (str): Nazwa pierwszej kolumny.
        col2 (str): Nazwa drugiej kolumny.

    Returns:
        Dict[str, Any]: Słownik zawierający wyniki testu hipotezy (nazwy kolumn, współczynnik korelacji, p-value oraz indykator czy p-value mniejsze od 5%).
    """
    logging.info(f"Hipoteza zerowa: Nie ma liniowej zależności między '{col1}', a '{col2}'.")
    logging.info(f"Hipoteza alternatywna: Istnieje liniowa zależność między '{col1}', a '{col2}'.")

    # Aby test statystyczny zadziałał poprawnie, upewniamy się, że nie ma nigdzie pustych wierszy
    clean_df = df[[col1, col2]].dropna()

    if len(clean_df) < 3:  # Test korelacji wymaga co najmniej 3 par danych
        logging.warning(
            f"Niewystarczająca liczba danych ({len(clean_df)}) do testu korelacji między '{col1}' i '{col2}'.")
        return {
            'kolumna_1': col1,
            'kolumna_2': col2,
            'wspolczynnik_korelacji': None,
            'p_value': None,
            'uwagi': 'Niewystarczająca liczba danych do przeprowadzenia testu.'
        }

    try:
        correlation, p_value = pearsonr(clean_df[col1], clean_df[col2])
        if p_value < poziom_istotnosci:
            logging.info(f"Wykryto istotną statystycznie korelację między '{col1}', a '{col2}'. Odrzucamy hipotezę zerową, na rzecz hipotezy alternatywnej.")
        else:
            logging.info(f"Nie ma podstaw do odrzucenia hipotezy zerowej. Brak istotnej statystycznie korelacji między  '{col1}', a '{col2}'.")

        return {
            'kolumna_1': col1,
            'kolumna_2': col2,
            'wspolczynnik_korelacji': correlation,
            'p_value': p_value,
            'istotnosc_statystyczna': p_value < poziom_istotnosci
        }
    except Exception as e:
        logging.error(f"Wystąpił błąd podczas testu korelacji między '{col1}' i '{col2}': {e}")
        return {
            'kolumna_1': col1,
            'kolumna_2': col2,
            'wspolczynnik_korelacji': None,
            'p_value': None,
            'uwagi': f'Błąd podczas obliczeń: {e}'
        }

