--Inserta usario de tipo visitante con Id = 0

INSERT INTO Usuarios(
    id_usuario, dni, nombre, apellido, email, contrasena_hash, telefono, fecha_alta, tipo 
) VALUES (
    '0',
    '00000000B',
    'Visitante',
    'Principal',
    'visitante@menule.com',
    '$2b$12$eU7/AaNLbEWybmHMM5pI1OsEPg95Bm/V2e0KZZ3fTR7FGqZUo1SpK',
    '600000000',
    CURDATE(),
    'visitante'
)