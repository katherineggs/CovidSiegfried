import streamlit as st
import pandas as pd
import MySQLdb
import time
import re

time.sleep(3)
st.set_page_config(layout="wide")
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
    st.write("Mapaaaas")

elif active_tab == "Analisis":
    st.write("En esta página se muestras algunos datos interesantes")

    cursor.execute("""SELECT SUM(Confirmed) FROM CovidConfirmed""")
    totalConf = str(cursor.fetchall())
    totalConf = re.sub(r"^.*?'", '', totalConf)
    totalConf = re.sub(r"'.*", '', totalConf)
    totalConf = int(totalConf)

    cursor.execute("""SELECT SUM(Deaths) FROM CovidDeaths""")
    totalDead = str(cursor.fetchall())
    totalDead = re.sub(r"^.*?'", '', totalDead)
    totalDead = re.sub(r"'.*", '', totalDead)
    totalDead = int(totalDead)

    cursor.execute("""SELECT SUM(Recovered) FROM CovidRecovered""")
    totalReco = str(cursor.fetchall())
    totalReco = re.sub(r"^.*?'", '', totalReco)
    totalReco = re.sub(r"'.*", '', totalReco)
    totalReco = int(totalReco)

    htmlHeader1 = """
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; 
      background: #eef9ea; padding-top: 5px; width: 350px; height: 50px;">
        <h3 class="card-title" style="background-color:#eef9ea; color:#008080; 
        font-family:Georgia; text-align: center; padding: 0px 0;">
    """
    htmlHeader2 = """</h3></div></div>"""

    titles = ["Total de Confirmados", "% de muertes", "% de Recuperados"]
    muertes = (totalDead * 100) / totalConf
    recuper = (totalReco * 100) / totalConf
    data = [totalConf, muertes, recuper]
    cont = 0

    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 15, 1, 15, 1, 15, 1])
        cols = [col1, col2, col3, col4, col5, col6, col7]
        for column in range(0, len(cols)):
            if column % 2:
                with cols[column]:
                    header = htmlHeader1 + titles[cont] + htmlHeader2
                    st.markdown(header, unsafe_allow_html=True)
                    st.write(data[cont])
                    st.write("------------------")
                cont += 1
            else:
                st.write("")

    st.write("Más del 50 % de los casos confirmadas no aclaran si se recuperaron, murieron o continuan luchando.")
    st.write("------------------")

    cases = ["Casos confirmados", "Muertes", "Recuperados"]
    st.write("Seleccione el caso que desea ver")
    caseOption = st.selectbox("País con mayor cantidad de", cases)

    if caseOption == "Casos confirmados":
        cursor.execute("""SELECT `Country/Region`, SUM(Confirmed) as Tot
                          FROM CovidConfirmed GROUP BY `Country/Region` ORDER BY tot DESC LIMIT 1""")
        confirmed = cursor.fetchall()

        st.write("País----", confirmed[0][0])
        st.write("Cantidad de personas----", confirmed[0][1])

        dfMap = pd.read_sql('SELECT * FROM table_name') #---------------
        dfMap = dfMap[dfMap["Country/Region"] == confirmed[0][0]]

        mapData = dfMap[["Lat", "Lon"]].copy()
        mapData = mapData.rename(columns={"Lat": "lat", "Lon": "lon"})

        st.map(mapData)

    elif caseOption == "Muertes":
        cursor.execute("""SELECT `Country/Region`, SUM(Deaths) as Tot
                          FROM CovidDeaths GROUP BY `Country/Region` ORDER BY tot DESC LIMIT 1""")
        deaths = cursor.fetchall()
    else:
        cursor.execute("""SELECT `Country/Region`, SUM(Recovered) as Tot
                          FROM CovidRecovered GROUP BY `Country/Region` ORDER BY tot DESC LIMIT 1""")
        recovered = cursor.fetchall()



# SELECT SUM(views) FROM (SELECT threadid, views FROM table_name GROUP BY threadid, views)
elif active_tab == "Regresion":
    st.write("If you'd like to contact me, then please don't.")
else:
    st.error("Something has gone terribly wrong.")


# Close the connection
db.close()
