-- Script para crear la tabla job_application (postulaciones)

USE gig;
GO

-- Eliminar tabla si existe (solo para desarrollo)
IF OBJECT_ID('job_application', 'U') IS NOT NULL
    DROP TABLE job_application;
GO

-- Crear tabla job_application
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
GO

-- Crear índices para mejorar el rendimiento
CREATE INDEX IX_job_application_job_offer ON job_application(job_offer_id);
CREATE INDEX IX_job_application_user ON job_application(user_id);
CREATE INDEX IX_job_application_status ON job_application(status);
CREATE INDEX IX_job_application_applied_at ON job_application(applied_at DESC);
GO

PRINT 'Tabla job_application creada exitosamente';
