-- ============================================
-- LIMPIAR COLUMNAS DE PASSWORD RESET
-- Eliminar columnas que ya no se usan
-- ============================================
-- 
-- INSTRUCCIONES:
-- 1. Ve a Supabase Dashboard → SQL Editor
-- 2. Copia y pega este script
-- 3. Ejecuta el script
--
-- EXPLICACIÓN:
-- El sistema de recuperación de contraseñas fue revertido,
-- pero las columnas quedaron en la base de datos.
-- Este script las elimina para limpiar la estructura.
-- ============================================

ALTER TABLE public.users DROP COLUMN IF EXISTS reset_token;
ALTER TABLE public.users DROP COLUMN IF EXISTS reset_token_expires;

-- Verificación
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;
