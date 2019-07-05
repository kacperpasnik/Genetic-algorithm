import argparse
import random
import math

parser = argparse.ArgumentParser(description='Algorytm genetyczny')
parser.add_argument('-ch','--chromosom', help="Pula chromosomow",type=int,default=6,required=False)
parser.add_argument('-pm','--p_mutacji', help="Prawdopodobienstwo mutacji",type=float,default=0.2,required=False)
parser.add_argument('-pk','--p_krzyzowania', help="Prawdopodobienstwo krzyzowania",type=float,default=0.8,required=False)
parser.add_argument('-max','--max_iteracji', help="Maksimum iteracji algorytmu",type=int,default=1000,required=False)
parser.add_argument('-f','--wspolczynniki', help="Wspolczynniki funkcji ax^3+bx^2+cx+d",type=float,required=True,nargs=4)



args = parser.parse_args()


def obliczanie_funkcji_przystosowania(x):

	return int(((args.wspolczynniki[0]*pow(x, 3)) + (args.wspolczynniki[1]*pow(x, 2)) + (args.wspolczynniki[2]*x) + args.wspolczynniki[3]))

def losowanie_chromosomu():
	x = "aaaaa"
	losowana_liczba = 0
	for i in range(5):
		losowana_liczba = random.randint(0,1)
		if (losowana_liczba == 0):
			x = x[:i] + '0' +x[i+1:]
		elif (losowana_liczba == 1):
			x = x[:i] + '1' +x[i+1:]

	return x

def nowy_chromosom_selekcja(kolo_ruletki):
    i=0
    z=0
    losowana_liczba=0
    z=random.randint(0,100)
    losowana_liczba=float(z/100)
    for i in range(args.chromosom):
        losowana_liczba=losowana_liczba-kolo_ruletki[i]
        if losowana_liczba <=0:
            return i
        else:
            continue
    return i-1

def obliczanie_fenotypu(x):
    fenotyp= 0
    zastepcza= 0
    potega_dwojki= 0
    i= 4
    while i>= 0:
        if x[i] == '0':
            zastepcza = 0
        elif x[i] == '1':
            zastepcza = 1
        fenotyp = fenotyp + (zastepcza*math.pow(2, potega_dwojki))
        i-=1
        potega_dwojki+=1
    #print(" ")
    return int(fenotyp);

def mutacja(x):
	z = 0;
	y = 0;
	z = random.randint(1,100)
	y = float(z / 100);
	if y < args.p_mutacji:
		z = random.randint(0,4)
		if x[z] == '0':
			x = x[:z] + '1' +x[z+1:]
		elif x[z] == '1':
			x = x[:z] + '0' +x[z+1:]
	return x

def krzyzowanie():
    pass

def maksimum_funkcji():

	wynik = obliczanie_funkcji_przystosowania(0)
	wynik_funkcji = wynik
	for i in range(31):
	
		wynik_funkcji = obliczanie_funkcji_przystosowania(i);
		if wynik < wynik_funkcji:
		
			wynik = wynik_funkcji
		
	
	return wynik;

def mnimum_funkcji():

	wynik = obliczanie_funkcji_przystosowania(0)
	wynik_funkcji = wynik
	for i in range(31):
	
		wynik_funkcji = obliczanie_funkcji_przystosowania(i)
		if wynik > wynik_funkcji:
		
			wynik = wynik_funkcji
		
	

	if wynik > 0:
		return 0;
	else:
	    return wynik

	


#print(args.wspolczynniki[0])

