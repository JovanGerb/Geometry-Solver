from time import time, ctime
from itertools import combinations, permutations
from math import gcd
import copy
from collections import defaultdict, Counter



should_it_output_some_interesting_found_things = True
should_it_output_everything_that_it_finds = False
allow_proof_by_contradiction = False
complexity_levels_per_loop = 30


class Bewijs:
    gebruikte_stellingen = defaultdict(int)
    onnodig = defaultdict(int)
    def __init__(self, bewezene, redenen = (), stelling = None, lastigheid=1, triviaal=False):
        #dit bewijs bewijst bewezene, met stelling stelling en gebruikt redenen, een lijst van al bekende dingen.
        if bewezene.toegestaan:
            self.bewezene = bewezene
            self.triviaal = triviaal

            if self.triviaal and len(redenen) == 1 and not isinstance(redenen[0], Hoekenjaging) and not redenen[0].redenen == {"given"}:
                self.stelling = redenen[0].stelling
                self.complexiteit = redenen[0].complexiteit
                self.redenen = redenen[0].redenen
            else:
                self.redenen = set(redenen)
                self.stelling = stelling
                self.complexiteit = sum((reden.complexiteit for reden in self.redenen), start=lastigheid)

            self.gebruik_bewijs()

    def gebruik_bewijs(self):
        tegengestelde_bewijs, bestaand_bewijs = self.bewezene.bewijzen.get(self.bewezene, (None, None)) [:: 2 * self.bewezene.waarheid - 1]
        #Hier zeg ik dat een bewijs ingewikkelder dan de bestaande oplossing niet mag:
        self.nuttig = (bestaand_bewijs == None or bestaand_bewijs.complexiteit > self.complexiteit)
        if self.nuttig:
            self.gebruikt = False

            Bewijs.gebruikte_stellingen[self.stelling, self.bewezene.__class__.__name__] += 1
            if None!= bestaand_bewijs:
                Bewijs.onnodig[bestaand_bewijs.stelling, bestaand_bewijs.bewezene.__class__.__name__] += 1

            self.bewezene.bewijs = self #zo kun je het bewijs later terugvinden als je de stelling self.bewezene hebt.
            self.bewezene.bewijzen[self.bewezene] = (tegengestelde_bewijs, self) [:: 2 * self.bewezene.waarheid - 1] #nu zit het bewezene in de lijst van alle bewezen dingen
            # try:
            Ontdekking.ToDoList[self.complexiteit].append(self.bewezene) #ik moet later het bewezene proberen te gebruiken.
            # except IndexError:
            #     pass
            self.bewezene.triviaal()
            #ook als dit niet een nieuw bewijs is maar een efficienter bewijs, moet ik kijken of dit andere dingen bewijst. (Dit lijkt echter inefficient te kunnen worden.)
            if self.bewezene.waarheid:
                Bewijs.laatste = self #het is leuk om altijd te weten wat als laatste is bewezen

            if allow_proof_by_contradiction:
                if tegengestelde_bewijs != None:
                    self.beschrijf_tegenstelling(tegengestelde_bewijs)
                    raise Exception("done :)")
            else:
                if self.bewezene == objective:
                    self.printen()
                    print(time() - t0, "complexity:", self.complexiteit, "\n")
                    raise Exception("done :)")

    def __eq__(self, other):
        return None != other and self.bewezene.echtgelijk(other.bewezene)

    def __hash__(self):
        return hash((self.bewezene.key, self.bewezene.waarheid))

    def beschrijf_tegenstelling(self, tegengestelde_bewijs):
        for i in self, tegengestelde_bewijs:
            i.printen()
        print("Contradiction")
        print(time() - t0, "complexity:", self.complexiteit + tegengestelde_bewijs.complexiteit, "\n")

    def hele_bewijs(self):
        alles=[]
        for reden in self.redenen:
            alles.append(reden.hele_bewijs())
        alles.sort(key = len, reverse = True)
        return [i for j in alles for i in j] + [self]

    def printen(self):
        nummer = 1
        Bewijs.bewijsnummers = {}
        for bewijs in self.hele_bewijs():
            if bewijs not in Bewijs.bewijsnummers:
                Bewijs.bewijsnummers[bewijs] = nummer
                nummer += 1
                print(bewijs)
        print()

    def nummertje(self):
        return "({:03d})".format(Bewijs.bewijsnummers[self])

    def __str__(self):
        stellingbeschrijving = " because of {}".format(self.stelling) if self.stelling != None else ""
        gebruikte_dingen = " from {}".format( ", ".join(i.nummertje() for i in self.redenen) ) if self.redenen else ""

        return( "{}{!s:45}{:26}{:35}".format(self.nummertje(), self.bewezene, gebruikte_dingen, stellingbeschrijving) )

    def leeg_bewijs(self):
        return Bewijs(self.bewezene, (self,),)

class Ontdekking:
    bewijsefficientie = None

    toegestaan = False
    ToDoList = [[] for _ in range(1000000)]

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.key() == other.key()

    def echtgelijk(self, other):
        return self.key() == other.key() and self.waarheid == other.waarheid

    def __hash__(self):
        return hash(self.key())

    def __bool__(self):
        return self.vind_bewijs() != None

    def triviaal(self):
        pass

    def vind_bewijs(self):
        if self.toegestaan:
            a = (self.bewijzen).get(self, [None, None]) [self.waarheid]
            if a != None and a.gebruikt:
                return a
        return None

    @classmethod
    def allemaal(cls):
        for i in cls.bewijzen.copy().values():
            for j in i:
                if j and j.gebruikt:
                    yield j.bewezene

    @classmethod
    def aantal(cls):
        return sum(len(subcls.bewijzen) for subcls in cls.subclasses)

    def __repr__(self):
        return(str(self.key()))


