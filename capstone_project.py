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
# pda = pd.read_csv("File csv dan excel/indonesia_livestock_chicken_202402111419.csv")
# pop_ayam = pda.loc[pda['year_added'] >= 2016]
# Above dataset not used anymore

# 2. populasi masyarakat Indonesia
pmi = pd.read_csv("File csv dan excel/Jumlah Penduduk Indonesia.csv")
pop_manusia = pmi.loc[pmi['Tahun'] >= 2018]

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

# 9. Produksi daging ayam di Indonesia per provinsi
pda2 = pd.read_csv("File csv dan excel/brand_new_produksi_daging_provinsi_indonesia.csv")

# 10. Produksi limbah di Indonesia
pl = pd.read_csv("File csv dan excel/brand_new_limbah.csv")

# 11. Pengeluaran bahan makanan rata-rata di Indonesia
pbm = pd.read_csv("File csv dan excel/brand_new_pengeluaran_bahan_makanan_per_kapita_sebulan_menurut_kelompok_barang.csv")

# 12. Produksi limbah di Indonesia 2
pl2 = pd.read_csv("File csv dan excel/brand_new_limbah2.csv")

# Basic processing if necessary
# 1. Creating a new dataframe for layered chart for I want the legend then change it to long-dataframe format
tahun_pop = pop_manusia['Tahun'].tolist()
jumlah_penduduk = pop_manusia['Jumlah Penduduk'].tolist()
jumlah_ayam = pda2['INDONESIA'].tolist()
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
    title='Perbandingan Populasi Masyarakat dan Produksi Daging Ayam Pedaging di Indonesia'
)

