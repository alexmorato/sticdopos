# T08. Anàlisi del test MADAMES

## 1. Abast de l'anàlisi

S'han analitzat les **123 preguntes** de
[`T08_MADAMES.json`](../../../assets/python/madames/T08_MADAMES.json).

La característica principal d'aquest banc és que **no conté 123 conceptes
diferents**. Hi ha molts grups de preguntes que repeteixen el mateix concepte amb
canvis d'ordre, negacions, distractors o una formulació aparentment nova.

Per aquest motiu, la part més útil no és memoritzar cada test, sinó identificar:

1. **el bloc del temari**;
2. **l'article o norma aplicable**;
3. **la formulació literal que es repeteix**;
4. **la negació o excepció que converteix la pregunta en trampa**.

## 2. Distribució per blocs del temari

La classificació següent assigna cada pregunta a **un únic bloc principal**.
No es comptabilitzen dos cops les preguntes que toquen més d'un tema; per exemple,
una pregunta sobre competències adquirides per la via de l'article 151 s'assigna
al bloc competencial si el que demana és el sostre de competències.

| Bloc principal | Preguntes | Percentatge | Lectura de la mostra |
|---|---:|---:|---|
| **8.1. Procés i configuració de l'Estat autonòmic** | 76 | 61,8 % | Domini absolut: principis, territori, vies, iniciatives, casos particulars i relacions interadministratives |
| **8.3. Òrgans i control** | 24 | 19,5 % | Parlament, President, Consell de Govern, circumscripció, TSJ, art. 153/155 i institucions de cooperació |
| **8.4. Competències** | 17 | 13,8 % | Articles 148/149/150, cultura, sistema monetari, cinc anys, prevalença i supletorietat |
| **8.2. Estatuts d'autonomia** | 6 | 4,9 % | Naturalesa, contingut de l'article 147.2, aprovació i reforma |
| **Total** | **123** | **100 %** |  |

> **Conclusió de prioritat:** en aquest banc convé prioritzar el **procés
> autonòmic i les vies d'accés**, especialment els articles 143, 144, 151 i les
> disposicions transitòries. La resta de blocs requereix menys volum, però
> concentra distractors literals molt repetits.

## 3. Distribució per famílies de pregunta

Els blocs anteriors s'han subdividit en famílies primàries, que sí sumen 123
preguntes:

| Família | Preguntes | Identificadors del banc | Percentatge |
|---|---:|---|---:|
| **Vies, iniciativa i procediment d'accés** | 45 | 3, 6, 7, 10, 13, 14, 17, 20, 23, 25-27, 29, 35, 36, 39, 41, 42, 47, 51, 55, 56, 62, 66, 69, 71, 72, 74, 80, 81, 88, 89, 91, 94-97, 103, 105, 111, 112, 116-118, 122 | 36,6 % |
| **Òrgans autonòmics** | 20 | 16, 19, 24, 44, 49, 57, 59-61, 65, 67, 77, 79, 85, 92, 100, 107, 114, 120, 123 | 16,3 % |
| **Competències i regles de tancament** | 17 | 1, 2, 11, 12, 22, 30, 33, 37, 53, 63, 70, 82, 83, 93, 102, 106, 110 | 13,8 % |
| **Principis, territori i mapa autonòmic** | 16 | 4, 5, 9, 18, 21, 31, 34, 38, 40, 43, 50, 73, 99, 109, 113, 119 | 13,0 % |
| **Cooperació i relacions entre administracions** | 15 | 8, 28, 45, 46, 48, 52, 64, 68, 75, 78, 84, 98, 104, 108, 115 | 12,2 % |
| **Estatuts d'autonomia** | 6 | 15, 58, 87, 90, 101, 121 | 4,9 % |
| **Control dels articles 155 i controls institucionals** | 4 | 32, 54, 76, 86 | 3,3 % |

## 4. Blocs i preguntes més repetits

### 4.1. Vies d'accés: el gran eix del banc

És la família més extensa: **45 de 123 preguntes (36,6 %)**. Es pregunta amb
variants sobre:

- via ordinària o comuna de l'article 143.2;
- via especial o reforçada de l'article 151.1;
- procediment estatutari de l'article 151.2;
- llei orgànica i clàusula de tancament de l'article 144;
- disposició transitòria segona per a Catalunya, País Basc i Galícia;
- disposició addicional primera per a Navarra;
- disposició transitòria cinquena per a Ceuta i Melilla;
- casos de Madrid, Andalusia, Segòvia, Múrcia i territoris amb entitat regional
  històrica.

#### Repeticions prioritàries

