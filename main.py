import pandas as pd
import streamlit as st
import plotly.graph_objects as go


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

    #***********テーブル・ソファ
    #グラフを描くときの土台となるオブジェクト
    fig10 = go.Figure()
    #今期のグラフの追加

    fig10.add_trace(
        go.Scatter(
            x=df_table2['時間軸（月次）'],
            y=df_table2['value'],
            # mode = 'lines+markers+text', #値表示
            # text=round(df3['合計']),
            # textposition="top center",
            name='仙台市'
            )
    )

    #レイアウト設定     
    fig10.update_layout(
        title='テーブル・ソファ',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig10, use_container_width=True) 

    #***********テーブル・ソファ 直近1年
    #グラフを描くときの土台となるオブジェクト
    fig11 = go.Figure()
    #今期のグラフの追加

    fig11.add_trace(
        go.Scatter(
            x=df_table2['時間軸（月次）'][-13:],
            y=df_table2['value'][-13:],
            mode = 'lines+markers+text', #値表示
            text=df_table2['value'][-13:],
            textposition="top center",
            name='仙台市'
            )
    )

    #レイアウト設定     
    fig11.update_layout(
        title='テーブル・ソファ　直近1年',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig11, use_container_width=True) 

    








def main():
    # アプリケーション名と対応する関数のマッピング
    apps = {
        '-': None,
        '宮城県': miyagi,
       
  
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