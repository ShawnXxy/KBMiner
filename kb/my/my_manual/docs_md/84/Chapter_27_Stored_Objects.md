Defining Stored Programs

This chapter describes how to use stored objects. The following sections provide additional information
about SQL syntax for statements related to these objects, and about object processing:

• For each object type, there are CREATE, ALTER, and DROP statements that control which objects

exist and how they are defined. See Section 15.1, “Data Definition Statements”.

• The CALL statement is used to invoke stored procedures. See Section 15.2.1, “CALL Statement”.

• Stored program definitions include a body that may use compound statements, loops, conditionals,

and declared variables. See Section 15.6, “Compound Statement Syntax”.

• Metadata changes to objects referred to by stored programs are detected and cause automatic

reparsing of the affected statements when the program is next executed. For more information, see
Section 10.10.3, “Caching of Prepared Statements and Stored Programs”.

27.1 Defining Stored Programs

Each stored program contains a body that consists of an SQL statement. This statement may be a
compound statement made up of several statements separated by semicolon (;) characters. For
example, the following stored procedure has a body made up of a BEGIN ... END block that contains
a SET statement and a REPEAT loop that itself contains another SET statement:

CREATE PROCEDURE dorepeat(p1 INT)
BEGIN
  SET @x = 0;
  REPEAT SET @x = @x + 1; UNTIL @x > p1 END REPEAT;
END;

If you use the mysql client program to define a stored program containing semicolon characters, a
problem arises. By default, mysql itself recognizes the semicolon as a statement delimiter, so you
must redefine the delimiter temporarily to cause mysql to pass the entire stored program definition to
the server.

To redefine the mysql delimiter, use the delimiter command. The following example shows how to
do this for the dorepeat() procedure just shown. The delimiter is changed to // to enable the entire
definition to be passed to the server as a single statement, and then restored to ; before invoking the
procedure. This enables the ; delimiter used in the procedure body to be passed through to the server
rather than being interpreted by mysql itself.

mysql> delimiter //

mysql> CREATE PROCEDURE dorepeat(p1 INT)
    -> BEGIN
    ->   SET @x = 0;
    ->   REPEAT SET @x = @x + 1; UNTIL @x > p1 END REPEAT;
    -> END
    -> //
Query OK, 0 rows affected (0.00 sec)

mysql> delimiter ;

mysql> CALL dorepeat(1000);
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @x;
+------+
| @x   |
+------+
| 1001 |
+------+
1 row in set (0.00 sec)

You can redefine the delimiter to a string other than //, and the delimiter can consist of a single
character or multiple characters. You should avoid the use of the backslash (\) character because that
is the escape character for MySQL.

4586

Trigger Syntax and Examples

CREATE TABLE test4(
  a4 INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  b4 INT DEFAULT 0
);

delimiter |

CREATE TRIGGER testref BEFORE INSERT ON test1
  FOR EACH ROW
  BEGIN
    INSERT INTO test2 SET a2 = NEW.a1;
    DELETE FROM test3 WHERE a3 = NEW.a1;
    UPDATE test4 SET b4 = b4 + 1 WHERE a4 = NEW.a1;
  END;
|

delimiter ;

INSERT INTO test3 (a3) VALUES
  (NULL), (NULL), (NULL), (NULL), (NULL),
  (NULL), (NULL), (NULL), (NULL), (NULL);

INSERT INTO test4 (a4) VALUES
  (0), (0), (0), (0), (0), (0), (0), (0), (0), (0);

Suppose that you insert the following values into table test1 as shown here:

mysql> INSERT INTO test1 VALUES
       (1), (3), (1), (7), (1), (8), (4), (4);
Query OK, 8 rows affected (0.01 sec)
Records: 8  Duplicates: 0  Warnings: 0

As a result, the four tables contain the following data:

mysql> SELECT * FROM test1;
+------+
| a1   |
+------+
|    1 |
|    3 |
|    1 |
|    7 |
|    1 |
|    8 |
|    4 |
|    4 |
+------+
8 rows in set (0.00 sec)

mysql> SELECT * FROM test2;
+------+
| a2   |
+------+
|    1 |
|    3 |
|    1 |
|    7 |
|    1 |
|    8 |
|    4 |
|    4 |
+------+
8 rows in set (0.00 sec)

mysql> SELECT * FROM test3;
+----+
| a3 |
+----+
|  2 |
|  5 |
|  6 |
|  9 |

4593

Event Scheduler Configuration

seen by users having the PROCESS privilege in the output of SHOW PROCESSLIST, as shown in the
discussion that follows.

The global event_scheduler system variable determines whether the Event Scheduler is enabled
and running on the server. It has one of the following values, which affect event scheduling as
described:

• ON: The Event Scheduler is started; the event scheduler thread runs and executes all scheduled

events. ON is the default event_scheduler value.

When the Event Scheduler is ON, the event scheduler thread is listed in the output of SHOW
PROCESSLIST as a daemon process, and its state is represented as shown here:

mysql> SHOW PROCESSLIST\G
*************************** 1. row ***************************
     Id: 1
   User: root
   Host: localhost
     db: NULL
Command: Query
   Time: 0
  State: NULL
   Info: show processlist
*************************** 2. row ***************************
     Id: 2
   User: event_scheduler
   Host: localhost
     db: NULL
Command: Daemon
   Time: 3
  State: Waiting for next activation
   Info: NULL
2 rows in set (0.00 sec)

Event scheduling can be stopped by setting the value of event_scheduler to OFF.

• OFF: The Event Scheduler is stopped. The event scheduler thread does not run, is not shown in the

output of SHOW PROCESSLIST, and no scheduled events execute.

When the Event Scheduler is stopped (event_scheduler is OFF), it can be started by setting the
value of event_scheduler to ON. (See next item.)

• DISABLED: This value renders the Event Scheduler nonoperational. When the Event Scheduler is

DISABLED, the event scheduler thread does not run (and so does not appear in the output of SHOW
PROCESSLIST). In addition, the Event Scheduler state cannot be changed at runtime.

If the Event Scheduler status has not been set to DISABLED, event_scheduler can be toggled
between ON and OFF (using SET). It is also possible to use 0 for OFF, and 1 for ON when setting this
variable. Thus, any of the following 4 statements can be used in the mysql client to turn on the Event
Scheduler:

SET GLOBAL event_scheduler = ON;
SET @@GLOBAL.event_scheduler = ON;
SET GLOBAL event_scheduler = 1;
SET @@GLOBAL.event_scheduler = 1;

Similarly, any of these 4 statements can be used to turn off the Event Scheduler:

SET GLOBAL event_scheduler = OFF;
SET @@GLOBAL.event_scheduler = OFF;
SET GLOBAL event_scheduler = 0;
SET @@GLOBAL.event_scheduler = 0;

Note

If the Event Scheduler is enabled, enabling the super_read_only system
variable prevents it from updating event “last executed” timestamps in the

4596

Event Scheduler Status

27.4.5 Event Scheduler Status

The Event Scheduler writes information about event execution that terminates with an error or warning
to the MySQL Server's error log. See Section 27.4.6, “The Event Scheduler and MySQL Privileges” for
an example.

To obtain information about the state of the Event Scheduler for debugging and troubleshooting
purposes, run mysqladmin debug (see Section 6.5.2, “mysqladmin — A MySQL Server
Administration Program”); after running this command, the server's error log contains output relating to
the Event Scheduler, similar to what is shown here:

Events status:
LLA = Last Locked At  LUA = Last Unlocked At
WOC = Waiting On Condition  DL = Data Locked

Event scheduler status:
State      : INITIALIZED
Thread id  : 0
LLA        : n/a:0
LUA        : n/a:0
WOC        : NO
Workers    : 0
Executed   : 0
Data locked: NO

Event queue status:
Element count   : 0
Data locked     : NO
Attempting lock : NO
LLA             : init_queue:95
LUA             : init_queue:103
WOC             : NO
Next activation : never

In statements that occur as part of events executed by the Event Scheduler, diagnostics messages
(not only errors, but also warnings) are written to the error log, and, on Windows, to the application
event log. For frequently executed events, it is possible for this to result in many logged messages.
For example, for SELECT ... INTO var_list statements, if the query returns no rows, a warning
with error code 1329 occurs (No data), and the variable values remain unchanged. If the query
returns multiple rows, error 1172 occurs (Result consisted of more than one row). For
either condition, you can avoid having the warnings be logged by declaring a condition handler; see
Section 15.6.7.2, “DECLARE ... HANDLER Statement”. For statements that may retrieve multiple rows,
another strategy is to use LIMIT 1 to limit the result set to a single row.

