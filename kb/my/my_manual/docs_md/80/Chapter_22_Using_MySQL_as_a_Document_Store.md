Interfaces to a MySQL Document Store

22.1 Interfaces to a MySQL Document Store

To work with MySQL as a document store, you use dedicated components and a choice of clients that
support communicating with the MySQL server to develop document based applications.

• The following MySQL products support X Protocol and enable you to use X DevAPI in your chosen

language to develop applications that communicate with a MySQL Server functioning as a document
store:

• MySQL Shell (which provides implementations of X DevAPI in JavaScript and Python)

• Connector/C++

• Connector/J

• Connector/Node.js

• Connector/NET

• Connector/Python

• MySQL Shell is an interactive interface to MySQL supporting JavaScript, Python, or SQL modes.
You can use MySQL Shell to prototype applications, execute queries and update data. Installing
MySQL Shell has instructions to download and install MySQL Shell.

• The quick-start guides (tutorials) in this chapter help you to get started using MySQL Shell with

MySQL as a document store.

The quick-start guide for JavaScript is here: Section 22.3, “JavaScript Quick-Start Guide: MySQL
Shell for Document Store”.

The quick-start guide for Python is here: Section 22.4, “Python Quick-Start Guide: MySQL Shell for
Document Store”.

• The MySQL Shell User Guide at MySQL Shell 8.0 provides detailed information about configuring

and using MySQL Shell.

22.2 Document Store Concepts

This section explains the concepts introduced as part of using MySQL as a document store.

• JSON Document

• Collection

• CRUD Operations

JSON Document

A JSON document is a data structure composed of key-value pairs and is the fundamental structure
for using MySQL as document store. For example, the world_x schema (installed later in this chapter)
contains this document:

{
    "GNP": 4834,
    "_id": "00005de917d80000000000000023",
    "Code": "BWA",
    "Name": "Botswana",
    "IndepYear": 1966,
    "geography": {
        "Region": "Southern Africa",
        "Continent": "Africa",

4062

Collection

        "SurfaceArea": 581730
    },
    "government": {
        "HeadOfState": "Festus G. Mogae",
        "GovernmentForm": "Republic"
    },
    "demographics": {
        "Population": 1622000,
        "LifeExpectancy": 39.29999923706055
    }
}

This document shows that the values of keys can be simple data types, such as integers or strings,
but can also contain other documents, arrays, and lists of documents. For example, the geography
key's value consists of multiple key-value pairs. A JSON document is represented internally using the
MySQL binary JSON object, through the JSON MySQL datatype.

The most important differences between a document and the tables known from traditional relational
databases are that the structure of a document does not have to be defined in advance, and a
collection can contain multiple documents with different structures. Relational tables on the other hand
require that their structure be defined, and all rows in the table must contain the same columns.

Collection

A collection is a container that is used to store JSON documents in a MySQL database. Applications
usually run operations against a collection of documents, for example to find a specific document.

CRUD Operations

The four basic operations that can be issued against a collection are Create, Read, Update and Delete
(CRUD). In terms of MySQL this means:

• Create a new document (insertion or addition)

• Read one or more documents (queries)

• Update one or more documents

• Delete one or more documents

22.3 JavaScript Quick-Start Guide: MySQL Shell for Document
Store

This quick-start guide provides instructions to begin prototyping document store applications
interactively with MySQL Shell. The guide includes the following topics:

• Introduction to MySQL functionality, MySQL Shell, and the world_x example schema.

• Operations to manage collections and documents.

• Operations to manage relational tables.

• Operations that apply to documents within tables.

To follow this quick-start guide you need a MySQL server with X Plugin installed, the default in 8.0, and
MySQL Shell to use as the client. MySQL Shell 8.0 provides more in-depth information about MySQL
Shell. The Document Store is accessed using X DevAPI, and MySQL Shell provides this API in both
JavaScript and Python.

Related Information

• MySQL Shell 8.0 provides more in-depth information about MySQL Shell.

4063

Download and Import world_x Database

• Backspace deletes the character before the cursor and typing new characters enters them at the

cursor position.

• Enter sends the current input line to the server.

Get Help for MySQL Shell

Type mysqlsh --help at the prompt of your command interpreter for a list of command-line options.

mysqlsh --help

Type \help at the MySQL Shell prompt for a list of available commands and their descriptions.

mysql-js> \help

Type \help followed by a command name for detailed help about an individual MySQL Shell
command. For example, to view help on the \connect command, issue:

mysql-js> \help \connect

Quit MySQL Shell

To quit MySQL Shell, issue the following command:

mysql-js> \quit

Related Information

• See Interactive Code Execution for an explanation of how interactive code execution works in

MySQL Shell.

• See Getting Started with MySQL Shell to learn about session and connection alternatives.

22.3.2 Download and Import world_x Database

As part of this quick-start guide, an example schema is provided which is referred to as the world_x
schema. Many of the examples demonstrate Document Store functionality using this schema. Start
your MySQL server so that you can load the world_x schema, then follow these steps:

1. Download world_x-db.zip.

2. Extract the installation archive to a temporary location such as /tmp/. Unpacking the archive

results in a single file named world_x.sql.

3.

Import the world_x.sql file to your server. You can either:

• Start MySQL Shell in SQL mode and import the file by issuing:

mysqlsh -u root --sql --file /tmp/world_x-db/world_x.sql
Enter password: ****

• Set MySQL Shell to SQL mode while it is running and source the schema file by issuing:

\sql
Switching to SQL mode... Commands end with ;
\source /tmp/world_x-db/world_x.sql

Replace /tmp/ with the path to the world_x.sql file on your system. Enter your password if
prompted. A non-root account can be used as long as the account has privileges to create new
schemas.

The world_x Schema

The world_x example schema contains the following JSON collection and relational tables:

4065

Documents and Collections

• Collection

• countryinfo: Information about countries in the world.

• Tables

• country: Minimal information about countries of the world.

• city: Information about some of the cities in those countries.

• countrylanguage: Languages spoken in each country.

Related Information

• MySQL Shell Sessions explains session types.

22.3.3 Documents and Collections

When you are using MySQL as a Document Store, collections are containers within a schema that you
can create, list, and drop. Collections contain JSON documents that you can add, find, update, and
remove.

The examples in this section use the countryinfo collection in the world_x schema. For
instructions on setting up the world_x schema, see Section 22.3.2, “Download and Import world_x
Database”.

Documents

In MySQL, documents are represented as JSON objects. Internally, they are stored in an efficient
binary format that enables fast lookups and updates.

• Simple document format for JavaScript:

{field1: "value", field2 : 10, "field 3": null}

An array of documents consists of a set of documents separated by commas and enclosed within [
and ] characters.

• Simple array of documents for JavaScript:

[{"Name": "Aruba", "Code:": "ABW"}, {"Name": "Angola", "Code:": "AGO"}]

MySQL supports the following JavaScript value types in JSON documents:

• numbers (integer and floating point)

• strings

• boolean (False and True)

• null

• arrays of more JSON values

• nested (or embedded) objects of more JSON values

Collections

Collections are containers for documents that share a purpose and possibly share one or more
indexes. Each collection has a unique name and exists within a single schema.

The term schema is equivalent to a database, which means a group of database objects as opposed to
a relational schema, used to enforce structure and constraints over data. A schema does not enforce
conformity on the documents in a collection.

4066

Documents and Collections

List Collections

To display all collections in the world_x schema, use the db object's getCollections() method.
Collections returned by the server you are currently connected to appear between brackets.

mysql-js> db.getCollections()
[
    <Collection:countryinfo>,
    <Collection:flags>
]

Drop a Collection

To drop an existing collection from a schema, use the db object's dropCollection() method. For
example, to drop the flags collection from the current schema, issue:

mysql-js> db.dropCollection("flags")

The dropCollection() method is also used in MySQL Shell to drop a relational table from a
schema.

Related Information

• See Collection Objects for more examples.

22.3.3.2 Working with Collections

To work with the collections in a schema, use the db global object to access the current schema. In this
example we are using the world_x schema imported previously, and the countryinfo collection.
Therefore, the format of the operations you issue is db.collection_name.operation, where
collection_name is the name of the collection which the operation is executed against. In the
following examples, the operations are executed against the countryinfo collection.

Add a Document

Use the add() method to insert one document or a list of documents into an existing collection. Insert
the following document into the countryinfo collection. As this is multi-line content, press Enter
twice to insert the document.

mysql-js> db.countryinfo.add(
 {
    GNP: .6,
    IndepYear: 1967,
    Name: "Sealand",
    Code: "SEA",
    demographics: {
        LifeExpectancy: 79,
        Population: 27
    },
    geography: {
        Continent: "Europe",
        Region: "British Islands",
        SurfaceArea: 193
    },
    government: {
        GovernmentForm: "Monarchy",
        HeadOfState: "Michael Bates"
    }
  }
)

The method returns the status of the operation. You can verify the operation by searching for the
document. For example:

mysql-js> db.countryinfo.find("Name = 'Sealand'")
{
    "GNP": 0.6,

4068

Documents and Collections

    "_id": "00005e2ff4af00000000000000f4",
    "Name": "Sealand",
    "Code:": "SEA",
    "IndepYear": 1967,
    "geography": {
        "Region": "British Islands",
        "Continent": "Europe",
        "SurfaceArea": 193
    },
    "government": {
        "HeadOfState": "Michael Bates",
        "GovernmentForm": "Monarchy"
    },
    "demographics": {
        "Population": 27,
        "LifeExpectancy": 79
    }
}

Note that in addition to the fields specified when the document was added, there is one more field,
the _id. Each document requires an identifier field called _id. The value of the _id field must be
unique among all documents in the same collection. In MySQL 8.0.11 and higher, document IDs are
generated by the server, not the client, so MySQL Shell does not automatically set an _id value. A
MySQL server at 8.0.11 or higher sets an _id value if the document does not contain the _id field.
A MySQL server at an earlier 8.0 release or at 5.7 does not set an _id value in this situation, so you
must specify it explicitly. If you do not, MySQL Shell returns error 5115 Document is missing a
required field. For more information see Understanding Document IDs.

Related Information

• See CollectionAddFunction for the full syntax definition.

• See Understanding Document IDs.

22.3.3.3 Find Documents

You can use the find() method to query for and return documents from a collection in a schema.
MySQL Shell provides additional methods to use with the find() method to filter and sort the returned
documents.

MySQL provides the following operators to specify search conditions: OR (||), AND (&&), XOR, IS, NOT,
BETWEEN, IN, LIKE, !=, <>, >, >=, <, <=, &, |, <<, >>, +, -, *, /, ~, and %.

Find All Documents in a Collection

To return all documents in a collection, use the find() method without specifying search conditions.
For example, the following operation returns all documents in the countryinfo collection.

mysql-js> db.countryinfo.find()
[
     {
          "GNP": 828,
          "Code:": "ABW",
          "Name": "Aruba",
          "IndepYear": null,
          "geography": {
              "Continent": "North America",
              "Region": "Caribbean",
              "SurfaceArea": 193
          },
          "government": {
              "GovernmentForm": "Nonmetropolitan Territory of The Netherlands",
              "HeadOfState": "Beatrix"
          }
          "demographics": {
              "LifeExpectancy": 78.4000015258789,
              "Population": 103000

4069

Documents and Collections

          },
          ...
      }
 ]
240 documents in set (0.00 sec)

The method produces results that contain operational information in addition to all documents in the
collection.

An empty set (no matching documents) returns the following information:

Empty set (0.00 sec)

Filter Searches

You can include search conditions with the find() method. The syntax for expressions that form a
search condition is the same as that of traditional MySQL Chapter 14, Functions and Operators. You
must enclose all expressions in quotes. For the sake of brevity, some of the examples do not display
output.

A simple search condition could consist of the Name field and a value we know is in a document. The
following example returns a single document:

mysql-js> db.countryinfo.find("Name = 'Australia'")
[
    {
        "GNP": 351182,
        "Code:": "AUS",
        "Name": "Australia",
        "IndepYear": 1901,
        "geography": {
            "Continent": "Oceania",
            "Region": "Australia and New Zealand",
            "SurfaceArea": 7741220
        },
        "government": {
            "GovernmentForm": "Constitutional Monarchy, Federation",
            "HeadOfState": "Elisabeth II"
        }
        "demographics": {
            "LifeExpectancy": 79.80000305175781,
            "Population": 18886000
        },
    }
]

The following example searches for all countries that have a GNP higher than $500 billion. The
countryinfo collection measures GNP in units of million.

mysql-js> db.countryinfo.find("GNP > 500000")
...[output removed]
10 documents in set (0.00 sec)

The Population field in the following query is embedded within the demographics object. To access
the embedded field, use a period between demographics and Population to identify the relationship.
Document and field names are case-sensitive.

mysql-js> db.countryinfo.find("GNP > 500000 and demographics.Population < 100000000")
...[output removed]
6 documents in set (0.00 sec)

Arithmetic operators in the following expression are used to query for countries with a GNP per capita
higher than $30000. Search conditions can include arithmetic operators and most MySQL functions.

Note

Seven documents in the countryinfo collection have a population value of
zero. Therefore warning messages appear at the end of the output.

4070

Documents and Collections

mysql-js> db.countryinfo.find("GNP*1000000/demographics.Population > 30000")
...[output removed]
9 documents in set, 7 warnings (0.00 sec)
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0

You can separate a value from the search condition by using the bind() method. For example,
instead of specifying a hard-coded country name as the condition, substitute a named placeholder
consisting of a colon followed by a name that begins with a letter, such as country. Then use the
bind(placeholder, value) method as follows:

mysql-js> db.countryinfo.find("Name = :country").bind("country", "Italy")
{
    "GNP": 1161755,
    "_id": "00005de917d8000000000000006a",
    "Code": "ITA",
    "Name": "Italy",
    "Airports": [],
    "IndepYear": 1861,
    "geography": {
        "Region": "Southern Europe",
        "Continent": "Europe",
        "SurfaceArea": 301316
    },
    "government": {
        "HeadOfState": "Carlo Azeglio Ciampi",
        "GovernmentForm": "Republic"
    },
    "demographics": {
        "Population": 57680000,
        "LifeExpectancy": 79
    }
}
1 document in set (0.01 sec)

Tip

