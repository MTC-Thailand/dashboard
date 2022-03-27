import streamlit as st
import pandas as pd
import altair as at
from sqlalchemy import create_engine


def setup_database():
    engine = create_engine(f'mysql+pymysql://{st.secrets["DB_USERNAME"]}:{st.secrets["DB_PASSWORD"]}@{st.secrets["DB_HOST"]}/{st.secrets["DB_NAME"]}?charset=utf8')
    return engine


engine = setup_database()
st.title('MTC Business Intelligence Dashboard')
data_load_state = st.text('Loading...')
df = pd.read_sql_query('''
select count(*) as total, member.office_type_id, office_type.type_name from member
inner join lic_mem on lic_mem.mem_id=member.mem_id
inner join emp_function on member.emp_function_id=emp_function.emp_function_id
inner join office_type on member.office_type_id=office_type.office_type_id
where lic_mem.lic_exp_date>now() and emp_function.emp_function_id=1
group by office_type_id;
''', con=engine)
data = st.dataframe(df.sort_values('total', ascending=False))
data_load_state.text('Done loading..')

st.subheader('Office Types')
chart = at.Chart(df.sort_values('total', ascending=False))\
    .mark_bar().encode(x='type_name', y='total')
st.altair_chart(chart, use_container_width=True)
print(engine.connect())