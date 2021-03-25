#https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html
#https://api.mongodb.com/python/current/tutorial.html
#https://www.psycopg.org/docs/usage.html
import psycopg2
from pymongo import MongoClient

def dataimportmgdb():
    cur.execute("DROP TABLE IF EXISTS all_prod;")
    cur.execute("DROP TABLE IF EXISTS all_ses;")
    cur.execute("DROP TABLE IF EXISTS all_prof;")

    cur.execute("CREATE TABLE all_prod (_ID varchar PRIMARY KEY, "
                "data varchar, "
                "price integer, "
                "category varchar,"
                "sub_category varchar, "
                "sub_sub_category varchar, "
                "gender varchar, "
                "color varchar, "
                "discount varchar,"
                "brand varchar);")

    cur.execute("CREATE TABLE all_ses (_ID varchar PRIMARY KEY, "
                "buid varchar, has_sale varchar, segment varchar, preferences varchar, itorder varchar);")

    cur.execute("CREATE TABLE all_prof (_ID varchar PRIMARY KEY, "
                "buids varchar,"
                "recommendations varchar,"
                "viewed_before varchar);")
    col = db.products
    products = col.find()
    count = 0
    for i in products:
        try:
            cur.execute(
                "INSERT INTO all_prod (_ID, data, price,category ,sub_category, sub_sub_category, gender, color, discount, brand) VALUES (%s, %s, %s,%s, %s, %s,%s, %s,%s,%s)",
                (i['_id'],
                 i['name'] if 'name' in i else None,
                 i['price']['selling_price'] if 'price' in i else None,
                 i['category'] if 'category' in i else None,
                 i['sub_category'] if 'sub_category' in i else None,
                 i['sub_sub_category'] if 'sub_sub_category' in i else None,
                 i['gender'] if 'gender' in i else None,
                 i['color'] if 'color' in i else None,
                 str(i['properties']['discount']) if 'properties' in i else None,
                 i['brand'] if 'brand' in i else None))
            count += 1
            if count % 1000 == 0:
                print(count, "Products")
        except:
            continue
    print("done with products")

    col = db.profiles
    profiles = col.find()
    count = 0
    for i in profiles:
        cur.execute("INSERT INTO all_prof (_ID, buids, recommendations,viewed_before) VALUES (%s, %s, %s,%s)",
                    (str(i['_id']),
                     i['buids'] if 'buids' in i else None,
                     "{}",
                     i['recommendations']['viewed_before'] if 'recommendations' in i else None))
        count += 1
        if count % 1000 == 0:
            print(count, "Profiles")
    print("done with profiles")

    col = db.sessions
    sessions = col.find()

    count = 0
    for i in sessions:
        orderstring = "{"
        try:
            for j in range(len(i['order']['products'])):
                # print(i['order']['products'][j].get('id'),end= " ")
                orderstring += i['order']['products'][j].get('id') + ","
            orderstring = orderstring[:-1]
            orderstring += "}"
        except:
            orderstring = "{}"

        cur.execute("INSERT INTO all_ses (_ID, buid, has_sale, preferences,itorder,segment) VALUES (%s, %s,%s,%s,%s,%s)",
                    (str(i['_id']),
                     str(i['buid']) if 'buid' in i else None,
                     str(i['has_sale']) if 'has_sale' in i else None,
                     str(i['preferences']) if 'preferences' in i else None,
                     orderstring,
                     str(i['segment']) if 'segment' in i else None))
        count += 1
        if count % 1000 == 0:
            print(count, "Sessions")
    print("done with sessions")
    conn.commit()


def clearerd():
    cur.execute("DROP TABLE IF EXISTS category CASCADE;")
    cur.execute("DROP TABLE IF EXISTS gender CASCADE;")
    cur.execute("DROP TABLE IF EXISTS brand CASCADE;")
    cur.execute("DROP TABLE IF EXISTS product CASCADE")
    cur.execute("DROP TABLE IF EXISTS profile CASCADE")
    cur.execute("DROP TABLE IF EXISTS session CASCADE")
    cur.execute("DROP TABLE IF EXISTS preference_session CASCADE")
    cur.execute("DROP TABLE IF EXISTS order_session CASCADE")

    return


client = MongoClient('localhost', 27017)    #MongodB connectie
db = client.huwebshop
print("mongo connect")
conn = psycopg2.connect("user=postgres password=pgadminJTgeest dbname=voordeelshopgpx")
cur = conn.cursor()
print("pg connected")

#~~~~~~~~~~~~~~~~~~~~~~~~ code voor product koppeling

dataimportmgdb()

clearerd()

#~~~~~~~~~~~~~~~~~~~~~~~~ code voor profil koppeling
#getsegmenttypes()
print("done")
# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()
print("done")