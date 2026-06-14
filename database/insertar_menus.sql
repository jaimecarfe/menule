-- Active: 1747325415285@@127.0.0.1@3306@menule
-- 1. Insertar variedad de platos (mínimo 6 primeros, 6 segundos, 4 postres)

INSERT INTO Platos (nombre, tipo, alergenos, activo) VALUES
-- Primeros (6)
('Ensalada mixta', 'primero', 'huevo,pescado', TRUE),
('Crema de verduras', 'primero', '', TRUE),
('Sopa de pescado', 'primero', 'pescado', TRUE),
('Macarrones boloñesa', 'primero', 'gluten', TRUE),
('Gazpacho', 'primero', '', TRUE),
('Arroz tres delicias', 'primero', 'huevo,soja', TRUE),

-- Segundos (6)
('Paella', 'segundo', 'gluten,mariscos', TRUE),
('Pollo asado', 'segundo', '', TRUE),
('Lasagna vegetal', 'segundo', 'gluten,lácteos', TRUE),
('Merluza rebozada', 'segundo', 'pescado,gluten', TRUE),
('Lomo a la plancha', 'segundo', '', TRUE),
('Tortilla de patatas', 'segundo', 'huevo', TRUE),

-- Postres (4)
('Fruta de temporada', 'postre', '', TRUE),
('Tarta de queso', 'postre', 'lácteos,huevo', TRUE),
('Yogur natural', 'postre', 'lácteos', TRUE),
('Flan casero', 'postre', 'huevo,lácteos', TRUE);

-- 2. Crear menús para todos los días hábiles (lunes a viernes) entre 17 de julio y 1 de agosto de 2025

INSERT INTO Menus (fecha, tipo, max_reservas, disponible) VALUES
('2025-07-17', 'almuerzo', 30, TRUE),
('2025-07-18', 'almuerzo', 30, TRUE),
('2025-07-21', 'almuerzo', 30, TRUE),
('2025-07-22', 'almuerzo', 30, TRUE),
('2025-07-23', 'almuerzo', 30, TRUE),
('2025-07-24', 'almuerzo', 30, TRUE),
('2025-07-25', 'almuerzo', 30, TRUE),
('2025-07-28', 'almuerzo', 30, TRUE),
('2025-07-29', 'almuerzo', 30, TRUE),
('2025-07-30', 'almuerzo', 30, TRUE),
('2025-07-31', 'almuerzo', 30, TRUE),
('2025-08-01', 'almuerzo', 30, TRUE);

-- 3. Asociar platos a cada menú.
-- ROTA los platos para dar variedad, pero siempre 3 primeros, 3 segundos, 2 postres

-- 2025-07-17
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-17' AND (
    (p.nombre = 'Ensalada mixta' AND p.tipo = 'primero') OR
    (p.nombre = 'Crema de verduras' AND p.tipo = 'primero') OR
    (p.nombre = 'Macarrones boloñesa' AND p.tipo = 'primero') OR
    (p.nombre = 'Paella' AND p.tipo = 'segundo') OR
    (p.nombre = 'Pollo asado' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lasagna vegetal' AND p.tipo = 'segundo') OR
    (p.nombre = 'Fruta de temporada' AND p.tipo = 'postre') OR
    (p.nombre = 'Tarta de queso' AND p.tipo = 'postre')
);

-- 2025-07-18
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-18' AND (
    (p.nombre = 'Sopa de pescado' AND p.tipo = 'primero') OR
    (p.nombre = 'Gazpacho' AND p.tipo = 'primero') OR
    (p.nombre = 'Arroz tres delicias' AND p.tipo = 'primero') OR
    (p.nombre = 'Merluza rebozada' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lomo a la plancha' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tortilla de patatas' AND p.tipo = 'segundo') OR
    (p.nombre = 'Yogur natural' AND p.tipo = 'postre') OR
    (p.nombre = 'Flan casero' AND p.tipo = 'postre')
);

-- 2025-07-21
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-21' AND (
    (p.nombre = 'Ensalada mixta' AND p.tipo = 'primero') OR
    (p.nombre = 'Gazpacho' AND p.tipo = 'primero') OR
    (p.nombre = 'Arroz tres delicias' AND p.tipo = 'primero') OR
    (p.nombre = 'Paella' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lomo a la plancha' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tortilla de patatas' AND p.tipo = 'segundo') OR
    (p.nombre = 'Fruta de temporada' AND p.tipo = 'postre') OR
    (p.nombre = 'Yogur natural' AND p.tipo = 'postre')
);

-- 2025-07-22
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-22' AND (
    (p.nombre = 'Sopa de pescado' AND p.tipo = 'primero') OR
    (p.nombre = 'Crema de verduras' AND p.tipo = 'primero') OR
    (p.nombre = 'Macarrones boloñesa' AND p.tipo = 'primero') OR
    (p.nombre = 'Merluza rebozada' AND p.tipo = 'segundo') OR
    (p.nombre = 'Pollo asado' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lasagna vegetal' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tarta de queso' AND p.tipo = 'postre') OR
    (p.nombre = 'Flan casero' AND p.tipo = 'postre')
);

