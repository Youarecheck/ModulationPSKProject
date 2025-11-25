# Dokumentacja Analityczna Symulacji NIDUC


# 📋 Założenia Projektowe - Projekt NIDUC

## 1. Cel Główny i Zakres Projektu

Celem projektu jest stworzenie symulatora cyfrowej komunikacji w Pythonie, który umożliwi **porównawczą analizę niezawodności** dwóch schematów modulacji: **QPSK** (Quadrature Phase Shift Keying) oraz **8PSK** (8-ary Phase Shift Keying).

Analiza ma skupić się na badaniu zależności **Bit Error Rate (BER)** od stosunku energii bitu do gęstości widmowej mocy szumu (**$E_b/N_0$**).

## 2. Wymagania Funkcjonalne (Moduły Symulatora)

System musi być zaimplementowany w architekturze modułowej, z jasno zdefiniowanymi funkcjami dla każdego etapu transmisji:

### 2.1. Modulacja (Modulator)
* Implementacja mapowania bitów na symbole dla:
    * **QPSK** (2 bity/symbol, 4 stany) – Zastosowanie mapowania Graya.
    * **8PSK** (3 bity/symbol, 8 stanów) – Zastosowanie mapowania Graya.
* Zapewnienie normalizacji mocy symboli ($E_s$) do wartości jednostkowej, co jest krytyczne dla poprawnego obliczenia $E_b/N_0$.

### 2.2. Kanał Transmisyjny (Channel)
* Wdrożenie modelu **kanału AWGN (Additive White Gaussian Noise)**.
* Poprawne skalowanie mocy szumu ($N_0$) na podstawie wartości **$E_b/N_0$** zgodnie z zależnością $E_s = k \cdot E_b$ (gdzie $k$ to liczba bitów na symbol).

### 2.3. Demodulacja i Dekodowanie (Demodulator)
* Zaimplementowanie optymalnego **demodulatora koherentnego** opartego na detekcji najbliższej odległości (Maximum Likelihood Detection) dla obu modulacji (QPSK i 8PSK).
* Poprawne odzyskanie strumienia bitów z odebranych symboli.

### 2.4. Metryki (Metrics)
* Implementacja funkcji obliczającej **BER** jako stosunek liczby błędnych bitów do całkowitej liczby przesłanych bitów.

## 3. Wymagania Niefunkcjonalne i Techniczne

| Aspekt | Wymaganie / Technologia | Uzasadnienie |
| :--- | :--- | :--- |
| **Język Programowania** | Python 3.x | Zgodność z wytycznymi projektu i literaturą `Viswanathan2019...`. |
| **Biblioteki** | NumPy, Matplotlib, SciPy | NumPy zapewnia wydajność (wektoryzacja) niezbędną dla szybkich symulacji BER. Matplotlib do generowania wykresów. |
| **Architektura** | Modułowa | Łatwość testowania, utrzymania i diagnostyki kodu. Proponowany podział: `modulator.py`, `channel.py`, `demodulator.py`, `diagnostics.py`, `main_simulator.py`. |
| **Wydajność** | Wektoryzacja | Cały kod musi wykorzystywać operacje na wektorach NumPy, aby zminimalizować czas symulacji, zwłaszcza dla niskich wartości BER (wymagających bilionów bitów). |

## 4. Zakres Diagnostyki Systemu

W celu zwiększenia niezawodności i możliwości oceny stanu kanału, system musi zawierać proste mechanizmy diagnostyczne:

1.  **Monitorowanie Mocy Sygnału:** Funkcja obliczająca średnią moc odebranego sygnału. Spadek poniżej progu (np. 50% oczekiwanej mocy) musi generować alarm.
2.  **Wykrywanie Utraty Synchronizacji (Uproszczone):** Wysłanie znanej sekwencji bitów (preambuły) na początku. Jeśli BER dla samej preambuły przekroczy ustalony próg (np. 20%), system zgłasza błąd synchronizacji lub krytycznie zły stan kanału.

## 5. Dane Wyjściowe i Oczekiwane Rezultaty

Kluczowym rezultatem projektu jest następujący wykres i towarzysząca mu analiza:

