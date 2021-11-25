import streamlit as st
import mysql.connector as connection
import pandas as pd
import MySQLdb
import time
import re

time.sleep(3)
st.set_page_config(layout="wide", page_title="Covid Siegfried")
st.title("Bienvenido!")
st.write("Esto es un analisis a partir de datos recuperados de la pandemia de COVID19")

# Connect
db = MySQLdb.connect(host="db",
                     user="test",
                     passwd="test123",
                     db="test")

connectPd = connection.connect(host="db", database='test', user="test", passwd="test123", use_pure=True)

cursor = db.cursor()
cursor.execute("USE test")
cursor.execute("SHOW TABLES;")
# st.write(str(cursor.fetchall()))

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()
tabs = ["Mapas", "Analisis"]

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
    st.subheader("En esta página se muestran los mapas por país y fecha")

    dfMapConf = pd.read_sql('SELECT * FROM CovidConfirmed', con=connectPd)
    conf = cursor.fetchall()

    lPaises = pd.read_sql('SELECT `Country/Region` FROM CovidConfirmed GROUP BY `Country/Region`', con=connectPd)
    lFecha = pd.read_sql('SELECT `Date` FROM CovidConfirmed GROUP BY `Date`', con=connectPd)

    # Seleccionar país
    pais = st.selectbox("Seleccione un país:", lPaises["Country/Region"].tolist())
    pais = str(pais)

    # Seleccionar Fecha
    fecha = st.selectbox('Seleccione una fecha:', lFecha["Date"].tolist())
    fecha = str(fecha).strip("00:00:00")

    st.subheader("Casos Confirmados de COVID19")

    confirmadosLL = pd.read_sql("""SELECT * FROM CovidConfirmed """, con=connectPd)

    cant = pd.read_sql("""SELECT Confirmed, `Date`, `Country/Region` FROM CovidConfirmed""", con=connectPd)
    cant = cant[cant["Country/Region"] == pais]
    cant = cant[cant["Date"] == fecha]
    st.write("En ", pais, "en la fecha", fecha)
    st.write("Hubo un total de casos de: ", cant["Confirmed"])

    confirmadosLL = confirmadosLL[confirmadosLL["Country/Region"] == pais]
    confirmadosLL = confirmadosLL[confirmadosLL["Date"] == fecha]

    mapData = confirmadosLL[["Lat", "Lon"]].copy()
    mapData = mapData.rename(columns={"Lat": "lat", "Lon": "lon"})
    st.map(mapData, zoom=None)
    st.write("----------------")

    # -----------------------------------------------------
    st.subheader("Casos Fallecidos de COVID19")

    cant = pd.read_sql("""SELECT Deaths, `Date`, `Country/Region` FROM CovidDeaths""", con=connectPd)
    cant = cant[cant["Country/Region"] == pais]
    cant = cant[cant["Date"] == fecha]
    st.write("En ", pais, "en la fecha", fecha)
    st.write("Hubo un total de casos de: ", cant["Deaths"])

    dfMapConf = pd.read_sql('SELECT * FROM CovidDeaths', con=connectPd)

    lPaises = pd.read_sql('SELECT `Country/Region` FROM CovidDeaths GROUP BY `Country/Region`', con=connectPd)
    lFecha = pd.read_sql('SELECT `Date` FROM CovidDeaths GROUP BY `Date`', con=connectPd)

    confirmadosLLF = pd.read_sql("""SELECT * FROM CovidDeaths """, con=connectPd)

    confirmadosLLF = confirmadosLLF[confirmadosLLF["Country/Region"] == pais]
    confirmadosLLF = confirmadosLLF[confirmadosLLF["Date"] == fecha]

    mapData = confirmadosLLF[["Lat", "Lon"]].copy()
    mapData = mapData.rename(columns={"Lat": "lat", "Lon": "lon"})
    st.map(mapData, zoom=None)
    st.write("----------------")

    # -----------------------------------------------------
    st.subheader("Casos Recuperados de COVID19")
    cant = pd.read_sql("""SELECT Recovered, `Date`, `Country/Region` FROM CovidRecovered""", con=connectPd)
    cant = cant[cant["Country/Region"] == pais]
    cant = cant[cant["Date"] == fecha]
    st.write("En ", pais, "en la fecha", fecha)
    st.write("Hubo un total de casos de: ", cant["Recovered"])


    dfMapConf = pd.read_sql('SELECT * FROM CovidRecovered', con=connectPd)

    lPaises = pd.read_sql('SELECT `Country/Region` FROM CovidRecovered GROUP BY `Country/Region`', con=connectPd)
    lFecha = pd.read_sql('SELECT `Date` FROM CovidRecovered GROUP BY `Date`', con=connectPd)

    confirmadosLLR = pd.read_sql("""SELECT * FROM CovidRecovered """, con=connectPd)

    confirmadosLLR = confirmadosLLR[confirmadosLLR["Country/Region"] == pais]
    confirmadosLLR = confirmadosLLR[confirmadosLLR["Date"] == fecha]

    mapData = confirmadosLLR[["Lat", "Lon"]].copy()
    mapData = mapData.rename(columns={"Lat": "lat", "Lon": "lon"})
    st.map(mapData, zoom=None)

