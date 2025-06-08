-- Hashea la contraseña 'admin1234' con bcrypt. Por ejemplo, usando Python:
-- import bcrypt; bcrypt.hashpw(b"admin1234", bcrypt.gensalt()).decode()
-- Ejemplo de hash generado (puedes usar el tuyo propio para mayor seguridad):
-- $2b$12$5bZah9yRw9NQOZpI7rQv8uWfFQxqDjv4h6k/8eVtRGZ1KUZvHAQfK6

INSERT INTO Usuarios (
    dni, nombre, apellido, email, contrasena_hash, telefono, fecha_alta, credencial_activa, tipo
) VALUES (
    '00000000A',
    'Admin',
    'Principal',
    'admin@menule.com',
    '$2b$12$gO4RBjo1AK59kCGXgHeGJe27FvKuQA9XUQEehHoH2rmR5Bo24H.kK',
    '600000000',
    CURDATE(),
    TRUE,
    'administrador'
);

