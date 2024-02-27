# import libraries
import streamlit as st
import pandas as pd
import altair as alt

# Page Layout setup
st.set_page_config(
    page_title = 'Daging Ayam di Indonesia',
    page_icon='📒',
    layout='wide'
)

# Calling data
# 1. populasi ayam
pda = pd.read_csv("File csv dan excel/indonesia_livestock_chicken_202402111419.csv")
pop_ayam = pda.loc[pda['year_added'] >= 2016]

# 2. populasi masyarakat Indonesia
pmi = pd.read_csv("File csv dan excel/Jumlah Penduduk Indonesia.csv")

# 3. rata-rata konsumsi masyarakat Indonesia per Kapita
rk = pd.read_csv("File csv dan excel/Rata-Rata Konsumsi Sampai 2023.csv")

# 4. SDG kelaparan di Indonesia
ski = pd.read_csv("File csv dan excel/sdg_indonesia_202402151955.csv")

# 5. harga daging ayam per bulan di Indonesia
hdg = pd.read_csv("File csv dan excel/brand_new_harga_ayam.csv")

# 6 . jumlah pendapatan masyarakat Indonesia
jumpen = pd.read_csv("File csv dan excel/brand_new_pendapatan_indonesia_per_tahun.csv")

# 7. harga_daging_ayam_per_tahun
hdgpt = pd.read_csv("File csv dan excel/harga_daging_ayam_per_tahun.csv")

# 8. produksi_sampah_di_Indonesia
psi = pd.read_csv("File csv dan excel/food_waste_data_and_research_202402042350.csv")