x = 0; p = 0
chromosom=[0 for a in range(args.chromosom)]
chromosom_selekcja=[0 for a in range(args.chromosom)]
pula_poczatkowa=[0 for a in range(args.chromosom)]
pula_najlepsza=[0 for a in range(args.chromosom)]
fenotyp_poczatkowy=[0 for a in range(args.chromosom)]
fenotyp=[0 for a in range(args.chromosom)]
fenotyp_najlepszy=[0 for a in range(args.chromosom)]
losowanie_krzyzowania = 0
funkcja_przystosowania=[0 for a in range(args.chromosom)]
funkcja_przystosowania_max = 0
kolo_ruletki=[0 for a in range(args.chromosom)]
max_fenotyp = 0
max_suma = 0
suma_przystosowania = 0;
i = 0							#ilosc iteracji algorytmu
max_funkcji = maksimum_funkcji()
anty_minus = mnimum_funkcji() * (-1)
ilosc_iteracji=args.max_iteracji
for i in range(ilosc_iteracji):
    if i<1:
        for j in range (args.chromosom):
            chromosom[j]=losowanie_chromosomu()
            pula_poczatkowa[j]=chromosom[j]
            fenotyp[j]=obliczanie_fenotypu(chromosom[j])
            fenotyp_poczatkowy[j]=fenotyp[j]
            funkcja_przystosowania[j]=obliczanie_funkcji_przystosowania(fenotyp[j]) +anty_minus
            suma_przystosowania=suma_przystosowania+funkcja_przystosowania[j]
        #zliczanie sumy przystosowania
    for j in range(args.chromosom):
        kolo_ruletki[j]=funkcja_przystosowania[j] / suma_przystosowania
        #selekcja + ruletka
    for j in range(args.chromosom):
        chromosom_selekcja[j]=chromosom[nowy_chromosom_selekcja(kolo_ruletki)]  #brak funkcji nowy chromosom
        #krzyzowanie
    for j in range(0,args.chromosom,2):
        p= random.randint(1,100)
        losowanie_krzyzowania= float(p/100)
        if losowanie_krzyzowania<args.p_krzyzowania:
             p= random.randint(0,4)
                
             for p in range(5):
                 zastepczy_char=chromosom_selekcja[j][p]
                 chromosom_selekcja[j]=chromosom_selekcja[j][:p] + chromosom_selekcja[j+1][p] +chromosom_selekcja[j][p+1:]
                 chromosom_selekcja[j+1]=chromosom_selekcja[j+1][:p] + zastepczy_char +chromosom_selekcja[j+1][p+1:]

        else:
             continue
        #mutacja
    for j in range(args.chromosom):
        chromosom_selekcja[j]=mutacja(chromosom_selekcja[j])
    suma_przystosowania = 0
    for j in range(args.chromosom):
        chromosom[j]=chromosom_selekcja[j]
        fenotyp[j]=obliczanie_fenotypu(chromosom[j])
        funkcja_przystosowania[j]=obliczanie_funkcji_przystosowania(fenotyp[j]) + anty_minus
        suma_przystosowania = suma_przystosowania + funkcja_przystosowania[j]

    funkcja_przystosowania_max=funkcja_przystosowania[0]
    if max_suma<=suma_przystosowania:
        max_suma=suma_przystosowania
        for j in range(6):
            pula_najlepsza[j] = chromosom[j]
            fenotyp_najlepszy[j]=fenotyp[j]

            if funkcja_przystosowania_max <= funkcja_przystosowania[j]:
                funkcja_przystosowania_max=funkcja_przystosowania[j]
                max_fenotyp = fenotyp[j]
                x=j


print("\n         Wyniki: \n\nPula poczatkowa: \n")
for j in range(args.chromosom):
    print("Chromosom " + str(j+1) + ": " + str(pula_poczatkowa[j]) + " jego fenotyp: " + str(fenotyp_poczatkowy[j]))
print("Pula \"wybrana\": ")
for j in range(6):
    print("Chromosom " + str(j+1) + ": " + str(pula_najlepsza[j]) + " jego fenotyp: " + str(fenotyp_najlepszy[j]) )
print("Maksymalna wartosc funkcji w przedziale: " + str(max_funkcji))
print("Wartosc 'x' dla maksymalnej wartosci: " + str(obliczanie_funkcji_przystosowania(max_fenotyp)))
print("Liczba iteracji: " + str(i+1))
print("Wybrany zostal chromosom o numerze: " + str(x+1) + " "+ str(pula_najlepsza[x]) + " "+ str(fenotyp_najlepszy[x]))


