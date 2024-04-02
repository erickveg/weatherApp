# Leveraging APIs for data sharing

## JavaScript Object Notation (JSON Format)

> Today, JSON is the de-facto standard for exchanging data between web and mobile clients and back-end services. [ref](https://www.infoworld.com/article/3222851/what-is-json-a-better-format-for-data-exchange.html)

> Well, when you’re writing frontend code in Javascript, getting JSON data back makes it easier to load that data into an object tree and work with it. And JSON formats data in a more succinct way, which saves bandwidth and improves response times when sending messages back and forth to a server.
>   
>In a world of APIs, cloud computing, and ever-growing data, JSON has a big role to play in greasing the wheels of a modern, open web. [ref](https://blog.sqlizer.io/posts/json-history/)

## REST APIs

> Over the course of the ’00s, another Web services technology, called Representational State Transfer, or REST, began to overtake [all other tools] for the purpose of transferring data. One of the big advantages of programming using REST APIs is that you can use multiple data formats — not just XML, but JSON and HTML as well. As web developers came to prefer JSON over XML, so did they favor REST over SOAP. As Kostyantyn Kharchenko put it on the Svitla blog, “In many ways, the success of REST is due to the JSON format because of its easy use on various platforms.” [ref](https://www.infoworld.com/article/3222851/what-is-json-a-better-format-for-data-exchange.html)

## GraphQL APIs

> GraphQL on the other hand is a query language which gives the client the power to request specific fields and elements it wants to retrieve from the server. It is, loosely speaking, __some kind of SQL for the Web__. It, therefore, has to have knowledge on the available data beforehand, which couples clients somehow to the server. ([ref](https://stackoverflow.com/questions/48022349/what-is-difference-between-rest-api-and-graph-api) and [another reference](https://zapier.com/engineering/graph-apis/)

## Using keys

### Local Computer

The `load_dotenv()` function from the `dotenv` package will look for a file named `.env` in the current directory and add all its variable definitions to the os.environ dictionary. If a .env file is not found in the current directory, then the parent directory is searched for it. The search keeps going up the directory hierarchy until a .env file is found or the top-level directory is reached.

In our `.env` file you store you keys with the variable name, an `=`, and the key with no spaces or quotes.

```
SAFEGRAPH_KEY=LNNmQ
GITHUB_PAT=ghp_1y
```

You can import your key to your environment using the following python code chunk. All other users would then need to use the same `dotenv` package and process for your script to work without anyone needing to store their key in their production script.

```python
import os
from dotenv import load_dotenv
load_dotenv()
sfkey = os.environ.get("SAFEGRAPH_KEY")
```

### Databricks

The recommended option focuses on `dbutils.secrets`.  However, the Community Edition doesn't allow its use.  On Community Edition, you are creating your own compute each time, and you could store your keys in the `Spark` tab under the `Environment variables` just like you would store them as shown in the `.env` example above.

When you are on a group compute environment, you don't want to store your keys in the `Environment variables` as others with access to the compute can retrieve this information. When I don't have access to the Databricks CLI, I create a second notebook called `keys` that stores my keys using a standard python chunk to create the variables.

```python
SAFEGRAPH_KEY = "LNNmQ"
GITHUB_PAT = "ghp_1y"
print("SAFEGRAPH_KEY and GITHUB_PAT created"
```

Then, I source this file using the following command in 

```
%run ./keys
```

## Parsing JSON 

JSON is simply a flat text file that follows a specific format.  Python handles JSON files leveraging [lists](https://www.programiz.com/python-programming/methods/list/append) and [dictionaries](https://www.programiz.com/python-programming/methods/dictionary) to represent the details in a JSON data object.

### Using Pandas `json_normalize()`

> Normalize semi-structured JSON data into a flat table. [reference](https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html)

### Using Pyspark with json (`.jsonl`)

The [Spark 3.5.0 Documentation on JSON Files](https://spark.apache.org/docs/latest/sql-data-sources-json.html) documents how to handle semi-structured JSON data.

## Thought questions

_Let's parse the data into a table._

1. Use the `graphql_noauth.py` and extend the current `query()` to include `image`, `origin`, and `episode`.
2. Convert the episode field from key/value (wide format) to a JSON array (long format) with the keys `number`, `name` and `air_date` and their associated arrays `[]` as the values.
3. Use `pd.parse_json()` to build your table. What do you notice?
4. Save your new `.jsonl` output to the `jsonlines` format using the [jsonlines python package](https://jsonlines.readthedocs.io/en/latest/). Your file should look like [output.jsonl](output.jsonl)
5. Read the `.jsonl` file with `pd.read_json()` and the correct arguments.

### `.jsonl` and array structure

Notice that the API returns the key/value pair for `episode` as

```JSON
'episode': [{'episode': 'S01E10',
   'name': 'Close Rick-counters of the Rick Kind',
   'air_date': 'April 7, 2014'},
  {'episode': 'S03E07',
   'name': 'The Ricklantis Mixup',
   'air_date': 'September 10, 2017'}]}
```
