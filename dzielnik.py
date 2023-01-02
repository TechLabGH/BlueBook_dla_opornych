
print("Skrypt oblicza najlepsza pare rezystorow ktore mozna wybrac z zadanego szeregu, aby napiecie wyjsciowe dzielnika bylo jak najbardziej zblizone do zadanego")
print()
print("   ------------             ")
print("   |          |             ")
print("   |         ---            ")
print("   |         | | R1         ")
print("   |         | |            ")
print("   |         ---            ")
print("   |          |             ")
print("   Vin        *---------    ")
print("   |          |        |    ")
print("   |         ---       |    ")
print("   |         | | R2    Vout ")
print("   |         | |       |    ")
print("   |         ---       |    ")
print("   |          |        |    ")
print("   -----------*---------    ")
print()
vin_str = input("podaj napiecie WEJsciowe Vin: ")
vout_str = input("podaj napiecie WYJsiowe Vout: ")
print("Wybierz szereg E3/E6/E12/E24/E48/E96")
szereg = input("wciśnij ENTER aby wybrac domyslny E24: ")
print("Podaj opor R1 (1-999) aby go wymusic")
r1_str = input("w obliczeniach (ENTER - pomin): ")

r1_fix = 0
if r1_str != "":
    r1_fix = int(r1_str)

vin = float(vin_str)
vout = float(vout_str)

if szereg == "":
    szereg = "E24"

if szereg not in ["E3", "E6", "E12", "E24", "E48", "E96"]:
    raise SystemExit('Nie ma takiego szeregu')

if szereg == "E3":
    E = [10, 22, 47]

if szereg == "E6":
    E = [10, 15, 22, 33, 47, 68]

if szereg == "E12":
    E = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]

if szereg == "E24":
    E = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30,
         33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]

if szereg == "E48":
    E = [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 196, 205, 215, 226, 237, 249, 261, 274, 287, 301,
         316, 332, 348, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715, 750, 787, 825, 866, 909, 953]

if szereg == "E96":
    E = [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174, 178, 182, 187, 191, 196, 200, 205, 210, 216, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309,
         316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732, 750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976]

vout_best = None
r1_best = None
r2_best = None

for i, rez_r1 in enumerate(E):
    if r1_fix > 0:
        rez_r1 = r1_fix
    for j, rez_r2 in enumerate(E):
        new_vout = (rez_r2 / (float(rez_r1) + float(rez_r2))) * vin
        if vout_best is None or abs(new_vout - vout) < abs(vout_best - vout):
            vout_best = new_vout
            r1_best = rez_r1
            r2_best = rez_r2

print()
print("Najblizsza para rezystorow z szeregu ", szereg, " :")
print("  Rezystor R1:             ", r1_best)
print("  Rezystor R2:             ", r2_best)
print("  Obliczone napięcie wyj:                                     ")
print("       ", r2_best, "                                        ")
print("  --------------- x ", vin, "  =  ",
      round(((r2_best / (float(r1_best) + float(r2_best))) * vin), 3), " V ")
print("  (", r1_best, " + ", r2_best, ")                             ")
