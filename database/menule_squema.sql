-- -----------------------------------------------------
-- MENULE: Estructura de base de datos
-- Compatible con MySQL 8.0+
-- -----------------------------------------------------
-- Instrucciones:
-- 1. Ejecuta este script en tu gestor MySQL para crear el esquema completo.
-- 2. Por defecto, todo está preparado para comenzar a usar la base de datos.
-- 3. Puedes modificar, ampliar o adaptar según las necesidades de tu aplicación.

-- Crear la base de datos y seleccionarla
CREATE DATABASE IF NOT EXISTS menule;
USE menule;

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

-- Tabla de estudiantes (cada estudiante es también un usuario)
CREATE TABLE Estudiantes (
    id_usuario INT PRIMARY KEY,
    grado_academico VARCHAR(50),
    tui_numero VARCHAR(20) UNIQUE,
    saldo DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla de profesores (cada profesor es también un usuario)
CREATE TABLE Profesores (
    id_usuario INT PRIMARY KEY,
    grado_academico VARCHAR(50),
    tui_numero VARCHAR(20) UNIQUE,
    saldo DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla de personal de comedor (cada miembro es también un usuario)
CREATE TABLE PersonalComedor (
    id_usuario INT PRIMARY KEY,
    fecha_contratacion DATE,
    especialidad VARCHAR(50),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla de platos disponibles en el menú
CREATE TABLE Platos (
    id_plato INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    alergenos VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE
);

-- Menús ofrecidos cada día
CREATE TABLE Menus (
    id_menu INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    tipo ENUM('desayuno', 'almuerzo', 'cena') NOT NULL,
    max_reservas INT,
    disponible BOOLEAN DEFAULT TRUE
);

-- Relación muchos a muchos entre Menús y Platos
CREATE TABLE MenuPlatos (
    id_menu INT,
    id_plato INT,
    PRIMARY KEY (id_menu, id_plato),
    FOREIGN KEY (id_menu) REFERENCES Menus(id_menu) ON DELETE CASCADE,
    FOREIGN KEY (id_plato) REFERENCES Platos(id_plato) ON DELETE CASCADE
);

-- Reservas realizadas por usuarios para un menú
CREATE TABLE Reservas (
    id_reserva INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_menu INT NOT NULL,
    fecha_reserva DATETIME NOT NULL,
    estado ENUM('pendiente', 'confirmada', 'cancelada', 'recogida') DEFAULT 'pendiente',
    estado_bit TINYINT(1) DEFAULT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_menu) REFERENCES Menus(id_menu)
);

-- Platos incluidos en una reserva
CREATE TABLE ReservaPlatos (
    id_reserva INT,
    id_plato INT,
    cantidad INT DEFAULT 1,
    PRIMARY KEY (id_reserva, id_plato),
    FOREIGN KEY (id_reserva) REFERENCES Reservas(id_reserva) ON DELETE CASCADE,
    FOREIGN KEY (id_plato) REFERENCES Platos(id_plato)
);

-- Pagos realizados por reservas
CREATE TABLE Pagos (
    id_pago INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_reserva INT,
    monto DECIMAL(10,2) NOT NULL,
    metodo ENUM('tui', 'bono', 'tarjeta', 'efectivo') NOT NULL,
    fecha_pago DATETIME NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0.00,
    estado ENUM('pendiente', 'completado', 'fallido', 'reembolsado') DEFAULT 'pendiente',
    correo VARCHAR(150),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_reserva) REFERENCES Reservas(id_reserva) ON DELETE CASCADE
);

-- Registro de incidencias (problemas, sugerencias, etc.)
CREATE TABLE Incidencias (
    id_incidencia INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT,
    id_responsable INT,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    numero_seguimiento VARCHAR(50), 
    fecha_reporte DATETIME NOT NULL,
    estado ENUM('abierta', 'en_proceso', 'resuelta', 'cerrada') DEFAULT 'abierta',
    prioridad ENUM('baja', 'media', 'alta', 'critica') DEFAULT 'media',
    fecha_resolucion DATETIME,
    solucion TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE SET NULL,
    FOREIGN KEY (id_responsable) REFERENCES Usuarios(id_usuario) ON DELETE SET NULL
);

-- Ingredientes para la preparación de platos
CREATE TABLE Ingredientes (
    id_ingrediente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    unidad_medida VARCHAR(20),
    stock_actual DECIMAL(10,2) DEFAULT 0,
    stock_minimo DECIMAL(10,2) DEFAULT 0,
    alergeno BOOLEAN DEFAULT FALSE,
    tipo_alergeno VARCHAR(50)
);

-- Índices recomendados para mejorar el rendimiento de consultas frecuentes
CREATE INDEX idx_usuario_email ON Usuarios(email);
CREATE INDEX idx_usuario_tipo ON Usuarios(tipo);
CREATE INDEX idx_menu_fecha ON Menus(fecha);
CREATE INDEX idx_reserva_usuario ON Reservas(id_usuario);
CREATE INDEX idx_reserva_menu ON Reservas(id_menu);
CREATE INDEX idx_reserva_estado ON Reservas(estado);
CREATE INDEX idx_pago_reserva ON Pagos(id_reserva);
CREATE INDEX idx_incidencia_estado ON Incidencias(estado);
CREATE INDEX idx_ingrediente_stock ON Ingredientes(stock_actual, stock_minimo);

-- Vistas útiles para reportes y consultas rápidas

-- Menús disponibles y número de reservas confirmadas
CREATE VIEW VistaMenusDisponibles AS
SELECT m.*, COUNT(r.id_reserva) AS reservas_actuales
FROM Menus m
LEFT JOIN Reservas r ON m.id_menu = r.id_menu AND r.estado = 'confirmada'
WHERE m.disponible = TRUE
GROUP BY m.id_menu;

-- Ingredientes con stock crítico (por debajo del mínimo)
CREATE VIEW VistaStockCritico AS
SELECT i.*, (i.stock_actual < i.stock_minimo) AS bajo_stock
FROM Ingredientes i
WHERE i.stock_actual < i.stock_minimo;

-- Estadísticas diarias de reservas, ingresos y platos vendidos
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