-- Script para agregar campos de CV a la tabla app_user

USE gig;
GO

-- Verificar si los campos ya existen antes de agregarlos
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_full_name')
BEGIN
    ALTER TABLE app_user ADD cv_full_name NVARCHAR(200) NULL;
    PRINT 'Campo cv_full_name agregado';
END
ELSE
    PRINT 'Campo cv_full_name ya existe';

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_phone')
BEGIN
    ALTER TABLE app_user ADD cv_phone NVARCHAR(50) NULL;
    PRINT 'Campo cv_phone agregado';
END
ELSE
    PRINT 'Campo cv_phone ya existe';

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_summary')
BEGIN
    ALTER TABLE app_user ADD cv_summary NVARCHAR(MAX) NULL;
    PRINT 'Campo cv_summary agregado';
END
ELSE
    PRINT 'Campo cv_summary ya existe';

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_experience')
BEGIN
    ALTER TABLE app_user ADD cv_experience NVARCHAR(MAX) NULL;
    PRINT 'Campo cv_experience agregado';
END
ELSE
    PRINT 'Campo cv_experience ya existe';

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_education')
BEGIN
    ALTER TABLE app_user ADD cv_education NVARCHAR(MAX) NULL;
    PRINT 'Campo cv_education agregado';
END
ELSE
    PRINT 'Campo cv_education ya existe';

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('app_user') AND name = 'cv_skills')
BEGIN
    ALTER TABLE app_user ADD cv_skills NVARCHAR(500) NULL;
    PRINT 'Campo cv_skills agregado';
END
ELSE
    PRINT 'Campo cv_skills ya existe';

GO

PRINT 'Tabla app_user actualizada con campos de CV';