class Vergelijking(Ontdekking):
    def __init__(self, vergelijking, extra_factor=None, waarheid=True, gesorteerd=False):
        if waarheid == False and (extra_factor!=None and extra_factor != self.gewone_extra_factor and extra_factor != 180):
            self.toegestaan = False
        else:
            #het doel van gesorteerd is om de efficientie te verhogen. gesorteerd betekent dat alle tweetallen punten (soms genaamd lijnstuk) al in de juiste (alfabetische) volgorde staan.
            if gesorteerd:
                verg = [list(vergelijking[0]), list(vergelijking[1])]
            else:
                self.extra_factor = self.gewone_extra_factor
                verg = [[],[]]
                for x in range(2):
                    for y in vergelijking[x]:
                        if y[0] > y[1]:
                            verg[x].append(y[::-1])
                            if isinstance(self, HoekMod360):
                                self.extra_factor += 180
                        else:
                            verg[x].append(y)

            for lijnstuk in verg[0][::-1]:
                if lijnstuk in verg[1]:
                    verg[0].remove(lijnstuk), verg[1].remove(lijnstuk)

            if not gesorteerd:
                self.toegestaan = True #deze check is alleen nodig bij de combineren stap, dus dan is gesorteerd waar
            elif len(verg[0]) > self.max_grootte[waarheid]:
                if len(verg[0]) == 2 and verg[0][0] == verg[0][1] and verg[1][0] == verg[1][1]:
                    self.toegestaan = True
                else:
                    self.toegestaan = False
            elif isinstance(self, HoekMod360) and len(set(verg[0]+verg[1])) > 4:
                self.toegestaan = False
            else:
                self.toegestaan = True

            if self.toegestaan:
                if gesorteerd:
                    self.extra_factor = self.gewone_extra_factor
                self.punten = set(i for k in verg for j in k for i in j)
                if extra_factor!=None:
                    self.extra_factor += extra_factor

                self.grootte = len(verg[0])
                verg[0].sort(), verg[1].sort()
                if verg[0] > verg[1]:
                    verg = verg[::-1]
                    self.extra_factor = -self.extra_factor
                self.vergelijking = tuple(verg[0]), tuple(verg[1])

                if isinstance(self, HoekModx):
                    self.extra_factor %= self.modulus
                self.waarheid = waarheid


    def key(self):
        return (self.vergelijking, self.extra_factor)

    def combineren(self):
        gecombineerd = self.bewijs.stelling == "combining"
        for other in self.allemaal():
            if not (gecombineerd and other.bewijs.stelling == "combining"):
                self.tweecombineren(other)

    def tweecombineren(self, other):
        waarheid = self.waarheid + other.waarheid - 1
        if waarheid == -1:
            return
        otherverg, otherfact = other.vergelijking, other.extra_factor
        if self is other:
            naam = "doubling"
        else:
            naam = "combining"
        for i in range(2):
            if i:
                otherverg = otherverg[::-1]
                otherfact = -otherfact
            non_cancellation = sum(k not in otherverg[1] for k in self.vergelijking[0]) + sum(k not in self.vergelijking[1] for k in otherverg[0])
            if non_cancellation <= max(2, self.max_grootte[waarheid]):
                if isinstance(self, HoekModx):
                    if non_cancellation > 1 or len(self.vergelijking[0])>1 or len(otherverg[0])>1:
                        lastigheid = 10000
                    else:
                        lastigheid = 100
                else:
                    lastigheid = 1

                Bewijs(self.__class__((self.vergelijking[0] + otherverg[0], self.vergelijking[1] + otherverg[1]), self.extra_factor + otherfact, bool(waarheid),  gesorteerd = True), (self.bewijs, other.bewijs), naam, lastigheid)

    def drie_punten(self):
        if len(self.punten) == 3 and self.grootte == 1:
            for i in range(2):
                for j in range(2):
                    if self.vergelijking[0][0][i] == self.vergelijking[1][0][j]:
                        yield self.vergelijking[0][0][i], self.vergelijking[0][0][1-i], self.vergelijking[1][0][1-j], i, j

    def is_teken(self):
        if self.waarheid:
            return "="
        else:
            return"≠"

class HoekModx(Vergelijking):

    gewone_extra_factor = 0

    def vertel(self):
        if self.waarheid and not isinstance(self.bewijs, Hoekenjaging):
            if self.grootte == 1:
                verg = self.vergelijking[0][0], self.vergelijking[1][0]
                fact = self.extra_factor
                for i in range(2):
                    if i:
                        verg = verg[::-1]
                        fact *= -1
                    self.lijnen[verg[0]].append(((verg[1], fact), self.bewijs))
                    if verg[0] < verg[1]:
                        self.abs_hoeken[verg].append((fact, self.bewijs))

            for hoeken in self.echte_hoeken():
                factor = self.extra_factor
                for i in range(2):
                    if i:
                        hoeken = hoeken[::-1]
                        factor *= -1
                    if hoeken[0][0] > hoeken[0][1]:
                        hoeken = hoeken[0][::-1], hoeken[1][::-1]
                        factor *= -1
                    self.hoeken[hoeken[0]].append(((hoeken[1], factor), self.bewijs))

    def hoekenjaag(self):
        if self.waarheid and not isinstance(self.bewijs, Hoekenjaging):
            for hoeken in self.echte_hoeken():
                Hoekenjaging(hoeken, (0, self.extra_factor), (self.bewijs,), self.__class__)
                Hoekenjaging.jaag()
            if self.grootte == 1:
                for extra in combinations(Punt.allemaal(), 2):
                    if (extra,) not in self.vergelijking:
                        Hoekenjaging(((self.vergelijking[0][0], extra), (self.vergelijking[1][0], extra)), (0, self.extra_factor), (self.bewijs,), self.__class__)
                        Hoekenjaging.jaag()


    def echte_hoeken(self):
        if self.grootte == 2:
            for i in range(2):
                yield (self.vergelijking[0][0], self.vergelijking[1][i]), (self.vergelijking[1][1-i], self.vergelijking[0][1])

    #dit gaat alleen over output
    def als_echte_hoeken(self):
        #dit is om de output leesbaarder te maken
        if self.grootte == 2:
            hoeken = []
            verg = self.vergelijking

            for i in range(2):
                for k in range(2):
                    for l in range(2):
                        if verg[0][0][k] == verg[1][i][l]:

                            for m in range(2):
                                for n in range(2):
                                    if verg[0][1][m] == verg[1][1-i][n]:

                                        optelling = (self.extra_factor + 180 * (k+l+m+n)) % self.modulus
                                        if optelling != 0:
                                            a = " + {}".format(optelling)
                                        else:
                                            a = ""
                                        yield "<{}{}{} {} <{}{}{}{}".format(verg[0][0][1-k], verg[0][0][k], verg[1][i][1-l],
                                        self.is_teken(), verg[1][1-i][1-n], verg[1][1-i][n], verg[0][1][1-m], a)

                if verg[0][0] == verg[0][1] or verg[1][0] == verg[1][1]:
                    break

    def __str__(self):
        if self.extra_factor % 1 == 0 and type(self.extra_factor) == float:
            self.extra_factor = int(self.extra_factor)
        if self.grootte == 1 and isinstance(self, HoekMod180):
            if self.extra_factor == 0:
                return "{}{}||{}{}{}".format(*self.vergelijking[0][0], *self.vergelijking[1][0], " doesn't hold" * (not self.waarheid))
            if self.extra_factor == 90:
                return "{}{} and {}{} are{} perpendicular".format(*self.vergelijking[0][0], *self.vergelijking[1][0], " not" * (not self.waarheid))


        hoeken = " / ".join(set(self.als_echte_hoeken()))
        if hoeken:
            return "{} mod {}".format(hoeken, self.modulus)
        else:
            verg = [[],[]]
            for i in range(2):
                for lijn, n in Counter(self.vergelijking[i]).items():
                    a = "<{}{}".format(*lijn)
                    if n!=1:
                        a = "{}*{}".format(n,a)
                    verg[i].append(a)
            if self.extra_factor != 0:
                verg[1].append("{}°".format(self.extra_factor))
            for i in range(2):
                if verg[i]:
                    verg[i] = " + ".join(verg[i])
                else:
                    verg[i] = "0°"
            return "{0} {3} {1} mod {2}".format(*verg, self.modulus, self.is_teken())

