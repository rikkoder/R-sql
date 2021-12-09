import mysql.connector as c
import getpass
import sys


print('''
                 >>>>> WELCOME TO R-SQL <<<<<
==============================================================
           A PROGRAM WRITTEN AND DESIGNED BY RITESH
______________________________________________________________

              CLASS XII , INVESTIGATORY PROJECT
==============================================================
''')

dbo = ''
u = ''
p = ''


def start():
    global u, p, dbo
    u = input('ENTER USER : ')
    p = getpass.getpass('ENTER PASSWORD : ')
    try:
        dbo = c.connect(host='localhost', user=u, passwd=p)
    except:
        print('------> INVALID USER/PASSWORD <------')
        start()


try:
    start()
except (KeyboardInterrupt, EOFError):
    print('\nexitting...\n')
    sys.exit(0)
cursor = dbo.cursor()


def choices(commands):
    no = len(commands)
    print('''
    ------------------------------------
    |   COMMAND NO   |     COMMANDS    |
    ------------------------------------''')
    for i in range(1, no + 1):
        print('    |     ', i, ' ------>', commands[i] + ' ' * (16 - len(commands[i])), '|')
    print('''    ------------------------------------''')
    try:
        choice = int(input('\nENTER COMMAND NO : '))
    except (KeyboardInterrupt, EOFError):
        print('\nexitting...\n')
        sys.exit(0)
    except:
        print('INVALID INPUT')
        return choices(commands)
    if choice in range(1, no + 1):
        return choice
    else:
        print('INVALID INPUT')
        return choices(commands)


def menu():
    options = {
        1: 'CREATE DATABASE ',
        2: 'DROP DATABASE ',
        3: 'USE DATABASE ',
        4: 'SHOW DATABASES ',
        5: 'QUIT '}

    choice = choices(options)
    database = ''

    if choice == 5:
        if input('ARE YOU SURE (Y/N): ').upper() == 'Y':
            print('\nexitting...\n')
            sys.exit(0)

    elif choice < 4:
        database = input('ENTER DATABASE NAME : ')
        if not database.strip() or database == '#back':
            return menu()

    try:
        if choice == 1:
            cursor.execute(options[choice] + database)
            print(f'DATABASE {database} CREATED')

        elif choice == 2:
            if input('ARE YOU SURE (Y/N): ').upper() == 'Y':
                cursor.execute(options[choice] + database)
                print(f'\nDATABASE {database} DELETED')

        elif choice == 3:
            cursor.execute(f'USE {database}')
            return database

        else:
            cursor.execute(options[choice] + database)
            data = cursor.fetchall()
            print()
            for x in data:
                print(' ' * 4, x[0], '\n', '-' * 35)

    except c.errors.ProgrammingError as e:
        print(e)

    except:
        if choice == 1:
            print(f'\nDATABASE, {database}, ALREADY EXISTS')
            if input('DO YOU WANT TO REPLACE EXISTING DATABASE WITH NEW ONE <Y/N> : ').upper() == 'Y':
                cursor.execute(options[2] + database)
                cursor.execute(options[1] + database)
        elif choice == 2:
            print(f'\n--------->DATABASE {database} DOESN\'T EXIST<---------')
        elif choice == 3:
            print(f'\nDATABASE {database} NOT FOUND')
            if input(f'DO YOU WANT TO CREATE {database.upper()} <Y/N> : ').upper() == 'Y':
                cursor.execute(options[1] + database)
    return menu()


def constraints(work, field=None):
    options = {
        1: 'PRIMARY KEY ',
        2: 'UNIQUE ',
        3: 'CHECK ',
        4: 'DEFAULT ',
        5: 'NOT NULL ',
        6: 'NONE '}
    if work == 'add':
        del options[4], options[5], options[6]
    elif work == 'drop':
        del options[3], options[4], options[5], options[6]

    checkers = {
        1: '>=',
        2: '>',
        3: '<=',
        4: '<',
        5: '=',
        6: '!=',
        7: 'LIKE',
        8: 'BETWEEN',
        9: 'IN'}

    constraint = options[choices(options)]
    if work == 'add':
        val = f'( {field} )'
    else:
        val = ''

    if constraint == 'CHECK ':
        condn = choices(checkers)
        check = input('ENTER VALUE FOR CHECK')
        val = f'( {field} {checkers[condn]} {check} )'

    elif constraint == 'DEFAULT ':
        val = {input('ENTER DEFAULT VALUE FOR THE FIELD : ')}

    elif constraint == 'NONE ':
        constraint = ''

    return f'{constraint} {val}'


