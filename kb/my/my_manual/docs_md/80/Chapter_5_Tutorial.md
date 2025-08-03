Entering Queries

$> mysql -h host -u user -p
Enter password: ********

host and user represent the host name where your MySQL server is running and the user name of
your MySQL account. Substitute appropriate values for your setup. The ******** represents your
password; enter it when mysql displays the Enter password: prompt.

If that works, you should see some introductory information followed by a mysql> prompt:

$> mysql -h host -u user -p
Enter password: ********
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 25338 to server version: 8.0.42-standard

Type 'help;' or '\h' for help. Type '\c' to clear the buffer.

mysql>

The mysql> prompt tells you that mysql is ready for you to enter SQL statements.

If you are logging in on the same machine that MySQL is running on, you can omit the host, and simply
use the following:

$> mysql -u user -p

If, when you attempt to log in, you get an error message such as ERROR 2002 (HY000): Can't
connect to local MySQL server through socket '/tmp/mysql.sock' (2), it means
that the MySQL server daemon (Unix) or service (Windows) is not running. Consult the administrator or
see the section of Chapter 2, Installing MySQL that is appropriate to your operating system.

For help with other problems often encountered when trying to log in, see Section B.3.2, “Common
Errors When Using MySQL Programs”.

Some MySQL installations permit users to connect as the anonymous (unnamed) user to the server
running on the local host. If this is the case on your machine, you should be able to connect to that
server by invoking mysql without any options:

$> mysql

After you have connected successfully, you can disconnect any time by typing QUIT (or \q) at the
mysql> prompt:

mysql> QUIT
Bye

On Unix, you can also disconnect by pressing Control+D.

Most examples in the following sections assume that you are connected to the server. They indicate
this by the mysql> prompt.

5.2 Entering Queries

Make sure that you are connected to the server, as discussed in the previous section. Doing so does
not in itself select any database to work with, but that is okay. At this point, it is more important to find
out a little about how to issue queries than to jump right in creating tables, loading data into them, and
retrieving data from them. This section describes the basic principles of entering queries, using several
queries you can try out to familiarize yourself with how mysql works.

Here is a simple query that asks the server to tell you its version number and the current date. Type it
in as shown here following the mysql> prompt and press Enter:

mysql> SELECT VERSION(), CURRENT_DATE;
+-----------+--------------+
| VERSION() | CURRENT_DATE |

330

Entering Queries

+-----------+--------------+
| 5.8.0-m17 | 2015-12-21   |
+-----------+--------------+
1 row in set (0.02 sec)
mysql>

This query illustrates several things about mysql:

• A query normally consists of an SQL statement followed by a semicolon. (There are some

exceptions where a semicolon may be omitted. QUIT, mentioned earlier, is one of them. We'll get to
others later.)

• When you issue a query, mysql sends it to the server for execution and displays the results, then

prints another mysql> prompt to indicate that it is ready for another query.

• mysql displays query output in tabular form (rows and columns). The first row contains labels for

the columns. The rows following are the query results. Normally, column labels are the names of the
columns you fetch from database tables. If you're retrieving the value of an expression rather than a
table column (as in the example just shown), mysql labels the column using the expression itself.

• mysql shows how many rows were returned and how long the query took to execute, which gives
you a rough idea of server performance. These values are imprecise because they represent wall
clock time (not CPU or machine time), and because they are affected by factors such as server load
and network latency. (For brevity, the “rows in set” line is sometimes not shown in the remaining
examples in this chapter.)

Keywords may be entered in any lettercase. The following queries are equivalent:

mysql> SELECT VERSION(), CURRENT_DATE;
mysql> select version(), current_date;
mysql> SeLeCt vErSiOn(), current_DATE;

Here is another query. It demonstrates that you can use mysql as a simple calculator:

mysql> SELECT SIN(PI()/4), (4+1)*5;
+------------------+---------+
| SIN(PI()/4)      | (4+1)*5 |
+------------------+---------+
| 0.70710678118655 |      25 |
+------------------+---------+
1 row in set (0.02 sec)

The queries shown thus far have been relatively short, single-line statements. You can even enter
multiple statements on a single line. Just end each one with a semicolon:

mysql> SELECT VERSION(); SELECT NOW();
+-----------+
| VERSION() |
+-----------+
| 8.0.13    |
+-----------+
1 row in set (0.00 sec)

+---------------------+
| NOW()               |
+---------------------+
| 2018-08-24 00:56:40 |
+---------------------+
1 row in set (0.00 sec)

A query need not be given all on a single line, so lengthy queries that require several lines are not a
problem. mysql determines where your statement ends by looking for the terminating semicolon, not
by looking for the end of the input line. (In other words, mysql accepts free-format input: it collects
input lines but does not execute them until it sees the semicolon.)

Here is a simple multiple-line statement:

331

Entering Queries

mysql> SELECT
    -> USER()
    -> ,
    -> CURRENT_DATE;
+---------------+--------------+
| USER()        | CURRENT_DATE |
+---------------+--------------+
| jon@localhost | 2018-08-24   |
+---------------+--------------+

In this example, notice how the prompt changes from mysql> to -> after you enter the first line of a
multiple-line query. This is how mysql indicates that it has not yet seen a complete statement and is
waiting for the rest. The prompt is your friend, because it provides valuable feedback. If you use that
feedback, you can always be aware of what mysql is waiting for.

If you decide you do not want to execute a query that you are in the process of entering, cancel it by
typing \c:

mysql> SELECT
    -> USER()
    -> \c
mysql>

Here, too, notice the prompt. It switches back to mysql> after you type \c, providing feedback to
indicate that mysql is ready for a new query.

The following table shows each of the prompts you may see and summarizes what they mean about
the state that mysql is in.

Prompt

mysql>

->

'>

">

`>

/*>

Meaning

Ready for new query

Waiting for next line of multiple-line query

Waiting for next line, waiting for completion of a
string that began with a single quote (')

Waiting for next line, waiting for completion of a
string that began with a double quote (")

Waiting for next line, waiting for completion of an
identifier that began with a backtick (`)