class Hoekenjaging(Bewijs):
    stelling = "anglehunting"
    triviaal = False

    def __init__(self, vergelijking, extra_factoren, redenen_geordend, soort, waarheid=True):
        #extra_factoren[0] is altijd 0

        #ik kan vergelijking op 4 manieren schrijven en dan zijn extra_factoren telkens anders, maar dat maakt niet uit.
        # if sorted(vergelijking[0]) > sorted(vergelijking[-1]):
        #     #achterstevoren
        #     vergelijking = vergelijking[::-1]
        #     extra_factoren =  extra_factoren[::-1]
        #     redenen = redenen[::-1]
        #
        # if vergelijking[0][0] > vergelijking[0][1]:
        #     vergelijking = (hoek[::-1] for hoek in vergelijking)
        #     extra_factoren = (-factor for factor in extra_factoren)
        self.vergelijking = tuple(vergelijking)
        self.extra_factoren = tuple(extra_factoren)#((factor - extra_factoren[0]) % 180 for factor in extra_factoren))
        self.redenen_geordend = tuple(redenen_geordend)
        self.soort = soort
        self.modulus = self.soort.modulus
        if len(self.redenen_geordend) != 1:
            self.redenen = set((i for reden in self.redenen_geordend for i in reden.redenen))
            self.complexiteit = sum((reden.complexiteit for reden in self.redenen_geordend))

            nieuwe_verg = [[],[]]
            for i in self.vergelijking[0], self.vergelijking[-1][::-1]:
                if i:
                    nieuwe_verg[0].append(i[0]), nieuwe_verg[1].append(i[1])
            self.bewezene = self.soort(nieuwe_verg, self.extra_factoren[-1] - self.extra_factoren[0], gesorteerd = True)
            if self.bewezene.grootte < bool(self.vergelijking[0]) + bool(self.vergelijking[-1]):
                self.complexiteit += 1
            self.gebruik_bewijs()

        if len(self.redenen_geordend) == 1 or self.nuttig:
            self.te_jagen.append(self)

    te_jagen = []
    nummer = 0
    @classmethod
    def jaag(cls):
        for i in cls.te_jagen:
            i.uitbreiden()
        cls.te_jagen = []

    def uitbreiden(self):
        verg, extra_factoren, redenen_geordend = list(self.vergelijking), list(self.extra_factoren), list(self.redenen_geordend)

        for j in range(2):
            if j:
                verg.reverse(), extra_factoren.reverse(), redenen_geordend.reverse()

            if verg[-1]:
                if verg[-1][0] > verg[-1][1]:
                    verg = [k[::-1] for k in verg]
                    extra_factoren = [-k for k in extra_factoren]

                #evenwijdige lijnen gebruiken, F/Z hoeken
                for i in range(2):
                    for (otherverg, otherfact), bewijs in self.soort.lijnen[verg[-1][i]]:
                        nieuwe_verg = (otherverg, verg[-1][1-i])
                        if nieuwe_verg[0] != nieuwe_verg[1]:
                            if i:
                                nieuwe_verg = nieuwe_verg[::-1]
                            if nieuwe_verg not in verg:
                                Hoekenjaging(verg + [nieuwe_verg], extra_factoren + [extra_factoren[-1] + otherfact], redenen_geordend + [bewijs], self.soort)
                #hoeken uitdrukken in graden
                for otherfact, bewijs in self.soort.abs_hoeken[verg[-1]]:
                    if () not in verg:
                        Hoekenjaging(verg + [()], extra_factoren + [extra_factoren[-1] + otherfact], redenen_geordend + [bewijs], self.soort)
                #hoeken die gelijk zijn gelijk stellen
                for (otherverg, otherfact), bewijs in self.soort.hoeken[verg[-1]]:
                    if otherverg not in verg:
                        Hoekenjaging(verg + [otherverg], extra_factoren + [extra_factoren[-1] + otherfact], redenen_geordend + [bewijs], self.soort)

            else:
                #een hoek in graden gelijkstellen aan een hoek
                for otherverg, a in self.soort.abs_hoeken.copy().items():
                    for otherfact, bewijs in a:
                        for i in (1,-1):
                            if otherverg[::i] not in verg:
                                Hoekenjaging(verg + [otherverg[::i]], extra_factoren + [extra_factoren[-1] + otherfact * i], redenen_geordend + [bewijs], self.soort)

    def hoekje(self, I):# hoek, factor):
        #dit is voor printen
        text = []
        hoek = self.vergelijking[I]
        if hoek:
            if len(set(hoek[0]) | set(hoek[1])) == 3:
                for i in range(2):
                    for j in range(2):
                        if hoek[0][i]==hoek[1][j]:
                            text.append("<{}{}{}".format(hoek[0][1-i], hoek[0][i], hoek[1][1-j]))
                            if (i+j)%2:
                                self.extra_factoren[I] += 180
            elif len(set(hoek[0]) | set(hoek[1])) == 4:
                text.append("<({}{}, {}{})".format(*hoek[0], *hoek[1]))

        factor = (self.extra_factoren[I] - self.extra_factoren[0]) % self.modulus
        if factor != 0:
            if type(factor) == float and factor % 1 == 0:
                factor = int(factor)
            text.append("{}°".format(factor))
        if not text:
            text.append("0°")
        return " + ".join(text).ljust(15)

    def __str__(self):
        extra_factoren = list(self.extra_factoren)
        hoeken = [[] for _ in range(len(self.vergelijking))]

        for i in range(len(self.vergelijking)):
            hoek = self.vergelijking[i]
            if hoek:
                if len(set(hoek[0]) | set(hoek[1])) == 3:
                    for j in range(2):
                        for k in range(2):
                            if hoek[0][j]==hoek[1][k]:
                                hoeken[i].append("<{}{}{}".format(hoek[0][1-j], hoek[0][j], hoek[1][1-k]))
                                if (j+k)%2:
                                    extra_factoren[i] += 180

                if len(set(hoek[0]) | set(hoek[1])) == 4:
                    hoeken[i].append("<({}{}, {}{})".format(*hoek[0], *hoek[1]))

        extra_factoren = [(factor - extra_factoren[0]) % self.modulus for factor in extra_factoren]
        for i in range(len(self.vergelijking)):
            factor = extra_factoren[i]
            if factor != 0:
                if type(factor) == float and factor % 1 == 0:
                    factor = int(factor)
                hoeken[i].append("{}°".format(factor))
            if not hoeken[i]:
                hoeken[i].append("0°")
        hoeken = [" + ".join(hoek).ljust(15) for hoek in hoeken]

        begin = "{} {}".format(self.nummertje(), hoeken[0])
        rest = []
        for i in range(1, len(self.vergelijking)):
            bewijs = self.redenen_geordend[i-1]

            stellingbeschrijving = " because of {}".format(bewijs.stelling) if bewijs.stelling != None else ""
            gebruikte_dingen = " from {}".format( ", ".join(i.nummertje() for i in bewijs.redenen) ) if bewijs.redenen else ""
            rest.append("= {}(mod {})   {:26}{}".format(hoeken[i], self.modulus, gebruikte_dingen, stellingbeschrijving))
        self.extra_factoren = tuple(self.extra_factoren)
        return begin + ("\n" + " "*len(begin)).join(rest)