* **Wykres BER vs $E_b/N_0$:** Jednolity wykres porównujący:
    1.  Teoretyczną krzywą BER dla QPSK.
    2.  Zsymulowaną krzywą BER dla QPSK.
    3.  Teoretyczną krzywą BER dla 8PSK.
    4.  Zsymulowaną krzywą BER dla 8PSK.
* **Analiza:** Pisemne wnioski dotyczące przesunięcia krzywych i kompromisu między niezawodnością (QPSK) a efektywnością widmową (8PSK).

### Oczekiwane Założenie Teoretyczne
Na wykresie należy oczekiwać, że:
* Krzywa **QPSK** będzie położona **bardziej na lewo** niż 8PSK (wymaga mniejszego $E_b/N_0$ dla tej samej niezawodności).
* Krzywa **8PSK** będzie położona **bardziej na prawo** (wymaga większego $E_b/N_0$ z uwagi na gęstszą konstelację symboli).

## Analiza Krok po Kroku: BPSK vs QPSK

Niniejszy dokument stanowi szczegółową analizę matematyczną pojedynczego przebiegu symulacji, porównując wyniki z programu z modelem teoretycznym.

**Dane Wejściowe (Program):**
* **Strumień bitów:** `[1 0 1 1 0 0 1 0 1 0]` (10 bitów)
* **Wyniki BPSK:** BER 0.0 (0/10 błędów)
* **Wyniki QPSK:** BER 0.0 (0/10 błędów)

---

## 1. Zastosowane Modele i Wzory Matematyczne

Analiza opiera się na następujących formułach:

### 1.1. Modulator BPSK
Modulacja BPSK mapuje jeden bit ($b$) na jeden symbol zespolony ($s$). Na podstawie danych programu, zastosowano mapowanie:
* Bit `0` $\to$ Symbol `+1.0 + 0j`
* Bit `1` $\to$ Symbol `-1.0 + 0j`

Wzór matematyczny (dla $b \in \{0, 1\}$):
$$s = (1 - 2b) + 0j$$

### 1.2. Modulator QPSK
Modulacja QPSK mapuje parę bitów ($b_1, b_2$) na jeden symbol zespolony ($s$). Zastosowano standardowe mapowanie Graya z normalizacją $E_s = 1$.

$$s = \frac{1}{\sqrt{2}} (I + jQ)$$

Na podstawie analizy danych programu, mapowanie bitów na składowe $I$ i $Q$ jest następujące:
* $b_1$ (pierwszy bit): Decyduje o znaku części urojonej ($Q$).
* $b_2$ (drugi bit): Decyduje o znaku części rzeczywistej ($I$).

Zasady mapowania (zgodne z danymi):
* `Im(s)` (oś $Q$): $b_1 = 0 \to +1/\sqrt{2}$; $b_1 = 1 \to -1/\sqrt{2}$
* `Re(s)` (oś $I$): $b_2 = 0 \to +1/\sqrt{2}$; $b_2 = 1 \to -1/\sqrt{2}$

Stąd (dla pary bitów `(b1, b2)`):
* `(0, 0)` $\to$ `(1+1j) / sqrt(2)`
* `(0, 1)` $\to$ `(-1+1j) / sqrt(2)`
* `(1, 1)` $\to$ `(-1-1j) / sqrt(2)`
* `(1, 0)` $\to$ `(1-1j) / sqrt(2)`

### 1.3. Kanał Transmisyjny (AWGN)
Model kanału jest addytywny. Odbierany symbol ($r$) jest sumą nadanego symbolu ($s$) i zespolonego szumu gaussowskiego ($n$).

$$r = s + n$$
$$n = n_I + j \cdot n_Q$$

W tej analizie, obliczamy wektor szumu $n$ na podstawie danych programu, używając przekształconego wzoru:

$$n = r - s$$



## 1.4. Demodulator (Reguły Decyzyjne) ✅

Reguły decyzyjne określają, po której stronie granicy (oś $I$ lub $Q$) wylądował symbol, co determinuje odzyskaną wartość bitu.