27.4.6 The Event Scheduler and MySQL Privileges

To enable or disable the execution of scheduled events, it is necessary to set the value of the global
event_scheduler system variable. This requires privileges sufficient to set global system variables.
See Section 7.1.9.1, “System Variable Privileges”.

The EVENT privilege governs the creation, modification, and deletion of events. This privilege can
be bestowed using GRANT. For example, this GRANT statement confers the EVENT privilege for the
schema named myschema on the user jon@ghidora:

GRANT EVENT ON myschema.* TO jon@ghidora;

(We assume that this user account already exists, and that we wish for it to remain unchanged
otherwise.)

To grant this same user the EVENT privilege on all schemas, use the following statement:

GRANT EVENT ON *.* TO jon@ghidora;

The EVENT privilege has global or schema-level scope. Therefore, trying to grant it on a single table
results in an error as shown:

4599

The Event Scheduler and MySQL Privileges

mysql> GRANT EVENT ON myschema.mytable TO jon@ghidora;
ERROR 1144 (42000): Illegal GRANT/REVOKE command; please
consult the manual to see which privileges can be used

It is important to understand that an event is executed with the privileges of its definer, and that it
cannot perform any actions for which its definer does not have the requisite privileges. For example,
suppose that jon@ghidora has the EVENT privilege for myschema. Suppose also that this user
has the SELECT privilege for myschema, but no other privileges for this schema. It is possible for
jon@ghidora to create a new event such as this one:

CREATE EVENT e_store_ts
    ON SCHEDULE
      EVERY 10 SECOND
    DO
      INSERT INTO myschema.mytable VALUES (UNIX_TIMESTAMP());

The user waits for a minute or so, and then performs a SELECT * FROM mytable; query, expecting
to see several new rows in the table. Instead, the table is empty. Since the user does not have the
INSERT privilege for the table in question, the event has no effect.

If you inspect the MySQL error log (hostname.err), you can see that the event is executing, but the
action it is attempting to perform fails:

2013-09-24T12:41:31.261992Z 25 [ERROR] Event Scheduler:
[jon@ghidora][cookbook.e_store_ts] INSERT command denied to user
'jon'@'ghidora' for table 'mytable'
2013-09-24T12:41:31.262022Z 25 [Note] Event Scheduler:
[jon@ghidora].[myschema.e_store_ts] event execution failed.
2013-09-24T12:41:41.271796Z 26 [ERROR] Event Scheduler:
[jon@ghidora][cookbook.e_store_ts] INSERT command denied to user
'jon'@'ghidora' for table 'mytable'
2013-09-24T12:41:41.272761Z 26 [Note] Event Scheduler:
[jon@ghidora].[myschema.e_store_ts] event execution failed.

Since this user very likely does not have access to the error log, it is possible to verify whether the
event's action statement is valid by executing it directly:

mysql> INSERT INTO myschema.mytable VALUES (UNIX_TIMESTAMP());
ERROR 1142 (42000): INSERT command denied to user
'jon'@'ghidora' for table 'mytable'

Inspection of the Information Schema EVENTS table shows that e_store_ts exists and is enabled,
but its LAST_EXECUTED column is NULL:

mysql> SELECT * FROM INFORMATION_SCHEMA.EVENTS
     >     WHERE EVENT_NAME='e_store_ts'
     >     AND EVENT_SCHEMA='myschema'\G
*************************** 1. row ***************************
   EVENT_CATALOG: NULL
    EVENT_SCHEMA: myschema
      EVENT_NAME: e_store_ts
         DEFINER: jon@ghidora
      EVENT_BODY: SQL
EVENT_DEFINITION: INSERT INTO myschema.mytable VALUES (UNIX_TIMESTAMP())
      EVENT_TYPE: RECURRING
      EXECUTE_AT: NULL
  INTERVAL_VALUE: 5
  INTERVAL_FIELD: SECOND
        SQL_MODE: NULL
          STARTS: 0000-00-00 00:00:00
            ENDS: 0000-00-00 00:00:00
          STATUS: ENABLED
   ON_COMPLETION: NOT PRESERVE
         CREATED: 2006-02-09 22:36:06
    LAST_ALTERED: 2006-02-09 22:36:06
   LAST_EXECUTED: NULL
   EVENT_COMMENT:
1 row in set (0.00 sec)

4600

Using Views

27.5 Using Views

MySQL supports views, including updatable views. Views are stored queries that when invoked
produce a result set. A view acts as a virtual table.

The following discussion describes the syntax for creating and dropping views, and shows some
examples of how to use them.

Additional Resources

• You may find the MySQL User Forums helpful when working with views.

• For answers to some commonly asked questions regarding views in MySQL, see Section A.6,

“MySQL 8.4 FAQ: Views”.

• There are some restrictions on the use of views; see Section 27.9, “Restrictions on Views”.

27.5.1 View Syntax

The CREATE VIEW statement creates a new view (see Section 15.1.23, “CREATE VIEW Statement”).
To alter the definition of a view or drop a view, use ALTER VIEW (see Section 15.1.11, “ALTER VIEW
Statement”), or DROP VIEW (see Section 15.1.35, “DROP VIEW Statement”).

A view can be created from many kinds of SELECT statements. It can refer to base tables or other
views. It can use joins, UNION, and subqueries. The SELECT need not even refer to any tables. The
following example defines a view that selects two columns from another table, as well as an expression
calculated from those columns:

mysql> CREATE TABLE t (qty INT, price INT);
mysql> INSERT INTO t VALUES(3, 50), (5, 60);
mysql> CREATE VIEW v AS SELECT qty, price, qty*price AS value FROM t;
mysql> SELECT * FROM v;
+------+-------+-------+
| qty  | price | value |
+------+-------+-------+
|    3 |    50 |   150 |
|    5 |    60 |   300 |
+------+-------+-------+
mysql> SELECT * FROM v WHERE qty = 5;
+------+-------+-------+
| qty  | price | value |
+------+-------+-------+
|    5 |    60 |   300 |
+------+-------+-------+

27.5.2 View Processing Algorithms

The optional ALGORITHM clause for CREATE VIEW or ALTER VIEW is a MySQL extension to standard
SQL. It affects how MySQL processes the view. ALGORITHM takes three values: MERGE, TEMPTABLE,
or UNDEFINED.

• For MERGE, the text of a statement that refers to the view and the view definition are merged such

that parts of the view definition replace corresponding parts of the statement.

• For TEMPTABLE, the results from the view are retrieved into a temporary table, which then is used to

execute the statement.

• For UNDEFINED, MySQL chooses which algorithm to use. It prefers MERGE over TEMPTABLE if
possible, because MERGE is usually more efficient and because a view cannot be updated if a
temporary table is used.

• If no ALGORITHM clause is present, the default algorithm is determined by the value of the

derived_merge flag of the optimizer_switch system variable. For additional discussion, see

4602

Updatable and Insertable Views

Section 10.2.2.4, “Optimizing Derived Tables, View References, and Common Table Expressions
with Merging or Materialization”.

A reason to specify TEMPTABLE explicitly is that locks can be released on underlying tables after the
temporary table has been created and before it is used to finish processing the statement. This might
result in quicker lock release than the MERGE algorithm so that other clients that use the view are not
blocked as long.

A view algorithm can be UNDEFINED for three reasons:

• No ALGORITHM clause is present in the CREATE VIEW statement.

• The CREATE VIEW statement has an explicit ALGORITHM = UNDEFINED clause.

• ALGORITHM = MERGE is specified for a view that can be processed only with a temporary table. In

this case, MySQL generates a warning and sets the algorithm to UNDEFINED.

As mentioned earlier, MERGE is handled by merging corresponding parts of a view definition into the
statement that refers to the view. The following examples briefly illustrate how the MERGE algorithm
works. The examples assume that there is a view v_merge that has this definition:

CREATE ALGORITHM = MERGE VIEW v_merge (vc1, vc2) AS
SELECT c1, c2 FROM t WHERE c3 > 100;

Example 1: Suppose that we issue this statement:

SELECT * FROM v_merge;

MySQL handles the statement as follows:

• v_merge becomes t

• * becomes vc1, vc2, which corresponds to c1, c2

• The view WHERE clause is added

The resulting statement to be executed becomes:

SELECT c1, c2 FROM t WHERE c3 > 100;

Example 2: Suppose that we issue this statement:

SELECT * FROM v_merge WHERE vc1 < 100;

This statement is handled similarly to the previous one, except that vc1 < 100 becomes c1 < 100
and the view WHERE clause is added to the statement WHERE clause using an AND connective (and
parentheses are added to make sure the parts of the clause are executed with correct precedence).
The resulting statement to be executed becomes:

SELECT c1, c2 FROM t WHERE (c3 > 100) AND (c1 < 100);

Effectively, the statement to be executed has a WHERE clause of this form:

WHERE (select WHERE) AND (view WHERE)

If the MERGE algorithm cannot be used, a temporary table must be used instead. Constructs
that prevent merging are the same as those that prevent merging in derived tables and common
table expressions. Examples are SELECT DISTINCT or LIMIT in the subquery. For details, see
Section 10.2.2.4, “Optimizing Derived Tables, View References, and Common Table Expressions with
Merging or Materialization”.

27.5.3 Updatable and Insertable Views

Some views are updatable and references to them can be used to specify tables to be updated in data
change statements. That is, you can use them in statements such as UPDATE, DELETE, or INSERT to
update the contents of the underlying table. Derived tables and common table expressions can also be

4603

Updatable and Insertable Views

specified in multiple-table UPDATE and DELETE statements, but can only be used for reading data to
specify rows to be updated or deleted. Generally, the view references must be updatable, meaning that
they may be merged and not materialized. Composite views have more complex rules.

For a view to be updatable, there must be a one-to-one relationship between the rows in the view
and the rows in the underlying table. There are also certain other constructs that make a view
nonupdatable. To be more specific, a view is not updatable if it contains any of the following:

• Aggregate functions or window functions (SUM(), MIN(), MAX(), COUNT(), and so forth)

• DISTINCT

• GROUP BY

• HAVING

• UNION or UNION ALL

• Subquery in the select list

Nondependent subqueries in the select list fail for INSERT, but are okay for UPDATE, DELETE. For
dependent subqueries in the select list, no data change statements are permitted.

• Certain joins (see additional join discussion later in this section)

• Reference to nonupdatable view in the FROM clause

• Subquery in the WHERE clause that refers to a table in the FROM clause

• Refers only to literal values (in this case, there is no underlying table to update)

• ALGORITHM = TEMPTABLE (use of a temporary table always makes a view nonupdatable)

• Multiple references to any column of a base table (fails for INSERT, okay for UPDATE, DELETE)

A generated column in a view is considered updatable because it is possible to assign to it. However,
if such a column is updated explicitly, the only permitted value is DEFAULT. For information about
generated columns, see Section 15.1.20.8, “CREATE TABLE and Generated Columns”.

It is sometimes possible for a multiple-table view to be updatable, assuming that it can be processed
with the MERGE algorithm. For this to work, the view must use an inner join (not an outer join or a
UNION). Also, only a single table in the view definition can be updated, so the SET clause must name
only columns from one of the tables in the view. Views that use UNION ALL are not permitted even
though they might be theoretically updatable.

With respect to insertability (being updatable with INSERT statements), an updatable view is insertable
if it also satisfies these additional requirements for the view columns:

• There must be no duplicate view column names.

• The view must contain all columns in the base table that do not have a default value.

• The view columns must be simple column references. They must not be expressions, such as these:

3.14159
col1 + 3
UPPER(col2)
col3 / col4
(subquery)

MySQL sets a flag, called the view updatability flag, at CREATE VIEW time. The flag is set to YES (true)
if UPDATE and DELETE (and similar operations) are legal for the view. Otherwise, the flag is set to NO
(false). The IS_UPDATABLE column in the Information Schema VIEWS table displays the status of this
flag. It means that the server always knows whether a view is updatable.

4604

Updatable and Insertable Views

If a view is not updatable, statements such UPDATE, DELETE, and INSERT are illegal and are rejected.
(Even if a view is updatable, it might not be possible to insert into it, as described elsewhere in this
section.)

The updatability of views may be affected by the value of the updatable_views_with_limit
system variable. See Section 7.1.8, “Server System Variables”.

For the following discussion, suppose that these tables and views exist:

CREATE TABLE t1 (x INTEGER);
CREATE TABLE t2 (c INTEGER);
CREATE VIEW vmat AS SELECT SUM(x) AS s FROM t1;
CREATE VIEW vup AS SELECT * FROM t2;
CREATE VIEW vjoin AS SELECT * FROM vmat JOIN vup ON vmat.s=vup.c;

INSERT, UPDATE, and DELETE statements are permitted as follows:

• INSERT: The insert table of an INSERT statement may be a view reference that is merged. If the

view is a join view, all components of the view must be updatable (not materialized). For a multiple-
table updatable view, INSERT can work if it inserts into a single table.

This statement is invalid because one component of the join view is nonupdatable:

INSERT INTO vjoin (c) VALUES (1);

This statement is valid; the view contains no materialized components:

INSERT INTO vup (c) VALUES (1);

• UPDATE: The table or tables to be updated in an UPDATE statement may be view references that are
merged. If a view is a join view, at least one component of the view must be updatable (this differs
from INSERT).

In a multiple-table UPDATE statement, the updated table references of the statement must be base
tables or updatable view references. Nonupdated table references may be materialized views or
derived tables.

This statement is valid; column c is from the updatable part of the join view:

UPDATE vjoin SET c=c+1;

This statement is invalid; column x is from the nonupdatable part:

UPDATE vjoin SET x=x+1;

This statement is valid; the updated table reference of the multiple-table UPDATE is an updatable
view (vup):

UPDATE vup JOIN (SELECT SUM(x) AS s FROM t1) AS dt ON ...
SET c=c+1;

This statement is invalid; it tries to update a materialized derived table:

UPDATE vup JOIN (SELECT SUM(x) AS s FROM t1) AS dt ON ...
SET s=s+1;

• DELETE: The table or tables to be deleted from in a DELETE statement must be merged views. Join

views are not allowed (this differs from INSERT and UPDATE).

This statement is invalid because the view is a join view:

DELETE vjoin WHERE ...;

This statement is valid because the view is a merged (updatable) view:

DELETE vup WHERE ...;

4605

The View WITH CHECK OPTION Clause

This statement is valid because it deletes from a merged (updatable) view:

DELETE vup FROM vup JOIN (SELECT SUM(x) AS s FROM t1) AS dt ON ...;

Additional discussion and examples follow.

Earlier discussion in this section pointed out that a view is not insertable if not all columns are simple
column references (for example, if it contains columns that are expressions or composite expressions).
Although such a view is not insertable, it can be updatable if you update only columns that are not
expressions. Consider this view:

CREATE VIEW v AS SELECT col1, 1 AS col2 FROM t;

This view is not insertable because col2 is an expression. But it is updatable if the update does not try
to update col2. This update is permissible:

UPDATE v SET col1 = 0;

This update is not permissible because it attempts to update an expression column:

UPDATE v SET col2 = 0;

If a table contains an AUTO_INCREMENT column, inserting into an insertable view on the table that
does not include the AUTO_INCREMENT column does not change the value of LAST_INSERT_ID(),
because the side effects of inserting default values into columns not part of the view should not be
visible.

27.5.4 The View WITH CHECK OPTION Clause

The WITH CHECK OPTION clause can be given for an updatable view to prevent inserts to rows for
which the WHERE clause in the select_statement is not true. It also prevents updates to rows for
which the WHERE clause is true but the update would cause it to be not true (in other words, it prevents
visible rows from being updated to nonvisible rows).

In a WITH CHECK OPTION clause for an updatable view, the LOCAL and CASCADED keywords
determine the scope of check testing when the view is defined in terms of another view. When neither
keyword is given, the default is CASCADED.

WITH CHECK OPTION testing is standard-compliant:

• With LOCAL, the view WHERE clause is checked, then checking recurses to underlying views and

applies the same rules.

• With CASCADED, the view WHERE clause is checked, then checking recurses to underlying views,

adds WITH CASCADED CHECK OPTION to them (for purposes of the check; their definitions remain
unchanged), and applies the same rules.