# Basic processing if necessary
# 1. Creating a new dataframe for layered chart for I want the legend then change it to long-dataframe format
tahun_pop = pmi['Tahun'].tolist()
jumlah_penduduk = pmi['Jumlah Penduduk'].tolist()
jumlah_ayam = pop_ayam['value'].tolist()
total_pop = pd.DataFrame({
    'Tahun':tahun_pop,
    'Jumlah Penduduk':jumlah_penduduk,
    'Jumlah Ayam':jumlah_ayam
})
data_long_for_total_pop = pd.melt(
    total_pop, 
    id_vars='Tahun',
    value_vars=['Jumlah Penduduk', 'Jumlah Ayam'],
    var_name='category',
    value_name='total_manusia_dan_ayam'
)
total_pop_line_chart = alt.Chart(data_long_for_total_pop).mark_line().encode(
    x=alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('total_manusia_dan_ayam:Q', title='Jumlah/1000 satuan', scale=alt.Scale(zero=False)),
    color='category:N'
).properties(
    title='Perbandingan Populasi Masyarakat dan Ayam di Indonesia'
)
note_text = "Rata-rata bobot ayam ketika dipanen adalah 0,7-2,0 kg (Nurjannah N., 2020)"
source_total_pop = "SOURCE: Food And Agriculture Orgnization of the United Nations, 2023; Badan Pusat Statistik, 2023"
note_layer = alt.Chart(pd.DataFrame({'note': [note_text]})).mark_text(
    align='left',
    baseline='middle',
    fontSize=10,
    fontWeight='normal',
    dx=-150,
    dy=45,
    color='gray'
).encode(
    text='note:N'
)
source_chart_total_pop = alt.Chart(pd.DataFrame({'note': [source_total_pop]})).mark_text(
    align='left',
    baseline='top',
    color='gray',
    fontSize=10,
    dx= -200,
    dy= 175
).encode(
    text='note:N',
)
hover_for_total_pop = alt.selection_single(
        fields=["Tahun"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
points_for_total_pop = total_pop_line_chart.transform_filter(hover_for_total_pop).mark_circle(size=65)
tooltips_for_total_pop = (
        alt.Chart(data_long_for_total_pop)
        .mark_rule()
        .encode(
            x=alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('total_manusia_dan_ayam:Q', title='Jumlah/1000 satuan', scale=alt.Scale(zero=False)),
            opacity=alt.condition(hover_for_total_pop, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Tahun", title="Tahun"),
                alt.Tooltip("total_manusia_dan_ayam", title="Jumlah manusia atau ayam hidup"),
            ],
        )
        .add_selection(hover_for_total_pop)
    )
combined_chart_total_pop = total_pop_line_chart + note_layer + source_chart_total_pop + points_for_total_pop + tooltips_for_total_pop

# 2. Creating a new dataframe for 'rata-rata konsumsi' for easy chart-making
jum_konsumsi = []
tahun_jum_konsumsi = rk.columns.values[2:].tolist()
for year in rk.columns.values[2:]:
    jum_konsumsi.append(rk[year].values[0]*52)
konsumsi_daging_ayam = pd.DataFrame({
    'Tahun': tahun_jum_konsumsi,
    'Konsumsi(kg)': jum_konsumsi
})
konsumsi_line_chart = alt.Chart(konsumsi_daging_ayam).mark_line().encode(
    x=alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Konsumsi(kg):Q', scale=alt.Scale(zero=False))
).properties(
    title='Jumlah Konsumsi Daging Ayam per Kapita di Indonesia'
)
source_total_jum_konsumsi = "SOURCE: Badan Pusat Statistik, 2023"
source_chart_total_jum_konsumsi = alt.Chart(pd.DataFrame({'note': [source_total_jum_konsumsi]})).mark_text(
    align='left',
    baseline='top',
    color='gray',
    fontSize=10,
    dx= -80,
    dy= 175
).encode(
    text='note:N',
)
hover_for_total_jum_konsumsi = alt.selection_single(
        fields=["Tahun"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
points_for_total_jum_konsumsi = konsumsi_line_chart.transform_filter(hover_for_total_jum_konsumsi).mark_circle(size=65)
tooltips_for_total_jum_konsumsi = (
        alt.Chart(konsumsi_daging_ayam)
        .mark_rule()
        .encode(
            x=alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Konsumsi(kg):Q', scale=alt.Scale(zero=False)),
            opacity=alt.condition(hover_for_total_jum_konsumsi, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Tahun", title="Tahun"),
                alt.Tooltip("Konsumsi(kg)", title="Konsumsi(kg)"),
            ],
        )
        .add_selection(hover_for_total_jum_konsumsi)
    )
combined_total_jum_konsumsi = konsumsi_line_chart + source_chart_total_jum_konsumsi + points_for_total_jum_konsumsi + tooltips_for_total_jum_konsumsi

# 3. Creating a new dataframe and line chart for 'surplus konsumsi daging ayam'
konsumsi_daging_ayam_per_tahun = jum_konsumsi[:4]
konsumsi_rata_rata_daging_ayam_per_tahun = []
jumlah_populasi_untuk_konsumsi = jumlah_penduduk[3:]
for i in range(len(jumlah_populasi_untuk_konsumsi)):
    konsumsi_rata_rata_daging_ayam_per_tahun.append(konsumsi_daging_ayam_per_tahun[i] * jumlah_populasi_untuk_konsumsi[i] * 1000)
populasi_ayam_2019_2022 = jumlah_ayam[3:]
produksi_daging_ayam_2019_2022 = []
for i in range(len(populasi_ayam_2019_2022)):
    produksi_daging_ayam_2019_2022.append(populasi_ayam_2019_2022[i] * 1000 * 0.7)
tahun_konsumsi = []
for year in range(2019, 2023):
    tahun_konsumsi.append(year)
konsumsi_produksi_daging_2019_2022 = []
for i in range(4):
    konsumsi_produksi_daging_2019_2022.append(produksi_daging_ayam_2019_2022[i] - konsumsi_rata_rata_daging_ayam_per_tahun[i])
surplus_dataframe = pd.DataFrame({
    'Tahun' : tahun_konsumsi,
    'Surplus(kg)' : konsumsi_produksi_daging_2019_2022
})
surplus_line_chart = alt.Chart(surplus_dataframe).mark_line().encode(
    x = alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
    y = alt.Y('Surplus(kg):Q', scale=alt.Scale(zero=False))
).properties(
    title='Surplus Konsumsi Daging Ayam di Indonesia'
)
hover_for_surplus = alt.selection_single(
        fields=["Tahun"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
points_for_surplus = surplus_line_chart.transform_filter(hover_for_surplus).mark_circle(size=65)
tooltips_for_surplus = (
        alt.Chart(surplus_dataframe)
        .mark_rule()
        .encode(
            x=alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Surplus(kg):Q', scale=alt.Scale(zero=False)),
            opacity=alt.condition(hover_for_surplus, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Tahun", title="Tahun"),
                alt.Tooltip("Surplus(kg)", title="Surplus(kg)"),
            ],
        )
        .add_selection(hover_for_surplus)
    )
combined_chart_for_surplus = surplus_line_chart + points_for_surplus + tooltips_for_surplus

# 4. Creating matrix for SGD Number 2 in Indonesia
# helper function
def format_big_number(num):
    if num >= 1e6:
        return f"{num / 1e6:.2f} Mio"
    elif num >= 1e3:
        return f"{num / 1e3:.3f}"
    else:
        return f"{num:.2f}"
CURR_SCORE = ski.loc[ski['year_added'] == 2023, 'goal_2_score'].values[0]
PERV_SCORE = ski.loc[ski['year_added'] == 2022, 'goal_2_score'].values[0]

# 5. Pie Chart for Category food waste in Indonesia
new_psi_column = ['Household Estimate', 'Retail Estimate', 'Food Service Estimate']
jum_food_waste = []
for value in psi.columns.values:
    if value in ["Household estimate (tonnes/year)","Retail estimate (tonnes/year)","Food service estimate (tonnes/year)"]:
        value_for_indonesia = psi.loc[psi['country'] == 'Indonesia', value].values[0]
        jum_food_waste.append(value_for_indonesia)
for_pie_chart_food_waste_dataframe = pd.DataFrame({
    'Category': new_psi_column,
    'Value (tonnes/year)': jum_food_waste 
})
psi_pie_chart = alt.Chart(for_pie_chart_food_waste_dataframe).mark_arc().encode(
    theta='Value (tonnes/year)',
    color='Category'
).properties(
    title='Kategori Penyumbang Sampah di Indonesia'
)
source_total_jum_food_waste = "SOURCE: United Nations Enviromental Program (UNEP), 2021"
source_chart_total_jum_food_waste = alt.Chart(pd.DataFrame({'note': [source_total_jum_food_waste]})).mark_text(
    align='left',
    baseline='top',
    color='gray',
    fontSize=10,
    dx= -130,
    dy= 175
).encode(
    text='note:N',
)
combined_pi_chart_food_waste = psi_pie_chart + source_chart_total_jum_food_waste

# 6. Persentase Jumlah Pendapatan dengan Jumlah Konsumsi per Kapita di Indonesia
persentase_jumlah_konsumsi = []
tahun_jumlah_konsumsi_baru = [2020, 2021, 2022, 2023]
persentase_jumlah_pendapatan = []
tahun_jumlah_pendapatan_baru = [2019, 2020, 2021, 2022, 2023]
for i in range(4):
    column_name_current = rk.columns[i+2]
    column_name_next = rk.columns[i+3]
    percentage = (rk[column_name_next].values[0] - rk[column_name_current].values[0]) / rk[column_name_current].values[0]
    persentase_jumlah_konsumsi.append(percentage)
for i in range(5):
    percentage = (jumpen['INDONESIA'].loc[i+1] - jumpen['INDONESIA'].loc[i]) / jumpen['INDONESIA'].loc[i]
    persentase_jumlah_pendapatan.append(percentage)
pers_jum_konsumsi = pd.DataFrame({
    'Tahun':tahun_jumlah_konsumsi_baru,
    'Persentase (%)': persentase_jumlah_konsumsi
})
pers_jum_pendapatan = pd.DataFrame({
    'Tahun':tahun_jumlah_pendapatan_baru,
    'Persentase (%)': persentase_jumlah_pendapatan
})
pers_jum_konsumsi_line_chart = alt.Chart(pers_jum_konsumsi).mark_line().encode(
    x=alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Persentase (%):Q', scale=alt.Scale(zero=False))
).properties(
    title='Perbandingan persentase jumlah konsumsi dan jumlah pendapatan setiap tahun'
)
pers_jum_pendapatan_line_chart = alt.Chart(pers_jum_pendapatan).mark_line(color='green').encode(
    x=alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Persentase (%):Q', scale=alt.Scale(zero=False))
).properties(
    title='Perbandingan persentase jumlah konsumsi dan jumlah pendapatan setiap tahun'
)
note_jum_konsumsi = 'Persentase Jumlah Konsumsi Daging Ayam'
note_jum_pendapatan = 'Persentase Jumlah Pendapatan'
label_pers_jum_konsumsi = alt.Chart(pd.DataFrame({'note':[note_jum_konsumsi]})).mark_text(
    align='left',
    baseline='middle',
    fontSize=10,
    fontWeight='normal',
    dy=30,
    dx=390,
    color='steelblue'
    ).encode(
        text='note:N'
)
label_pers_jum_pendapatan = alt.Chart(pd.DataFrame({'note':[note_jum_pendapatan]})).mark_text(
    align='left',
    baseline='middle',
    fontSize=10,
    fontWeight='normal',
    dy=-25,
    dx=390,
    color='green'
    ).encode(
        text='note:N'
)
combined_chart_for_pers_jum = pers_jum_konsumsi_line_chart + pers_jum_pendapatan_line_chart + label_pers_jum_konsumsi + label_pers_jum_pendapatan

# Start writing
st.title('KECUKUPAN DAGING AYAM DI INDONESIA')
st.header('1. Keadaan Produksi Daging Ayam di Indonesia')
st.write("""
         Daging ayam merupakan sumber protein hewani yang umum dikonsumsi oleh rakyat Indonesia. 
         Seiring dengan pertumbuhan penduduk yang pesat dengan kesadaran yang tinggi tentang pentingnya 
         protein hewani, maka perlu diimbangi dengan penyediaannya.
         """)
st.write('''
         Dapat kita simpulkan pada 3 diagram tersebut bahwa jumlah populasi ayam hidup jauh lebih
         banyak dibandingkan dengan jumlah populasi manusia. Produksi daging ayam di Indonesia
         jauh melebihi konsumsi masyarakat Indonesia, yang menghasilkan surplus daging ayam yang dapat
         diekspor maupun diolah kedalam bentuk makanan lainnya.
             ''')
st.write('')

column1, column2 = st.columns(2)
with column1:
    st.altair_chart(combined_chart_total_pop, use_container_width=True)
with column2:
    st.altair_chart(combined_total_jum_konsumsi, use_container_width=True)
column3, column4 = st.columns(2)

st.altair_chart(combined_chart_for_surplus, use_container_width=True)

st.markdown("**Namun...**")

tab1, tab2, tab3 = st.tabs(["Gambar 1", "Gambar 2", "Gambar 3"])
with tab1:
    st.image('File csv dan excel/Foto-foto untuk report/Kelaparan 1.PNG', caption='Kompas, 2023')
with tab2:
    st.image('File csv dan excel/Foto-foto untuk report/Kelaparan 2.PNG', caption='CNBC, 2023')
with tab3:
    st.image('File csv dan excel/Foto-foto untuk report/Kelaparan 3.PNG', caption='Tempo, 2023')
    
column5, column6 = st.columns(2)
with column5:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('Surplus daging ayam cukup tinggi, tapi masih ada kelaparan di Indonesia?')
with column6:
    st.write('')
    st.write('')
    st.metric("**Zero Hunger Goal in Indonesia**", value=f'{format_big_number(CURR_SCORE)}%', delta=f'{(CURR_SCORE - PERV_SCORE):.2f}')

st.header('2. Pendapatan Masyarakat Indonesia')
st.write('')
st.write('')
st.write('')


selected_countries = st.multiselect('Select provinces to compare:', hdg.columns[1:].tolist(), ['INDONESIA'])
color_scale = alt.Scale(domain=selected_countries, range='category')

# Processing for interactive chart harga_daging_ayam
hdg['Bulan'] = pd.to_datetime(hdg['Bulan'], format='%b-%y') + pd.offsets.MonthBegin(0)
data_long_for_harga_daging_ayam = pd.melt(hdg, id_vars=['Bulan'], var_name='Nama Provinsi', value_name='provinsi_indonesia')
hdg_line_chart = alt.Chart(data_long_for_harga_daging_ayam).mark_line().encode(
    x='Bulan:T',
    y=alt.Y('provinsi_indonesia:Q', title='Harga Daging Ayam', scale=alt.Scale(zero=False)),
    color=alt.Color('Nama Provinsi:N', legend=None, scale=color_scale)
).properties(
    title='Harga Daging Ayam per Bulan di Beberapa Provinsi di Indonesia'
)
label_harga_daging_ayam = alt.Chart(data_long_for_harga_daging_ayam).mark_text(align='left', dx=3).encode(
    x = alt.X('Bulan:T', aggregate='max', title='Bulan'),
    y = alt.Y('provinsi_indonesia:Q', title='Harga Daging Ayam', aggregate={'argmax':'Bulan'}),
    text = alt.Text('Nama Provinsi'),
    color = alt.Color('Nama Provinsi:N' ,legend=None)
)
source_harga_daging_ayam = "SOURCE: Badan Pangan Nasional, 2024"
source_chart_harga_daging_ayam = alt.Chart(pd.DataFrame({'note': [source_harga_daging_ayam]})).mark_text(
    align='left',
    baseline='top',
    color='gray',
    fontSize=10,
    dx= -80,
    dy= 175
).encode(
    text='note:N',
)
hover_for_harga_daging_ayam = alt.selection_single(
        fields=["Bulan"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
points_for_harga_daging_ayam = hdg_line_chart.transform_filter(hover_for_harga_daging_ayam).mark_circle(size=65)
tooltips_for_harga_daging_ayam = (
        alt.Chart(data_long_for_harga_daging_ayam)
        .mark_rule()
        .encode(
            x='Bulan:T',
            y=alt.Y('provinsi_indonesia:Q', title='Harga Daging Ayam', scale=alt.Scale(zero=False)),
            opacity=alt.condition(hover_for_harga_daging_ayam, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Bulan", title="Bulan"),
                alt.Tooltip('provinsi_indonesia', title='Harga Daging Ayam'),
            ],
        )
        .add_selection(hover_for_harga_daging_ayam)
    )
combined_chart_harga_daging_ayam = hdg_line_chart + label_harga_daging_ayam + source_chart_harga_daging_ayam

# Processing for interactive chart jumlah_pendapatan
data_long_for_jumpen = pd.melt(jumpen, id_vars=['Tahun'], var_name='Nama Provinsi', value_name='provinsi_indonesia')
jumpen_line_chart = alt.Chart(data_long_for_jumpen).mark_line().encode(
    x=alt.X('Tahun:N',axis=alt.Axis(labelAngle=0)),
    y=alt.Y('provinsi_indonesia:Q', title='Pendapatan per Kapita (/ribu rupiah)', scale=alt.Scale(zero=False)),
    color=alt.Color('Nama Provinsi:N', legend=None, scale=color_scale)
).properties(
    title='Jumlah Pendapatan per Kapita Masyarakat Indonesia di Beberapa Provinsi di Indonesia'
)
label_jumpen = alt.Chart(data_long_for_jumpen).mark_text(align='left', dx=3).encode(
    x=alt.X('Tahun:N', aggregate='max', title='Tahun'),
    y=alt.Y('provinsi_indonesia:Q', title='Pendapatan per Kapita (/ribu rupiah)', aggregate={'argmax':'Tahun'}),
    color=alt.Color('Nama Provinsi:N', legend=None),
    text=alt.Text('Nama Provinsi')
)
source_total_pendapatan = "SOURCE: Badan Pusat Statistik, 2023"
source_chart_total_pendapatan = alt.Chart(pd.DataFrame({'note': [source_total_pendapatan]})).mark_text(
    align='left',
    baseline='top',
    color='gray',
    fontSize=10,
    dx= -80,
    dy= 175
).encode(
    text='note:N',
)
hover_for_total_pendapatan = alt.selection_single(
        fields=["Tahun"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
points_for_total_pendapatan = jumpen_line_chart.transform_filter(hover_for_total_pendapatan).mark_circle(size=65)
tooltips_for_total_pendapatan = (
        alt.Chart(data_long_for_jumpen)
        .mark_rule()
        .encode(
            x=alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('provinsi_indonesia:Q', title='Pendapatan per Kapita (/ribu rupiah)', scale=alt.Scale(zero=False)),
            opacity=alt.condition(hover_for_total_pendapatan, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Tahun", title="Tahun"),
                alt.Tooltip('provinsi_indonesia', title='Pendapatan per Kapita (/ribu rupiah)'),
            ],
        )
        .add_selection(hover_for_total_pendapatan)
    )
combine_chart_jumpen = jumpen_line_chart + label_jumpen + source_chart_total_pendapatan

column7, column8 = st.columns(2)
with column7:
    st.altair_chart(combined_chart_harga_daging_ayam, use_container_width=True)
with column8:
    st.altair_chart(combine_chart_jumpen, use_container_width=True)

column9, column10 = st.columns(2)
with column9:
    st.metric("**Rata-rata Harga Daging Ayam Terbaru per Tahun di Indonesia**", 
              value=f'Rp {format_big_number(hdgpt["Indonesia"].iloc[-1])}', 
              delta=f'{format_big_number((hdgpt["Indonesia"].iloc[-1]) - (hdgpt["Indonesia"].iloc[-2]))}')
with column10:
    st.metric('**Rata-rata Pendapatan Masyarakat Terbaru per Kapita di Indonesia (/ribu rupiah)**',
              value=f'Rp {jumpen["INDONESIA"].iloc[-1]}',
              delta=f'{format_big_number((jumpen["INDONESIA"].iloc[-1]) - (jumpen["INDONESIA"].iloc[-2]))}')
st.write('')
st.write('')
st.write('''
         Harga ayam per bulannya mengalami kenaikan dan penurunan yang fluktuatif, namun harga berada di range yang tidak berubah.
         Dapat dilihat bahwa harga daging ayam di Indonesia bagian barat berada di rentang 35rb/kg kebawah, sedangkan di Indonesia bagian timur
         harga daging ayam dapat mencapai 50rb/kg yang berada di wilayah Papua. Perbedaan harga ini dapat terjadi
         karena perbedaan produksi ayam hidup di wilayah tersebut. Ketika produksi ayam hidup kecil, maka
         produksi daging ayam pun akan kecil, sehingga untuk mencukupi konsumsi daging ayam harus membeli
         dari wilayah lain dengan harga yang tinggi. Harga dapat naik akibat dari biaya transportasinya.
         ''')
st.write('''
         Ketika jumlah pendapatan penduduk meningkat, jumlah konsumsi daging ayam pun ikut meningkat. Begitu juga sebaliknya,
         ketika pendapatan menurun, maka jumlah konsumsi daging ayam ikut menurun. Akan tetapi, pada tahun 2021 - 2022. Peningkatan jumlah pendapatan
         yang besar, membuat masyarakat menabung dan membeli barang atau bahan pangan yang lain, sehingga membuat konsumsi daging ayam
         pada tahun itu menurun.
         ''')
st.altair_chart(combined_chart_for_pers_jum, use_container_width=True)

st.header('3. Produksi Sampah di Indonesia')
st.write('')
st.write('**Estimasi Produksi Sampah**')

# Processing radio option for food waste bar chart
options_for_food_waste = ['Household estimate (tonnes/year)', 'Retail estimate (tonnes/year)', 'Food service estimate (tonnes/year)']
selected_option_for_food_waste = st.radio('**Silahkan Pilih dari Opsi Berikut:**', options_for_food_waste)
psi_sorted = psi.sort_values(by=f'{selected_option_for_food_waste}', ascending=False)
y_scale_psi = psi_sorted.reset_index(drop=True).loc[0:9]
highlight_color_psi = alt.condition(
    alt.datum['country'] == 'Indonesia',
    alt.value('steelblue'),
    alt.value('lightblue')
)
psi_bar_chart = alt.Chart(y_scale_psi).mark_bar().encode(
    y=alt.Y('country:N', sort=alt.SortField(field=f'{selected_option_for_food_waste}', order='descending'), title='Negara'),
    x=alt.X(f'{selected_option_for_food_waste}'),
    color = highlight_color_psi
)
source_total_jum_food_waste_bar = "SOURCE: United Nations Enviromental Program (UNEP), 2021"
source_chart_total_jum_food_waste_bar = alt.Chart(pd.DataFrame({'note': [source_total_jum_food_waste_bar]})).mark_text(
    align='left',
    baseline='top',
    color='gray',
    fontSize=10,
    dx= -130,
    dy= 175
).encode(
    text='note:N',
)
combined_bar_Chart_food_waste = psi_bar_chart + source_chart_total_jum_food_waste_bar
st.altair_chart(combined_bar_Chart_food_waste, use_container_width=True)

column11, column12 = st.columns(2)
with column11:
    st.altair_chart(combined_pi_chart_food_waste, use_container_width=True)
with column12:
    st.write('')
    st.write('')
    st.write('''
             Indonesia merupakan negara penyumbang sampah nomor 4 terbesar di dunia. Sampah rumah tangga merupakan produsen sampah yang
             terbanyak. Bahan pangan yang berjamur, basi, membuang makanan yang eksesif, dan ketidak-pedulian terhadap sampah makanan
             dapat menambah jumlah produksi sampah di Indonesia.
             ''')
    
st.header('4. Kesimpulan dan Saran')
st.write('''
         Produksi ayam hidup yang tinggi, akan membuat produksi daging ayam juga akan tinggi. Harapannya seperti itu,
         namun penurunan berat ayam saat transportasi, daging yang berjamur, daging yang kurang layak dikonsumsi,
         dan penduduk yang tidak peduli pada sampah organik dapat membuat jumlah daging ayam yang sebenarnya
         berada di tangan masyarakat akan lebih sedikit.
         ''')
st.write('''
         Pemerataan harga daging ayam harus diberlakukan. Akan tetapi harus diikuti dengan
         pemerataan pembangunan dan pendidikan dari program pemerintah. Hal ini diharapkan akan
         menyamakan harga daging ayam di setiap wilayahnya dan dapat meningkatkan produksi daging ayam nasional.
         ''')
st.write('''
         Selain itu, pemberitahuan dan pendidikan tentang sampah organik dan anorganik, khususnya
         cara untuk mempertahankan kesegaran daging ayam, harus disosialisasikan kepada masyarakat umum.
         Hal ini dapat membuat jumlah sampah yang terbuang di Indonesia berkurang.
         ''')
