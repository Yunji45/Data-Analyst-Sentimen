# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask,render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from apps.authentication.models import Pembelajaran

from apps.authentication.util import verify_pass
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import io
import plotly.express as px
import plotly.io as pio
import base64
import plotly.express as px
import plotly.io as pio
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

analyzer = SentimentIntensityAnalyzer()

# Global dictionary to store processed data
processed_data = {}
def analyze_sentiment(text):
    score = analyzer.polarity_scores(str(text))
    if score['compound'] >= 0.05:
        return "Positif"
    elif score['compound'] <= -0.05:
        return "Negatif"
    else:
        return "Netral"
    
@blueprint.route('/upload', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST':
        file_csv = request.files.get('file_csv')
        file_excel = request.files.get('file_excel')

        if file_csv and file_excel:
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
                fig1 = px.pie(
                    names=sentiment_counts.index, 
                    values=sentiment_counts.values, 
                    # title="Distribusi Sentimen Komentar Terbuka",
                    color=sentiment_counts.index, 
                    color_discrete_sequence=px.colors.qualitative.Set3
                )

                # fig1 = px.pie(names=sentiment_counts.index, values=sentiment_counts.values, title="Distribusi Sentimen Komentar Terbuka")
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

                # Plotly charts
                fig2 = px.bar(
                    top_materials, 
                    x=post_test_average_column, 
                    y='Judul Diklat', 
                    orientation='h', 
                    # title="10 Materi Pembelajaran Terbaik",
                    color=post_test_average_column,  # Warna berdasarkan nilai
                    color_continuous_scale='Viridis',  # Skala warna yang lebih menarik
                    labels={post_test_average_column: 'Nilai Rata-Rata', 'Judul Diklat': 'Materi Pembelajaran'}
                )
                # fig2 = px.bar(top_materials, x=post_test_average_column, y='Judul Diklat', orientation='h', title="10 Materi Pembelajaran Terbaik")
                plot_url2 = pio.to_html(fig2, full_html=False)

                # fig3 = px.bar(bottom_materials, x=post_test_average_column, y='Judul Diklat', orientation='h', title="10 Materi Pembelajaran Perlu Perbaikan")
                fig3 = px.bar(
                    bottom_materials, 
                    x=post_test_average_column, 
                    y='Judul Diklat', 
                    orientation='h', 
                    # title="10 Materi Pembelajaran Perlu Perbaikan",
                    color=post_test_average_column,
                    color_continuous_scale='RdYlGn',
                    labels={post_test_average_column: 'Nilai Rata-Rata', 'Judul Diklat': 'Materi Pembelajaran'}
                )
                plot_url3 = pio.to_html(fig3, full_html=False)

                # fig4 = px.bar(popular_materials, x='Jumlah Peserta', y='Judul Diklat', orientation='h', title="Materi Pembelajaran Terpopuler")
                fig4 = px.bar(
                    popular_materials, 
                    x='Jumlah Peserta', 
                    y='Judul Diklat', 
                    orientation='h', 
                    # title="Materi Pembelajaran Terpopuler",
                    color='Jumlah Peserta',
                    color_continuous_scale='Blues',
                    labels={'Jumlah Peserta': 'Jumlah Peserta', 'Judul Diklat': 'Materi Pembelajaran'}
                )
                plot_url4 = pio.to_html(fig4, full_html=False)

                # Store results
                processed_data.update({
                    'top_materials': top_materials,
                    'plot_url2': plot_url2,
                    'bottom_materials': bottom_materials,
                    'plot_url3': plot_url3,
                    'popular_materials': popular_materials,
                    'plot_url4': plot_url4,
                })

                # Analisis Materi Perlu Dievaluasi
            if post_test_average_column in data_feedback.columns:
                # Data bottom materials
                data_feedback[post_test_average_column] = pd.to_numeric(data_feedback[post_test_average_column], errors='coerce')
                data_feedback.dropna(subset=[post_test_average_column], inplace=True)

                grouped_materials = data_feedback.groupby(['Judul Diklat'])[post_test_average_column].mean().reset_index()
                bottom_materials_evaluasi = grouped_materials.sort_values(by=post_test_average_column).head(10)

                # Plot materi perlu dievaluasi
                fig_bottom = px.bar(
                    bottom_materials_evaluasi,
                    x=post_test_average_column,
                    y='Judul Diklat',
                    orientation='h',
                    color=post_test_average_column,
                    color_continuous_scale='RdYlGn',
                    labels={post_test_average_column: 'Nilai Rata-Rata', 'Judul Diklat': 'Materi Pembelajaran'},
                )
                plot_url_bottom = pio.to_html(fig_bottom, full_html=False)

                # Simpan hasil ke `processed_data`
                processed_data.update({
                    'bottom_materials_evaluasi': bottom_materials_evaluasi.to_dict(orient='records'),
                    'plot_url_bottom': plot_url_bottom,
                })


                ## pembelajaran perlu dievaluasi
                threshold = 60 
                materials_to_evaluate = grouped_materials[grouped_materials[post_test_average_column] < threshold]
                evaluation_table_html = materials_to_evaluate.to_html(index=False, classes="table table-striped table-bordered", header=True)

                fig_eval = px.bar(
                    materials_to_evaluate,
                    x=post_test_average_column,
                    y='Judul Diklat',
                    orientation='h',
                    color=post_test_average_column,
                    color_continuous_scale='OrRd',
                    labels={post_test_average_column: 'Nilai Rata-Rata', 'Judul Diklat': 'Materi Pembelajaran'},
                )
                plot_url_eval = pio.to_html(fig_eval, full_html=False)

                # Store evaluation data
                processed_data.update({
                    'evaluation_table': evaluation_table_html,
                    'plot_url_eval': plot_url_eval,
                })


            # Top Instructors Analysis
            if instructor_quality_column in data_instructor.columns and instructor_name_column in data_instructor.columns:
                data_instructor[instructor_quality_column] = pd.to_numeric(data_instructor[instructor_quality_column], errors='coerce')
                data_instructor.dropna(subset=[instructor_quality_column], inplace=True)
                
                # Calculate the top 10 instructors based on average score
                top_instructors = data_instructor.groupby(instructor_name_column)[instructor_quality_column].mean().reset_index().sort_values(by=instructor_quality_column, ascending=False).head(10)

                # Prepare detailed instructor table with training period, but only for the top 10 instructors
                instructor_table = data_instructor[data_instructor[instructor_name_column].isin(top_instructors[instructor_name_column])]
                instructor_table = instructor_table[['NAMA INSTRUKTUR', 'RATA-RATA PER INSTRUKTUR', 'JUDUL PEMBELAJARAN', 'PERIODE', 'Unnamed: 4']].copy()
                instructor_table.columns = ['Nama Instruktur', 'Rata-Rata Per Instruktur', 'Judul Pembelajaran', 'Tanggal Mulai', 'Tanggal Selesai']
                instructor_table.dropna(subset=['Nama Instruktur', 'Rata-Rata Per Instruktur'], inplace=True)
                
                # Sort instructor_table by 'Rata-Rata Per Instruktur' in descending order for ranking
                instructor_table = instructor_table.sort_values(by='Rata-Rata Per Instruktur', ascending=False).reset_index(drop=True)
                instructor_table.index += 1  # Start numbering from 1 for ranking display
                
                # Convert to HTML, displaying only the top 10 instructors
                instructor_table_html = instructor_table.to_html(index=True, classes="table table-striped table-bordered", header=True)

                # Plotly bar chart
                # fig5 = px.bar(top_instructors, x=instructor_quality_column, y=instructor_name_column, orientation='h', title="10 Instruktur Terbaik")
                fig5 = px.bar(
                    top_instructors, 
                    x=instructor_quality_column, 
                    y=instructor_name_column, 
                    orientation='h', 
                    # title="10 Instruktur Terbaik",
                    color=instructor_quality_column,
                    color_continuous_scale='YlGnBu',
                    labels={instructor_quality_column: 'Nilai Rata-Rata Instruktur', 'NAMA INSTRUKTUR': 'Nama Instruktur'}
                )

                plot_url5 = pio.to_html(fig5, full_html=False)

                # Store top instructors data
                processed_data.update({
                    'top_instructors': instructor_table_html,
                    'plot_url5': plot_url5,
                })

        # Memastikan kolom yang benar
        post_test_average_column = 'N Rata2'  # Gantilah dengan nama kolom rata-rata yang sesuai

        # Menampilkan 5 penyelenggara terbaik
        top_organizers = grouped_materials[['Judul Diklat', post_test_average_column]].nlargest(5, post_test_average_column)

        # Membuat tabel HTML untuk Top Penyelenggara
        top_organizers_table_html = top_organizers.to_html(index=False, classes="table table-striped table-bordered", header=True)

        # Membuat grafik bar untuk Top Penyelenggara
        fig_top_organizers = px.bar(
            top_organizers,
            x=post_test_average_column,
            y='Judul Diklat',
            orientation='h',
            color=post_test_average_column,
            color_continuous_scale='Viridis',
            labels={post_test_average_column: 'Nilai Rata-Rata', 'Penyelenggara': 'Penyelenggara'},
        )

        # Mengonversi grafik menjadi HTML
        plot_url_top_organizers = pio.to_html(fig_top_organizers, full_html=False)

        # Menyimpan data untuk dikirim ke template
        processed_data.update({
            'top_organizers_table': top_organizers_table_html,
            'plot_url_top_organizers': plot_url_top_organizers,
        })

    return render_template('home/dashboard.html', processed_data=processed_data)


@blueprint.route('/sentiment_analysis')
def sentiment_analysis():
    return render_template('home/sentimen_analysis.html', plot_url1=processed_data.get('plot_url1'))

@blueprint.route('/top_materials')
def top_materials_page():
    top_materials = processed_data.get('top_materials', pd.DataFrame())
    data_feedback = processed_data.get('data_feedback', pd.DataFrame())
    if not top_materials.empty and 'Sentimen' in data_feedback.columns:
        sentiment_counts = (
            data_feedback[data_feedback['Judul Diklat'].isin(top_materials['Judul Diklat'])]
            .groupby(['Judul Diklat', 'Sentimen']).size().unstack(fill_value=0)
        ).reset_index()
        top_materials = top_materials.merge(sentiment_counts, on='Judul Diklat', how='left')
        top_materials_html = top_materials.to_html(index=False, classes="table table-striped table-bordered")
    else:
        top_materials_html = "<p>Data tidak tersedia.</p>"
    return render_template('home/tables-bootstrap-tables.html', top_materials=top_materials_html, plot_url2=processed_data.get('plot_url2'))

@blueprint.route('/bottom_materials')
def bottom_materials_page():
    bottom_materials = processed_data.get('bottom_materials', pd.DataFrame())
    data_feedback = processed_data.get('data_feedback', pd.DataFrame())
    if not bottom_materials.empty and 'Sentimen' in data_feedback.columns:
        sentiment_counts = (
            data_feedback[data_feedback['Judul Diklat'].isin(bottom_materials['Judul Diklat'])]
            .groupby(['Judul Diklat', 'Sentimen']).size().unstack(fill_value=0)
        ).reset_index()
        bottom_materials = bottom_materials.merge(sentiment_counts, on='Judul Diklat', how='left')
        bottom_materials_html = bottom_materials.to_html(index=False, classes="table table-striped table-bordered")
    else:
        bottom_materials_html = "<p>Data tidak tersedia.</p>"
    return render_template('home/klasifikasi_materi.html', bottom_materials=bottom_materials_html, plot_url3=processed_data.get('plot_url3'))

@blueprint.route('/popular_materials')
def popular_materials_page():
    popular_materials = processed_data.get('popular_materials', pd.DataFrame())
    data_feedback = processed_data.get('data_feedback', pd.DataFrame())
    if not popular_materials.empty and 'Sentimen' in data_feedback.columns:
        sentiment_counts = (
            data_feedback[data_feedback['Judul Diklat'].isin(popular_materials['Judul Diklat'])]
            .groupby(['Judul Diklat', 'Sentimen']).size().unstack(fill_value=0)
        ).reset_index()
        popular_materials = popular_materials.merge(sentiment_counts, on='Judul Diklat', how='left')
        popular_materials_html = popular_materials.to_html(index=False, classes="table table-striped table-bordered")
    else:
        popular_materials_html = "<p>Data tidak tersedia.</p>"
    return render_template('home/populer_materials.html', popular_materials=popular_materials_html, plot_url4=processed_data.get('plot_url4'))


@blueprint.route('/materi_evaluasi')
def material_evaluasi_page():
    bottom_materials_evaluasi = processed_data.get('bottom_materials_evaluasi', pd.DataFrame())
    plot_url_bottom = processed_data.get('plot_url_bottom', pd.DataFrame())
    if not bottom_materials_evaluasi.empty and 'Sentimen' in plot_url_bottom.columns:
        sentiment_counts = (
            plot_url_bottom[plot_url_bottom['Judul Diklat'].isin(bottom_materials_evaluasi['Judul Diklat'])]
            .groupby(['Judul Diklat', 'Sentimen']).size().unstack(fill_value=0)
        ).reset_index()
        bottom_materials_evaluasi = bottom_materials_evaluasi.merge(sentiment_counts, on='Judul Diklat', how='left')
        bottom_materials_html = bottom_materials_evaluasi.to_html(index=False, classes="table table-striped table-bordered")
    else:
        bottom_materials_html = "<p>Data tidak tersedia.</p>"
    return render_template('home/materi_evaluasi.html', bottom_materials_evaluasi=bottom_materials_html, plot_url_bottom=processed_data.get('plot_url_bottom'))

@blueprint.route('/top_instructors')
def top_instructors_page():
    return render_template(
        'home/top_instructurs.html',
        top_instructors=processed_data.get('top_instructors'),
        plot_url5=processed_data.get('plot_url5')
    )

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route("/github")
def login_github():
    """ Github login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.upload'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()
        
        return render_template('accounts/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

#evaluasi
@blueprint.route('/evaluasi/tambah', methods=['GET', 'POST'])
def add_pembelajaran():
    form = PembelajaranForm(request.form)
    if request.method == 'POST' and form.validate():
        pembelajaran = Pembelajaran(
            kode_pembelajaran=form.kode_pembelajaran.data,
            judul_pembelajaran=form.judul_pembelajaran.data,
            periode=form.periode.data,
            nama_instruktur=form.nama_instruktur.data,
            tanggal_mulai=form.tanggal_mulai.data,
            tanggal_selesai=form.tanggal_selesai.data,
            waktu=form.waktu.data,
            penampilan=form.penampilan.data,
            pengenalan=form.pengenalan.data,
            membangun_suasana=form.membangun_suasana.data,
            penguasaan_materi=form.penguasaan_materi.data,
            penyampaian_materi=form.penyampaian_materi.data
        )
        db.session.add(pembelajaran)
        db.session.commit()
        return redirect(url_for('authentication_blueprint.pembelajaran_list'))
    return render_template('pembelajaran/add.html', form=form)


@blueprint.route('/evaluasi', methods=['GET'])
def pembelajaran_list():
    pembelajarans = Pembelajaran.query.all()
    return render_template('evaluasi/list.html', pembelajarans=pembelajarans)


@blueprint.route('/evaluasi/edit/<int:id>', methods=['GET', 'POST'])
def edit_pembelajaran(id):
    pembelajaran = Pembelajaran.query.get_or_404(id)
    form = PembelajaranForm(obj=pembelajaran)
    if request.method == 'POST' and form.validate():
        pembelajaran.kode_pembelajaran = form.kode_pembelajaran.data
        pembelajaran.judul_pembelajaran = form.judul_pembelajaran.data
        pembelajaran.periode = form.periode.data
        pembelajaran.nama_instruktur = form.nama_instruktur.data
        pembelajaran.tanggal_mulai = form.tanggal_mulai.data
        pembelajaran.tanggal_selesai = form.tanggal_selesai.data
        pembelajaran.waktu = form.waktu.data
        pembelajaran.penampilan = form.penampilan.data
        pembelajaran.pengenalan = form.pengenalan.data
        pembelajaran.membangun_suasana = form.membangun_suasana.data
        pembelajaran.penguasaan_materi = form.penguasaan_materi.data
        pembelajaran.penyampaian_materi = form.penyampaian_materi.data
        pembelajaran.hitung_rata_rata()  # Menghitung rata-rata penilaian
        db.session.commit()
        return redirect(url_for('authentication_blueprint.pembelajaran_list'))
    return render_template('pembelajaran/edit.html', form=form, pembelajaran=pembelajaran)


@blueprint.route('/evaluasi/hapus/<int:id>', methods=['POST'])
def delete_pembelajaran(id):
    pembelajaran = Pembelajaran.query.get_or_404(id)
    db.session.delete(pembelajaran)
    db.session.commit()
    return redirect(url_for('authentication_blueprint.pembelajaran_list'))
