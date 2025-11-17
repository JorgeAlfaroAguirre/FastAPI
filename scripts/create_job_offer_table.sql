-- Script para crear la tabla job_offer (ofertas de trabajo)

USE gig;
GO

-- Eliminar tabla si existe (solo para desarrollo)
IF OBJECT_ID('job_offer', 'U') IS NOT NULL
    DROP TABLE job_offer;
GO

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
GO

-- Crear índices para mejorar el rendimiento
CREATE INDEX IX_job_offer_created_by ON job_offer(created_by);
CREATE INDEX IX_job_offer_is_active ON job_offer(is_active);
CREATE INDEX IX_job_offer_created_at ON job_offer(created_at DESC);
CREATE INDEX IX_job_offer_job_type ON job_offer(job_type);
GO

PRINT 'Tabla job_offer creada exitosamente';
