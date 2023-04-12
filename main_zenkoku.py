import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots #2軸


st.set_page_config(page_title='merket_condition')
st.markdown('### 市況情報')

#***************関数
def make_line(x, y, legend, title):
            #グラフを描くときの土台となるオブジェクト
    fig = go.Figure()
    #今期のグラフの追加

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode = 'lines+markers+text', #値表示
            text=round(y),
            textposition="top center",
            name=legend
            )
    )

    #レイアウト設定     
    fig.update_layout(
        title=title,
        showlegend=True #凡例表示
    )
    st.plotly_chart(fig, use_container_width=True) 
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

#******make_linenonvalue 値ラベルなし
def make_line_nonvalue(x, y, legend, title):
            #グラフを描くときの土台となるオブジェクト
    fig = go.Figure()
    #今期のグラフの追加

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            # mode = 'lines+markers+text', #値表示
            # text=round(y),
            # textposition="top center",
            name=legend
            )
    )

    #レイアウト設定     
    fig.update_layout(
        title=title,
        showlegend=True #凡例表示
    )
    st.plotly_chart(fig, use_container_width=True) 
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅

#****************make_line2
def make_line2(df, x, title):
     #可視化
    #グラフを描くときの土台となるオブジェクト
    fig = go.Figure()
    #今期のグラフの追加
    for col in df.columns:
        fig.add_trace(
            go.Scatter(
                x=x, #strにしないと順番が崩れる
                y=df[col],
                mode = 'lines+markers+text', #値表示
                text=round(df[col]),
                textposition="top center", 
                name=col)
        )

    #レイアウト設定     
    fig.update_layout(
        title=title,
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig, use_container_width=True) 

#****************make_line2_nonvalue
def make_line2_nonvalue(df, x, title):
     #可視化
    #グラフを描くときの土台となるオブジェクト
    fig = go.Figure()
    #今期のグラフの追加
    for col in df.columns:
        fig.add_trace(
            go.Scatter(
                x=x, #strにしないと順番が崩れる
                y=df[col],
                # mode = 'lines+markers+text', #値表示
                # text=round(df[col]/10000),
                # textposition="top center", 
                name=col)
        )

    #レイアウト設定     
    fig.update_layout(
        title=title,
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig, use_container_width=True) 

