# kodi
Kodi will be your best friend while you're driving 🚗💨



### Nota per chi usa Windows 
Se si fa andare il docker compose con la parte "server" su Windows spostare a mano il file mosquitto.conf nella cartella mosquitto/config che verrà creata dal docker compose, poi far partire lo script python per la popolazione dei database(ci impiega un po'). A questo punto tutto funziona correttamente.

## Server
### Dependencies
Per far partire il server flask la prima volta sulla vostra macchina è necessario scarica delle librerie di python.

Digitare `pip install -r requirements.txt` dentro la cartella **/server**

### Run
Per far partire il server digitare `python3 app.py`. **NB** è indispensabile avere una videocamera come periferica, va bene anche quella default del portatile

## Use Case
Per il prototipo in uso potete vedere questo piccolo video: [prototipo in uso](https://drive.google.com/file/d/1k_Q3X471oNPFuRMEiGusge-NTMzBEOlF/view?usp=share_link)
