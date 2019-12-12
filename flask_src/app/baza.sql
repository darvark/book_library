BEGIN TRANSACTION;
DROP TABLE IF EXISTS `zamowienie`;
CREATE TABLE IF NOT EXISTS `zamowienie` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`id_ksiazka`	INTEGER,
	`id_czytelnik`	INTEGER,
	`data_zamowienia`	TEXT NOT NULL,
	`data_wypozyczenia`	TEXT NOT NULL,
	`data_zwrotu`	TEXT,
	FOREIGN KEY (`id_ksiazka`) REFERENCES `ksiazka` ('id'),
	FOREIGN KEY (`id_czytelnik`) REFERENCES `czytelnik` ('id_czytelnik')
);
DROP TABLE IF EXISTS `ksiazka`;
CREATE TABLE IF NOT EXISTS `ksiazka` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`tytul`	TEXT NOT NULL,
	`autor`	TEXT NOT NULL,
	`wydawca`	TEXT NOT NULL,
	`wlasciciel`	TEXT NOT NULL,
	`isbn`	INTEGER NOT NULL,
	`stron`	INTEGER NOT NULL,
	`opis`	TEXT
);
DROP TABLE IF EXISTS `czytelnik`;
CREATE TABLE IF NOT EXISTS `czytelnik` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`imie`	TEXT NOT NULL,
	`nazwisko`	TEXT NOT NULL,
	`telefon`	INTEGER NOT NULL,
	`mail`	TEXT NOT NULL
);
COMMIT;

CREATE TABLE reader (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	fullname VARCHAR, 
	mail VARCHAR, 
	phone INTEGER, 
	PRIMARY KEY (id)
)

CREATE TABLE book (
	id INTEGER NOT NULL, 
	title VARCHAR, 
	author VARCHAR, 
	publisher VARCHAR, 
	book_owner VARCHAR, 
	isbn INTEGER, 
	pages INTEGER, 
	description VARCHAR, 
	PRIMARY KEY (id)
)

CREATE TABLE "order" (
	id INTEGER NOT NULL, 
	book_id INTEGER, 
	reader_id INTEGER, 
	order_date DATE, 
	return_date DATE, 
	rent_date DATE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(book_id) REFERENCES book (id), 
	FOREIGN KEY(reader_id) REFERENCES reader (id)
)
