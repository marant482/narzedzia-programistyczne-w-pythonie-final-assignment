import json
import logging
from typing import Dict, Any


def generuj_raport(wszystkie_dane_do_raportu: Dict[str, Any], output_path: str) -> bool:
    """
    Zapisuje wyniki analizy do pliku w formacie JSON.

    Funkcja tworzy jeden główny obiekt JSON, który zawiera wszystkie
    przekazane wyniki.

    Args:
        wszystkie_dane_do_raportu (Dict[str, Any]): Słownik zawierający wyniki analizy
                                           do zapisania w raporcie.
        output_path (str): Ścieżka do pliku wyjściowego, w którym
                           zostanie zapisany raport.

    Returns:
        bool: True, jeśli raport został zapisany pomyślnie, False w przeciwnym razie.
    """
    logging.info(f"Rozpoczynam generowanie raportu do pliku: {output_path}")

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(wszystkie_dane_do_raportu, f, ensure_ascii=False, indent=4)
            #bez drugiego argumentu problem z polskimi znakami, ostatni argument poprawia czytelność
        logging.info(f"Raport pomyślnie zapisano w: {output_path}")
        return True

    except (IOError, TypeError) as e:
        logging.error(f"Wystąpił błąd podczas zapisywania raportu do pliku {output_path}: {e}")
        return False