class HoekMod180(HoekModx):
    bewijzen = {}
    hoeken = {}

    modulus = 180
    max_grootte = (1, 2)

    hoeken = defaultdict(list)
    abs_hoeken = defaultdict(list)
    lijnen = defaultdict(list)

    def bewijs_nieuws(self):
        self.drie_op_lijn()
        self.koordenvierhoek()
        self.vertel()
        self.hoekenjaag()
        self.verdubbelen()
        self.halveren()
        self.combineren()

    def drie_op_lijn(self):
        if self.grootte==1 and len(self.punten)==3:
            if self.extra_factor == 0:
                Bewijs(Lijn(self.punten, waarheid = self.waarheid), (self.bewijs,), "three points on a line")#, triviaal=True)
            elif self.waarheid == True:
                Bewijs(Lijn(self.punten, waarheid = False), (self.bewijs,), "three points on a line")#, triviaal=True)
            #wil ik inderdaad dat deze tussenstap overgeslagen wordt in het bewijs?

    def koordenvierhoek(self):
        if (len(self.punten) == 4 and self.grootte == 2 and self.extra_factor == 0
            and len(set(self.vergelijking[0][0] + self.vergelijking[0][1])) == 4
            and len(set(self.vergelijking[1][0] + self.vergelijking[1][1])) == 4):

            onhandig = any(Lijn(puntjes).vind_bewijs() for puntjes in combinations(self.punten, 3))
            if not onhandig:
                Bewijs(Cirkel(tuple(self.punten), middelpunt=None, waarheid=self.waarheid), (self.bewijs,), "cyclic angles")

                for TB in (Lijn(puntjes, waarheid=False).vind_bewijs() for puntjes in combinations(self.punten, 3)):
                    if TB:
                        Bewijs(Cirkel(tuple(self.punten), middelpunt=None, waarheid=self.waarheid), (self.bewijs, TB), "cyclic angles")


    def verdubbelen(self):
        if self.grootte == 1 and self.waarheid:
            a = Bewijs(HoekMod360([i*2 for i in self.vergelijking], self.extra_factor*2, self.waarheid, gesorteerd=True), (self.bewijs,), "doubling", 1000)

    def halveren(self):
        if not self.waarheid and self.grootte >= 2 and self.extra_factor == 0:
            if all(sorted(i[::2]*2) == list(i) for i in self.vergelijking):
                Bewijs(HoekMod180([i[::2] for i in self.vergelijking], waarheid=False), (self.bewijs,), "halving")

class HoekMod360(HoekModx):
    bewijzen = {}

    modulus = 360
    max_grootte = (1,4)

    hoeken = defaultdict(list)
    abs_hoeken = defaultdict(list)
    lijnen = defaultdict(list)

    def triviaal(self):
        self.mod180()

    def bewijs_nieuws(self):
        self.halveren()
        self.gericht_op_lijn()
        self.vertel()
        self.hoekenjaag()
        self.combineren()

        # self.middelpuntomtrekshoek()

    def halveren(self):
        if self.waarheid:
            if all(sorted(i[::2]*2) == list(i) for i in self.vergelijking):
                Bewijs(HoekMod180([i[::2] for i in self.vergelijking], self.extra_factor/2, self.waarheid), (self.bewijs,), "halving")

    def mod180(self):
        if self.waarheid:
            Bewijs(HoekMod180(self.vergelijking, self.extra_factor), (self.bewijs,), "taking it mod 180", triviaal=True)

    def gericht_op_lijn(self):
        if self.waarheid:
            for A, B, C, i, j in self.drie_punten():
                if self.extra_factor == 180 * ((i+j-1) % 2):
                    Bewijs(Lijn((B, A, C), volgorde=True), (self.bewijs,), "three points on a line")

    @classmethod
    def ingeschreven_cirkel(cls):
        TB=[0,0,0]
        for A,B in combinations(Punt.allemaal(), 2):
            for C in Punt.allemaal():
                TB[0] = Lijn((A,B,C), waarheid=False).vind_bewijs()
                if TB[0]:
                    for I in Punt.allemaal():
                        TB[1] = HoekMod360(( ((A,I),(A,I)), ((A,B),(A,C)) )).vind_bewijs()
                        TB[2] = HoekMod360(( ((B,I),(B,I)), ((B,A),(B,C)) )).vind_bewijs()
                        if TB[1] and TB[2]:
                            Bewijs(HoekMod360(( ((C,I),(C,I)), ((C,A),(C,B)) )), TB, "the inscribed circle")
                            for _ in range(3):
                                Bewijs(HoekMod180(( ((A,B),(C,I)), ((A,I),(B,I)) ), 90), TB, "the inscribed circle")
                                A,B,C = B,C,A

