# upload.py
import pandas as pd
import plotly.express as px
import plotly.io as pio
from sentiment_analysis import analyze_sentiment  # Pastikan fungsi ini didefinisikan di tempat yang sesuai

def process_upload(file_csv, file_excel):
    processed_data = {}

    # Load CSV and Excel data
    data_feedback = pd.read_csv(file_csv)
    data_instructor = pd.read_excel(file_excel, header=3)

    # Define column names
    sentiment_column = 'Komentar Terbuka'
    post_test_average_column = 'N Rata2'
    instructor_quality_column = 'RATA-RATA PER INSTRUKTUR'
    instructor_name_column = 'NAMA INSTRUKTUR'

    # Sentiment Analysis on Feedback Comments
    if sentiment_column in data_feedback.columns:
        data_feedback['Sentimen'] = data_feedback[sentiment_column].apply(analyze_sentiment)
        sentiment_counts = data_feedback['Sentimen'].value_counts()
        fig1 = px.pie(names=sentiment_counts.index, values=sentiment_counts.values, title="Distribusi Sentimen Komentar Terbuka")
        plot_url1 = pio.to_html(fig1, full_html=False)
        processed_data['sentiment_counts'] = sentiment_counts.to_dict()
        processed_data['plot_url1'] = plot_url1

    # Store data_feedback for further use
    processed_data['data_feedback'] = data_feedback

    # Top and Bottom Materials and Popularity Analysis
    if post_test_average_column in data_feedback.columns:
        data_feedback[post_test_average_column] = pd.to_numeric(data_feedback[post_test_average_column], errors='coerce')
        data_feedback.dropna(subset=[post_test_average_column], inplace=True)

        grouped_materials = data_feedback.groupby(['Judul Diklat'])[post_test_average_column].mean().reset_index()
        top_materials = grouped_materials.sort_values(by=post_test_average_column, ascending=False).head(10)
        bottom_materials = grouped_materials.sort_values(by=post_test_average_column).head(10)
        popular_materials = data_feedback['Judul Diklat'].value_counts().head(10).reset_index(name='Jumlah Peserta').rename(columns={'index': 'Judul Diklat'})

        fig2 = px.bar(top_materials, x=post_test_average_column, y='Judul Diklat', orientation='h', title="10 Materi Pembelajaran Terbaik")
        plot_url2 = pio.to_html(fig2, full_html=False)

        fig3 = px.bar(bottom_materials, x=post_test_average_column, y='Judul Diklat', orientation='h', title="10 Materi Pembelajaran Perlu Perbaikan")
        plot_url3 = pio.to_html(fig3, full_html=False)

        fig4 = px.bar(popular_materials, x='Jumlah Peserta', y='Judul Diklat', orientation='h', title="Materi Pembelajaran Terpopuler")
        plot_url4 = pio.to_html(fig4, full_html=False)

        processed_data.update({
            'top_materials': top_materials,
            'plot_url2': plot_url2,
            'bottom_materials': bottom_materials,
            'plot_url3': plot_url3,
            'popular_materials': popular_materials,
            'plot_url4': plot_url4,
        })

    # Top Instructors Analysis
    if instructor_quality_column in data_instructor.columns and instructor_name_column in data_instructor.columns:
        data_instructor[instructor_quality_column] = pd.to_numeric(data_instructor[instructor_quality_column], errors='coerce')
        data_instructor.dropna(subset=[instructor_quality_column], inplace=True)
        
        top_instructors = data_instructor.groupby(instructor_name_column)[instructor_quality_column].mean().reset_index().sort_values(by=instructor_quality_column, ascending=False).head(10)
        instructor_table = data_instructor[data_instructor[instructor_name_column].isin(top_instructors[instructor_name_column])]
        instructor_table = instructor_table[['NAMA INSTRUKTUR', 'RATA-RATA PER INSTRUKTUR', 'JUDUL PEMBELAJARAN', 'PERIODE', 'Unnamed: 4']].copy()
        instructor_table.columns = ['Nama Instruktur', 'Rata-Rata Per Instruktur', 'Judul Pembelajaran', 'Tanggal Mulai', 'Tanggal Selesai']
        instructor_table.dropna(subset=['Nama Instruktur', 'Rata-Rata Per Instruktur'], inplace=True)
        instructor_table = instructor_table.sort_values(by='Rata-Rata Per Instruktur', ascending=False).reset_index(drop=True)
        instructor_table.index += 1  
        instructor_table_html = instructor_table.to_html(index=True, classes="table table-striped table-bordered", header=True)

        fig5 = px.bar(top_instructors, x=instructor_quality_column, y=instructor_name_column, orientation='h', title="10 Instruktur Terbaik")
        plot_url5 = pio.to_html(fig5, full_html=False)

        processed_data.update({
            'top_instructors': instructor_table_html,
            'plot_url5': plot_url5,
        })

    return processed_data