-- 2025-07-23
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-23' AND (
    (p.nombre = 'Ensalada mixta' AND p.tipo = 'primero') OR
    (p.nombre = 'Gazpacho' AND p.tipo = 'primero') OR
    (p.nombre = 'Arroz tres delicias' AND p.tipo = 'primero') OR
    (p.nombre = 'Paella' AND p.tipo = 'segundo') OR
    (p.nombre = 'Pollo asado' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tortilla de patatas' AND p.tipo = 'segundo') OR
    (p.nombre = 'Fruta de temporada' AND p.tipo = 'postre') OR
    (p.nombre = 'Yogur natural' AND p.tipo = 'postre')
);

-- 2025-07-24
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-24' AND (
    (p.nombre = 'Sopa de pescado' AND p.tipo = 'primero') OR
    (p.nombre = 'Crema de verduras' AND p.tipo = 'primero') OR
    (p.nombre = 'Macarrones boloñesa' AND p.tipo = 'primero') OR
    (p.nombre = 'Merluza rebozada' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lomo a la plancha' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lasagna vegetal' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tarta de queso' AND p.tipo = 'postre') OR
    (p.nombre = 'Flan casero' AND p.tipo = 'postre')
);

-- 2025-07-25
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-25' AND (
    (p.nombre = 'Ensalada mixta' AND p.tipo = 'primero') OR
    (p.nombre = 'Gazpacho' AND p.tipo = 'primero') OR
    (p.nombre = 'Arroz tres delicias' AND p.tipo = 'primero') OR
    (p.nombre = 'Paella' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lomo a la plancha' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tortilla de patatas' AND p.tipo = 'segundo') OR
    (p.nombre = 'Fruta de temporada' AND p.tipo = 'postre') OR
    (p.nombre = 'Yogur natural' AND p.tipo = 'postre')
);

-- 2025-07-28
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-28' AND (
    (p.nombre = 'Sopa de pescado' AND p.tipo = 'primero') OR
    (p.nombre = 'Crema de verduras' AND p.tipo = 'primero') OR
    (p.nombre = 'Macarrones boloñesa' AND p.tipo = 'primero') OR
    (p.nombre = 'Merluza rebozada' AND p.tipo = 'segundo') OR
    (p.nombre = 'Pollo asado' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lasagna vegetal' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tarta de queso' AND p.tipo = 'postre') OR
    (p.nombre = 'Flan casero' AND p.tipo = 'postre')
);

-- 2025-07-29
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-29' AND (
    (p.nombre = 'Ensalada mixta' AND p.tipo = 'primero') OR
    (p.nombre = 'Gazpacho' AND p.tipo = 'primero') OR
    (p.nombre = 'Arroz tres delicias' AND p.tipo = 'primero') OR
    (p.nombre = 'Paella' AND p.tipo = 'segundo') OR
    (p.nombre = 'Pollo asado' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tortilla de patatas' AND p.tipo = 'segundo') OR
    (p.nombre = 'Fruta de temporada' AND p.tipo = 'postre') OR
    (p.nombre = 'Yogur natural' AND p.tipo = 'postre')
);

-- 2025-07-30
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-30' AND (
    (p.nombre = 'Sopa de pescado' AND p.tipo = 'primero') OR
    (p.nombre = 'Crema de verduras' AND p.tipo = 'primero') OR
    (p.nombre = 'Macarrones boloñesa' AND p.tipo = 'primero') OR
    (p.nombre = 'Merluza rebozada' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lomo a la plancha' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lasagna vegetal' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tarta de queso' AND p.tipo = 'postre') OR
    (p.nombre = 'Flan casero' AND p.tipo = 'postre')
);

-- 2025-07-31
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-07-31' AND (
    (p.nombre = 'Ensalada mixta' AND p.tipo = 'primero') OR
    (p.nombre = 'Gazpacho' AND p.tipo = 'primero') OR
    (p.nombre = 'Arroz tres delicias' AND p.tipo = 'primero') OR
    (p.nombre = 'Paella' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lomo a la plancha' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tortilla de patatas' AND p.tipo = 'segundo') OR
    (p.nombre = 'Fruta de temporada' AND p.tipo = 'postre') OR
    (p.nombre = 'Yogur natural' AND p.tipo = 'postre')
);

-- 2025-08-01
INSERT INTO MenuPlatos (id_menu, id_plato)
SELECT m.id_menu, p.id_plato FROM Menus m, Platos p
WHERE m.fecha = '2025-08-01' AND (
    (p.nombre = 'Sopa de pescado' AND p.tipo = 'primero') OR
    (p.nombre = 'Crema de verduras' AND p.tipo = 'primero') OR
    (p.nombre = 'Macarrones boloñesa' AND p.tipo = 'primero') OR
    (p.nombre = 'Merluza rebozada' AND p.tipo = 'segundo') OR
    (p.nombre = 'Pollo asado' AND p.tipo = 'segundo') OR
    (p.nombre = 'Lasagna vegetal' AND p.tipo = 'segundo') OR
    (p.nombre = 'Tarta de queso' AND p.tipo = 'postre') OR
    (p.nombre = 'Flan casero' AND p.tipo = 'postre')
);