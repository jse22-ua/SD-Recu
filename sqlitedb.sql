CREATE TABLE personaje(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nivel INT default 1,
alias text unique,
user_password text,
EF int,
EC int);



create table ciudad(
id integer primary key autoincrement,
nombre text,
temperatura int);

create table casilla(
x int, 
y int,
contenido text default 'vacio',
ciudad integer,
personaje_id integer,
id_mapa INTEGER,
primary key(x,y,id_mapa),
constraint fk_casilla_ciudad foreign key(ciudad) references ciudad(id),
constraint fk_casilla_personaje foreign key(personaje_id) references personaje(id)
FOREIGN KEY (id_mapa) REFERENCES mapa(id)
);



create table ciudades_mapa(
    id_mapa INTEGER,
    id_ciudad INTEGER,
    PRIMARY KEY (id_mapa, id_ciudad),
    FOREIGN KEY (id_mapa) REFERENCES mapa(id),
    FOREIGN KEY (id_ciudad) REFERENCES ciudad(id)
);
	

create table mapa(
  id INTEGER PRIMARY KEY AUTOINCREMENT
  partida text
);