Waiting for next line, waiting for completion of a
comment that began with /*

Multiple-line statements commonly occur by accident when you intend to issue a query on a single line,
but forget the terminating semicolon. In this case, mysql waits for more input:

mysql> SELECT USER()
    ->

If this happens to you (you think you've entered a statement but the only response is a -> prompt),
most likely mysql is waiting for the semicolon. If you don't notice what the prompt is telling you, you
might sit there for a while before realizing what you need to do. Enter a semicolon to complete the
statement, and mysql executes it:

mysql> SELECT USER()
    -> ;
+---------------+
| USER()        |
+---------------+
| jon@localhost |
+---------------+

The '> and "> prompts occur during string collection (another way of saying that MySQL is waiting
for completion of a string). In MySQL, you can write strings surrounded by either ' or " characters (for

332

Creating and Using a Database

example, 'hello' or "goodbye"), and mysql lets you enter strings that span multiple lines. When
you see a '> or "> prompt, it means that you have entered a line containing a string that begins with
a ' or " quote character, but have not yet entered the matching quote that terminates the string. This
often indicates that you have inadvertently left out a quote character. For example:

mysql> SELECT * FROM my_table WHERE name = 'Smith AND age < 30;
    '>

If you enter this SELECT statement, then press Enter and wait for the result, nothing happens. Instead
of wondering why this query takes so long, notice the clue provided by the '> prompt. It tells you that
mysql expects to see the rest of an unterminated string. (Do you see the error in the statement? The
string 'Smith is missing the second single quotation mark.)

At this point, what do you do? The simplest thing is to cancel the query. However, you cannot just type
\c in this case, because mysql interprets it as part of the string that it is collecting. Instead, enter the
closing quote character (so mysql knows you've finished the string), then type \c:

mysql> SELECT * FROM my_table WHERE name = 'Smith AND age < 30;
    '> '\c
mysql>

The prompt changes back to mysql>, indicating that mysql is ready for a new query.

The `> prompt is similar to the '> and "> prompts, but indicates that you have begun but not
completed a backtick-quoted identifier.

It is important to know what the '>, ">, and `> prompts signify, because if you mistakenly enter
an unterminated string, any further lines you type appear to be ignored by mysql—including a line
containing QUIT. This can be quite confusing, especially if you do not know that you need to supply the
terminating quote before you can cancel the current query.

Note

Multiline statements from this point on are written without the secondary (->
or other) prompts, to make it easier to copy and paste the statements to try for
yourself.

5.3 Creating and Using a Database

Once you know how to enter SQL statements, you are ready to access a database.

Suppose that you have several pets in your home (your menagerie) and you would like to keep track
of various types of information about them. You can do so by creating tables to hold your data and
loading them with the desired information. Then you can answer different sorts of questions about
your animals by retrieving data from the tables. This section shows you how to perform the following
operations:

• Create a database

• Create a table

• Load data into the table

• Retrieve data from the table in various ways

• Use multiple tables

The menagerie database is simple (deliberately), but it is not difficult to think of real-world situations
in which a similar type of database might be used. For example, a database like this could be used by
a farmer to keep track of livestock, or by a veterinarian to keep track of patient records. A menagerie
distribution containing some of the queries and sample data used in the following sections can be

333

Retrieving Information from a Table

| Chirpy   | Gwen  | bird    | f    | 1998-09-11 | NULL  |
| Puffball | Diane | hamster | f    | 1999-03-30 | NULL  |
+----------+-------+---------+------+------------+-------+

You can combine conditions, for example, to locate female dogs:

mysql> SELECT * FROM pet WHERE species = 'dog' AND sex = 'f';
+-------+--------+---------+------+------------+-------+
| name  | owner  | species | sex  | birth      | death |
+-------+--------+---------+------+------------+-------+
| Buffy | Harold | dog     | f    | 1989-05-13 | NULL  |
+-------+--------+---------+------+------------+-------+

The preceding query uses the AND logical operator. There is also an OR operator:

mysql> SELECT * FROM pet WHERE species = 'snake' OR species = 'bird';
+----------+-------+---------+------+------------+-------+
| name     | owner | species | sex  | birth      | death |
+----------+-------+---------+------+------------+-------+
| Chirpy   | Gwen  | bird    | f    | 1998-09-11 | NULL  |
| Whistler | Gwen  | bird    | NULL | 1997-12-09 | NULL  |
| Slim     | Benny | snake   | m    | 1996-04-29 | NULL  |
+----------+-------+---------+------+------------+-------+

AND and OR may be intermixed, although AND has higher precedence than OR. If you use both
operators, it is a good idea to use parentheses to indicate explicitly how conditions should be grouped:

mysql> SELECT * FROM pet WHERE (species = 'cat' AND sex = 'm')
       OR (species = 'dog' AND sex = 'f');
+-------+--------+---------+------+------------+-------+
| name  | owner  | species | sex  | birth      | death |
+-------+--------+---------+------+------------+-------+
| Claws | Gwen   | cat     | m    | 1994-03-17 | NULL  |
| Buffy | Harold | dog     | f    | 1989-05-13 | NULL  |
+-------+--------+---------+------+------------+-------+

5.3.4.3 Selecting Particular Columns

If you do not want to see entire rows from your table, just name the columns in which you are
interested, separated by commas. For example, if you want to know when your animals were born,
select the name and birth columns:

mysql> SELECT name, birth FROM pet;
+----------+------------+
| name     | birth      |
+----------+------------+
| Fluffy   | 1993-02-04 |
| Claws    | 1994-03-17 |
| Buffy    | 1989-05-13 |
| Fang     | 1990-08-27 |
| Bowser   | 1989-08-31 |
| Chirpy   | 1998-09-11 |
| Whistler | 1997-12-09 |
| Slim     | 1996-04-29 |
| Puffball | 1999-03-30 |
+----------+------------+

To find out who owns pets, use this query:

mysql> SELECT owner FROM pet;
+--------+
| owner  |
+--------+
| Harold |
| Gwen   |
| Harold |
| Benny  |
| Diane  |
| Gwen   |
| Gwen   |

339

Retrieving Information from a Table

| Benny  |
| Diane  |
+--------+

Notice that the query simply retrieves the owner column from each record, and some of them appear
more than once. To minimize the output, retrieve each unique output record just once by adding the
keyword DISTINCT:

mysql> SELECT DISTINCT owner FROM pet;
+--------+
| owner  |
+--------+
| Benny  |
| Diane  |
| Gwen   |
| Harold |
+--------+

You can use a WHERE clause to combine row selection with column selection. For example, to get birth
dates for dogs and cats only, use this query:

mysql> SELECT name, species, birth FROM pet
       WHERE species = 'dog' OR species = 'cat';
+--------+---------+------------+
| name   | species | birth      |
+--------+---------+------------+
| Fluffy | cat     | 1993-02-04 |
| Claws  | cat     | 1994-03-17 |
| Buffy  | dog     | 1989-05-13 |
| Fang   | dog     | 1990-08-27 |
| Bowser | dog     | 1989-08-31 |
+--------+---------+------------+

5.3.4.4 Sorting Rows

You may have noticed in the preceding examples that the result rows are displayed in no particular
order. It is often easier to examine query output when the rows are sorted in some meaningful way. To
sort a result, use an ORDER BY clause.

Here are animal birthdays, sorted by date:

mysql> SELECT name, birth FROM pet ORDER BY birth;
+----------+------------+
| name     | birth      |
+----------+------------+
| Buffy    | 1989-05-13 |
| Bowser   | 1989-08-31 |
| Fang     | 1990-08-27 |
| Fluffy   | 1993-02-04 |
| Claws    | 1994-03-17 |
| Slim     | 1996-04-29 |
| Whistler | 1997-12-09 |
| Chirpy   | 1998-09-11 |
| Puffball | 1999-03-30 |
+----------+------------+

On character type columns, sorting—like all other comparison operations—is normally performed in a
case-insensitive fashion. This means that the order is undefined for columns that are identical except
for their case. You can force a case-sensitive sort for a column by using BINARY like so: ORDER BY
BINARY col_name.

The default sort order is ascending, with smallest values first. To sort in reverse (descending) order,
add the DESC keyword to the name of the column you are sorting by:

mysql> SELECT name, birth FROM pet ORDER BY birth DESC;
+----------+------------+
| name     | birth      |

340

Retrieving Information from a Table

+----------+------------+
| Puffball | 1999-03-30 |
| Chirpy   | 1998-09-11 |
| Whistler | 1997-12-09 |
| Slim     | 1996-04-29 |
| Claws    | 1994-03-17 |
| Fluffy   | 1993-02-04 |
| Fang     | 1990-08-27 |
| Bowser   | 1989-08-31 |
| Buffy    | 1989-05-13 |
+----------+------------+

You can sort on multiple columns, and you can sort different columns in different directions. For
example, to sort by type of animal in ascending order, then by birth date within animal type in
descending order (youngest animals first), use the following query:

mysql> SELECT name, species, birth FROM pet
       ORDER BY species, birth DESC;
+----------+---------+------------+
| name     | species | birth      |
+----------+---------+------------+
| Chirpy   | bird    | 1998-09-11 |
| Whistler | bird    | 1997-12-09 |
| Claws    | cat     | 1994-03-17 |
| Fluffy   | cat     | 1993-02-04 |
| Fang     | dog     | 1990-08-27 |
| Bowser   | dog     | 1989-08-31 |
| Buffy    | dog     | 1989-05-13 |
| Puffball | hamster | 1999-03-30 |
| Slim     | snake   | 1996-04-29 |
+----------+---------+------------+

The DESC keyword applies only to the column name immediately preceding it (birth); it does not
affect the species column sort order.

5.3.4.5 Date Calculations

MySQL provides several functions that you can use to perform calculations on dates, for example, to
calculate ages or extract parts of dates.

To determine how many years old each of your pets is, use the TIMESTAMPDIFF() function. Its
arguments are the unit in which you want the result expressed, and the two dates for which to take
the difference. The following query shows, for each pet, the birth date, the current date, and the age in
years. An alias (age) is used to make the final output column label more meaningful.

mysql> SELECT name, birth, CURDATE(),
       TIMESTAMPDIFF(YEAR,birth,CURDATE()) AS age
       FROM pet;
+----------+------------+------------+------+
| name     | birth      | CURDATE()  | age  |
+----------+------------+------------+------+
| Fluffy   | 1993-02-04 | 2003-08-19 |   10 |
| Claws    | 1994-03-17 | 2003-08-19 |    9 |
| Buffy    | 1989-05-13 | 2003-08-19 |   14 |
| Fang     | 1990-08-27 | 2003-08-19 |   12 |
| Bowser   | 1989-08-31 | 2003-08-19 |   13 |
| Chirpy   | 1998-09-11 | 2003-08-19 |    4 |
| Whistler | 1997-12-09 | 2003-08-19 |    5 |
| Slim     | 1996-04-29 | 2003-08-19 |    7 |
| Puffball | 1999-03-30 | 2003-08-19 |    4 |
+----------+------------+------------+------+

The query works, but the result could be scanned more easily if the rows were presented in some
order. This can be done by adding an ORDER BY name clause to sort the output by name:

mysql> SELECT name, birth, CURDATE(),
       TIMESTAMPDIFF(YEAR,birth,CURDATE()) AS age
       FROM pet ORDER BY name;

341

Retrieving Information from a Table

+----------+------------+--------------+

Finding animals with birthdays in the upcoming month is also simple. Suppose that the current month is
April. Then the month value is 4 and you can look for animals born in May (month 5) like this:

mysql> SELECT name, birth FROM pet WHERE MONTH(birth) = 5;
+-------+------------+
| name  | birth      |
+-------+------------+
| Buffy | 1989-05-13 |
+-------+------------+

There is a small complication if the current month is December. You cannot merely add one to the
month number (12) and look for animals born in month 13, because there is no such month. Instead,
you look for animals born in January (month 1).

You can write the query so that it works no matter what the current month is, so that you do not have to
use the number for a particular month. DATE_ADD() enables you to add a time interval to a given date.
If you add a month to the value of CURDATE(), then extract the month part with MONTH(), the result
produces the month in which to look for birthdays:

mysql> SELECT name, birth FROM pet
       WHERE MONTH(birth) = MONTH(DATE_ADD(CURDATE(),INTERVAL 1 MONTH));

A different way to accomplish the same task is to add 1 to get the next month after the current one after
using the modulo function (MOD) to wrap the month value to 0 if it is currently 12:

mysql> SELECT name, birth FROM pet
       WHERE MONTH(birth) = MOD(MONTH(CURDATE()), 12) + 1;

MONTH() returns a number between 1 and 12. And MOD(something,12) returns a number between
0 and 11. So the addition has to be after the MOD(), otherwise we would go from November (11) to
January (1).

If a calculation uses invalid dates, the calculation fails and produces warnings:

mysql> SELECT '2018-10-31' + INTERVAL 1 DAY;
+-------------------------------+
| '2018-10-31' + INTERVAL 1 DAY |
+-------------------------------+
| 2018-11-01                    |
+-------------------------------+
mysql> SELECT '2018-10-32' + INTERVAL 1 DAY;
+-------------------------------+
| '2018-10-32' + INTERVAL 1 DAY |
+-------------------------------+
| NULL                          |
+-------------------------------+
mysql> SHOW WARNINGS;
+---------+------+----------------------------------------+
| Level   | Code | Message                                |
+---------+------+----------------------------------------+
| Warning | 1292 | Incorrect datetime value: '2018-10-32' |
+---------+------+----------------------------------------+

5.3.4.6 Working with NULL Values

The NULL value can be surprising until you get used to it. Conceptually, NULL means “a missing
unknown value” and it is treated somewhat differently from other values.

To test for NULL, use the IS NULL and IS NOT NULL operators, as shown here:

mysql> SELECT 1 IS NULL, 1 IS NOT NULL;
+-----------+---------------+
| 1 IS NULL | 1 IS NOT NULL |
+-----------+---------------+
|         0 |             1 |

343

Retrieving Information from a Table

+-----------+---------------+

You cannot use arithmetic comparison operators such as =, <, or <> to test for NULL. To demonstrate
this for yourself, try the following query:

mysql> SELECT 1 = NULL, 1 <> NULL, 1 < NULL, 1 > NULL;
+----------+-----------+----------+----------+
| 1 = NULL | 1 <> NULL | 1 < NULL | 1 > NULL |
+----------+-----------+----------+----------+
|     NULL |      NULL |     NULL |     NULL |
+----------+-----------+----------+----------+

Because the result of any arithmetic comparison with NULL is also NULL, you cannot obtain any
meaningful results from such comparisons.

In MySQL, 0 or NULL means false and anything else means true. The default truth value from a
boolean operation is 1.

This special treatment of NULL is why, in the previous section, it was necessary to determine which
animals are no longer alive using death IS NOT NULL instead of death <> NULL.

Two NULL values are regarded as equal in a GROUP BY.

When doing an ORDER BY, NULL values are presented first if you do ORDER BY ... ASC and last if
you do ORDER BY ... DESC.

A common error when working with NULL is to assume that it is not possible to insert a zero or an
empty string into a column defined as NOT NULL, but this is not the case. These are in fact values,
whereas NULL means “not having a value.” You can test this easily enough by using IS [NOT] NULL
as shown:

mysql> SELECT 0 IS NULL, 0 IS NOT NULL, '' IS NULL, '' IS NOT NULL;
+-----------+---------------+------------+----------------+
| 0 IS NULL | 0 IS NOT NULL | '' IS NULL | '' IS NOT NULL |
+-----------+---------------+------------+----------------+
|         0 |             1 |          0 |              1 |
+-----------+---------------+------------+----------------+

Thus it is entirely possible to insert a zero or empty string into a NOT NULL column, as these are in fact
NOT NULL. See Section B.3.4.3, “Problems with NULL Values”.

5.3.4.7 Pattern Matching

MySQL provides standard SQL pattern matching as well as a form of pattern matching based on
extended regular expressions similar to those used by Unix utilities such as vi, grep, and sed.

SQL pattern matching enables you to use _ to match any single character and % to match an arbitrary
number of characters (including zero characters). In MySQL, SQL patterns are case-insensitive by
default. Some examples are shown here. Do not use = or <> when you use SQL patterns. Use the
LIKE or NOT LIKE comparison operators instead.

To find names beginning with b:

mysql> SELECT * FROM pet WHERE name LIKE 'b%';
+--------+--------+---------+------+------------+------------+
| name   | owner  | species | sex  | birth      | death      |
+--------+--------+---------+------+------------+------------+
| Buffy  | Harold | dog     | f    | 1989-05-13 | NULL       |
| Bowser | Diane  | dog     | m    | 1989-08-31 | 1995-07-29 |
+--------+--------+---------+------+------------+------------+

To find names ending with fy:

mysql> SELECT * FROM pet WHERE name LIKE '%fy';
+--------+--------+---------+------+------------+-------+

344

Retrieving Information from a Table

| name   | owner  | species | sex  | birth      | death |
+--------+--------+---------+------+------------+-------+
| Fluffy | Harold | cat     | f    | 1993-02-04 | NULL  |
| Buffy  | Harold | dog     | f    | 1989-05-13 | NULL  |
+--------+--------+---------+------+------------+-------+

To find names containing a w:

mysql> SELECT * FROM pet WHERE name LIKE '%w%';
+----------+-------+---------+------+------------+------------+
| name     | owner | species | sex  | birth      | death      |
+----------+-------+---------+------+------------+------------+
| Claws    | Gwen  | cat     | m    | 1994-03-17 | NULL       |
| Bowser   | Diane | dog     | m    | 1989-08-31 | 1995-07-29 |
| Whistler | Gwen  | bird    | NULL | 1997-12-09 | NULL       |
+----------+-------+---------+------+------------+------------+

To find names containing exactly five characters, use five instances of the _ pattern character:

mysql> SELECT * FROM pet WHERE name LIKE '_____';
+-------+--------+---------+------+------------+-------+
| name  | owner  | species | sex  | birth      | death |
+-------+--------+---------+------+------------+-------+
| Claws | Gwen   | cat     | m    | 1994-03-17 | NULL  |
| Buffy | Harold | dog     | f    | 1989-05-13 | NULL  |
+-------+--------+---------+------+------------+-------+

The other type of pattern matching provided by MySQL uses extended regular expressions. When you
test for a match for this type of pattern, use the REGEXP_LIKE() function (or the REGEXP or RLIKE
operators, which are synonyms for REGEXP_LIKE()).

The following list describes some characteristics of extended regular expressions:

• . matches any single character.

• A character class [...] matches any character within the brackets. For example, [abc] matches
a, b, or c. To name a range of characters, use a dash. [a-z] matches any letter, whereas [0-9]
matches any digit.

• * matches zero or more instances of the thing preceding it. For example, x* matches any number of

x characters, [0-9]* matches any number of digits, and .* matches any number of anything.

• A regular expression pattern match succeeds if the pattern matches anywhere in the value being
tested. (This differs from a LIKE pattern match, which succeeds only if the pattern matches the
entire value.)

• To anchor a pattern so that it must match the beginning or end of the value being tested, use ^ at the

beginning or $ at the end of the pattern.

To demonstrate how extended regular expressions work, the LIKE queries shown previously are
rewritten here to use REGEXP_LIKE().

To find names beginning with b, use ^ to match the beginning of the name:

mysql> SELECT * FROM pet WHERE REGEXP_LIKE(name, '^b');
+--------+--------+---------+------+------------+------------+
| name   | owner  | species | sex  | birth      | death      |
+--------+--------+---------+------+------------+------------+
| Buffy  | Harold | dog     | f    | 1989-05-13 | NULL       |
| Bowser | Diane  | dog     | m    | 1979-08-31 | 1995-07-29 |
+--------+--------+---------+------+------------+------------+

To force a regular expression comparison to be case-sensitive, use a case-sensitive collation, or
use the BINARY keyword to make one of the strings a binary string, or specify the c match-control
character. Each of these queries matches only lowercase b at the beginning of a name:

SELECT * FROM pet WHERE REGEXP_LIKE(name, '^b' COLLATE utf8mb4_0900_as_cs);

345

Retrieving Information from a Table

+----------+

Earlier, you retrieved the names of the people who owned pets. You can use COUNT() if you want to
find out how many pets each owner has:

mysql> SELECT owner, COUNT(*) FROM pet GROUP BY owner;
+--------+----------+
| owner  | COUNT(*) |
+--------+----------+
| Benny  |        2 |
| Diane  |        2 |
| Gwen   |        3 |
| Harold |        2 |
+--------+----------+

The preceding query uses GROUP BY to group all records for each owner. The use of COUNT()
in conjunction with GROUP BY is useful for characterizing your data under various groupings. The
following examples show different ways to perform animal census operations.

Number of animals per species:

mysql> SELECT species, COUNT(*) FROM pet GROUP BY species;
+---------+----------+
| species | COUNT(*) |
+---------+----------+
| bird    |        2 |
| cat     |        2 |
| dog     |        3 |
| hamster |        1 |
| snake   |        1 |
+---------+----------+

Number of animals per sex:

mysql> SELECT sex, COUNT(*) FROM pet GROUP BY sex;
+------+----------+
| sex  | COUNT(*) |
+------+----------+
| NULL |        1 |
| f    |        4 |
| m    |        4 |
+------+----------+

(In this output, NULL indicates that the sex is unknown.)

Number of animals per combination of species and sex:

mysql> SELECT species, sex, COUNT(*) FROM pet GROUP BY species, sex;
+---------+------+----------+
| species | sex  | COUNT(*) |
+---------+------+----------+
| bird    | NULL |        1 |
| bird    | f    |        1 |
| cat     | f    |        1 |
| cat     | m    |        1 |
| dog     | f    |        1 |
| dog     | m    |        2 |
| hamster | f    |        1 |
| snake   | m    |        1 |
+---------+------+----------+

You need not retrieve an entire table when you use COUNT(). For example, the previous query, when
performed just on dogs and cats, looks like this:

mysql> SELECT species, sex, COUNT(*) FROM pet
       WHERE species = 'dog' OR species = 'cat'
       GROUP BY species, sex;
+---------+------+----------+
| species | sex  | COUNT(*) |

347

Retrieving Information from a Table

Given these considerations, the CREATE TABLE statement for the event table might look like this:

mysql> CREATE TABLE event (name VARCHAR(20), date DATE,
       type VARCHAR(15), remark VARCHAR(255));

As with the pet table, it is easiest to load the initial records by creating a tab-delimited text file
containing the following information.

name

Fluffy

Buffy

Buffy

Chirpy

Slim

Bowser

Fang

Fang

Claws

date

1995-05-15

1993-06-23

1994-06-19

1999-03-21

1997-08-03

1991-10-12

1991-10-12

1998-08-28

type

litter

litter

litter

vet

vet

kennel

kennel

birthday

1998-03-17

birthday

remark

4 kittens, 3 female, 1
male

5 puppies, 2 female, 3
male

3 puppies, 3 female

needed beak
straightened

broken rib

Gave him a new chew
toy

Gave him a new flea
collar

Whistler

1998-12-09

birthday

First birthday

Load the records like this:

mysql> LOAD DATA LOCAL INFILE 'event.txt' INTO TABLE event;

Based on what you have learned from the queries that you have run on the pet table, you should be
able to perform retrievals on the records in the event table; the principles are the same. But when is
the event table by itself insufficient to answer questions you might ask?

Suppose that you want to find out the ages at which each pet had its litters. We saw earlier how to
calculate ages from two dates. The litter date of the mother is in the event table, but to calculate
her age on that date you need her birth date, which is stored in the pet table. This means the query
requires both tables:

mysql> SELECT pet.name,
       TIMESTAMPDIFF(YEAR,birth,date) AS age,
       remark
       FROM pet INNER JOIN event
         ON pet.name = event.name
       WHERE event.type = 'litter';
+--------+------+-----------------------------+
| name   | age  | remark                      |
+--------+------+-----------------------------+
| Fluffy |    2 | 4 kittens, 3 female, 1 male |
| Buffy  |    4 | 5 puppies, 2 female, 3 male |
| Buffy  |    5 | 3 puppies, 3 female         |
+--------+------+-----------------------------+

There are several things to note about this query:

• The FROM clause joins two tables because the query needs to pull information from both of them.

• When combining (joining) information from multiple tables, you need to specify how records in one
table can be matched to records in the other. This is easy because they both have a name column.
The query uses an ON clause to match up records in the two tables based on the name values.

349

Getting Information About Databases and Tables

The query uses an INNER JOIN to combine the tables. An INNER JOIN permits rows from either
table to appear in the result if and only if both tables meet the conditions specified in the ON clause.
In this example, the ON clause specifies that the name column in the pet table must match the name
column in the event table. If a name appears in one table but not the other, the row does not appear
in the result because the condition in the ON clause fails.

• Because the name column occurs in both tables, you must be specific about which table you mean

when referring to the column. This is done by prepending the table name to the column name.

You need not have two different tables to perform a join. Sometimes it is useful to join a table to itself,
if you want to compare records in a table to other records in that same table. For example, to find
breeding pairs among your pets, you can join the pet table with itself to produce candidate pairs of live
males and females of like species:

mysql> SELECT p1.name, p1.sex, p2.name, p2.sex, p1.species
       FROM pet AS p1 INNER JOIN pet AS p2
         ON p1.species = p2.species
         AND p1.sex = 'f' AND p1.death IS NULL
         AND p2.sex = 'm' AND p2.death IS NULL;
+--------+------+-------+------+---------+
| name   | sex  | name  | sex  | species |
+--------+------+-------+------+---------+
| Fluffy | f    | Claws | m    | cat     |
| Buffy  | f    | Fang  | m    | dog     |
+--------+------+-------+------+---------+

In this query, we specify aliases for the table name to refer to the columns and keep straight which
instance of the table each column reference is associated with.

5.4 Getting Information About Databases and Tables

What if you forget the name of a database or table, or what the structure of a given table is (for
example, what its columns are called)? MySQL addresses this problem through several statements
that provide information about the databases and tables it supports.

You have previously seen SHOW DATABASES, which lists the databases managed by the server. To
find out which database is currently selected, use the DATABASE() function:

mysql> SELECT DATABASE();
+------------+
| DATABASE() |
+------------+
| menagerie  |
+------------+

If you have not yet selected any database, the result is NULL.

To find out what tables the default database contains (for example, when you are not sure about the
name of a table), use this statement:

mysql> SHOW TABLES;
+---------------------+
| Tables_in_menagerie |
+---------------------+
| event               |
| pet                 |
+---------------------+

The name of the column in the output produced by this statement is always Tables_in_db_name,
where db_name is the name of the database. See Section 15.7.7.39, “SHOW TABLES Statement”, for
more information.

If you want to find out about the structure of a table, the DESCRIBE statement is useful; it displays
information about each of a table's columns:

350

Examples of Common Queries

• You can catch the output in a file for further processing:

$> mysql < batch-file > mysql.out

• You can distribute your script to other people so that they can also run the statements.

• Some situations do not allow for interactive use, for example, when you run a query from a cron job.

In this case, you must use batch mode.

The default output format is different (more concise) when you run mysql in batch mode than when
you use it interactively. For example, the output of SELECT DISTINCT species FROM pet looks
like this when mysql is run interactively:

+---------+
| species |
+---------+
| bird    |
| cat     |
| dog     |
| hamster |
| snake   |
+---------+

In batch mode, the output looks like this instead:

species
bird
cat
dog
hamster
snake

If you want to get the interactive output format in batch mode, use mysql -t. To echo to the output
the statements that are executed, use mysql -v.

You can also use scripts from the mysql prompt by using the source command or \. command:

mysql> source filename;
mysql> \. filename

See Section 6.5.1.5, “Executing SQL Statements from a Text File”, for more information.

5.6 Examples of Common Queries

Here are examples of how to solve some common problems with MySQL.

Some of the examples use the table shop to hold the price of each article (item number) for certain
traders (dealers). Supposing that each trader has a single fixed price per article, then (article,
dealer) is a primary key for the records.

Start the command-line tool mysql and select a database:

$> mysql your-database-name

To create and populate the example table, use these statements:

CREATE TABLE shop (
    article INT UNSIGNED  DEFAULT '0000' NOT NULL,
    dealer  CHAR(20)      DEFAULT ''     NOT NULL,
    price   DECIMAL(16,2) DEFAULT '0.00' NOT NULL,
    PRIMARY KEY(article, dealer));
INSERT INTO shop VALUES
    (1,'A',3.45),(1,'B',3.99),(2,'A',10.99),(3,'B',1.45),
    (3,'C',1.69),(3,'D',1.25),(4,'D',19.95);

After issuing the statements, the table should have the following contents:

352

The Maximum Value for a Column

SELECT * FROM shop ORDER BY article;

+---------+--------+-------+
| article | dealer | price |
+---------+--------+-------+
|       1 | A      |  3.45 |
|       1 | B      |  3.99 |
|       2 | A      | 10.99 |
|       3 | B      |  1.45 |
|       3 | C      |  1.69 |
|       3 | D      |  1.25 |
|       4 | D      | 19.95 |
+---------+--------+-------+

5.6.1 The Maximum Value for a Column

“What is the highest item number?”

SELECT MAX(article) AS article FROM shop;

+---------+
| article |
+---------+
|       4 |
+---------+

5.6.2 The Row Holding the Maximum of a Certain Column

Task: Find the number, dealer, and price of the most expensive article.

This is easily done with a subquery:

SELECT article, dealer, price
FROM   shop
WHERE  price=(SELECT MAX(price) FROM shop);

+---------+--------+-------+
| article | dealer | price |
+---------+--------+-------+
|    0004 | D      | 19.95 |
+---------+--------+-------+

Another solution is to use a LEFT JOIN, as shown here:

SELECT s1.article, s1.dealer, s1.price
FROM shop s1
LEFT JOIN shop s2 ON s1.price < s2.price
WHERE s2.article IS NULL;

You can also do this by sorting all rows descending by price and get only the first row using the
MySQL-specific LIMIT clause, like this:

SELECT article, dealer, price
FROM shop
ORDER BY price DESC
LIMIT 1;

Note

If there were several most expensive articles, each with a price of 19.95, the
LIMIT solution would show only one of them.

5.6.3 Maximum of Column per Group

Task: Find the highest price per article.

SELECT article, MAX(price) AS price

353

The Rows Holding the Group-wise Maximum of a Certain Column

FROM   shop
GROUP BY article
ORDER BY article;

+---------+-------+
| article | price |
+---------+-------+
|    0001 |  3.99 |
|    0002 | 10.99 |
|    0003 |  1.69 |
|    0004 | 19.95 |
+---------+-------+

5.6.4 The Rows Holding the Group-wise Maximum of a Certain Column

Task: For each article, find the dealer or dealers with the most expensive price.

This problem can be solved with a subquery like this one:

SELECT article, dealer, price
FROM   shop s1
WHERE  price=(SELECT MAX(s2.price)
              FROM shop s2
              WHERE s1.article = s2.article)
ORDER BY article;

+---------+--------+-------+
| article | dealer | price |
+---------+--------+-------+
|    0001 | B      |  3.99 |
|    0002 | A      | 10.99 |
|    0003 | C      |  1.69 |
|    0004 | D      | 19.95 |
+---------+--------+-------+

The preceding example uses a correlated subquery, which can be inefficient (see Section 15.2.15.7,
“Correlated Subqueries”). Other possibilities for solving the problem are to use an uncorrelated
subquery in the FROM clause, a LEFT JOIN, or a common table expression with a window function.

Uncorrelated subquery:

SELECT s1.article, dealer, s1.price
FROM shop s1
JOIN (
  SELECT article, MAX(price) AS price
  FROM shop
  GROUP BY article) AS s2
  ON s1.article = s2.article AND s1.price = s2.price
ORDER BY article;

LEFT JOIN:

SELECT s1.article, s1.dealer, s1.price
FROM shop s1
LEFT JOIN shop s2 ON s1.article = s2.article AND s1.price < s2.price
WHERE s2.article IS NULL
ORDER BY s1.article;

The LEFT JOIN works on the basis that when s1.price is at its maximum value, there is no
s2.price with a greater value and thus the corresponding s2.article value is NULL. See
Section 15.2.13.2, “JOIN Clause”.

Common table expression with window function:

WITH s1 AS (
   SELECT article, dealer, price,
          RANK() OVER (PARTITION BY article
                           ORDER BY price DESC
                      ) AS `Rank`

354

Using User-Defined Variables

     FROM shop
)
SELECT article, dealer, price
  FROM s1
  WHERE `Rank` = 1
ORDER BY article;

5.6.5 Using User-Defined Variables

You can employ MySQL user variables to remember results without having to store them in temporary
variables in the client. (See Section 11.4, “User-Defined Variables”.)

For example, to find the articles with the highest and lowest price you can do this:

mysql> SELECT @min_price:=MIN(price),@max_price:=MAX(price) FROM shop;
mysql> SELECT * FROM shop WHERE price=@min_price OR price=@max_price;
+---------+--------+-------+
| article | dealer | price |
+---------+--------+-------+
|    0003 | D      |  1.25 |
|    0004 | D      | 19.95 |
+---------+--------+-------+

Note

It is also possible to store the name of a database object such as a table or a
column in a user variable and then to use this variable in an SQL statement;
however, this requires the use of a prepared statement. See Section 15.5,
“Prepared Statements”, for more information.

5.6.6 Using Foreign Keys

MySQL supports foreign keys, which permit cross-referencing related data across tables, and foreign
key constraints, which help keep the related data consistent.

A foreign key relationship involves a parent table that holds the initial column values, and a child table
with column values that reference the parent column values. A foreign key constraint is defined on the
child table.

This following example relates parent and child tables through a single-column foreign key and
shows how a foreign key constraint enforces referential integrity.

Create the parent and child tables using the following SQL statements:

CREATE TABLE parent (
    id INT NOT NULL,
    PRIMARY KEY (id)
) ENGINE=INNODB;

CREATE TABLE child (
    id INT,
    parent_id INT,
    INDEX par_ind (parent_id),
    FOREIGN KEY (parent_id)
        REFERENCES parent(id)
) ENGINE=INNODB;

Insert a row into the parent table, like this:

mysql> INSERT INTO parent (id) VALUES ROW(1);

Verify that the data was inserted. You can do this simply by selecting all rows from parent, as shown
here:

mysql> TABLE parent;

355

Using Foreign Keys

+----+
| id |
+----+
|  1 |
+----+

Insert a row into the child table using the following SQL statement:

mysql> INSERT INTO child (id,parent_id) VALUES ROW(1,1);

The insert operation is successful because parent_id 1 is present in the parent table.

Insertion of a row into the child table with a parent_id value that is not present in the parent table is
rejected with an error, as you can see here:

mysql> INSERT INTO child (id,parent_id) VALUES ROW(2,2);
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
(`test`.`child`, CONSTRAINT `child_ibfk_1` FOREIGN KEY (`parent_id`)
REFERENCES `parent` (`id`))

The operation fails because the specified parent_id value does not exist in the parent table.

Trying to delete the previously inserted row from the parent table also fails, as shown here:

mysql> DELETE FROM parent WHERE id = 1;
ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails
(`test`.`child`, CONSTRAINT `child_ibfk_1` FOREIGN KEY (`parent_id`)
REFERENCES `parent` (`id`))

This operation fails because the record in the child table contains the referenced id (parent_id)
value.

When an operation affects a key value in the parent table that has matching rows in the child table,
the result depends on the referential action specified by ON UPDATE and ON DELETE subclauses of
the FOREIGN KEY clause. Omitting ON DELETE and ON UPDATE clauses (as in the current child table
definition) is the same as specifying the RESTRICT option, which rejects operations that affect a key
value in the parent table that has matching rows in the parent table.

To demonstrate ON DELETE and ON UPDATE referential actions, drop the child table and recreate it
to include ON UPDATE and ON DELETE subclauses with the CASCADE option. The CASCADE option
automatically deletes or updates matching rows in the child table when deleting or updating rows in the
parent table.

DROP TABLE child;

CREATE TABLE child (
    id INT,
    parent_id INT,
    INDEX par_ind (parent_id),
    FOREIGN KEY (parent_id)
        REFERENCES parent(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=INNODB;

Insert some rows into the child table using the statement shown here:

mysql> INSERT INTO child (id,parent_id) VALUES ROW(1,1), ROW(2,1), ROW(3,1);

Verify that the data was inserted, like this:

mysql> TABLE child;
+------+-----------+
| id   | parent_id |
+------+-----------+
|    1 |         1 |
|    2 |         1 |
|    3 |         1 |

356

Searching on Two Keys

+------+-----------+

Update the ID in the parent table, changing it from 1 to 2, using the SQL statement shown here:

mysql> UPDATE parent SET id = 2 WHERE id = 1;

Verify that the update was successful by selecting all rows from the parent table, as shown here:

mysql> TABLE parent;
+----+
| id |
+----+
|  2 |
+----+

Verify that the ON UPDATE CASCADE referential action updated the child table, like this:

mysql> TABLE child;
+------+-----------+
| id   | parent_id |
+------+-----------+
|    1 |         2 |
|    2 |         2 |
|    3 |         2 |
+------+-----------+

To demonstrate the ON DELETE CASCADE referential action, delete records from the parent table
where parent_id = 2; this deletes all records in the parent table.

mysql> DELETE FROM parent WHERE id = 2;

Because all records in the child table are associated with parent_id = 2, the ON DELETE CASCADE
referential action removes all records from the child table, as shown here:

mysql> TABLE child;
Empty set (0.00 sec)

For more information about foreign key constraints, see Section 15.1.20.5, “FOREIGN KEY
Constraints”.

5.6.7 Searching on Two Keys

An OR using a single key is well optimized, as is the handling of AND.

The one tricky case is that of searching on two different keys combined with OR:

SELECT field1_index, field2_index FROM test_table
WHERE field1_index = '1' OR  field2_index = '1'

This case is optimized. See Section 10.2.1.3, “Index Merge Optimization”.

You can also solve the problem efficiently by using a UNION that combines the output of two separate
SELECT statements. See Section 15.2.18, “UNION Clause”.

Each SELECT searches only one key and can be optimized:

SELECT field1_index, field2_index
    FROM test_table WHERE field1_index = '1'
UNION
SELECT field1_index, field2_index
    FROM test_table WHERE field2_index = '1';

5.6.8 Calculating Visits Per Day

The following example shows how you can use the bit group functions to calculate the number of days
per month a user has visited a Web page.

357

Using AUTO_INCREMENT

CREATE TABLE t1 (year YEAR, month INT UNSIGNED,
             day INT UNSIGNED);
INSERT INTO t1 VALUES(2000,1,1),(2000,1,20),(2000,1,30),(2000,2,2),
            (2000,2,23),(2000,2,23);

The example table contains year-month-day values representing visits by users to the page. To
determine how many different days in each month these visits occur, use this query:

SELECT year,month,BIT_COUNT(BIT_OR(1<<day)) AS days FROM t1
       GROUP BY year,month;

Which returns:

+------+-------+------+
| year | month | days |
+------+-------+------+
| 2000 |     1 |    3 |
| 2000 |     2 |    2 |
+------+-------+------+

The query calculates how many different days appear in the table for each year/month combination,
with automatic removal of duplicate entries.

5.6.9 Using AUTO_INCREMENT

The AUTO_INCREMENT attribute can be used to generate a unique identity for new rows:

CREATE TABLE animals (
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     name CHAR(30) NOT NULL,
     PRIMARY KEY (id)
);

INSERT INTO animals (name) VALUES
    ('dog'),('cat'),('penguin'),
    ('lax'),('whale'),('ostrich');

SELECT * FROM animals;

Which returns:

+----+---------+
| id | name    |
+----+---------+
|  1 | dog     |
|  2 | cat     |
|  3 | penguin |
|  4 | lax     |
|  5 | whale   |
|  6 | ostrich |
+----+---------+

No value was specified for the AUTO_INCREMENT column, so MySQL assigned sequence numbers
automatically. You can also explicitly assign 0 to the column to generate sequence numbers, unless
the NO_AUTO_VALUE_ON_ZERO SQL mode is enabled. For example:

INSERT INTO animals (id,name) VALUES(0,'groundhog');

If the column is declared NOT NULL, it is also possible to assign NULL to the column to generate
sequence numbers. For example:

INSERT INTO animals (id,name) VALUES(NULL,'squirrel');

When you insert any other value into an AUTO_INCREMENT column, the column is set to that value
and the sequence is reset so that the next automatically generated value follows sequentially from the
largest column value. For example:

INSERT INTO animals (id,name) VALUES(100,'rabbit');

358

Using AUTO_INCREMENT

INSERT INTO animals (id,name) VALUES(NULL,'mouse');
SELECT * FROM animals;
+-----+-----------+
| id  | name      |
+-----+-----------+
|   1 | dog       |
|   2 | cat       |
|   3 | penguin   |
|   4 | lax       |
|   5 | whale     |
|   6 | ostrich   |
|   7 | groundhog |
|   8 | squirrel  |
| 100 | rabbit    |
| 101 | mouse     |
+-----+-----------+

Updating an existing AUTO_INCREMENT column value also resets the AUTO_INCREMENT sequence.

You can retrieve the most recent automatically generated AUTO_INCREMENT value with the
LAST_INSERT_ID() SQL function or the mysql_insert_id() C API function. These functions
are connection-specific, so their return values are not affected by another connection which is also
performing inserts.

Use the smallest integer data type for the AUTO_INCREMENT column that is large enough to hold the
maximum sequence value you require. When the column reaches the upper limit of the data type, the
next attempt to generate a sequence number fails. Use the UNSIGNED attribute if possible to allow a
greater range. For example, if you use TINYINT, the maximum permissible sequence number is 127.
For TINYINT UNSIGNED, the maximum is 255. See Section 13.1.2, “Integer Types (Exact Value) -
INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT” for the ranges of all the integer types.

Note

For a multiple-row insert, LAST_INSERT_ID() and mysql_insert_id()
actually return the AUTO_INCREMENT key from the first of the inserted rows.
This enables multiple-row inserts to be reproduced correctly on other servers in
a replication setup.

To start with an AUTO_INCREMENT value other than 1, set that value with CREATE TABLE or ALTER
TABLE, like this:

mysql> ALTER TABLE tbl AUTO_INCREMENT = 100;

InnoDB Notes

For information about AUTO_INCREMENT usage specific to InnoDB, see Section 17.6.1.6,
“AUTO_INCREMENT Handling in InnoDB”.

MyISAM Notes

• For MyISAM tables, you can specify AUTO_INCREMENT on a secondary column in a multiple-

column index. In this case, the generated value for the AUTO_INCREMENT column is calculated as
MAX(auto_increment_column) + 1 WHERE prefix=given-prefix. This is useful when you
want to put data into ordered groups.

CREATE TABLE animals (
    grp ENUM('fish','mammal','bird') NOT NULL,
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    name CHAR(30) NOT NULL,
    PRIMARY KEY (grp,id)
) ENGINE=MyISAM;

INSERT INTO animals (grp,name) VALUES
    ('mammal','dog'),('mammal','cat'),
    ('bird','penguin'),('fish','lax'),('mammal','whale'),

359

Using MySQL with Apache

LOAD DATA INFILE '/local/access_log' INTO TABLE tbl_name
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'

The named table should be created to have columns that correspond to those that the LogFormat line
writes to the log file.

361

362

