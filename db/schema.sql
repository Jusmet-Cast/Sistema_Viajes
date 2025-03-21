CREATE TABLE Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL
);

CREATE TABLE Colaborador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE Sucursal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    direccion TEXT NOT NULL
);

CREATE TABLE Transportista (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tarifa_por_km REAL NOT NULL
);

CREATE TABLE AsignacionSucursal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colaborador_id INTEGER NOT NULL,
    sucursal_id INTEGER NOT NULL,
    distancia_km REAL NOT NULL,
    FOREIGN KEY (colaborador_id) REFERENCES Colaborador(id),
    FOREIGN KEY (sucursal_id) REFERENCES Sucursal(id),
    CHECK (distancia_km > 0 AND distancia_km <= 50),
    UNIQUE (colaborador_id, sucursal_id)
);

CREATE TABLE Viaje (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    sucursal_id INTEGER NOT NULL,
    transportista_id INTEGER NOT NULL,
    usuario_registro_id INTEGER NOT NULL,
    distancia_total REAL NOT NULL,
    FOREIGN KEY (sucursal_id) REFERENCES Sucursal(id),
    FOREIGN KEY (transportista_id) REFERENCES Transportista(id),
    FOREIGN KEY (usuario_registro_id) REFERENCES Usuario(id)
);

CREATE TABLE ViajeColaborador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    viaje_id INTEGER NOT NULL,
    colaborador_id INTEGER NOT NULL,
    FOREIGN KEY (viaje_id) REFERENCES Viaje(id),
    FOREIGN KEY (colaborador_id) REFERENCES Colaborador(id),
    UNIQUE (colaborador_id, viaje_id)
);