source_total_pop = "SOURCE: Badan Pusat Statistik, 2022 & 2023"
source_chart_total_pop = alt.Chart(pd.DataFrame({'note': [source_total_pop]})).mark_text(
    align='left',
    baseline='top',
    color='gray',
    fontSize=10,
    dx= -90,
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
combined_chart_total_pop = total_pop_line_chart + source_chart_total_pop + points_for_total_pop + tooltips_for_total_pop

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
jumlah_populasi_untuk_konsumsi = jumlah_penduduk[1:]
for i in range(len(jumlah_populasi_untuk_konsumsi)):
    konsumsi_rata_rata_daging_ayam_per_tahun.append(konsumsi_daging_ayam_per_tahun[i] * jumlah_populasi_untuk_konsumsi[i] * 1000)
populasi_ayam_2019_2022 = jumlah_ayam[1:]
produksi_daging_ayam_2019_2022 = []
for i in range(len(populasi_ayam_2019_2022)):
    produksi_daging_ayam_2019_2022.append(populasi_ayam_2019_2022[i] * 1000)
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

def format_other_big_number(number):
    formatted_number = "{:,.0f}".format(number)
    return formatted_number


# 5. Pie Chart for Category food waste in Indonesia
new_psi_column = ['Household Estimate', 'Retail Estimate', 'Food Service Estimate']
jum_food_waste = []
for value in psi.columns.values:
    if value in ["Household estimate (tonnes/year)","Retail estimate (tonnes/year)","Food service estimate (tonnes/year)"]:
        value_for_indonesia = psi.loc[psi['country'] == 'Indonesia', value].values[0]
        jum_food_waste.append(value_for_indonesia)
for_pie_chart_food_waste_dataframe = pd.DataFrame({
    'Category': new_psi_column,
    'Amount': jum_food_waste
})
psi_pie_chart = alt.Chart(for_pie_chart_food_waste_dataframe).encode(
    x=alt.X('Amount:Q', title='Jumlah (kg)'),
    y=alt.Y('Category:N', title='Kategori', sort=alt.SortField(field= 'Amount',order='descending')),
    color=alt.value('lightblue')
).properties(
    title='Kategori Penyumbang Sampah di Indonesia'
)
psi_pie_charted = psi_pie_chart.mark_bar()
psi_pie_text = psi_pie_chart.mark_text(align='left', dx=5).encode(text=alt.Text('Amount:Q'), color=alt.value('black'))

source_total_jum_food_waste = "SOURCE: United Nations Enviromental Program (UNEP), 2021"
source_chart_total_jum_food_waste = alt.Chart(pd.DataFrame({'note': [source_total_jum_food_waste]})).mark_text(
    align='left',
    baseline='top',
    color='gray',
    fontSize=10,
    dx= -130,
    dy= 100
).encode(
    text='note:N',
)
combined_pi_chart_food_waste = psi_pie_charted + source_chart_total_jum_food_waste + psi_pie_text

# 6. Chart Persentase Kenaikan Jumlah Pendapatan
persentase_jumlah_pendapatan = []
tahun_jumlah_pendapatan_baru = [2019, 2020, 2021, 2022, 2023]
for i in range(5):
    pencapaian = (jumpen['INDONESIA'].loc[i+1] - jumpen['INDONESIA'].loc[i])
    persentase_jumlah_pendapatan.append(pencapaian)
pers_jum_pendapatan = pd.DataFrame({
    'Tahun':tahun_jumlah_pendapatan_baru,
    'Kenaikan': persentase_jumlah_pendapatan
})
jumpen_first_row = {'Tahun':'Begin', 'Kenaikan':1638.55}
jumpen_last_row = {'Tahun':'End', 'Kenaikan':0}
jumpen_first_row_df = pd.DataFrame([jumpen_first_row])
jumpen_last_row_df = pd.DataFrame([jumpen_last_row])
source = pd.concat([jumpen_first_row_df, pers_jum_pendapatan,jumpen_last_row_df], ignore_index=True)

# 7. Chart Pendapatan per Kapita di Indonesia
line_chart_pendapatan = alt.Chart(jumpen).mark_line().encode(
    x = alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
    y = alt.Y("INDONESIA:Q" ,scale=alt.Scale(zero=False))
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
).properties(
    title='Jumlah Pendapatan per Kapita di Indonesia'
)
hover_for_total_pendapatan = alt.selection_single(
        fields=["Tahun"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
points_for_total_pendapatan = line_chart_pendapatan.transform_filter(hover_for_total_pendapatan).mark_circle(size=65)
tooltips_for_total_pendapatan = (
        alt.Chart(jumpen)
        .mark_rule()
        .encode(
            x=alt.X('Tahun:N', axis=alt.Axis(labelAngle=0)),
            y=alt.Y("INDONESIA:Q", title='Pendapatan per Kapita (/ribu rupiah)', scale=alt.Scale(zero=False)),
            opacity=alt.condition(hover_for_total_pendapatan, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Tahun", title="Tahun"),
                alt.Tooltip("INDONESIA", title='Pendapatan per Kapita (/ribu rupiah)'),
            ],
        )
        .add_selection(hover_for_total_pendapatan)
    )
new_combine_chart_jumpen = line_chart_pendapatan + source_chart_total_pendapatan + points_for_total_pendapatan + tooltips_for_total_pendapatan

# 8. Making a waterfall chart
def waterfall_chart_jumpen(source):
    base_chart = alt.Chart(source).transform_window(
        window_sum_amount="sum(Kenaikan)",
        window_lead_label="lead(Tahun)",
    ).transform_calculate(
        calc_lead="datum.window_lead_label === null ? datum.Tahun : datum.window_lead_label",
        calc_prev_sum="datum.Tahun === 'End' ? 0 : datum.window_sum_amount - datum.Kenaikan",
        calc_amount="datum.Tahun === 'End' ? datum.window_sum_amount : datum.Kenaikan",
        calc_text_amount="(datum.Tahun !== 'Begin' && datum.Tahun !== 'End' && datum.calc_amount > 0 ? '+' : '') + datum.calc_amount",
        calc_center="(datum.window_sum_amount + datum.calc_prev_sum) / 2",
        calc_sum_dec="datum.window_sum_amount < datum.calc_prev_sum ? datum.window_sum_amount : ''",
        calc_sum_inc="datum.window_sum_amount > datum.calc_prev_sum ? datum.window_sum_amount : ''",
    ).encode(
        x=alt.X(
            "Tahun:O",
            axis=alt.Axis(title="Tahun", labelAngle=0),
            sort=None,
        )
    ).properties(
        title='Rata-rata Pendapatan per Kapita di Indonesia'
    )
    color_coding = {
        "condition": [
            {"test": "datum.Tahun === 'Begin' || datum.Tahun === 'End'", "value": "#878d96"},
            {"test": "datum.calc_amount < 0", "value": "#fa4d56"},
        ],
        "value": "#24a148",
    }
    bar = base_chart.mark_bar(size=45).encode(
        y=alt.Y("calc_prev_sum:Q", title="Pendapatan (/ribu)"),
        y2=alt.Y2("window_sum_amount:Q"),
        color=color_coding,
    )
    rule = base_chart.mark_rule(
        xOffset=-22.5,
        x2Offset=22.5,
    ).encode(
        y="window_sum_amount:Q",
        x2="calc_lead",
    )
    text_pos_values_top_of_bar = base_chart.mark_text(
        baseline="bottom",
        dy=-4
    ).encode(
        text=alt.Text("calc_sum_inc:N", format='.2f'),
        y="calc_sum_inc:Q",
    )
    text_neg_values_bot_of_bar = base_chart.mark_text(
        baseline="top",
        dy=4
    ).encode(
        text=alt.Text("calc_sum_dec:N", format='.2f'),
        y="calc_sum_dec:Q"
    )
    text_bar_values_mid_of_bar = base_chart.mark_text(baseline="middle").encode(
        text=alt.Text("calc_text_amount:N", format='.2f'),
        y="calc_center:Q",
        color=alt.value('black'),
    )
    
    combined = bar + rule + text_pos_values_top_of_bar + text_neg_values_bot_of_bar + text_bar_values_mid_of_bar
    return st.altair_chart(combined, use_container_width=True)

# 9. Making Facet Chart for Pengeluaran File
def facet_chart_pengeluaran(pbm):
    pbm = pbm.loc[pbm['Kelompok Barang'] >= 2019].reset_index(drop=True)
    pbm = pbm.rename(columns={'Kelompok Barang' : 'Tahun'})
    data_melt = pd.melt(
        pbm, 
        id_vars='Tahun',
        value_vars=['Jumlah makanan', 'Jumlah bukan makanan'],
        var_name='kategori',
        value_name='Jumlah Pengeluaran'
    )
    chart = alt.Chart(data_melt).encode(
        x=alt.X('kategori:N', title='Kategori', axis=None),
        y=alt.Y('Jumlah Pengeluaran:Q', title='Jumlah Pengeluaran (%)'),
        color='kategori:N',
        text=alt.Text('Jumlah Pengeluaran:Q', format='.2f')
    ).properties(
        height=100,
        width=60
    )
    text = chart.mark_text(baseline='bottom')
    charted = chart.mark_bar()
    combined = charted + text
    facet_chart = combined.facet(
        facet=alt.Facet('Tahun:O', title='Tahun'),
        columns=3
    ).resolve_scale(y='independent').properties(
        title='Jumlah Pengeluaran per Bulan di Indonesia'
    )
    return st.altair_chart(facet_chart, use_container_width=True)

# 10. Making Facet Chart of Kategori jumlah makanan in pbm file
def facet_chart_jumlah_makanan(pbm):
    columns_to_drop = ['Perumahan dan fasilitas rumahtangga' ,'Barang dan jasa', 'Pakaian, alas kaki dan tutup kepala' ,'Barang-barang tahan lama' ,'Pajak dan asuransi' ,'Keperluan pesta dan upacara' ,'Jumlah makanan' ,'Jumlah bukan makanan']
    pbm = pbm.drop(columns=columns_to_drop)
    pbm = pbm.loc[pbm['Kelompok Barang'] >= 2019].reset_index(drop=True)
    pbm = pbm.rename(columns={'Kelompok Barang' : 'Tahun'})
    data_melt = pd.melt(
        pbm, 
        id_vars='Tahun',
        var_name='kategori',
        value_name='Jumlah Pengeluaran'
    )
    chart = alt.Chart(data_melt).encode(
        y=alt.Y('kategori:N', title='Kategori', sort=alt.SortField(field='Jumlah Pengeluaran', order='descending')),
        x=alt.X('Jumlah Pengeluaran:Q', title='Jumlah Pengeluaran (%)'),
        color=alt.condition(
            alt.datum.kategori == 'Daging',
            alt.value('steelblue'),
            alt.value('lightblue')
        ),
        text=alt.condition(
            alt.datum.kategori == 'Daging',
            alt.Text('Jumlah Pengeluaran:Q', format='.2f' ),
            alt.value('')
        )
    )
    charted = chart.mark_bar()
    text = chart.mark_text(align='left', dx=5)
    combined = charted + text
    facet_chart = combined.facet(
        facet=alt.Facet('Tahun:O', title='Tahun'),
        columns=2
    ).resolve_scale(y='independent', x='independent').properties(
        title='Persentasi Pengeluaran Khusus Makanan per Bulan di Indonesia'
    )

    return st.altair_chart(facet_chart, use_container_width=True)
 
# 11. Making bar chart for waste
bar_chart_kategori = alt.Chart(pl2).encode(
    x=alt.X('Sampah Dikumpulkan (Kg):Q'),
    y=alt.Y('Kategori:N', sort=alt.SortField(field='Sampah Dikumpulkan (Kg)', order='descending'), title='Kategori Sampah'),
    color=alt.condition(
        alt.datum['Kategori'] == 'SISA MAKANAN',
        alt.value('steelblue'),
        alt.value('lightblue')
    ),
    text=alt.condition(
        alt.datum['Kategori'] == 'SISA MAKANAN',
        'Sampah Dikumpulkan (Kg):Q',
        alt.value('')
    )
).properties(
    title='Kategori sampah yang terkumpul di Indonesia'
)
bar_charted_kategori = bar_chart_kategori.mark_bar()
bar_text_kategori = bar_chart_kategori.mark_text(align='left', dx=5)
source_total_waste = "SOURCE: Sistem Informasi Dirjen PSLB3, 2023"
source_chart_total_waste = alt.Chart(pd.DataFrame({'note': [source_total_waste]})).mark_text(
    align='left',
    baseline='top',
    color='gray',
    fontSize=10,
    dx= -95,
    dy= 200
).encode(
    text='note:N',
)
combined_waste_chart = bar_charted_kategori + source_chart_total_waste + bar_text_kategori



# Start writing
st.title('KECUKUPAN DAGING AYAM DI INDONESIA')
st.header('1. Keadaan Produksi Daging Ayam di Indonesia')
st.write("""
         Daging ayam merupakan sumber protein hewani yang umum dikonsumsi oleh rakyat Indonesia. 
         Seiring dengan pertumbuhan penduduk yang pesat dengan kesadaran yang tinggi tentang pentingnya 
         protein hewani, maka perlu diimbangi dengan penyediaannya.
         """)
st.write('')

column1, column2 = st.columns(2)
with column1:
    st.altair_chart(combined_chart_total_pop, use_container_width=True)
with column2:
    st.altair_chart(combined_total_jum_konsumsi, use_container_width=True)
column3, column4 = st.columns(2)
with column3:
    st.altair_chart(combined_chart_for_surplus, use_container_width=True)
with column4:
    st.write('')
    st.write('')
    st.write('')
    st.write('''
             Dapat kita simpulkan pada 3 diagram tersebut bahwa jumlah populasi ayam hidup jauh lebih
             banyak dibandingkan dengan jumlah populasi manusia. Produksi daging ayam di Indonesia
             jauh melebihi konsumsi masyarakat Indonesia, yang menghasilkan surplus daging ayam yang dapat
             diekspor maupun diolah kedalam bentuk makanan lainnya.
             ''')

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
    
st.write('')
st.write('Apakah ada keterkaitannya dengan harga daging ayam dan jumlah sampah makanan yang terbuang di Indonesia?')
st.write('')

st.header('2. Harga Daging Ayam di Indonesia')
st.write('')
st.write('')
st.write('')

waterfall_chart_jumpen(source)
st.write('')
st.write('')
column8, column9=st.columns(2)
with column8:
    facet_chart_pengeluaran(pbm)
    st.markdown('<span style="color: grey">SOURCE: Badan Pusat Statistika, 2023</span>', unsafe_allow_html=True)
with column9:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('''
             Masyarakat Indonesia lebih terlihat seimbang dalam pengeluarannya terkait kategori
             jumlah pengeluarannya. Akan tetapi, kategori pengeluaran bukan makanan lebih besar sedikit
             dibandingkan dengan kategori pengeluaran makanan tiap tahunnya.
             ''')

with st.expander('Tekan untuk melihat perbandingan beberapa bahan makanan'):
    st.write('')
    facet_chart_jumlah_makanan(pbm)
    st.markdown('<span style="color: grey">SOURCE: Badan Pusat Statistika, 2023</span>', unsafe_allow_html=True)

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
st.altair_chart(combined_chart_harga_daging_ayam, use_container_width=True)

cols2 = st.columns(3)
with cols2[1]:
    st.metric("**Rata-rata Harga Daging Ayam Terbaru per Tahun di Indonesia**", 
                value=f'Rp {format_other_big_number(hdgpt["Indonesia"].iloc[-1])}',
                delta=f'{format_big_number((hdgpt["Indonesia"].iloc[-1]) - (hdgpt["Indonesia"].iloc[-2]))}')    

st.write('')
st.write('')
st.write('''
         Harga ayam per bulannya mengalami kenaikan dan penurunan yang fluktuatif, namun harga berada di range yang tidak berubah.
         Dapat dilihat bahwa harga daging ayam di Indonesia kerap berada di jangkauan 35rb - 40rb rupiah.
         ''')

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
psi_bar_chart = alt.Chart(y_scale_psi).encode(
    y=alt.Y('country:N', sort=alt.SortField(field=f'{selected_option_for_food_waste}', order='descending'), title='Negara'),
    x=alt.X(f'{selected_option_for_food_waste}'),
    color = highlight_color_psi,
    text = alt.condition(
        alt.datum['country'] == 'Indonesia',
        f'{selected_option_for_food_waste}:Q',
        alt.value('')
    )
)
psi_charted = psi_bar_chart.mark_bar()
psi_text = psi_bar_chart.mark_text(align='left', dx=5)
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
combined_bar_Chart_food_waste = psi_charted + psi_text + source_chart_total_jum_food_waste_bar
st.altair_chart(combined_bar_Chart_food_waste, use_container_width=True)

column7, column8 = st.columns(2)
with column7:
    st.altair_chart(combined_pi_chart_food_waste, use_container_width=True)
with column8:
    st.write('')
    st.write('')
    st.write('''
             Indonesia merupakan negara penyumbang sampah nomor 4 terbesar di dunia. Sampah rumah tangga merupakan produsen sampah yang
             terbanyak. Bahan pangan yang berjamur, basi, membuang makanan yang eksesif, dan ketidak-pedulian terhadap sampah makanan
             dapat menambah jumlah produksi sampah di Indonesia.
             ''')

st.altair_chart(combined_waste_chart, use_container_width=True)
st.write('')
st.write('Sampah sisa makanan sebesar 1,7 juta kg, jika sebelum dibuang, berjamur, dll, ketika dipertahankan kesegarannya maupun diolah kedalam makanan jadi yang lain. Dapat menaikkan angka zero hunger goal di Indonesia')

st.header('4. Kesimpulan dan Saran')
st.write('''
         Masyarakat Indonesia mampu untuk membeli bahan makanan berupa daging. Akan tetapi untuk tahun ini juga masyarakat mementingkan
         pembelian bukan makanan. Pada saat membeli makanan pun, masyarakat lebih mementingkan membeli makanan jadi. Bisa disimpulkan bahwa
         harga daging ayam bukanlah salah satu alasan mengapa masih ada kelaparan di Indonesia
         ''')
st.write('''
         Pembuangan sampah bahan organik dapat mempengaruhi angka kelaparan. Sebaiknya, pemberitahuan dan pendidikan tentang sampah organik dan anorganik, khususnya
         cara untuk mempertahankan kesegaran daging ayam, harus disosialisasikan kepada masyarakat umum.
         Hal ini dapat membuat jumlah sampah yang terbuang di Indonesia berkurang.
         ''')
