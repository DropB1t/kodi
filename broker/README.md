Questa e' la cartella del server come dovrebbe apparire come quando deployata


51 immagini per iniziare e poi basta NOTA
encoding base64 
ritorno riconoscimento persona
```
{
  id: 0,
  persona: "Mario Rossi"
}
```
riconosco nessuno: id -1, persona: "unknown"


adv/0000/musicRanking
adv/0000/placeRanking
{
  id: 0
  adv: stringa
}

il consiglio lo mandi ogni tot.
```
adv/0000/musicList
adv/0000/placeList

{
  [{title: "cane", author: "gianni"},{}]
}
{"name":1,"album":1, "artists":1}
{"name":1,"latitude_radian":1, "longitude_radian":1}
```


Formato del payload dell'update per luoghi
```
{
    place: {
             'name': "YAYCHI, WEST AZERBAIJAN"
           },
    'emotion': 'Happy',
    'score': -3
}
```

Formato del payload dell'update per canzoni
```
{
    'song': {
                'name': 'Testify',
                'album': 'The Battle Of Los Angeles'
            },
    'emotion': "Happy",
    'score': 2
}
```
