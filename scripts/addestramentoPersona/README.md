## imgStorer.py
Questo e' lo snippet di codice che salva le immagini all'interno di mongoDB. Nota:
```
CONNECTION_STRING = "mongodb://root:root@localhost:27017/"
                            /             \
                           |usrname:password|
```
Per ora le foto vengono salvate una ad una e sembra che tutto vada bene anche mandando numerose foto
una dietro l'altra. Nota pero' che al posto di usare "insert_one" si puo' anche usare "insert_many"
chi inserisce piu' documenti all'interno della collection.
Questo script prendi in INPUT le immagini encodate come per riconoscimentoPersona e salva su mongoDB
seguendo questo albero:
```
trainingDatabase
├── 0000
│   ├── 0
│   │   ├── foto1
│   │   ├── foto2
│   │   └── ...
│   ├── 1
│   ├── 2
│   ├── 3
│   └── ...
├── 0001
│   ├── 0
│   ├── 1
│   └── ...
└── ...
```
Dove:
+ 0000, 0001 ... sono gli id delle macchine
+ 0, 1, ... sono gli id delle persone
+ foto sono file json di questo tipo:
```
foto = {
            "foto_id" : startingId+1,
            "foto" : img
}
```
Dove l'id e' generato in modo progressivo. Forse l'id non serve ma per sicurezza l'ho messo