| Repetició conceptual | Quantitat detectada | Dada clau |
|---|---:|---|
| Andalusia com a resposta a preguntes sobre via especial o històrica | 6 aparicions | Andalusia és l'única comunitat que va completar la via de l'article 151.1 |
| Article 143.2 i les seves majories | Almenys 4 formulacions | Totes les diputacions/òrgans interinsulars + dues terceres parts dels municipis |
| Referèndum en la via especial | 2 formulacions | En el sistema de l'article 151, el projecte passa per referèndum; no existeix una alternativa sense referèndum |
| Termini de la iniciativa de la via ordinària | 2 formulacions | Sis mesos des del primer acord |
| Termini d'examen de la Comissió Constitucional | 2 formulacions literals + variants | Dos mesos |
| CCAA per disposició transitòria segona | 2 formulacions negades i una amb Navarra | Catalunya, País Basc i Galícia; no Navarra |
| Article 144 i Corts Generals per llei orgànica | 4 formulacions o més | La intervenció estatal compleix la clàusula de tancament i requereix llei orgànica |
| Convocatòria/autoconstitució de l'assemblea estatutària | 2 contextos | Via ordinària i via especial han d'estudiar-se per separat |
| Accés o Estatuts de Ceuta/Melilla | 4 formulacions | Article 144 i disposició transitòria cinquena |
| Cas Segòvia | 2 formulacions | Aplicació de l'article 144.c per motius d'interès nacional |

#### Quadre de vies que cal dominar

| Via o supòsit | Norma | Territori o exemple | Competències o característica |
|---|---|---|---|
| Via ordinària | Art. 143.2 CE | Majoria de comunitats | Inici amb dotació competencial inicial de l'article 148 |
| Via especial o reforçada | Art. 151.1 CE | Andalusia | Majories qualificades i referèndum; màxim sostre competencial inicial |
| Via històrica transitòria | DT 2a CE | Catalunya, País Basc i Galícia | Règims preautonòmics + plebiscits històrics; tramitació de l'article 151.2 |
| Intervenció per interès nacional | Art. 144.a-c CE | Madrid, Ceuta/Melilla en els supòsits corresponents, Segòvia en la substitució d'iniciativa | Corts Generals mitjançant llei orgànica |
| Navarra | DA 1a CE + LO 13/1982 | Comunitat Foral de Navarra | Règim foral i consolidació del règim d'autogovern |
| Ceuta i Melilla | DT 5a i art. 144 CE | Ciutats autònomes | Els seus Estatuts tenen una forma pròpia; no segueixen exactament el model institucional general |

### 4.2. Òrgans autonòmics

Són **20 preguntes** dedicades a:

- unicameralitat de l'Assemblea Legislativa;
- representació proporcional i circumscripció provincial;
- President: elecció, nomenament pel Rei, representació i responsabilitat;
- Consell de Govern: composició, naturalesa col·legiada, potestat executiva i
  reglamentària;
- exclusió de la sanció i promulgació com a funció pròpia del Consell;
- TSJ dins el poder judicial únic;
- Conferència de Presidents;
- Consell Econòmic i Social;
- comissions territorials de coordinació.

#### Respostes literals repetides

- **President:** elegit per l'Assemblea entre els seus membres i **nomenat pel
  Rei**.
- **Assemblees legislatives:** cambres parlamentàries **unicamerals**.
- **Circumscripció electoral autonòmica:** la **província**, com a regla general.
- **Consell de Govern:** no sanciona ni promulga les lleis com si fos el President.
- **TSJ:** integra el poder judicial, **comú i general per a tot l'Estat**.
- **Article 152.1:** no preveu representació majoritària de l'Assemblea, sinó
  **proporcional**.

### 4.3. Competències: menys preguntes, més risc

La família competencial conté **17 preguntes** i combina memòria literal,
terminis i interpretació:

- cinc anys per a l'ampliació de competències de les comunitats de via comuna;
- article 148.1 com a llista mínimament assumible;
- article 149.1 i competències estatals;
- sistema monetari com a competència exclusiva estatal;
- cultura a l'article 149.2 com a servei essencial de l'Estat, sense impedir la
  competència autonòmica;
- prevalença, residualitat i supletorietat de l'article 149.3;
- llei d'harmonització com a llei ordinària especial, no llei orgànica.

#### Repeticions

| Concepte repetit | Resposta o regla |
|---|---|
| Via lenta i ampliació | Cinc anys + reforma estatutària |
| Sistema monetari | Competència exclusiva de l'Estat, art. 149.1.11 CE |
| Cultura | Art. 149.2 CE |
| Supletorietat | Dret estatal supletori del dret autonòmic |
| Clàusula residual | Les matèries no assumides es poden atribuir a l'Estat segons l'article 149.3 |
| Llei d'harmonització | Lleis ordinàries; la regla d'aprovació incorporada a l'art. 150.3 exigeix apreciació prèvia per majoria absoluta |

