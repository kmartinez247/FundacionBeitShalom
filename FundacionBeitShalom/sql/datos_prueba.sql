-- OPCIONAL: 16 solicitudes de ejemplo para probar listado, filtros, páginas y Excel.
-- Ejecutar UNA sola vez, después de crear_base_datos.sql. Se pueden borrar desde el panel.
USE BeitShalomDB;
GO

INSERT INTO Colaboradores
    (nombre_completo, pais, correo, telefono, modalidad, disponibilidad,
     motivacion, acepta_privacidad, estado, fecha_registro)
VALUES
('Ana María López', 'El Salvador', 'ana.lopez@ejemplo.com', '7777-0001', 'Presencial', 'Fines de semana', 'Quiero apoyar a los niños.', 1, 'Pendiente', DATEADD(DAY, -16, SYSDATETIME())),
('Carlos Hernández', 'Guatemala', 'carlos.hernandez@ejemplo.com', '5555-0002', 'Virtual', 'Entre semana', 'Puedo ayudar con computadoras.', 1, 'En revisión', DATEADD(DAY, -15, SYSDATETIME())),
('Lucía Fernández', 'Colombia', 'lucia.fernandez@ejemplo.com', '3001-0003', 'Ambas', 'Horarios flexibles', 'Soy docente y me gustaría enseñar.', 1, 'Aprobado', DATEADD(DAY, -14, SYSDATETIME())),
('Miguel Ángel Rivas', 'El Salvador', 'miguel.rivas@ejemplo.com', '7777-0004', 'Presencial', 'Entre semana', 'Organizo eventos en mi iglesia.', 1, 'Aprobado', DATEADD(DAY, -13, SYSDATETIME())),
('Sofía Martínez', 'México', 'sofia.martinez@ejemplo.com', '55-1000-0005', 'Virtual', 'Ocasional', 'Trabajo en redes sociales.', 1, 'Pendiente', DATEADD(DAY, -12, SYSDATETIME())),
('José Pérez', 'Honduras', 'jose.perez@ejemplo.com', '9999-0006', 'Presencial', 'Fines de semana', NULL, 1, 'Rechazado', DATEADD(DAY, -11, SYSDATETIME())),
('Valeria Castillo', 'Costa Rica', 'valeria.castillo@ejemplo.com', '8888-0007', 'Ambas', 'Horarios flexibles', 'Tengo experiencia administrativa.', 1, 'Pendiente', DATEADD(DAY, -10, SYSDATETIME())),
('Diego Ramírez', 'Argentina', 'diego.ramirez@ejemplo.com', '11-5555-0008', 'Virtual', 'Entre semana', 'Quiero gestionar donaciones.', 1, 'En revisión', DATEADD(DAY, -9, SYSDATETIME())),
('Camila Torres', 'Chile', 'camila.torres@ejemplo.com', '9-8888-0009', 'Virtual', 'Ocasional', 'Diseño material de difusión.', 1, 'Aprobado', DATEADD(DAY, -8, SYSDATETIME())),
('Andrés Molina', 'El Salvador', 'andres.molina@ejemplo.com', '7777-0010', 'Presencial', 'Entre semana', 'Me gusta trabajar con niños.', 1, 'Pendiente', DATEADD(DAY, -7, SYSDATETIME())),
('Daniela Ortiz', 'Panamá', 'daniela.ortiz@ejemplo.com', '6000-0011', 'Ambas', 'Fines de semana', NULL, 1, 'Pendiente', DATEADD(DAY, -6, SYSDATETIME())),
('Rafael Quintanilla', 'El Salvador', 'rafael.quintanilla@ejemplo.com', '7777-0012', 'Presencial', 'Fines de semana', 'Quiero ayudar con las donaciones.', 1, 'Aprobado', DATEADD(DAY, -5, SYSDATETIME())),
('Gabriela Mejía', 'Nicaragua', 'gabriela.mejia@ejemplo.com', '8333-0013', 'Virtual', 'Horarios flexibles', 'Puedo ayudar a difundir.', 1, 'Pendiente', DATEADD(DAY, -4, SYSDATETIME())),
('Tomás Aguilar', 'España', 'tomas.aguilar@ejemplo.com', '600-000-014', 'Virtual', 'Ocasional', NULL, 1, 'Rechazado', DATEADD(DAY, -3, SYSDATETIME())),
('Paola Núñez', 'Perú', 'paola.nunez@ejemplo.com', '999-000-015', 'Ambas', 'Entre semana', 'Soy psicóloga y quiero aportar.', 1, 'En revisión', DATEADD(DAY, -2, SYSDATETIME())),
('Héctor Villalta', 'El Salvador', 'hector.villalta@ejemplo.com', '7777-0016', 'Presencial', 'Fines de semana', 'Tengo tiempo libre los sábados.', 1, 'Pendiente', DATEADD(DAY, -1, SYSDATETIME()));
GO

INSERT INTO ColaboradorAreas (colaborador_id, area_id)
SELECT c.id, a.id
FROM (VALUES
    ('ana.lopez@ejemplo.com', 1), ('ana.lopez@ejemplo.com', 3),
    ('carlos.hernandez@ejemplo.com', 2),
    ('lucia.fernandez@ejemplo.com', 3), ('lucia.fernandez@ejemplo.com', 5),
    ('miguel.rivas@ejemplo.com', 1), ('miguel.rivas@ejemplo.com', 4),
    ('sofia.martinez@ejemplo.com', 5),
    ('jose.perez@ejemplo.com', 1),
    ('valeria.castillo@ejemplo.com', 4), ('valeria.castillo@ejemplo.com', 6),
    ('diego.ramirez@ejemplo.com', 2), ('diego.ramirez@ejemplo.com', 7),
    ('camila.torres@ejemplo.com', 5), ('camila.torres@ejemplo.com', 3),
    ('andres.molina@ejemplo.com', 1), ('andres.molina@ejemplo.com', 4),
    ('daniela.ortiz@ejemplo.com', 6),
    ('rafael.quintanilla@ejemplo.com', 1), ('rafael.quintanilla@ejemplo.com', 7),
    ('gabriela.mejia@ejemplo.com', 5), ('gabriela.mejia@ejemplo.com', 8),
    ('tomas.aguilar@ejemplo.com', 2),
    ('paola.nunez@ejemplo.com', 3), ('paola.nunez@ejemplo.com', 6),
    ('hector.villalta@ejemplo.com', 1), ('hector.villalta@ejemplo.com', 4),
    ('hector.villalta@ejemplo.com', 8)
) AS m (correo, area_id)
JOIN Colaboradores c ON c.correo = m.correo
JOIN AreasColaboracion a ON a.id = m.area_id;
GO