Within a program, binding enables you to specify placeholders in your
expressions, which are filled in with values before execution and can benefit
from automatic escaping, as appropriate.

Always use binding to sanitize input. Avoid introducing values in queries using
string concatenation, which can produce invalid input and, in some cases, can
cause security issues.

You can use placeholders and the bind() method to create saved searches which you can then call
with different values. For example to create a saved search for a country:

mysql-js> var myFind = db.countryinfo.find("Name = :country")
mysql-js> myFind.bind('country', 'France')
{
    "GNP": 1424285,
    "_id": "00005de917d80000000000000048",
    "Code": "FRA",
    "Name": "France",
    "IndepYear": 843,
    "geography": {
        "Region": "Western Europe",
        "Continent": "Europe",
        "SurfaceArea": 551500
    },
    "government": {
        "HeadOfState": "Jacques Chirac",
        "GovernmentForm": "Republic"

4071

Documents and Collections

    },
    "demographics": {
        "Population": 59225700,
        "LifeExpectancy": 78.80000305175781
    }
}
1 document in set (0.0028 sec)

mysql-js> myFind.bind('country', 'Germany')
{
    "GNP": 2133367,
    "_id": "00005de917d80000000000000038",
    "Code": "DEU",
    "Name": "Germany",
    "IndepYear": 1955,
    "geography": {
        "Region": "Western Europe",
        "Continent": "Europe",
        "SurfaceArea": 357022
    },
    "government": {
        "HeadOfState": "Johannes Rau",
        "GovernmentForm": "Federal Republic"
    },
    "demographics": {
        "Population": 82164700,
        "LifeExpectancy": 77.4000015258789
    }
}

1 document in set (0.0026 sec)

Project Results

You can return specific fields of a document, instead of returning all the fields. The following example
returns the GNP and Name fields of all documents in the countryinfo collection matching the search
conditions.

Use the fields() method to pass the list of fields to return.

mysql-js> db.countryinfo.find("GNP > 5000000").fields(["GNP", "Name"])
[
    {
        "GNP": 8510700,
        "Name": "United States"
    }
]
1 document in set (0.00 sec)

In addition, you can alter the returned documents—adding, renaming, nesting and even computing new
field values—with an expression that describes the document to return. For example, alter the names
of the fields with the following expression to return only two documents.

mysql-js> db.countryinfo.find().fields(
mysqlx.expr('{"Name": upper(Name), "GNPPerCapita": GNP*1000000/demographics.Population}')).limit(2)
{
    "Name": "ARUBA",
    "GNPPerCapita": 8038.834951456311
}
{
    "Name": "AFGHANISTAN",
    "GNPPerCapita": 263.0281690140845
}

Limit, Sort, and Skip Results

You can apply the limit(), sort(), and skip() methods to manage the number and order of
documents returned by the find() method.

4072

Documents and Collections

To specify the number of documents included in a result set, append the limit() method with a
value to the find() method. The following query returns the first five documents in the countryinfo
collection.

mysql-js> db.countryinfo.find().limit(5)
... [output removed]
5 documents in set (0.00 sec)

To specify an order for the results, append the sort() method to the find() method. Pass to
the sort() method a list of one or more fields to sort by and, optionally, the descending (desc) or
ascending (asc) attribute as appropriate. Ascending order is the default order type.

For example, the following query sorts all documents by the IndepYear field and then returns the first
eight documents in descending order.

mysql-js> db.countryinfo.find().sort(["IndepYear desc"]).limit(8)
... [output removed]
8 documents in set (0.00 sec)

By default, the limit() method starts from the first document in the collection. You can use the
skip() method to change the starting document. For example, to ignore the first document and return
the next eight documents matching the condition, pass to the skip() method a value of 1.

mysql-js> db.countryinfo.find().sort(["IndepYear desc"]).limit(8).skip(1)
... [output removed]
8 documents in set (0.00 sec)

Related Information

• The MySQL Reference Manual provides detailed documentation on functions and operators.

• See CollectionFindFunction for the full syntax definition.

22.3.3.4 Modify Documents

You can use the modify() method to update one or more documents in a collection. The X DevAPI
provides additional methods for use with the modify() method to:

• Set and unset fields within documents.

• Append, insert, and delete arrays.

• Bind, limit, and sort the documents to be modified.

Set and Unset Document Fields

The modify() method works by filtering a collection to include only the documents to be modified and
then applying the operations that you specify to those documents.

In the following example, the modify() method uses the search condition to identify the document to
change and then the set() method replaces two values within the nested demographics object.

mysql-js> db.countryinfo.modify("Code = 'SEA'").set(
"demographics", {"LifeExpectancy": 78, "Population": 28})

After you modify a document, use the find() method to verify the change.

To remove content from a document, use the modify() and unset() methods. For example, the
following query removes the GNP from a document that matches the search condition.

mysql-js> db.countryinfo.modify("Name = 'Sealand'").unset("GNP")

Use the find() method to verify the change.

mysql-js> db.countryinfo.find("Name = 'Sealand'")

4073

Documents and Collections

{
    "_id": "00005e2ff4af00000000000000f4",
    "Name": "Sealand",
    "Code:": "SEA",
    "IndepYear": 1967,
    "geography": {
        "Region": "British Islands",
        "Continent": "Europe",
        "SurfaceArea": 193
    },
    "government": {
        "HeadOfState": "Michael Bates",
        "GovernmentForm": "Monarchy"
    },
    "demographics": {
        "Population": 27,
        "LifeExpectancy": 79
    }
}

Append, Insert, and Delete Arrays

To append an element to an array field, or insert, or delete elements in an array, use the
arrayAppend(), arrayInsert(), or arrayDelete() methods. The following examples modify the
countryinfo collection to enable tracking of international airports.

The first example uses the modify() and set() methods to create a new Airports field in all
documents.

Caution

Use care when you modify documents without specifying a search condition;
doing so modifies all documents in the collection.

mysql-js> db.countryinfo.modify("true").set("Airports", [])

With the Airports field added, the next example uses the arrayAppend() method to add a new airport
to one of the documents. $.Airports in the following example represents the Airports field of the current
document.

mysql-js> db.countryinfo.modify("Name = 'France'").arrayAppend("$.Airports", "ORY")

Use find() to see the change.

mysql-js> db.countryinfo.find("Name = 'France'")
{
    "GNP": 1424285,
    "_id": "00005de917d80000000000000048",
    "Code": "FRA",
    "Name": "France",
    "Airports": [
        "ORY"
    ],
    "IndepYear": 843,
    "geography": {
        "Region": "Western Europe",
        "Continent": "Europe",
        "SurfaceArea": 551500
    },
    "government": {
        "HeadOfState": "Jacques Chirac",
        "GovernmentForm": "Republic"
    },
    "demographics": {
        "Population": 59225700,
        "LifeExpectancy": 78.80000305175781
    }
}

4074

Documents and Collections

To insert an element at a different position in the array, use the arrayInsert() method to specify
which index to insert in the path expression. In this case, the index is 0, or the first element in the array.

mysql-js> db.countryinfo.modify("Name = 'France'").arrayInsert("$.Airports[0]", "CDG")

To delete an element from the array, you must pass to the arrayDelete() method the index of the
element to be deleted.

mysql-js> db.countryinfo.modify("Name = 'France'").arrayDelete("$.Airports[1]")

Related Information

• The MySQL Reference Manual provides instructions to help you search for and modify JSON values.

• See CollectionModifyFunction for the full syntax definition.

22.3.3.5 Remove Documents

You can use the remove() method to delete some or all documents from a collection in a schema.
The X DevAPI provides additional methods for use with the remove() method to filter and sort the
documents to be removed.

Remove Documents Using Conditions

The following example passes a search condition to the remove() method. All documents matching
the condition are removed from the countryinfo collection. In this example, one document matches
the condition.

mysql-js> db.countryinfo.remove("Code = 'SEA'")

Remove the First Document

To remove the first document in the countryinfo collection, use the limit() method with a value of
1.

mysql-js> db.countryinfo.remove("true").limit(1)

Remove the Last Document in an Order

The following example removes the last document in the countryinfo collection by country name.

mysql-js> db.countryinfo.remove("true").sort(["Name desc"]).limit(1)

Remove All Documents in a Collection

You can remove all documents in a collection. To do so, use the remove("true") method without
specifying a search condition.

Caution

Use care when you remove documents without specifying a search condition.
This action deletes all documents from the collection.

Alternatively, use the db.drop_collection('countryinfo') operation to delete the
countryinfo collection.

Related Information

• See CollectionRemoveFunction for the full syntax definition.

• See Section 22.3.2, “Download and Import world_x Database” for instructions to recreate the

world_x schema.

4075

Relational Tables

22.3.3.6 Create and Drop Indexes

Indexes are used to find documents with specific field values quickly. Without an index, MySQL must
begin with the first document and then read through the entire collection to find the relevant fields.
The larger the collection, the more this costs. If a collection is large and queries on a specific field are
common, then consider creating an index on a specific field inside a document.

For example, the following query performs better with an index on the Population field:

mysql-js> db.countryinfo.find("demographics.Population < 100")
...[output removed]
8 documents in set (0.00 sec)

The createIndex() method creates an index that you can define with a JSON document that
specifies which fields to use. This section is a high level overview of indexing. For more information see
Indexing Collections.

Add a Nonunique Index

To create a nonunique index, pass an index name and the index information to the createIndex()
method. Duplicate index names are prohibited.

The following example specifies an index named popul, defined against the Population field from
the demographics object, indexed as an Integer numeric value. The final parameter indicates
whether the field should require the NOT NULL constraint. If the value is false, the field can contain
NULL values. The index information is a JSON document with details of one or more fields to include in
the index. Each field definition must include the full document path to the field, and specify the type of
the field.

mysql-js> db.countryinfo.createIndex("popul", {fields:
[{field: '$.demographics.Population', type: 'INTEGER'}]})

Here, the index is created using an integer numeric value. Further options are available, including
options for use with GeoJSON data. You can also specify the type of index, which has been omitted
here because the default type “index” is appropriate.

Add a Unique Index

To create a unique index, pass an index name, the index definition, and the index type “unique” to the
createIndex() method. This example shows a unique index created on the country name ("Name"),
which is another common field in the countryinfo collection to index. In the index field description,
"TEXT(40)" represents the number of characters to index, and "required": True specifies that
the field is required to exist in the document.

mysql-js> db.countryinfo.createIndex("name",
{"fields": [{"field": "$.Name", "type": "TEXT(40)", "required": true}], "unique": true})

Drop an Index

To drop an index, pass the name of the index to drop to the dropIndex() method. For example, you
can drop the “popul” index as follows:

mysql-js> db.countryinfo.dropIndex("popul")

Related Information

• See Indexing Collections for more information.

• See Defining an Index for more information on the JSON document that defines an index.

• See Collection Index Management Functions for the full syntax definition.

22.3.4 Relational Tables

4076

Relational Tables

You can also use X DevAPI to work with relational tables. In MySQL, each relational table is associated
with a particular storage engine. The examples in this section use InnoDB tables in the world_x
schema.

Confirm the Schema

To show the schema that is assigned to the db global variable, issue db.

mysql-js> db
<Schema:world_x>

If the returned value is not Schema:world_x, set the db variable as follows:

mysql-js> \use world_x
Schema `world_x` accessible through db.

Show All Tables

To display all relational tables in the world_x schema, use the getTables() method on the db
object.

mysql-js> db.getTables()
{
    "city": <Table:city>,
    "country": <Table:country>,
    "countrylanguage": <Table:countrylanguage>
}

Basic Table Operations

Basic operations scoped by tables include:

Operation form

db.name.insert()

db.name.select()

db.name.update()

db.name.delete()

Description

The insert() method inserts one or more records
into the named table.

The select() method returns some or all records in
the named table.

The update() method updates records in the
named table.

The delete() method deletes one or more records
from the named table.

Related Information

• See Working with Relational Tables for more information.

• CRUD EBNF Definitions provides a complete list of operations.

• See Section 22.3.2, “Download and Import world_x Database” for instructions on setting up the

world_x schema sample.

22.3.4.1 Insert Records into Tables

You can use the insert() method with the values() method to insert records into an existing
relational table. The insert() method accepts individual columns or all columns in the table. Use one
or more values() methods to specify the values to be inserted.

Insert a Complete Record

To insert a complete record, pass to the insert() method all columns in the table. Then pass to the
values() method one value for each column in the table. For example, to add a new record to the city
table in the world_x schema, insert the following record and press Enter twice.

4077

Relational Tables

mysql-js> db.city.insert("ID", "Name", "CountryCode", "District", "Info").values(
None, "Olympia", "USA", "Washington", '{"Population": 5000}')

The city table has five columns: ID, Name, CountryCode, District, and Info. Each value must match the
data type of the column it represents.

Insert a Partial Record

The following example inserts values into the ID, Name, and CountryCode columns of the city table.

mysql-js> db.city.insert("ID", "Name", "CountryCode").values(
None, "Little Falls", "USA").values(None, "Happy Valley", "USA")

When you specify columns using the insert() method, the number of values must match the
number of columns. In the previous example, you must supply three values to match the three columns
specified.

Related Information

• See TableInsertFunction for the full syntax definition.

22.3.4.2 Select Tables

You can use the select() method to query for and return records from a table in a database. The X
DevAPI provides additional methods to use with the select() method to filter and sort the returned
records.

MySQL provides the following operators to specify search conditions: OR (||), AND (&&), XOR, IS, NOT,
BETWEEN, IN, LIKE, !=, <>, >, >=, <, <=, &, |, <<, >>, +, -, *, /, ~, and %.

Select All Records

To issue a query that returns all records from an existing table, use the select() method without
specifying search conditions. The following example selects all records from the city table in the
world_x database.

Note

Limit the use of the empty select() method to interactive statements. Always
use explicit column-name selections in your application code.

mysql-js> db.city.select()
+------+------------+-------------+------------+-------------------------+
| ID   | Name       | CountryCode | District   | Info                    |
+------+------------+-------------+------------+-------------------------+
|    1 | Kabul      | AFG         | Kabol      |{"Population": 1780000}  |
|    2 | Qandahar   | AFG         | Qandahar   |{"Population": 237500}   |
|    3 | Herat      | AFG         | Herat      |{"Population": 186800}   |
...    ...          ...           ...          ...
| 4079 | Rafah      | PSE         | Rafah      |{"Population": 92020}    |
+------+------- ----+-------------+------------+-------------------------+
4082 rows in set (0.01 sec)