elif active_tab == "Analisis":
    st.subheader("En esta página se muestran algunos datos interesantes")

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
    st.subheader("Seleccione el caso que desea ver")
    caseOption = st.selectbox("País con mayor cantidad de", cases)

    if caseOption == "Casos confirmados":
        cursor.execute("""SELECT `Country/Region`, SUM(Confirmed) as Tot
                          FROM CovidConfirmed GROUP BY `Country/Region` ORDER BY tot DESC LIMIT 1""")
        confirmed = cursor.fetchall()
        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write("País ---- ", confirmed[0][0])
                st.write("Cantidad de personas ---- ", confirmed[0][1])
            with col2:
                dfMap = pd.read_sql('SELECT * FROM CovidConfirmed', con=connectPd) #---------------
                dfMap = dfMap[dfMap["Country/Region"] == confirmed[0][0]]
                # st.write(dfMap)

                mapData = dfMap[["Lat", "Lon"]].copy()
                mapData = mapData.rename(columns={"Lat": "lat", "Lon": "lon"})
                # st.write(mapData)
                st.map(mapData)

    elif caseOption == "Muertes":
        cursor.execute("""SELECT `Country/Region`, SUM(Deaths) as Tot
                          FROM CovidDeaths GROUP BY `Country/Region` ORDER BY tot DESC LIMIT 1""")
        deaths = cursor.fetchall()
        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write("País ---- ", deaths[0][0])
                st.write("Cantidad de personas ---- ", deaths[0][1])
            with col2:
                dfMap = pd.read_sql('SELECT * FROM CovidDeaths', con=connectPd) #---------------
                dfMap = dfMap[dfMap["Country/Region"] == deaths[0][0]]
                # st.write(dfMap)

                mapData = dfMap[["Lat", "Lon"]].copy()
                mapData = mapData.rename(columns={"Lat": "lat", "Lon": "lon"})
                # st.write(mapData)
                st.map(mapData, zoom=None)

    else:
        cursor.execute("""SELECT `Country/Region`, SUM(Recovered) as Tot
                          FROM CovidRecovered GROUP BY `Country/Region` ORDER BY tot DESC LIMIT 1""")
        recovered = cursor.fetchall()

        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write("País ---- ", recovered[0][0])
                st.write("Cantidad de personas ---- ", recovered[0][1])
            with col2:
                dfMap = pd.read_sql('SELECT * FROM CovidRecovered', con=connectPd) #---------------
                dfMap = dfMap[dfMap["Country/Region"] == recovered[0][0]]
                # st.write(dfMap)

                mapData = dfMap[["Lat", "Lon"]].copy()
                mapData = mapData.rename(columns={"Lat": "lat", "Lon": "lon"})
                # st.write(mapData)
                st.map(mapData)

    st.subheader("Las fechas más fuertes")
    with st.container():
        confirmedFechas = pd.read_sql("""SELECT SUM(Confirmed) as tot, `Date`, `Country/Region`
                                         FROM test.CovidConfirmed
                                         GROUP BY `Date`, `Country/Region`
                                         ORDER BY tot DESC LIMIT 10""", con=connectPd)
        confirmedFechas = confirmedFechas.rename(columns={'tot': 'TOTAL', "Date": "FECHA", "Country/Region": "PAÍS"})
        st.write("Casos confrimados")
        st.table(confirmedFechas)
        recoveredFechas = pd.read_sql("""SELECT SUM(Recovered) as tot, `Date`, `Country/Region`
                                         FROM test.CovidRecovered
                                         GROUP BY `Date`, `Country/Region`
                                         ORDER BY tot DESC LIMIT 10""", con=connectPd)
        recoveredFechas = recoveredFechas.rename(columns={'tot': 'TOTAL', "Date": "FECHA", "Country/Region": "PAÍS"})
        st.write("Casos Recuperados")
        st.table(recoveredFechas)
        deathsssFechas = pd.read_sql("""SELECT SUM(Deaths) as tot, `Date`, `Country/Region`
                                         FROM test.CovidDeaths
                                         GROUP BY `Date`, `Country/Region`
                                         ORDER BY tot DESC LIMIT 10""", con=connectPd)
        deathsssFechas = deathsssFechas.rename(columns={'tot': 'TOTAL', "Date": "FECHA", "Country/Region": "PAÍS"})
        st.write("Casos Fallecidos")
        st.table(deathsssFechas)
else:
    st.error("Something has gone terribly wrong.")


# Close the connection
db.close()
