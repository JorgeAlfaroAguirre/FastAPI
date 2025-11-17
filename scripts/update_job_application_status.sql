-- Script para actualizar la tabla job_application con nuevos estados

USE gig;
GO

PRINT '========================================';
PRINT 'Actualizando estados de job_application';
PRINT '========================================';
PRINT '';

-- Eliminar la restricción CHECK antigua si existe
IF EXISTS (SELECT * FROM sys.check_constraints WHERE name = 'CK__job_appli__statu__XXX' AND parent_object_id = OBJECT_ID('job_application'))
BEGIN
    ALTER TABLE job_application DROP CONSTRAINT CK__job_appli__statu__XXX;
    PRINT '✓ Restricción CHECK antigua eliminada';
END

-- Agregar nueva restricción CHECK con todos los estados
ALTER TABLE job_application DROP CONSTRAINT IF EXISTS CK_job_application_status;
GO

ALTER TABLE job_application
ADD CONSTRAINT CK_job_application_status
CHECK (status IN (
    'pending',           -- Postulación recibida, sin revisar
    'under_review',      -- En revisión por el reclutador
    'interview_scheduled', -- Entrevista programada
    'interviewed',       -- Entrevista realizada
    'offered',          -- Oferta de trabajo enviada
    'hired',            -- Contratado
    'rejected'          -- Rechazado
));
GO

PRINT '✓ Nueva restricción CHECK agregada con estados expandidos';
PRINT '';
PRINT 'Estados disponibles:';
PRINT '  - pending: Postulación recibida';
PRINT '  - under_review: En revisión';
PRINT '  - interview_scheduled: Entrevista programada';
PRINT '  - interviewed: Entrevista realizada';
PRINT '  - offered: Oferta enviada';
PRINT '  - hired: Contratado';
PRINT '  - rejected: Rechazado';
PRINT '';
PRINT '========================================';
PRINT '✓ Actualización completada';
PRINT '========================================';
