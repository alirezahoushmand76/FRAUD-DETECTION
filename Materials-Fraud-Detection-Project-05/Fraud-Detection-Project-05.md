### Check Postgresql tabels

```bash
docker exec -it postgres bash

psql -U postgres;

\l

\c postgresql_dump

\dt

select * from dumped;
```

