# PsyMz

Just a simple class that keeps a Psycopg2 postgres connection alive indefinitely. 
If a connection has timed out then it will automatically create a new one without any interruption.

## Install
Use pip to install for python 
```commandline
$ pip install psymz
```

## Usage

> :warning: Remember kids, never add your sql arguments directly into the query string. 
> This may lead to SQL injection attacks and quite possible death :dizzy_face:

For setting up a simple connection to your database

```python
from psymz import PostgresConnection
db = PostgresConnection(
    host='http://www.5z8.info/gruesome-gunshot-wounds_c9y3up_animated-gifs-of-train-accidents'
    port=69420
    dbname='awesome_db'
    user='foo'
    password='bar'
)
```

### Simple Read

Makes a normal query with arguments.

```python
>>> some_id = "johnny_boy"
>>> db.execute('SELECT name,value FROM dumb_table WHERE id = %s;', args=(some_id,))
[("John",1,)]
```


### Simple Write

In order to run a write query make sure to tell the class that you're not expecting a result.
> _This could probably be detected by the query itself so if you know more please contribute._

```python
>>> some_id = "johnny_boy"
>>> new_value = 420
>>> statement = "UPDATE dumb_table SET value = %s WHERE id = %s;"
>>> db.execute(statement, args=(new_value,some_id,), return_result=False)
```

### Reading only one row

Makes a normal query with arguments.

```python
>>> some_id = "johnny_boy"
>>> db.execute('SELECT name,value FROM dumb_table WHERE id = %s;', args=(some_id,), fetchone=True)
("John",1,)
```

### Large table read (stream results)

Makes a normal query with arguments.

```python
>>> arguments = (1638154221,)
>>> statement = "SELECT name,value FROM dumb_table WHERE time < %s;"
>>> for row in db.execute_many(statement, args=arguments):
>>>     row
("John",1,)
("Paul",2,)
("George",3,)
("Ringo",4,)
...
```

# License
MIT License: see the LICENSE file.