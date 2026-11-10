-- Ejecutar en SQL Server Management Studio (después de crear_base_datos.sql)
USE BeitShalomDB;
GO

CREATE TABLE Administradores (
    id INT IDENTITY(1,1) PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,   -- nunca se guarda la contraseña real
    activo BIT NOT NULL DEFAULT 1,
    fecha_creacion DATETIME2 DEFAULT SYSDATETIME(),
    CONSTRAINT UQ_Administradores_Usuario UNIQUE (usuario)
);
GO