def chakkou():
    st.markdown('#### 建築着工統計調査')
    st.caption('住宅着工統計/都道府県別、工事別、利用関係別／戸数・件数、床面積/持家分譲/新設+その他')
    #建築着工統計調査 住宅着工統計/都道府県別、工事別、利用関係別／戸数・件数、床面積/持家分譲/新設+その他
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdTab=18&cdCat01=12%2C15&cdCat02=12%2C13&appId=&lang=J&statsDataId=0003114535&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
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
    df_val2 = df_val[['地域', '時間軸(月次)', 'value']]

    #data型の変換
    df_val2['時間軸(月次)'] = pd.to_datetime(df_val2['時間軸(月次)'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('int')

    # 地域選択
    with st.form("chakkou"):
        areas = st.multiselect(
        '地域選択 ※複数選択可',
        df_val2['地域'].unique())

        submitted = st.form_submit_button("決定")

    if submitted:
        df_selected = df_val2[df_val2['地域'].isin(areas)]

        #'時間軸(月次)'でgroupby
        sum_selected = df_selected.groupby('時間軸(月次)')['value'].sum()

        #*******可視化
        # #*******月単位
        make_line_nonvalue(sum_selected.index, sum_selected, '着工数', '着工数/月単位')

        #*******年単位
        df_selected['year'] = df_selected['時間軸(月次)'].apply(lambda x: x.year)
        sum_year = df_selected.groupby('year')['value'].sum()

        make_line(sum_year.index, sum_year, '着工数', '着工数/年単位')

        #月単位　直近1年

        make_line(sum_selected[-13:].index, sum_selected[-13:], '着工数', '着工数/月単位/直近1年')
    
            
def keiki():

    #******************景気ウォッチャー調査
    st.markdown('#### 景気ウォッチャー調査')
    st.caption('0から100/50が境目') 
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?appId=&lang=J&statsDataId=0003348424&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = st.secrets['PRIVATE']['appId'] #.streamlit\secret.tmolから参照
    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    #dfの分割　後半が本データ
    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['地域', '時間軸(月次)', 'value']]

    df_val2['時間軸(月次)'] = pd.to_datetime(df_val2['時間軸(月次)'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('float')

     # 地域選択
    with st.form("keiki"):
        area = st.selectbox(
        '地域選択',
        df_val2['地域'].unique())

        submitted = st.form_submit_button("決定")

    if submitted:
        df_selected = df_val2[df_val2['地域']==area]

        make_line_nonvalue(df_selected['時間軸(月次)'][:37], df_selected['value'][:37], 
                           '指数', '景気ウオッチャー調査/月単位/過去3年')

        #*****景気ウオッチャー調査　月/直近1年

        make_line(df_selected['時間軸(月次)'][:13], df_selected['value'][:13], \
                  '指数', '景気ウオッチャー調査/月/直近1年')

#     #********************************消費者物価指数
def bukka():
    st.markdown('#### 消費者物価指数')
    st.caption('基準2020年')
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=0001&cdTab=1&appId=&lang=J&statsDataId=0003427113&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = st.secrets['PRIVATE']['appId'] #.streamlit\secret.tmolから参照

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['地域（2020年基準）', '時間軸（年・月）', 'value']]

     # 地域選択
    with st.form("bukka"):
        area = st.selectbox(
        '地域選択',
        df_val2['地域（2020年基準）'].unique())

        submitted = st.form_submit_button("決定")

    if submitted:

        #年集計行の削除
        for idx, val in enumerate(df_val2['時間軸（年・月）']):
            if '月' not in val:
                df_val2.drop(index=idx, axis=0, inplace=True)

        df_val2['時間軸（年・月）'] = pd.to_datetime(df_val2['時間軸（年・月）'], format='%Y年%m月')
        df_val2['value'] = df_val2['value'].astype('float') 

        df_selected = df_val2[df_val2['地域（2020年基準）']==area]

        #******************可視化
        # *********消費者物価指数 月

        make_line_nonvalue(df_selected['時間軸（年・月）'], df_selected['value'], '指数', \
                           '消費者物価指数/月単位 2020年基準')

        # *********消費者物価指数 月/直近1年

        make_line(df_selected['時間軸（年・月）'][:13], df_selected['value'][:13], '指数',\
                  '消費者物価指数/月/直近1年') 

#     #*********************************家計調査
def kakei():
    st.markdown('#### 家計消費状況調査')
    st.caption('二人以上世帯/全国約3万世帯/1世帯当たり1か月間の支出金額')

    #**************************************ネット購入以外
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=0100%2C0110%2C0120%2C0130%2C0220%2C0230%2C0310%2C0320&cdCat03=0030&appId=&lang=J&statsDataId=0003168511&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = st.secrets['PRIVATE']['appId'] #.streamlit\secret.tmolから参照

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_travel = df_val[df_val['品目区分(平成29年改定)'].isin(\
        ['０４　航空運賃', '０５　宿泊料', '０６　パック旅行費（国内）', '０７　パック旅行費（外国）'])]
    df_watch = df_val[df_val['品目区分(平成29年改定)'].isin(\
        ['１６　腕時計', '１７　装身具（アクセサリー類）'])]
    df_furniture = df_val[df_val['品目区分(平成29年改定)'].isin(\
        ['２５　食卓セット', '２６　応接セット'])]
    
    df_travel = df_travel[['全国・地方・都市階級(平成29年改定)', '時間軸（月次・四半期・年次）', 'value']]
    df_watch = df_watch[['全国・地方・都市階級(平成29年改定)', '時間軸（月次・四半期・年次）', 'value']]
    df_furniture = df_furniture[['全国・地方・都市階級(平成29年改定)', '時間軸（月次・四半期・年次）', 'value']]

    df_travel['時間軸（月次・四半期・年次）'] = pd.to_datetime(df_travel['時間軸（月次・四半期・年次）'], \
                                                 format='%Y年%m月')
    df_travel['value'] = df_travel['value'].apply(lambda x: 0 if x=='-' else x)
    df_travel['value'] = df_travel['value'].astype('int')

    df_watch['時間軸（月次・四半期・年次）'] = pd.to_datetime(df_watch['時間軸（月次・四半期・年次）'], \
                                                 format='%Y年%m月')
    df_watch['value'] = df_watch['value'].apply(lambda x: 0 if x=='-' else x)
    df_watch['value'] = df_watch['value'].astype('int')

    df_furniture['時間軸（月次・四半期・年次）'] = pd.to_datetime(df_furniture['時間軸（月次・四半期・年次）'], \
                                                 format='%Y年%m月')
    df_furniture['value'] = df_furniture['value'].apply(lambda x: 0 if x=='-' else x)
    df_furniture['value'] = df_furniture['value'].astype('int')

    #**************************************ネット購入

        #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=0780&appId=&lang=J&statsDataId=0003168329&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = st.secrets['PRIVATE']['appId'] #.streamlit\secret.tmolから参照

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")
    
    df_furniture_net = df_val[['全国・地方・都市階級(平成29年改定)', '時間軸（月次・四半期・年次）', 'value']]

    df_furniture_net['時間軸（月次・四半期・年次）'] = pd.to_datetime(df_furniture_net['時間軸（月次・四半期・年次）'], \
                                                 format='%Y年%m月')
    df_furniture_net['value'] = df_furniture_net['value'].apply(lambda x: 0 if x=='-' else x)
    df_furniture_net['value'] = df_furniture_net['value'].astype('int')

     # ***************地域選択
    with st.form("kakei"):
        area = st.selectbox(
        '地域選択',
        df_travel['全国・地方・都市階級(平成29年改定)'].unique())

        submitted = st.form_submit_button("決定")

    if submitted:
        df_travel2 = df_travel[df_travel['全国・地方・都市階級(平成29年改定)']==area]
        #***************可視化
        #*******旅行
        s_travel = df_travel2.groupby('時間軸（月次・四半期・年次）')['value'].sum()

        make_line_nonvalue(s_travel.index, s_travel, '旅行', '旅行/月単位')

        #*******旅行　直近1年
        make_line(s_travel.index[-13:], s_travel[-13:], '旅行', '旅行/直近1年')

        #******時計、アクセサリー
        s_watch = df_watch.groupby('時間軸（月次・四半期・年次）')['value'].sum()

        make_line_nonvalue(s_watch.index, s_watch, '時計/アクセサリー', '時計/アクセサリー/月単位')

        #*******時計、アクセサリー　直近1年
        make_line(s_watch.index[-13:], s_watch[-13:], '時計/アクセサリー', '時計/アクセサリー/直近1年')

        #******家具
        s_furniture = df_furniture.groupby('時間軸（月次・四半期・年次）')['value'].sum()
        s_furniture_net = df_furniture_net.groupby('時間軸（月次・四半期・年次）')['value'].sum()

        s_furniture.rename('実店舗購入', inplace=True)
        s_furniture_net.rename('ネット購入', inplace=True)

        df_furniture_m = pd.concat([s_furniture, s_furniture_net], axis=1, join='inner')

        st.write(df_furniture_m)
   
        make_line2_nonvalue(df_furniture_m, df_furniture_m.index, '食卓/応接セット/月単位')


        #*******家具　直近1年
        make_line2(df_furniture_m[-13:], df_furniture_m[-13:].index, '食卓/応接セット/直近1年')

        make_line(s_furniture.index[-13:], s_furniture[-13:], '食卓/応接セット', '食卓/応接セット/直近1年')
        make_line(s_furniture_net.index[-13:], s_furniture_net[-13:], '食卓/応接セット', 'ネット購入: 食卓/応接セット/直近1年')





def main():
    # アプリケーション名と対応する関数のマッピング
    apps = {
        '-': None,
        '建築着工統計調査': chakkou,
        '景気ウォッチャー調査': keiki,
        '消費者物価指数': bukka,
        '家計消費状況調査': kakei
       
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