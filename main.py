import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots #2軸


st.set_page_config(page_title='merket_condition')
st.markdown('#### 市況情報')

def miyagi():
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdArea=04000&cdTab=18&cdCat01=12%2C15&cdCat02=12%2C13&appId=&lang=J&statsDataId=0003114535&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = st.secrets['PRIVATE']['appId'] #.streamlit\secret.tmolから参照

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    #csvファイルの取得＋df化
    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    #metaデータと本データの切れ目に'VALUE'がある
    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    #カラムの絞込み
    df_val2 = df_val[['時間軸(月次)', 'value']]

    #data型の変換
    df_val2['時間軸(月次)'] = pd.to_datetime(df_val2['時間軸(月次)'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('int')

    #'時間軸(月次)'でgroupby
    s_val2 = df_val2.groupby('時間軸(月次)')['value'].sum()

    #*******可視化
    #月単位
    #グラフを描くときの土台となるオブジェクト
    fig = go.Figure()
    #今期のグラフの追加

    fig.add_trace(
        go.Scatter(
            x=s_val2.index,
            y=s_val2,
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='宮城'
            )
    )

    #レイアウト設定     
    fig.update_layout(
        title='着工数　月',
        showlegend=True #凡例表示
    )
    st.plotly_chart(fig, use_container_width=True) 
        #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

    #月単位　直近1年
    #グラフを描くときの土台となるオブジェクト
    fig2 = go.Figure()
    #今期のグラフの追加

    fig2.add_trace(
        go.Scatter(
            x=s_val2[-13:].index,
            y=s_val2[-13:],
            mode = 'lines+markers+text', #値表示
            text=s_val2[-13:],
            textposition="top center",
            name='宮城'
            )
    )

    #レイアウト設定     
    fig2.update_layout(
        title='着工数 月/直近1年',
        showlegend=True #凡例表示
    )
    st.plotly_chart(fig2, use_container_width=True) 
        #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    
    #年単位
    df_val2['year'] = df_val2['時間軸(月次)'].apply(lambda x: x.year)
    val2_year = df_val2.groupby('year')['value'].sum()

    #グラフを描くときの土台となるオブジェクト
    fig3 = go.Figure()
    #今期のグラフの追加

    fig3.add_trace(
        go.Scatter(
            x=val2_year.index,
            y=val2_year,
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='宮城（年単位）'
            )
    )

    #レイアウト設定     
    fig3.update_layout(
        title='着工数 年',
        showlegend=True #凡例表示
    )
    st.plotly_chart(fig3, use_container_width=True) 
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

    #******************景気ウォッチャー調査
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdTab=140&cdCat01=100&cdCat02=100&cdArea=00043&appId=&lang=J&statsDataId=0003348426&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    #dfの分割　後半が本データ
    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['時間軸(月次)', 'value']]

    df_val2['時間軸(月次)'] = pd.to_datetime(df_val2['時間軸(月次)'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('float')

    df_watch = df_val2.copy()

    #*******可視化
    #*****景気ウオッチャー調査　月
    #グラフを描くときの土台となるオブジェクト
    fig4 = go.Figure()
    #今期のグラフの追加

    fig4.add_trace(
        go.Scatter(
            x=df_val2['時間軸(月次)'],
            y=df_val2['value'],
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='宮城'
            )
    )

    #レイアウト設定     
    fig4.update_layout(
        title='景気ウオッチャー調査　月',
        showlegend=True #凡例表示
    )
    st.plotly_chart(fig4, use_container_width=True) 
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

    #*****景気ウオッチャー調査　月/直近1年
    #グラフを描くときの土台となるオブジェクト
    fig5 = go.Figure()
    #今期のグラフの追加

    fig5.add_trace(
        go.Scatter(
            x=df_val2['時間軸(月次)'][:13], #新しい順に並んでいる
            y=df_val2['value'][:13],
            mode = 'lines+markers+text', #値表示
            text=df_val2['value'][:13],
            textposition="top center",
            name='宮城'
            )
    )

    #レイアウト設定     
    fig5.update_layout(
        title='景気ウオッチャー調査 月/直近1年',
        showlegend=True #凡例表示
    )
    st.plotly_chart(fig5, use_container_width=True) 
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅

    #********************************消費者物価指数
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=0001&cdTab=1&cdArea=04A01&appId=&lang=J&statsDataId=0003427113&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['時間軸（年・月）', 'value']]

    #年集計行の削除
    for idx, val in enumerate(df_val2['時間軸（年・月）']):
        if '月' not in val:
            df_val2.drop(index=idx, axis=0, inplace=True)

    df_val2['時間軸（年・月）'] = pd.to_datetime(df_val2['時間軸（年・月）'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('float') 

    #******************可視化
    # *********消費者物価指数 月
    #グラフを描くときの土台となるオブジェクト
    fig6 = go.Figure()
    #今期のグラフの追加

    fig6.add_trace(
        go.Scatter(
            x=df_val2['時間軸（年・月）'],
            y=df_val2['value'],
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='仙台市'
            )
    )

    #レイアウト設定     
    fig6.update_layout(
        title='消費者物価指数　月 2000年基準',
        showlegend=True #凡例表示
    )
    st.plotly_chart(fig6, use_container_width=True) 
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

    # *********消費者物価指数 月/直近1年
    #グラフを描くときの土台となるオブジェクト
    fig7 = go.Figure()
    #今期のグラフの追加

    fig7.add_trace(
        go.Scatter(
            x=df_val2['時間軸（年・月）'][:13],
            y=df_val2['value'][:13],
            mode = 'lines+markers+text', #値表示
            text=df_val2['value'][:13],
            textposition="top center",
            name='仙台市'
            )
    )

    #レイアウト設定     
    fig7.update_layout(
        title='消費者物価指数　月/直近1年',
        showlegend=True #凡例表示
    )
    st.plotly_chart(fig7, use_container_width=True) 
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

    #*********************************家計調査
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=040130030%2C090410001%2C090420000&cdCat02=03&cdArea=04003&appId=&lang=J&statsDataId=0003343671&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_travel2 = df_val[df_val['品目分類（2020年改定）'].isin(['9.4.1 宿泊料', '9.4.2 パック旅行費'])]
    df_table2 = df_val[df_val['品目分類（2020年改定）']=='482 テーブル・ソファー']

    df_travel2 = df_travel2[['時間軸（月次）', 'value']]
    df_table2 = df_table2[['時間軸（月次）', 'value']]

    df_travel2['時間軸（月次）'] = pd.to_datetime(df_travel2['時間軸（月次）'], format='%Y年%m月')
    df_travel2['value'] = df_travel2['value'].astype('int')
    df_table2['時間軸（月次）'] = pd.to_datetime(df_table2['時間軸（月次）'], format='%Y年%m月')
    df_table2['value'] = df_table2['value'].astype('int')

    #***************可視化
    #*******旅行
    s_travel = df_travel2.groupby('時間軸（月次）')['value'].sum()

    #グラフを描くときの土台となるオブジェクト
    fig8 = go.Figure()
    #今期のグラフの追加

    fig8.add_trace(
        go.Scatter(
            x=s_travel.index,
            y=s_travel,
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='仙台市'
            )
    )

    #レイアウト設定     
    fig8.update_layout(
        title='旅行　月',
        showlegend=True #凡例表示
    )

    st.plotly_chart(fig8, use_container_width=True) 

    #*******旅行　直近1年
    s_travel = df_travel2.groupby('時間軸（月次）')['value'].sum()

    #グラフを描くときの土台となるオブジェクト
    fig9 = go.Figure()
    #今期のグラフの追加

    fig9.add_trace(
        go.Scatter(
            x=s_travel.index[-13:],
            y=s_travel[-13:],
            mode = 'lines+markers+text', #値表示
            text=s_travel[-13:],
            textposition="top center",
            name='仙台市'
            )
    )

    #レイアウト設定     
    fig9.update_layout(
        title='旅行　直近1年',
        showlegend=True #凡例表示
    )

    st.plotly_chart(fig9, use_container_width=True) 

    # ********************************************************着工数と売上比較
    st.markdown('###### 着工数と売上の比較')
    @st.cache_data
    def make_data(file):
        df_sales = pd.read_excel(file, usecols=[3, 15, 16])
        df_sales = df_sales.sort_values('受注日')

        df_sales['受注月'] = df_sales['受注日'].apply(lambda x: x.strftime('%Y-%m'))
        df_sales['受注月'] = pd.to_datetime(df_sales['受注月'])

        sendai_list = ['㈱家具の橋本', '(有)相馬屋家具店', '㈱東京ｲﾝﾃﾘｱ 仙台港本店', \
                    '㈱東京ｲﾝﾃﾘｱ 仙台泉店', '㈱東京ｲﾝﾃﾘｱ 仙台南店']
        
        df_sendai = df_sales[df_sales['得意先名'].isin(sendai_list)] 

        s_sendai = df_sendai.groupby('受注月')['金額'].sum()

        return s_sendai

    # ***ファイルアップロード 今期***
    uploaded_file = st.sidebar.file_uploader('売上', type='xlsx', key='sales')
    s_sendai = pd.Series()
    if uploaded_file:
        s_sendai = make_data(uploaded_file)

    else:
        st.info('売上のファイルを選択してください。')
        st.stop()

    start_month = s_sendai.index[0]
    num_house = s_val2[start_month:] 

    #**************可視化
    fig_sales = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_sales.add_trace(
        go.Scatter(x=s_sendai.index, y=num_house, name="着工数"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_sales.add_trace(
        go.Scatter(x=s_sendai.index, y=s_sendai, name="売上"),
        secondary_y=True,
    )

    fig_sales.update_yaxes(title_text="<b>primary</b> 着工数", secondary_y=False)
    fig_sales.update_yaxes(title_text="<b>secondary</b> 売上", secondary_y=True)

    st.plotly_chart(fig_sales, use_container_width=True) 

    #**************************************景気ウォッチャー調査と売り上げの比較
    st.markdown('###### 景気ウオッチャー調査と売上の比較')

    df_watch_selected = df_watch[df_watch['時間軸(月次)'] >= start_month] 
    df_watch_selected = df_watch_selected.sort_values('時間軸(月次)')

    #**************可視化
    fig_watch = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_watch.add_trace(
        go.Scatter(x=s_sendai.index, y=df_watch_selected['value'], name="景気ウオッチャー調査"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_watch.add_trace(
        go.Scatter(x=s_sendai.index, y=s_sendai, name="売上"),
        secondary_y=True,
    )

    fig_watch.update_yaxes(title_text="<b>primary</b> 景気ウオッチャー調査", secondary_y=False)
    fig_watch.update_yaxes(title_text="<b>secondary</b> 売上", secondary_y=True)

    st.plotly_chart(fig_watch, use_container_width=True)


 
#********************************************************************************山形
def yamagata():
    #********************************着工数
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdArea=06201%2C06206%2C06207%2C06208%2C06209%2C06210%2C06211%2C06213&cdTab=18&cdCat01=12%2C15&cdCat02=12%2C13&appId=&lang=J&statsDataId=0003114535&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_meta = pd.DataFrame(df[:idx]).set_index(0) #0列目をindexに
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_meta = df_meta.dropna(axis=1, how="all")
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['時間軸(月次)', 'value']]

    df_val2['時間軸(月次)'] = pd.to_datetime(df_val2['時間軸(月次)'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('int')

    s_val2 = df_val2.groupby('時間軸(月次)')['value'].sum()

    #*********************可視化
    #グラフを描くときの土台となるオブジェクト
    fig = go.Figure()
    #今期のグラフの追加

    fig.add_trace(
        go.Scatter(
            x=s_val2.index,
            y=s_val2,
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='山形'
            )
    )

    #レイアウト設定     
    fig.update_layout(
        title='着工数',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig, use_container_width=True) 

    #**************着工数　直近1年
    #可視化
    #グラフを描くときの土台となるオブジェクト
    fig2 = go.Figure()
    #今期のグラフの追加

    fig2.add_trace(
        go.Scatter(
            x=s_val2[-13:].index,
            y=s_val2[-13:],
            mode = 'lines+markers+text', #値表示
            text=s_val2[-13:],
            textposition="top center",
            name='山形'
            )
    )

    #レイアウト設定     
    fig2.update_layout(
        title='着工数',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig2, use_container_width=True) 

    #*************着工数　年
    df_val2['year'] = df_val2['時間軸(月次)'].apply(lambda x: x.year)
    val2_year = df_val2.groupby('year')['value'].sum()

    #グラフを描くときの土台となるオブジェクト
    fig3 = go.Figure()
    #今期のグラフの追加

    fig3.add_trace(
        go.Scatter(
            x=val2_year.index,
            y=val2_year,
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='山形（年単位）'
            )
    )

    #レイアウト設定     
    fig3.update_layout(
        title='着工数',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig3, use_container_width=True) 

    #*************************************景気ウオッチャー調査
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdTab=140&cdCat01=100&cdCat02=100&cdArea=00043&appId=&lang=J&statsDataId=0003348426&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['時間軸(月次)', 'value']]

    df_val2['時間軸(月次)'] = pd.to_datetime(df_val2['時間軸(月次)'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('float')

    df_watch = df_val2.copy()

    #**************************景気ウオッチャー調査　月
    #グラフを描くときの土台となるオブジェクト
    fig4 = go.Figure()
    #今期のグラフの追加

    fig4.add_trace(
        go.Scatter(
            x=df_val2['時間軸(月次)'],
            y=df_val2['value'],
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='東北'
            )
    )

    #レイアウト設定     
    fig4.update_layout(
        title='景気ウオッチャー',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig4, use_container_width=True) 

    #**************************景気ウオッチャー調査　直近1年
    #グラフを描くときの土台となるオブジェクト
    fig5 = go.Figure()
    #今期のグラフの追加

    fig5.add_trace(
        go.Scatter(
            x=df_val2['時間軸(月次)'][:13],
            y=df_val2['value'][:13],
            mode = 'lines+markers+text', #値表示
            text=df_val2['value'][:13],
            textposition="top center",
            name='東北'
            )
    )

    #レイアウト設定     
    fig5.update_layout(
        title='景気ウオッチャー',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig5, use_container_width=True) 

    #******************消費者物価指数
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=0001&cdTab=1&cdArea=06A01&appId=&lang=J&statsDataId=0003427113&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['時間軸（年・月）', 'value']]

    for idx, val in enumerate(df_val2['時間軸（年・月）']):
        if '月' not in val:
            df_val2.drop(index=idx, axis=0, inplace=True)

    df_val2['時間軸（年・月）'] = pd.to_datetime(df_val2['時間軸（年・月）'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('float')

    #***********************消費者物価指数　月
    #グラフを描くときの土台となるオブジェクト
    fig6 = go.Figure()
    #今期のグラフの追加

    fig6.add_trace(
        go.Scatter(
            x=df_val2['時間軸（年・月）'],
            y=df_val2['value'],
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='山形市'
            )
    )

    #レイアウト設定     
    fig6.update_layout(
        title='消費者物価指数',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig6, use_container_width=True)  

    #***********************消費者物価指数　月 直近1年
    #グラフを描くときの土台となるオブジェクト
    fig7 = go.Figure()
    #今期のグラフの追加

    fig7.add_trace(
        go.Scatter(
            x=df_val2['時間軸（年・月）'][:13],
            y=df_val2['value'][:13],
            mode = 'lines+markers+text', #値表示
            text=df_val2['value'][:13],
            textposition="top center",
            name='山形市'
            )
    )

    #レイアウト設定     
    fig7.update_layout(
        title='消費者物価指数 直近1年',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig7, use_container_width=True) 

    #********************家計調査
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=040130030%2C090410001%2C090420000&cdCat02=03&cdArea=06003&appId=&lang=J&statsDataId=0003343671&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50)) 

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_travel2 = df_val[df_val['品目分類（2020年改定）'].isin(['9.4.1 宿泊料', '9.4.2 パック旅行費'])]
    df_table2 = df_val[df_val['品目分類（2020年改定）']=='482 テーブル・ソファー']

    df_travel2 = df_travel2[['時間軸（月次）', 'value']]
    df_table2 = df_table2[['時間軸（月次）', 'value']]

    df_travel2['時間軸（月次）'] = pd.to_datetime(df_travel2['時間軸（月次）'], format='%Y年%m月')
    df_travel2['value'] = df_travel2['value'].astype('int')
    df_table2['時間軸（月次）'] = pd.to_datetime(df_table2['時間軸（月次）'], format='%Y年%m月')
    df_table2['value'] = df_table2['value'].astype('int')

    s_travel = df_travel2.groupby('時間軸（月次）')['value'].sum()

    #***********************家計調査　旅行
    #グラフを描くときの土台となるオブジェクト
    fig8 = go.Figure()
    #今期のグラフの追加

    fig8.add_trace(
        go.Scatter(
            x=s_travel.index,
            y=s_travel,
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='旅行'
            )
    )

    #レイアウト設定     
    fig8.update_layout(
        title='旅行',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig8, use_container_width=True) 

    #***********************家計調査　旅行 直近1年
    #グラフを描くときの土台となるオブジェクト
    fig9 = go.Figure()
    #今期のグラフの追加

    fig9.add_trace(
        go.Scatter(
            x=s_travel.index[-13:],
            y=s_travel[-13:],
            mode = 'lines+markers+text', #値表示
            text=s_travel[-13:],
            textposition="top center",
            name='旅行'
            )
    )

    #レイアウト設定     
    fig9.update_layout(
        title='旅行　直近1年',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig9, use_container_width=True) 

# ********************************************************着工数と売上比較
    st.markdown('###### 着工数と売上の比較')
    @st.cache_data
    def make_data(file):
        df_sales = pd.read_excel(file, usecols=[3, 15, 16])
        df_sales = df_sales.sort_values('受注日')

        df_sales['受注月'] = df_sales['受注日'].apply(lambda x: x.strftime('%Y-%m'))
        df_sales['受注月'] = pd.to_datetime(df_sales['受注月'])

        sendai_list = ['㈱家具のオツタカ', '㈱東京ｲﾝﾃﾘｱ 山形店']
        
        df_sendai = df_sales[df_sales['得意先名'].isin(sendai_list)] 

        s_sendai = df_sendai.groupby('受注月')['金額'].sum()

        return s_sendai

    # ***ファイルアップロード 今期***
    uploaded_file = st.sidebar.file_uploader('売上', type='xlsx', key='sales')
    s_sendai = pd.Series()
    if uploaded_file:
        s_sendai = make_data(uploaded_file)

    else:
        st.info('売上のファイルを選択してください。')
        st.stop()

    start_month = s_sendai.index[0]
    num_house = s_val2[start_month:] 

    #**************可視化
    fig_sales = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_sales.add_trace(
        go.Scatter(x=s_sendai.index, y=num_house, name="着工数"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_sales.add_trace(
        go.Scatter(x=s_sendai.index, y=s_sendai, name="売上"),
        secondary_y=True,
    )

    fig_sales.update_yaxes(title_text="<b>primary</b> 着工数", secondary_y=False)
    fig_sales.update_yaxes(title_text="<b>secondary</b> 売上", secondary_y=True)

    st.plotly_chart(fig_sales, use_container_width=True) 

    # #**************************************景気ウォッチャー調査と売り上げの比較
    st.markdown('###### 景気ウオッチャー調査と売上の比較')

    df_watch_selected = df_watch[df_watch['時間軸(月次)'] >= start_month] 
    df_watch_selected = df_watch_selected.sort_values('時間軸(月次)')

    #**************可視化
    fig_watch = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_watch.add_trace(
        go.Scatter(x=s_sendai.index, y=df_watch_selected['value'], name="景気ウオッチャー調査"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_watch.add_trace(
        go.Scatter(x=s_sendai.index, y=s_sendai, name="売上"),
        secondary_y=True,
    )

    fig_watch.update_yaxes(title_text="<b>primary</b> 景気ウオッチャー調査", secondary_y=False)
    fig_watch.update_yaxes(title_text="<b>secondary</b> 売上", secondary_y=True)

    st.plotly_chart(fig_watch, use_container_width=True)

#********************************************************************************山形

def fukushima():
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdArea=07201%2C07203%2C07204%2C07207%2C07210%2C07211%2C07213%2C07214&cdTab=18&cdCat01=12%2C15&cdCat02=12%2C13&appId=&lang=J&statsDataId=0003114535&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    #metadataとdataの分割
    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_meta = pd.DataFrame(df[:idx]).set_index(0) #0列目をindexに
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_meta = df_meta.dropna(axis=1, how="all")
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['時間軸(月次)', '地域', 'value']]

    df_val2['時間軸(月次)'] = pd.to_datetime(df_val2['時間軸(月次)'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('int')

    #エリア毎に集計
    fukushima_list = ['福島市', '伊達市', '二本松市']
    koriyama_list =['郡山市', '須賀川市', '本宮市', '田村市']

    #fukushima
    df_fukushima = df_val2[df_val2['地域'].isin(fukushima_list)]
    fukushima_g = df_fukushima.groupby('時間軸(月次)')['value'].sum()

    #koriyama
    df_koriyama = df_val2[df_val2['地域'].isin(koriyama_list)]
    koriyama_g = df_koriyama.groupby('時間軸(月次)')['value'].sum()

    #iwaki
    df_iwaki = df_val2[df_val2['地域']== 'いわき市']
    iwaki_g = df_iwaki.groupby('時間軸(月次)')['value'].sum()

    #****************************************福島市
    st.markdown('##### 福島市')
    #***********着工数
    #グラフを描くときの土台となるオブジェクト
    fig = go.Figure()
    #今期のグラフの追加

    fig.add_trace(
        go.Scatter(
            x=fukushima_g.index,
            y=fukushima_g,
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='福島市'
            )
    )

    #レイアウト設定     
    fig.update_layout(
        title='着工数（月）',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig, use_container_width=True) 

    #***********着工数（月）直近1年
    #グラフを描くときの土台となるオブジェクト
    fig2 = go.Figure()
    #今期のグラフの追加

    fig2.add_trace(
        go.Scatter(
            x=fukushima_g[-13:].index,
            y=fukushima_g[-13:],
            mode = 'lines+markers+text', #値表示
            text=fukushima_g[-13:],
            textposition="top center",
            name='福島市'
            )
    )

    #レイアウト設定     
    fig2.update_layout(
        title='着工数（月）直近1年',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig2, use_container_width=True) 

    #***************着工数　年
    df_fukushima['year'] = df_fukushima['時間軸(月次)'].apply(lambda x: x.year)
    fukushima_year = df_fukushima.groupby('year')['value'].sum()

    #グラフを描くときの土台となるオブジェクト
    fig3 = go.Figure()
    #今期のグラフの追加

    fig3.add_trace(
        go.Scatter(
            x=fukushima_year.index,
            y=fukushima_year,
            mode = 'lines+markers+text', #値表示
            text=fukushima_year,
            textposition="top center",
            name='福島市'
            )
    )

    #レイアウト設定     
    fig3.update_layout(
        title='着工数（年）',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig3, use_container_width=True) 

    #************************************************郡山
    st.markdown('##### 郡山市')
    #着工数　月
    #グラフを描くときの土台となるオブジェクト
    fig4 = go.Figure()
    #今期のグラフの追加

    fig4.add_trace(
        go.Scatter(
            x=koriyama_g.index,
            y=koriyama_g,
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='郡山市'
            )
    )

    #レイアウト設定     
    fig4.update_layout(
        title='着工数（月）',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig4, use_container_width=True) 

    #************着工数　直近1年
    #可視化
    #グラフを描くときの土台となるオブジェクト
    fig5 = go.Figure()
    #今期のグラフの追加

    fig5.add_trace(
        go.Scatter(
            x=koriyama_g[-13:].index,
            y=koriyama_g[-13:],
            mode = 'lines+markers+text', #値表示
            text=koriyama_g[-13:],
            textposition="top center",
            name='郡山市'
            )
    )

    #レイアウト設定     
    fig5.update_layout(
        title='着工数（月）',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig5, use_container_width=True) 

    #**********************着工数　年単位
    df_koriyama['year'] = df_koriyama['時間軸(月次)'].apply(lambda x: x.year)
    koriyama_year = df_koriyama.groupby('year')['value'].sum()

    #グラフを描くときの土台となるオブジェクト
    fig6 = go.Figure()
    #今期のグラフの追加

    fig6.add_trace(
        go.Scatter(
            x=koriyama_year.index,
            y=koriyama_year,
            mode = 'lines+markers+text', #値表示
            text=koriyama_year,
            textposition="top center",
            name='郡山市'
            )
    )

    #レイアウト設定     
    fig6.update_layout(
        title='着工数（年）',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig6, use_container_width=True)

    #*******************************************いわき
    st.markdown('##### いわき市')
    #**************着工数　月
    #グラフを描くときの土台となるオブジェクト
    fig7 = go.Figure()
    #今期のグラフの追加

    fig7.add_trace(
        go.Scatter(
            x=iwaki_g.index,
            y=iwaki_g,
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='いわき市'
            )
    )

    #レイアウト設定     
    fig7.update_layout(
        title='着工数（月）',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig7, use_container_width=True)

    #******************着工数　直近1年
    #グラフを描くときの土台となるオブジェクト
    fig8 = go.Figure()
    #今期のグラフの追加

    fig8.add_trace(
        go.Scatter(
            x=iwaki_g[-13:].index,
            y=iwaki_g[-13:],
            mode = 'lines+markers+text', #値表示
            text=iwaki_g[-13:],
            textposition="top center",
            name='いわき市'
            )
    )

    #レイアウト設定     
    fig8.update_layout(
        title='着工数（月）直近1年',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig8, use_container_width=True)

    #**********************着工数　年
    df_iwaki['year'] = df_iwaki['時間軸(月次)'].apply(lambda x: x.year)
    iwaki_year = df_iwaki.groupby('year')['value'].sum()

    #グラフを描くときの土台となるオブジェクト
    fig9 = go.Figure()
    #今期のグラフの追加

    fig9.add_trace(
        go.Scatter(
            x=iwaki_year.index,
            y=iwaki_year,
            mode = 'lines+markers+text', #値表示
            text=iwaki_year,
            textposition="top center",
            name='いわき市'
            )
    )

    #レイアウト設定     
    fig9.update_layout(
        title='着工数（年）',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig9, use_container_width=True)

    #***********************************************************景気ウオッチャー
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdTab=140&cdCat01=100&cdCat02=100&cdArea=00043&appId=&lang=J&statsDataId=0003348426&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['時間軸(月次)', 'value']]

    df_val2['時間軸(月次)'] = pd.to_datetime(df_val2['時間軸(月次)'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('float')

    df_watch = df_val2.copy()

    #**************可視化
    #グラフを描くときの土台となるオブジェクト
    fig10 = go.Figure()
    #今期のグラフの追加

    fig10.add_trace(
        go.Scatter(
            x=df_val2['時間軸(月次)'],
            y=df_val2['value'],
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='東北'
            )
    )

    #レイアウト設定     
    fig10.update_layout(
        title='景気ウオッチャー調査',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig10, use_container_width=True)

    #**************直近1年
    #グラフを描くときの土台となるオブジェクト
    fig10 = go.Figure()
    #今期のグラフの追加

    fig10.add_trace(
        go.Scatter(
            x=df_val2['時間軸(月次)'][:13],
            y=df_val2['value'][:13],
            mode = 'lines+markers+text', #値表示
            text=df_val2['value'][:13],
            textposition="top center",
            name='東北'
            )
    )

    #レイアウト設定     
    fig10.update_layout(
        title='景気ウオッチャー調査/直近1年',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig10, use_container_width=True)

    #*************************************************************消費者物価指数
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=0001&cdTab=1&cdArea=07A01&appId=&lang=J&statsDataId=0003427113&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['時間軸（年・月）', 'value']]

    #年のみの行をカット
    for idx, val in enumerate(df_val2['時間軸（年・月）']):
        if '月' not in val:
            df_val2.drop(index=idx, axis=0, inplace=True)
    
    df_val2['時間軸（年・月）'] = pd.to_datetime(df_val2['時間軸（年・月）'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('float')

    #***************消費者物価指数
    #グラフを描くときの土台となるオブジェクト
    fig11 = go.Figure()
    #今期のグラフの追加

    fig11.add_trace(
        go.Scatter(
            x=df_val2['時間軸（年・月）'],
            y=df_val2['value'],
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='福島市(基準地域)'
            )
    )

    #レイアウト設定     
    fig11.update_layout(
        title='消費者物価指数',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig11, use_container_width=True)

    #********************消費者物価指数　直近1年
    #グラフを描くときの土台となるオブジェクト
    fig12 = go.Figure()
    #今期のグラフの追加

    fig12.add_trace(
        go.Scatter(
            x=df_val2['時間軸（年・月）'][:13],
            y=df_val2['value'][:13],
            mode = 'lines+markers+text', #値表示
            text=df_val2['value'][:13],
            textposition="top center",
            name='福島市(基準地域)'
            )
    )

    #レイアウト設定     
    fig12.update_layout(
        title='消費者物価指数',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig12, use_container_width=True)

        #*********************************家計調査
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=040130030%2C090410001%2C090420000&cdCat02=03&cdArea=04003&appId=&lang=J&statsDataId=0003343671&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = '6b63c4952895e9a215c2b6f009401e5145207bc9'

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_travel2 = df_val[df_val['品目分類（2020年改定）'].isin(['9.4.1 宿泊料', '9.4.2 パック旅行費'])]
    df_table2 = df_val[df_val['品目分類（2020年改定）']=='482 テーブル・ソファー']

    df_travel2 = df_travel2[['時間軸（月次）', 'value']]
    df_table2 = df_table2[['時間軸（月次）', 'value']]

    df_travel2['時間軸（月次）'] = pd.to_datetime(df_travel2['時間軸（月次）'], format='%Y年%m月')
    df_travel2['value'] = df_travel2['value'].astype('int')
    df_table2['時間軸（月次）'] = pd.to_datetime(df_table2['時間軸（月次）'], format='%Y年%m月')
    df_table2['value'] = df_table2['value'].astype('int')

    #***************可視化
    #*******旅行
    s_travel = df_travel2.groupby('時間軸（月次）')['value'].sum()

    #グラフを描くときの土台となるオブジェクト
    fig8 = go.Figure()
    #今期のグラフの追加

    fig8.add_trace(
        go.Scatter(
            x=s_travel.index,
            y=s_travel,
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='仙台市'
            )
    )

    #レイアウト設定     
    fig8.update_layout(
        title='旅行　月',
        showlegend=True #凡例表示
    )

    st.plotly_chart(fig8, use_container_width=True) 

    #*******旅行　直近1年
    s_travel = df_travel2.groupby('時間軸（月次）')['value'].sum()

    #グラフを描くときの土台となるオブジェクト
    fig9 = go.Figure()
    #今期のグラフの追加

    fig9.add_trace(
        go.Scatter(
            x=s_travel.index[-13:],
            y=s_travel[-13:],
            mode = 'lines+markers+text', #値表示
            text=s_travel[-13:],
            textposition="top center",
            name='仙台市'
            )
    )

    #レイアウト設定     
    fig9.update_layout(
        title='旅行　直近1年',
        showlegend=True #凡例表示
    )

    st.plotly_chart(fig9, use_container_width=True) 

     # ********************************************************着工数と売上比較
    st.markdown('###### 着工数と売上の比較')
    @st.cache_data
    def make_data(file):
        df_sales = pd.read_excel(file, usecols=[3, 15, 16])
        df_sales = df_sales.sort_values('受注日')

        df_sales['受注月'] = df_sales['受注日'].apply(lambda x: x.strftime('%Y-%m'))
        df_sales['受注月'] = pd.to_datetime(df_sales['受注月'])

        fukushima_list = ['（有）ケンポク家具', '㈱東京ｲﾝﾃﾘｱ 福島店']
        koriyama_list = ['ラボット・プランナー株式会社', '㈱東京ｲﾝﾃﾘｱ 郡山店']
        iwaki_list = ['株式会社丸ほん', '㈱吉田家具店', '㈱東京ｲﾝﾃﾘｱ いわき店']
        
        df_fukushima = df_sales[df_sales['得意先名'].isin(fukushima_list)]
        df_koriyama = df_sales[df_sales['得意先名'].isin(koriyama_list)] 
        df_iwaki = df_sales[df_sales['得意先名'].isin(iwaki_list)] 

        s_fukushima = df_fukushima.groupby('受注月')['金額'].sum()
        s_koriyama = df_koriyama.groupby('受注月')['金額'].sum()
        s_iwaki = df_iwaki.groupby('受注月')['金額'].sum()

        return s_fukushima, s_koriyama, s_iwaki

    # ***ファイルアップロード 今期***
    uploaded_file = st.sidebar.file_uploader('売上', type='xlsx', key='sales')

    s_fukushima = pd.Series()
    s_koriyama = pd.Series()
    s_iwaki = pd.Series()

    if uploaded_file:
        s_fukushima, s_koriyama, s_iwaki = make_data(uploaded_file)

    else:
        st.info('売上のファイルを選択してください。')
        st.stop()

    #**************福島市　着工数/売上
    st.markdown('###### 福島市')
    start_month = s_fukushima.index[0]
    house_fukushima = fukushima_g[start_month:] 

    fig_fukushima1 = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_fukushima1.add_trace(
        go.Scatter(x=s_fukushima.index, y=house_fukushima, name="着工数"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_fukushima1.add_trace(
        go.Scatter(x=s_fukushima.index, y=s_fukushima, name="売上"),
        secondary_y=True,
    )

    fig_fukushima1.update_yaxes(title_text="<b>primary</b> 着工数", secondary_y=False)
    fig_fukushima1.update_yaxes(title_text="<b>secondary</b> 売上", secondary_y=True)

    st.plotly_chart(fig_fukushima1, use_container_width=True) 

    #**************************************景気ウォッチャー調査と売り上げの比較
    st.markdown('###### 景気ウオッチャー調査と売上の比較')
    st.markdown('###### 福島市')


    df_watch_selected = df_watch[df_watch['時間軸(月次)'] >= start_month] 
    df_watch_selected = df_watch_selected.sort_values('時間軸(月次)')

    #**************可視化
    fig_watch_f = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_watch_f.add_trace(
        go.Scatter(x=s_fukushima.index, y=df_watch_selected['value'], name="景気ウオッチャー調査"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_watch_f.add_trace(
        go.Scatter(x=s_fukushima.index, y=s_fukushima, name="売上"),
        secondary_y=True,
    )

    fig_watch_f.update_yaxes(title_text="<b>primary</b> 景気ウオッチャー調査", secondary_y=False)
    fig_watch_f.update_yaxes(title_text="<b>secondary</b> 売上", secondary_y=True)

    st.plotly_chart(fig_watch_f, use_container_width=True)

    #**************郡山市　着工数/売上
    st.markdown('###### 郡山市')
    start_month = s_koriyama.index[0]
    house_koriyama = koriyama_g[start_month:] 

    fig_koriyama1 = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_koriyama1.add_trace(
        go.Scatter(x=s_koriyama.index, y=house_koriyama, name="着工数"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_koriyama1.add_trace(
        go.Scatter(x=s_koriyama.index, y=s_koriyama, name="売上"),
        secondary_y=True,
    )

    fig_koriyama1.update_yaxes(title_text="<b>primary</b> 着工数", secondary_y=False)
    fig_koriyama1.update_yaxes(title_text="<b>secondary</b> 売上", secondary_y=True)

    st.plotly_chart(fig_koriyama1, use_container_width=True) 

    #**************************************景気ウォッチャー調査と売り上げの比較
    st.markdown('###### 景気ウオッチャー調査と売上の比較')
    st.markdown('###### 郡山市')


    df_watch_selected = df_watch[df_watch['時間軸(月次)'] >= start_month] 
    df_watch_selected = df_watch_selected.sort_values('時間軸(月次)')

    #**************可視化
    fig_watch_k = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_watch_k.add_trace(
        go.Scatter(x=s_koriyama.index, y=df_watch_selected['value'], name="景気ウオッチャー調査"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_watch_k.add_trace(
        go.Scatter(x=s_koriyama.index, y=s_koriyama, name="売上"),
        secondary_y=True,
    )

    fig_watch_k.update_yaxes(title_text="<b>primary</b> 景気ウオッチャー調査", secondary_y=False)
    fig_watch_k.update_yaxes(title_text="<b>secondary</b> 売上", secondary_y=True)

    st.plotly_chart(fig_watch_k, use_container_width=True)

    #**************いわき市　着工数/売上
    st.markdown('###### いわき市')
    start_month = s_iwaki.index[0]
    house_iwaki = iwaki_g[start_month:] 

    fig_iwaki1 = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_iwaki1.add_trace(
        go.Scatter(x=s_iwaki.index, y=house_iwaki, name="着工数"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_iwaki1.add_trace(
        go.Scatter(x=s_iwaki.index, y=s_iwaki, name="売上"),
        secondary_y=True,
    )

    fig_iwaki1.update_yaxes(title_text="<b>primary</b> 着工数", secondary_y=False)
    fig_iwaki1.update_yaxes(title_text="<b>secondary</b> 売上", secondary_y=True)

    st.plotly_chart(fig_iwaki1, use_container_width=True) 

    #**************************************景気ウォッチャー調査と売り上げの比較
    st.markdown('###### 景気ウオッチャー調査と売上の比較')
    st.markdown('###### いわき市')


    df_watch_selected = df_watch[df_watch['時間軸(月次)'] >= start_month] 
    df_watch_selected = df_watch_selected.sort_values('時間軸(月次)')

    #**************可視化
    fig_watch_i = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_watch_i.add_trace(
        go.Scatter(x=s_iwaki.index, y=df_watch_selected['value'], name="景気ウオッチャー調査"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_watch_i.add_trace(
        go.Scatter(x=s_iwaki.index, y=s_iwaki, name="売上"),
        secondary_y=True,
    )

    fig_watch_i.update_yaxes(title_text="<b>primary</b> 景気ウオッチャー調査", secondary_y=False)
    fig_watch_i.update_yaxes(title_text="<b>secondary</b> 売上", secondary_y=True)

    st.plotly_chart(fig_watch_i, use_container_width=True)





    








def main():
    # アプリケーション名と対応する関数のマッピング
    apps = {
        '-': None,
        '宮城県': miyagi,
        '山形': yamagata,
        '福島': fukushima
       
    }
    selected_app_name = st.sidebar.selectbox(label='分析項目の選択',
                                             options=list(apps.keys()))

    if selected_app_name == '-':
        st.info('サイドバーから分析項目を選択してください')
        st.stop()

    link = '[home](http://linkpagetest.s3-website-ap-northeast-1.amazonaws.com/)'
    st.sidebar.markdown(link, unsafe_allow_html=True)
    st.sidebar.caption('homeに戻る')    

    # 選択されたアプリケーションを処理する関数を呼び出す
    render_func = apps[selected_app_name]
    render_func()

if __name__ == '__main__':
    main()