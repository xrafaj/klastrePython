import random
from collections import defaultdict
import numpy as np
from matplotlib import pyplot as plt
import time
# farby sú napevno, snažil sa vybrať farby, ktoré jednoducho rozlíšiť aby nesplývali
colors = ["lightgray", "magenta",
          "navy", "deepskyblue",
          "teal", "lime",
          "yellow", "darkorange",
          "red", "gray",
          "black", "olive",
          "purple", "brown",
          "lightpink", "moccasin",
          "thistle", "tan",
          "blue", "chocolate"]

start = time.time()


def k_medoids_clustering(full_list, pocet_medoidov):
    medoids = []

    for cc in range(pocet_medoidov):                                        # vytvorenie prvých napr. 20 náhodných medoidov
        rand_index = random.randrange(0, len(full_list), 1)
        medoids.append((full_list[rand_index][0], full_list[rand_index][1]))
    vykresli = 0
    cntr = 0
    zhoda = 0
    prev_medoid = []
    # Vypočítanie počiatočných klastrov pre dané body
    # Najprv kopírujeme pred zmenou predošlé centroidy do prev_centroids, kde neskôr kontrolujeme konvergenciu
    # Potom pre každý bod zistíme vzdialenosť od každého medoidu
    # Do najbližšieho medoidu priradíme bod ( resp. do klastra, ktorému prislúcha daný medoid )
    while 1:
        if cntr != 0:
            prev_medoid = medoids.copy()
        cntr = cntr + 1
        k = defaultdict(list)
        for x in range(len(full_list)):
            distances = []
            min = -1
            min_index = -1
            for cc in range(pocet_medoidov):
                distance = (full_list[x][0]-medoids[cc][0]) ** 2 + (full_list[x][1]-medoids[cc][1]) ** 2
                distance = np.sqrt(distance)
                distances.append(distance)
            for yy in range(len(distances)):
                if min == -1:
                    min = distances[yy]
                    min_index = yy
                elif min > distances[yy]:
                    min = distances[yy]
                    min_index = yy
            k[min_index].append((full_list[x][0], full_list[x][1]))

        # Vykreslenie
        # Vypočítame taktiež aj úspešnosť jednotlivých klastrov.
        # Medoidy označujeme červenými hviezdičkami s bielymi okrajmi.
        if vykresli == 1:
            vzdialenosti_bodov = []
            for kk in range(len(k)):
                sum_vzdialenost = 0
                sum = 0
                for each_item in range(len(k[kk])):
                    sum_vzdialenost = sum_vzdialenost + np.sqrt(
                        (k[kk][each_item][0] - medoids[kk][0]) ** 2 + (k[kk][each_item][1] - medoids[kk][1]) ** 2)
                    sum = sum + 1
                    plt.plot(k[kk][each_item][0], k[kk][each_item][1], c=colors[kk], marker='o')
                if sum > 0:
                    vzdialenosti_bodov.append(sum_vzdialenost / sum)
            chybny_kluster = 0
            for zzz in range(len(vzdialenosti_bodov)):
                if vzdialenosti_bodov[zzz] > 500:
                    chybny_kluster = chybny_kluster + 1
            print('Počet klastrov (klastre s 0 bodmi sem neberiem)')
            print(len(vzdialenosti_bodov))
            print('Počet úspešných klastrov (t.j. vzdialenosť pod 500):')
            print(str(len(vzdialenosti_bodov) - chybny_kluster))
            print('Počet neúspešných klastrov (t.j. vzdialenosť nad 500):')
            print(chybny_kluster)
            counter = 0

            for i in medoids:                                                       # Zakreslenie medoidu, dá sa zakomentovať, ak by prekrývalo značnú časť bodov.
                counter = counter + 1
                plt.plot(i[0], i[1], 'r*', markeredgecolor='white', markersize=10)
                plt.annotate(counter, (i[0], i[1]))

            end = time.time()
            print(end - start)
            plt.show()

            break

        temp_medoids = medoids
        new_medoids = []

        # Počítanie medoidov
        # Medodi sa počíta ako bod, ktorý je od ostatných najmenej vzdialený, obdoba od divizívneho, kde počítame najviac
        # vzdialený bod. V prípade nezmenenia viackrát po sebe je detekovaná konvergencia, čiže cyklus končí
        for iii in range(len(medoids)):
            for j in range(len(temp_medoids)):
                new_medoids.append(temp_medoids[j])                                     # v prípade, že swap nenastal, vyhodíme ten swap akoby
            compute_price = 0
            for each_point in k[iii]:
                compute_price = compute_price + np.sqrt( ( new_medoids[iii][0] - each_point[0] ) ** 2 + ( new_medoids[iii][1] - each_point[1] ) ** 2 )
            if len(k[iii]) != 0:                                                        # v prípade, že tam nič nebolo ideme dalej
                compute_price = compute_price / len(k[iii])
                for each_point in k[iii]:                                               # swapujeme postupne každý bod
                    new_medoids[iii] = each_point
                    price_local = 0                                                     # inicializacia na 0
                    for each_2_point in k[iii]:                                         # vyrátanie hodnoty
                        price_local = price_local + np.sqrt( ( new_medoids[iii][0] - each_2_point[0] ) ** 2 + ( new_medoids[iii][1] - each_2_point[1] ) ** 2 )
                    if len(k[iii]) != 0:                                                # v prípade, že tam nič nebolo ideme dalej
                        price_local = price_local / len(k[iii])
                        if price_local < compute_price :
                            compute_price = price_local                                 # v prípade, že sme našli lepšiu cenu prepíšeme a loopujeme sa dalej ak nenájdeme, tak skok na začiatok
                            temp_medoids[iii] = new_medoids[iii]
        if prev_medoid != temp_medoids:                                                 # zmena -> v poriadku
            medoids = temp_medoids
        else:                                                                           # zhoda -> konverguje ... zrejme
            zhoda = zhoda + 1
        if zhoda == 5:
            vykresli = 1


