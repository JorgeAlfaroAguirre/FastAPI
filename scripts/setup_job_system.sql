-- Script maestro para crear el sistema de ofertas de trabajo
-- Ejecuta todos los scripts en orden correcto

USE gig;
GO

PRINT '========================================';
PRINT 'Iniciando configuración del sistema de ofertas de trabajo';
PRINT '========================================';
PRINT '';

-- 1. Actualizar tabla app_user con campos de CV
PRINT 'Paso 1/3: Actualizando tabla app_user con campos de CV...';
PRINT '';

-- Verificar si los campos ya existen antes de agregarlos
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_full_name')
BEGIN
    ALTER TABLE app_user ADD cv_full_name NVARCHAR(200) NULL;
    PRINT '✓ Campo cv_full_name agregado';
END
ELSE
    PRINT '○ Campo cv_full_name ya existe';

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_phone')
BEGIN
    ALTER TABLE app_user ADD cv_phone NVARCHAR(50) NULL;
    PRINT '✓ Campo cv_phone agregado';
END
ELSE
    PRINT '○ Campo cv_phone ya existe';

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_summary')
BEGIN
    ALTER TABLE app_user ADD cv_summary NVARCHAR(MAX) NULL;
    PRINT '✓ Campo cv_summary agregado';
END
ELSE
    PRINT '○ Campo cv_summary ya existe';

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_experience')
BEGIN
    ALTER TABLE app_user ADD cv_experience NVARCHAR(MAX) NULL;
    PRINT '✓ Campo cv_experience agregado';
END
ELSE
    PRINT '○ Campo cv_experience ya existe';

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_education')
BEGIN
    ALTER TABLE app_user ADD cv_education NVARCHAR(MAX) NULL;
    PRINT '✓ Campo cv_education agregado';
END
ELSE
    PRINT '○ Campo cv_education ya existe';

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_skills')
BEGIN
    ALTER TABLE app_user ADD cv_skills NVARCHAR(500) NULL;
    PRINT '✓ Campo cv_skills agregado';
END
ELSE
    PRINT '○ Campo cv_skills ya existe';

PRINT '';
PRINT '✓ Tabla app_user actualizada';
PRINT '';

-- 2. Crear tabla job_offer
PRINT 'Paso 2/3: Creando tabla job_offer...';
PRINT '';

-- Eliminar tabla si existe (solo para desarrollo)
IF OBJECT_ID('job_application', 'U') IS NOT NULL
BEGIN
    DROP TABLE job_application;
    PRINT '○ Tabla job_application eliminada (existía previamente)';
END

IF OBJECT_ID('job_offer', 'U') IS NOT NULL
BEGIN
    DROP TABLE job_offer;
    PRINT '○ Tabla job_offer eliminada (existía previamente)';
END

-- Crear tabla job_offer
CREATE TABLE job_offer (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(200) NOT NULL,
    company NVARCHAR(200) NOT NULL,
    location NVARCHAR(200) NOT NULL,
    job_type NVARCHAR(20) NOT NULL CHECK (job_type IN ('full_time', 'part_time', 'replacement', 'urgent')),
    description NVARCHAR(MAX) NOT NULL,
    salary_range NVARCHAR(100) NULL,
    requirements NVARCHAR(MAX) NULL,
    created_by INT NOT NULL,
    is_active INT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE(),

    -- Foreign key constraint
    CONSTRAINT FK_job_offer_user FOREIGN KEY (created_by)
        REFERENCES app_user(id)
);

-- Crear índices
CREATE INDEX IX_job_offer_created_by ON job_offer(created_by);
CREATE INDEX IX_job_offer_is_active ON job_offer(is_active);
CREATE INDEX IX_job_offer_created_at ON job_offer(created_at DESC);
CREATE INDEX IX_job_offer_job_type ON job_offer(job_type);

PRINT '✓ Tabla job_offer creada con índices';
PRINT '';

-- 3. Crear tabla job_application
PRINT 'Paso 3/3: Creando tabla job_application...';
PRINT '';

CREATE TABLE job_application (
    id INT IDENTITY(1,1) PRIMARY KEY,
    job_offer_id INT NOT NULL,
    user_id INT NOT NULL,
    cover_letter NVARCHAR(MAX) NULL,
    status NVARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'accepted', 'rejected')),
    recruiter_notes NVARCHAR(MAX) NULL,
    applied_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE(),

    -- Foreign key constraints
    CONSTRAINT FK_job_application_job_offer FOREIGN KEY (job_offer_id)
        REFERENCES job_offer(id)
        ON DELETE CASCADE,
    CONSTRAINT FK_job_application_user FOREIGN KEY (user_id)
        REFERENCES app_user(id),

    -- Constraint para evitar postulaciones duplicadas
    CONSTRAINT UQ_job_application_user_offer UNIQUE (job_offer_id, user_id)
);

-- Crear índices
CREATE INDEX IX_job_application_job_offer ON job_application(job_offer_id);
CREATE INDEX IX_job_application_user ON job_application(user_id);
CREATE INDEX IX_job_application_status ON job_application(status);
CREATE INDEX IX_job_application_applied_at ON job_application(applied_at DESC);

PRINT '✓ Tabla job_application creada con índices';
PRINT '';

PRINT '========================================';
PRINT '✓ Sistema de ofertas de trabajo configurado exitosamente';
PRINT '========================================';
PRINT '';
PRINT 'Tablas creadas:';
PRINT '  - job_offer (ofertas de trabajo)';
PRINT '  - job_application (postulaciones)';
PRINT '';
PRINT 'Tabla actualizada:';
PRINT '  - app_user (agregados campos de CV)';
PRINT '';
