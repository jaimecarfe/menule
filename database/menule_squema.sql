-- Active: 1747325415285@@127.0.0.1@3306@menule
-- -----------------------------------------------------
-- MENULE: Estructura de base de datos
-- Compatible con MySQL 8.0+
-- -----------------------------------------------------

-- DROP SCHEMA IF EXISTS menule;
-- CREATE SCHEMA menule;
-- USE menule;

-- Tabla principal de usuarios
CREATE TABLE Usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    dni VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    fecha_alta DATE,
    credencial_activa BOOLEAN DEFAULT TRUE,
    tipo ENUM('estudiante', 'profesor', 'administrador', 'personal_comedor', 'visitante') NOT NULL
);

-- Estudiantes
/*
ALTER TABLE Estudiantes
DROP FOREIGN KEY estudiantes_ibfk_1;

ALTER TABLE Estudiantes
ADD CONSTRAINT estudiantes_ibfk_1
FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
ON DELETE CASCADE;
*/

CREATE TABLE Estudiantes (
    id_usuario INT PRIMARY KEY,
    precio DECIMAL(10,2),
    grado_academico VARCHAR(50),
    tui_numero VARCHAR(20) UNIQUE,
    saldo DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- Profesores
CREATE TABLE Profesores (
    id_usuario INT PRIMARY KEY,
    precio DECIMAL(10,2),
    grado_academico VARCHAR(50),
    saldo DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- Personal de comedor
CREATE TABLE PersonalComedor (
    id_usuario INT PRIMARY KEY,
    fecha_contratacion DATE,
    especialidad VARCHAR(50),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- Platos
CREATE TABLE Platos (
    id_plato INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50),
    precio DECIMAL(10,2) NOT NULL,
    alergenos VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    imagen VARCHAR(255)
);

-- Menús
CREATE TABLE Menus (
    id_menu INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    tipo ENUM('desayuno', 'almuerzo', 'cena') NOT NULL,
    max_reservas INT,
    disponible BOOLEAN DEFAULT TRUE
);

-- Relación muchos a muchos: Menús - Platos
CREATE TABLE MenuPlatos (
    id_menu INT,
    id_plato INT,
    PRIMARY KEY (id_menu, id_plato),
    FOREIGN KEY (id_menu) REFERENCES Menus(id_menu),
    FOREIGN KEY (id_plato) REFERENCES Platos(id_plato)
);

-- Reservas
CREATE TABLE Reservas (
    id_reserva INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_menu INT NOT NULL,
    fecha_reserva DATETIME NOT NULL,
    estado ENUM('pendiente', 'confirmada', 'cancelada', 'recogida') DEFAULT 'pendiente',
    estado_bit TINYINT(1) DEFAULT NULL,
    fecha_cancelacion DATETIME,
    motivo_cancelacion TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_menu) REFERENCES Menus(id_menu)
);

-- Platos dentro de una reserva
CREATE TABLE ReservaPlatos (
    id_reserva INT,
    id_plato INT,
    cantidad INT DEFAULT 1,
    observaciones TEXT,
    PRIMARY KEY (id_reserva, id_plato),
    FOREIGN KEY (id_reserva) REFERENCES Reservas(id_reserva),
    FOREIGN KEY (id_plato) REFERENCES Platos(id_plato)
);

-- Tickets
CREATE TABLE Tickets (
    id_ticket INT PRIMARY KEY AUTO_INCREMENT,
    id_reserva INT NOT NULL,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    fecha_generacion DATETIME NOT NULL,
    estado ENUM('pendiente', 'usado', 'cancelado') DEFAULT 'pendiente',
    fecha_uso DATETIME,
    FOREIGN KEY (id_reserva) REFERENCES Reservas(id_reserva)
);

-- Pagos
CREATE TABLE Pagos (
    id_pago INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_reserva INT,
    monto DECIMAL(10,2) NOT NULL,
    metodo ENUM('tui', 'bono', 'tarjeta', 'efectivo') NOT NULL,
    fecha_pago DATETIME NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0.00,
    estado ENUM('pendiente', 'completado', 'fallido', 'reembolsado') DEFAULT 'pendiente',
    transaccion_id VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_reserva) REFERENCES Reservas(id_reserva)
);

-- Incidencias
CREATE TABLE Incidencias (
    id_incidencia INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_reporte DATETIME NOT NULL,
    estado ENUM('abierta', 'en_proceso', 'resuelta', 'cerrada') DEFAULT 'abierta',
    prioridad ENUM('baja', 'media', 'alta', 'critica') DEFAULT 'media',
    fecha_resolucion DATETIME,
    solucion TEXT,
    id_responsable INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_responsable) REFERENCES Usuarios(id_usuario)
);

-- Ingredientes
CREATE TABLE Ingredientes (
    id_ingrediente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    unidad_medida VARCHAR(20),
    stock_actual DECIMAL(10,2) DEFAULT 0,
    stock_minimo DECIMAL(10,2) DEFAULT 0,
    alergeno BOOLEAN DEFAULT FALSE,
    tipo_alergeno VARCHAR(50)
);

-- Ingredientes por plato
CREATE TABLE PlatoIngredientes (
    id_plato INT,
    id_ingrediente INT,
    cantidad DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_plato, id_ingrediente),
    FOREIGN KEY (id_plato) REFERENCES Platos(id_plato),
    FOREIGN KEY (id_ingrediente) REFERENCES Ingredientes(id_ingrediente)
);

