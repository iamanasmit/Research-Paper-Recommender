import streamlit as st
import pickle
import re

vectorstore = pickle.load(open('vectorstore.pkl', 'rb'))
st.title('ML based Research Paper Recommender')

title, abstract= "", ""

title=st.text_input("Enter title of the paper", key='title')
abstract=st.text_input("Enter a brief abstract for the paper", key='abstract')
no_recommendation=st.number_input("Number of Recommendations", min_value=1, max_value=10, step=1, key='no_recommendation')

if st.button('Submit'):
    query=f'titles: {title} abstracts: {abstract}'
    results=vectorstore.similarity_search_with_score(query, k=no_recommendation)
    i=0
    for result in results:
        text=result[0].page_content
        text=re.sub(r'\n', '', text)

        pattern = r"terms:\s*(.*?)\s*titles:\s*(.*?)\s*abstracts:\s*(.*)"

        # Search for the pattern
        match = re.search(pattern, text)

        # Extract the matches
        if match:
            terms = match.group(1).strip()
            titles = match.group(2).strip()
            abstracts = match.group(3).strip()
            st.write(i+1, "Recommendation")
            st.write("Technologies used:", terms)
            st.write("Title:", titles)
            st.write("Abstract:", abstracts)
            i+=1
        else:
            st.write("Pattern not found in the text.")
        