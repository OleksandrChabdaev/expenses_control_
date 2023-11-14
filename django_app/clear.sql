DROP SCHEMA public CASCADE;

CREATE SCHEMA public AUTHORIZATION expenses_control_user;

GRANT ALL ON SCHEMA public TO expenses_control_user;
COMMENT ON SCHEMA public IS 'standard public schema';