### A. BPSK (Decyzja oparta na osi rzeczywistej)
* **Jeśli $\text{Re}(r) > 0$** (Pozytywna strona osi $I$) $\to$ Bit $\hat{b} = 0$.
* **Jeśli $\text{Re}(r) < 0$** (Negatywna strona osi $I$) $\to$ Bit $\hat{b} = 1$.

### B. QPSK (Dwa Bity Niezależnie)
#### Bit $\hat{b}_1$ (Oś Urojona / $Q$):
* **Jeśli $\text{Im}(r) > 0$** (Pozytywna strona osi $Q$) $\to$ Bit $\hat{b}_1 = 0$.
* **Jeśli $\text{Im}(r) < 0$** (Negatywna strona osi $Q$) $\to$ Bit $\hat{b}_1 = 1$.

#### Bit $\hat{b}_2$ (Oś Rzeczywista / $I$):
* **Jeśli $\text{Re}(r) > 0$** (Pozytywna strona osi $I$) $\to$ Bit $\hat{b}_2 = 0$.
* **Jeśli $\text{Re}(r) < 0$** (Negatywna strona osi $I$) $\to$ Bit $\hat{b}_2 = 1$.

***

## 2. Analiza Krok po Kroku (Przykładowe Obliczenia)

Poniżej prześledzimy pierwsze dwa etapy (symbole) dla obu modulacji, stosując powyższe wzory.

### 2.1. Przykład BPSK

**Bity wejściowe:** `[1, 0, ...]`

**Symbol 1:**
1.  **Bit Wejściowy:** `1`
2.  **Modulacja (Model):** $s_1 = (1 - 2 \cdot 1) = -1.0 + 0j$
3.  **Symbol Nadany (Program):** `bpsk_symbols[0] = -1.+0.j`
4.  **Symbol Odebrany (Program):** `bpsk_received[0] = -1.24738922 - 0.41988784j`
5.  **Obliczony Szum (Model):**
    $n_1 = r_1 - s_1$
    $n_1 = (-1.247... - 0.419...j) - (-1.0 + 0j)$
    $n_1 = -0.2473... - 0.4198...j$
6.  **Demodulacja (Model):**
    $\text{Re}(r_1) = -1.247...$
    Ponieważ $-1.247... < 0$, reguła decyzyjna daje: $\hat{b}_1 = 1$.
7.  **Bit Zdekodowany (Program):** `1`
8.  **Wniosek:** Model i program są zgodne.

**Symbol 2:**
1.  **Bit Wejściowy:** `0`
2.  **Modulacja (Model):** $s_2 = (1 - 2 \cdot 0) = 1.0 + 0j$
3.  **Symbol Nadany (Program):** `bpsk_symbols[1] = 1.+0.j`
4.  **Symbol Odebrany (Program):** `bpsk_received[1] = 1.29640351 - 0.44746477j`
5.  **Obliczony Szum (Model):**
    $n_2 = r_2 - s_2$
    $n_2 = (1.296... - 0.447...j) - (1.0 + 0j)$
    $n_2 = 0.2964... - 0.4474...j$
6.  **Demodulacja (Model):**
    $\text{Re}(r_2) = 1.296...$
    Ponieważ $1.296... > 0$, reguła decyzyjna daje: $\hat{b}_2 = 0$.
7.  **Bit Zdekodowany (Program):** `0`
8.  **Wniosek:** Model i program są zgodne.

### 2.2. Przykład QPSK

**Bity wejściowe:** `[1, 0, 1, 1, ...]`

**Symbol 1 (Bity: `(1, 0)`):**
1.  **Bity Wejściowe:** `(b1=1, b2=0)`
2.  **Modulacja (Model):** Zgodnie z mapowaniem dla `(1, 0)`:
    $s_1 = (1 - 1j) / \sqrt{2} \approx 0.7071... - 0.7071...j$
3.  **Symbol Nadany (Program):** `qpsk_symbols[0] = 0.70710678 - 0.70710678j`
4.  **Symbol Odebrany (Program):** `qpsk_received[0] = 0.69317012 - 1.72613373j`
5.  **Obliczony Szum (Model):**
    $n_1 = r_1 - s_1$
    $n_1 = (0.693... - 1.726...j) - (0.707... - 0.707...j)$
    $n_1 = (0.693... - 0.707...) + j(-1.726... + 0.707...)$
    $n_1 = -0.0139... - 1.0190...j$
