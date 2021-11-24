import streamlit as st
import MySQLdb
import time

time.sleep(3)
st.title("Hola!")

# Connect
db = MySQLdb.connect(host="db",
                     user="test",
                     passwd="test123",
                     db="test")

cursor = db.cursor()
cursor.execute("USE test")
cursor.execute("SHOW TABLES;")
st.write(str(cursor.fetchall()))

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()
tabs = ["Mapas", "Analisis", "Regresion"]

if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Mapas"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Mapas")
    active_tab = "Mapas"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Mapas":
    st.write("Welcome to my lovely page!")
elif active_tab == "Analisis":
    st.write("This page was created as a hacky demo of tabs")
    # --------------- nombre de columnas
    # cursor.execute("""SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS`
    # WHERE `TABLE_SCHEMA` = 'test'AND `TABLE_NAME` = 'CovidConfirmed';""")

    cursor.execute("""SELECT Confirmed, `Country/Region`, Sum(Case When `Country/Region` = '$chosentrack' 
         Then totalConf Else 0 End) AS totalConf, FROM CovidConfirmed""")
    conf = cursor.fetchall()
    st.write(conf)

elif active_tab == "Regresion":
    st.write("If you'd like to contact me, then please don't.")
else:
    st.error("Something has gone terribly wrong.")


# Close the connection
db.close()
