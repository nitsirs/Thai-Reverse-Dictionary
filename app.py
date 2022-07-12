from pandas import value_counts
import streamlit as st
from pythainlp.translate import Translate
import nltk
import requests
#nltk.download('wordnet')
#nltk.download('omw-1.4')

#python -m nltk.downloader all
from collections import OrderedDict 
from nltk.corpus import wordnet as wn
from annotated_text import annotated_text

@st.cache
def load_model():
    th2en = Translate('th', 'en')
    return (th2en)

st.set_page_config(page_title="ค้นคำ", page_icon="open-book.png")
streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@500&display=swap');
			html, body, [class*="css"]  {
			font-family: 'IBM Plex Sans Thai', sans-serif;
            line-height: 2.15;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)
st.title('ค้นหาคำจากความหมาย')
search = st.text_input('พิมพ์คำอธิบายพอสังเขป:', value='คนชั่ว โกงกินประเทศชาติ')

th2en = load_model()

def main():

    if search:
        output = "annotated_text("
        search_result = search_words(search)
        for i in search_result:
            output += ''.join(['"  ",(" ',i,'",""),']) 
        output += ')'
        eval(output)



def search_words(query):
    query =  th2en.translate(query)
    params = {
    'q': query,
    'm': 'EnEn',
}
    response = requests.get('https://wantwords.net/EnglishRD/', params=params)
    candidate = [i['w'] for i in eval(response.text)]
    i=0
    synonyms = []
    for x in range(50):
        while(i<20):
            try:
                synonyms += wn.synsets(candidate[x])[i].lemma_names('tha')
            except:
                i+=1
                pass
            i+=1
        i=0
    synonyms = list(OrderedDict.fromkeys(synonyms))
    return synonyms

if __name__ == '__main__':
    main()