def fields_maker(src=''):
    types = {
        1: 'INTEGER ',
        2: 'BIGINT',
        3: 'DECIMAL ',
        4: 'CHARACTER ',
        5: 'VARCHAR '}

    fields = []
    while src != 'modify field':
        n = input('ENTER NO OF FIELDS : ')
        if n.isnumeric() and float(n) // 1 == int(n) and int(n) > 0:
            n = int(n)
            break
        else:
            print('\n------->INVALID INPUT<-------')
    else:
        n = 1
    for i in range(n):
        if src == 'modify field':
            field_name = (input('\nENTER NEW NAME FOR OF THE FIELD : '))
        else:
            field_name = (input(f'\nENTER FIELDNAME OF FIELD {i + 1} : '))

        print('ENTER DATA-TYPE OF FIELD', i + 1, 'FROM BELOW !!')
        Type = choices(types)
        if Type == 2:
            lim = ''
        elif Type == 3:
            while True:
                a = int(input('ENTER NO OF TOTAL DIGITS : '))
                b = int(input(f'ENTER NO OF DECIMAL PLACES OUT OF {a} : '))
                if a >= b:
                    break
                else:
                    print('\nTOTAL DIGITS MUST BE >= DECIMAL PLACES : ')
            lim = (a, b)
        else:
            lim = '(' + input('ENTER MAX LENGTH OF VALUE : ') + ')'

        constraint = constraints('field_maker', field_name)

        fields.append(f'{field_name} {types[Type]} {str(lim)} {constraint}')

    return fields


def describe(data):
    rows = []
    for x in data:
        rows.append(x)
    print('''     FIELD     |      TYPE     |      NULL     |      KEY      |    DEFAULT    |      EXTRA    |

________________________________________________________________________________________________''')
    for i in range(len(rows)):
        # print('loop')
        for j in range(6):
            #    print('loop')
            print(str(rows[i][j]) + ' ' * (15 - len(str(rows[i][j]))), end='|')
        print()
        print('-' * 96)


def display_query(fields, data):
    length = []
    for column, field in enumerate(fields):
        col_len = [len(field)]
        for row in data:
            col_len.append(len(str(row[column])))
        length.append(max(col_len))

    print()
    for n, field in enumerate(fields):
        print(f'| {field + " " * (length[n] - len(field))} ', end='|')
    print()
    #print(f'| {"-" * sum(length)} |')

    for row in data:
        print()
        for n, column in enumerate(row):
            print(f'| {str(column) + " " * (length[n] - len(str(column)))} ', end='|')
        print()


