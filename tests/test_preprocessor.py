import pandas as pd
import pytest
from data_analyzer import preprocessor as ppr
from pandas.testing import assert_frame_equal


def test_usun_woj_domyslny_prefix():
    """
    Sprawdza czy funkcja poprawnie usuwa domyślny prefix
    """

    dane_wejsciowe = pd.DataFrame({
        "Województwo": ["WOJ. MAZOWIECKIE", "WOJ. MAŁOPOLSKIE", "LUBELSKIE"],
        "wartość": [1, 2, 3]
    })
    oczekiwany_wynik = pd.DataFrame({
        "Województwo": ["MAZOWIECKIE", "MAŁOPOLSKIE", "LUBELSKIE"],
        "wartość": [1, 2, 3]
    })

    wynik_rzeczywisty = ppr.usun_woj(dane_wejsciowe)

    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)


def test_usun_woj_niestandardowy_prefix_i_kolumna():
    """
    Sprawdza czy funkcja działa poprawnie z niestandardową nazwą kolumny i prefixem.
    """
    dane_wejsciowe = pd.DataFrame({
        "Region": ["Region: Pomorze", "Region: Śląsk", "Mazowsze"]
    })
    oczekiwany_wynik = pd.DataFrame({
        "Region": [" Pomorze", " Śląsk", "Mazowsze"]
    })

    wynik_rzeczywisty = ppr.usun_woj(dane_wejsciowe, column="Region", prefix="Region:")

    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)

def test_usun_woj_nieistniejaca_kolumna():
    """
    Sprawdza czy funkcja zwraca oryginalny DataFrame bez zmian,
    jeśli podana kolumna nie istnieje.
    """

    dane_wejsciowe = pd.DataFrame({
        "Wojewuctwo": ["MAZOWIECKIE"],
    })
    oczekiwany_wynik = dane_wejsciowe.copy()
    wynik_rzeczywisty = ppr.usun_woj(dane_wejsciowe, column="Województwo")
    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)







def test_litery_na_male_standardowe_uzycie():
    dane_wejsciowe = pd.DataFrame({
        "Województwo": ["MAZOWIECKIE", "MaŁoPoLsKiE", "lubelskie", "ŚLĄSKIE"],
        "InnaKolumna": [1, 2, 3, 4]
    })
    oczekiwany_wynik = pd.DataFrame({
        "Województwo": ["mazowieckie", "małopolskie", "lubelskie", "śląskie"],
        "InnaKolumna": [1, 2, 3, 4]
    })

    wynik_rzeczywisty = ppr.litery_na_male(dane_wejsciowe)
    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)


def test_litery_na_male_niestandardowa_kolumna():
    """
    Sprawdza czy funkcja działa poprawnie z niestandardową nazwą kolumny.
    """
    # ARRANGE
    dane_wejsciowe = pd.DataFrame({
        "Nazwa Miasta": ["WARSZAWA", "Kraków", "gdańsk"]
    })
    oczekiwany_wynik = pd.DataFrame({
        "Nazwa Miasta": ["warszawa", "kraków", "gdańsk"]
    })

    wynik_rzeczywisty = ppr.litery_na_male(dane_wejsciowe, column="Nazwa Miasta")
    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)

def test_litery_na_male_nieistniejaca_kolumna():
    """
    Sprawdza czy funkcja zwraca oryginalny DataFrame bez zmian,
    jeśli podana kolumna nie istnieje.
    """

    dane_wejsciowe = pd.DataFrame({
        "Wojewuctwo": ["MAZOWIECKIE"],
    })
    oczekiwany_wynik = dane_wejsciowe.copy()
    wynik_rzeczywisty = ppr.litery_na_male(dane_wejsciowe, column="Województwo")
    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)












def test_usun_z_ostatnia_cyfra_usuwa_poprawne_wiersze():
    """
    Sprawdza czy funkcja poprawnie usuwa wiersze, których wartość w kolumnie
    kończy się na jedną z podanych cyfr.
    """
    # ARRANGE
    dane_testowe = {
        'TERYT': ['02144', '02145', '14298', '14299'],
        'Wartosc': [10, 20, 30, 40]
    }
    df_testowy = pd.DataFrame(dane_testowe)
    cyfry_do_usuniecia = ['4', '5', '9']
    wynikowy_df = ppr.usun_z_ostatnia_cyfra(df_testowy, column='TERYT', cyfry=cyfry_do_usuniecia)
    oczekiwane_teryt = ['14298']
    assert len(wynikowy_df) == 1
    assert wynikowy_df['TERYT'].iloc[0] == oczekiwane_teryt[0]


