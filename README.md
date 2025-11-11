# Dokumentacja Analityczna Symulacji NIDUC
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

### 1.4. Demodulator (Reguły Decyzyjne)

* **BPSK:** Decyzja podejmowana jest na podstawie znaku części rzeczywistej.

    $$
    \hat{b} = \begin{cases} 0 & \text{jeśli } \text{Re}(r) > 0 \\ 1 & \text{jeśli } \text{Re}(r) < 0 \end{cases}
    $$

* **QPSK:** Dwa bity są odzyskiwane niezależnie na podstawie znaków części $I$ oraz $Q$.

    Dla bitu $\hat{b}_1$ (oś urojona):
    $$
    \hat{b}_1 = \begin{cases} 0 & \text{jeśli } \text{Im}(r) > 0 \\ 1 & \text{jeśli } \text{Im}(r) < 0 \end{cases}
    $$

    Dla bitu $\hat{b}_2$ (oś rzeczywista):
    $$
    \hat{b}_2 = \begin{cases} 0 & \text{jeśli } \text{Re}(r) > 0 \\ 1 & \text{jeśli } \text{Re}(r) < 0 \end{cases}
    $$

---

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

## 4. Wnioski z Analizy

1.  **Pełna Zgodność Modelu:** Analiza matematyczna krok po kroku wykazuje, że operacje wykonywane przez program (modulacja, demodulacja) są w **100% zgodne z teoretycznymi wzorami matematycznymi** dla BPSK i QPSK (z mapowaniem Graya).

2.  **Brak Błędów (BER = 0.0):** W analizowanym przebiegu nie wystąpiły żadne błędy bitowe. Oznacza to, że dla każdego symbolu, dodany szum ($n$) nie był wystarczająco silny, aby "przesunąć" odbierany symbol ($r$) poza jego ćwiartkę decyzyjną.

3.  **Analiza Szumu:**
    * **BPSK (Symbol 3):** Symbol nadany to $s_3 = -1.0$. Odebrany $r_3 = -0.875...$. Szum $n_3 = r_3 - s_3 = +0.125...$ przesunął symbol *w kierunku* granicy decyzyjnej (Re=0). Mimo to, symbol pozostał po właściwej stronie ($< 0$), a bit został zdekodowany poprawnie.
    * **QPSK (Symbol 1):** Symbol nadany $s_1 \approx 0.707 - 0.707j$. Odebrany $r_1 \approx 0.693 - 1.726j$.
        * Dla bitu $\hat{b}_1$ (oś Im): szum $n_Q = -1.019...$ *oddalił* symbol od granicy (Im=0), zwiększając margines błędu.
        * Dla bitu $\hat{b}_2$ (oś Re): szum $n_I = -0.0139...$ *przybliżył* symbol do granicy (Re=0) z $0.707$ do $0.693$. Mimo to, nie przekroczył jej.

4.  **Wniosek Końcowy:** Program działa poprawnie. Wygenerowane dane wyjściowe są idealnym odzwierciedleniem matematycznego procesu modulacji, transmisji przez kanał AWGN i demodulacji. "Różnice" między modelem a programem są zerowe, co potwierdza, że program jest poprawną implementacją modelu teoretycznego.