An empty set (no matching records) returns the following information:

Empty set (0.00 sec)

Filter Searches

To issue a query that returns a set of table columns, use the select() method and specify the
columns to return between square brackets. This query returns the Name and CountryCode columns
from the city table.

mysql-js> db.city.select(["Name", "CountryCode"])

4078

Relational Tables

+-------------------+-------------+
| Name              | CountryCode |
+-------------------+-------------+
| Kabul             | AFG         |
| Qandahar          | AFG         |
| Herat             | AFG         |
| Mazar-e-Sharif    | AFG         |
| Amsterdam         | NLD         |
...                 ...
| Rafah             | PSE         |
| Olympia           | USA         |
| Little Falls      | USA         |
| Happy Valley      | USA         |
+-------------------+-------------+
4082 rows in set (0.00 sec)

To issue a query that returns rows matching specific search conditions, use the where() method to
include those conditions. For example, the following example returns the names and country codes of
the cities that start with the letter Z.

mysql-js> db.city.select(["Name", "CountryCode"]).where("Name like 'Z%'")
+-------------------+-------------+
| Name              | CountryCode |
+-------------------+-------------+
| Zaanstad          | NLD         |
| Zoetermeer        | NLD         |
| Zwolle            | NLD         |
| Zenica            | BIH         |
| Zagazig           | EGY         |
| Zaragoza          | ESP         |
| Zamboanga         | PHL         |
| Zahedan           | IRN         |
| Zanjan            | IRN         |
| Zabol             | IRN         |
| Zama              | JPN         |
| Zhezqazghan       | KAZ         |
| Zhengzhou         | CHN         |
...                 ...
| Zeleznogorsk      | RUS         |
+-------------------+-------------+
59 rows in set (0.00 sec)

You can separate a value from the search condition by using the bind() method. For example,
instead of using "Name = 'Z%' " as the condition, substitute a named placeholder consisting of a colon
followed by a name that begins with a letter, such as name. Then include the placeholder and value in
the bind() method as follows:

mysql-js> db.city.select(["Name", "CountryCode"]).
              where("Name like :name").bind("name", "Z%")

Tip

Within a program, binding enables you to specify placeholders in your
expressions, which are filled in with values before execution and can benefit
from automatic escaping, as appropriate.

Always use binding to sanitize input. Avoid introducing values in queries using
string concatenation, which can produce invalid input and, in some cases, can
cause security issues.

Project Results

To issue a query using the AND operator, add the operator between search conditions in the where()
method.

mysql-js> db.city.select(["Name", "CountryCode"]).where(
"Name like 'Z%' and CountryCode = 'CHN'")
+----------------+-------------+

4079

Relational Tables

| Name           | CountryCode |
+----------------+-------------+
| Zhengzhou      | CHN         |
| Zibo           | CHN         |
| Zhangjiakou    | CHN         |
| Zhuzhou        | CHN         |
| Zhangjiang     | CHN         |
| Zigong         | CHN         |
| Zaozhuang      | CHN         |
...              ...
| Zhangjiagang   | CHN         |
+----------------+-------------+
22 rows in set (0.01 sec)

To specify multiple conditional operators, you can enclose the search conditions in parenthesis to
change the operator precedence. The following example demonstrates the placement of AND and OR
operators.

mysql-js> db.city.select(["Name", "CountryCode"]).
where("Name like 'Z%' and (CountryCode = 'CHN' or CountryCode = 'RUS')")
+-------------------+-------------+
| Name              | CountryCode |
+-------------------+-------------+
| Zhengzhou         | CHN         |
| Zibo              | CHN         |
| Zhangjiakou       | CHN         |
| Zhuzhou           | CHN         |
...                 ...
| Zeleznogorsk      | RUS         |
+-------------------+-------------+
29 rows in set (0.01 sec)

Limit, Order, and Offset Results

You can apply the limit(), orderBy(), and offSet() methods to manage the number and order
of records returned by the select() method.

To specify the number of records included in a result set, append the limit() method with a value
to the select() method. For example, the following query returns the first five records in the country
table.

mysql-js> db.country.select(["Code", "Name"]).limit(5)
+------+-------------+
| Code | Name        |
+------+-------------+
| ABW  | Aruba       |
| AFG  | Afghanistan |
| AGO  | Angola      |
| AIA  | Anguilla    |
| ALB  | Albania     |
+------+-------------+
5 rows in set (0.00 sec)

To specify an order for the results, append the orderBy() method to the select() method. Pass to
the orderBy() method a list of one or more columns to sort by and, optionally, the descending (desc)
or ascending (asc) attribute as appropriate. Ascending order is the default order type.

For example, the following query sorts all records by the Name column and then returns the first three
records in descending order .

mysql-js> db.country.select(["Code", "Name"]).orderBy(["Name desc"]).limit(3)
+------+------------+
| Code | Name       |
+------+------------+
| ZWE  | Zimbabwe   |
| ZMB  | Zambia     |
| YUG  | Yugoslavia |
+------+------------+
3 rows in set (0.00 sec)

4080

Relational Tables

By default, the limit() method starts from the first record in the table. You can use the offset()
method to change the starting record. For example, to ignore the first record and return the next three
records matching the condition, pass to the offset() method a value of 1.

mysql-js> db.country.select(["Code", "Name"]).orderBy(["Name desc"]).limit(3).offset(1)
+------+------------+
| Code | Name       |
+------+------------+
| ZMB  | Zambia     |
| YUG  | Yugoslavia |
| YEM  | Yemen      |
+------+------------+
3 rows in set (0.00 sec)

Related Information

• The MySQL Reference Manual provides detailed documentation on functions and operators.

• See TableSelectFunction for the full syntax definition.

22.3.4.3 Update Tables

You can use the update() method to modify one or more records in a table. The update() method
works by filtering a query to include only the records to be updated and then applying the operations
you specify to those records.

To replace a city name in the city table, pass to the set() method the new city name. Then, pass to
the where() method the city name to locate and replace. The following example replaces the city
Peking with Beijing.

mysql-js> db.city.update().set("Name", "Beijing").where("Name = 'Peking'")

Use the select() method to verify the change.

mysql-js> db.city.select(["ID", "Name", "CountryCode", "District", "Info"]).where("Name = 'Beijing'")
+------+-----------+-------------+----------+-----------------------------+
| ID   | Name      | CountryCode | District | Info                        |
+------+-----------+-------------+----------+-----------------------------+
| 1891 | Beijing   | CHN         | Peking   | {"Population": 7472000}     |
+------+-----------+-------------+----------+-----------------------------+
1 row in set (0.00 sec)

Related Information

• See TableUpdateFunction for the full syntax definition.

22.3.4.4 Delete Tables

You can use the delete() method to remove some or all records from a table in a database. The X
DevAPI provides additional methods to use with the delete() method to filter and order the records
to be deleted.

Delete Records Using Conditions

The following example passes search conditions to the delete() method. All records matching the
condition are deleted from the city table. In this example, one record matches the condition.

mysql-js> db.city.delete().where("Name = 'Olympia'")

Delete the First Record

To delete the first record in the city table, use the limit() method with a value of 1.

mysql-js> db.city.delete().limit(1)

4081

Documents in Tables

Delete All Records in a Table

You can delete all records in a table. To do so, use the delete() method without specifying a search
condition.

Caution

Use care when you delete records without specifying a search condition; doing
so deletes all records from the table.

Drop a Table

The dropCollection() method is also used in MySQL Shell to drop a relational table from a
database. For example, to drop the citytest table from the world_x database, issue:

mysql-js> session.dropCollection("world_x", "citytest")

Related Information

• See TableDeleteFunction for the full syntax definition.

• See Section 22.3.2, “Download and Import world_x Database” for instructions to recreate the

world_x database.

22.3.5 Documents in Tables

In MySQL, a table may contain traditional relational data, JSON values, or both. You can combine
traditional data with JSON documents by storing the documents in columns having a native JSON data
type.

Examples in this section use the city table in the world_x schema.

city Table Description

The city table has five columns (or fields).

+---------------+------------+-------+-------+---------+------------------+
| Field         | Type       | Null  | Key   | Default | Extra            |
+---------------+------------+-------+-------+---------+------------------+
| ID            | int(11)    | NO    | PRI   | null    | auto_increment   |
| Name          | char(35)   | NO    |       |         |                  |
| CountryCode   | char(3)    | NO    |       |         |                  |
| District      | char(20)   | NO    |       |         |                  |
| Info          | json       | YES   |       | null    |                  |
+---------------+------------+-------+-------+---------+------------------+

Insert a Record

To insert a document into the column of a table, pass to the values() method a well-formed JSON
document in the correct order. In the following example, a document is passed as the final value to be
inserted into the Info column.

mysql-js> db.city.insert().values(
None, "San Francisco", "USA", "California", '{"Population":830000}')

Select a Record

You can issue a query with a search condition that evaluates document values in the expression.

mysql-js> db.city.select(["ID", "Name", "CountryCode", "District", "Info"]).where(
"CountryCode = :country and Info->'$.Population' > 1000000").bind(
'country', 'USA')
+------+----------------+-------------+----------------+-----------------------------+
| ID   | Name           | CountryCode | District       | Info                        |

4082

Python Quick-Start Guide: MySQL Shell for Document Store

+------+----------------+-------------+----------------+-----------------------------+
| 3793 | New York       | USA         | New York       | {"Population": 8008278}     |
| 3794 | Los Angeles    | USA         | California     | {"Population": 3694820}     |
| 3795 | Chicago        | USA         | Illinois       | {"Population": 2896016}     |
| 3796 | Houston        | USA         | Texas          | {"Population": 1953631}     |
| 3797 | Philadelphia   | USA         | Pennsylvania   | {"Population": 1517550}     |
| 3798 | Phoenix        | USA         | Arizona        | {"Population": 1321045}     |
| 3799 | San Diego      | USA         | California     | {"Population": 1223400}     |
| 3800 | Dallas         | USA         | Texas          | {"Population": 1188580}     |
| 3801 | San Antonio    | USA         | Texas          | {"Population": 1144646}     |
+------+----------------+-------------+----------------+-----------------------------+
9 rows in set (0.01 sec)

Related Information

• See Working with Relational Tables and Documents for more information.

• See Section 13.5, “The JSON Data Type” for a detailed description of the data type.

22.4 Python Quick-Start Guide: MySQL Shell for Document Store

This quick-start guide provides instructions to begin prototyping document store applications
interactively with MySQL Shell. The guide includes the following topics:

• Introduction to MySQL functionality, MySQL Shell, and the world_x example schema.

• Operations to manage collections and documents.

• Operations to manage relational tables.

• Operations that apply to documents within tables.

To follow this quick-start guide you need a MySQL server with X Plugin installed, the default in 8.0, and
MySQL Shell to use as the client. MySQL Shell includes X DevAPI, implemented in both JavaScript
and Python, which enables you to connect to the MySQL server instance using X Protocol and use the
server as a Document Store.

Related Information

• MySQL Shell 8.0 provides more in-depth information about MySQL Shell.

• See Installing MySQL Shell and Section 22.5, “X Plugin” for more information about the tools used in

this quick-start guide.

• See Supported Languages for more information about the languages MySQL Shell supports.

• X DevAPI User Guide provides more examples of using X DevAPI to develop applications which use

MySQL as a Document Store.

• A JavaScript quick-start guide is also available.

22.4.1 MySQL Shell

This quick-start guide assumes a certain level of familiarity with MySQL Shell. The following section
is a high level overview, see the MySQL Shell documentation for more information. MySQL Shell is a
unified scripting interface to MySQL Server. It supports scripting in JavaScript and Python. JavaScript
is the default processing mode.

Start MySQL Shell

After you have installed and started MySQL server, connect MySQL Shell to the server instance. You
need to know the address of the MySQL server instance you plan to connect to. To be able to use
the instance as a Document Store, the server instance must have X Plugin installed and you should

4083

Download and Import world_x Database

Quit MySQL Shell

To quit MySQL Shell, issue the following command:

mysql-py> \quit

Related Information

• See Interactive Code Execution for an explanation of how interactive code execution works in

MySQL Shell.

• See Getting Started with MySQL Shell to learn about session and connection alternatives.

22.4.2 Download and Import world_x Database

As part of this quick-start guide, an example schema is provided which is referred to as the world_x
schema. Many of the examples demonstrate Document Store functionality using this schema. Start
your MySQL server so that you can load the world_x schema, then follow these steps:

1. Download world_x-db.zip.

2. Extract the installation archive to a temporary location such as /tmp/. Unpacking the archive

results in a single file named world_x.sql.

3.

Import the world_x.sql file to your server. You can either:

• Start MySQL Shell in SQL mode and import the file by issuing:

mysqlsh -u root --sql --file /tmp/world_x-db/world_x.sql
Enter password: ****

• Set MySQL Shell to SQL mode while it is running and source the schema file by issuing:

\sql
Switching to SQL mode... Commands end with ;
\source /tmp/world_x-db/world_x.sql

Replace /tmp/ with the path to the world_x.sql file on your system. Enter your password if
prompted. A non-root account can be used as long as the account has privileges to create new
schemas.

The world_x Schema

The world_x example schema contains the following JSON collection and relational tables:

• Collection

• countryinfo: Information about countries in the world.

• Tables

• country: Minimal information about countries of the world.

• city: Information about some of the cities in those countries.

• countrylanguage: Languages spoken in each country.

Related Information

• MySQL Shell Sessions explains session types.

22.4.3 Documents and Collections

4085

Documents and Collections

When you are using MySQL as a Document Store, collections are containers within a schema that you
can create, list, and drop. Collections contain JSON documents that you can add, find, update, and
remove.

The examples in this section use the countryinfo collection in the world_x schema. For
instructions on setting up the world_x schema, see Section 22.4.2, “Download and Import world_x
Database”.

Documents

In MySQL, documents are represented as JSON objects. Internally, they are stored in an efficient
binary format that enables fast lookups and updates.

• Simple document format for Python:

{"field1": "value", "field2" : 10, "field 3": null}

