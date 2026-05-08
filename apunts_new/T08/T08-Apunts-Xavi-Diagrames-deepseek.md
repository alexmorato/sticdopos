A continuació et presento diversos diagrames **Mermaid** que resumeixen els conceptes clau del Tema 8 sobre l'Estat autonòmic. Cada diagrama va precedit d'un petit text explicatiu per situar-lo dins del temari.

---

## 1. Principis de l'Estat autonòmic

Aquest diagrama mostra els principals principis que regeixen l'Estat autonòmic segons la Constitució Espanyola (CE) i la jurisprudència constitucional. El principi d'**unitat** n'és el fonament, mentre que l'**autonomia**, la **solidaritat**, la **cooperació** i la **igualtat** actuen com a principis articuladors que permeten conciliar la diversitat territorial amb la indissoluble unitat de la nació espanyola.

```mermaid
flowchart TD
    A["Principis de l'Estat autonòmic"]
    
    subgraph Unitat ["Unitat (Art. 2 CE)"]
        direction TB
        B1["Sobirania nacional"]
        B2["Unitat de l'ordenament jurídic"]
        B3["Unitat econòmica i mercat nacional"]
    end
    
    subgraph Autonomia ["Autonomia (Art. 137, 143 CE)"]
        direction TB
        C1["Autonomia política (CCAA)"]
        C2["Autonomia administrativa (ens locals)"]
        C3["Límits: no sobirania, control de legalitat"]
    end
    
    subgraph Solidaritat ["Solidaritat (Art. 2, 138, 158 CE)"]
        direction TB
        D1["Equilibri interterritorial"]
        D2["Fons de Compensació"]
    end
    
    subgraph Cooperacio ["Cooperació (Arts. 145, 154 CE)"]
        direction TB
        E1["Lleialtat institucional"]
        E2["Conferències sectorials"]
        E3["Convenis de col·laboració"]
    end
    
    subgraph Igualtat ["Igualtat (Art. 139 CE)"]
        direction TB
        F1["Igualtat de drets i obligacions"]
        F2["Lliure circulació"]
    end
    
    A --> Unitat
    Unitat --> Autonomia
    Autonomia --> Solidaritat
    Solidaritat --> Cooperacio
    Cooperacio --> Igualtat
```

---

## 2. Vies d'accés a l'autonomia (classificació de Comunitats Autònomes)

Aquest diagrama organitza les diferents **vies d'accés** a l'autonomia que estableix la CE, mostrant quines Comunitats o territoris van seguir cada via. Inclou tant la “via lenta” (art. 143.2 CE) com la “via ràpida” (art. 151.1 CE i disposició transitòria 2a), així com els casos especials de Madrid per Llei Orgànica (art. 144.a CE) i les singularitats de Navarra, Ceuta i Melilla.

```mermaid
flowchart LR
    subgraph Vies_accés
        direction LR
        A[Via lenta<br>Art. 143.2 CE] --> B[13 CCAA:<br>Astúries, Cantàbria, Aragó,<br>Castella i Lleó, La Rioja,<br>Comunitat Valenciana,<br>Castella-la Manxa, Múrcia,<br>Extremadura, Balears, Canàries]
        C[Via ràpida] --> D[Art. 151.1 CE<br>Andalusia]
        C --> E[DT 2a CE<br>Catalunya, País Basc, Galícia]
        F[Art. 144.a CE<br>Llei Orgànica] --> G[Comunitat de Madrid]
        H[Supòsits especials] --> I[Disp. Add. 1a + LO 13/82<br>Navarra - règim foral]
        H --> J[Art. 144.b CE<br>Ceuta i Melilla<br>Ciutats Autònomes]
    end
```

---

## 3. Procés d'elaboració dels Estatuts d'Autonomia

L'elaboració de l'Estatut d'Autonomia és l'últim pas perquè un territori es converteixi en Comunitat Autònoma. Aquest diagrama diferencia els tres supòsits previstos a la CE: el **general** (art. 146 CE) per a la via lenta, l’**especial** (art. 151.2 CE) per a la via ràpida, i el **particular** de la disposició transitòria 2a (que de fet aplica el procediment especial). Es visualitzen els òrgans que intervenen i la necessitat de referèndum en la via especial.

