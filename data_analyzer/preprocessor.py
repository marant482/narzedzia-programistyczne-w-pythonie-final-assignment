import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', encoding='utf-8')



def usun_woj(df: pd.DataFrame, column: str = "Województwo", prefix: str = "WOJ. ") -> pd.DataFrame:
    """
        Usuwa "Woj. " z nazwy Województwa w kolumnie, lub inny podany prefix
    """

    if column not in df.columns:
        logging.warning(f"Kolumna '{column}' nie istnieje w DataFrame. Pomijam krok.")
        return df

    df_copy = df.copy()
    df_copy[column] = df_copy[column].str.removeprefix(prefix)
    logging.info(f"Usunięto prefiks '{prefix}' z kolumny '{column}'.")
    return df_copy


def litery_na_male(df: pd.DataFrame, column: str = "Województwo") -> pd.DataFrame:
    """
        Zmienia litery w kolumnie na małe
    """
    if column not in df.columns:
        logging.warning(f"Kolumna '{column}' nie istnieje w DataFrame.")
        return df

    df_copy = df.copy()
    df_copy[column] = df_copy[column].str.lower()
    logging.info(f"Zmieniono litery na małe w kolumnie '{column}'.")
    return df_copy



def usun_z_ostatnia_cyfra(df: pd.DataFrame, column: str, cyfry: list[str]) -> pd.DataFrame:
    """
        Usuwa wiersze, w których wartość w podanej kolumnie (jako string) kończy się na jedną z podanych cyfr.
    """
    df_copy = df.copy()
    df_copy[column] = df_copy[column].astype(str) #powinny być stringi, ale lepiej się ubezpieczyć
    maska = df_copy[column].str.endswith(tuple(cyfry), na=False) #na=False jest na wszelki wypadek, żeby maska na pewno działała
    df_cleaned = df_copy[~maska]

    logging.info(
        f"Usunięto {len(df_copy) - len(df_cleaned)} wierszy z kolumny '{column}' kończących się na {cyfry}.")
    return df_cleaned




