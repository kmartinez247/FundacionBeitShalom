-- Ejecutar en SQL Server Management Studio
IF DB_ID('BeitShalomDB') IS NULL CREATE DATABASE BeitShalomDB;
GO
USE BeitShalomDB;
GO

CREATE TABLE Colaboradores (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL,
    pais VARCHAR(80) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    telefono VARCHAR(30),
    modalidad VARCHAR(30) NOT NULL,
    disponibilidad VARCHAR(100) NOT NULL,
    motivacion VARCHAR(1000),
    acepta_privacidad BIT NOT NULL,
    fecha_registro DATETIME2 DEFAULT SYSDATETIME(),
    estado VARCHAR(20) DEFAULT 'Pendiente',
    CONSTRAINT UQ_Colaboradores_Correo UNIQUE (correo),
    CONSTRAINT CK_Colaboradores_Estado
        CHECK (estado IN ('Pendiente','En revisión','Aprobado','Rechazado')),
    CONSTRAINT CK_Colaboradores_Privacidad CHECK (acepta_privacidad = 1)
);
GO

CREATE TABLE AreasColaboracion (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    activa BIT DEFAULT 1
);
GO

INSERT INTO AreasColaboracion (nombre) VALUES
('Voluntariado presencial'),
('Apoyo profesional o técnico'),
('Apoyo educativo'),
('Organización de actividades'),
('Comunicación y difusión'),
('Apoyo administrativo'),
('Donaciones y gestión de recursos'),
('Otro tipo de colaboración');
GO

CREATE TABLE ColaboradorAreas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    colaborador_id INT NOT NULL,
    area_id INT NOT NULL,
    FOREIGN KEY (colaborador_id) REFERENCES Colaboradores(id),
    FOREIGN KEY (area_id) REFERENCES AreasColaboracion(id),
    CONSTRAINT UQ_Colaborador_Area UNIQUE (colaborador_id, area_id)
);
GO