```mermaid
flowchart TD
    Inici[Inici del procés autonòmic] --> General{Supòsit general<br>Art. 146 CE}
    Inici --> Especial{Supòsit especial<br>Art. 151.2 CE}
    Inici --> Particular[Supòsit particular<br>DT 2a CE]
    
    General --> Assemblea1[Assemblea de parlamentaris:<br>Diputacions + Diputats/Senadors]
    Assemblea1 --> Projecte1[Projecte d'Estatut]
    Projecte1 --> Corts1[Corts Generals<br>tramiten com a LO]
    Corts1 --> EA1[Estatut aprovat]
    
    Especial --> Assemblea2[Assemblea de parlamentaris]
    Assemblea2 --> Comissió[Comissió Constitucional<br>+ delegació de l'assemblea]
    Comissió --> Acord{Hi ha acord?}
    Acord -- Sí --> Referèndum1[Referèndum<br>al territori]
    Acord -- No --> Corts2[Corts Generals:<br>projecte de llei]
    Corts2 --> Referèndum2[Referèndum]
    Referèndum1 --> Ratificació[Ratificació per Corts Generals]
    Referèndum2 --> Ratificació
    Ratificació --> EA2[Estatut aprovat]
    
    Particular --> Iniciativa[Òrgans preautonòmics<br>acorden via ràpida]
    Iniciativa --> Seguir[Segueixen procediment<br>art. 151.2 CE]
    Seguir --> EA3[Estatut aprovat]
```

---

## 4. Institucions de les Comunitats Autònomes

Totes les Comunitats Autònomes s'organitzen al voltant d'un **sistema institucional** que, malgrat les petites peculiaritats, és força homogeni. Aquest diagrama representa els òrgans principals: l'**Assemblea Legislativa** (parlament unicameral), el **President** (amb triple condició), el **Consell de Govern** i l'**Administració autonòmica**. També s'hi afegeixen les institucions estatals de relació (Delegat del Govern) i els òrgans de control (TSJ, Tribunal de Comptes, etc.).

```mermaid
graph TB
    subgram[Òrgans de la Comunitat Autònoma]
    subgram --> A[Assemblea Legislativa<br>unicameral, 4 anys,s<br>sufragi universal]
    subgram --> B[President<br>- Cap del Govern autonòmic<br>- Representant suprem de la CCAA<br>- Representant ordinari de l'Estat]
    subgram --> C[Consell de Govern<br>President + Consellers<br>doble vessants<br>política i administrativa]
    subgram --> D[Administraciós<br>autonòmica]
    subgram --> E[Tribunal Superiors<br>de Justícia<br>culminas<br>l'organització judicial]
    
    F[Delegat del Govern<br>coordinació Estat-CCAA] -.-> B
    F -.-> D
    
```

```mermaid
graph TB

    G[Òrgans de control] --> H[TC - control constitucionalitat]
    G --> I[Jurisdicció contenciosa]
    G --> J[Tribunal de Comptes]
    G --> K[Control polític art. 155 CE<br>Govern + Senat]
    
    L[Altres institucions:<br>Defensor del Poble autonòmic,<br>Cambres de Comptes,<br>Consells de Justícia]
```


---

## 5. Tipus de repartiment competencial entre Estat i Comunitats Autònomes