def k_means_plus(full_list, pocet_k, kreslenie, centroids, append_worst_centroid):

    cntr = 0
    zhoda = 0
    prev_centroid = []
    # Vypočítanie počiatočných klastrov pre dané body
    # Najprv kopírujeme pred zmenou predošlé centroidy do prev_centroids, kde neskôr kontrolujeme konvergenciu
    # Potom pre každý bod zistíme vzdialenosť od každého centroidu
    # Do najbližšieho centroidu priradíme bod ( resp. do klastra, ktorému prislúcha daný centroid )
    while 1:
        if cntr != 0:
            prev_centroid = centroids.copy()
        cntr = cntr + 1
        k = defaultdict(list)
        for x in range(len(full_list)):
            distances = []
            min = -1
            min_index = -1
            for kk in range(pocet_k):
                distance = (full_list[x][0] - centroids[kk][0]) ** 2 + (full_list[x][1] - centroids[kk][1]) ** 2
                distance = np.sqrt(distance)
                distances.append(distance)
            for yy in range(len(distances)):
                if min == -1:
                    min = distances[yy]
                    min_index = yy
                elif min > distances[yy]:
                    min = distances[yy]
                    min_index = yy
            k[min_index].append((full_list[x][0], full_list[x][1]))
        # Počítanie centroidov
        # Centroid sa počíta ako priemer bodov, t.j. súčet všetkých x suradníc deleno ich počet a to isté aj pre y os,
        # kde x a y po delení budú výsledné súradnice centroidu
        # V prípade nezmenenia viackrát po sebe je detekovaná konvergencia, čiže cyklus končí
        for i in range(pocet_k):
            temp_x = 0
            temp_y = 0
            counter_x = 0
            counter_y = 0
            for j in range(len(k[i])):
                temp_x = temp_x + k[i][j][0]
                counter_x = counter_x + 1
                temp_y = temp_y + k[i][j][1]
                counter_y = counter_y + 1
            if len(k[i]) != 0 and counter_x != 0 and counter_y != 0:
                centroids[i] = (temp_x / counter_x, temp_y / counter_y)
        if prev_centroid == centroids:
            zhoda = zhoda + 1
        if zhoda == 5:
            break

    if append_worst_centroid == 1:                                              # v prípade, že chcem nakoniec ešte označiť bod, ktorý je najviac vzdialený od ostatných
        ultimate_max = 0                                                        # toto sa využíva pri divizivne klastrovanie
        ultimate_max_index = -1
        max = -1
        max_bod = (-9999, -9999)
        max_body = []
        max_ceny = []
        for i in range(len(k)):                                                 # zistenie maximálne vzdieleného bodu od všetkých ostatných pre každý klaster
            for j in range(len(k[i])):
                bod = k[i][j]
                cena = 0
                for ii in range(len(k[i])):
                    cena = cena + np.sqrt( ( bod[0] - k[i][ii][0] ) ** 2 + ( bod[1] - k[i][ii][1] ) ** 2 )
                if cena > max:
                    max = cena
                    max_bod = bod
            max_body.append(max_bod)
            max_ceny.append(max)
            max = -1
            max_bod = (-9999, -9999)
        for i in range(len(max_ceny)):                                          # zistenie maxima z maxím klastrov, kde delíme cenu počtom bodov aby to bolo objektívne
            max_ceny[i] = max_ceny[i] / len(k[i])
        for i in range(len(max_ceny)):
            if max_ceny[i] > ultimate_max:
                ultimate_max = max_ceny[i]
                ultimate_max_index = i
        novy_centroid = max_body[ultimate_max_index]
        centroids.append(novy_centroid)
    if kreslenie == 1:                                                          # v prípade, že sa naplní podmienka kreslenia
        vzdialenosti_bodov = []                                                 # tak vypíšeme úpešnosť klasterov na základe ich cien, priemer nesmie byť ako 500
        for kk in range(len(k)):                                                # rovno aj body zakreslíme pomocou plot do plt s ich príslušnou farbou
            sum_vzdialenost = 0
            sum = 0
            for each_item in range(len(k[kk])):
                sum_vzdialenost = sum_vzdialenost + np.sqrt( (k[kk][each_item][0] - centroids[kk][0]) ** 2 + (k[kk][each_item][1] - centroids[kk][1]) ** 2 )
                sum = sum + 1
                plt.plot(k[kk][each_item][0], k[kk][each_item][1], c=colors[kk], marker='o')
            if sum > 0:
                vzdialenosti_bodov.append( sum_vzdialenost / sum )
        chybny_kluster = 0
        for zzz in range(len(vzdialenosti_bodov)):
            if vzdialenosti_bodov[zzz] > 500:
                chybny_kluster = chybny_kluster + 1
        print('Počet klastrov (klastre s 0 bodmi sem neberiem)')
        print(len(vzdialenosti_bodov))
        print('Počet úspešných klastrov (t.j. vzdialenosť pod 500):')
        print(str(len(vzdialenosti_bodov)-chybny_kluster))
        print('Počet neúspešných klastrov (t.j. vzdialenosť nad 500):')
        print(chybny_kluster)
        counter = -1
        for x in centroids:                                                     # Zakreslenie centroidov, dá sa pokojne zakomentovať
            counter = counter + 1
            plt.plot(x[0], x[1], 'r*', markeredgecolor='white', markersize=10)
            plt.annotate(counter ,( x[0], x[1]) )
        end = time.time()
        print(end - start)
        plt.show()
    return centroids


