DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
           WHERE  rolname = 'admin') THEN
      CREATE USER admin LOGIN PASSWORD 'admin';
   END IF;
END
$do$;



