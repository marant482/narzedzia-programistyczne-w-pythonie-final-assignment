import argparse
import logging
import pandas as pd
from data_analyzer import data_loader as dl
from data_analyzer import preprocessor as ppr
from data_analyzer import analysis as anal
from data_analyzer import reporter as rep

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', encoding='utf-8')

def main():
    """
    Funkcja łączy dane ze wskazanych plików, liczy podstawowe statystyki kolumn, testuje hipotezy o korelacji kolumn i
    zapisuje wyniki analizy do nowego pliku o podanej nazwie
    """
    parser = argparse.ArgumentParser(
        description="Skrypt do analizy danych publicznych dotyczących gmin."
    )
    parser.add_argument(
        '--pozary',
        required=True,
        help="Ścieżka do pliku z danymi o pożarach."
    )
    parser.add_argument(
        '--populacje',
        required=True,
        help="Ścieżka do pliku z danymi o populacji."
    )
    parser.add_argument(
        '--powierzchnie',
        required=True,
        help="Ścieżka do pliku z danymi o powierzchniach."
    )
    parser.add_argument(
        '--koncesje',
        required=True,
        help="Ścieżka do pliku z danymi o koncesjach na alkohol."
    )
    parser.add_argument(
        '--output',
        required=True,
        help="Ścieżka do pliku wyjściowego, w którym zostanie zapisany raport (np. raport.json). SKRYPT STWORZY LUB NADPISZE PLIK!"
    )
    args = parser.parse_args()

    path_pozary = args.pozary
    path_powierzchnie = args.powierzchnie
    path_populacja = args.populacje
    path_alkohol = args.koncesje

    try:
        logging.info("Rozpoczynam wczytywanie plików z danymi")
        pozary = dl.load_data(path_pozary)
        powierzchnie = dl.load_data(path_powierzchnie)
        populacja = dl.load_data(path_populacja)
        alkohol = dl.load_data(path_alkohol)

        if pozary is None or powierzchnie is None or populacja is None or alkohol is None:
            logging.error("Nie udało się wczytać jednego lub więcej plików. Przerwanie analizy.")
            return

        logging.info("Rozpoczynam preprocessing danych")

        logging.info("Rozpoczynam preprocessing datasetu z koncesjami")
        alkohol = alkohol.iloc[:, 3:6]
        alkohol_miejscowosc = alkohol["Miejscowość"].value_counts().reset_index()
        alkohol_miejscowosc.columns = ["Miejscowość", "Liczba koncesji"]
        alkohol_wojewodztwo = alkohol["Województwo"].value_counts().reset_index()
        alkohol_wojewodztwo.columns = ["Województwo", "Liczba koncesji"]
        alkohol_wojewodztwo = ppr.usun_woj(alkohol_wojewodztwo)
        alkohol_wojewodztwo = ppr.litery_na_male(alkohol_wojewodztwo)


        logging.info("Rozpoczynam preprocessing datasetu z populacjami")
        populacja = populacja.iloc[8:, :3]
        populacja.columns = ["Gmina", "TERYT", "Ludność"]
        populacja = ppr.usun_puste_wiersze(populacja)
        populacja = ppr.usun_rozdzielone_gminy_mw(populacja)
        populacja = ppr.usun_ostatnia_cyfre(populacja, "TERYT")
        populacja["Ludność"] = populacja["Ludność"].astype(int)
        populacja = ppr.str_to_int(populacja, "TERYT")


        logging.info("Rozpoczynam preprocessing datasetu z powierzchniami")
        powierzchnie = powierzchnie.iloc[:, :3]
        powierzchnie = ppr.usun_puste_wiersze(powierzchnie)
        powierzchnie = ppr.usun_odstepy(powierzchnie)
        powierzchnie = ppr.usun_krotkie(powierzchnie)
        powierzchnie = ppr.usun_rozdzielone_gminy_mw(powierzchnie)
        powierzchnie = ppr.usun_dzielnice_miast(powierzchnie)
        powierzchnie = ppr.usun_ostatnia_cyfre(powierzchnie, "TERYT")
        powierzchnie = ppr.zlacz_gminy(powierzchnie,"Kamienica", "Szczawa", "Powierzchnia [ha]", "Nazwa jednostki")
        powierzchnie = ppr.zlacz_gminy(powierzchnie, "Supraśl", "Grabówka", "Powierzchnia [ha]", "Nazwa jednostki")
        powierzchnie = ppr.str_to_int(powierzchnie, "TERYT")


        logging.info("Rozpoczynam preprocessing datasetu z pożarami")
        pozary = pozary.iloc[:, :5]
        pozary = ppr.zmien_nazwe(pozary, "RAZEM Pożar (P)", "Liczba Pożarów")
        pozary = ppr.usun_puste_wiersze(pozary)
        pozary = ppr.zlacz_dzielnice(pozary, "Liczba Pożarów")
        pozary = pozary.drop(348)
        pozary = pozary.drop(610)
        pozary = pozary.drop(1526)
        pozary = ppr.zlacz_gminy(pozary, 200209, 200216, "Liczba Pożarów", "TERYT")
        pozary = ppr.zlacz_gminy(pozary, 120705, 120713, "Liczba Pożarów", "TERYT")



        logging.info("Sprawdzam zgodność między zbiorami danych")
        ppr.sprawdz_zgodnosc(pozary, populacja, "TERYT")
        ppr.sprawdz_zgodnosc(powierzchnie, populacja, "TERYT")



        logging.info("Rozpoczynam łączenie zbiorów.")
        wszystkie_dane = pd.merge(pozary, powierzchnie[['TERYT', 'Powierzchnia [ha]']], on='TERYT', how='left')
        wszystkie_dane = pd.merge(wszystkie_dane, populacja[['TERYT', 'Ludność']], on='TERYT', how='left')
        wszystkie_dane = wszystkie_dane.drop(['TERYT', 'Powiat'], axis=1)
        wszystkie_dane_wojewodztwo = wszystkie_dane.groupby('Województwo').agg({
            'Liczba Pożarów': 'sum',
            'Powierzchnia [ha]': 'sum',
            'Ludność': 'sum'
        }).reset_index()
        wszystkie_dane_miejscowosc = wszystkie_dane[wszystkie_dane["Gmina"].isin(alkohol_miejscowosc["Miejscowość"])]
        wszystkie_dane_miejscowosc = wszystkie_dane_miejscowosc.groupby('Gmina').agg({
            'Liczba Pożarów': 'sum',
            'Powierzchnia [ha]': 'sum',
            'Ludność': 'sum'
        }).reset_index()
        wszystkie_dane_wojewodztwo = pd.merge(wszystkie_dane_wojewodztwo, alkohol_wojewodztwo, on="Województwo")
        wszystkie_dane_miejscowosc.rename(columns={"Gmina": "Miejscowość"}, inplace=True)
        wszystkie_dane_miejscowosc = pd.merge(wszystkie_dane_miejscowosc, alkohol_miejscowosc, on="Miejscowość")



        logging.info("Rozpoczynam analizę zbiorów.")

        stat_wszystkie_gminy = anal.oblicz_statystyki(wszystkie_dane, ["Liczba Pożarów", "Powierzchnia [ha]", "Ludność"])

        stat_miejsc_z_koncesja = anal.oblicz_statystyki(wszystkie_dane_miejscowosc,
                                       ["Liczba Pożarów", "Powierzchnia [ha]", "Ludność", "Liczba koncesji"])

        stat_woj = anal.oblicz_statystyki(wszystkie_dane_wojewodztwo,
                                        ["Liczba Pożarów", "Powierzchnia [ha]", "Ludność", "Liczba koncesji"])

        statystyki={
            "statystyki wszystkich gmin": stat_wszystkie_gminy,
            "statystyki gmin, w których istnieje firma z koncesją": stat_miejsc_z_koncesja,
            "statystyki województw": stat_woj,
        }

        logging.info("Rozpoczynam analizę testowanie hipotez.")
        logging.info("Hipotezy o danych na poziomie wszystkich gmin w Polsce:")
        test_gmin_lud_poz = anal.testuj_korelacje(wszystkie_dane, "Ludność", "Liczba Pożarów")
        test_gmin_pow_poz = anal.testuj_korelacje(wszystkie_dane, "Powierzchnia [ha]", "Liczba Pożarów")

        logging.info("Hipotezy o danych ze wszystkich miejscowości, w których zarejestrowana jest conajmniej jedna firma z koncesją:")
        test_miejsc_lud_konc = anal.testuj_korelacje(wszystkie_dane_miejscowosc, "Ludność", "Liczba koncesji")
        test_miejsc_poz_konc = anal.testuj_korelacje(wszystkie_dane_miejscowosc, "Liczba Pożarów", "Liczba koncesji")
        test_miejsc_pow_konc = anal.testuj_korelacje(wszystkie_dane_miejscowosc, "Powierzchnia [ha]", "Liczba koncesji")

        logging.info("Hipotezy o danych na poziomie województw:")
        test_woj_lud_poz = anal.testuj_korelacje(wszystkie_dane_wojewodztwo, "Ludność", "Liczba Pożarów")
        test_woj_pow_poz = anal.testuj_korelacje(wszystkie_dane_wojewodztwo, "Powierzchnia [ha]", "Liczba Pożarów")
        test_woj_lud_konc = anal.testuj_korelacje(wszystkie_dane_wojewodztwo, "Ludność", "Liczba koncesji")
        test_woj_poz_konc = anal.testuj_korelacje(wszystkie_dane_wojewodztwo, "Liczba Pożarów", "Liczba koncesji")
        test_woj_pow_konc = anal.testuj_korelacje(wszystkie_dane_wojewodztwo, "Powierzchnia [ha]", "Liczba koncesji")

        testy_gmina={
            "Test korelacji między liczbą ludności, a liczbą pożarów": test_gmin_lud_poz,
            "Test korelacji między powierzchnią gminy, a liczbą pożarów": test_gmin_pow_poz
        }

        testy_miejsc={
            "Test korelacji między liczbą ludności, a liczbą koncesji": test_miejsc_lud_konc,
            "Test korelacji między liczbą pożarów, a liczbą koncesji": test_miejsc_poz_konc,
            "Test korelacji między powierzchnią, a liczbą koncesji": test_miejsc_pow_konc
        }

        testy_woj={
            "Test korelacji między liczbą ludności, a liczbą pożarów": test_woj_lud_poz,
            "Test korelacji między powierzchnią gminy, a liczbą pożarów": test_woj_pow_poz,
            "Test korelacji między liczbą ludności, a liczbą koncesji": test_woj_lud_konc,
            "Test korelacji między liczbą pożarów, a liczbą koncesji": test_woj_poz_konc,
            "Test korelacji między powierzchnią, a liczbą koncesji": test_woj_pow_konc
        }

        testy={
            "dane na poziomie gmin":testy_gmina,
            "dane z miejscowości, w których jest conajmniej jedna koncesja":testy_miejsc,
            "dane na poziomie województw":testy_woj
        }

        wyniki_analizy={
            "statystyki":statystyki,
            "testy":testy
        }

        rep.generuj_raport(wyniki_analizy, args.output)

    except Exception as e:
        logging.error(f"Wystąpił nieoczekiwany, krytyczny błąd podczas analizy: {e}")


if __name__ == '__main__':
    main()