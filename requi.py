import streamlit as st
import glob
import pandas as pd

# stand-alone version !
import tika
from tika import parser

def show_request(infile, col1, col2):
     """
     show_request zeigt das Anforderungsformular, welches als HTML oder XML in der Variable infile übergeben wurde
     auf dem Bildschirm an
     """
     try:
          # neues Formular = falsch 
          newForm = False
          df = pd.read_html(infile, encoding='utf-8', index_col=False)
          if "Verbindungsdaten" or "Call Detail Records" in infile:
               newForm = True
          df = df[0]
          df.drop(columns=[2], inplace=True)
          df.fillna("", inplace=True)
          
          if newForm: # neues Formular
               # 1. Zeile löschen (Verbindungsdaten bzw. Call Detail Records)
               df.drop([0], inplace=True)
               
          else: # altes Formular
               # erste beiden und letzte Zeile löschen (Beschreibung, 1. KONTAKT und letzte (leere Zeile))
               df.drop([0], inplace=True) 
               df.drop([0], inplace=True)
               df.drop([len(df)], inplace=True)
          
          i = 0
          contents = {}
          for row in df.itertuples():
               if i < len(df)/2:
                    if row._2 != "":
                         with col1:
                              st.write(f'**{row._1}**')
                              st.text_input('', row._2)
                    else:
                         with col1:
                              st.write(row._1) # text_input(row._1, row._2)
               else:
                    if row._2 != "":
                         with col2:
                              st.write(f'**{row._1}**')
                              st.text_input('', row._2)
                    else:
                         with col2:
                              st.write(row._1)
               field = row._1
               typ = field.split(' ')
               #st.write(typ)
               contents[' '.join(typ[1:])] = row._2
               i += 1
          
          with st.beta_expander("Extrahierte Daten"):
               st.write(contents)
               
          # if st.button('Übernehmen'):
          #      # in Datenbank speichern
          #      st.write('saved')
     except:
          st.write("Not a valid request")
          pass

def main():
     st.sidebar.text('Work in progress')

     selection = st.sidebar.selectbox('Options', ['Upload new request'])

     if selection == 'Upload new request':
          uploaded_file = st.file_uploader('Upload file')
          if uploaded_file is not None:
               # save file
               col1, col2 = st.beta_columns(2)
               #with open(f'd:/{uploaded_file.name}', 'wb') as f:
               #     f.write(uploaded_file.getvalue())
               bytes_data = uploaded_file.getvalue()
               parsed = parser.from_buffer(bytes_data, xmlContent=True)
               show_request(parsed['content'], col1, col2)
     else:
          st.error('This shouldn\'t have happened')

if __name__ == '__main__':
     tika.initVM()
     main()
