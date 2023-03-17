SELECT '{}' || dag_id || '/' || task_id || '/' || replace(start_date::text, ' ', 'T') || ':00' AS log_dir
FROM task_instance
WHERE start_date::DATE <= now()::DATE - INTERVAL '{} days'