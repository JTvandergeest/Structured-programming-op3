from flask import Flask
import json
import random
import traceback

app = Flask(__name__)
import psycopg2

# Database
connect = psycopg2.connect("user=postgres password=pgadminJTgeest dbname=voordeelshopgpx")
c = connect.cursor()
print("Postgres connected")


# Routing
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/product/update')
def get_products_recs():

    # c.execute("DROP TABLE IF EXISTS rec_eng1_ses_prods;")

    # c.execute("CREATE TABLE rec_eng1_ses_prods "
    #           "(id varchar NOT NULL,"
    #           "prod1 varchar,"
    #           "prod2 varchar,"
    #           "prod3 varchar,"
    #           "prod4 varchar, "
    #           "prod5 varchar, "
    #           "CONSTRAINT rec_eng1_ses_prods_pkey PRIMARY KEY (id))")

    c.execute("SELECT _id FROM all_p where _id not in (SELECT id FROM rec_eng1_ses_prods)")
    connect.commit()

    items = c.fetchall()

    for idx, item in enumerate(items):

        try:

            pid = item[0]

            catprods = get_products_same_category(pid)
            sesprods = get_same_session_products(pid)

            # Shuffle, unique and max 5 recommendations
            total_recs = catprods + sesprods
            non_duplicates = list(dict.fromkeys(total_recs))
            random.shuffle(non_duplicates)
            recs = non_duplicates[0:5]

            while len(recs) < 5:
                recs.append('null')

            if len(recs) == 5:
                c.execute("INSERT INTO rec_eng1_ses_prods VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(pid, recs[0], recs[1], recs[2], recs[3], recs[4]))
                connect.commit()

            print("{}/{} Item Recommendations loaded for ({}) : {} ({}%)".format(idx, len(items), pid, recs, (idx/len(items)) * 100))

        except:
            if c is not None:
                connect.commit()
            print("Rec failed for product idx {}".format(idx))

    return ""

# Collaborative filtering
# Gebaseerd op sessions van eerdere bezoekers

def get_same_session_products(id):

    # Selecteerd alle sessions waarbij items in het mandje zitten

    c.execute("select * from all_se where itorder LIKE '%{}%'".format(id))
    filtered_sessions = c.fetchall()

    # Maak een heatmap op basis van alle gefilterde session producten
    heatmap = {}
    for fs in filtered_sessions:
        ids = fs[5][1:-1]
        split_ids = ids.split(",")
        for sid in split_ids:
            try:
                heatmap[sid] += 1
            except:
                heatmap[sid] = 1

    # Reset heatmap for id
    heatmap[str(id)] = -1

    # Filter met min amt barrier
    total = 0
    collab_prods = []
    for item in heatmap.items():
        total += item[1]
    barrier = total / len(heatmap)

    if barrier < 2.1:
        barrier = 2.1

    for item in heatmap.items():
        if item[1] >= barrier:
            collab_prods.append(item)

    # Bubble sort op basis van hoevaak hij is gekocht
    bubble_sort_heatmap(collab_prods)

    return [x[0] for x in collab_prods][0:5]

def bubble_sort_heatmap(nums):
    # We set swapped to True so the loop looks runs at least once
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(nums) - 1):
            if nums[i][1] < nums[i + 1][1]:
                # Swap the elements
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                # Set the flag to True so we'll loop again
                swapped = True

def get_products_same_category(id):

    # Vind product en gender
    c.execute("SELECT * FROM all_p WHERE _id = '{}'::varchar".format(id))
    found_prod = c.fetchall()[0]
    sub_sub_cat_selected_prod = found_prod[5]

    #Create gender check string
    check_gender = ""
    if found_prod[6] is not None:
        check_gender = " and (gender = '{}' or gender =  'Unisex')".format(found_prod[6])

    # Create brand check string
    check_brand = ""
    if found_prod[9] is not None:
        check_brand = " and (brand = '{}')".format(found_prod[9])

    # print(check_gender)
    # print(check_brand)
    # print(found_prod)
    # print(sub_sub_cat_selected_prod)

    # If has sub sub category get other prods from sub cat
    if sub_sub_cat_selected_prod is not None:
        c.execute("SELECT _id FROM all_p WHERE sub_sub_category = '{}'::varchar {} {} limit 5".format(sub_sub_cat_selected_prod, check_brand, check_gender))
        other_prods = c.fetchall()
        pids = [x[0] for x in other_prods]
        return pids
    return []

if __name__ == '__main__':
    app.run(host='localhost', port=5400)
