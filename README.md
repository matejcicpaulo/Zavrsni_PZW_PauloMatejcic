# Zavrsni_PZW_PauloMatejcic - Sustav za upravljanje inventarom i skladištem

Završni projekt iz kolegija programiranje za web

## Autor
Paulo Matejčić

## Opis projekta
Web aplikacija razvijena u Django frameworku za upravljanje skladištem, proizvodima i zalihama.

Aplikacija omogućuje:
- Upravljanje proizvodima (CRUD)
- Upravljanje skladištima (CRUD)
- Upravljanje inventarom (StockItem)
- Pretragu podataka
- Registraciju i prijavu korisnika
- Prikaz low stock stavki
- Dashboard s pregledom podataka

## Modeli

Aplikacija sadrži 3 glavna entiteta:
- Product
- Warehouse
- StockItem

StockItem povezuje Product i Warehouse relacijama (ForeignKey).

## Funkcionalnosti
- Unos novih vrijednosti
- Prikaz i pretraga podataka
- Ažuriranje podataka
- Brisanje podataka
- Generiranje testnih podataka (management command)
- Login i registracija
- Dashboard (broj proizvoda, skladišta i low stock stavki)
- Testovi

## Tehnologije
- Python 3.13
- Django 5.x
- SQLite

## Pokretanje projekta

1. python -m venv venv
2. venv\Scripts\activate
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py seed
6. python manage.py runserver

## Pokretanje testova

python manage.py test
