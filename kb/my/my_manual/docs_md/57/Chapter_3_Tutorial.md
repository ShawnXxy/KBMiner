Entering Queries

need to specify a host name. Contact your administrator to find out what connection parameters you
should use to connect (that is, what host, user name, and password to use). Once you know the proper
parameters, you should be able to connect like this:

$> mysql -h host -u user -p
Enter password: ********

host and user represent the host name where your MySQL server is running and the user name of your
MySQL account. Substitute appropriate values for your setup. The ******** represents your password;
enter it when mysql displays the Enter password: prompt.

If that works, you should see some introductory information followed by a mysql> prompt:

$> mysql -h host -u user -p
Enter password: ********
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 25338 to server version: 5.7.44-standard

Type 'help;' or '\h' for help. Type '\c' to clear the buffer.

mysql>

The mysql> prompt tells you that mysql is ready for you to enter SQL statements.

If you are logging in on the same machine that MySQL is running on, you can omit the host, and simply
use the following:

$> mysql -u user -p

If, when you attempt to log in, you get an error message such as ERROR 2002 (HY000): Can't
connect to local MySQL server through socket '/tmp/mysql.sock' (2), it means that
the MySQL server daemon (Unix) or service (Windows) is not running. Consult the administrator or see the
section of Chapter 2, Installing and Upgrading MySQL that is appropriate to your operating system.

For help with other problems often encountered when trying to log in, see Section B.3.2, “Common Errors
When Using MySQL Programs”.

Some MySQL installations permit users to connect as the anonymous (unnamed) user to the server
running on the local host. If this is the case on your machine, you should be able to connect to that server
by invoking mysql without any options:

$> mysql

After you have connected successfully, you can disconnect any time by typing QUIT (or \q) at the mysql>
prompt:

mysql> QUIT
Bye

On Unix, you can also disconnect by pressing Control+D.

Most examples in the following sections assume that you are connected to the server. They indicate this by
the mysql> prompt.

3.2 Entering Queries

Make sure that you are connected to the server, as discussed in the previous section. Doing so does not in
itself select any database to work with, but that is okay. At this point, it is more important to find out a little
about how to issue queries than to jump right in creating tables, loading data into them, and retrieving data

270

Entering Queries

from them. This section describes the basic principles of entering queries, using several queries you can
try out to familiarize yourself with how mysql works.

Here is a simple query that asks the server to tell you its version number and the current date. Type it in as
shown here following the mysql> prompt and press Enter:

mysql> SELECT VERSION(), CURRENT_DATE;
+--------------+--------------+
| VERSION()    | CURRENT_DATE |
+--------------+--------------+
| 5.7.1-m4-log | 2012-12-25   |
+--------------+--------------+
1 row in set (0.01 sec)
mysql>

This query illustrates several things about mysql:

• A query normally consists of an SQL statement followed by a semicolon. (There are some exceptions
where a semicolon may be omitted. QUIT, mentioned earlier, is one of them. We'll get to others later.)

• When you issue a query, mysql sends it to the server for execution and displays the results, then prints

another mysql> prompt to indicate that it is ready for another query.

• mysql displays query output in tabular form (rows and columns). The first row contains labels for

the columns. The rows following are the query results. Normally, column labels are the names of the
columns you fetch from database tables. If you're retrieving the value of an expression rather than a
table column (as in the example just shown), mysql labels the column using the expression itself.

• mysql shows how many rows were returned and how long the query took to execute, which gives you

a rough idea of server performance. These values are imprecise because they represent wall clock time
(not CPU or machine time), and because they are affected by factors such as server load and network
latency. (For brevity, the “rows in set” line is sometimes not shown in the remaining examples in this
chapter.)

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

The queries shown thus far have been relatively short, single-line statements. You can even enter multiple
statements on a single line. Just end each one with a semicolon:

mysql> SELECT VERSION(); SELECT NOW();
+------------------+
| VERSION()        |
+------------------+
| 5.7.10-ndb-7.5.1 |
+------------------+
1 row in set (0.00 sec)

+---------------------+

271

Entering Queries

| NOW()               |
+---------------------+
| 2016-01-29 18:02:55 |
+---------------------+
1 row in set (0.00 sec)

A query need not be given all on a single line, so lengthy queries that require several lines are not a
problem. mysql determines where your statement ends by looking for the terminating semicolon, not by
looking for the end of the input line. (In other words, mysql accepts free-format input: it collects input lines
but does not execute them until it sees the semicolon.)

Here is a simple multiple-line statement:

mysql> SELECT
    -> USER()
    -> ,
    -> CURRENT_DATE;
+---------------+--------------+
| USER()        | CURRENT_DATE |
+---------------+--------------+
| jon@localhost | 2010-08-06   |
+---------------+--------------+

In this example, notice how the prompt changes from mysql> to -> after you enter the first line of a
multiple-line query. This is how mysql indicates that it has not yet seen a complete statement and is
waiting for the rest. The prompt is your friend, because it provides valuable feedback. If you use that
feedback, you can always be aware of what mysql is waiting for.

If you decide you do not want to execute a query that you are in the process of entering, cancel it by typing
\c:

mysql> SELECT
    -> USER()
    -> \c
mysql>

Here, too, notice the prompt. It switches back to mysql> after you type \c, providing feedback to indicate
that mysql is ready for a new query.

The following table shows each of the prompts you may see and summarizes what they mean about the
state that mysql is in.

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

Multiple-line statements commonly occur by accident when you intend to issue a query on a single line, but
forget the terminating semicolon. In this case, mysql waits for more input:

272

Creating and Using a Database

mysql> SELECT USER()
    ->

If this happens to you (you think you've entered a statement but the only response is a -> prompt), most
likely mysql is waiting for the semicolon. If you don't notice what the prompt is telling you, you might sit
there for a while before realizing what you need to do. Enter a semicolon to complete the statement, and
mysql executes it:

mysql> SELECT USER()
    -> ;
+---------------+
| USER()        |
+---------------+
| jon@localhost |
+---------------+

The '> and "> prompts occur during string collection (another way of saying that MySQL is waiting
for completion of a string). In MySQL, you can write strings surrounded by either ' or " characters (for
example, 'hello' or "goodbye"), and mysql lets you enter strings that span multiple lines. When
you see a '> or "> prompt, it means that you have entered a line containing a string that begins with a '
or " quote character, but have not yet entered the matching quote that terminates the string. This often
indicates that you have inadvertently left out a quote character. For example:

mysql> SELECT * FROM my_table WHERE name = 'Smith AND age < 30;
    '>

If you enter this SELECT statement, then press Enter and wait for the result, nothing happens. Instead
of wondering why this query takes so long, notice the clue provided by the '> prompt. It tells you that
mysql expects to see the rest of an unterminated string. (Do you see the error in the statement? The string
'Smith is missing the second single quotation mark.)

At this point, what do you do? The simplest thing is to cancel the query. However, you cannot just type \c
in this case, because mysql interprets it as part of the string that it is collecting. Instead, enter the closing
quote character (so mysql knows you've finished the string), then type \c:

mysql> SELECT * FROM my_table WHERE name = 'Smith AND age < 30;
    '> '\c
mysql>

The prompt changes back to mysql>, indicating that mysql is ready for a new query.

The `> prompt is similar to the '> and "> prompts, but indicates that you have begun but not completed a
backtick-quoted identifier.

It is important to know what the '>, ">, and `> prompts signify, because if you mistakenly enter an
unterminated string, any further lines you type appear to be ignored by mysql—including a line containing
QUIT. This can be quite confusing, especially if you do not know that you need to supply the terminating
quote before you can cancel the current query.

Note

Multiline statements from this point on are written without the secondary (->
or other) prompts, to make it easier to copy and paste the statements to try for
yourself.

3.3 Creating and Using a Database

Once you know how to enter SQL statements, you are ready to access a database.

273

Retrieving Information from a Table

When you want to add new records one at a time, the INSERT statement is useful. In its simplest form,
you supply values for each column, in the order in which the columns were listed in the CREATE TABLE
statement. Suppose that Diane gets a new hamster named “Puffball.” You could add a new record using
an INSERT statement like this:

mysql> INSERT INTO pet
       VALUES ('Puffball','Diane','hamster','f','1999-03-30',NULL);

String and date values are specified as quoted strings here. Also, with INSERT, you can insert NULL
directly to represent a missing value. You do not use \N like you do with LOAD DATA.

From this example, you should be able to see that there would be a lot more typing involved to load your
records initially using several INSERT statements rather than a single LOAD DATA statement.

3.3.4 Retrieving Information from a Table

The SELECT statement is used to pull information from a table. The general form of the statement is:

SELECT what_to_select
FROM which_table
WHERE conditions_to_satisfy;

what_to_select indicates what you want to see. This can be a list of columns, or * to indicate “all
columns.” which_table indicates the table from which you want to retrieve data. The WHERE clause
is optional. If it is present, conditions_to_satisfy specifies one or more conditions that rows must
satisfy to qualify for retrieval.

3.3.4.1 Selecting All Data

The simplest form of SELECT retrieves everything from a table:

mysql> SELECT * FROM pet;
+----------+--------+---------+------+------------+------------+
| name     | owner  | species | sex  | birth      | death      |
+----------+--------+---------+------+------------+------------+
| Fluffy   | Harold | cat     | f    | 1993-02-04 | NULL       |
| Claws    | Gwen   | cat     | m    | 1994-03-17 | NULL       |
| Buffy    | Harold | dog     | f    | 1989-05-13 | NULL       |
| Fang     | Benny  | dog     | m    | 1990-08-27 | NULL       |
| Bowser   | Diane  | dog     | m    | 1979-08-31 | 1995-07-29 |
| Chirpy   | Gwen   | bird    | f    | 1998-09-11 | NULL       |
| Whistler | Gwen   | bird    | NULL | 1997-12-09 | NULL       |
| Slim     | Benny  | snake   | m    | 1996-04-29 | NULL       |
| Puffball | Diane  | hamster | f    | 1999-03-30 | NULL       |
+----------+--------+---------+------+------------+------------+

This form of SELECT uses *, which is shorthand for “select all columns.” This is useful if you want to review
your entire table, for example, after you've just loaded it with your initial data set. For example, you may
happen to think that the birth date for Bowser does not seem quite right. Consulting your original pedigree
papers, you find that the correct birth year should be 1989, not 1979.

There are at least two ways to fix this:

• Edit the file pet.txt to correct the error, then empty the table and reload it using DELETE and LOAD

DATA:

mysql> DELETE FROM pet;
mysql> LOAD DATA LOCAL INFILE '/path/pet.txt' INTO TABLE pet;

However, if you do this, you must also re-enter the record for Puffball.

278

Retrieving Information from a Table

• Fix only the erroneous record with an UPDATE statement:

mysql> UPDATE pet SET birth = '1989-08-31' WHERE name = 'Bowser';

The UPDATE changes only the record in question and does not require you to reload the table.

3.3.4.2 Selecting Particular Rows

As shown in the preceding section, it is easy to retrieve an entire table. Just omit the WHERE clause from
the SELECT statement. But typically you don't want to see the entire table, particularly when it becomes
large. Instead, you're usually more interested in answering a particular question, in which case you specify
some constraints on the information you want. Let's look at some selection queries in terms of questions
about your pets that they answer.

You can select only particular rows from your table. For example, if you want to verify the change that you
made to Bowser's birth date, select Bowser's record like this:

mysql> SELECT * FROM pet WHERE name = 'Bowser';
+--------+-------+---------+------+------------+------------+
| name   | owner | species | sex  | birth      | death      |
+--------+-------+---------+------+------------+------------+
| Bowser | Diane | dog     | m    | 1989-08-31 | 1995-07-29 |
+--------+-------+---------+------+------------+------------+

The output confirms that the year is correctly recorded as 1989, not 1979.

String comparisons normally are case-insensitive, so you can specify the name as 'bowser', 'BOWSER',
and so forth. The query result is the same.

You can specify conditions on any column, not just name. For example, if you want to know which animals
were born during or after 1998, test the birth column:

mysql> SELECT * FROM pet WHERE birth >= '1998-1-1';
+----------+-------+---------+------+------------+-------+
| name     | owner | species | sex  | birth      | death |
+----------+-------+---------+------+------------+-------+
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

AND and OR may be intermixed, although AND has higher precedence than OR. If you use both operators, it
is a good idea to use parentheses to indicate explicitly how conditions should be grouped:

279

Retrieving Information from a Table

mysql> SELECT * FROM pet WHERE (species = 'cat' AND sex = 'm')
       OR (species = 'dog' AND sex = 'f');
+-------+--------+---------+------+------------+-------+
| name  | owner  | species | sex  | birth      | death |
+-------+--------+---------+------+------------+-------+
| Claws | Gwen   | cat     | m    | 1994-03-17 | NULL  |
| Buffy | Harold | dog     | f    | 1989-05-13 | NULL  |
+-------+--------+---------+------+------------+-------+

3.3.4.3 Selecting Particular Columns

If you do not want to see entire rows from your table, just name the columns in which you are interested,
separated by commas. For example, if you want to know when your animals were born, select the name
and birth columns:

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
| Benny  |
| Diane  |
+--------+

Notice that the query simply retrieves the owner column from each record, and some of them appear more
than once. To minimize the output, retrieve each unique output record just once by adding the keyword
DISTINCT:

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

280

Retrieving Information from a Table

| Buffy | 1989-05-13 |
+-------+------------+

There is a small complication if the current month is December. You cannot merely add one to the month
number (12) and look for animals born in month 13, because there is no such month. Instead, you look for
animals born in January (month 1).

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

MONTH() returns a number between 1 and 12. And MOD(something,12) returns a number between 0
and 11. So the addition has to be after the MOD(), otherwise we would go from November (11) to January
(1).

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

3.3.4.6 Working with NULL Values

The NULL value can be surprising until you get used to it. Conceptually, NULL means “a missing unknown
value” and it is treated somewhat differently from other values.

To test for NULL, use the IS NULL and IS NOT NULL operators, as shown here:

mysql> SELECT 1 IS NULL, 1 IS NOT NULL;
+-----------+---------------+
| 1 IS NULL | 1 IS NOT NULL |
+-----------+---------------+
|         0 |             1 |
+-----------+---------------+

You cannot use arithmetic comparison operators such as =, <, or <> to test for NULL. To demonstrate this
for yourself, try the following query:

284

Retrieving Information from a Table

mysql> SELECT 1 = NULL, 1 <> NULL, 1 < NULL, 1 > NULL;
+----------+-----------+----------+----------+
| 1 = NULL | 1 <> NULL | 1 < NULL | 1 > NULL |
+----------+-----------+----------+----------+
|     NULL |      NULL |     NULL |     NULL |
+----------+-----------+----------+----------+

Because the result of any arithmetic comparison with NULL is also NULL, you cannot obtain any meaningful
results from such comparisons.

In MySQL, 0 or NULL means false and anything else means true. The default truth value from a boolean
operation is 1.

This special treatment of NULL is why, in the previous section, it was necessary to determine which
animals are no longer alive using death IS NOT NULL instead of death <> NULL.

Two NULL values are regarded as equal in a GROUP BY.

When doing an ORDER BY, NULL values are presented first if you do ORDER BY ... ASC and last if you
do ORDER BY ... DESC.

A common error when working with NULL is to assume that it is not possible to insert a zero or an empty
string into a column defined as NOT NULL, but this is not the case. These are in fact values, whereas NULL
means “not having a value.” You can test this easily enough by using IS [NOT] NULL as shown:

mysql> SELECT 0 IS NULL, 0 IS NOT NULL, '' IS NULL, '' IS NOT NULL;
+-----------+---------------+------------+----------------+
| 0 IS NULL | 0 IS NOT NULL | '' IS NULL | '' IS NOT NULL |
+-----------+---------------+------------+----------------+
|         0 |             1 |          0 |              1 |
+-----------+---------------+------------+----------------+

Thus it is entirely possible to insert a zero or empty string into a NOT NULL column, as these are in fact
NOT NULL. See Section B.3.4.3, “Problems with NULL Values”.

3.3.4.7 Pattern Matching

MySQL provides standard SQL pattern matching as well as a form of pattern matching based on extended
regular expressions similar to those used by Unix utilities such as vi, grep, and sed.

SQL pattern matching enables you to use _ to match any single character and % to match an arbitrary
number of characters (including zero characters). In MySQL, SQL patterns are case-insensitive by default.
Some examples are shown here. Do not use = or <> when you use SQL patterns. Use the LIKE or NOT
LIKE comparison operators instead.

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
| name   | owner  | species | sex  | birth      | death |
+--------+--------+---------+------+------------+-------+
| Fluffy | Harold | cat     | f    | 1993-02-04 | NULL  |

285

Retrieving Information from a Table

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
test for a match for this type of pattern, use the REGEXP and NOT REGEXP operators (or RLIKE and NOT
RLIKE, which are synonyms).

The following list describes some characteristics of extended regular expressions:

• . matches any single character.

• A character class [...] matches any character within the brackets. For example, [abc] matches a, b,
or c. To name a range of characters, use a dash. [a-z] matches any letter, whereas [0-9] matches
any digit.

• * matches zero or more instances of the thing preceding it. For example, x* matches any number of x

characters, [0-9]* matches any number of digits, and .* matches any number of anything.

• A regular expression pattern match succeeds if the pattern matches anywhere in the value being tested.
(This differs from a LIKE pattern match, which succeeds only if the pattern matches the entire value.)

• To anchor a pattern so that it must match the beginning or end of the value being tested, use ^ at the

beginning or $ at the end of the pattern.

To demonstrate how extended regular expressions work, the LIKE queries shown previously are rewritten
here to use REGEXP.

To find names beginning with b, use ^ to match the beginning of the name:

mysql> SELECT * FROM pet WHERE name REGEXP '^b';
+--------+--------+---------+------+------------+------------+
| name   | owner  | species | sex  | birth      | death      |
+--------+--------+---------+------+------------+------------+
| Buffy  | Harold | dog     | f    | 1989-05-13 | NULL       |
| Bowser | Diane  | dog     | m    | 1989-08-31 | 1995-07-29 |
+--------+--------+---------+------+------------+------------+

To force a REGEXP comparison to be case-sensitive, use the BINARY keyword to make one of the strings a
binary string. This query matches only lowercase b at the beginning of a name:

SELECT * FROM pet WHERE name REGEXP BINARY '^b';

286

Retrieving Information from a Table

To find names ending with fy, use $ to match the end of the name:

mysql> SELECT * FROM pet WHERE name REGEXP 'fy$';
+--------+--------+---------+------+------------+-------+
| name   | owner  | species | sex  | birth      | death |
+--------+--------+---------+------+------------+-------+
| Fluffy | Harold | cat     | f    | 1993-02-04 | NULL  |
| Buffy  | Harold | dog     | f    | 1989-05-13 | NULL  |
+--------+--------+---------+------+------------+-------+

To find names containing a w, use this query:

mysql> SELECT * FROM pet WHERE name REGEXP 'w';
+----------+-------+---------+------+------------+------------+
| name     | owner | species | sex  | birth      | death      |
+----------+-------+---------+------+------------+------------+
| Claws    | Gwen  | cat     | m    | 1994-03-17 | NULL       |
| Bowser   | Diane | dog     | m    | 1989-08-31 | 1995-07-29 |
| Whistler | Gwen  | bird    | NULL | 1997-12-09 | NULL       |
+----------+-------+---------+------+------------+------------+

Because a regular expression pattern matches if it occurs anywhere in the value, it is not necessary in the
previous query to put a wildcard on either side of the pattern to get it to match the entire value as would be
true with an SQL pattern.

To find names containing exactly five characters, use ^ and $ to match the beginning and end of the name,
and five instances of . in between:

mysql> SELECT * FROM pet WHERE name REGEXP '^.....$';
+-------+--------+---------+------+------------+-------+
| name  | owner  | species | sex  | birth      | death |
+-------+--------+---------+------+------------+-------+
| Claws | Gwen   | cat     | m    | 1994-03-17 | NULL  |
| Buffy | Harold | dog     | f    | 1989-05-13 | NULL  |
+-------+--------+---------+------+------------+-------+

You could also write the previous query using the {n} (“repeat-n-times”) operator:

mysql> SELECT * FROM pet WHERE name REGEXP '^.{5}$';
+-------+--------+---------+------+------------+-------+
| name  | owner  | species | sex  | birth      | death |
+-------+--------+---------+------+------------+-------+
| Claws | Gwen   | cat     | m    | 1994-03-17 | NULL  |
| Buffy | Harold | dog     | f    | 1989-05-13 | NULL  |
+-------+--------+---------+------+------------+-------+

For more information about the syntax for regular expressions, see Section 12.8.2, “Regular Expressions”.

3.3.4.8 Counting Rows

Databases are often used to answer the question, “How often does a certain type of data occur in a table?”
For example, you might want to know how many pets you have, or how many pets each owner has, or you
might want to perform various kinds of census operations on your animals.

Counting the total number of animals you have is the same question as “How many rows are in the pet
table?” because there is one record per pet. COUNT(*) counts the number of rows, so the query to count
your animals looks like this:

mysql> SELECT COUNT(*) FROM pet;
+----------+
| COUNT(*) |
+----------+
|        9 |

287

Retrieving Information from a Table

+----------+

Earlier, you retrieved the names of the people who owned pets. You can use COUNT() if you want to find
out how many pets each owner has:

mysql> SELECT owner, COUNT(*) FROM pet GROUP BY owner;
+--------+----------+
| owner  | COUNT(*) |
+--------+----------+
| Benny  |        2 |
| Diane  |        2 |
| Gwen   |        3 |
| Harold |        2 |
+--------+----------+

The preceding query uses GROUP BY to group all records for each owner. The use of COUNT() in
conjunction with GROUP BY is useful for characterizing your data under various groupings. The following
examples show different ways to perform animal census operations.

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

288

Retrieving Information from a Table

• The pet name so that you know which animal each event pertains to.

• A date so that you know when the event occurred.

• A field to describe the event.

• An event type field, if you want to be able to categorize events.

Given these considerations, the CREATE TABLE statement for the event table might look like this:

mysql> CREATE TABLE event (name VARCHAR(20), date DATE,
       type VARCHAR(15), remark VARCHAR(255));

As with the pet table, it is easiest to load the initial records by creating a tab-delimited text file containing
the following information.

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

1998-03-17

Whistler

1998-12-09

Load the records like this:

type

litter

litter

litter

vet

vet

kennel

kennel

birthday

birthday

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

First birthday

mysql> LOAD DATA LOCAL INFILE 'event.txt' INTO TABLE event;

Based on what you have learned from the queries that you have run on the pet table, you should be able
to perform retrievals on the records in the event table; the principles are the same. But when is the event
table by itself insufficient to answer questions you might ask?

Suppose that you want to find out the ages at which each pet had its litters. We saw earlier how to
calculate ages from two dates. The litter date of the mother is in the event table, but to calculate her age
on that date you need her birth date, which is stored in the pet table. This means the query requires both
tables:

mysql> SELECT pet.name,
       TIMESTAMPDIFF(YEAR,birth,date) AS age,
       remark
       FROM pet INNER JOIN event
         ON pet.name = event.name
       WHERE event.type = 'litter';
+--------+------+-----------------------------+
| name   | age  | remark                      |

290

Getting Information About Databases and Tables

+--------+------+-----------------------------+
| Fluffy |    2 | 4 kittens, 3 female, 1 male |
| Buffy  |    4 | 5 puppies, 2 female, 3 male |
| Buffy  |    5 | 3 puppies, 3 female         |
+--------+------+-----------------------------+

There are several things to note about this query:

• The FROM clause joins two tables because the query needs to pull information from both of them.

• When combining (joining) information from multiple tables, you need to specify how records in one table
can be matched to records in the other. This is easy because they both have a name column. The query
uses an ON clause to match up records in the two tables based on the name values.

The query uses an INNER JOIN to combine the tables. An INNER JOIN permits rows from either table
to appear in the result if and only if both tables meet the conditions specified in the ON clause. In this
example, the ON clause specifies that the name column in the pet table must match the name column in
the event table. If a name appears in one table but not the other, the row does not appear in the result
because the condition in the ON clause fails.

• Because the name column occurs in both tables, you must be specific about which table you mean when

referring to the column. This is done by prepending the table name to the column name.

You need not have two different tables to perform a join. Sometimes it is useful to join a table to itself, if
you want to compare records in a table to other records in that same table. For example, to find breeding
pairs among your pets, you can join the pet table with itself to produce candidate pairs of live males and
females of like species:

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

3.4 Getting Information About Databases and Tables

What if you forget the name of a database or table, or what the structure of a given table is (for example,
what its columns are called)? MySQL addresses this problem through several statements that provide
information about the databases and tables it supports.

You have previously seen SHOW DATABASES, which lists the databases managed by the server. To find
out which database is currently selected, use the DATABASE() function:

mysql> SELECT DATABASE();
+------------+
| DATABASE() |
+------------+
| menagerie  |
+------------+

If you have not yet selected any database, the result is NULL.

291

Using mysql in Batch Mode

To find out what tables the default database contains (for example, when you are not sure about the name
of a table), use this statement:

mysql> SHOW TABLES;
+---------------------+
| Tables_in_menagerie |
+---------------------+
| event               |
| pet                 |
+---------------------+

The name of the column in the output produced by this statement is always Tables_in_db_name, where
db_name is the name of the database. See Section 13.7.5.37, “SHOW TABLES Statement”, for more
information.

If you want to find out about the structure of a table, the DESCRIBE statement is useful; it displays
information about each of a table's columns:

mysql> DESCRIBE pet;
+---------+-------------+------+-----+---------+-------+
| Field   | Type        | Null | Key | Default | Extra |
+---------+-------------+------+-----+---------+-------+
| name    | varchar(20) | YES  |     | NULL    |       |
| owner   | varchar(20) | YES  |     | NULL    |       |
| species | varchar(20) | YES  |     | NULL    |       |
| sex     | char(1)     | YES  |     | NULL    |       |
| birth   | date        | YES  |     | NULL    |       |
| death   | date        | YES  |     | NULL    |       |
+---------+-------------+------+-----+---------+-------+

Field indicates the column name, Type is the data type for the column, NULL indicates whether the
column can contain NULL values, Key indicates whether the column is indexed, and Default specifies the
column's default value. Extra displays special information about columns: If a column was created with
the AUTO_INCREMENT option, the value is auto_increment rather than empty.

DESC is a short form of DESCRIBE. See Section 13.8.1, “DESCRIBE Statement”, for more information.

You can obtain the CREATE TABLE statement necessary to create an existing table using the SHOW
CREATE TABLE statement. See Section 13.7.5.10, “SHOW CREATE TABLE Statement”.

If you have indexes on a table, SHOW INDEX FROM tbl_name produces information about them. See
Section 13.7.5.22, “SHOW INDEX Statement”, for more about this statement.

3.5 Using mysql in Batch Mode

In the previous sections, you used mysql interactively to enter statements and view the results. You can
also run mysql in batch mode. To do this, put the statements you want to run in a file, then tell mysql to
read its input from the file:

$> mysql < batch-file

If you are running mysql under Windows and have some special characters in the file that cause
problems, you can do this:

C:\> mysql -e "source batch-file"

If you need to specify connection parameters on the command line, the command might look like this:

$> mysql -h host -u user -p < batch-file
Enter password: ********

292

Using mysql in Batch Mode

When you use mysql this way, you are creating a script file, then executing the script.

If you want the script to continue even if some of the statements in it produce errors, you should use the --
force command-line option.

Why use a script? Here are a few reasons:

• If you run a query repeatedly (say, every day or every week), making it a script enables you to avoid

retyping it each time you execute it.

• You can generate new queries from existing ones that are similar by copying and editing script files.

• Batch mode can also be useful while you are developing a query, particularly for multiple-line statements
or multiple-statement sequences. If you make a mistake, you do not have to retype everything. Just edit
your script to correct the error, then tell mysql to execute it again.

• If you have a query that produces a lot of output, you can run the output through a pager rather than

watching it scroll off the top of your screen:

$> mysql < batch-file | more

• You can catch the output in a file for further processing:

$> mysql < batch-file > mysql.out

• You can distribute your script to other people so that they can also run the statements.

• Some situations do not allow for interactive use, for example, when you run a query from a cron job. In

this case, you must use batch mode.

The default output format is different (more concise) when you run mysql in batch mode than when you
use it interactively. For example, the output of SELECT DISTINCT species FROM pet looks like this
when mysql is run interactively:

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

If you want to get the interactive output format in batch mode, use mysql -t. To echo to the output the
statements that are executed, use mysql -v.

You can also use scripts from the mysql prompt by using the source command or \. command:

mysql> source filename;
mysql> \. filename

See Section 4.5.1.5, “Executing SQL Statements from a Text File”, for more information.

293

Examples of Common Queries

3.6 Examples of Common Queries

Here are examples of how to solve some common problems with MySQL.

Some of the examples use the table shop to hold the price of each article (item number) for certain traders
(dealers). Supposing that each trader has a single fixed price per article, then (article, dealer) is a
primary key for the records.

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

3.6.1 The Maximum Value for a Column

“What is the highest item number?”

SELECT MAX(article) AS article FROM shop;

+---------+
| article |
+---------+
|       4 |
+---------+

3.6.2 The Row Holding the Maximum of a Certain Column

Task: Find the number, dealer, and price of the most expensive article.

This is easily done with a subquery:

SELECT article, dealer, price
FROM   shop
WHERE  price=(SELECT MAX(price) FROM shop);

+---------+--------+-------+
| article | dealer | price |

294

Maximum of Column per Group

+---------+--------+-------+
|    0004 | D      | 19.95 |
+---------+--------+-------+

Another solution is to use a LEFT JOIN, as shown here:

SELECT s1.article, s1.dealer, s1.price
FROM shop s1
LEFT JOIN shop s2 ON s1.price < s2.price
WHERE s2.article IS NULL;

You can also do this by sorting all rows descending by price and get only the first row using the MySQL-
specific LIMIT clause, like this:

SELECT article, dealer, price
FROM shop
ORDER BY price DESC
LIMIT 1;

Note

If there were several most expensive articles, each with a price of 19.95, the LIMIT
solution would show only one of them.

3.6.3 Maximum of Column per Group

Task: Find the highest price per article.

SELECT article, MAX(price) AS price
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

3.6.4 The Rows Holding the Group-wise Maximum of a Certain Column

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

295

Using Foreign Keys

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

mysql> INSERT INTO parent (id) VALUES (1);

Verify that the data was inserted. You can do this simply by selecting all rows from parent, as shown
here:

mysql> SELECT * FROM parent;
+----+
| id |
+----+
|  1 |
+----+

Insert a row into the child table using the following SQL statement:

mysql> INSERT INTO child (id,parent_id) VALUES (1,1);

The insert operation is successful because parent_id 1 is present in the parent table.

Insertion of a row into the child table with a parent_id value that is not present in the parent table is
rejected with an error, as you can see here:

mysql> INSERT INTO child (id,parent_id) VALUES(2,2);
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
(`test`.`child`, CONSTRAINT `child_ibfk_1` FOREIGN KEY (`parent_id`)
REFERENCES `parent` (`id`))

The operation fails because the specified parent_id value does not exist in the parent table.

Trying to delete the previously inserted row from the parent table also fails, as shown here:

mysql> DELETE FROM parent WHERE id = 1;
ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails
(`test`.`child`, CONSTRAINT `child_ibfk_1` FOREIGN KEY (`parent_id`)
REFERENCES `parent` (`id`))

This operation fails because the record in the child table contains the referenced id (parent_id) value.

When an operation affects a key value in the parent table that has matching rows in the child table,
the result depends on the referential action specified by ON UPDATE and ON DELETE subclauses of
the FOREIGN KEY clause. Omitting ON DELETE and ON UPDATE clauses (as in the current child table
definition) is the same as specifying the RESTRICT option, which rejects operations that affect a key value
in the parent table that has matching rows in the parent table.

To demonstrate ON DELETE and ON UPDATE referential actions, drop the child table and recreate it
to include ON UPDATE and ON DELETE subclauses with the CASCADE option. The CASCADE option

297

Using Foreign Keys

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

mysql> INSERT INTO child (id,parent_id) VALUES(1,1),(2,1),(3,1);

Verify that the data was inserted, like this:

mysql> SELECT * FROM child;
+------+-----------+
| id   | parent_id |
+------+-----------+
|    1 |         1 |
|    2 |         1 |
|    3 |         1 |
+------+-----------+

Update the ID in the parent table, changing it from 1 to 2, using the SQL statement shown here:

mysql> UPDATE parent SET id = 2 WHERE id = 1;

Verify that the update was successful by selecting all rows from the parent table, as shown here:

mysql> SELECT * FROM parent;
+----+
| id |
+----+
|  2 |
+----+

Verify that the ON UPDATE CASCADE referential action updated the child table, like this:

mysql> SELECT * FROM child;
+------+-----------+
| id   | parent_id |
+------+-----------+
|    1 |         2 |
|    2 |         2 |
|    3 |         2 |
+------+-----------+

To demonstrate the ON DELETE CASCADE referential action, delete records from the parent table where
parent_id = 2; this deletes all records in the parent table.

mysql> DELETE FROM parent WHERE id = 2;

Because all records in the child table are associated with parent_id = 2, the ON DELETE CASCADE
referential action removes all records from the child table, as shown here:

mysql> SELECT * FROM child;
Empty set (0.00 sec)

298

Searching on Two Keys

For more information about foreign key constraints, see Section 13.1.18.5, “FOREIGN KEY Constraints”.

3.6.7 Searching on Two Keys

An OR using a single key is well optimized, as is the handling of AND.

The one tricky case is that of searching on two different keys combined with OR:

SELECT field1_index, field2_index FROM test_table
WHERE field1_index = '1' OR  field2_index = '1'

This case is optimized. See Section 8.2.1.3, “Index Merge Optimization”.

You can also solve the problem efficiently by using a UNION that combines the output of two separate
SELECT statements. See Section 13.2.9.3, “UNION Clause”.

Each SELECT searches only one key and can be optimized:

SELECT field1_index, field2_index
    FROM test_table WHERE field1_index = '1'
UNION
SELECT field1_index, field2_index
    FROM test_table WHERE field2_index = '1';

3.6.8 Calculating Visits Per Day

The following example shows how you can use the bit group functions to calculate the number of days per
month a user has visited a Web page.

CREATE TABLE t1 (year YEAR, month INT UNSIGNED,
             day INT UNSIGNED);
INSERT INTO t1 VALUES(2000,1,1),(2000,1,20),(2000,1,30),(2000,2,2),
            (2000,2,23),(2000,2,23);

The example table contains year-month-day values representing visits by users to the page. To determine
how many different days in each month these visits occur, use this query:

SELECT year,month,BIT_COUNT(BIT_OR(1<<day)) AS days FROM t1
       GROUP BY year,month;

Which returns:

+------+-------+------+
| year | month | days |
+------+-------+------+
| 2000 |     1 |    3 |
| 2000 |     2 |    2 |
+------+-------+------+

The query calculates how many different days appear in the table for each year/month combination, with
automatic removal of duplicate entries.

3.6.9 Using AUTO_INCREMENT

The AUTO_INCREMENT attribute can be used to generate a unique identity for new rows:

CREATE TABLE animals (
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     name CHAR(30) NOT NULL,
     PRIMARY KEY (id)
);

299

Using AUTO_INCREMENT

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
automatically. You can also explicitly assign 0 to the column to generate sequence numbers, unless the
NO_AUTO_VALUE_ON_ZERO SQL mode is enabled. For example:

INSERT INTO animals (id,name) VALUES(0,'groundhog');

If the column is declared NOT NULL, it is also possible to assign NULL to the column to generate sequence
numbers. For example:

INSERT INTO animals (id,name) VALUES(NULL,'squirrel');

When you insert any other value into an AUTO_INCREMENT column, the column is set to that value and
the sequence is reset so that the next automatically generated value follows sequentially from the largest
column value. For example:

INSERT INTO animals (id,name) VALUES(100,'rabbit');
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

Updating an existing AUTO_INCREMENT column value in an InnoDB table does not reset the
AUTO_INCREMENT sequence as it does for MyISAM and NDB tables.

You can retrieve the most recent automatically generated AUTO_INCREMENT value with the
LAST_INSERT_ID() SQL function or the mysql_insert_id() C API function. These functions are
connection-specific, so their return values are not affected by another connection which is also performing
inserts.

Use the smallest integer data type for the AUTO_INCREMENT column that is large enough to hold the
maximum sequence value you need. When the column reaches the upper limit of the data type, the
next attempt to generate a sequence number fails. Use the UNSIGNED attribute if possible to allow a

300

Using AUTO_INCREMENT

greater range. For example, if you use TINYINT, the maximum permissible sequence number is 127. For
TINYINT UNSIGNED, the maximum is 255. See Section 11.1.2, “Integer Types (Exact Value) - INTEGER,
INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT” for the ranges of all the integer types.

Note

For a multiple-row insert, LAST_INSERT_ID() and mysql_insert_id() actually
return the AUTO_INCREMENT key from the first of the inserted rows. This enables
multiple-row inserts to be reproduced correctly on other servers in a replication
setup.

To start with an AUTO_INCREMENT value other than 1, set that value with CREATE TABLE or ALTER
TABLE, like this:

mysql> ALTER TABLE tbl AUTO_INCREMENT = 100;

InnoDB Notes

For information about AUTO_INCREMENT usage specific to InnoDB, see Section 14.6.1.6,
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
    ('bird','ostrich');

SELECT * FROM animals ORDER BY grp,id;

Which returns:

+--------+----+---------+
| grp    | id | name    |
+--------+----+---------+
| fish   |  1 | lax     |
| mammal |  1 | dog     |
| mammal |  2 | cat     |
| mammal |  3 | whale   |
| bird   |  1 | penguin |
| bird   |  2 | ostrich |
+--------+----+---------+

In this case (when the AUTO_INCREMENT column is part of a multiple-column index), AUTO_INCREMENT
values are reused if you delete the row with the biggest AUTO_INCREMENT value in any group. This
happens even for MyISAM tables, for which AUTO_INCREMENT values normally are not reused.

• If the AUTO_INCREMENT column is part of multiple indexes, MySQL generates sequence values using
the index that begins with the AUTO_INCREMENT column, if there is one. For example, if the animals

301

Using MySQL with Apache

table contained indexes PRIMARY KEY (grp, id) and INDEX (id), MySQL would ignore the
PRIMARY KEY for generating sequence values. As a result, the table would contain a single sequence,
not a sequence per grp value.

Further Reading

More information about AUTO_INCREMENT is available here:

• How to assign the AUTO_INCREMENT attribute to a column: Section 13.1.18, “CREATE TABLE

Statement”, and Section 13.1.8, “ALTER TABLE Statement”.

• How AUTO_INCREMENT behaves depending on the NO_AUTO_VALUE_ON_ZERO SQL mode:

Section 5.1.10, “Server SQL Modes”.

• How to use the LAST_INSERT_ID() function to find the row that contains the most recent

AUTO_INCREMENT value: Section 12.15, “Information Functions”.

• Setting the AUTO_INCREMENT value to be used: Section 5.1.7, “Server System Variables”.

• Section 14.6.1.6, “AUTO_INCREMENT Handling in InnoDB”

• AUTO_INCREMENT and replication: Section 16.4.1.1, “Replication and AUTO_INCREMENT”.

• Server-system variables related to AUTO_INCREMENT (auto_increment_increment and

auto_increment_offset) that can be used for replication: Section 5.1.7, “Server System Variables”.

3.7 Using MySQL with Apache

There are programs that let you authenticate your users from a MySQL database and also let you write
your log files into a MySQL table.

You can change the Apache logging format to be easily readable by MySQL by putting the following into
the Apache configuration file:

LogFormat \
        "\"%h\",%{%Y%m%d%H%M%S}t,%>s,\"%b\",\"%{Content-Type}o\",  \
        \"%U\",\"%{Referer}i\",\"%{User-Agent}i\""

To load a log file in that format into MySQL, you can use a statement something like this:

LOAD DATA INFILE '/local/access_log' INTO TABLE tbl_name
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'

The named table should be created to have columns that correspond to those that the LogFormat line
writes to the log file.

302