An array of documents consists of a set of documents separated by commas and enclosed within [
and ] characters.

• Simple array of documents for Python:

[{"Name": "Aruba", "Code:": "ABW"}, {"Name": "Angola", "Code:": "AGO"}]

MySQL supports the following Python value types in JSON documents:

• numbers (integer and floating point)

• strings

• boolean (False and True)

• None

• arrays of more JSON values

• nested (or embedded) objects of more JSON values

Collections

Collections are containers for documents that share a purpose and possibly share one or more
indexes. Each collection has a unique name and exists within a single schema.

The term schema is equivalent to a database, which means a group of database objects as opposed to
a relational schema, used to enforce structure and constraints over data. A schema does not enforce
conformity on the documents in a collection.

In this quick-start guide:

• Basic objects include:

Object form

db

db.get_collections()

4086

Description

db is a global variable assigned to the current
active schema. When you want to run operations
against the schema, for example to retrieve a
collection, you use methods available for the db
variable.

db.get_collections() returns a list of collections
in the schema. Use the list to get references to
collection objects, iterate over them, and so on.

Documents and Collections

• Basic operations scoped by collections include:

Operation form

db.name.add()

db.name.find()

db.name.modify()

db.name.remove()

Description

The add() method inserts one document or a list
of documents into the named collection.

The find() method returns some or all documents
in the named collection.

The modify() method updates documents in the
named collection.

The remove() method deletes one document or a
list of documents from the named collection.

Related Information

• See Working with Collections for a general overview.

• CRUD EBNF Definitions provides a complete list of operations.

22.4.3.1 Create, List, and Drop Collections

In MySQL Shell, you can create new collections, get a list of the existing collections in a schema, and
remove an existing collection from a schema. Collection names are case-sensitive and each collection
name must be unique.

Confirm the Schema

To show the value that is assigned to the schema variable, issue:

mysql-py> db

If the schema value is not Schema:world_x, then set the db variable by issuing:

mysql-py> \use world_x

Create a Collection

To create a new collection in an existing schema, use the db object's createCollection() method.
The following example creates a collection called flags in the world_x schema.

mysql-py> db.create_collection("flags")

The method returns a collection object.

<Collection:flags>

List Collections

To display all collections in the world_x schema, use the db object's get_collections() method.
Collections returned by the server you are currently connected to appear between brackets.

mysql-py> db.get_collections()
[
    <Collection:countryinfo>,
    <Collection:flags>
]

Drop a Collection

To drop an existing collection from a schema, use the db object's drop_collection() method. For
example, to drop the flags collection from the current schema, issue:

4087

Documents and Collections

mysql-py> db.drop_collection("flags")

The drop_collection() method is also used in MySQL Shell to drop a relational table from a
schema.

Related Information

• See Collection Objects for more examples.

22.4.3.2 Working with Collections

To work with the collections in a schema, use the db global object to access the current schema. In this
example we are using the world_x schema imported previously, and the countryinfo collection.
Therefore, the format of the operations you issue is db.collection_name.operation, where
collection_name is the name of the collection which the operation is executed against. In the
following examples, the operations are executed against the countryinfo collection.

Add a Document

Use the add() method to insert one document or a list of documents into an existing collection. Insert
the following document into the countryinfo collection. As this is multi-line content, press Enter
twice to insert the document.

mysql-py> db.countryinfo.add(
 {
    "GNP": .6,
    "IndepYear": 1967,
    "Name": "Sealand",
    "Code:": "SEA",
    "demographics": {
        "LifeExpectancy": 79,
        "Population": 27
    },
    "geography": {
        "Continent": "Europe",
        "Region": "British Islands",
        "SurfaceArea": 193
    },
    "government": {
        "GovernmentForm": "Monarchy",
        "HeadOfState": "Michael Bates"
    }
  }
)

The method returns the status of the operation. You can verify the operation by searching for the
document. For example:

mysql-py> db.countryinfo.find("Name = 'Sealand'")
{
    "GNP": 0.6,
    "_id": "00005e2ff4af00000000000000f4",
    "Name": "Sealand",
    "Code:": "SEA",
    "IndepYear": 1967,
    "geography": {
        "Region": "British Islands",
        "Continent": "Europe",
        "SurfaceArea": 193
    },
    "government": {
        "HeadOfState": "Michael Bates",
        "GovernmentForm": "Monarchy"
    },
    "demographics": {
        "Population": 27,
        "LifeExpectancy": 79

4088

Documents and Collections

    }
}

Note that in addition to the fields specified when the document was added, there is one more field,
the _id. Each document requires an identifier field called _id. The value of the _id field must be
unique among all documents in the same collection. In MySQL 8.0.11 and higher, document IDs are
generated by the server, not the client, so MySQL Shell does not automatically set an _id value. A
MySQL server at 8.0.11 or higher sets an _id value if the document does not contain the _id field.
A MySQL server at an earlier 8.0 release or at 5.7 does not set an _id value in this situation, so you
must specify it explicitly. If you do not, MySQL Shell returns error 5115 Document is missing a
required field. For more information see Understanding Document IDs.

Related Information

• See CollectionAddFunction for the full syntax definition.

• See Understanding Document IDs.

22.4.3.3 Find Documents

You can use the find() method to query for and return documents from a collection in a schema.
MySQL Shell provides additional methods to use with the find() method to filter and sort the returned
documents.

MySQL provides the following operators to specify search conditions: OR (||), AND (&&), XOR, IS, NOT,
BETWEEN, IN, LIKE, !=, <>, >, >=, <, <=, &, |, <<, >>, +, -, *, /, ~, and %.

Find All Documents in a Collection

To return all documents in a collection, use the find() method without specifying search conditions.
For example, the following operation returns all documents in the countryinfo collection.

mysql-py> db.countryinfo.find()
[
     {
          "GNP": 828,
          "Code:": "ABW",
          "Name": "Aruba",
          "IndepYear": null,
          "geography": {
              "Continent": "North America",
              "Region": "Caribbean",
              "SurfaceArea": 193
          },
          "government": {
              "GovernmentForm": "Nonmetropolitan Territory of The Netherlands",
              "HeadOfState": "Beatrix"
          }
          "demographics": {
              "LifeExpectancy": 78.4000015258789,
              "Population": 103000
          },
          ...
      }
 ]
240 documents in set (0.00 sec)

The method produces results that contain operational information in addition to all documents in the
collection.

An empty set (no matching documents) returns the following information:

Empty set (0.00 sec)

Filter Searches

4089

Documents and Collections

You can include search conditions with the find() method. The syntax for expressions that form a
search condition is the same as that of traditional MySQL Chapter 14, Functions and Operators. You
must enclose all expressions in quotes. For the sake of brevity, some of the examples do not display
output.

A simple search condition could consist of the Name field and a value we know is in a document. The
following example returns a single document:

mysql-py> db.countryinfo.find("Name = 'Australia'")
[
    {
        "GNP": 351182,
        "Code:": "AUS",
        "Name": "Australia",
        "IndepYear": 1901,
        "geography": {
            "Continent": "Oceania",
            "Region": "Australia and New Zealand",
            "SurfaceArea": 7741220
        },
        "government": {
            "GovernmentForm": "Constitutional Monarchy, Federation",
            "HeadOfState": "Elisabeth II"
        }
        "demographics": {
            "LifeExpectancy": 79.80000305175781,
            "Population": 18886000
        },
    }
]

The following example searches for all countries that have a GNP higher than $500 billion. The
countryinfo collection measures GNP in units of million.

mysql-py> db.countryinfo.find("GNP > 500000")
...[output removed]
10 documents in set (0.00 sec)

The Population field in the following query is embedded within the demographics object. To access
the embedded field, use a period between demographics and Population to identify the relationship.
Document and field names are case-sensitive.

mysql-py> db.countryinfo.find("GNP > 500000 and demographics.Population < 100000000")
...[output removed]
6 documents in set (0.00 sec)

Arithmetic operators in the following expression are used to query for countries with a GNP per capita
higher than $30000. Search conditions can include arithmetic operators and most MySQL functions.

Note

Seven documents in the countryinfo collection have a population value of
zero. Therefore warning messages appear at the end of the output.

mysql-py> db.countryinfo.find("GNP*1000000/demographics.Population > 30000")
...[output removed]
9 documents in set, 7 warnings (0.00 sec)
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0
Warning (Code 1365): Division by 0

You can separate a value from the search condition by using the bind() method. For example,
instead of specifying a hard-coded country name as the condition, substitute a named placeholder

4090

Documents and Collections

consisting of a colon followed by a name that begins with a letter, such as country. Then use the
bind(placeholder, value) method as follows:

mysql-py> db.countryinfo.find("Name = :country").bind("country", "Italy")
{
    "GNP": 1161755,
    "_id": "00005de917d8000000000000006a",
    "Code": "ITA",
    "Name": "Italy",
    "Airports": [],
    "IndepYear": 1861,
    "geography": {
        "Region": "Southern Europe",
        "Continent": "Europe",
        "SurfaceArea": 301316
    },
    "government": {
        "HeadOfState": "Carlo Azeglio Ciampi",
        "GovernmentForm": "Republic"
    },
    "demographics": {
        "Population": 57680000,
        "LifeExpectancy": 79
    }
}
1 document in set (0.01 sec)

Tip

Within a program, binding enables you to specify placeholders in your
expressions, which are filled in with values before execution and can benefit
from automatic escaping, as appropriate.

Always use binding to sanitize input. Avoid introducing values in queries using
string concatenation, which can produce invalid input and, in some cases, can
cause security issues.

You can use placeholders and the bind() method to create saved searches which you can then call
with different values. For example to create a saved search for a country:

mysql-py> myFind = db.countryinfo.find("Name = :country")
mysql-py> myFind.bind('country', 'France')
{
    "GNP": 1424285,
    "_id": "00005de917d80000000000000048",
    "Code": "FRA",
    "Name": "France",
    "IndepYear": 843,
    "geography": {
        "Region": "Western Europe",
        "Continent": "Europe",
        "SurfaceArea": 551500
    },
    "government": {
        "HeadOfState": "Jacques Chirac",
        "GovernmentForm": "Republic"
    },
    "demographics": {
        "Population": 59225700,
        "LifeExpectancy": 78.80000305175781
    }
}
1 document in set (0.0028 sec)

mysql-py> myFind.bind('country', 'Germany')
{
    "GNP": 2133367,
    "_id": "00005de917d80000000000000038",
    "Code": "DEU",
    "Name": "Germany",

4091

Documents and Collections

    "IndepYear": 1955,
    "geography": {
        "Region": "Western Europe",
        "Continent": "Europe",
        "SurfaceArea": 357022
    },
    "government": {
        "HeadOfState": "Johannes Rau",
        "GovernmentForm": "Federal Republic"
    },
    "demographics": {
        "Population": 82164700,
        "LifeExpectancy": 77.4000015258789
    }
}

1 document in set (0.0026 sec)

Project Results

You can return specific fields of a document, instead of returning all the fields. The following example
returns the GNP and Name fields of all documents in the countryinfo collection matching the search
conditions.

Use the fields() method to pass the list of fields to return.

mysql-py> db.countryinfo.find("GNP > 5000000").fields(["GNP", "Name"])
[
    {
        "GNP": 8510700,
        "Name": "United States"
    }
]
1 document in set (0.00 sec)

In addition, you can alter the returned documents—adding, renaming, nesting and even computing new
field values—with an expression that describes the document to return. For example, alter the names
of the fields with the following expression to return only two documents.

mysql-py> db.countryinfo.find().fields(
mysqlx.expr('{"Name": upper(Name), "GNPPerCapita": GNP*1000000/demographics.Population}')).limit(2)
{
    "Name": "ARUBA",
    "GNPPerCapita": 8038.834951456311
}
{
    "Name": "AFGHANISTAN",
    "GNPPerCapita": 263.0281690140845
}

Limit, Sort, and Skip Results

You can apply the limit(), sort(), and skip() methods to manage the number and order of
documents returned by the find() method.

To specify the number of documents included in a result set, append the limit() method with a
value to the find() method. The following query returns the first five documents in the countryinfo
collection.

mysql-py> db.countryinfo.find().limit(5)
... [output removed]
5 documents in set (0.00 sec)

To specify an order for the results, append the sort() method to the find() method. Pass to
the sort() method a list of one or more fields to sort by and, optionally, the descending (desc) or
ascending (asc) attribute as appropriate. Ascending order is the default order type.

4092

Documents and Collections

For example, the following query sorts all documents by the IndepYear field and then returns the first
eight documents in descending order.

mysql-py> db.countryinfo.find().sort(["IndepYear desc"]).limit(8)
... [output removed]
8 documents in set (0.00 sec)

By default, the limit() method starts from the first document in the collection. You can use the
skip() method to change the starting document. For example, to ignore the first document and return
the next eight documents matching the condition, pass to the skip() method a value of 1.

mysql-py> db.countryinfo.find().sort(["IndepYear desc"]).limit(8).skip(1)
... [output removed]
8 documents in set (0.00 sec)

Related Information

• The MySQL Reference Manual provides detailed documentation on functions and operators.

• See CollectionFindFunction for the full syntax definition.

22.4.3.4 Modify Documents

You can use the modify() method to update one or more documents in a collection. The X DevAPI
provides additional methods for use with the modify() method to:

• Set and unset fields within documents.

• Append, insert, and delete arrays.

• Bind, limit, and sort the documents to be modified.

Set and Unset Document Fields

The modify() method works by filtering a collection to include only the documents to be modified and
then applying the operations that you specify to those documents.

In the following example, the modify() method uses the search condition to identify the document to
change and then the set() method replaces two values within the nested demographics object.

mysql-py> db.countryinfo.modify("Code = 'SEA'").set(
"demographics", {"LifeExpectancy": 78, "Population": 28})

After you modify a document, use the find() method to verify the change.

To remove content from a document, use the modify() and unset() methods. For example, the
following query removes the GNP from a document that matches the search condition.

mysql-py> db.countryinfo.modify("Name = 'Sealand'").unset("GNP")

Use the find() method to verify the change.