• With no check option, the view WHERE clause is not checked, then checking recurses to underlying

views, and applies the same rules.

Consider the definitions for the following table and set of views:

CREATE TABLE t1 (a INT);
CREATE VIEW v1 AS SELECT * FROM t1 WHERE a < 2
WITH CHECK OPTION;
CREATE VIEW v2 AS SELECT * FROM v1 WHERE a > 0
WITH LOCAL CHECK OPTION;
CREATE VIEW v3 AS SELECT * FROM v1 WHERE a > 0
WITH CASCADED CHECK OPTION;

Here the v2 and v3 views are defined in terms of another view, v1.

Inserts for v2 are checked against its LOCAL check option, then the check recurses to v1 and the rules
are applied again. The rules for v1 cause a check failure. The check for v3 also fails:

4606

View Metadata

mysql> INSERT INTO v2 VALUES (2);
ERROR 1369 (HY000): CHECK OPTION failed 'test.v2'
mysql> INSERT INTO v3 VALUES (2);
ERROR 1369 (HY000): CHECK OPTION failed 'test.v3'

27.5.5 View Metadata

To obtain metadata about views:

• Query the VIEWS table of the INFORMATION_SCHEMA database. See Section 28.3.47, “The

INFORMATION_SCHEMA VIEWS Table”.

• Use the SHOW CREATE VIEW statement. See Section 15.7.7.14, “SHOW CREATE VIEW

Statement”.

27.6 Stored Object Access Control

Stored programs (procedures, functions, triggers, and events) and views are defined prior to use and,
when referenced, execute within a security context that determines their privileges. The privileges
applicable to execution of a stored object are controlled by its DEFINER attribute and SQL SECURITY
characteristic.

• The DEFINER Attribute

• The SQL SECURITY Characteristic

• Examples

• Orphan Stored Objects

• Risk-Minimization Guidelines

The DEFINER Attribute

A stored object definition can include a DEFINER attribute that names a MySQL account. If a definition
omits the DEFINER attribute, the default object definer is the user who creates it.

The following rules determine which accounts you can specify as the DEFINER attribute for a stored
object:

• If you have the SET_ANY_DEFINER privilege, you can specify any account as the DEFINER attribute.
If the account does not exist, a warning is generated. Additionally, to set a stored object DEFINER
attribute to an account that has the SYSTEM_USER privilege, you must have the SYSTEM_USER
privilege.

• Otherwise, the only permitted account is your own, specified either literally or as CURRENT_USER or

CURRENT_USER(). You cannot set the definer to any other account.

Creating a stored object with a nonexistent DEFINER account creates an orphan object, which may
have negative consequences; see Orphan Stored Objects.

The SQL SECURITY Characteristic

For stored routines (procedures and functions) and views, the object definition can include an SQL
SECURITY characteristic with a value of DEFINER or INVOKER to specify whether the object executes
in definer or invoker context. If the definition omits the SQL SECURITY characteristic, the default is
definer context.

Triggers and events have no SQL SECURITY characteristic and always execute in definer context. The
server invokes these objects automatically as necessary, so there is no invoking user.

Definer and invoker security contexts differ as follows:

4607

Examples

• A stored object that executes in definer security context executes with the privileges of the account

named by its DEFINER attribute. These privileges may be entirely different from those of the invoking
user. The invoker must have appropriate privileges to reference the object (for example, EXECUTE to
call a stored procedure or SELECT to select from a view), but during object execution, the invoker's
privileges are ignored and only the DEFINER account privileges matter. If the DEFINER account has
few privileges, the object is correspondingly limited in the operations it can perform. If the DEFINER
account is highly privileged (such as an administrative account), the object can perform powerful
operations no matter who invokes it.

• A stored routine or view that executes in invoker security context can perform only operations for

which the invoker has privileges. The DEFINER attribute has no effect on object execution.

Examples

Consider the following stored procedure, which is declared with SQL SECURITY DEFINER to execute
in definer security context:

CREATE DEFINER = 'admin'@'localhost' PROCEDURE p1()
SQL SECURITY DEFINER
BEGIN
  UPDATE t1 SET counter = counter + 1;
END;

Any user who has the EXECUTE privilege for p1 can invoke it with a CALL statement. However,
when p1 executes, it does so in definer security context and thus executes with the privileges of
'admin'@'localhost', the account named as its DEFINER attribute. This account must have the
EXECUTE privilege for p1 as well as the UPDATE privilege for the table t1 referenced within the object
body. Otherwise, the procedure fails.

Now consider this stored procedure, which is identical to p1 except that its SQL SECURITY
characteristic is INVOKER:

CREATE DEFINER = 'admin'@'localhost' PROCEDURE p2()
SQL SECURITY INVOKER
BEGIN
  UPDATE t1 SET counter = counter + 1;
END;

Unlike p1, p2 executes in invoker security context and thus with the privileges of the invoking user
regardless of the DEFINER attribute value. p2 fails if the invoker lacks the EXECUTE privilege for p2 or
the UPDATE privilege for the table t1.

Orphan Stored Objects

An orphan stored object is one for which its DEFINER attribute names a nonexistent account:

• An orphan stored object can be created by specifying a nonexistent DEFINER account at object-

creation time.

• An existing stored object can become orphaned through execution of a DROP USER statement that

drops the object DEFINER account, or a RENAME USER statement that renames the object DEFINER
account.

An orphan stored object may be problematic in these ways:

• Because the DEFINER account does not exist, the object may not work as expected if it executes in

definer security context:

• For a stored routine, an error occurs at routine execution time if the SQL SECURITY value is

DEFINER but the definer account does not exist.

• For a trigger, it is not a good idea for trigger activation to occur until the account actually does

exist. Otherwise, the behavior with respect to privilege checking is undefined.

4608

Orphan Stored Objects

• For an event, an error occurs at event execution time if the account does not exist.

• For a view, an error occurs when the view is referenced if the SQL SECURITY value is DEFINER

but the definer account does not exist.

• The object may present a security risk if the nonexistent DEFINER account is subsequently re-

created for a purpose unrelated to the object. In this case, the account “adopts” the object and, with
the appropriate privileges, is able to execute it even if that is not intended.

The server imposes the following account-management security checks designed to prevent operations
that (perhaps inadvertently) cause stored objects to become orphaned or that cause adoption of stored
objects that are currently orphaned:

• DROP USER fails with an error if any account to be dropped is named as the DEFINER attribute for

any stored object. (That is, the statement fails if dropping an account would cause a stored object to
become orphaned.)

• RENAME USER fails with an error if any account to be renamed is named as the DEFINER attribute

for any stored object. (That is, the statement fails if renaming an account would cause a stored object
to become orphaned.)

• CREATE USER fails with an error if any account to be created is named as the DEFINER attribute

for any stored object. (That is, the statement fails if creating an account would cause the account to
adopt a currently orphaned stored object.)

In certain situations, it may be necessary to deliberately execute those account-management
statements even when they would otherwise fail. To make this possible, if a user has the
ALLOW_NONEXISTENT_DEFINER privilege, that privilege overrides the orphan object security checks
and the statements succeed with a warning rather than failing with an error.

To obtain information about the accounts used as stored object definers in a MySQL installation, query
the INFORMATION_SCHEMA.

This query identifies which INFORMATION_SCHEMA tables describe objects that have a DEFINER
attribute:

mysql> SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS
       WHERE COLUMN_NAME = 'DEFINER';
+--------------------+------------+
| TABLE_SCHEMA       | TABLE_NAME |
+--------------------+------------+
| information_schema | EVENTS     |
| information_schema | ROUTINES   |
| information_schema | TRIGGERS   |
| information_schema | VIEWS      |
+--------------------+------------+

The result tells you which tables to query to discover which stored object DEFINER values exist and
which objects have a particular DEFINER value:

• To identify which DEFINER values exist in each table, use these queries:

SELECT DISTINCT DEFINER FROM INFORMATION_SCHEMA.EVENTS;
SELECT DISTINCT DEFINER FROM INFORMATION_SCHEMA.ROUTINES;
SELECT DISTINCT DEFINER FROM INFORMATION_SCHEMA.TRIGGERS;
SELECT DISTINCT DEFINER FROM INFORMATION_SCHEMA.VIEWS;

The query results are significant for any account displayed as follows:

• If the account exists, dropping or renaming it causes stored objects to become orphaned. If

you plan to drop or rename the account, consider first dropping its associated stored objects or
redefining them to have a different definer.

4609

Risk-Minimization Guidelines

• If the account does not exist, creating it causes it to adopt currently orphaned stored objects. If you
plan to create the account, consider whether the orphaned objects should be associated with it. If
not, redefine them to have a different definer.

To redefine an object with a different definer, you can use ALTER EVENT or ALTER VIEW to directly
modify the DEFINER account of events and views. For stored procedures and functions and for
triggers, you must drop the object and re-create it to assign a different DEFINER account

• To identify which objects have a given DEFINER account, use these queries, substituting the account

of interest for user_name@host_name:

SELECT EVENT_SCHEMA, EVENT_NAME FROM INFORMATION_SCHEMA.EVENTS
WHERE DEFINER = 'user_name@host_name';
SELECT ROUTINE_SCHEMA, ROUTINE_NAME, ROUTINE_TYPE
FROM INFORMATION_SCHEMA.ROUTINES
WHERE DEFINER = 'user_name@host_name';
SELECT TRIGGER_SCHEMA, TRIGGER_NAME FROM INFORMATION_SCHEMA.TRIGGERS
WHERE DEFINER = 'user_name@host_name';
SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS
WHERE DEFINER = 'user_name@host_name';

For the ROUTINES table, the query includes the ROUTINE_TYPE column so that output rows
distinguish whether the DEFINER is for a stored procedure or stored function.

If the account you are searching for does not exist, any objects displayed by those queries are
orphan objects.

Risk-Minimization Guidelines

To minimize the risk potential for stored object creation and use, follow these guidelines:

• Do not create orphan stored objects; that is, objects for which the DEFINER attribute names a

nonexistent account. Do not cause stored objects to become orphaned by dropping or renaming an
account named by the DEFINER attribute of any existing object.

• For a stored routine or view, use SQL SECURITY INVOKER in the object definition when possible so
that it can be used only by users with permissions appropriate for the operations performed by the
object.

• If you create definer-context stored objects while using an account that has the SET_ANY_DEFINER
privilege, specify an explicit DEFINER attribute that names an account possessing only the privileges
required for the operations performed by the object. Specify a highly privileged DEFINER account
only when absolutely necessary.

• Administrators can prevent users from creating stored objects that specify highly privileged DEFINER

accounts by not granting them the SET_ANY_DEFINER privilege.

• Definer-context objects should be written keeping in mind that they may be able to access data

for which the invoking user has no privileges. In some cases, you can prevent references to these
objects by not granting unauthorized users particular privileges:

• A stored routine cannot be referenced by a user who does not have the EXECUTE privilege for it.

• A view cannot be referenced by a user who does not have the appropriate privilege for it (SELECT

to select from it, INSERT to insert into it, and so forth).

However, no such control exists for triggers and events because they always execute in definer
context. The server invokes these objects automatically as necessary, and users do not reference
them directly:

• A trigger is activated by access to the table with which it is associated, even ordinary table

accesses by users with no special privileges.

4610

Stored Program Binary Logging

• An event is executed by the server on a scheduled basis.

In both cases, if the DEFINER account is highly privileged, the object may be able to perform
sensitive or dangerous operations. This remains true if the privileges needed to create the object
are revoked from the account of the user who created it. Administrators should be especially careful
about granting users object-creation privileges.

• By default, when a routine with the SQL SECURITY DEFINER characteristic is executed, MySQL

Server does not set any active roles for the MySQL account named in the DEFINER clause, only the
default roles. The exception is if the activate_all_roles_on_login system variable is enabled,
in which case MySQL Server sets all roles granted to the DEFINER user, including mandatory
roles. Any privileges granted through roles are therefore not checked by default when the CREATE
PROCEDURE or CREATE FUNCTION statement is issued. For stored programs, if execution should
occur with roles different from the default, the program body can execute SET ROLE to activate
the required roles. This must be done with caution since the privileges assigned to roles can be
changed.

27.7 Stored Program Binary Logging

The binary log contains information about SQL statements that modify database contents. This
information is stored in the form of “events” that describe the modifications. (Binary log events differ
from scheduled event stored objects.) The binary log has two important purposes:

• For replication, the binary log is used on source replication servers as a record of the statements

to be sent to replica servers. The source sends the events contained in its binary log to its replicas,
which execute those events to make the same data changes that were made on the source. See
Section 19.2, “Replication Implementation”.

• Certain data recovery operations require use of the binary log. After a backup file has been restored,
the events in the binary log that were recorded after the backup was made are re-executed. These
events bring databases up to date from the point of the backup. See Section 9.3.2, “Using Backups
for Recovery”.

However, if logging occurs at the statement level, there are certain binary logging issues with respect to
stored programs (stored procedures and functions, triggers, and events):

• In some cases, a statement might affect different sets of rows on source and replica.

• Replicated statements executed on a replica are processed by the replica's applier thread. Unless

you implement replication privilege checks (see Section 19.3.3, “Replication Privilege Checks”), the
applier thread has full privileges. In this situation, it is possible for a procedure to follow different
execution paths on source and replica servers, so a user could write a routine containing a
dangerous statement that executes only on the replica.

• If a stored program that modifies data is nondeterministic, it is not repeatable. This can result in

different data on source and replica, or cause restored data to differ from the original data.

This section describes how MySQL handles binary logging for stored programs. It states the current
conditions that the implementation places on the use of stored programs, and what you can do to avoid
logging problems. It also provides additional information about the reasons for these conditions.

Unless noted otherwise, the remarks here assume that binary logging is enabled on the server (see
Section 7.4.4, “The Binary Log”.) If the binary log is not enabled, replication is not possible, nor is the
binary log available for data recovery. Binary logging is enabled by default, and is disabled only if you
start the server with --skip-log-bin or --disable-log-bin at startup.

In general, the issues described here result when binary logging occurs at the SQL statement level
(statement-based binary logging). If you use row-based binary logging, the log contains changes made
to individual rows as a result of executing SQL statements. When routines or triggers execute, row
changes are logged, not the statements that make the changes. For stored procedures, this means

4611

Stored Program Binary Logging

that the CALL statement is not logged. For stored functions, row changes made within the function are
logged, not the function invocation. For triggers, row changes made by the trigger are logged. On the
replica side, only the row changes are seen, not the stored program invocation.

Mixed format binary logging (binlog_format=MIXED) uses statement-based binary logging, except
for cases where only row-based binary logging is guaranteed to lead to proper results. With mixed
format, when a stored function, stored procedure, trigger, event, or prepared statement contains
anything that is not safe for statement-based binary logging, the entire statement is marked as unsafe
and logged in row format. The statements used to create and drop procedures, functions, triggers,
and events are always safe, and are logged in statement format. For more information about row-
based, mixed, and statement-based logging, and how safe and unsafe statements are determined, see
Section 19.2.1, “Replication Formats”.

The conditions on the use of stored functions in MySQL can be summarized as follows. These
conditions do not apply to stored procedures or Event Scheduler events and they do not apply unless
binary logging is enabled.

• To create or alter a stored function, you must have the SET_ANY_DEFINER privilege, in addition
to the CREATE ROUTINE or ALTER ROUTINE privilege that is normally required. (Depending on
the DEFINER value in the function definition, SET_ANY_DEFINER might be required regardless of
whether binary logging is enabled. See Section 15.1.17, “CREATE PROCEDURE and CREATE
FUNCTION Statements”.)

• When you create a stored function, you must declare either that it is deterministic or that it does not

modify data. Otherwise, it may be unsafe for data recovery or replication.

By default, for a CREATE FUNCTION statement to be accepted, at least one of DETERMINISTIC, NO
SQL, or READS SQL DATA must be specified explicitly. Otherwise an error occurs:

ERROR 1418 (HY000): This function has none of DETERMINISTIC, NO SQL,
or READS SQL DATA in its declaration and binary logging is enabled
(you *might* want to use the less safe log_bin_trust_function_creators
variable)

This function is deterministic (and does not modify data), so it is safe:

CREATE FUNCTION f1(i INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
  RETURN i;
END;

This function uses UUID(), which is not deterministic, so the function also is not deterministic and is
not safe:

CREATE FUNCTION f2()
RETURNS CHAR(36) CHARACTER SET utf8mb4
BEGIN
  RETURN UUID();
END;

This function modifies data, so it may not be safe:

CREATE FUNCTION f3(p_id INT)
RETURNS INT
BEGIN
  UPDATE t SET modtime = NOW() WHERE id = p_id;
  RETURN ROW_COUNT();
END;

Assessment of the nature of a function is based on the “honesty” of the creator. MySQL does not
check that a function declared DETERMINISTIC is free of statements that produce nondeterministic
results.

4612

Stored Program Binary Logging

• When you attempt to execute a stored function, if binlog_format=STATEMENT is set, the

DETERMINISTIC keyword must be specified in the function definition. If this is not the case, an error
is generated and the function does not run, unless log_bin_trust_function_creators=1
is specified to override this check (see below). For recursive function calls, the DETERMINISTIC
keyword is required on the outermost call only. If row-based or mixed binary logging is in use, the
statement is accepted and replicated even if the function was defined without the DETERMINISTIC
keyword.

• Because MySQL does not check if a function really is deterministic at creation time, the invocation
of a stored function with the DETERMINISTIC keyword might carry out an action that is unsafe for
statement-based logging, or invoke a function or procedure containing unsafe statements. If this
occurs when binlog_format=STATEMENT is set, a warning message is issued. If row-based or
mixed binary logging is in use, no warning is issued, and the statement is replicated in row-based
format.

• To relax the preceding conditions on function creation (that you must have the SUPER privilege

and that a function must be declared deterministic or to not modify data), set the global
log_bin_trust_function_creators system variable to 1. By default, this variable has a value
of 0, but you can change it like this:

mysql> SET GLOBAL log_bin_trust_function_creators = 1;

You can also set this variable at server startup.

If binary logging is not enabled, log_bin_trust_function_creators does not apply. SUPER is
not required for function creation unless, as described previously, the DEFINER value in the function
definition requires it.

• For information about built-in functions that may be unsafe for replication (and thus cause stored

functions that use them to be unsafe as well), see Section 19.5.1, “Replication Features and Issues”.

Triggers are similar to stored functions, so the preceding remarks regarding functions also apply to
triggers with the following exception: CREATE TRIGGER does not have an optional DETERMINISTIC
characteristic, so triggers are assumed to be always deterministic. However, this assumption might be
invalid in some cases. For example, the UUID() function is nondeterministic (and does not replicate).
Be careful about using such functions in triggers.

Triggers can update tables, so error messages similar to those for stored functions occur with CREATE
TRIGGER if you do not have the required privileges. On the replica side, the replica uses the trigger
DEFINER attribute to determine which user is considered to be the creator of the trigger.

The rest of this section provides additional detail about the logging implementation and its implications.
You need not read it unless you are interested in the background on the rationale for the current
logging-related conditions on stored routine use. This discussion applies only for statement-based
logging, and not for row-based logging, with the exception of the first item: CREATE and DROP
statements are logged as statements regardless of the logging mode.

• The server writes CREATE EVENT, CREATE PROCEDURE, CREATE FUNCTION, ALTER EVENT,

ALTER PROCEDURE, ALTER FUNCTION, DROP EVENT, DROP PROCEDURE, and DROP FUNCTION
statements to the binary log.

• A stored function invocation is logged as a SELECT statement if the function changes data and

occurs within a statement that would not otherwise be logged. This prevents nonreplication of data
changes that result from use of stored functions in nonlogged statements. For example, SELECT
statements are not written to the binary log, but a SELECT might invoke a stored function that makes
changes. To handle this, a SELECT func_name() statement is written to the binary log when the
given function makes a change. Suppose that the following statements are executed on the source
server:

CREATE FUNCTION f1(a INT) RETURNS INT
BEGIN

4613

Stored Program Binary Logging

  IF (a < 3) THEN
    INSERT INTO t2 VALUES (a);
  END IF;
  RETURN 0;
END;

CREATE TABLE t1 (a INT);
INSERT INTO t1 VALUES (1),(2),(3);

SELECT f1(a) FROM t1;

When the SELECT statement executes, the function f1() is invoked three times. Two of those
invocations insert a row, and MySQL logs a SELECT statement for each of them. That is, MySQL
writes the following statements to the binary log:

SELECT f1(1);
SELECT f1(2);

The server also logs a SELECT statement for a stored function invocation when the function invokes
a stored procedure that causes an error. In this case, the server writes the SELECT statement to the
log along with the expected error code. On the replica, if the same error occurs, that is the expected
result and replication continues. Otherwise, replication stops.

• Logging stored function invocations rather than the statements executed by a function has a security

implication for replication, which arises from two factors:

• It is possible for a function to follow different execution paths on source and replica servers.

• Statements executed on a replica are processed by the replica's applier thread. Unless you

implement replication privilege checks (see Section 19.3.3, “Replication Privilege Checks”), the
applier thread has full privileges.

The implication is that although a user must have the CREATE ROUTINE privilege to create a
function, the user can write a function containing a dangerous statement that executes only on the
replica where it is processed by a thread that has full privileges. For example, if the source and
replica servers have server ID values of 1 and 2, respectively, a user on the source server could
create and invoke an unsafe function unsafe_func() as follows:

mysql> delimiter //
mysql> CREATE FUNCTION unsafe_func () RETURNS INT
    -> BEGIN
    ->   IF @@server_id=2 THEN dangerous_statement; END IF;
    ->   RETURN 1;
    -> END;
    -> //
mysql> delimiter ;
mysql> INSERT INTO t VALUES(unsafe_func());

The CREATE FUNCTION and INSERT statements are written to the binary log, so the replica
executes them. Because the replica's applier thread has full privileges, it executes the dangerous
statement. Thus, the function invocation has different effects on the source and replica and is not
replication-safe.

To guard against this danger for servers that have binary logging enabled, stored function creators
must have the SUPER privilege, in addition to the usual CREATE ROUTINE privilege that is required.
Similarly, to use ALTER FUNCTION, you must have the SUPER privilege in addition to the ALTER
ROUTINE privilege. Without the SUPER privilege, an error occurs:

ERROR 1419 (HY000): You do not have the SUPER privilege and
binary logging is enabled (you *might* want to use the less safe
log_bin_trust_function_creators variable)

If you do not want to require function creators to have the SUPER privilege (for example, if all users
with the CREATE ROUTINE privilege on your system are experienced application developers), set
the global log_bin_trust_function_creators system variable to 1. You can also set this

4614

Stored Program Binary Logging

variable at server startup. If binary logging is not enabled, log_bin_trust_function_creators
does not apply. SUPER is not required for function creation unless, as described previously, the
DEFINER value in the function definition requires it.

• The use of replication privilege checks recommended regardless of any choices you make about
privileges for function creators. Replication privilege checks can be set up to ensure that only
expected and relevant operations are authorized for the replication channel. For instructions to do
this, see Section 19.3.3, “Replication Privilege Checks”.

• If a function that performs updates is nondeterministic, it is not repeatable. This can have two

undesirable effects:

• It causes a replica to differ from the source.

• Restored data does not match the original data.

To deal with these problems, MySQL enforces the following requirement: On a source server,
creation and alteration of a function is refused unless you declare the function to be deterministic or
to not modify data. Two sets of function characteristics apply here:

• The DETERMINISTIC and NOT DETERMINISTIC characteristics indicate whether a function
always produces the same result for given inputs. The default is NOT DETERMINISTIC if
neither characteristic is given. To declare that a function is deterministic, you must specify
DETERMINISTIC explicitly.

• The CONTAINS SQL, NO SQL, READS SQL DATA, and MODIFIES SQL DATA characteristics

provide information about whether the function reads or writes data. Either NO SQL or READS SQL
DATA indicates that a function does not change data, but you must specify one of these explicitly
because the default is CONTAINS SQL if no characteristic is given.

By default, for a CREATE FUNCTION statement to be accepted, at least one of DETERMINISTIC, NO
SQL, or READS SQL DATA must be specified explicitly. Otherwise an error occurs:

ERROR 1418 (HY000): This function has none of DETERMINISTIC, NO SQL,
or READS SQL DATA in its declaration and binary logging is enabled
(you *might* want to use the less safe log_bin_trust_function_creators
variable)

If you set log_bin_trust_function_creators to 1, the requirement that functions be
deterministic or not modify data is dropped.

• Stored procedure calls are logged at the statement level rather than at the CALL level. That is, the
server does not log the CALL statement, it logs those statements within the procedure that actually
execute. As a result, the same changes that occur on the source server also occur on replicas. This
prevents problems that could result from a procedure having different execution paths on different
machines.

In general, statements executed within a stored procedure are written to the binary log using the
same rules that would apply were the statements to be executed in standalone fashion. Some
special care is taken when logging procedure statements because statement execution within
procedures is not quite the same as in nonprocedure context:

•  A statement to be logged might contain references to local procedure variables. These variables
do not exist outside of stored procedure context, so a statement that refers to such a variable
cannot be logged literally. Instead, each reference to a local variable is replaced by this construct
for logging purposes:

NAME_CONST(var_name, var_value)

var_name is the local variable name, and var_value is a constant indicating the value that the
variable has at the time the statement is logged. NAME_CONST() has a value of var_value, and
a “name” of var_name. Thus, if you invoke this function directly, you get a result like this:

4615

Stored Program Binary Logging

mysql> SELECT NAME_CONST('myname', 14);
+--------+
| myname |
+--------+
|     14 |
+--------+

NAME_CONST() enables a logged standalone statement to be executed on a replica with the same
effect as the original statement that was executed on the source within a stored procedure.

The use of NAME_CONST() can result in a problem for CREATE TABLE ... SELECT statements
when the source column expressions refer to local variables. Converting these references to
NAME_CONST() expressions can result in column names that are different on the source and
replica servers, or names that are too long to be legal column identifiers. A workaround is to supply
aliases for columns that refer to local variables. Consider this statement when myvar has a value
of 1:

CREATE TABLE t1 SELECT myvar;

This is rewritten as follows:

CREATE TABLE t1 SELECT NAME_CONST(myvar, 1);

To ensure that the source and replica tables have the same column names, write the statement
like this:

CREATE TABLE t1 SELECT myvar AS myvar;

The rewritten statement becomes:

CREATE TABLE t1 SELECT NAME_CONST(myvar, 1) AS myvar;

• A statement to be logged might contain references to user-defined variables. To handle this,
MySQL writes a SET statement to the binary log to make sure that the variable exists on the
replica with the same value as on the source. For example, if a statement refers to a variable
@my_var, that statement is preceded in the binary log by the following statement, where value is
the value of @my_var on the source:

SET @my_var = value;

• Procedure calls can occur within a committed or rolled-back transaction. Transactional context is
accounted for so that the transactional aspects of procedure execution are replicated correctly.
That is, the server logs those statements within the procedure that actually execute and modify
data, and also logs BEGIN, COMMIT, and ROLLBACK statements as necessary. For example, if
a procedure updates only transactional tables and is executed within a transaction that is rolled
back, those updates are not logged. If the procedure occurs within a committed transaction, BEGIN
and COMMIT statements are logged with the updates. For a procedure that executes within a
rolled-back transaction, its statements are logged using the same rules that would apply if the
statements were executed in standalone fashion:

• Updates to transactional tables are not logged.

• Updates to nontransactional tables are logged because rollback does not cancel them.

• Updates to a mix of transactional and nontransactional tables are logged surrounded by BEGIN

and ROLLBACK so that replicas make the same changes and rollbacks as on the source.

• A stored procedure call is not written to the binary log at the statement level if the procedure is

invoked from within a stored function. In that case, the only thing logged is the statement that invokes
the function (if it occurs within a statement that is logged) or a DO statement (if it occurs within a
statement that is not logged). For this reason, care should be exercised in the use of stored functions
that invoke a procedure, even if the procedure is otherwise safe in itself.

4616

Restrictions on Stored Programs

27.8 Restrictions on Stored Programs

• SQL Statements Not Permitted in Stored Routines

• Restrictions for Stored Functions

• Restrictions for Triggers

• Name Conflicts within Stored Routines

• Replication Considerations

• Debugging Considerations

• Unsupported Syntax from the SQL:2003 Standard

• Stored Routine Concurrency Considerations

• Event Scheduler Restrictions

• Stored routines and triggers in NDB Cluster

These restrictions apply to the features described in Chapter 27, Stored Objects.

Some of the restrictions noted here apply to all stored routines; that is, both to stored procedures
and stored functions. There are also some restrictions specific to stored functions but not to stored
procedures.

The restrictions for stored functions also apply to triggers. There are also some restrictions specific to
triggers.

The restrictions for stored procedures also apply to the DO clause of Event Scheduler event definitions.
There are also some restrictions specific to events.

SQL Statements Not Permitted in Stored Routines

Stored routines cannot contain arbitrary SQL statements. The following statements are not permitted:

• The locking statements LOCK TABLES and UNLOCK TABLES.

• ALTER VIEW.

• LOAD DATA and LOAD XML.

• SQL prepared statements (PREPARE, EXECUTE, DEALLOCATE PREPARE) can be used in stored
procedures, but not in stored functions or triggers. Thus, stored functions and triggers cannot use
dynamic SQL (where you construct statements as strings and then execute them).

• Generally, statements not permitted in SQL prepared statements are also not permitted in stored

programs. For a list of statements supported as prepared statements, see Section 15.5, “Prepared
Statements”. Exceptions are SIGNAL, RESIGNAL, and GET DIAGNOSTICS, which are not
permissible as prepared statements but are permitted in stored programs.

• Because local variables are in scope only during stored program execution, references to them
are not permitted in prepared statements created within a stored program. Prepared statement
scope is the current session, not the stored program, so the statement could be executed after the
program ends, at which point the variables would no longer be in scope. For example, SELECT ...
INTO local_var cannot be used as a prepared statement. This restriction also applies to stored
procedure and function parameters. See Section 15.5.1, “PREPARE Statement”.

• Within all stored programs (stored procedures and functions, triggers, and events), the parser treats

BEGIN [WORK] as the beginning of a BEGIN ... END block.

To begin a transaction within a stored procedure or event, use START TRANSACTION instead.

4617

Restrictions for Stored Functions

START TRANSACTION cannot be used within a stored function or trigger.

Restrictions for Stored Functions

The following additional statements or operations are not permitted within stored functions. They are
permitted within stored procedures, except stored procedures that are invoked from within a stored
function or trigger. For example, if you use FLUSH in a stored procedure, that stored procedure cannot
be called from a stored function or trigger.

• Statements that perform explicit or implicit commit or rollback. Support for these statements is not
required by the SQL standard, which states that each DBMS vendor may decide whether to permit
them.

• Statements that return a result set. This includes SELECT statements that do not have an INTO

var_list clause and other statements such as SHOW, EXPLAIN, and CHECK TABLE. A function
can process a result set either with SELECT ... INTO var_list or by using a cursor and FETCH
statements. See Section 15.2.13.1, “SELECT ... INTO Statement”, and Section 15.6.6, “Cursors”.

• FLUSH statements.

• Stored functions cannot be used recursively.

• A stored function or trigger cannot modify a table that is already being used (for reading or writing) by

the statement that invoked the function or trigger.

• If you refer to a temporary table multiple times in a stored function under different aliases, a Can't
reopen table: 'tbl_name' error occurs, even if the references occur in different statements
within the function.

• HANDLER ... READ statements that invoke stored functions can cause replication errors and are

disallowed.

Restrictions for Triggers

For triggers, the following additional restrictions apply:

• Triggers are not activated by foreign key actions.

• When using row-based replication, triggers on the replica are not activated by statements originating
on the source. The triggers on the replica are activated when using statement-based replication. For
more information, see Section 19.5.1.36, “Replication and Triggers”.

• The RETURN statement is not permitted in triggers, which cannot return a value. To exit a trigger

immediately, use the LEAVE statement.

• Triggers are not permitted on tables in the mysql database. Nor are they permitted on

INFORMATION_SCHEMA or performance_schema tables. Those tables are actually views and
triggers are not permitted on views.

• The trigger cache does not detect when metadata of the underlying objects has changed. If a trigger

uses a table and the table has changed since the trigger was loaded into the cache, the trigger
operates using the outdated metadata.

Name Conflicts within Stored Routines

The same identifier might be used for a routine parameter, a local variable, and a table column. Also,
the same local variable name can be used in nested blocks. For example:

CREATE PROCEDURE p (i INT)
BEGIN
  DECLARE i INT DEFAULT 0;
  SELECT i FROM t;

4618

Replication Considerations

  BEGIN
    DECLARE i INT DEFAULT 1;
    SELECT i FROM t;
  END;
END;

In such cases, the identifier is ambiguous and the following precedence rules apply:

• A local variable takes precedence over a routine parameter or table column.

• A routine parameter takes precedence over a table column.

• A local variable in an inner block takes precedence over a local variable in an outer block.

The behavior that variables take precedence over table columns is nonstandard.

Replication Considerations

Use of stored routines can cause replication problems. This issue is discussed further in Section 27.7,
“Stored Program Binary Logging”.

The --replicate-wild-do-table=db_name.tbl_name option applies to tables, views, and
triggers. It does not apply to stored procedures and functions, or events. To filter statements operating
on the latter objects, use one or more of the --replicate-*-db options.

Debugging Considerations

There are no stored routine debugging facilities.

Unsupported Syntax from the SQL:2003 Standard

The MySQL stored routine syntax is based on the SQL:2003 standard. The following items from that
standard are not currently supported:

• UNDO handlers

• FOR loops

Stored Routine Concurrency Considerations

To prevent problems of interaction between sessions, when a client issues a statement, the server
uses a snapshot of routines and triggers available for execution of the statement. That is, the server
calculates a list of procedures, functions, and triggers that may be used during execution of the
statement, loads them, and then proceeds to execute the statement. While the statement executes, it
does not see changes to routines performed by other sessions.

For maximum concurrency, stored functions should minimize their side-effects; in particular, updating
a table within a stored function can reduce concurrent operations on that table. A stored function
acquires table locks before executing, to avoid inconsistency in the binary log due to mismatch of the
order in which statements execute and when they appear in the log. When statement-based binary
logging is used, statements that invoke a function are recorded rather than the statements executed
within the function. Consequently, stored functions that update the same underlying tables do not
execute in parallel. In contrast, stored procedures do not acquire table-level locks. All statements
executed within stored procedures are written to the binary log, even for statement-based binary
logging. See Section 27.7, “Stored Program Binary Logging”.

Event Scheduler Restrictions

The following limitations are specific to the Event Scheduler:

• Event names are handled in case-insensitive fashion. For example, you cannot have two events in

the same database with the names anEvent and AnEvent.

4619

Stored routines and triggers in NDB Cluster

• An event may not be created from within a stored program. An event may not be altered, or dropped
from within a stored program, if the event name is specified by means of a variable. An event also
may not create, alter, or drop stored routines or triggers.

• DDL statements on events are prohibited while a LOCK TABLES statement is in effect.

• Event timings using the intervals YEAR, QUARTER, MONTH, and YEAR_MONTH are resolved in months;
those using any other interval are resolved in seconds. There is no way to cause events scheduled
to occur at the same second to execute in a given order. In addition—due to rounding, the nature of
threaded applications, and the fact that a nonzero length of time is required to create events and to
signal their execution—events may be delayed by as much as 1 or 2 seconds. However, the time
shown in the Information Schema EVENTS table's LAST_EXECUTED column is always accurate to
within one second of the actual event execution time. (See also Bug #16522.)

• Each execution of the statements contained in the body of an event takes place in a new connection;
thus, these statements have no effect in a given user session on the server's statement counts such
as Com_select and Com_insert that are displayed by SHOW STATUS. However, such counts are
updated in the global scope. (Bug #16422)

• Events do not support times later than the end of the Unix Epoch; this is approximately the beginning
of the year 2038. Such dates are specifically not permitted by the Event Scheduler. (Bug #16396)

• References to stored functions, loadable functions, and tables in the ON SCHEDULE clauses of

CREATE EVENT and ALTER EVENT statements are not supported. These sorts of references are not
permitted. (See Bug #22830 for more information.)

Stored routines and triggers in NDB Cluster

While stored procedures, stored functions, triggers, and scheduled events are all supported by tables
using the NDB storage engine, you must keep in mind that these do not propagate automatically
between MySQL Servers acting as Cluster SQL nodes. This is because stored routine and trigger
definitions are stored in tables in the mysql system database using InnoDB tables, which are not
copied between Cluster nodes.

Any stored routine or trigger that interacts with MySQL Cluster tables must be re-created by running
the appropriate CREATE PROCEDURE, CREATE FUNCTION, or CREATE TRIGGER statements on
each MySQL Server that participates in the cluster where you wish to use the stored routine or trigger.
Similarly, any changes to existing stored routines or triggers must be carried out explicitly on all Cluster
SQL nodes, using the appropriate ALTER or DROP statements on each MySQL Server accessing the
cluster.

Warning

Do not attempt to work around the issue just described by converting any
mysql database tables to use the NDB storage engine. Altering the system
tables in the mysql database is not supported and is very likely to produce
undesirable results.

27.9 Restrictions on Views

The maximum number of tables that can be referenced in the definition of a view is 61.

View processing is not optimized:

• It is not possible to create an index on a view.

• Indexes can be used for views processed using the merge algorithm. However, a view that is

processed with the temptable algorithm is unable to take advantage of indexes on its underlying
tables (although indexes can be used during generation of the temporary tables).

4620

Restrictions on Views

There is a general principle that you cannot modify a table and select from the same table in a
subquery. See Section 15.2.15.12, “Restrictions on Subqueries”.

The same principle also applies if you select from a view that selects from the table, if the view selects
from the table in a subquery and the view is evaluated using the merge algorithm. Example:

CREATE VIEW v1 AS
SELECT * FROM t2 WHERE EXISTS (SELECT 1 FROM t1 WHERE t1.a = t2.a);

UPDATE t1, v2 SET t1.a = 1 WHERE t1.b = v2.b;

If the view is evaluated using a temporary table, you can select from the table in the view subquery
and still modify that table in the outer query. In this case, the view is stored in a temporary table
and thus you are not really selecting from the table in a subquery and modifying it at the same time.
(This is another reason you might wish to force MySQL to use the temptable algorithm by specifying
ALGORITHM = TEMPTABLE in the view definition.)

You can use DROP TABLE or ALTER TABLE to drop or alter a table that is used in a view definition.
No warning results from the DROP or ALTER operation, even though this invalidates the view. Instead,
an error occurs later, when the view is used. CHECK TABLE can be used to check for views that have
been invalidated by DROP or ALTER operations.

With regard to view updatability, the overall goal for views is that if any view is theoretically updatable,
it should be updatable in practice. Many theoretically updatable views can be updated now, but
limitations still exist. For details, see Section 27.5.3, “Updatable and Insertable Views”.

There exists a shortcoming with the current implementation of views. If a user is granted the basic
privileges necessary to create a view (the CREATE VIEW and SELECT privileges), that user cannot call
SHOW CREATE VIEW on that object unless the user is also granted the SHOW VIEW privilege.

That shortcoming can lead to problems backing up a database with mysqldump, which may fail due to
insufficient privileges. This problem is described in Bug #22062.

The workaround to the problem is for the administrator to manually grant the SHOW VIEW privilege to
users who are granted CREATE VIEW, since MySQL doesn't grant it implicitly when views are created.

Views do not have indexes, so index hints do not apply. Use of index hints when selecting from a view
is not permitted.

SHOW CREATE VIEW displays view definitions using an AS alias_name clause for each column. If a
column is created from an expression, the default alias is the expression text, which can be quite long.
Aliases for column names in CREATE VIEW statements are checked against the maximum column
length of 64 characters (not the maximum alias length of 256 characters). As a result, views created
from the output of SHOW CREATE VIEW fail if any column alias exceeds 64 characters. This can cause
problems in the following circumstances for views with too-long aliases:

• View definitions fail to replicate to newer replicas that enforce the column-length restriction.

• Dump files created with mysqldump cannot be loaded into servers that enforce the column-length

restriction.

A workaround for either problem is to modify each problematic view definition to use aliases that
provide shorter column names. Then the view replicates properly, and can be dumped and reloaded
without causing an error. To modify the definition, drop and create the view again with DROP VIEW and
CREATE VIEW, or replace the definition with CREATE OR REPLACE VIEW.

For problems that occur when reloading view definitions in dump files, another workaround is to edit
the dump file to modify its CREATE VIEW statements. However, this does not change the original view
definitions, which may cause problems for subsequent dump operations.

4621

4622