6.  **Demodulacja (Model):**
    * $\text{Im}(r_1) = -1.726...$ (jest $< 0$) $\implies \hat{b}_1 = 1$
    * $\text{Re}(r_1) = 0.693...$ (jest $> 0$) $\implies \hat{b}_2 = 0$
    Zdekodowana para to `(1, 0)`.
7.  **Bity Zdekodowane (Program):** `[1, 0]`
8.  **Wniosek:** Model i program są zgodne.

**Symbol 2 (Bity: `(1, 1)`):**
1.  **Bity Wejściowe:** `(b1=1, b2=1)`
2.  **Modulacja (Model):** Zgodnie z mapowaniem dla `(1, 1)`:
    $s_2 = (-1 - 1j) / \sqrt{2} \approx -0.7071... - 0.7071...j$
3.  **Symbol Nadany (Program):** `qpsk_symbols[1] = -0.70710678 - 0.70710678j`
4.  **Symbol Odebrany (Program):** `qpsk_received[1] = -1.64189167 - 1.3827197j`
5.  **Obliczony Szum (Model):**
    $n_2 = r_2 - s_2$
    $n_2 = (-1.641... - 1.382...j) - (-0.707... - 0.707...j)$
    $n_2 = (-1.641... + 0.707...) + j(-1.382... + 0.707...)$
    $n_2 = -0.9347... - 0.6755...j$
6.  **Demodulacja (Model):**
    * $\text{Im}(r_2) = -1.382...$ (jest $< 0$) $\implies \hat{b}_1 = 1$
    * $\text{Re}(r_2) = -1.641...$ (jest $< 0$) $\implies \hat{b}_2 = 1$
    Zdekodowana para to `(1, 1)`.
7.  **Bity Zdekodowane (Program):** `[1, 1]`
8.  **Wniosek:** Model i program są zgodne.

---

## 3. Tabela Porównawcza Wyników

Poniższe tabele podsumowują zgodność modelu matematycznego z wynikami programu dla pierwszych 4 bitów.

### Tabela 3.1: Modulacja BPSK

| Etap | Model Matematyczny (Obliczenia) | Wynik z Programu | Różnica / Zgodność |
| :--- | :--- | :--- | :--- |
| **Bit 1** | `1` | `1` | Zgodne |
| Modulacja | $s = (1-2 \cdot 1) = -1.0$ | `bpsk_symbols[0] = -1.0` | Zgodne |
| Odbiór | $r_1 = s_1 + n_1$ | `bpsk_received[0] = -1.247...`| (Dane wejściowe) |
| Demodulacja | $\text{Re}(-1.247) < 0 \implies \hat{b}=1$ | `Decoded bits[0] = 1` | Zgodne |
| **Bit 2** | `0` | `0` | Zgodne |
| Modulacja | $s = (1-2 \cdot 0) = 1.0$ | `bpsk_symbols[1] = 1.0` | Zgodne |
| Odbiór | $r_2 = s_2 + n_2$ | `bpsk_received[1] = 1.296...`| (Dane wejściowe) |
| Demodulacja | $\text{Re}(1.296) > 0 \implies \hat{b}=0$ | `Decoded bits[1] = 0` | Zgodne |
| **Bit 3** | `1` | `1` | Zgodne |
| Modulacja | $s = (1-2 \cdot 1) = -1.0$ | `bpsk_symbols[2] = -1.0` | Zgodne |
| Odbiór | $r_3 = s_3 + n_3$ | `bpsk_received[2] = -0.875...`| (Dane wejściowe) |
| Demodulacja | $\text{Re}(-0.875) < 0 \implies \hat{b}=1$ | `Decoded bits[2] = 1` | Zgodne |
| **Bit 4** | `1` | `1` | Zgodne |
| Modulacja | $s = (1-2 \cdot 1) = -1.0$ | `bpsk_symbols[3] = -1.0` | Zgodne |
| Odbiór | $r_4 = s_4 + n_4$ | `bpsk_received[4] = -1.726...`| (Dane wejściowe) |
| Demodulacja | $\text{Re}(-1.726) < 0 \implies \hat{b}=1$ | `Decoded bits[3] = 1` | Zgodne |