def k_means_clustering(full_list, pocet_k, kreslenie, append_worst_centroid):

    centroids = []

    # Vygenerovanie pôvodných 20 náhodných centroidov / klastrov
    for kk in range(pocet_k):
        tempx = random.randrange(-5000, 5001, 1)
        tempy = random.randrange(-5000, 5001, 1)
        local_tuple = tuple((tempx, tempy))
        centroids.append(local_tuple)

    cntr = 0
    zhoda = 0
    prev_centroid = []
    # Vypočítanie počiatočných klastrov pre dané body
    # Najprv kopírujeme pred zmenou predošlé centroidy do prev_centroids, kde neskôr kontrolujeme konvergenciu
    # Potom pre každý bod zistíme vzdialenosť od každého centroidu
    # Do najbližšieho centroidu priradíme bod ( resp. do klastra, ktorému prislúcha daný centroid )
    while 1:
        if cntr != 0:
            prev_centroid = centroids.copy()
        cntr = cntr + 1
        k = defaultdict(list)
        for x in range(len(full_list)):
            distances = []
            min = -1
            min_index = -1
            for kk in range(pocet_k):
                distance = (full_list[x][0]-centroids[kk][0]) ** 2 + (full_list[x][1]-centroids[kk][1]) ** 2
                distance = np.sqrt(distance)
                distances.append(distance)
            for yy in range(len(distances)):
                if min == -1:
                    min = distances[yy]
                    min_index = yy
                elif min > distances[yy]:
                    min = distances[yy]
                    min_index = yy
            k[min_index].append((full_list[x][0], full_list[x][1]))
        # Počítanie centroidov
        # Centroid sa počíta ako priemer bodov, t.j. súčet všetkých x suradníc deleno ich počet a to isté aj pre y os,
        # kde x a y po delení budú výsledné súradnice centroidu
        # V prípade nezmenenia viackrát po sebe je detekovaná konvergencia, čiže cyklus končí
        for i in range(pocet_k):
            temp_x = 0
            temp_y = 0
            counter_x = 0
            counter_y = 0
            for j in range(len(k[i])):
                temp_x = temp_x + k[i][j][0]
                counter_x = counter_x + 1
                temp_y = temp_y + k[i][j][1]
                counter_y = counter_y + 1
            if len(k[i]) != 0 and counter_x != 0 and counter_y != 0:
                centroids[i] = ( temp_x / counter_x, temp_y / counter_y )
        if prev_centroid == centroids:
            zhoda = zhoda + 1
        if zhoda == 5:
            break

    if append_worst_centroid == 1:                                                      # v prípade, že chcem nakoniec ešte označiť bod, ktorý je najviac vzdialený od ostatných
        ultimate_max = 0                                                                # toto sa využíva pri divizivne klastrovanie
        ultimate_max_index = -1
        max = -1
        max_bod = (-9999, -9999)
        max_body = []
        max_ceny = []
        for i in range(len(k)):                                                         # zistenie maximálne vzdieleného bodu od všetkých ostatných pre každý klaster
            for j in range(len(k[i])):
                bod = k[i][j]
                cena = 0
                for ii in range(len(k[i])):
                    cena = cena + np.sqrt( ( bod[0] - k[i][ii][0] ) ** 2 + ( bod[1] - k[i][ii][1] ) ** 2 )
                if cena > max:
                    max = cena
                    max_bod = bod
            max_body.append(max_bod)
            max_ceny.append(max)
            max = -1
            max_bod = (-9999, -9999)
        for i in range(len(max_ceny)):
            max_ceny[i] = max_ceny[i] / len(k[i])
        for i in range(len(max_ceny)):                                                  # zistenie maxima z maxím klastrov, kde delíme cenu počtom bodov aby to bolo objektívne
            if max_ceny[i] > ultimate_max:
                ultimate_max = max_ceny[i]
                ultimate_max_index = i
        novy_centroid = max_body[ultimate_max_index]
        centroids.append(novy_centroid)
    if kreslenie == 1:                                                                  # v prípade, že sa naplní podmienka kreslenia
        vzdialenosti_bodov = []                                                         # tak vypíšeme úpešnosť klasterov na základe ich cien, priemer nesmie byť ako 500
        for kk in range(len(k)):                                                        # rovno aj body zakreslíme pomocou plot do plt s ich príslušnou farbou
            sum_vzdialenost = 0
            sum = 0
            for each_item in range(len(k[kk])):
                sum_vzdialenost = sum_vzdialenost + np.sqrt( (k[kk][each_item][0] - centroids[kk][0]) ** 2 + (k[kk][each_item][1] - centroids[kk][1]) ** 2 )
                sum = sum + 1
                plt.plot(k[kk][each_item][0], k[kk][each_item][1], c=colors[kk], marker='o')
            if sum > 0:
                vzdialenosti_bodov.append( sum_vzdialenost / sum )
        chybny_kluster = 0
        for zzz in range(len(vzdialenosti_bodov)):                                      # rátanie nevyhovujúcich klastrov
            if vzdialenosti_bodov[zzz] > 500:
                chybny_kluster = chybny_kluster + 1
        print('Počet klastrov (klastre s 0 bodmi sem neberiem)')
        print(len(vzdialenosti_bodov))
        print('Počet úspešných klastrov (t.j. vzdialenosť pod 500):')
        print(str(len(vzdialenosti_bodov)-chybny_kluster))
        print('Počet neúspešných klastrov (t.j. vzdialenosť nad 500):')
        print(chybny_kluster)
        counter = -1
        for x in centroids:                                                         # zakreslenie centroidov, dá sa pokojne zakomentovať
            counter = counter + 1
            plt.plot(x[0], x[1], 'r*', markeredgecolor='white', markersize=10)
            plt.annotate(counter+1 ,( x[0], x[1]) )
        end = time.time()
        print(end - start)                                                          # vyrátame a vypíšeme čas
        plt.show()
    return centroids