### 4.4. Estatuts d'autonomia

Només hi ha **6 preguntes primàries**, però tres conceptes són molt literalitzats:

1. L'article 147.2 **no exigeix el procediment d'investidura del President**.
2. Els Estatuts **no són aprovats exclusivament per l'assemblea legislativa
   autonòmica**.
3. Els Estatuts de la via ordinària requereixen la intervenció i aprovació de les
   **Corts Generals**.

Els quatre elements de l'article 147.2 que cal memoritzar són:

1. denominació de la comunitat;
2. delimitació territorial;
3. denominació, organització i seu de les institucions;
4. competències assumides i bases per al traspàs dels serveis.

### 4.5. Principis, territori i mapa autonòmic

Són **16 preguntes** basades en dades curtes i formulacions directes:

- Títol VIII;
- municipis, províncies i comunitats autònomes;
- 17 comunitats autònomes;
- autonomia com a dret, no com a deure;
- independència entre autonomia i sobirania;
- garantia estatal de la solidaritat;
- Fons de Compensació Interterritorial;
- igualtat de tots els espanyols;
- prohibició de federació de comunitats.

### 4.6. Cooperació i relacions interadministratives

Són **15 preguntes**, però moltes són variacions de:

- **col·laboració:** deure d'actuar amb altres administracions per assolir
  finalitats comunes;
- **cooperació:** compromisos específics, voluntaris i en nom d'una acció comuna;
- **principi de competència** com a criteri ordenant;
- **subministrament d'informació** com a forma de fer efectiu el deure de
  col·laboració;
- **convenis entre comunitats:** no necessiten autorització de les Corts en tot
  cas;
- **Conferència de Presidents** com a òrgan multilateral de cooperació de màxim
  nivell.

Norma principal: **Llei 40/2015, especialment els articles 140 i següents sobre
relacions interadministratives**.

## 5. Tècniques de trampa més utilitzades

### 5.1. Canviar una sola categoria

Exemples:

- 143 en lloc de 151;
- 2/3 en lloc de totes les diputacions;
- comunitat autònoma en lloc de ciutat autònoma;
- llei orgànica en lloc de llei ordinària;
- representació majoritària en lloc de proporcional.

### 5.2. Formular la pregunta en negatiu

Expressions com:

- «quin no és correcte?»;
- «indica l'afirmació falsa»;
- «quin territori no...»;
- «no s'inclou...»;
- «no és una llei orgànica».

En aquestes preguntes, la resposta correcta és sovint **l'opció que, sense el
“no”, seria falsa**.

### 5.3. Intercanviar el titular d'una funció

- El Rei nomena el President autonòmic.
- El President, no el Consell de Govern com a òrgan, sanciona i promulga les
  lleis autonòmiques per delegació constitucional.
- L'Assemblea legisla i elegeix el President.
- Les Corts Generals aproven l'Estatut a través del procediment corresponent.

### 5.4. Confondre control ordinari i control excepcional

- **Article 153:** controls jurídics, administratius i pressupostaris.
- **Article 155:** mecanisme polític excepcional.
- El Senat intervé en l'article 155 mitjançant **majoria absoluta**.

## 6. Repeticions que cal convertir en flashcards

| Davant | Darrere |
|---|---|
| Títol d'organització territorial | Títol VIII |
| Fórmula territorial | Municipis + províncies + CCAA que es constitueixin |
| Nombre de CCAA | 17, més Ceuta i Melilla com a ciutats autònomes |
| Autonomia | Dret reconegut, no deure |
| Iniciativa via 143.2 | Totes les diputacions/òrgans insulars + 2/3 dels municipis |
| Termini de la iniciativa | 6 mesos |
| Via ordinària | Art. 143.2 i inicialment competències de l'art. 148 |
| Via especial | Art. 151.1; Andalusia |
| Via catalana | Disposició transitòria 2a |
| Ampliació competencial de la via lenta | 5 anys + reforma de l'Estatut |
| Comissió Constitucional, via especial | 2 mesos |
| Reforma territorial estatutària | Corts + procediment aplicable + llei orgànica |
| Parlament autonòmic | Unicameral |
| Sistema electoral | Representació proporcional; província com a circumscripció general |
| President autonòmic | Nomenat pel Rei |
| Poder judicial | Únic per a tot l'Estat |
| Art. 153 | TC + Govern en competències delegades + contenciós + Tribunal de Comptes |
| Art. 155 | Requeriment + majoria absoluta del Senat |
| Art. 149.1.4 | Defensa i forces armades |
| Art. 149.1.11 | Sistema monetari |
| Art. 149.2 | Servei de la cultura |
| Art. 149.3 | Residualitat + prevalença + supletorietat |
| Llei d'harmonització | Ordinària, amb apreciació prèvia de necessitat per majoria absoluta |

