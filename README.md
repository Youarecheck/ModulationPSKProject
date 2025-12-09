Oto kompletna dokumentacja techniczna projektu symulacji systemów telekomunikacyjnych, przygotowana na podstawie dostarczonych plików kodu źródłowego.

-----

# Dokumentacja Projektu: Symulator Modulacji Cyfrowych (PSK/QAM) w Kanale AWGN

## 1\. Przegląd Projektu

Projekt jest narzędziem symulacyjnym napisanym w języku Python, służącym do analizy wydajności różnych schematów modulacji cyfrowej (**BPSK, QPSK, 8-PSK, 16-QAM**) w obecności szumu. Głównym celem jest wyznaczenie zależności stopy błędów bitowych (**BER** - Bit Error Rate) od stosunku energii bitu do gęstości widmowej mocy szumu (**$E_b/N_0$**).

Symulacja realizuje pełny tor transmisyjny:

1.  Generowanie losowego strumienia bitów.
2.  Modulacja (mapowanie bitów na symbole zespolone).
3.  Transmisja przez kanał z szumem (AWGN).
4.  Demodulacja (detekcja).
5.  Obliczenie stopy błędów (BER).

-----

## 2\. Wymagania i Zależności

Do uruchomienia projektu wymagane są następujące biblioteki języka Python:

  * **NumPy**: Obliczenia macierzowe, generowanie szumu, operacje na tablicach.
  * **Matplotlib**: (Opcjonalnie w obecnym kodzie używany do wykresów, choć w `main.py` głównie importowany).
  * **SciPy**: Wykorzystywany w `Modulator.py` (importy `cosine`, `pbdn_seq`), choć główna logika opiera się na NumPy.

-----

## 3\. Struktura Modułów

System został podzielony na funkcjonalne moduły. Poniżej znajduje się szczegółowy opis każdego z nich.

### 3.1. `main.py` (Główny sterownik)

Plik ten zarządza przebiegiem symulacji dla wszystkich typów modulacji.

  * **Funkcja `calculate_ber(original_bits, decoded_bits)`**:
      * Porównuje bit po bicie ciąg nadany z odebranym.
      * Zwraca stosunek liczby błędów do całkowitej liczby bitów.
  * **Funkcje symulacyjne (`simulate_bpsk`, `simulate_qpsk`, `simulate_16qam`, `simulate_8psk`)**:
      * Przyjmują zakres wartości $E_b/N_0$ (w dB) oraz liczbę bitów do symulacji.
      * Dla każdego punktu pomiarowego wykonują pełną pętlę: Generacja $\rightarrow$ Modulacja $\rightarrow$ Kanał $\rightarrow$ Demodulacja $\rightarrow$ BER.
      * Zwracają listę wartości BER.
      * **Ważne:** Funkcje te dbają o to, by liczba generowanych bitów była podzielna przez liczbę bitów na symbol (np. podzielna przez 3 dla 8-PSK).
  * **`main()`**:
      * Definiuje parametry symulacji (zakres $E_b/N_0$ od -2 do 15 dB).
      * Uruchamia symulacje sekwencyjnie i wypisuje wyniki na konsolę.

### 3.2. `Modulator.py` (Mapowanie symboli)

Odpowiada za zamianę ciągu bitów na liczby zespolone (konstelacje).

  * **`bpsk_modulation(bits)`**:
      * Mapuje 1 bit na symbol.
      * Logika: $0 \rightarrow 1$, $1 \rightarrow -1$.
  * **`qpsk_modulation(bits)`**:
      * Mapuje 2 bity na symbol.
      * Stosuje **kodowanie Graya**.
      * Normalizacja: Symbole są skalowane przez $1/\sqrt{2}$, aby zachować jednostkową energię.
  * **`psk8_modulation(bits)`**:
      * Mapuje 3 bity na symbol.
      * Wykorzystuje fazy będące wielokrotnościami $\pi/4$.
      * Zastosowano kodowanie Graya w celu minimalizacji błędów bitowych przy pomyłce o sąsiedni symbol.
  * **`qam16_modulation(bits)`**:
      * Mapuje 4 bity na symbol.
      * Dzieli bity na część rzeczywistą (I) i urojoną (Q).
      * Mapowanie PAM-4: pary bitów $(00, 01, 11, 10)$ mapowane na poziomy $(-3, -1, 1, 3)$.
      * **Normalizacja:** Wynik jest mnożony przez $1/\sqrt{10}$, aby uzyskać średnią energię symbolu równą 1.

