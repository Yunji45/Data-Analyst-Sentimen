# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, FloatField
from wtforms.validators import Email, DataRequired ,Length, Optional

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
                            

class PembelajaranForm(FlaskForm):
    kode_pembelajaran = StringField(
        'Kode Pembelajaran',
        id='kode_pembelajaran',
        validators=[DataRequired(), Length(min=1, max=50)]
    )
    judul_pembelajaran = StringField(
        'Judul Pembelajaran',
        id='judul_pembelajaran',
        validators=[DataRequired(), Length(min=1, max=255)]
    )
    periode = StringField(
        'Periode',
        id='periode',
        validators=[DataRequired(), Length(min=1, max=50)]
    )
    nama_instruktur = StringField(
        'Nama Instruktur',
        id='nama_instruktur',
        validators=[DataRequired(), Length(min=1, max=100)]
    )
    tanggal_mulai = DateTimeField(
        'Tanggal Mulai',
        id='tanggal_mulai',
        validators=[DataRequired()],
        format='%Y-%m-%d %H:%M:%S'
    )
    tanggal_selesai = DateTimeField(
        'Tanggal Selesai',
        id='tanggal_selesai',
        validators=[Optional()],
        format='%Y-%m-%d %H:%M:%S'
    )
    waktu = StringField(
        'Waktu',
        id='waktu',
        validators=[Optional(), Length(max=50)]
    )
    penampilan = FloatField(
        'Penampilan',
        id='penampilan',
        validators=[Optional()]
    )
    pengenalan = FloatField(
        'Pengenalan',
        id='pengenalan',
        validators=[Optional()]
    )
    membangun_suasana = FloatField(
        'Membangun Suasana',
        id='membangun_suasana',
        validators=[Optional()]
    )
    penguasaan_materi = FloatField(
        'Penguasaan Materi',
        id='penguasaan_materi',
        validators=[Optional()]
    )
    penyampaian_materi = FloatField(
        'Penyampaian Materi',
        id='penyampaian_materi',
        validators=[Optional()]
    )
    rata_rata_per_instruktur = FloatField(
        'Rata-rata Per Instruktur',
        id='rata_rata_per_instruktur',
        validators=[Optional()]
    )