## 7. Articles i lleis que concentren el banc

### Constitució Espanyola

| Precepte | Funció en el banc |
|---|---|
| Art. 2 | Unitat, autonomia i solidaritat |
| Art. 137 | Organització territorial |
| Art. 138 | Principi de solidaritat i igualtat econòmica |
| Art. 139 | Igualtat de drets, circulació i establiment |
| Arts. 143 i 144 | Vies d'accés ordinària i casos particulars |
| Art. 145 | Prohibició de federació de comunitats |
| Arts. 146, 147 i 151.2 | Elaboració, naturalesa, contingut i reforma dels Estatuts |
| Arts. 148 i 149 | Repartiment competencial i tancament |
| Art. 150 | Lleis marc, transferència/delegació i harmonització |
| Art. 152.1 | Assemblea, Consell, President i TSJ |
| Arts. 153 i 155 | Controls ordinaris i control excepcional |
| Art. 158.2 | Fons de Compensació Interterritorial |
| DT 2a | Via històrica de Catalunya, País Basc i Galícia |
| DT 5a | Ceuta i Melilla |
| DA 1a | Drets històrics dels territoris forals |

### Lleis relacionades

- **Llei 40/2015, d'1 d'octubre, de règim jurídic del sector públic:**
  col·laboració, cooperació, conferències, comissions i instruments
  interadministratius.
- **Llei Orgànica 13/1982:** reintegració i millorament del règim foral de
  Navarra.
- **Llei 22/2001, de 27 de desembre, reguladora dels Fons de Compensació
  Interterritorial.**
- **Estatuts d'autonomia de les diferents comunitats:** organització
  institucional, funcions i competències concretes.

## 8. Precaucions amb la font

MADAMES és útil per detectar fórmules d'examen, però algunes raons abreujades
no substitueixen la interpretació tècnica:

1. **La clàusula competencial és l'article 149.3 CE**, no l'article 149.1.3.
   Alguns textos del banc es refereixen a ella amb una numeració abreujada o
   confusa.
2. La **supletorietat no autoritza l'Estat a legislar en una matèria sense títol
   competencial**. Actua quan el dret estatal té títol propi i el dret
   autonòmic presenta una llacuna que ha de cobrir-se.
3. Els articles 148 i 149 **no són simples llistes rígides**: cal distingir tota
   la matèria, legislació bàsica, potestat legislativa, execució i regulació
   organitzativa.
4. Les respostes sobre “via lenta” i “via ràpida” expliquen el model inicial;
   la posterior evolució i homogenització estatutària fa que la simplificació
   històrica s'hagi d'utilitzar només com a context.
5. Quan aparegui «Ceuta i Melilla» en una pregunta sobre l'article 152.1, cal
   recordar que els seus Estatuts tenen una configuració singular.

## 9. Pla d'estudi recomanat

1. **Fer primer una fitxa exclusiva de vies:** articles 143, 144, 151 i
   disposicions transitòries 2a i 5a.
2. **Fer un quadre de territoris:** Catalunya, País Basc, Galícia, Andalusia,
   Navarra, Madrid, Segòvia, Ceuta i Melilla.
3. **Memoritzar les dades numèriques:** 17 CCAA, 6 mesos, 5 anys, 2 mesos,
   2/3 dels municipis, 3/4 de municipis en la iniciativa reforçada.
4. **Repasar l'article 147.2 com una llista tancada de quatre punts**.
5. **Separar 152, 153 i 155 en tres fitxes:** institució, controls ordinaris i
   control excepcional.
6. **Practicar totes les preguntes negatives** independentment de l'ordre i
   indicar prèviament si l'enunciat parla d'una excepció.
7. **Agrupar les repeticions:** no respondre cada variant com si fos nova.

## 10. Conclusió

El rendiment de l'estudi sobre MADAMES millorarà sobretot si es treballen dos
mapes visuals:

1. **Mapa de vies d'accés i territoris:** resol aproximadament una de cada tres
   preguntes del banc.
2. **Mapa 148/149/150 i òrgans 152/153/155:** resol els distractors més tècnics.

La prioritat pràctica és:

1. vies d'accés i iniciatives;
2. òrgans autonòmics;
3. competències i clàusules de tancament;
4. principis i territori;
5. cooperació;
6. Estatuts.