El sistema de distribució de competències és complex. Aquest diagrama il·lustra els diferents **tipus de competències** que poden sorgir de la interacció entre les llistes dels articles 148 i 149 CE: competències exclusives (absolutes o relatives), compartides (de regulació o d'execució), competències mínimes (art. 148) i competències residuals (art. 149.3). També es mostren les vies extraestatutàries d'assumpció (lleis marc, harmonització, transferència/delegació).

```mermaid
mindmap
  root((Repartiment competencial<br>Estat - CCAA))
    Competències exclusives de l'Estat
      Absolutes / integrals
        Relacions internacionals
        Defensa i Forces Armades
        Nacionalitat, immigració
      Relatives
        Administració de Justícia (bases)
        Legislació laboral (bases)
    Competències exclusives de la CCAA
      Assumides pels EAs
        Exemples: museus, turisme, cultura
    Competències compartides
      De regulació (bases estatals + desenvolupament CCAA)
        Educació, sanitat, medi ambient
      D'execució (legislació estatal, execució CCAA)
        Propietat intel·lectual, productes farmacèutics
    Competències mínimes (art. 148.1)
      Punt de partida per a totes les CCAA
    Competències residuals (art. 149.3)
      Si no assumides per l'EA, corresponen a l'Estat
      Clàusula de prevalença del Dret estatal
      Dret estatal supletori
    Assumpció extraestatutària (art. 150)
      Lleis marc (150.1)
      Lleis de transferència/delegació (150.2)
      Lleis d'harmonització (150.3)
```

---

## 6. Esquema de control de l'activitat autonòmica

Aquest diagrama aplega els diferents **mecanismes de control** als quals estan sotmesos els òrgans i l'activitat de les Comunitats Autònomes. Es distingeix el control jurisdiccional (TC, contenciós, Tribunal de Comptes), el control polític (art. 155 CE, suspensió de l'art. 161.2 CE) i el control sobre funcions delegades (art. 150.2 CE). És una visió integrada dels “frens i contrapesos” de l'Estat autonòmic.

```mermaid
flowchart LR
    Control[Control de l'activitat autonòmica<br>Art. 153 CE i altres] --> TC[Tribunal Constitucional<br>Constitucionalitats<br>de normes amb rang de llei<br>i altres processos]
    Control --> Contenciós[Jurisdicció contenciosa<br>Actes i reglaments<br>de l'Administració autonòmica]
    Control --> TribunalComptes[Tribunal de Comptes<br>Control econòmic i pressupostari]
    Control --> Govern[Govern de l'Estat<br>Control sobre funcions delegades<br>art. 150.2<br>previ dictamen Consell d'Estat]
    
    Control --> Politic[Control polític excepcional<br>Art. 155 CE]
    Politic --> Requeriment[Requeriment<br>al President<br>de la CCAA]
    Requeriment --> NoAtès[No atès<br>o resposta<br>insuficient]
    NoAtès --> Senat[Aprovació per<br>majoria absoluta<br>del Senat]
    Senat --> Mesures[Adopció de<br>mesures necessàries<br>instruccions a<br>autoritats<br>autonòmiques]
    
    Control --> Suspensió[Suspensió de resolucions<br>Art. 161.2 CE]
    Suspensió --> Veto[Govern<br>pot vetar<br>resolucions<br>autonòmiques]
    Veto --> Ratificació[Ratificació<br>o aixecament<br>pel TC<br>en 5 mesos]
```

---

## 7. Resum de les vies d'accés a l'autonomia (taula visual)

Un diagrama de flux senzill que resumeix el procés de decisió sobre quina via d'accés correspon a cada territori, des de la iniciativa autonòmica fins a l'aprovació de l'Estatut.

```mermaid
flowchart LR
    Iniciativa[Iniciativa autonòmica<br>arts. 143.2, 151.1, DT 1a i 2a] --> Via{Via escollida}
    Via -->|Art. 143.2| Lenta[Via lenta<br>Competències mínimes<br>Procediment art. 146 CE]
    Via -->|Art. 151.1 / DT 2a| Rapida[Via ràpida<br>Màxim nivell competencial<br>Procediment art. 151.2 CE <br>referèndum]
    Via -->|Art. 144.a| Madrid[Llei Orgànica<br>Madrid]
    Via -->|Art. 144.b / DA 1a| Especials[Casos especials<br>Navarra, Ceuta, Melilla]
    
    Lenta --> EA[Estatut d'Autonomia<br>Llei Orgànica]
    Rapida --> EA
    Madrid --> EA
    Especials --> EA
```

Aquests diagrames cobreixen els aspectes més estructurals del Tema 8. Si necessites algun altre enfocament o un diagrama més detallat sobre un apartat concret (per exemple, només les lleis de l'art. 150 o només el control de l'art. 155), no dubtis a demanar-ho.