### Tabela 3.2: Modulacja QPSK

| Etap | Model Matematyczny (Obliczenia) | Wynik z Programu | Różnica / Zgodność |
| :--- | :--- | :--- | :--- |
| **Bity 1-2** | `(1, 0)` | `[1, 0]` | Zgodne |
| Modulacja | $s = (1-1j)/\sqrt{2}$ | `qpsk_symbols[0] = 0.707...-0.707...j`| Zgodne |
| Odbiór | $r_1 = s_1 + n_1$ | `qpsk_received[0] = 0.693...-1.726...j` | (Dane wejściowe) |
| Demodulacja $\hat{b}_1$| $\text{Im}(-1.726) < 0 \implies \hat{b}_1=1$ | `Decoded bits[0] = 1` | Zgodne |
| Demodulacja $\hat{b}_2$| $\text{Re}(0.693) > 0 \implies \hat{b}_2=0$ | `Decoded bits[1] = 0` | Zgodne |
| **Bity 3-4** | `(1, 1)` | `[1, 1]` | Zgodne |
| Modulacja | $s = (-1-1j)/\sqrt{2}$ | `qpsk_symbols[1] = -0.707...-0.707...j`| Zgodne |
| Odbiór | $r_2 = s_2 + n_2$ | `qpsk_received[1] = -1.641...-1.382...j` | (Dane wejściowe) |
| Demodulacja $\hat{b}_1$| $\text{Im}(-1.382) < 0 \implies \hat{b}_1=1$ | `Decoded bits[2] = 1` | Zgodne |
| Demodulacja $\hat{b}_2$| $\text{Re}(-1.641) < 0 \implies \hat{b}_2=1$ | `Decoded bits[3] = 1` | Zgodne |

---


### Tabela 3.3: Porównanie Całego Strumienia Bitów (10 Bitów)

| Modulacja | Bity Nadane (Wejście Modelu) | Bity Otrzymane (Wyjście Programu) | Liczba Błędów | BER | Weryfikacja |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BPSK** | `[1 0 1 1 0 0 1 0 1 0]` | `[1 0 1 1 0 0 1 0 1 0]` | 0 / 10 | 0.0000 | **ZGODNOŚĆ** |
| **QPSK** | `[1 0 1 1 0 0 1 0 1 0]` | `[1 0 1 1 0 0 1 0 1 0]` | 0 / 10 | 0.0000 | **ZGODNOŚĆ** |

***

## 3.4 Szczegółowa Weryfikacja Działania (Model Matematyczny vs. Program)

Poniższe tabele weryfikują, że **Model Matematyczny (Teoretyczna Decyzja)** jest identyczny z **Wynikiem Programu**.

### 3.5. Weryfikacja Modulacji BPSK (10 Bitów)

| Bit (i) | Bit Nadany ($b_i$) | Symbol Nadany ($s_i$) | Symbol Odebrany ($r_i$) | $\text{Re}(r)$ | **Decyzja Mat. ($\hat{b}_i$)** | **Wynik Programu** |
| :---: | :---: | :---: | :--- | :---: | :---: | :---: |
| 1 | **1** | -1.0 + 0j | -1.247... - 0.419...j | -1.247 | **1** ($\text{Re}<0$) | 1 |
| 2 | **0** | 1.0 + 0j | 1.296... - 0.447...j | +1.296 | **0** ($\text{Re}>0$) | 0 |
| 3 | **1** | -1.0 + 0j | -0.875... + 0.491...j | -0.875 | **1** ($\text{Re}<0$) | 1 |
| 4 | **1** | -1.0 + 0j | -1.726... - 0.287...j | -1.726 | **1** ($\text{Re}<0$) | 1 |
| 5 | **0** | 1.0 + 0j | 0.563... - 0.436...j | +0.563 | **0** ($\text{Re}>0$) | 0 |
| 6 | **0** | 1.0 + 0j | 1.092... - 0.889...j | +1.092 | **0** ($\text{Re}>0$) | 0 |
| 7 | **1** | -1.0 + 0j | -1.513... - 0.449...j | -1.513 | **1** ($\text{Re}<0$) | 1 |
| 8 | **0** | 1.0 + 0j | 0.636... + 0.003...j | +0.636 | **0** ($\text{Re}>0$) | 0 |
| 9 | **1** | -1.0 + 0j | -0.882... - 0.242...j | -0.882 | **1** ($\text{Re}<0$) | 1 |
| 10 | **0** | 1.0 + 0j | 0.378... - 0.258...j | +0.378 | **0** ($\text{Re}>0$) | 0 |