def test_usun_z_ostatnia_cyfra_radzi_sobie_z_rozne_typy_danych():
    """
    Sprawdza czy funkcja radzi sobie z kolumną zawierającą różne typy danych
    """
    dane_testowe = {
        'TERYT': ['02144', 123, None, 'abcde'],
        'Wartosc': [10, 50, 60, 70]
    }
    df_testowy = pd.DataFrame(dane_testowe)
    cyfry_do_usuniecia = ['3']

    wynikowy_df = ppr.usun_z_ostatnia_cyfra(df_testowy, column='TERYT', cyfry=cyfry_do_usuniecia)

    assert len(wynikowy_df) == 3


def test_usun_z_ostatnia_cyfra_gdy_pusta_lista_cyfr():
    """
    Sprawdza czy funkcja niczego nie usuwa, gdy lista cyfr do usunięcia jest pusta.
    """
    # ARRANGE
    dane_testowe = {
        'TERYT': ['02144', '02145'],
        'Wartosc': [10, 20]
    }
    df_testowy = pd.DataFrame(dane_testowe)
    oczekiwany_wynik = df_testowy.copy()
    cyfry_do_usuniecia = []
    wynikowy_df = ppr.usun_z_ostatnia_cyfra(df_testowy, column='TERYT', cyfry=cyfry_do_usuniecia)
    assert_frame_equal(wynikowy_df, oczekiwany_wynik)






def test_usun_ostatnia_cyfre_standardowe_dzialanie():
    """
    Sprawdza czy funkcja poprawnie dla standardowego wejścia
    """
    dane_wejsciowe = pd.DataFrame({
        'TERYT': ["12345", "0214", 987, "A"],
        'InnaKolumna': [1, 2, 3, 4]
    })
    oczekiwany_wynik = pd.DataFrame({
        'TERYT': ["1234", "021", "98", ""],
        'InnaKolumna': [1, 2, 3, 4]
    })
    wynik_rzeczywisty = ppr.usun_ostatnia_cyfre(dane_wejsciowe, column='TERYT')
    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)


def test_usun_ostatnia_cyfre_puste_wartosci_i_none():
    """
    Sprawdza jak funkcja zachowuje się dla pustych stringów i wartości None
    """
    # ARRANGE
    dane_wejsciowe = pd.DataFrame({
        'TERYT': ["", None],
    })
    oczekiwany_wynik = pd.DataFrame({
        'TERYT': ["", "Non"],
    })
    wynik_rzeczywisty = ppr.usun_ostatnia_cyfre(dane_wejsciowe, column='TERYT')
    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)







def test_str_to_int_konwertuje_poprawne_dane():
    """
    Sprawdza czy funkcja poprawnie konwertuje kolumnę zawierającą
    wyłącznie stringi reprezentujące liczby.
    """
    dane_wejsciowe = pd.DataFrame({
        'ID': ['123', '45', '9876'],
        'Inna': ['a', 'b', 'c']
    })

    wynik_rzeczywisty = ppr.str_to_int(dane_wejsciowe, column='ID')

    assert pd.api.types.is_numeric_dtype(wynik_rzeczywisty['ID'])
    assert pd.api.types.is_string_dtype(dane_wejsciowe['ID'])


def test_str_to_int_zwraca_oryginal_gdy_bledne_dane():
    """
    Sprawdza czy funkcja zwraca oryginalny DataFrame, gdy w kolumnie
    znajdują się wartości niemożliwe do skonwertowania na liczbę.
    """
    dane_wejsciowe = pd.DataFrame({
        'ID': ['123', 'aaa', '9876']
    })
    oczekiwany_wynik = dane_wejsciowe.copy()

    wynik_rzeczywisty = ppr.str_to_int(dane_wejsciowe, column='ID')
    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)


def test_str_to_int_pusty_dataframe():
    """
    Sprawdza jak funkcja zachowuje się dla pustego df
    """
    dane_wejsciowe = pd.DataFrame({'ID': []})
    oczekiwany_wynik = dane_wejsciowe.copy()

    wynik_rzeczywisty = ppr.str_to_int(dane_wejsciowe, column='ID')

    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)





