W pliku nagłówkowym `lcd44780.h` znajduje się poniższy fragment:
```c
#define PORT(x)  SPORT(x)
#define SPORT(x) (PORT##x)
#define PIN(x)   SPIN(x)
#define SPIN(x)  (PIN##x)
#define DDR(x)   SDDR(x)
#define SDDR(x)  (DDR##x)
```
Długo się głowiłem, o co w tym chodzi. (Wiem - Mirek podlinkował na swoim blogu wpis wyjaśniający, ale mnie to wyjaśnienie jakoś nie specjalnie pomogło. Dlatego poszukałem troszkę dodatkowych materiałów...

Słowo - klucz: ***"makrorozwinięcia z parametrami"***

Normalnie `#define WYR1 WYR2` spowoduje, że preprocesor zastąpi w kodzie ciąg znaków `WYR1` ciągiem `WYR2` - z kilkoma wyjątkami:
 - makrorozwinięcia nie obowiązują wewnątrz stałych tekstowych - Czyli jeśli ztefiniujemy sobie `char t[] = "Wyrazenie WYR1"`, to nie zostanie ono zmienione na `char t[] = "Wyrazenie WYR2"`
 - makrorozwinięcia dotyczą tylko całych jednostek leksykalnych - `WYR1_x` nie zostanie zastąpione `WYR2_x`

Jeśli identyczne makro ma zostać zastosowane w wielu miejscach i różnych wywołań, możemy wywoływać je z argumentem

przykład:

`#define ps(a, b) (a^2 + 2*a*b + b^2)` 

spowoduje, że jeśli w kodzie wpiszemy

`x = ps(4,3)`

to zostanie ono podmienione na 

`x = (4^2 + 2*4*3 + 3^2)`

Wracamy więc do kodu 

Na samym początku musimy przyjąć, że linia sterujące RS będzie podłączona do pinu 0 na porcie B 

Dlatego w pliku nagłówkowym `lcd44780.h` mamy na samym początku:

```c
#define LCD_RSPORT  A
#define LCD_RS 0
```

Następnie nasze makrodefinicje

```c
#define PORT(x) SPORT(x)
#define SPORT(x) (PORT##x)
#define PIN(x) SPIN(x)
#define SPIN(x) (PIN##x)
#define DDR(x) SDDR(x)
#define SDDR(x) (DDR##x)
```

Natomiast w pliku źródłowym `lcd44780.c` mamy makra ustawiające wybrane piny:

```c
#define SET_RS  PORT(LCD_RSPORT) |= (1<<LCD_RS)
#define CLR_RS  PORT(LCD_RSPORT) &= ~(1<<LCD_RS)
```

a pod sam koniec, w definicji funkcji lcd_init:

```c
DDR(LCD_RSPORT) |= (1<<LCD_RS);       // ustawienie pinu RS jako wyjscia
PORT(LCD_RSPORT) |= (1<<LCD_RS);      // Stan wysoki na pinie RS
```

i kilka dodatkowych instrukcji wydawanych z innych funkcji

```c
lcd_write_data - SET_RS;
check_BF       - CLR_RS;
lcd_write_cmd  - CLR_RS;
```

W końcu możemy to poskładać w jedną całość - oto, co wykonuje po kolei preprocesor:

1. Podstawienie w kodzie wybranego portu i pinu dla linii RS **LCD_RSPORT->A i LCD_RS->0**
```c
DDR(LCD_RSPORT) |= (1<<LCD_RS);                  => DDR(A) |= (1<<0);
PORT(LCD_RSPORT) |= (1<<LCD_RS);                 => PORT(A) |= (1<<0);
#define SET_RS  PORT(LCD_RSPORT) |= (1<<LCD_RS)  => #define SET_RS  PORT(A) |= (1<<0)
#define CLR_RS  PORT(LCD_RSPORT) &= ~(1<<LCD_RS) => #define CLR_RS  PORT(A) &= ~(1<<0)
```
2. To, co otrzymaliśmy w punkckie 1 jest jeszcze raz przerabiane **PORT(x)->SPORT(x) i DDR(x)->SDDR(x)**
```c
DDR(A) |= (1<<0);                                => SDDR(A) |= (1<<0);  
PORT(A) |= (1<<0);                               => SPORT(A) |= (1<<0);
#define SET_RS  PORT(A) |= (1<<0)                => #define SET_RS  SPORT(A) |= (1<<0)
#define CLR_RS  PORT(A) &= ~(1<<0)               => #define CLR_RS  SPORT(A) &= ~(1<<0)
```
3. I jeszcze raz... **SPORT(x)->(PORT##x) i SDDR(x)->(DDR##x)**
```c
SDDR(A) |= (1<<0);                               => DDRA |= (1<<0);
SPORT(A) |= (1<<0);                              => PORTA |= (1<<0);
#define SET_RS  SPORT(A) |= (1<<0)               => #define SET_RS  PORTA |= (1<<0)
#define CLR_RS  SPORT(A) &= ~(1<<0)              => #define CLR_RS  PORTA &= ~(1<<0)
```
Co tu się stało???

Użycie ## powoduje **"sklejenie"** paramatrów, z którymi zostało wywołane makro. 

Makro: `#define sklej(X, Y) (X##Y)`

wywołane przez `sklej(poczatek, koniec)` spowoduje rozwinięcie `poczatekkoniec`

Makro: `#define sklej(X, Y) (X##_i_##Y)`

wywołane przez `sklej(poczatek, koniec)` spowoduje rozwinięcie `poczatek_i_koniec`

Makro: `#define doklej(Y) (poczatek_i_##Y)`

wywołane przez `doklej(koniec)` również spowoduje rozwinięcie `poczatek_i_koniec`

W naszym przypadku chodzi nam o zamianę `PORT(A)` and `PORTA` 

#### I nie możemy po prostu użyć 

`#define PORT(x) (PORT##x)`

bo po drodze mamy też

`#define SET_RS  PORT(LCD_RSPORT) |= (1<<LCD_RS)`

które zostałoby zamienienione na

`#define SET_RS  PORTLCD_RSPORT |= (1<<0)`

dlatego właśnie potrzebny jest dodatkowy krok z użyciem SPORT i SDDR