class Breuk(tuple):
    def __new__(cls, a=1, b=1):
        ggd = gcd(a,b)
        return tuple.__new__(cls, (a//ggd, b//ggd))
    def __neg__(self):
        return Breuk(*self[::-1])
    def __add__(self, other):
        return Breuk(*(self[i]*other[i] for i in range(2)))

class Verhouding(Vergelijking):
    bewijzen = {}
    max_grootte = (3,3)
    gewone_extra_factor = Breuk()

    def bewijs_nieuws(self):
        self.vind_cirkel()
        self.machtlijn()
        self.combineren()
        self.bissectricestelling()

    def vind_cirkel(self):
        if self.waarheid and self.extra_factor == Breuk():
            for O, A, B, _ , _ in self.drie_punten():
                Bewijs(Cirkel((A,B), O), (self.bewijs,), "isosceles triangle")
                Bewijs(HoekMod360((((O,A), (O,B)), ((A,B), (A,B))), 180), (self.bewijs,), "isosceles triangle")

    def machtlijn(self):
        if self.waarheid and self.extra_factor == Breuk():
            for O, A, B, _ , _ in self.drie_punten():
                Bewijs(Lijn((O,), machtcirkels=(A,B)), (self.bewijs,), "equal distance")

    def bissectricestelling(self):
        s = self.vergelijking
        if (len(self.punten) == 4 and self.grootte == 2 and self.extra_factor == Breuk()
            and len(set(s[0][0] + s[0][1])) == 4 and len(set(s[1][0] + s[1][1])) == 4):

            sets = set(s[0][0]), set(s[1][0]), set(s[0][1]), set(s[1][1])
            (A,), (B,), (C,), (D,) = sets[0]&sets[1], sets[1]&sets[2], sets[2]&sets[3], sets[3]&sets[0]

            Bewijs(HoekMod360(( ((A,B), (B,C), (C,D), (D,A)), ((A,C), (A,C), (B,D), (B,D)) ), 180, self.waarheid), (self.bewijs,), "the genalized angle bisector theorem", lastigheid=2)
            for i in range(4):
                TB = Lijn((B,C,D)).vind_bewijs()
                if TB:
                    Bewijs(HoekMod180(( ((A,B), (A,D)), ((A,C), (A,C))) ), (self.bewijs, TB), "the angle bisector theorem")
                A,B,C,D = B,C,D,A

    # @classmethod
    # def verhouding_omrekenen(cls):
    #     for verh in list(cls.bewijzen):
    #         for A, B, C, _ , _ in verh.drie_punten():
    #             ene, andere = HoekMod360(( ((A,B),), (A,C) ), 180), HoekMod360(( ((A,B),), (A,C) ), 0)
    #             if ene:
    #                 som = verh.extra_factor[0] + verh.extra_factor[1]
    #                 Verhouding(( ((A,B)), (B,C)), Breuk(verh.extra_factor[0], som), bewijs=Bewijs({verh, ene}, "verhouding omrekenen"))
    #                 Verhouding(( ((A,C)), (B,C)), Breuk(verh.extra_factor[1], som), bewijs=Bewijs({verh, ene}, "verhouding omrekenen"))
    #             elif andere:
    #                 versch = abs(verh.extra_factor[0] - verh.extra_factor[1])
    #                 Verhouding(( ((A,B)), (B,C)), Breuk(verh.extra_factor[0], versch), bewijs=Bewijs({verh, andere}, "verhouding omrekenen"))
    #                 Verhouding(( ((A,C)), (B,C)), Breuk(verh.extra_factor[1], versch), bewijs=Bewijs({verh, andere}, "verhouding omrekenen"))
    #                 a=1 if verh.extra_factor[0] < verh.extra_factor[1] else -1
    #                 Lijn((A,) + (B,C)[::a], volgorde=True, bewijs=Bewijs({verh, andere}, "lengte/configuratie"))

    def __str__(self):
        verg = [[],[]]
        for i in range(2):
            if self.extra_factor[i] != 1:
                verg[i].append(str(self.extra_factor[i]))
            for lijn in self.vergelijking[i]:
                verg[i].append("|{}{}|".format(*lijn))
        return "{} {} {}".format(' * '.join(verg[0]), self.is_teken(), ' * '.join(verg[1]))


class Cirkel(Ontdekking):
    bewijzen = {}
    max_punten = 6

    def __init__(self, punten, middelpunt=True, volgorde=False, waarheid=True):
        if volgorde:
            #ik zet de punten op volgorde, waarbij de geometrische volgorde hetzelfde blijft
            self.punten = punten
            for _ in range(2):
                for _ in range(len(punten)):
                    if punten < self.punten:
                        self.punten = punten
                    punten = punten[1::] + (punten[0],)
                punten = punten[::-1]
        else:
            self.punten = frozenset(punten)
        self.waarheid = waarheid
        self.middelpunt = middelpunt #middelpunt is None, True of een punt. Als het None is, kan de cirkel ook een lijn zijn
        self.volgorde = volgorde
        self.toegestaan = True

    def key(self):
        return (self.punten, self.middelpunt, self.volgorde)

    def triviaal(self):
        self.zonder_dingen()
        self.kleinere_cirkel()

    def bewijs_nieuws(self):
        self.grotere_cirkel()
        self.kvh_stelling()
        self.middelpunt_omtrek()
        self.configuratie()

    def kvh_stelling(self):
        if len(self.punten) == 4:
            A,B,C,D = self.punten
            if self.volgorde == True:
                A,B,C,D = self.punten
                Bewijs(HoekMod360(( ((A,B), (C,D)), ((A,C), (B,D)) ), waarheid = self.waarheid), (self.bewijs,), "adjacent cyclic angles")
                Bewijs(HoekMod360(( ((A,D), (B,C)), ((A,C), (B,D)) ), waarheid = self.waarheid), (self.bewijs,), "adjacent cyclic angles")

                Bewijs(HoekMod360(( ((A,B), (C,D)), ((A,D), (B,C)) ), waarheid = self.waarheid), (self.bewijs,), "opposite cyclic angles")
            else:
                for _ in range(3):
                    Bewijs(HoekMod180(( ((A,B), (C,D)), ((A,C), (B,D)) ), waarheid = self.waarheid), (self.bewijs,), "cyclic angles")
                    A,B,C,D = A,C,D,B

    def middelpunt_omtrek(self):
        if len(self.punten) == 3 and isinstance(self.middelpunt, Punt):
            A,B,C = self.punten
            O = self.middelpunt
            for _ in range(3):
                Bewijs(HoekMod180(( ((O,A), (B,C)), ((A,B), (A,C))), 90, waarheid = self.waarheid), (self.bewijs,), "the central angle theorem")
                A,B,C = B,C,A
                #dit is de versie waarbij ik meteen hoekensom driehoek gedaan heb in de gelijkbenige driehoek.
                #Dit bevat ook meteen de raaklijn-omtrekshoekstelling.

    def kleinere_cirkel(self):
        if self.waarheid:
            minste_punten = 3 if isinstance(self.middelpunt, Punt) else 4

            for aantal_punten in range(minste_punten, len(self.punten)):
                for punten in combinations(self.punten, aantal_punten):
                    Bewijs(Cirkel(punten, self.middelpunt, self.volgorde), (self.bewijs,), triviaal=True)

    def grotere_cirkel(self):
        if self.waarheid and isinstance(self.middelpunt, Punt):
            for other in self.allemaal():
                if other.waarheid and other.middelpunt == self.middelpunt and set(self.punten) & set(other.punten):
                    Bewijs(Cirkel(set(self.punten) | set(other.punten), self.middelpunt), (self.bewijs, other.bewijs), "same midpoint and radius")

    def zonder_dingen(self):
        if self.waarheid and len(self.punten) >= 4:
            if self.middelpunt != None:
                Bewijs(Cirkel(self.punten, None, self.volgorde), (self.bewijs,), triviaal=True)
                if self.middelpunt != True:
                    Bewijs(Cirkel(self.punten, True, self.volgorde), (self.bewijs,), triviaal=True)

        if self.waarheid:
            Bewijs(Cirkel(self.punten, self.middelpunt, False), (self.bewijs,), triviaal=True)

    def configuratie(self):
        if self.waarheid and self.middelpunt != None:
            for A,B,C in combinations(self.punten, 3):
                Bewijs(Lijn((A,B,C), waarheid = False), (self.bewijs,), "the configuration")

    @classmethod
    def Thales(cls):
        TB = [0,0,0]
        for A,B in combinations(Punt.allemaal(), 2):
            for O in Punt.allemaal():
                TB[0] = Lijn((A,B,O)).vind_bewijs()
                if TB[0]:
                    TB[1] = Verhouding(( ((A,O),), ((B,O),) )).vind_bewijs()
                    if TB[1]:
                        for C in Punt.allemaal():
                            TB[2] = HoekMod180(( ((A,C),),((B,C),) ), 90).vind_bewijs()
                            if TB[2]:
                                Bewijs(cls((A,B,C), O), TB, "Thales")

    def __str__(self):

        return "{}{} lie {}on a{} circle{}".format(", ".join(str(punt) for punt in self.punten), " don't" * (not self.waarheid), "in that order " * self.volgorde,
        " true" * (self.middelpunt==True), " with midpoint {}".format(self.middelpunt) * isinstance(self.middelpunt, Punt))

    def beschrijving(self):
        mid = ", with midpoint {}".format(self.middelpunt) if isinstance(self.middelpunt, Punt) else ""
        return "the circle through {}{}".format(", ".join(str(punt) for punt in self.punten), mid)

class Lijn(Ontdekking):
    bewijzen = {}
    machtlijnen = defaultdict(list)

    def __init__(self, punten, machtcirkels=None, volgorde=False, waarheid=True):
        if volgorde:
            self.punten = min(punten, punten[::-1])
        else:
            self.punten = frozenset(punten)
        self.toegestaan = len(self.punten) >= 3 or machtcirkels != None
        if self.toegestaan:
            self.waarheid = waarheid
            self.volgorde = volgorde
            self.machtcirkels = None if machtcirkels==None else frozenset(machtcirkels)

    def key(self):
        return(self.punten, self.machtcirkels, self.volgorde)

    def triviaal(self):
        self.verkort()
        if self.machtcirkels != None:
            self.zonder_macht()

    def bewijs_nieuws(self):
        self.per_definitie()
        self.verleng()

        if self.machtcirkels != None:
            self.zelfde_machtlijn()
            self.vertel()
            self.loodrecht()
            self.gelijke_lengte()

    def per_definitie(self):
        if self.waarheid or len(self.punten) == 3:
            #er geldt evenwijdigheid tussen lijnstukken op dezelfde lijn
            for i,j in combinations(combinations(self.punten, 2), 2):
                if self.volgorde and self.waarheid:
                    Bewijs(HoekMod360(((i,), (j,))), (self.bewijs,), "points ordered on a line")
                    #de punten in i en j staan al op de goede volgorde om de mod360 variant te doen
                else:
                    Bewijs(HoekMod180(((i,), (j,)), waarheid = self.waarheid), (self.bewijs,), "points on a line")

    def verleng(self):
        if self.waarheid:
            for other in Lijn.allemaal():
                if other.waarheid and len(set(self.punten) & set(other.punten)) >= 2:
                    punten = set(self.punten) | set(other.punten)
                    for cirkels in self.machtcirkels, other.machtcirkels:
                        Bewijs(Lijn(punten, cirkels), (self.bewijs, other.bewijs), "the same line")
    def verkort(self):
        if self.waarheid:
            min = 3 if self.machtcirkels==None else 1
            for n in range(min, len(self.punten)):
                for punten in combinations(self.punten, n):
                    Bewijs(Lijn(punten, self.machtcirkels, self.volgorde), (self.bewijs,), triviaal=True)

    def zelfde_machtlijn(self):
        if self.waarheid:
            for other in Lijn.machtlijnen[self.machtcirkels]:
                Bewijs(Lijn(set(self.punten) | set(other.punten), self.machtcirkels), (self.bewijs, other.bewijs), "the same radical axis")

    def vertel(self):
        if self.waarheid:
            self.machtlijnen[self.machtcirkels].append(self)

    def zonder_macht(self):
        if self.waarheid and len(self.punten) >= 3:
            Bewijs(Lijn(self.punten, volgorde=self.volgorde), (self.bewijs,), triviaal=True)

    def loodrecht(self):
        if self.waarheid:
            #ik wil ook het omgekeerde van deze stelling hebben
            middens = []
            for i in self.machtcirkels:
                if isinstance(i, Punt):
                    middens.append(i)
                else:
                    a = i.middelpunt
                    if isinstance(a, Punt):
                        middens.append(a)
                    else:
                        return
            for A,B in combinations(self.punten, 2):
                name = "bisector" if all(isinstance(i, Punt) for i in self.machtcirkels) else " radical axis"
                Bewijs(HoekMod180((((A,B),), (tuple(middens),)), 90), (self.bewijs,), "the perpendicular {}".format(name))

    def gelijke_lengte(self):
        if self.waarheid:
            if all(isinstance(P, Punt) for P in self.machtcirkels):
                for A in self.punten:
                    Bewijs(Verhouding([((A, P),) for P in self.machtcirkels]), (self.bewijs,), "perpendicular bisector")

    def __str__(self):
        if self.machtcirkels == None:
            return "{}{} lie{} on a line".format(", ".join(str(punt) for punt in self.punten)," don't" * (not self.waarheid), " in that order" * self.volgorde)
        else:
            meervoud = "lies" if len(self.punten) == 1 else "lie"

            figuur = "perpendicular bisector" if all(isinstance(i, Punt) for i in self.machtcirkels) else "radical axis"

            cirkels = []
            for i in self.machtcirkels:
                if isinstance(i, Punt):
                    cirkels.append(i)
                else:
                    cirkels.append(i.beschrijving)
            return "{} {}{}{} on the {} of {} and {}".format(", ".join(str(punt) for punt in self.punten), meervoud,
            " not" * (not self.waarheid), " in that order" * self.volgorde, figuur, *cirkels)

class Gelijkvormigheid(Ontdekking):
    bewijzen = {}

    def __init__(self, driehoeken, orientatie=None, waarheid=True):
        self.driehoeken = tuple(min( sorted( tuple(driehoeken[i][j] for j in order) for i in range(2) ) for order in permutations(range(3)) ))
        #ik sorteer de letters van de driehoeken
        self.orientatie = orientatie
        self.waarheid = waarheid

        if self.orientatie == None:
            (A, B, C) , (D, E, F) = self.driehoeken
            for _ in range(3):
                if A == D and B == E and C != F:
                    self.orientatie = False
                A,B,C = B,C,A
                D,E,F = E,F,D

        self.toegestaan = True


    def key(self):
        return (self.driehoeken, self.orientatie)

    def triviaal(self):
        self.zonder_orientatie()

    def bewijs_nieuws(self):
        if self.waarheid:
            #self.vertel_orientatie()
            #self.vind_orientatie()
            self.hoeken_en_verhoudingen()

    def hoeken_en_verhoudingen(self):
        #de hoeken en verhoudingen die volgen uit de gelijkvormigheid
        (A,B,C) , (D,E,F) = self.driehoeken
        for _ in range(3):
            Bewijs(Verhouding(( ((A,B),(D,F)), ((A,C),(D,E)) )), (self.bewijs,), "similarity")
            if self.orientatie == True:
                Bewijs(HoekMod360(( ((A,B), (D,F)), ((A,C), (D,E)) )), (self.bewijs,), "similarity")
            elif self.orientatie == False:
                Bewijs(HoekMod360(( ((A,B), (D,E)), ((A,C), (D,F)) )), (self.bewijs,), "similarity")
            A,B,C = B,C,A
            D,E,F = E,F,D

    def zonder_orientatie(self):
        if self.orientatie != None:
            Bewijs(Gelijkvormigheid(self.driehoeken), (self.bewijs,), triviaal=True)

    @staticmethod
    def driehoektweetallen():
        for (A,B,C), DEF in combinations(combinations(Punt.allemaal(), 3), 2):
            for D,E,F in permutations(DEF):
                yield A,B,C,D,E,F

    @classmethod
    def gelijkvormig_vinden(cls):
        for A,B,C,D,E,F in cls.driehoektweetallen():
            z, h, gelukt = [], [[], []], False
            for _ in range(3):
                z.append(Verhouding(( ((A,B), (D,F)), ((A,C), (D,E)) )).vind_bewijs())
                for i in range(2):
                    h[i].append(HoekMod180(( ((A,B), (D,E)), ((A,C), (D,F)) )).vind_bewijs())
                    E,F = F,E

                A,B,C = B,C,A
                D,E,F = E,F,D
            #hh
            if Lijn((A,B,C), waarheid=False) and not Lijn((A,B,C), waarheid=True):
                for i in range(2):
                    if all(h[i]):
                        for lijn in Lijn((A,B,C), waarheid=False), Lijn((D,E,F), waarheid=False):
                            TB = lijn.vind_bewijs()
                            if TB == None:
                                continue
                            for a,b in combinations(h[i], 2):
                                Bewijs(cls(((A,B,C), (D,E,F)), orientatie=bool(i)), (a, b, TB), "(AA) similarity")
                                gelukt = True

            #zhz
            for j in range(3):
                for i in range(2):
                    if h[i][j] and z[j]:
                        #zhz
                        if i:
                            TB = HoekMod360(( ((A,B), (D,F)), ((A,C), (D,E)) )).vind_bewijs()
                        else:
                            TB = HoekMod360(( ((A,B), (D,E)), ((A,C), (D,F)) )).vind_bewijs()

                        if TB:
                            Bewijs(cls(((A,B,C), (D,E,F)), bool(i)), (z[j], TB), "(SAS) similarity")
                        #zrz
                        elif h[1-i][j] and not gelukt:
                            TB = HoekMod180(( ((A,B),), ((A,C),) ), 90).vind_bewijs(), HoekMod180(( ((D,E),), ((D,F),) ), 90).vind_bewijs()
                            if all(TB):
                                Bewijs(cls(((A,B,C), (D,E,F))), (z[j], TB[0], TB[1]), "(SRS) similarity")
                                gelukt = True
                A,B,C = B,C,A
                D,E,F = E,F,D

            #zzr
            for i in range(3):
                for j in range(3):
                    if i!=j:
                        if z[j] and h[0][i] and h[1][i]:
                            TB = HoekMod180(( ((A,B),), ((A,C),) ), 90).vind_bewijs(), HoekMod180(( ((D,E),), ((D,F),) ), 90).vind_bewijs()
                            if all(TB):
                                Bewijs(cls(((A,B,C), (D,E,F))), (z[j], TB[0], TB[1]), "(SSR) similarity")
                A,B,C = B,C,A
                D,E,F = E,F,D

            #zzz
            if all(z):
                for a,b in combinations(z, 2):
                    Bewijs(cls(((A,B,C), (D,E,F))), (a,b), "(SSS) gelijkvomigheid")

            #zzh/sinusregel
            for j in range(3):
                if z[j]:
                    for k, hoeken in enumerate(([(((A,B), (E,F)), ((B,C), (D,E))), (((A,C), (D,F)), ((B,C), (E,F)))], [(((A,B), (D,E)), ((B,C), (E,F))), (((A,C), (E,F)), ((B,C), (D,F)))])):
                        for i in range(2):
                            if h[(k+i+1)%2][(j+i+1)%3]:
                                TB = HoekMod360(hoeken[i], 180).vind_bewijs()
                                if TB:
                                    Bewijs(HoekMod360(hoeken[1-i]), (TB, z[j]), "the sine rule")
                A,B,C = B,C,A
                D,E,F = E,F,D
            #verkeerde hh/sinusregel
            if Lijn((A,B,C), waarheid=False) and not Lijn((A,B,C), waarheid=True):
                for k,i,j in permutations(range(3)):
                    if h[0][i] and h[1][j]:
                        A2,B2,C2 = [A,B,C][k:] + [A,B,C][:k]
                        D2,E2,F2 = [D,E,F][k:] + [D,E,F][:k]
                        for lijn in Lijn((A,B,C), waarheid=False), Lijn((D,E,F), waarheid=False):
                            if lijn.vind_bewijs() == None:
                                continue
                            Bewijs(Verhouding(( ((A2,B2), (D2,F2)), ((A2,C2), (D2,E2)) )), (h[0][i], h[1][j], lijn.vind_bewijs()), "the sine rule", lastigheid = 3)
                            # de lastigheid moet groot genoeg zijn dat deze stelling niet wordt gebruikt in plaats van (hh) geliujkvormigheid




    def __str__(self):
        return "▲{}{}{} ~ ▲{}{}{}, with {} orientation{}".format(*self.driehoeken[0], *self.driehoeken[1],
            {None:"unknown", False:"opposite", True:"equal"} [self.orientatie], ", doesn't hold" * (not self.waarheid))

Ontdekking.subclasses = (HoekMod180, HoekMod360, Verhouding, Lijn, Cirkel, Gelijkvormigheid)#, Driehoekorientatie)

class Punt(int):
    getallen, namen = {}, {}
    #deze dictionaries gaan van puntnamen naar getallen en andersom.
    aantal = 0

    def __new__(cls, getal):
        return int.__new__(cls, getal)

    def __eq__(self, other):
        return type(other)==Punt and int(self) == int(other)

    def __hash__(self):
        return hash(int(self))

    @classmethod
    def introduceer(cls):
        aantal += 1
        return cls(aantal-1)

    @classmethod
    def allemaal(cls):
        return (Punt(i) for i in range(cls.aantal))

    def __str__(self):
        try:
            # ik kijk of er al een naam bedacht is voor dit punt
            return self.namen[self]
        except:
            # ik maak een nieuwe naam die nog geen ander punt heeft.
            accenten = 0
            while True:
                for letter in range(26):
                    naam = chr(65 + letter) + "'" * accenten
                    if naam not in self.getallen:
                        self.definieer_naam(naam)
                        #ik onthoudt dat deze nieuwe naam hoort bij dit punt met de functie definieer_naam
                        return naam
                accenten += 1

    def definieer_naam(self, naam):
        self.namen[self] = naam
        self.getallen[naam] = self

for getal, naam in enumerate(input("Which points are in the diagram? ").split()):
    Punt(getal).definieer_naam(naam)
Punt.aantal = len(Punt.namen)
if Punt.aantal == 0:
    raise Exception("You didn't input anything :(")

def verwerk(tekst):
    for i in [' ', '=', '+', '*', '|', ';', ':', ',']:
        if i in tekst:
            return tuple((verwerk(j) for j in tekst.split(i) if j!=''))
    try:return Punt.getallen[tekst]
    except:
        return eval(tekst)

print()
x = input("What shall I prove? ")
if x:
    soort, *args = verwerk(x)
    if allow_proof_by_contradiction:
        Bewijs(soort(*args, waarheid=False), stelling = "given")
    else:
        objective = soort(*args)

while True:
    print()
    inp = input("give me a given: ")
    if inp!="":
        soort,*args = verwerk(inp)
        Bewijs(soort(*args), stelling = "given")
    else:
        break


def DoeToDo():
    non_empties = []
    for ontdekkingen in Ontdekking.ToDoList:
        if ontdekkingen:
            non_empties.append(ontdekkingen)
            if len(ontdekkingen) == complexity_levels_per_loop:
                break
    if not non_empties:
        raise Exception("couldn't solve the problem")
    for ontdekkingen in non_empties:
        for ontdekking in ontdekkingen:
            if not ontdekking.vind_bewijs(): #checking that this is the first time working with this ontdekking
                ontdekking.bewijs.gebruikt = True
                if should_it_output_everything_that_it_finds:
                    print(ontdekking)#, ontdekking.bewijs.complexiteit)
                elif should_it_output_some_interesting_found_things:
                    # if not ontdekking.bewijs.triviaal and (isinstance(ontdekking, Cirkel) or isinstance(ontdekking, Gelijkvormigheid) or (isinstance(ontdekking, Lijn) and ontdekking.machtcirkels!=None)):
                    if (isinstance(ontdekking, Cirkel) or isinstance(ontdekking, Gelijkvormigheid) or isinstance(ontdekking, Lijn)):
                        print(ontdekking)#, ontdekking.bewijs.complexiteit)
                ontdekking.bewijs_nieuws()
        ontdekkingen.clear()



stellingen = (Gelijkvormigheid.gelijkvormig_vinden, Cirkel.Thales, HoekMod360.ingeschreven_cirkel)

t0 = time()
print(ctime(t0))
DoeToDo()

aantal_bewezen, nieuw_aantal_bewezen = -1, Ontdekking.aantal()
while True:
    print(time() - t0)

    for stelling in stellingen:
        stelling()
    DoeToDo()
    aantal_bewezen, nieuw_aantal_bewezen = nieuw_aantal_bewezen, Ontdekking.aantal()


print(time()-t0)

'''
A B C E F M O Q
Verhouding E,Q*=F,Q*
Lijn B,M,C
Lijn Q,E,F
Lijn A,B,E
Lijn A,C,F
Lijn O,M,A
Lijn Q,B,C
HoekMod180 E,F+=Q,O+ 90
HoekMod180 A,B+=B,O+ 90
Verhouding M,B+=M,C+
Verhouding A,B+=A,C+


'''
#Ibero America 4
'''
A B C D E F G P Q
HoekMod180 G,D+F,C=D,F+D,C
Lijn G,A,P,Q,B None True
Cirkel A,E,F,B,C,D True True
HoekMod180 A,B+=C,D+
Verhouding A,P+=Q,B+
Lijn C,P,E
Lijn C,Q,F
Lijn G,E,F


'''
#Ibero America 3
'''
A B C D E P Q M J X Y Z
Verhouding  Y,B*P,Z*Q,C=B,P*Z,Q*C,Y
Cirkel A,B,C,D,E,Y
HoekMod180 A,C+=B,D+
HoekMod180 A,B+=C,E+
Lijn A,B,P
Lijn C,D,P
Lijn A,C,Q
Lijn B,E,Q
Lijn E,M,D None True
Verhouding E,M*=D,M*
Lijn A,M,Y,J
Lijn P,J,Q,Z
Cirkel B,C,J,Z
Lijn B,Q,X
Lijn C,P,X


'''
'''
A B C D
Cirkel A,B,C,D True  True
Verhouding A,B*=A,D*
Verhouding C,B*=C,D*
Cirkel A,B,C,D


'''
#EGMO 4
'''
A B C I D E F A'
Lijn B,C,A'
Lijn A,B,C None False False
HoekMod360 A,I+A,I=A,B+A,C
HoekMod360 B,I+B,I=B,A+B,C
Lijn B,C,D
Lijn B,I,F
Lijn C,I,E
HoekMod180 D,F+=C,I+ 90
HoekMod180 D,E+=B,I+ 90
Verhouding A,E*=A',E*
Verhouding A,F*=A',F*


'''
#EGMO 3
'''
A B C D E F H M N X Y
Cirkel E,F,M,N,D,H
Lijn A,B,C None False False
Lijn B,E,Y,H
Lijn C,F,X,H
Lijn A,B,X
Lijn A,C,Y
HoekMod180 A,B+=C,F+ 90
HoekMod180 A,C+=B,E+ 90
Lijn A,E,F
HoekMod360 A,E+A,E=A,B+A,C 180
Lijn C,E,M
Lijn B,F,N
HoekMod180 A,C+E,M=A,M+B,C
HoekMod180 A,B+F,N=A,N+B,C
Cirkel A,B,N,D
Cirkel A,C,M,D


'''

'''
A B C D E F H X Y
Cirkel E,F,D,H
Lijn A,B,C None False False
Lijn B,E,Y,H
Lijn C,F,X,H
Lijn A,B,X
Lijn A,C,Y
HoekMod180 A,B+=C,F+ 90
HoekMod180 A,C+=B,E+ 90
Lijn A,E,F
HoekMod360 A,E+A,E=A,B+A,C 180
HoekMod180 A,C+C,D=A,D+B,C
HoekMod180 A,B+B,D=A,D+B,C


'''
#EGMO 1 2022
'''
A B C P Q T H S
Lijn T,H,S
Lijn A,B,C None False False
Lijn A,P,B
Lijn A,Q,C
Verhouding B,C*=B,Q*
Verhouding B,C*=P,C*
Verhouding T,A*=T,P*
Verhouding T,A*=T,Q*
HoekMod180 A,B+=C,H+ 90
HoekMod180 A,C+=B,H+ 90
Lijn B,S,Q
Lijn C,S,P


'''
#Joe
'''
A B C P Q
HoekMod180 A,Q+A,P=A,B+A,C
Lijn A,B,C None False False
Lijn P,B,C None False False
HoekMod180 A,B+A,C=B,P+C,P
HoekMod180 P,B+=Q,C+
HoekMod180 P,C+=B,Q+


'''
#Joe 2
'''
A B C D E F
HoekMod180 E,F+C,D+C,B=D,F+A,C+E,C
Lijn A,B,C
Cirkel A,B,D,E
HoekMod180 A,C+B,C=D,C+E,C
HoekMod180 D,F+A,B=D,A+D,B
HoekMod180 E,F+A,B=E,A+E,B


'''
# IMO 4 2022
'''
A B C D E T P Q R S
Cirkel P,S,Q,R
Verhouding T,B*=T,D*
Verhouding T,C*=T,E*
Verhouding B,C*=D,E*
HoekMod180 A,B+A,E=T,B+T,E
Lijn C,D,P
Lijn C,T,Q
Lijn C,D,R
Lijn D,T,S
Lijn P,B,A,Q
Lijn R,E,A,S
HoekMod360 T,E+T,B=T,D+T,C



'''
# EGMO 2 2023
'''
A B C D H K L O
Lijn K,L,H
Cirkel A,B,D,C True True
Lijn A,K,B None True
Lijn A,L,C None True
Verhouding A,O*=B,O*
Verhouding A,O*=C,O*
Verhouding A,O*=D,O*
Lijn A,O,D
HoekMod180 A,B+=C,H+ 90
HoekMod180 A,C+=B,H+ 90
HoekMod180 B,C+=A,H+ 90
HoekMod180 D,L+A,K=A,L+K,L
HoekMod180 D,K+A,L=A,K+K,L



'''
# lemma 7 (i)
'''
A B C I P E D
Lijn D,E,P
Lijn A,B,C None False False
Lijn A,E,C None True
Lijn B,D,C None True
Verhouding A,E+=E,C+
Verhouding B,D+=D,C+
HoekMod360 A,I+A,I=A,B+A,C
HoekMod360 B,I+B,I=B,A+B,C
HoekMod360 C,I+C,I=C,A+C,B
Lijn A,I,P
HoekMod180 A,P+=C,P+ 90


'''
# lemma 7 (ii)
'''
A B C D F I P
Lijn D,F,P
Lijn A,B,C None False False
Lijn A,B,F
Lijn D,B,C
Lijn A,I,P
HoekMod180 A,P+=C,P+ 90
HoekMod360 A,I+A,I=A,B+A,C
HoekMod360 B,I+B,I=B,A+B,C
HoekMod360 C,I+C,I=C,A+C,B
HoekMod180 I,D+=B,C+ 90
HoekMod180 I,F+=A,B+ 90


'''