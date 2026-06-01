# Projekt 3 – Elections Scraper

Scraper výsledků voleb do Poslanecké sněmovny 2017 z webu volby.cz.

## Instalace

```bash
pip install -r requirements.txt
```

## Spuštění

```bash
python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_prostejov.csv
```

## Argumenty

1. URL územního celku z volby.cz
2. Název výstupního CSV souboru

## Ukázka

```bash
python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_prostejov.csv
```

Výstup:

```text
Uloženo do souboru: vysledky_prostejov.csv
```
