import streamlit as st
import pandas as pd

def app():
    st.title('Age-wise Population Distribution in South Korea (Top 5 Administrative Districts)')

    # Load the data
    df = pd.read_csv('202505_202505_연령별인구현황_월간.csv')

    # Data preprocessing steps
    df['행정구역'] = df['행정구역'].astype(str).str.split(' ').str[0]

    new_columns = []
    for col in df.columns:
        if '2025년05월_계_' in col:
            new_col = col.replace('2025년05월_계_', '')
            if '총인구수' in new_col:
                new_col = '총인구수'
            elif '연령구간인구수' in new_col:
                new_col = '연령구간인구수'
            else:
                new_col = new_col.replace('세', '세')
            new_columns.append(new_col)
        else:
            new_columns.append(col)
    df.columns = new_columns

    cols_to_convert = [col for col in df.columns if col != '행정구역']
    for col in cols_to_convert:
        df[col] = df[col].astype(str).str.replace(',', '', regex=False).astype(int)

    top_5_regions = df.sort_values(by='총인구수', ascending=False).head(5)['행정구역'].tolist()

    df_top_5 = df[df['행정구역'].isin(top_5_regions)].copy()

    df_melted = df_top_5.melt(id_vars=['행정구역', '총인구수', '연령구간인구수'],
                              var_name='Age',
                              value_name='Population')

    df_melted['Age'] = df_melted['Age'].str.extract('(\d+)').astype(int)

    st.write("---")
    st.header("Original Data")
    st.dataframe(df)

    st.write("---")
    st.header(f"Age-wise Population Distribution for Top 5 Administrative Districts")
    # Streamlit requires a "long-form" dataframe to render multiple series in one chart,
    # or separate columns for each series. Since we want lines for each '행정구역',
    # we need to pivot the melted dataframe or use altair directly with melted data.
    # st.line_chart expects the dataframe to be in wide format or have a single series.

    # To plot multiple series in one chart using st.line_chart,
    # the dataframe should be in a wide format where each series is a column.
    # Alternatively, use Altair for more control.
    # For simplicity with st.line_chart, let's pivot the data first.
    pivot_df = df_melted.pivot_table(index='Age', columns='행정구역', values='Population')
    st.line_chart(pivot_df)

if __name__ == '__main__':
    app()