def dbmenu(database):
    dbo = c.connect(host='localhost', user=u, passwd=p, database=database)
    cursor = dbo.cursor()

    options = {
        1: 'CREATE TABLE ',
        2: 'DROP TABLE ',
        3: 'DESCRIBE TABLE ',
        4: 'MODIFY TABLE ',
        5: 'RUN QUERIES ',
        6: 'INSERT VALUES ',
        7: 'SHOW TABLES ',
        8: 'MENU ',
        9: 'QUIT '}

    choice = choices(options)

    if choice == 1:
        table = input('ENTER TABLE NAME : ')
        if not table.strip() or table == '#back':
            return dbmenu(database)

        try:
            cursor.execute(f'DESC {table}')
            data = cursor.fetchall()
            describe(data)
            print()
            print(f'TABLE {table} ALREADY EXISTS')
            if input('DO YOU WANT TO REPLACE EXISTING TABLE WITH NEW ONE <Y/N> : ').upper() == 'Y':
                fields = fields_maker()
                cursor.execute(f'DROP TABLE {table}')
                cursor.execute(f'CREATE TABLE {table} ( {",".join(fields)})')
                cursor.execute(f'DESC {table}')
                data = cursor.fetchall()
                describe(data)

        except:
            try:
                fields = fields_maker()
                cursor.execute(f'CREATE TABLE {table} ( {",".join(fields)})')
                cursor.execute(f'DESC {table}')
                data = cursor.fetchall()
                describe(data)
            except c.errors.ProgrammingError as e:
                print(e)
            except:
                print('-----> INVALID TABLE NAME <-----')

    elif choice == 2:
        table = input('ENTER TABLE NAME: ')
        if not table.strip() or table == '#back':
            return dbmenu(database)

        if input('ARE YOU SURE <Y/N> : ').upper() == 'Y':
            try:
                cursor.execute(f'{options[2]} {table}')
                print(f'TABLE {table} DELETED')
            except c.errors.ProgrammingError as e:
                print(e)
            except:
                print(f'\n--------->TABLE {table} DOESN\'T EXIST<---------')

    elif choice == 3:
        table = input('ENTER TABLE NAME: ')
        if table.isspace() or table == '#back':
            return dbmenu(database)

        try:
            cursor.execute(f'DESC {table}')
            data = cursor.fetchall()
            describe(data)

        except c.errors.ProgrammingError as e:
            print(e)
        except:
            print(f'TABLE {table} DOESN\'T EXIST')

    elif choice == 4:
        table = input('ENTER TABLE NAME: ')
        if table.isspace() or table == '#back':
            return dbmenu(database)

        try:
            cursor.execute(f'DESC {table}')
            data = cursor.fetchall()
            describe(data)
            modify = {
                1: 'RENAME TABLE ',
                2: 'ADD CONSTRAINT ',
                3: 'DROP CONSTRAINT ',
                4: 'ADD FIELD(S) ',
                5: 'DROP FIELD(S) ',
                6: 'MODIFY FIELD',
                7: 'BACK '
            }
            mod_no = choices(modify)

            if mod_no == 1:
                new_name = input('ENTER NEW NAME: ')
                if new_name.isspace() or new_name == '#back':
                    return dbmenu(database)
                if input('ARE YOU SURE <Y/N> : ').upper() == 'Y' and new_name != table:
                    cursor.execute(f'RENAME TABLE {table} TO {new_name}')
                    print('RENAMED SUCCESSFULLY')

            elif mod_no == 2:
                field_name = input('ENTER NAME OF THE FIELD : ')
                if field_name.isspace() or field_name == '#back':
                    return dbmenu(database)
                constraint = constraints('add', field_name)
                cursor.execute(f'ALTER TABLE {table} ADD {constraint}')
                print(f'TABLE {table} MODIFIED')

            elif mod_no == 3:
                constraint = constraints('drop')
                cursor.execute(f'ALTER TABLE {table} DROP {constraint}')
                print(f'TABLE {table} MODIFIED')

            elif mod_no == 4:
                fields = fields_maker()
                cursor.execute(f'ALTER TABLE {table} ADD COLUMN ({",".join(fields)})')
                print(f'{len(fields)} FIELD(S) ADDED TO TABLE {table}')

            elif mod_no == 5:
                n = int(input('ENTER NO OF FIELD(S) TO DROP : '))
                fields = []
                for i in range(n):
                    field = input(f'ENTER FIELD {i + 1} NAME : ')
                    fields.append(field)
                print('\nFOLLOWING FIELD(S) WILL BE DROPPED : ')
                for i in range(n):
                    print(' ' * 4, fields[i], '\n', '-' * 35)
                if input('ARE YOU SURE <Y/N> : ').upper() == 'Y':
                    for i in range(n):
                        cursor.execute(f'ALTER TABLE {table} DROP {fields[i]}')
                    print(f'{n} FIELD(S) DROPPED FROM TABLE {table}')
                else:
                    print('...COMMAND TERMINATED SUCCESSFULLY')

            elif mod_no == 6:
                field_name = input('ENTER FIELD NAME : ')
                field_data = fields_maker('modify field')
                try:
                    cursor.execute(f'ALTER TABLE {table} CHANGE {field_name} {field_data[0]}')
                    print('MODIFIED SUCCESSFULLY ....')
                except c.errors.ProgrammingError as e:
                    print(e)
                except:
                    print(
                        f'--------> FIELD {field_name} DOESN\'T EXIST OR ITS VALUES CONTRADICTS NEW DATA TYPE <--------')

            else:
                return dbmenu(database)
        except c.errors.ProgrammingError as e:
            print(e)
        except:
            print(f'TABLE {table} DOESN\'T EXIST')

    elif choice == 5:
        while True:
            tab_no = input('ON HOW MANY TABLES ? ')
            if tab_no.isdigit() and int(tab_no) >= 0:
                tab_no = int(tab_no)
                break
            else:
                print('-----> INVALID INPUT <-----')

        tables = []
        fields = []
        no_of_fields = []
        fields_conditions = []
        for i in range(tab_no):
            print()
            table = input(f'ENTER TABLE {i + 1} NAME : ')
            tables.append(table)

            if tab_no == 1:
                while True:
                    n = input(f'ENTER NO OF FIELDS FROM TABLE {table} or type  * for all : ')
                    if n == '*':
                        n = 0
                        fields.append('*')
                        break

                    else:
                        try:
                            n = int(n)
                            break
                        except:
                            print('------> INVALID INPUT <------')
            else:
                while True:
                    try:
                        n = int(input(f'ENTER NO OF FIELDS FROM TABLE {table} : '))
                        if n > 0:
                            no_of_fields.append(n)
                            break

                        else:
                            print('------> INVALID INPUT <------')
                    except:
                        print('------> INVALID INPUT <------')

            for j in range(n):
                field = input(f'ENTER NAME OF FIELD {j + 1} : ')
                fields.append(field)
                field_condition = input('ENTER CONDITION TO CHECK (IF ANY) : ')
                fields_conditions.append(field_condition)

        if tab_no > 1:
            alias = []
            temp_alias = [tab[0] + str(n) for (n, tab) in enumerate(
                tables)]  # could have stuck to my old idea of using dictionary in format table:fields
            for n, a in enumerate(temp_alias):
                for j in range(no_of_fields[n]):
                    alias.append(a)

            fields_with_alias = [f"{a}.{f}" for a, f in zip(alias, fields)]
            tables_with_alias = [f"{t} {a}" for t, a in zip(tables, temp_alias)]

            condition = [a + b for a, b in zip(fields_with_alias, fields_conditions) if b]
            if condition:
                condition[0] = f'AND {condition[0]}'

            common_field = input('ENTER NAME OF THE COMMON FIELD : ')
            cursor.execute(
                f'SELECT {",".join(fields_with_alias)} FROM {",".join(tables_with_alias)} WHERE {f".{common_field}=".join(temp_alias) + f".{common_field} "} {" AND ".join(condition)}')

        elif tab_no == 1:
            condition = [a + b for a, b in zip(fields, fields_conditions) if b]
            if condition:
                condition[0] = f'WHERE AND {condition[0]}'
            cursor.execute(f'SELECT {",".join(fields)} FROM {",".join(tables)}')

        data = cursor.fetchall()

        if fields == ['*']:
            fields = []
            cursor.execute(f'DESC {tables[0]}')
            rows = cursor.fetchall()
            for i in rows:
                fields.append(i[0])

        display_query(fields, data)


    elif choice == 6:
        table = input('ENTER TABLE NAME : ')

        fields = []
        types = []
        cursor.execute(f'DESC {table}')
        rows = cursor.fetchall()
        for i in rows:
            fields.append(i[0])
            types.append(i[1])

        n = int(input('ENTER NO OF ENTRIES : '))
        values = []
        for i in range(n):
            entry = []
            for field,Type in zip(fields, types):
                field_value = input(f'ENTER VALUE FOR ENTRY {i+1}, {field} : ')
                if 'int' in Type:
                    field_value = int(field_value)
                elif 'float' in Type or 'decimal' in Type:
                    field_value = float(field_value)
                entry.append(field_value)
            values.append(str(tuple(entry)))

        print(values)
        cursor.execute(f'INSERT INTO {table} VALUES {",".join(values)}')
        dbo.commit()
        rows_affected = cursor.rowcount
        print(f'{rows_affected} ROWS AFFECTED...')

    elif choice == 7:
        cursor.execute('SHOW TABLES')
        print(f'TABLES IN DATABASE {database}\n')
        for x in cursor:
            print(' ' * 4, x[0], '\n', '-' * 35)

    elif choice == 8:
        menu()

    elif choice == 9:
        if input('ARE YOU SURE (Y/N): ').upper() == 'Y':
            print('\nexitting...\n')
            sys.exit(0)

    dbmenu(database)

try:
    dbmenu(menu())
except c.errors.ProgrammingError as e:
    print(e)
except (KeyboardInterrupt, EOFError):
    print('\nexitting...\n')
    sys.exit(0)
except Exception as e:
    print(type(e), e)
    print('xxxxx    SOMETHING WENT WRONG    xxxxx')
    dbmenu(menu())
