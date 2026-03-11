-- ============================================
-- HABILITAR ROW LEVEL SECURITY (RLS)
-- Para corregir vulnerabilidades de Supabase
-- ============================================
-- 
-- INSTRUCCIONES:
-- 1. Ve a Supabase Dashboard → SQL Editor
-- 2. Copia y pega este script completo
-- 3. Ejecuta el script
--
-- EXPLICACIÓN:
-- Esto habilita RLS en todas las tablas y crea políticas
-- que SOLO permiten acceso vía service_role (tu app Flask)
-- y BLOQUEAN acceso público vía PostgREST API
-- ============================================

-- Habilitar RLS en todas las tablas
ALTER TABLE public.allowed_emails ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.phases ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.comment ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.predictions ENABLE ROW LEVEL SECURITY;

-- ============================================
-- POLÍTICAS: DENEGAR TODO ACCESO PÚBLICO
-- Solo permitir acceso vía service_role (Flask app)
-- ============================================

-- allowed_emails: Solo service_role
DROP POLICY IF EXISTS "Service role only" ON public.allowed_emails;
CREATE POLICY "Service role only" ON public.allowed_emails
    FOR ALL 
    USING (auth.role() = 'service_role');

-- groups: Solo service_role
DROP POLICY IF EXISTS "Service role only" ON public.groups;
CREATE POLICY "Service role only" ON public.groups
    FOR ALL 
    USING (auth.role() = 'service_role');

-- teams: Solo service_role
DROP POLICY IF EXISTS "Service role only" ON public.teams;
CREATE POLICY "Service role only" ON public.teams
    FOR ALL 
    USING (auth.role() = 'service_role');

-- phases: Solo service_role
DROP POLICY IF EXISTS "Service role only" ON public.phases;
CREATE POLICY "Service role only" ON public.phases
    FOR ALL 
    USING (auth.role() = 'service_role');

-- matches: Solo service_role
DROP POLICY IF EXISTS "Service role only" ON public.matches;
CREATE POLICY "Service role only" ON public.matches
    FOR ALL 
    USING (auth.role() = 'service_role');

-- users: Solo service_role
DROP POLICY IF EXISTS "Service role only" ON public.users;
CREATE POLICY "Service role only" ON public.users
    FOR ALL 
    USING (auth.role() = 'service_role');

-- comment: Solo service_role
DROP POLICY IF EXISTS "Service role only" ON public.comment;
CREATE POLICY "Service role only" ON public.comment
    FOR ALL 
    USING (auth.role() = 'service_role');

-- predictions: Solo service_role
DROP POLICY IF EXISTS "Service role only" ON public.predictions;
CREATE POLICY "Service role only" ON public.predictions
    FOR ALL 
    USING (auth.role() = 'service_role');

-- ============================================
-- VERIFICACIÓN
-- ============================================
-- Ejecuta esta query para verificar que RLS está habilitado:
-- 
-- SELECT tablename, rowsecurity 
-- FROM pg_tables 
-- WHERE schemaname = 'public' 
-- ORDER BY tablename;
--
-- Deberías ver rowsecurity = true en todas las tablas
-- ============================================