### 3.6. Weryfikacja Modulacji QPSK (5 Symboli / 10 Bitów)

| Symbol (i) | Bity Nadane ($b_1, b_2$) | Symbol Nadany ($s_i$) | Symbol Odebrany ($r_i$) | $\text{Im}(r)$ ($\hat{b}_1$) | $\text{Re}(r)$ ($\hat{b}_2$) | **Decyzja Mat. ($\hat{b}_1, \hat{b}_2$)** | **Wynik Programu** |
| :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | **1, 0** | 0.707-0.707j | 0.693... - 1.726...j | -1.726 ($\mathbf{1}$) | +0.693 ($\mathbf{0}$) | **1, 0** | 1, 0 |
| 2 | **1, 1** | -0.707-0.707j | -1.641... - 1.382...j | -1.382 ($\mathbf{1}$) | -1.641 ($\mathbf{1}$) | **1, 1** | 1, 1 |
| 3 | **0, 0** | 0.707+0.707j | 0.829... + 0.946...j | +0.946 ($\mathbf{0}$) | +0.829 ($\mathbf{0}$) | **0, 0** | 0, 0 |
| 4 | **1, 0** | 0.707-0.707j | 1.270... - 0.506...j | -0.506 ($\mathbf{1}$) | +1.270 ($\mathbf{0}$) | **1, 0** | 1, 0 |
| 5 | **1, 0** | 0.707-0.707j | 0.735... - 1.159...j | -1.159 ($\mathbf{1}$) | +0.735 ($\mathbf{0}$) | **1, 0** | 1, 0 |

***


## 4. Wnioski z Analizy

1.  **Pełna Zgodność Modelu:** Analiza matematyczna krok po kroku wykazuje, że operacje wykonywane przez program (modulacja, demodulacja) są w **100% zgodne z teoretycznymi wzorami matematycznymi** dla BPSK i QPSK (z mapowaniem Graya).

2.  **Brak Błędów (BER = 0.0):** W analizowanym przebiegu nie wystąpiły żadne błędy bitowe. Oznacza to, że dla każdego symbolu, dodany szum ($n$) nie był wystarczająco silny, aby "przesunąć" odbierany symbol ($r$) poza jego ćwiartkę decyzyjną.

3.  **Analiza Szumu:**
    * **BPSK (Symbol 3):** Symbol nadany to $s_3 = -1.0$. Odebrany $r_3 = -0.875...$. Szum $n_3 = r_3 - s_3 = +0.125...$ przesunął symbol *w kierunku* granicy decyzyjnej (Re=0). Mimo to, symbol pozostał po właściwej stronie ($< 0$), a bit został zdekodowany poprawnie.
    * **QPSK (Symbol 1):** Symbol nadany $s_1 \approx 0.707 - 0.707j$. Odebrany $r_1 \approx 0.693 - 1.726j$.
        * Dla bitu $\hat{b}_1$ (oś Im): szum $n_Q = -1.019...$ *oddalił* symbol od granicy (Im=0), zwiększając margines błędu.
        * Dla bitu $\hat{b}_2$ (oś Re): szum $n_I = -0.0139...$ *przybliżył* symbol do granicy (Re=0) z $0.707$ do $0.693$. Mimo to, nie przekroczył jej.

4.  **Wniosek Końcowy:** Program działa poprawnie. Wygenerowane dane wyjściowe są idealnym odzwierciedleniem matematycznego procesu modulacji, transmisji przez kanał AWGN i demodulacji. "Różnice" między modelem a programem są zerowe, co potwierdza, że program jest poprawną implementacją modelu teoretycznego.