mysql-py> db.countryinfo.find("Name = 'Sealand'")
{
    "_id": "00005e2ff4af00000000000000f4",
    "Name": "Sealand",
    "Code:": "SEA",
    "IndepYear": 1967,
    "geography": {
        "Region": "British Islands",
        "Continent": "Europe",
        "SurfaceArea": 193
    },
    "government": {
        "HeadOfState": "Michael Bates",
        "GovernmentForm": "Monarchy"
    },

4093

Documents and Collections

    "demographics": {
        "Population": 27,
        "LifeExpectancy": 79
    }
}

Append, Insert, and Delete Arrays

To append an element to an array field, or insert, or delete elements in an array, use the
array_append(), array_insert(), or array_delete() methods. The following examples
modify the countryinfo collection to enable tracking of international airports.

The first example uses the modify() and set() methods to create a new Airports field in all
documents.

Caution

Use care when you modify documents without specifying a search condition;
doing so modifies all documents in the collection.

mysql-py> db.countryinfo.modify("true").set("Airports", [])

With the Airports field added, the next example uses the array_append() method to add a new
airport to one of the documents. $.Airports in the following example represents the Airports field of the
current document.

mysql-py> db.countryinfo.modify("Name = 'France'").array_append("$.Airports", "ORY")

Use find() to see the change.

mysql-py> db.countryinfo.find("Name = 'France'")
{
    "GNP": 1424285,
    "_id": "00005de917d80000000000000048",
    "Code": "FRA",
    "Name": "France",
    "Airports": [
        "ORY"
    ],
    "IndepYear": 843,
    "geography": {
        "Region": "Western Europe",
        "Continent": "Europe",
        "SurfaceArea": 551500
    },
    "government": {
        "HeadOfState": "Jacques Chirac",
        "GovernmentForm": "Republic"
    },
    "demographics": {
        "Population": 59225700,
        "LifeExpectancy": 78.80000305175781
    }
}

To insert an element at a different position in the array, use the array_insert() method to specify
which index to insert in the path expression. In this case, the index is 0, or the first element in the array.

mysql-py> db.countryinfo.modify("Name = 'France'").array_insert("$.Airports[0]", "CDG")

To delete an element from the array, you must pass to the array_delete() method the index of the
element to be deleted.

mysql-py> db.countryinfo.modify("Name = 'France'").array_delete("$.Airports[1]")

Related Information

• The MySQL Reference Manual provides instructions to help you search for and modify JSON values.

4094

Documents and Collections

• See CollectionModifyFunction for the full syntax definition.

22.4.3.5 Remove Documents

You can use the remove() method to delete some or all documents from a collection in a schema.
The X DevAPI provides additional methods for use with the remove() method to filter and sort the
documents to be removed.

Remove Documents Using Conditions

The following example passes a search condition to the remove() method. All documents matching
the condition are removed from the countryinfo collection. In this example, one document matches
the condition.

mysql-py> db.countryinfo.remove("Code = 'SEA'")

Remove the First Document

To remove the first document in the countryinfo collection, use the limit() method with a value of
1.

mysql-py> db.countryinfo.remove("true").limit(1)

Remove the Last Document in an Order

The following example removes the last document in the countryinfo collection by country name.

mysql-py> db.countryinfo.remove("true").sort(["Name desc"]).limit(1)

Remove All Documents in a Collection

You can remove all documents in a collection. To do so, use the remove("true") method without
specifying a search condition.

Caution

Use care when you remove documents without specifying a search condition.
This action deletes all documents from the collection.

Alternatively, use the db.drop_collection('countryinfo') operation to delete the
countryinfo collection.

Related Information

• See CollectionRemoveFunction for the full syntax definition.

• See Section 22.4.2, “Download and Import world_x Database” for instructions to recreate the

world_x schema.

22.4.3.6 Create and Drop Indexes

Indexes are used to find documents with specific field values quickly. Without an index, MySQL must
begin with the first document and then read through the entire collection to find the relevant fields.
The larger the collection, the more this costs. If a collection is large and queries on a specific field are
common, then consider creating an index on a specific field inside a document.

For example, the following query performs better with an index on the Population field:

mysql-py> db.countryinfo.find("demographics.Population < 100")
...[output removed]
8 documents in set (0.00 sec)

4095

Relational Tables

The create_index() method creates an index that you can define with a JSON document that
specifies which fields to use. This section is a high level overview of indexing. For more information see
Indexing Collections.

Add a Nonunique Index

To create a nonunique index, pass an index name and the index information to the create_index()
method. Duplicate index names are prohibited.

The following example specifies an index named popul, defined against the Population field from
the demographics object, indexed as an Integer numeric value. The final parameter indicates
whether the field should require the NOT NULL constraint. If the value is false, the field can contain
NULL values. The index information is a JSON document with details of one or more fields to include in
the index. Each field definition must include the full document path to the field, and specify the type of
the field.

mysql-py> db.countryinfo.createIndex("popul", {fields:
[{field: '$.demographics.Population', type: 'INTEGER'}]})

Here, the index is created using an integer numeric value. Further options are available, including
options for use with GeoJSON data. You can also specify the type of index, which has been omitted
here because the default type “index” is appropriate.

Add a Unique Index

To create a unique index, pass an index name, the index definition, and the index type “unique” to
the create_index() method. This example shows a unique index created on the country name
("Name"), which is another common field in the countryinfo collection to index. In the index field
description, "TEXT(40)" represents the number of characters to index, and "required": True
specifies that the field is required to exist in the document.

mysql-py> db.countryinfo.create_index("name",
{"fields": [{"field": "$.Name", "type": "TEXT(40)", "required": True}], "unique": True})

Drop an Index

To drop an index, pass the name of the index to drop to the drop_index() method. For example, you
can drop the “popul” index as follows:

mysql-py> db.countryinfo.drop_index("popul")

Related Information

• See Indexing Collections for more information.

• See Defining an Index for more information on the JSON document that defines an index.

• See Collection Index Management Functions for the full syntax definition.

22.4.4 Relational Tables

You can also use X DevAPI to work with relational tables. In MySQL, each relational table is associated
with a particular storage engine. The examples in this section use InnoDB tables in the world_x
schema.

Confirm the Schema

To show the schema that is assigned to the db global variable, issue db.

mysql-py> db
<Schema:world_x>

If the returned value is not Schema:world_x, set the db variable as follows:

4096

Relational Tables

mysql-py> \use world_x
Schema `world_x` accessible through db.

Show All Tables

To display all relational tables in the world_x schema, use the get_tables() method on the db
object.

mysql-py> db.get_tables()
[
    <Table:city>,
    <Table:country>,
    <Table:countrylanguage>
]

Basic Table Operations

Basic operations scoped by tables include:

Operation form

db.name.insert()

db.name.select()

db.name.update()

db.name.delete()

Description

The insert() method inserts one or more records
into the named table.

The select() method returns some or all records in
the named table.

The update() method updates records in the
named table.

The delete() method deletes one or more records
from the named table.

Related Information

• See Working with Relational Tables for more information.

• CRUD EBNF Definitions provides a complete list of operations.

• See Section 22.4.2, “Download and Import world_x Database” for instructions on setting up the

world_x schema sample.

22.4.4.1 Insert Records into Tables

You can use the insert() method with the values() method to insert records into an existing
relational table. The insert() method accepts individual columns or all columns in the table. Use one
or more values() methods to specify the values to be inserted.

Insert a Complete Record

To insert a complete record, pass to the insert() method all columns in the table. Then pass to the
values() method one value for each column. For example, to add a new record to the city table in the
world_x database, insert the following record and press Enter twice.

mysql-py> db.city.insert("ID", "Name", "CountryCode", "District", "Info").values(
None, "Olympia", "USA", "Washington", '{"Population": 5000}')

The city table has five columns: ID, Name, CountryCode, District, and Info. Each value must match the
data type of the column it represents.

Insert a Partial Record

The following example inserts values into the ID, Name, and CountryCode columns of the city table.

mysql-py> db.city.insert("ID", "Name", "CountryCode").values(

4097

Relational Tables

None, "Little Falls", "USA").values(None, "Happy Valley", "USA")

When you specify columns using the insert() method, the number of values must match the
number of columns. In the previous example, you must supply three values to match the three columns
specified.

Related Information

• See TableInsertFunction for the full syntax definition.

22.4.4.2 Select Tables

You can use the select() method to query for and return records from a table in a database. The X
DevAPI provides additional methods to use with the select() method to filter and sort the returned
records.

MySQL provides the following operators to specify search conditions: OR (||), AND (&&), XOR, IS, NOT,
BETWEEN, IN, LIKE, !=, <>, >, >=, <, <=, &, |, <<, >>, +, -, *, /, ~, and %.

Select All Records

To issue a query that returns all records from an existing table, use the select() method without
specifying search conditions. The following example selects all records from the city table in the
world_x database.

Note

Limit the use of the empty select() method to interactive statements. Always
use explicit column-name selections in your application code.

mysql-py> db.city.select()
+------+------------+-------------+------------+-------------------------+
| ID   | Name       | CountryCode | District   | Info                    |
+------+------------+-------------+------------+-------------------------+
|    1 | Kabul      | AFG         | Kabol      |{"Population": 1780000}  |
|    2 | Qandahar   | AFG         | Qandahar   |{"Population": 237500}   |
|    3 | Herat      | AFG         | Herat      |{"Population": 186800}   |
...    ...          ...           ...          ...
| 4079 | Rafah      | PSE         | Rafah      |{"Population": 92020}    |
+------+------- ----+-------------+------------+-------------------------+
4082 rows in set (0.01 sec)

An empty set (no matching records) returns the following information:

Empty set (0.00 sec)

Filter Searches

To issue a query that returns a set of table columns, use the select() method and specify the
columns to return between square brackets. This query returns the Name and CountryCode columns
from the city table.

mysql-py> db.city.select(["Name", "CountryCode"])
+-------------------+-------------+
| Name              | CountryCode |
+-------------------+-------------+
| Kabul             | AFG         |
| Qandahar          | AFG         |
| Herat             | AFG         |
| Mazar-e-Sharif    | AFG         |
| Amsterdam         | NLD         |
...                 ...
| Rafah             | PSE         |
| Olympia           | USA         |
| Little Falls      | USA         |

4098

Relational Tables

| Happy Valley      | USA         |
+-------------------+-------------+
4082 rows in set (0.00 sec)

To issue a query that returns rows matching specific search conditions, use the where() method to
include those conditions. For example, the following example returns the names and country codes of
the cities that start with the letter Z.

mysql-py> db.city.select(["Name", "CountryCode"]).where("Name like 'Z%'")
+-------------------+-------------+
| Name              | CountryCode |
+-------------------+-------------+
| Zaanstad          | NLD         |
| Zoetermeer        | NLD         |
| Zwolle            | NLD         |
| Zenica            | BIH         |
| Zagazig           | EGY         |
| Zaragoza          | ESP         |
| Zamboanga         | PHL         |
| Zahedan           | IRN         |
| Zanjan            | IRN         |
| Zabol             | IRN         |
| Zama              | JPN         |
| Zhezqazghan       | KAZ         |
| Zhengzhou         | CHN         |
...                 ...
| Zeleznogorsk      | RUS         |
+-------------------+-------------+
59 rows in set (0.00 sec)

You can separate a value from the search condition by using the bind() method. For example,
instead of using "Name = 'Z%' " as the condition, substitute a named placeholder consisting of a colon
followed by a name that begins with a letter, such as name. Then include the placeholder and value in
the bind() method as follows:

mysql-py> db.city.select(["Name", "CountryCode"]).where(
"Name like :name").bind("name", "Z%")

Tip

Within a program, binding enables you to specify placeholders in your
expressions, which are filled in with values before execution and can benefit
from automatic escaping, as appropriate.

Always use binding to sanitize input. Avoid introducing values in queries using
string concatenation, which can produce invalid input and, in some cases, can
cause security issues.

Project Results

To issue a query using the AND operator, add the operator between search conditions in the where()
method.

mysql-py> db.city.select(["Name", "CountryCode"]).where(
"Name like 'Z%' and CountryCode = 'CHN'")
+----------------+-------------+
| Name           | CountryCode |
+----------------+-------------+
| Zhengzhou      | CHN         |
| Zibo           | CHN         |
| Zhangjiakou    | CHN         |
| Zhuzhou        | CHN         |
| Zhangjiang     | CHN         |
| Zigong         | CHN         |
| Zaozhuang      | CHN         |
...              ...
| Zhangjiagang   | CHN         |
+----------------+-------------+

4099

Relational Tables

22 rows in set (0.01 sec)

To specify multiple conditional operators, you can enclose the search conditions in parenthesis to
change the operator precedence. The following example demonstrates the placement of AND and OR
operators.

mysql-py> db.city.select(["Name", "CountryCode"]).where(
"Name like 'Z%' and (CountryCode = 'CHN' or CountryCode = 'RUS')")
+-------------------+-------------+
| Name              | CountryCode |
+-------------------+-------------+
| Zhengzhou         | CHN         |
| Zibo              | CHN         |
| Zhangjiakou       | CHN         |
| Zhuzhou           | CHN         |
...                 ...
| Zeleznogorsk      | RUS         |
+-------------------+-------------+
29 rows in set (0.01 sec)

Limit, Order, and Offset Results

You can apply the limit(), order_by(), and offset() methods to manage the number and order
of records returned by the select() method.

To specify the number of records included in a result set, append the limit() method with a value
to the select() method. For example, the following query returns the first five records in the country
table.

mysql-py> db.country.select(["Code", "Name"]).limit(5)
+------+-------------+
| Code | Name        |
+------+-------------+
| ABW  | Aruba       |
| AFG  | Afghanistan |
| AGO  | Angola      |
| AIA  | Anguilla    |
| ALB  | Albania     |
+------+-------------+
5 rows in set (0.00 sec)

To specify an order for the results, append the order_by() method to the select() method. Pass
to the order_by() method a list of one or more columns to sort by and, optionally, the descending
(desc) or ascending (asc) attribute as appropriate. Ascending order is the default order type.

For example, the following query sorts all records by the Name column and then returns the first three
records in descending order .

mysql-py> db.country.select(["Code", "Name"]).order_by(["Name desc"]).limit(3)
+------+------------+
| Code | Name       |
+------+------------+
| ZWE  | Zimbabwe   |
| ZMB  | Zambia     |
| YUG  | Yugoslavia |
+------+------------+
3 rows in set (0.00 sec)

