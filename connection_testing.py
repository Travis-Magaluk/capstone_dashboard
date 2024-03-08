import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(layout="wide")
# Create your title, header, and subheader
st.sidebar.success("Select a demo above.")
st.title("Playground")
st.header("Playing with some code")
st.subheader("Neat subheader!!!")

conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM all_moves;', ttl="10m")

# Print results.
st.write(df.head())

move_counts = df.groupby('year_move')['id'].count().reset_index(name='Count')

# Bar plot using Matplotlib
fig, ax = plt.subplots()
move_counts.plot(kind='bar', x='year_move', y='Count', ax=ax)
plt.title('Number of Moves per Category')
plt.xlabel('Category')
plt.ylabel('Count')
st.pyplot(fig)