-- Movimientos de stock
CREATE TABLE MovimientosStock (
    id_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    id_ingrediente INT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    tipo ENUM('entrada', 'salida', 'ajuste') NOT NULL,
    fecha DATETIME NOT NULL,
    motivo VARCHAR(255),
    id_usuario INT,
    FOREIGN KEY (id_ingrediente) REFERENCES Ingredientes(id_ingrediente),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- Estadísticas
CREATE TABLE Estadisticas (
    id_estadistica INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    total_reservas INT DEFAULT 0,
    total_pedidos INT DEFAULT 0,
    ingresos DECIMAL(15,2) DEFAULT 0.00,
    plato_mas_popular INT,
    incidencias_reportadas INT DEFAULT 0,
    FOREIGN KEY (plato_mas_popular) REFERENCES Platos(id_plato)
);

-- Configuraciones
CREATE TABLE configuraciones (
    clave VARCHAR(100) PRIMARY KEY,
    valor TEXT
);


-- Índices recomendados
CREATE INDEX idx_usuario_email ON Usuarios(email);
CREATE INDEX idx_usuario_tipo ON Usuarios(tipo);
CREATE INDEX idx_menu_fecha ON Menus(fecha);
CREATE INDEX idx_reserva_usuario ON Reservas(id_usuario);
CREATE INDEX idx_reserva_menu ON Reservas(id_menu);
CREATE INDEX idx_reserva_estado ON Reservas(estado);
CREATE INDEX idx_ticket_codigo ON Tickets(codigo);
CREATE INDEX idx_pago_reserva ON Pagos(id_reserva);
CREATE INDEX idx_incidencia_estado ON Incidencias(estado);
CREATE INDEX idx_ingrediente_stock ON Ingredientes(stock_actual, stock_minimo);

-- Vistas
CREATE VIEW VistaMenusDisponibles AS
SELECT m.*, COUNT(r.id_reserva) AS reservas_actuales
FROM Menus m
LEFT JOIN Reservas r ON m.id_menu = r.id_menu AND r.estado = 'confirmada'
WHERE m.disponible = TRUE
GROUP BY m.id_menu;

CREATE VIEW VistaStockCritico AS
SELECT i.*, (i.stock_actual < i.stock_minimo) AS bajo_stock
FROM Ingredientes i
WHERE i.stock_actual < i.stock_minimo;

CREATE VIEW VistaEstadisticasDiarias AS
SELECT 
    DATE(r.fecha_reserva) AS fecha,
    COUNT(r.id_reserva) AS total_reservas,
    SUM(p.monto) AS ingresos,
    GROUP_CONCAT(DISTINCT rp.id_plato) AS platos_vendidos
FROM Reservas r
JOIN Pagos p ON r.id_reserva = p.id_reserva AND p.estado = 'completado'
LEFT JOIN ReservaPlatos rp ON r.id_reserva = rp.id_reserva
GROUP BY DATE(r.fecha_reserva);



'''
-- Eliminar reservas cuando se borra un usuario
ALTER TABLE Reservas DROP FOREIGN KEY reservas_ibfk_1;
ALTER TABLE Reservas ADD CONSTRAINT reservas_ibfk_1 FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE;

-- Eliminar reserva_platos cuando se borra una reserva
ALTER TABLE ReservaPlatos DROP FOREIGN KEY reservaplatos_ibfk_1;
ALTER TABLE ReservaPlatos ADD CONSTRAINT reservaplatos_ibfk_1 FOREIGN KEY (id_reserva) REFERENCES Reservas(id_reserva) ON DELETE CASCADE;

-- Eliminar tickets cuando se borra una reserva
ALTER TABLE Tickets DROP FOREIGN KEY tickets_ibfk_1;
ALTER TABLE Tickets ADD CONSTRAINT tickets_ibfk_1 FOREIGN KEY (id_reserva) REFERENCES Reservas(id_reserva) ON DELETE CASCADE;

-- Eliminar pagos cuando se borra una reserva
ALTER TABLE Pagos DROP FOREIGN KEY pagos_ibfk_2;
ALTER TABLE Pagos ADD CONSTRAINT pagos_ibfk_2 FOREIGN KEY (id_reserva) REFERENCES Reservas(id_reserva) ON DELETE CASCADE;

-- Eliminar pagos cuando se borra un usuario
ALTER TABLE Pagos DROP FOREIGN KEY pagos_ibfk_1;
ALTER TABLE Pagos ADD CONSTRAINT pagos_ibfk_1 FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE;

-- Eliminar incidencias cuando se borra un usuario
ALTER TABLE Incidencias DROP FOREIGN KEY incidencias_ibfk_1;
ALTER TABLE Incidencias ADD CONSTRAINT incidencias_ibfk_1 FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE SET NULL;

-- Eliminar incidencias cuando se borra el responsable
ALTER TABLE Incidencias DROP FOREIGN KEY incidencias_ibfk_2;
ALTER TABLE Incidencias ADD CONSTRAINT incidencias_ibfk_2 FOREIGN KEY (id_responsable) REFERENCES Usuarios(id_usuario) ON DELETE SET NULL;

-- Eliminar estudiantes, profesores y personal de comedor si se borra el usuario
ALTER TABLE Estudiantes DROP FOREIGN KEY estudiantes_ibfk_1;
ALTER TABLE Estudiantes ADD CONSTRAINT estudiantes_ibfk_1 FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE;

ALTER TABLE Profesores DROP FOREIGN KEY profesores_ibfk_1;
ALTER TABLE Profesores ADD CONSTRAINT profesores_ibfk_1 FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE;

ALTER TABLE PersonalComedor DROP FOREIGN KEY personalcomedor_ibfk_1;
ALTER TABLE PersonalComedor ADD CONSTRAINT personalcomedor_ibfk_1 FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE;
'''