By default, the limit() method starts from the first record in the table. You can use the offset()
method to change the starting record. For example, to ignore the first record and return the next three
records matching the condition, pass to the offset() method a value of 1.

mysql-py> db.country.select(["Code", "Name"]).order_by(["Name desc"]).limit(3).offset(1)
+------+------------+
| Code | Name       |
+------+------------+
| ZMB  | Zambia     |
| YUG  | Yugoslavia |

4100

Relational Tables

| YEM  | Yemen      |
+------+------------+
3 rows in set (0.00 sec)

Related Information

• The MySQL Reference Manual provides detailed documentation on functions and operators.

• See TableSelectFunction for the full syntax definition.

22.4.4.3 Update Tables

You can use the update() method to modify one or more records in a table. The update() method
works by filtering a query to include only the records to be updated and then applying the operations
you specify to those records.

To replace a city name in the city table, pass to the set() method the new city name. Then, pass to
the where() method the city name to locate and replace. The following example replaces the city
Peking with Beijing.

mysql-py> db.city.update().set("Name", "Beijing").where("Name = 'Peking'")

Use the select() method to verify the change.

mysql-py> db.city.select(["ID", "Name", "CountryCode", "District", "Info"]).where("Name = 'Beijing'")
+------+-----------+-------------+----------+-----------------------------+
| ID   | Name      | CountryCode | District | Info                        |
+------+-----------+-------------+----------+-----------------------------+
| 1891 | Beijing   | CHN         | Peking   | {"Population": 7472000}     |
+------+-----------+-------------+----------+-----------------------------+
1 row in set (0.00 sec)

Related Information

• See TableUpdateFunction for the full syntax definition.

22.4.4.4 Delete Tables

You can use the delete() method to remove some or all records from a table in a database. The X
DevAPI provides additional methods to use with the delete() method to filter and order the records
to be deleted.

Delete Records Using Conditions

The example that follows passes search conditions to the delete() method. All records matching the
condition are deleted from the city table. In this example, one record matches the condition.

mysql-py> db.city.delete().where("Name = 'Olympia'")

Delete the First Record

To delete the first record in the city table, use the limit() method with a value of 1.

mysql-py> db.city.delete().limit(1)

Delete All Records in a Table

You can delete all records in a table. To do so, use the delete() method without specifying a search
condition.

Caution

Use care when you delete records without specifying a search condition; doing
so deletes all records from the table.

4101

Documents in Tables

Drop a Table

The drop_collection() method is also used in MySQL Shell to drop a relational table from a
database. For example, to drop the citytest table from the world_x database, issue:

mysql-py> db.drop_collection("citytest")

Related Information

• See TableDeleteFunction for the full syntax definition.

• See Section 22.4.2, “Download and Import world_x Database” for instructions to recreate the

world_x database.

22.4.5 Documents in Tables

In MySQL, a table may contain traditional relational data, JSON values, or both. You can combine
traditional data with JSON documents by storing the documents in columns having a native JSON data
type.

Examples in this section use the city table in the world_x schema.

city Table Description

The city table has five columns (or fields).

+---------------+------------+-------+-------+---------+------------------+
| Field         | Type       | Null  | Key   | Default | Extra            |
+---------------+------------+-------+-------+---------+------------------+
| ID            | int(11)    | NO    | PRI   | null    | auto_increment   |
| Name          | char(35)   | NO    |       |         |                  |
| CountryCode   | char(3)    | NO    |       |         |                  |
| District      | char(20)   | NO    |       |         |                  |
| Info          | json       | YES   |       | null    |                  |
+---------------+------------+-------+-------+---------+------------------+

Insert a Record

To insert a document into the column of a table, pass to the values() method a well-formed JSON
document in the correct order. In the following example, a document is passed as the final value to be
inserted into the Info column.

mysql-py> db.city.insert().values(
None, "San Francisco", "USA", "California", '{"Population":830000}')

Select a Record

You can issue a query with a search condition that evaluates document values in the expression.

mysql-py> db.city.select(["ID", "Name", "CountryCode", "District", "Info"]).where(
"CountryCode = :country and Info->'$.Population' > 1000000").bind(
'country', 'USA')
+------+----------------+-------------+----------------+-----------------------------+
| ID   | Name           | CountryCode | District       | Info                        |
+------+----------------+-------------+----------------+-----------------------------+
| 3793 | New York       | USA         | New York       | {"Population": 8008278}     |
| 3794 | Los Angeles    | USA         | California     | {"Population": 3694820}     |
| 3795 | Chicago        | USA         | Illinois       | {"Population": 2896016}     |
| 3796 | Houston        | USA         | Texas          | {"Population": 1953631}     |
| 3797 | Philadelphia   | USA         | Pennsylvania   | {"Population": 1517550}     |
| 3798 | Phoenix        | USA         | Arizona        | {"Population": 1321045}     |
| 3799 | San Diego      | USA         | California     | {"Population": 1223400}     |
| 3800 | Dallas         | USA         | Texas          | {"Population": 1188580}     |
| 3801 | San Antonio    | USA         | Texas          | {"Population": 1144646}     |
+------+----------------+-------------+----------------+-----------------------------+
9 rows in set (0.01 sec)

4102

X Plugin

Related Information

• See Working with Relational Tables and Documents for more information.

• See Section 13.5, “The JSON Data Type” for a detailed description of the data type.

22.5 X Plugin

This section explains how to use, configure and monitor X Plugin.

22.5.1 Checking X Plugin Installation

X Plugin is enabled by default in MySQL 8, therefore installing or upgrading to MySQL 8 makes the
plugin available. You can verify X Plugin is installed on an instance of MySQL server by using the SHOW
plugins statement to view the plugins list.

To use MySQL Shell to verify X Plugin is installed, issue:

$> mysqlsh -u user --sqlc -P 3306 -e "SHOW plugins"

To use MySQL Client to verify X Plugin is installed, issue:

$> mysql -u user -p -e "SHOW plugins"

An example result if X Plugin is installed is highlighted here:

+----------------------------+----------+--------------------+---------+---------+
| Name                       | Status   | Type               | Library | License |
+----------------------------+----------+--------------------+---------+---------+

...

| mysqlx                     | ACTIVE   | DAEMON             | NULL    | GPL     |

...

+----------------------------+----------+--------------------+---------+---------+

22.5.2 Disabling X Plugin

The X Plugin can be disabled at startup by either setting mysqlx=0 in your MySQL configuration file,
or by passing in either --mysqlx=0 or --skip-mysqlx when starting the MySQL server.

Alternatively, use the -DWITH_MYSQLX=OFF CMake option to compile MySQL Server without X Plugin.

22.5.3 Using Encrypted Connections with X Plugin

This section explains how to configure X Plugin to use encrypted connections. For more background
information, see Section 8.3, “Using Encrypted Connections”.

To enable configuring support for encrypted connections, X Plugin has mysqlx_ssl_xxx system
variables, which can have different values from the ssl_xxx system variables used with MySQL
Server. For example, X Plugin can have SSL key, certificate, and certificate authority files that
differ from those used for MySQL Server. These variables are described at Section 22.5.6.2, “X
Plugin Options and System Variables”. Similarly, X Plugin has its own Mysqlx_ssl_xxx status
variables that correspond to the MySQL Server encrypted-connection Ssl_xxx status variables. See
Section 22.5.6.3, “X Plugin Status Variables”.

At initialization, X Plugin determines its TLS context for encrypted connections as follows:

• If all mysqlx_ssl_xxx system variables have their default values, X Plugin uses the same TLS

context as the MySQL Server main connection interface, which is determined by the values of the
ssl_xxx system variables.

4103

Connection Compression with X Plugin

over an X Protocol connection with SSL, to supply the password to the X Plugin authentication cache.
Once this initial authentication over SSL has succeeded, non-SSL X Protocol connections can be used.

It is possible to disable the mysqlx_cache_cleaner plugin by starting the MySQL server with
the option --mysqlx_cache_cleaner=0. If you do this, the X Plugin authentication cache is
disabled, and therefore SSL must always be used for X Protocol connections when authenticating with
SHA256_MEMORY authentication.

22.5.5 Connection Compression with X Plugin

From MySQL 8.0.19, X Plugin supports compression of messages sent over X Protocol connections.
Connections can be compressed if the server and the client agree on a mutually supported
compression algorithm. Enabling compression reduces the number of bytes sent over the network, but
adds to the server and client an additional CPU cost for compression and decompression operations.
The benefits of compression therefore occur primarily when there is low network bandwidth, network
transfer time dominates the cost of compression and decompression operations, and result sets are
large.

Note

Different MySQL clients implement support for connection compression
differently; consult your client documentation for details. For example, for classic
MySQL protocol connections, see Section 6.2.8, “Connection Compression
Control”.

• Configuring Connection Compression for X Plugin

• Compressed Connection Characteristics for X Plugin

• Monitoring Connection Compression for X Plugin

Configuring Connection Compression for X Plugin

By default, X Plugin supports the zstd, LZ4, and Deflate compression algorithms. Compression with the
Deflate algorithm is carried out using the zlib software library, so the deflate_stream compression
algorithm setting for X Protocol connections is equivalent to the zlib setting for classic MySQL
protocol connections.

On the server side, you can disallow any of the compression algorithms by setting the
mysqlx_compression_algorithms system variable to include only those permitted. The algorithm
names zstd_stream, lz4_message, and deflate_stream can be specified in any combination,
and the order and lettercase are not important. If the system variable value is the empty string, no
compression algorithms are permitted and connections are uncompressed.

The following table compares the characteristics of the different compression algorithms and shows
their assigned priorities. By default, the server chooses the highest-priority algorithm permitted in
common by the server and the client; clients may change the priorities as described later. The short
form alias for the algorithms can be used by clients when specifying them.

Table 22.1 X Protocol Compression Algorithm Characteristics

Algorithm

Alias

Compression
Ratio

Throughput

CPU Cost

Default Priority

zsth_stream zstd

lz4_message lz4

deflate_streamdeflate

High

Low

High

High

High

Low

Medium

Lowest

Highest

First

Second

Third

The X Protocol set of permitted compression algorithms (whether user-specified or default) is
independent of the set of compression algorithms permitted by MySQL Server for classic MySQL
protocol connections, which is specified by the protocol_compression_algorithms server

4105

Connection Compression with X Plugin

compression levels are initially set to 11 for zstd, 8 for LZ4, and 5 for Deflate. You can
adjust these settings using the mysqlx_zstd_max_client_compression_level,
mysqlx_lz4_max_client_compression_level, and
mysqlx_deflate_max_client_compression_level system variables.

If the server and client permit more than one algorithm in common, the default priority order for
choosing an algorithm during negotiation is shown in Table 22.1, “X Protocol Compression Algorithm
Characteristics”. From MySQL 8.0.22, for clients that support specifying compression algorithms, the
connection request can include a list of algorithms permitted by the client, specified using the algorithm
name or its alias. The order of these algorithms in the list is taken as a priority order by the server. The
algorithm used in this case is the first of those in the client list that is also permitted on the server side.
However, the option for compression algorithms is subject to the compression mode:

• If the compression mode is disabled, the compression algorithms option is ignored.

• If the compression mode is preferred but no algorithm permitted on the client side is permitted on

the server side, the connection is uncompressed.

• If the compression mode is required but no algorithm permitted on the client side is permitted on

the server side, an error occurs.

To monitor the effects of message compression, use the X Plugin status variables described in
Monitoring Connection Compression for X Plugin. You can use these status variables to calculate
the benefit of message compression with your current settings, and use that information to tune your
settings.

Compressed Connection Characteristics for X Plugin

X Protocol connection compression operates with the following behaviors and boundaries:

• The _stream and _message suffixes in algorithm names refer to two different operational modes:
In stream mode, all X Protocol messages in a single connection are compressed into a continuous
stream and must be decompressed in the same manner—following the order they were compressed
and without skipping any messages. In message mode, each message is compressed individually
and independently, and need not be decompressed in the order in which they were compressed.
Also, message mode does not require all compressed messages to be decompressed.

• Compression is not applied to any messages that are sent before authentication succeeds.

• Compression is not applied to control flow messages such as Mysqlx.Ok, Mysqlx.Error, and

Mysqlx.Sql.StmtExecuteOk messages.

• All other X Protocol messages can be compressed if the server and client agree on a mutually
permitted compression algorithm during capability negotiation. If the client does not request
compression at that stage, neither the client nor the server applies compression to messages.

• When messages sent over X Protocol connections are compressed, the limit specified by the

mysqlx_max_allowed_packet system variable still applies. The network packet must be smaller
than this limit after the message payload has been decompressed. If the limit is exceeded, X Plugin
returns a decompression error and closes the connection.

• The following points pertain to compression level requests by clients, which is supported only by

MySQL Shell:

• Compression levels must be specified by the client as an integer. If any other type of value is

supplied, the connection closes with an error.

• If a client specifies an algorithm but not a compression level, the server uses its default

compression level for the algorithm.

• If a client requests an algorithm compression level that exceeds the server maximum permitted

level, the server uses the maximum permitted level.

4107

X Plugin Options and Variables

• If a client requests an algorithm compression level that is less than the server minimum permitted

level, the server uses the minimum permitted level.

Monitoring Connection Compression for X Plugin

You can monitor the effects of message compression using the X Plugin status variables. When
message compression is in use, the session Mysqlx_compression_algorithm status
variable shows which compression algorithm is in use for the current X Protocol connection, and
Mysqlx_compression_level shows the compression level that was selected. These session status
variables are available from MySQL 8.0.20.

From MySQL 8.0.19, X Plugin status variables can be used to calculate the efficiency of the
compression algorithms that are selected (the data compression ratio), and the overall effect of using
message compression. Use the session value of the status variables in the following calculations to
see what the benefit of message compression was for a specific session with a known compression
algorithm. Or use the global value of the status variables to check the overall benefit of message
compression for your server across all sessions using X Protocol connections, including all the
compression algorithms that have been used for those sessions, and all sessions that did not
use message compression. You can then tune message compression by adjusting the permitted
compression algorithms, maximum compression level, and default compression level, as described in
Configuring Connection Compression for X Plugin.