def test_zmien_nazwe_poprawnie_zmienia_nazwe_kolumny():
    dane_wejsciowe = pd.DataFrame({
        'StaraNazwa': [1, 2, 3],
        'InnaKolumna': ['a', 'b', 'c']
    })
    wynik_rzeczywisty = ppr.zmien_nazwe(dane_wejsciowe, old_name='StaraNazwa', new_name='NowaNazwa')

    assert 'NowaNazwa' in wynik_rzeczywisty.columns
    assert 'StaraNazwa' not in wynik_rzeczywisty.columns


def test_zmien_nazwe_nieistniejaca_kolumna():
    """
    Sprawdza czy funkcja zwraca oryginalny DataFrame, gdy próbujemy
    zmienić nazwę kolumny, która nie istnieje.
    """
    dane_wejsciowe = pd.DataFrame({
        'AktualnaNazwa': [1, 2, 3]
    })
    oczekiwany_wynik = dane_wejsciowe.copy()

    wynik_rzeczywisty = ppr.zmien_nazwe(dane_wejsciowe, old_name='NieistniejacaNazwa', new_name='NowaNazwa')

    assert_frame_equal(wynik_rzeczywisty, oczekiwany_wynik)






def test_usun_puste_wiersze_usuwa_nan_i_none():
    """
    Sprawdza czy funkcja poprawnie usuwa wiersze z wartościami None
    """
    dane_wejsciowe = pd.DataFrame({
        'TERYT': ['0123', None, '5678'],
        'Inna': [1, 2, 3]
    })
    oczekiwany_wynik = pd.DataFrame({
        'TERYT': ['0123', '5678'],
        'Inna': [1, 3]
    })
    wynik_rzeczywisty = ppr.usun_puste_wiersze(dane_wejsciowe, nazwa_kolumny='TERYT')
    assert_frame_equal(oczekiwany_wynik, wynik_rzeczywisty.reset_index(drop=True))



def test_usun_puste_wiersze_usuwa_puste_stringi_i_spacje():
    """
    Sprawdza czy funkcja poprawnie usuwa wiersze zawierające
    puste stringi lub stringi składające się tylko z białych znaków
    """
    dane_wejsciowe = pd.DataFrame({
        'TERYT': ['0123', '', '   ', '5678'],
        'Inna': [1, 2, 3, 4]
    })

    oczekiwany_wynik = pd.DataFrame({
        'TERYT': ['0123', '5678'],
        'Inna': [1, 4]
    })
    wynik_rzeczywisty = ppr.usun_puste_wiersze(dane_wejsciowe, nazwa_kolumny='TERYT')
    assert_frame_equal(oczekiwany_wynik, wynik_rzeczywisty.reset_index(drop=True))






def test_usun_krotkie_domyslne_wartosci():
    """
    Sprawdza czy funkcja poprawnie usuwa wiersze w domyślnej kolumnie
    """
    dane_wejsciowe = pd.DataFrame({
        'TERYT': ['1234567', '123456', '12345', '12345678'],
        'Inna': [1, 2, 3, 4]
    })
    wynik_rzeczywisty = ppr.usun_krotkie(dane_wejsciowe)  # Używamy domyślnych argumentów

    assert len(wynik_rzeczywisty) == 2
    assert all(wynik_rzeczywisty['TERYT'].str.len() >= 7)


def test_usun_krotkie_niestandardowe_wartosci():
    """
    Sprawdza czy funkcja działa poprawnie z niestandardową kolumną i progiem długości.
    """
    dane_wejsciowe = pd.DataFrame({
        'KOD': ['ABC', 'A', 'ABCD', 'ABCDE'],
    })

    wynik_rzeczywisty = ppr.usun_krotkie(dane_wejsciowe, column='KOD', wartosc=4)

    assert len(wynik_rzeczywisty) == 2


def test_usun_krotkie_rozne_int():
    """
    Sprawdza czy funkcja radzi sobie z intami
    """
    dane_wejsciowe = pd.DataFrame({
        'TERYT': [123456, 1234567, 123]
    })

    wynik_rzeczywisty = ppr.usun_krotkie(dane_wejsciowe)

    assert len(wynik_rzeczywisty) == 1
    assert wynik_rzeczywisty['TERYT'].iloc[0] == 1234567