def usun_ostatnia_cyfre(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
        Usuwa ostatni znak z wartości w podanej kolumnie (traktując je jako string).
    """
    if column not in df.columns:
        logging.warning(f"Kolumna '{column}' nie istnieje w DataFrame. Zwracam oryginalny dataframe.")
        return df

    df_copy = df.copy()
    df_copy[column] = df_copy[column].astype(str).str[:-1]
    logging.info(f"Usunięto ostatnią cyfrę w kolumnie '{column}'.")
    return df_copy



def str_to_int(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    zamienia string na int w całej kolumnie
    """
    if column not in df.columns:
        logging.warning(f"Kolumna '{column}' nie istnieje w DataFrame. Zwracam oryginalny dataframe.")
        return df

    df_copy = df.copy()

    df_copy[column] = pd.to_numeric(df_copy[column], errors='coerce') # errors='coerce' zamieni niepoprawne wartości na NaN

    if df_copy[column].isna().any():
        logging.warning(f"Kolumna '{column}' zawiera wartości, których nie da się zamienić na integer. Zwracam oryginalny dataframe.")
        return df
    else:
        return df_copy




def znajdz_duplikaty(df: pd.DataFrame, column: str):
    """
    pokazuje liczbę duplikatów (nieunikalnych wartości) w danej kolumnie i wypisuje te wiersze
    (nic nie zwraca, jedynie wyświetla informacje)
    """
    if column not in df.columns:
        logging.warning(f"Kolumna '{column}' nie istnieje w DataFrame.")
        return

    duplicates = df[df.duplicated(subset=[column], keep=False)]
    if not duplicates.empty:
        logging.warning(
            f"Znaleziono {len(duplicates)} wierszy z {duplicates[column].nunique()} zduplikowanymi wartościami w kolumnie '{column}':")
        print(duplicates.sort_values(by=column))
    else:
        logging.info(f"Brak zduplikowanych wartości w kolumnie '{column}'.")



def zmien_nazwe(df: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
    """
    Zmienia nazwę kolumny
    """
    if old_name not in df.columns:
        logging.warning(f"Kolumna '{old_name}' nie istnieje w DataFrame.")
        return df

    df_copy = df.copy()
    df_copy.rename(columns={old_name: new_name}, inplace=True)
    logging.info(f"Zmieniono nazwę kolumny '{old_name}' na '{new_name}'.")
    return df_copy

def usun_puste_wiersze(df: pd.DataFrame, nazwa_kolumny: str="TERYT") -> pd.DataFrame:
    """
    usuwa puste wiersze z kolumny o wskazanej nazwie (domyślnie TERYT)
    """
    if nazwa_kolumny not in df.columns:
        logging.warning(f"Kolumna '{nazwa_kolumny}' nie istnieje w DataFrame.")
        return df
    df_copy = df.copy()
    # w niektórych datasetach, zamiast pustych wartości Nan, mieliśmy puste stringi (lub same białe znaki)
    #zamienimy je na Nan, żeby się ich pozbyć
    df_copy[nazwa_kolumny] = df_copy[nazwa_kolumny].replace(r'^\s*$', pd.NA, regex=True)
    # ^ to początek, \s to biały znak *to dowolna ilość, $ to koniec
    df_filtr=df_copy.dropna(subset=[nazwa_kolumny])
    logging.info(f"usunięto {len(df_copy)-len(df_filtr)} pustych wierszy.")
    return df_filtr




def usun_krotkie(df: pd.DataFrame, column: str="TERYT", wartosc: int=7) -> pd.DataFrame:
    """
    usuwa wszystkie wiersze, które w danej kolumnie zawierają napis krótszy niż wskazna wartość
    """
    if column not in df.columns:
        logging.warning(f"Kolumna '{column}' nie istnieje w DataFrame.")
        return df

    df_copy=df.copy()
    oryginalna_liczba_wierszy = len(df_copy)

    maska = df_copy[column].astype(str).str.len() >= wartosc
    df_przefiltrowany=df_copy[maska]

    nowa_liczba_wierszy = len(df_przefiltrowany)
    liczba_usunietych = oryginalna_liczba_wierszy - nowa_liczba_wierszy

    logging.info(f"W kolumnie '{column}' usunięto {liczba_usunietych} wierszy.")

    return df_przefiltrowany



def usun_odstepy(df: pd.DataFrame, column: str="TERYT") -> pd.DataFrame:
    """
    Funkcja usuwa spacje i tabulacje w całej kolumnie

    """
    if column not in df.columns:
        logging.warning(f"Kolumna '{column}' nie istnieje w DataFrame.")
        return df

    df_copy = df.copy()
    df_copy[column] = df_copy[column].str.replace(' ', '')
    logging.info(f"Usunięto odstępy z kolumny '{column}'.")
    return df_copy


def sprawdz_zgodnosc(df1: pd.DataFrame, df2: pd.DataFrame, key_column: str):
    """
    sprawdza ile jest wspólnych kodów, wyświetla te wiersze z obu tabel, których kody nie mają pary
    zakłada, że nazwy kolumn, których zgodność sprawdzamy są takie same
    """
    if key_column not in df1.columns or key_column not in df2.columns:
        logging.error(f"Kolumna klucza '{key_column}' nie istnieje w conajmniej jednym z DataFrame'ów. Przerywam sprawdzanie.")
        return

    keys1 = df1[key_column].unique()
    keys2 = df2[key_column].unique()

    unmatched_rows_in_df1 = df1[~df1[key_column].isin(keys2)]
    unmatched_rows_in_df2 = df2[~df2[key_column].isin(keys1)]

    if not unmatched_rows_in_df1.empty:
        logging.warning(
            f"Znaleziono {len(unmatched_rows_in_df1)} wierszy w pierwszym DataFrame, które nie mają odpowiednika w drugim:")
        print(unmatched_rows_in_df1.to_string())
    else:
        logging.info("Wszystkie wiersze z pierwszego DataFrame mają odpowiedniki w drugim.")

    if not unmatched_rows_in_df2.empty:
        logging.warning(
            f"Znaleziono {len(unmatched_rows_in_df2)} wierszy w drugim DataFrame, które nie mają odpowiednika w pierwszym:")
        print(unmatched_rows_in_df2.to_string())
    else:
        logging.info("Wszystkie wiersze z drugiego DataFrame mają odpowiedniki w pierwszym.")

    if unmatched_rows_in_df1.empty and unmatched_rows_in_df2.empty:
        logging.info(f"Pełna spójność kluczy w kolumnie '{key_column}' między oboma DataFrame'ami.")



def zlacz_dzielnice(df: pd.DataFrame, sum_col: str, gmina_col: str="Gmina", powiat_col: str="Powiat") -> pd.DataFrame:
    """
    Niektóre zbiory danych mają rozdzielone duże miasta na dzielnice, możemy znaleźć je w taki sposób, że tam, gdzie Powiat jest taki sam jak Gmina,
    to na pewno mamy do czynienia z dużym miastem na prawach powiatu, ponieważ mniejsze miasta, jeśli mają nazwę powiatu pochodzącą od miasta,
    to jest ona odmieniona, na przykład gmina Bełchatów jest w powiecie Bełchatowskim, ale gmina Warszawa jest w powiecie Warszawa.
    W związku z tym łatwo możemy sprawdzić, które z tych znalezionych miast się powtarzają i to będą właśnie dzielnice tego miasta.
    Funkcja zatem agreguje dane dla miast na prawach powiatu, które są rozbite na dzielnice, grupuje po podanych kolumnach (np. Gmina, Powiat),
    sumuje wartości w `sum_col` i zachowuje pierwszy kod terytorialny z grupy.
    """

    klucze_grupowania = [gmina_col, powiat_col]

    maska = (df[gmina_col] == df[powiat_col]) & \
                           df.duplicated(subset=klucze_grupowania, keep=False)

    dzielnice = df[maska]

    if dzielnice.empty:
        logging.info("Nie znaleziono dzielnic do zagregowania.")
        return df

    logging.info(f"Znaleziono {len(dzielnice)} wierszy reprezentujących dzielnice.")

    # Chcemy przekopiować wszystkie inne kolumny (biorąc pierwszą wartość) i zsumować jedną.
    inne_kolumny = [col for col in df.columns if col not in klucze_grupowania and col != sum_col]

    agg_dict = {}
    for kolumna in inne_kolumny:
        agg_dict[kolumna] = (kolumna, 'first')

    agg_dict[sum_col] = (sum_col, 'sum')

    zagregowane_miasta = dzielnice.groupby(klucze_grupowania).agg(**agg_dict).reset_index()

    indeksy_do_usuniecia = dzielnice.index #usuwamy wszystkie znalezione wcześniej dzielnice, żeby zaraz dołączyć już zagregowane
    df_bez_dzielnic = df.drop(indeksy_do_usuniecia)
    df_finalny = pd.concat([df_bez_dzielnic, zagregowane_miasta], ignore_index=True)
    df_finalny = df_finalny.reset_index(drop=True)
    logging.info(f"Zakończono agregację. Usunięto: {len(df)-len(df_finalny)} wierszy.")
    return df_finalny

def zlacz_gminy(df: pd.DataFrame, gmina_docelowa, gmina_do_wlaczenia, kolumna_wartosci: str, kolumna_nazw: str) -> pd.DataFrame:
    """
    Funkckcja łączy dwa wiersze w jeden, sumując wybrany wiersz i pozostawiając resztę taką jak w pierwszym wierszu.
    Często mamy sytuacje, w ktorej jakas gmina odlacza się od starej i jest to uwzględnione w jednym zbiorze danych
    ,ale w reszcie danych jeszcze tego nie uwzgledniono. Ta funkcja pozwala ręcznie dostosować ten zbiór, aby pasował do reszty.
    """
    df_kopia = df.copy()

    wiersz_gminy_docelowej = df_kopia[df_kopia[kolumna_nazw] == gmina_docelowa]
    wiersz_gminy_do_wlaczenia = df_kopia[df_kopia[kolumna_nazw] == gmina_do_wlaczenia]

    if wiersz_gminy_docelowej.empty or wiersz_gminy_do_wlaczenia.empty:
        logging.warning(
            f"Nie znaleziono jednej z gmin: '{gmina_docelowa}' lub '{gmina_do_wlaczenia}'. ")
        return df

    wartosc_do_dodania = wiersz_gminy_do_wlaczenia[kolumna_wartosci].iloc[0]
    indeks_gminy_docelowej = wiersz_gminy_docelowej.index[0]
    df_kopia.loc[indeks_gminy_docelowej, kolumna_wartosci] += wartosc_do_dodania
    indeks_gminy_do_wlaczenia = wiersz_gminy_do_wlaczenia.index[0]
    df_kopia.drop(indeks_gminy_do_wlaczenia, inplace=True)

    logging.info(
        f"Połączono gminę '{gmina_do_wlaczenia}' z '{gmina_docelowa}'. "
        f"Dodano wartość {wartosc_do_dodania} do kolumny '{kolumna_wartosci}'."
    )

    return df_kopia


def usun_dzielnice_miast(df: pd.DataFrame,teryt_col: str="TERYT") -> pd.DataFrame:
    """
    W 7 cyfrowych kodach terytorialnych, ostatnia cyfra równająca się 8 lub 9 oznacza dzielnice miast (których dane są również zagregowane w całej gminie)
    Funkcja pozwala je łatwo usunąć.

    """
    if teryt_col not in df.columns:
        logging.warning(f"Kolumna '{teryt_col}' nie istnieje.")
        return df

    if df.empty:
        logging.info("DataFrame jest pusty.")
        return df

    teryt_pierwszego_wiersza = str(df[teryt_col].iloc[0])

    warunek1 = teryt_pierwszego_wiersza.startswith("0") and len(teryt_pierwszego_wiersza) == 7
    warunek2 = (not teryt_pierwszego_wiersza.startswith("0")) and len(teryt_pierwszego_wiersza) == 6 #jeżeli kody były zamienione na inta, to znika pierwsza cyfra

    if warunek1 or warunek2:
        df_przetworzony = usun_z_ostatnia_cyfra(df, column=teryt_col, cyfry=['8', '9'])
        return df_przetworzony
    else:
        logging.info("Nie usuniętgo żadnych wierszy.")
        return df


def usun_rozdzielone_gminy_mw(df: pd.DataFrame, teryt_col: str="TERYT") -> pd.DataFrame:
    """
    Wywołuje funkcję usun_z_ostatnia_cyfra, usuwając wszystkie wiersze, które kończą się na 4 lub 5.
    W kodach (7-cyfrowych) często mamy gminę miejsko-wiejską i oddzielnie miasto i wieś, zazwyczaj chcemy zostawić tylko gminę.
    """
    if teryt_col not in df.columns:
        logging.warning(f"Kolumna '{teryt_col}' nie istnieje.")
        return df

    if df.empty:
        logging.info("DataFrame jest pusty.")
        return df

    teryt_pierwszego_wiersza = str(df[teryt_col].iloc[0])

    warunek1=teryt_pierwszego_wiersza.startswith("0") and len(teryt_pierwszego_wiersza)==7
    warunek2=(not teryt_pierwszego_wiersza.startswith("0")) and len(teryt_pierwszego_wiersza)==6 #jeżeli kody były zamienione na inta, to znika pierwsza cyfra
    if warunek1 or warunek2:
        df_przetworzony = usun_z_ostatnia_cyfra(df, column=teryt_col, cyfry=['4', '5'])
        return df_przetworzony
    else:
        logging.info("Nie usuniętgo żadnych wierszy.")
        return df