When message compression is in use, the Mysqlx_bytes_sent status variable shows the total
number of bytes sent out from the server, including compressed message payloads measured after
compression, any items in compressed messages that were not compressed such as X Protocol
headers, and any uncompressed messages. The Mysqlx_bytes_sent_compressed_payload
status variable shows the total number of bytes sent as compressed message payloads, measured
after compression, and the Mysqlx_bytes_sent_uncompressed_frame status variable shows
the total number of bytes for those same message payloads but measured before compression.
The compression ratio, which shows the efficiency of the compression algorithm, can therefore be
calculated using the following expression:

mysqlx_bytes_sent_uncompressed_frame / mysqlx_bytes_sent_compressed_payload

The effectiveness of compression for X Protocol messages sent by the server can be calculated using
the following expression:

(mysqlx_bytes_sent - mysqlx_bytes_sent_compressed_payload + mysqlx_bytes_sent_uncompressed_frame) / mysqlx_bytes_sent

For messages received by the server from clients, the
Mysqlx_bytes_received_compressed_payload status variable shows the total number
of bytes received as compressed message payloads, measured before decompression, and
the Mysqlx_bytes_received_uncompressed_frame status variable shows the total
number of bytes for those same message payloads but measured after decompression. The
Mysqlx_bytes_received status variable includes compressed message payloads measured
before decompression, any uncompressed items in compressed messages, and any uncompressed
messages.

22.5.6 X Plugin Options and Variables

This section describes the command options and system variables that configure X Plugin, as well
as the status variables available for monitoring purposes. If configuration values specified at startup
time are incorrect, X Plugin could fail to initialize properly and the server does not load it. In this case,
the server could also produce error messages for other X Plugin settings because it cannot recognize
them.

22.5.6.1 X Plugin Option and Variable Reference

This table provides an overview of the command options, system variables, and status variables
provided by X Plugin.

4108

X Plugin Options and Variables

Table 22.2 X Plugin Option and Variable Reference

Name

mysqlx

Cmd-Line

Option File System Var Status Var

Var Scope

Dynamic

Yes

Yes

Mysqlx_aborted_clients

Mysqlx_address

mysqlx_bind_address

Yes

Yes

Yes

Mysqlx_bytes_received

Mysqlx_bytes_received_compressed_payload

Mysqlx_bytes_received_uncompressed_frame

Mysqlx_bytes_sent

Mysqlx_bytes_sent_compressed_payload

Mysqlx_bytes_sent_uncompressed_frame

Mysqlx_compression_algorithm

Yes
mysqlx_compression_algorithms
Yes

Mysqlx_compression_level

mysqlx_connect_timeout

Yes

Yes

Mysqlx_connection_accept_errors

Mysqlx_connection_errors

Mysqlx_connections_accepted

Mysqlx_connections_closed

Mysqlx_connections_rejected

Mysqlx_crud_create_view

Mysqlx_crud_delete

Mysqlx_crud_drop_view

Mysqlx_crud_find

Mysqlx_crud_insert

Mysqlx_crud_modify_view

Mysqlx_crud_update

mysqlx_deflate_default_compression_level

Yes

Yes

Yes

Yes

Yes

Yes
mysqlx_deflate_max_client_compression_level

Yes

Yes

mysqlx_document_id_unique_prefix

Yes

Yes

mysqlx_enable_hello_notice

Yes

Yes

Mysqlx_errors_sent

Mysqlx_errors_unknown_message_type

Mysqlx_expect_close

Mysqlx_expect_open

mysqlx_idle_worker_thread_timeout

Yes

Yes

Mysqlx_init_error

mysqlx_interactive_timeout

Yes

Yes

mysqlx_lz4_default_compression_level

Yes

Yes

mysqlx_lz4_max_client_compression_level

Yes

Yes

mysqlx_max_allowed_packet

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Both

Both

Both

Both

Both

Both

Session

Global

Session

Global

Both

Both

Global

Global

Global

Both

Both

Both

Both

Both

Both

Both

Global

Global

Global

Global

Both

Both

Both

Both

Global

Both

Global

Global

Global

Global

No

No

No

No

No

No

No

No

No

No

Yes

No

Yes

No

No

No

No

No

No

No

No

No

No

No

No

Yes

Yes

Yes

Yes

No

No

No

No

Yes

No

Yes

Yes

Yes

Yes

4109

X Plugin Options and Variables

Name

Cmd-Line

Option File System Var Status Var

Var Scope

Dynamic

Mysqlx_stmt_create_collection_index

Mysqlx_stmt_disable_notices

Mysqlx_stmt_drop_collection

Mysqlx_stmt_drop_collection_index

Mysqlx_stmt_enable_notices

Mysqlx_stmt_ensure_collection

Mysqlx_stmt_execute_mysqlx

Mysqlx_stmt_execute_sql

Mysqlx_stmt_execute_xplugin

Mysqlx_stmt_get_collection_options

Mysqlx_stmt_kill_client

Mysqlx_stmt_list_clients

Mysqlx_stmt_list_notices

Mysqlx_stmt_list_objects

Mysqlx_stmt_modify_collection_options

Mysqlx_stmt_ping

mysqlx_wait_timeout

Yes

Yes

Yes

Mysqlx_worker_threads

Mysqlx_worker_threads_active

mysqlx_write_timeout

Yes

Yes

mysqlx_zstd_default_compression_level

Yes

Yes

Yes

Yes

mysqlx_zstd_max_client_compression_level

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Session

Global

Global

Session

Global

Global

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Yes

No

No

Yes

Yes

Yes

22.5.6.2 X Plugin Options and System Variables

To control activation of X Plugin, use this option:

• --mysqlx[=value]

Command-Line Format

Type

Default Value

Valid Values

--mysqlx[=value]

Enumeration

ON

ON

OFF

FORCE

FORCE_PLUS_PERMANENT

This option controls how the server loads X Plugin at startup. In MySQL 8.0, X Plugin is enabled by
default, but this option may be used to control its activation state.

The option value should be one of those available for plugin-loading options, as described in
Section 7.6.1, “Installing and Uninstalling Plugins”.

If X Plugin is enabled, it exposes several system variables that permit control over its operation:

• mysqlx_bind_address

4111

X Plugin Options and Variables

• For a given address, the network namespace is optional. If given, it must be specified as a /ns

suffix immediately following the address.

• An address with no /ns suffix uses the host system global namespace. The global namespace is

therefore the default.

• An address with a /ns suffix uses the namespace named ns.

• The host system must support network namespaces and each named namespace must previously

have been set up. Naming a nonexistent namespace produces an error.

• If the variable value specifies multiple addresses, it can include addresses in the global

namespace, in named namespaces, or a mix.

For additional information about network namespaces, see Section 7.1.14, “Network Namespace
Support”.

Important

Because X Plugin is not a mandatory plugin, it does not prevent server
startup if there is an error in the specified address or list of addresses (as
MySQL Server does for bind_address errors). With X Plugin, if one of
the listed addresses cannot be parsed or if X Plugin cannot bind to it, the
address is skipped, an error message is logged, and X Plugin attempts to
bind to each of the remaining addresses. X Plugin's Mysqlx_address
status variable displays only those addresses from the list for which the
bind succeeded. If none of the listed addresses results in a successful
bind, or if a single specified address fails, X Plugin logs the error message
ER_XPLUGIN_FAILED_TO_PREPARE_IO_INTERFACES stating that X
Protocol cannot be used. mysqlx_bind_address is not dynamic, so to fix
any issues you must stop the server, correct the system variable value, and
restart the server.

• mysqlx_compression_algorithms

Command-Line Format

Introduced

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Valid Values

--mysqlx-compression-
algorithms=value

8.0.19

mysqlx_compression_algorithms

Global

Yes

No

Set

deflate_stream,lz4_message,zstd_stream

deflate_stream

lz4_message

zstd_stream

The compression algorithms that are permitted for use on X Protocol connections. By default,
the Deflate, LZ4, and zstd algorithms are all permitted. To disallow any of the algorithms, set
mysqlx_compression_algorithms to include only the ones you permit. The algorithm names
deflate_stream, lz4_message, and zstd_stream can be specified in any combination, and the
order and case are not important. If you set the system variable to the empty string, no compression
algorithms are permitted and only uncompressed connections are used. Use the algorithm-specific

4113

X Plugin Options and Variables

system variables to adjust the default and maximum compression level for each permitted algorithm.
For more details, and information on how connection compression for X Protocol relates to the
equivalent settings for MySQL Server, see Section 22.5.5, “Connection Compression with X Plugin”.

• mysqlx_connect_timeout

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

Unit

--mysqlx-connect-timeout=#

mysqlx_connect_timeout

Global

Yes

No

Integer

30

1

1000000000

seconds

The number of seconds X Plugin waits for the first packet to be received from newly connected
clients. This is the X Plugin equivalent of connect_timeout; see that variable description for more
information.

• mysqlx_deflate_default_compression_level

Command-Line Format

Introduced

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

--
mysqlx_deflate_default_compression_level=#

8.0.20

mysqlx_deflate_default_compression_level

Global

Yes

No

Integer

3

1

9

The default compression level that the server uses for the Deflate algorithm on X Protocol
connections. Specify the level as an integer from 1 (the lowest compression effort) to 9 (the
highest effort). This level is used if the client does not request a compression level during capability
negotiation. If you do not specify this system variable, the server uses level 3 as the default. For
more information, see Section 22.5.5, “Connection Compression with X Plugin”.

• mysqlx_deflate_max_client_compression_level

Command-Line Format

Introduced

System Variable

Scope

Dynamic

SET_VAR Hint Applies

--
mysqlx_deflate_max_client_compression_level=#

8.0.20

mysqlx_deflate_max_client_compression_level

Global

Yes

No

4114

X Plugin Options and Variables

Type

Default Value

Minimum Value

Maximum Value

Integer

5

1

9

The maximum compression level that the server permits for the Deflate algorithm on X Protocol
connections. The range is the same as for the default compression level for this algorithm. If the
client requests a higher compression level than this, the server uses the level you set here. If you do
not specify this system variable, the server sets a maximum compression level of 5.

• mysqlx_document_id_unique_prefix

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

--mysqlx-document-id-unique-prefix=#

mysqlx_document_id_unique_prefix

Global

Yes

No

Integer

0

0

65535

Sets the first 4 bytes of document IDs generated by the server when documents are added to a
collection. By setting this variable to a unique value per instance, you can ensure document IDs are
unique across instances. See Understanding Document IDs.

• mysqlx_enable_hello_notice

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

--mysqlx-enable-hello-notice[={OFF|
ON}]

mysqlx_enable_hello_notice

Global

Yes

No

Boolean

ON

Controls messages sent to classic MySQL protocol clients that try to connect over X Protocol. When
enabled, clients which do not support X Protocol that attempt to connect to the server X Protocol port
receive an error explaining they are using the wrong protocol.

• mysqlx_idle_worker_thread_timeout

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

--mysqlx-idle-worker-thread-
timeout=#

mysqlx_idle_worker_thread_timeout

Global

Yes

No

Integer

4115

X Plugin Options and Variables

Default Value

Minimum Value

Maximum Value

Unit

60

0

3600

seconds

The number of seconds after which idle worker threads are terminated.

• mysqlx_interactive_timeout

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

Unit

--mysqlx-interactive-timeout=#

mysqlx_interactive_timeout

Global

Yes

No

Integer

28800

1

2147483

seconds

The default value of the mysqlx_wait_timeout session variable for interactive clients. (The
number of seconds to wait for interactive clients to timeout.)

• mysqlx_lz4_default_compression_level

Command-Line Format

Introduced

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

--
mysqlx_lz4_default_compression_level=#

8.0.20

mysqlx_lz4_default_compression_level

Global

Yes

No

Integer

2

0

16

The default compression level that the server uses for the LZ4 algorithm on X Protocol connections.
Specify the level as an integer from 0 (the lowest compression effort) to 16 (the highest effort). This
level is used if the client does not request a compression level during capability negotiation. If you
do not specify this system variable, the server uses level 2 as the default. For more information, see
Section 22.5.5, “Connection Compression with X Plugin”.

• mysqlx_lz4_max_client_compression_level

Command-Line Format

Introduced

System Variable

4116

--
mysqlx_lz4_max_client_compression_level=#

8.0.20

mysqlx_lz4_max_client_compression_level

X Plugin Options and Variables

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

Global

Yes

No

Integer

8

0

16

The maximum compression level that the server permits for the LZ4 algorithm on X Protocol
connections. The range is the same as for the default compression level for this algorithm. If the
client requests a higher compression level than this, the server uses the level you set here. If you do
not specify this system variable, the server sets a maximum compression level of 8.

• mysqlx_max_allowed_packet

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

Unit

--mysqlx-max-allowed-packet=#

mysqlx_max_allowed_packet

Global

Yes

No

Integer

67108864

512

1073741824

bytes

The maximum size of network packets that can be received by X Plugin. This limit also applies when
compression is used for the connection, so the network packet must be smaller than this size after
the message has been decompressed. This is the X Plugin equivalent of max_allowed_packet;
see that variable description for more information.

• mysqlx_max_connections

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

--mysqlx-max-connections=#

mysqlx_max_connections

Global

Yes

No

Integer

100

1

65535

The maximum number of concurrent client connections X Plugin can accept. This is the X Plugin
equivalent of max_connections; see that variable description for more information.

For modifications to this variable, if the new value is smaller than the current number of connections,
the new limit is taken into account only for new connections.

• mysqlx_min_worker_threads

4117

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

X Plugin Options and Variables

--mysqlx-min-worker-threads=#

mysqlx_min_worker_threads

Global

Yes

No

Integer

2

1

100

The minimum number of worker threads used by X Plugin for handling client requests.

• mysqlx_port

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

--mysqlx-port=port_num

mysqlx_port

Global

No

No

Integer

33060

1

65535

The network port on which X Plugin listens for TCP/IP connections. This is the X Plugin equivalent of
port; see that variable description for more information.

• mysqlx_port_open_timeout

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

Unit

--mysqlx-port-open-timeout=#

mysqlx_port_open_timeout

Global

No

No

Integer

0

0

120

seconds

The number of seconds X Plugin waits for a TCP/IP port to become free.

• mysqlx_read_timeout

Command-Line Format

System Variable

Scope

4118

--mysqlx-read-timeout=#

mysqlx_read_timeout

Session

X Plugin Options and Variables

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

Unit

Yes

No

Integer

