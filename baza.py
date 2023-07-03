import psycopg2

def new_user_id(user):
    conn = psycopg2.connect(database="bot_oyb", user="postgres", password="oybizyay")
    with conn.cursor() as cur:
        cur.execute("""
        create table if not exists users_id(
        id serial primary key,
        name_id_user varchar(40)
        );
        """)
        cur.execute("""
        insert into users_id(name_id_user) 
        values(%s);
        """ %(user))
        conn.commit()
        conn.close()



def search_id():
    conn = psycopg2.connect(database="bot_oyb", user="postgres", password="oybizyay")
    with conn.cursor() as cur:
        cur.execute("""
                create table if not exists users_id(
                id serial primary key,
                name_id_user varchar(40)
                );
                """)
        cur.execute("""
        select name_id_user from users_id;
        """)
        list_id = cur.fetchall()
        list_id = [i[0] for i in list_id]
        conn.close()
        return list_id