### 3.3. `Demodulator.py` (Detekcja)

Odpowiada za odtworzenie bitów z zaszumionych symboli zespolonych.

  * **`bpsk_demodulation`**:
      * Sprawdza część rzeczywistą sygnału. Jeśli $< 0$, zwraca 1, w przeciwnym razie 0.
  * **`qpsk_demodulation`**:
      * Decyzja na podstawie ćwiartki układu współrzędnych (znak części rzeczywistej i urojonej).
  * **`psk8_demodulation`**:
      * Demodulator ML (Maximum Likelihood).
      * Oblicza odległość euklidesową odebranego punktu od wszystkich 8 punktów konstelacji i wybiera najbliższy.
  * **`qam16_demodulation`**:
      * Najpierw denormalizuje sygnał (mnoży przez $\sqrt{10}$).
      * Stosuje progi decyzyjne dla PAM-4 (progi: -2, 0, 2) niezależnie dla części rzeczywistej i urojonej.

### 3.4. `AddAWGNNoise.py` (Model Kanału)

Implementuje dodawanie Addytywnego Białego Szumu Gaussowskiego (AWGN).

  * **`add_awgn_noise(symbols, eb_n0_db)`**:
    1.  Konwertuje $E_b/N_0$ z dB na skalę liniową.
    2.  Zakłada znormalizowaną energię bitu $E_b = 1.0$.
    3.  Oblicza gęstość widmową mocy szumu $N_0 = E_b / (E_b/N_0)_{lin}$.
    4.  Generuje szum zespolony, gdzie części rzeczywista i urojona są niezależnymi zmiennymi losowymi o rozkładzie normalnym ze standardowym odchyleniem $\sigma = \sqrt{N_0/2}$.
    5.  Dodaje szum do sygnału wejściowego.

### 3.5. `TransmissionChannel.py`

Warstwa abstrakcji nad kanałem szumu.

  * **`transmission_channel`**: Funkcja opakowująca (wrapper), która bezpośrednio wywołuje `add_awgn_noise`. Ułatwia potencjalną przyszłą rozbudowę modelu kanału (np. o zaniki) bez zmieniania reszty kodu.

### 3.6. `GetBytes.py`

Generator danych wejściowych.

  * **`gen_bites(N_bits)`**: Generuje losową tablicę NumPy o długości `N_bits` zawierającą zera i jedynki (typ `int`).

-----

## 4\. Przepływ Danych (Data Flow)

Dla każdej iteracji w `main.py`:

1.  **Źródło:** `gen_bites(n)` $\rightarrow$ wektor bitów $[0, 1, 0, ...]$.
2.  **Modulator:** Np. `qpsk_modulation` bierze wektor bitów $\rightarrow$ wektor symboli zespolonych $[0.7+0.7j, -0.7+0.7j, ...]$.
3.  **Kanał:** `transmission_channel` bierze symbole i parametr dB $\rightarrow$ dodaje losowy szum Gaussa.
4.  **Demodulator:** Np. `qpsk_demodulation` analizuje zaszumione punkty $\rightarrow$ odtwarza wektor bitów (estymata).
5.  **Licznik Błędów:** Porównanie wektora z pkt 1 i pkt 4 $\rightarrow$ wynik BER.

-----

## 5\. Instrukcja Uruchomienia

1.  Upewnij się, że wszystkie pliki (`main.py`, `Modulator.py`, `Demodulator.py`, `AddAWGNNoise.py`, `TransmissionChannel.py`, `GetBytes.py`) znajdują się w tym samym katalogu.
2.  Uruchom plik `main.py`:
    ```bash
    python main.py
    ```
3.  Wyniki zostaną wyświetlone w konsoli w formacie:
    ```text
    Running Simulations...
    [1/4] BPSK
    Eb/N0 = -2 dB  =>  BER = 0.103400
    ...
    Eb/N0 = 10 dB  =>  BER = 0.000000
    ```

## 6\. Uwagi Implementacyjne

  * **Wektoryzacja:** Kod intensywnie wykorzystuje bibliotekę NumPy, unikając wolnych pętli `for` przy przetwarzaniu bitów wewnątrz funkcji modulacji/demodulacji.
  * **Normalizacja Energii:** Kluczowym elementem poprawności symulacji jest fakt, że modulatory (szczególnie 16-QAM i QPSK) normalizują energię symbolu. Dzięki temu założenie w generatorze szumu ($E_b=1$) jest spójne z resztą systemu.