30

1

2147483

seconds

The number of seconds that X Plugin waits for blocking read operations to complete. After this time,
if the read operation is not successful, X Plugin closes the connection and returns a warning notice
with the error code ER_IO_READ_ERROR to the client application.

• mysqlx_socket

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

--mysqlx-socket=file_name

mysqlx_socket

Global

No

No

String

/tmp/mysqlx.sock

The path to a Unix socket file which X Plugin uses for connections. This setting is only used by
MySQL Server when running on Unix operating systems. Clients can use this socket to connect to
MySQL Server using X Plugin.

The default mysqlx_socket path and file name is based on the default path and file name for the
main socket file for MySQL Server, with the addition of an x appended to the file name. The default
path and file name for the main socket file is /tmp/mysql.sock, therefore the default path and file
name for the X Plugin socket file is /tmp/mysqlx.sock.

If you specify an alternative path and file name for the main socket file at server startup using the
socket system variable, this does not affect the default for the X Plugin socket file. In this situation,
if you want to store both sockets at a single path, you must set the mysqlx_socket system variable
as well. For example in a configuration file:

socket=/home/sockets/mysqld/mysql.sock
mysqlx_socket=/home/sockets/xplugin/xplugin.sock

If you change the default path and file name for the main socket file at compile time using the
MYSQL_UNIX_ADDR compile option, this does affect the default for the X Plugin socket file, which is
formed by appending an x to the MYSQL_UNIX_ADDR file name. If you want to set a different default
for the X Plugin socket file at compile time, use the MYSQLX_UNIX_ADDR compile option.

The MYSQLX_UNIX_PORT environment variable can also be used to set a default for the X
Plugin socket file at server startup (see Section 6.9, “Environment Variables”). If you set this
environment variable, it overrides the compiled MYSQLX_UNIX_ADDR value, but is overridden by the
mysqlx_socket value.

• mysqlx_ssl_ca

Command-Line Format

--mysqlx-ssl-ca=file_name

System Variable

Scope

mysqlx_ssl_ca

Global

4119

X Plugin Options and Variables

• mysqlx_ssl_crl

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

--mysqlx-ssl-crl=file_name

mysqlx_ssl_crl

Global

No

No

File name

NULL

The mysqlx_ssl_crl system variable is like ssl_crl, except that it applies to X Plugin rather
than the MySQL Server main connection interface. For information about configuring encryption
support for X Plugin, see Section 22.5.3, “Using Encrypted Connections with X Plugin”.

• mysqlx_ssl_crlpath

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

--mysqlx-ssl-crlpath=dir_name

mysqlx_ssl_crlpath

Global

No

No

Directory name

NULL

The mysqlx_ssl_crlpath system variable is like ssl_crlpath, except that it applies to X
Plugin rather than the MySQL Server main connection interface. For information about configuring
encryption support for X Plugin, see Section 22.5.3, “Using Encrypted Connections with X Plugin”.

• mysqlx_ssl_key

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

--mysqlx-ssl-key=file_name

mysqlx_ssl_key

Global

No

No

File name

NULL

The mysqlx_ssl_key system variable is like ssl_key, except that it applies to X Plugin rather
than the MySQL Server main connection interface. For information about configuring encryption
support for X Plugin, see Section 22.5.3, “Using Encrypted Connections with X Plugin”.

• mysqlx_wait_timeout

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

--mysqlx-wait-timeout=#

mysqlx_wait_timeout

Session

Yes

No

Integer

4121

X Plugin Options and Variables

Default Value

Minimum Value

Maximum Value

Unit

28800

1

2147483

seconds

The number of seconds that X Plugin waits for activity on a connection. After this time, if the read
operation is not successful, X Plugin closes the connection. If the client is noninteractive, the initial
value of the session variable is copied from the global mysqlx_wait_timeout variable. For
interactive clients, the initial value is copied from the session mysqlx_interactive_timeout.

• mysqlx_write_timeout

Command-Line Format

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

Unit

--mysqlx-write-timeout=#

mysqlx_write_timeout

Session

Yes

No

Integer

60

1

2147483

seconds

The number of seconds that X Plugin waits for blocking write operations to complete. After this time,
if the write operation is not successful, X Plugin closes the connection.

• mysqlx_zstd_default_compression_level

Command-Line Format

Introduced

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

--
mysqlx_zstd_default_compression_level=#

8.0.20

mysqlx_zstd_default_compression_level

Global

Yes

No

Integer

3

-131072

22

The default compression level that the server uses for the zstd algorithm on X Protocol connections.
For versions of the zstd library from 1.4.0, you can set positive values from 1 to 22 (the highest
compression effort), or negative values which represent progressively lower effort. A value of 0 is
converted to a value of 1. For earlier versions of the zstd library, you can only specify the value 3.
This level is used if the client does not request a compression level during capability negotiation. If
you do not specify this system variable, the server uses level 3 as the default. For more information,
see Section 22.5.5, “Connection Compression with X Plugin”.

4122

X Plugin Options and Variables

• mysqlx_zstd_max_client_compression_level

Command-Line Format

Introduced

System Variable

Scope

Dynamic

SET_VAR Hint Applies

Type

Default Value

Minimum Value

Maximum Value

--
mysqlx_zstd_max_client_compression_level=#

8.0.20

mysqlx_zstd_max_client_compression_level

Global

Yes

No

Integer

11

-131072

22

The maximum compression level that the server permits for the zstd algorithm on X Protocol
connections. The range is the same as for the default compression level for this algorithm. If the
client requests a higher compression level than this, the server uses the level you set here. If you do
not specify this system variable, the server sets a maximum compression level of 11.

22.5.6.3 X Plugin Status Variables

The X Plugin status variables have the following meanings.

• Mysqlx_aborted_clients

The number of clients that were disconnected because of an input or output error.

• Mysqlx_address

The network address or addresses for which X Plugin accepts TCP/IP connections. If multiple
addresses were specified using the mysqlx_bind_address system variable, Mysqlx_address
displays only those addresses for which the bind succeeded. If the bind has failed for every network
address specified by mysqlx_bind_address, or if the skip_networking option has been used,
the value of Mysqlx_address is UNDEFINED. If X Plugin startup is not yet complete, the value of
Mysqlx_address is empty.

• Mysqlx_bytes_received

The total number of bytes received through the network. If compression is used for the connection,
this figure comprises compressed message payloads measured before decompression
(Mysqlx_bytes_received_compressed_payload), any items in compressed messages that
were not compressed such as X Protocol headers, and any uncompressed messages.

• Mysqlx_bytes_received_compressed_payload

The number of bytes received as compressed message payloads, measured before decompression.

• Mysqlx_bytes_received_uncompressed_frame

The number of bytes received as compressed message payloads, measured after decompression.

• Mysqlx_bytes_sent

The total number of bytes sent through the network. If compression is used for the connection,
this figure comprises compressed message payloads measured after compression
(Mysqlx_bytes_sent_compressed_payload), any items in compressed messages that were
not compressed such as X Protocol headers, and any uncompressed messages.

4123

X Plugin Options and Variables

• Mysqlx_bytes_sent_compressed_payload

The number of bytes sent as compressed message payloads, measured after compression.

• Mysqlx_bytes_sent_uncompressed_frame

The number of bytes sent as compressed message payloads, measured before compression.

• Mysqlx_compression_algorithm

(Session scope) The compression algorithm in use for the X Protocol connection for this session.
The permitted compression algorithms are listed by the mysqlx_compression_algorithms
system variable.

• Mysqlx_compression_level

(Session scope) The compression level in use for the X Protocol connection for this session.

• Mysqlx_connection_accept_errors

The number of connections which have caused accept errors.

• Mysqlx_connection_errors

The number of connections which have caused errors.

• Mysqlx_connections_accepted

The number of connections which have been accepted.

• Mysqlx_connections_closed

The number of connections which have been closed.

• Mysqlx_connections_rejected

The number of connections which have been rejected.

• Mysqlx_crud_create_view

The number of create view requests received.

• Mysqlx_crud_delete

The number of delete requests received.

• Mysqlx_crud_drop_view

The number of drop view requests received.

• Mysqlx_crud_find

The number of find requests received.

• Mysqlx_crud_insert

The number of insert requests received.

• Mysqlx_crud_modify_view

The number of modify view requests received.

• Mysqlx_crud_update

The number of update requests received.

4124

X Plugin Options and Variables

• Mysqlx_cursor_close

The number of cursor-close messages received

• Mysqlx_cursor_fetch

The number of cursor-fetch messages received

• Mysqlx_cursor_open

The number of cursor-open messages received

• Mysqlx_errors_sent

The number of errors sent to clients.

• Mysqlx_errors_unknown_message_type

The number of unknown message types that have been received.

• Mysqlx_expect_close

The number of expectation blocks closed.

• Mysqlx_expect_open

The number of expectation blocks opened.

• Mysqlx_init_error

The number of errors during initialisation.

• Mysqlx_messages_sent

The total number of messages of all types sent to clients.

• Mysqlx_notice_global_sent

The number of global notifications sent to clients.

• Mysqlx_notice_other_sent

The number of other types of notices sent back to clients.

• Mysqlx_notice_warning_sent

The number of warning notices sent back to clients.

• Mysqlx_notified_by_group_replication

Number of Group Replication notifications sent to clients.

• Mysqlx_port

The TCP port which X Plugin is listening to. If a network bind has failed, or if the skip_networking
system variable is enabled, the value shows UNDEFINED.

• Mysqlx_prep_deallocate

The number of prepared-statement-deallocate messages received

• Mysqlx_prep_execute

The number of prepared-statement-execute messages received

4125

X Plugin Options and Variables

• Mysqlx_prep_prepare

The number of prepared-statement messages received

• Mysqlx_rows_sent

The number of rows sent back to clients.

• Mysqlx_sessions

The number of sessions that have been opened.

• Mysqlx_sessions_accepted

The number of session attempts which have been accepted.

• Mysqlx_sessions_closed

The number of sessions that have been closed.

• Mysqlx_sessions_fatal_error

The number of sessions that have closed with a fatal error.

• Mysqlx_sessions_killed

The number of sessions which have been killed.

• Mysqlx_sessions_rejected

The number of session attempts which have been rejected.

• Mysqlx_socket

The Unix socket which X Plugin is listening to.

• Mysqlx_ssl_accept_renegotiates

The number of negotiations needed to establish the connection.

• Mysqlx_ssl_accepts

The number of accepted SSL connections.

• Mysqlx_ssl_active

If SSL is active.

• Mysqlx_ssl_cipher

The current SSL cipher (empty for non-SSL connections).

• Mysqlx_ssl_cipher_list

A list of possible SSL ciphers (empty for non-SSL connections).

• Mysqlx_ssl_ctx_verify_depth

The certificate verification depth limit currently set in ctx.

• Mysqlx_ssl_ctx_verify_mode

The certificate verification mode currently set in ctx.

• Mysqlx_ssl_finished_accepts

4126

X Plugin Options and Variables

The number of successful SSL connections to the server.

• Mysqlx_ssl_server_not_after

The last date for which the SSL certificate is valid.

• Mysqlx_ssl_server_not_before

The first date for which the SSL certificate is valid.

• Mysqlx_ssl_verify_depth

The certificate verification depth for SSL connections.

• Mysqlx_ssl_verify_mode

The certificate verification mode for SSL connections.

• Mysqlx_ssl_version

The name of the protocol used for SSL connections.

• Mysqlx_stmt_create_collection

The number of create collection statements received.

• Mysqlx_stmt_create_collection_index

The number of create collection index statements received.

• Mysqlx_stmt_disable_notices

The number of disable notice statements received.

• Mysqlx_stmt_drop_collection

The number of drop collection statements received.

• Mysqlx_stmt_drop_collection_index

The number of drop collection index statements received.

• Mysqlx_stmt_enable_notices

The number of enable notice statements received.

• Mysqlx_stmt_ensure_collection

The number of ensure collection statements received.

• Mysqlx_stmt_execute_mysqlx

The number of StmtExecute messages received with namespace set to mysqlx.

• Mysqlx_stmt_execute_sql

The number of StmtExecute requests received for the SQL namespace.

• Mysqlx_stmt_execute_xplugin

The number of StmtExecute requests received for the xplugin namespace. From MySQL 8.0.19,
the xplugin namespace has been removed so this status variable is no longer used.

• Mysqlx_stmt_get_collection_options

4127

Monitoring X Plugin

The number of get collection object statements received.

• Mysqlx_stmt_kill_client

The number of kill client statements received.

• Mysqlx_stmt_list_clients

The number of list client statements received.

• Mysqlx_stmt_list_notices

The number of list notice statements received.

• Mysqlx_stmt_list_objects

The number of list object statements received.

• Mysqlx_stmt_modify_collection_options

The number of modify collection options statements received.

• Mysqlx_stmt_ping

The number of ping statements received.

• Mysqlx_worker_threads

The number of worker threads available.

• Mysqlx_worker_threads_active

The number of worker threads currently used.

22.5.7 Monitoring X Plugin

For general X Plugin monitoring, use the status variables that it exposes. See Section 22.5.6.3,
“X Plugin Status Variables”. For information specifically about monitoring the effects of message
compression, see Monitoring Connection Compression for X Plugin.

Monitoring SQL Generated by X Plugin

This section describes how to monitor the SQL statements which X Plugin generates when you run
X DevAPI operations. When you execute a CRUD statement, it is translated into SQL and executed
against the server. To be able to monitor the generated SQL, the Performance Schema tables must be
enabled. The SQL is registered under the performance_schema.events_statements_current,
performance_schema.events_statements_history, and
performance_schema.events_statements_history_long tables. The following example uses
the world_x schema, imported as part of the quickstart tutorials in this section. We use MySQL Shell
in Python mode, and the \sql command which enables you to issue SQL statements without changing
to SQL mode. This is important, because if you instead try to switch to SQL mode, the procedure
shows the result of this operation rather than the X DevAPI operation. The \sql command is used in
the same way if you are using MySQL Shell in JavaScript mode.

1. Check if the events_statements_history consumer is enabled. Issue:

mysql-py> \sql SELECT enabled FROM performance_schema.setup_consumers WHERE NAME = 'events_statements_history'
+---------+
| enabled |
+---------+
| YES     |
+---------+

4128

4130