def divizivne(k, full_list):                                                        # divizivne klastrovanie
    centroidy = k_means_clustering(full_list, 2, 0, 1)                              # pre prvykrat rozdelime klasicky body na 2 klastre, kde dorobíme ešte jeden 3tí centroid
    for i in range(3, k+1):
        if i == k:
            centroidy = k_means_plus(full_list, i, 1, centroidy, 0)                 # v poslednom kroku nepridáme centroid navyše
        else:
            centroidy = k_means_plus(full_list, i, 0, centroidy, 1)                 # v každom kroku, vyrátame nové klastre a centroidy, pričom pridáme o jeden viac centroid


def main():

    local_list = []
    randomx = random.sample(range(-5000,5001), 20)
    for tt in range(len(randomx)):
        tempy = random.randrange(-5000, 5001, 1)
        local_tuple = tuple((randomx[tt], tempy))
        local_list.append(local_tuple)
    for kk in range(100):
        picked_index = random.randrange(0, len(local_list), 1)
        x_offset = random.randrange(-100, 101, 1)
        y_offset = random.randrange(-100, 101, 1)
        local_list.append(tuple((local_list[picked_index][0]+x_offset, local_list[picked_index][1]+y_offset)))

    pocet_klastrov = 5
    divizivne(pocet_klastrov, local_list)
    #k_means_clustering(local_list, pocet_klastrov, 1, 0)
    #k_medoids_clustering(local_list, pocet_klastrov)


main()