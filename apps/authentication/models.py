# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from datetime import datetime

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    email         = db.Column(db.String(64), unique=True)
    password      = db.Column(db.LargeBinary)

    oauth_github  = db.Column(db.String(100), nullable=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)
            setattr(self, property, value)
    def __repr__(self):
        return str(self.username) 


class Pembelajaran(db.Model):
    __tablename__ = 'Pembelajaran'

    id                   = db.Column(db.Integer, primary_key=True)
    kode_pembelajaran    = db.Column(db.String(50), unique=True, nullable=False)
    judul_pembelajaran   = db.Column(db.String(255), nullable=False)
    periode              = db.Column(db.String(50), nullable=False)
    nama_instruktur      = db.Column(db.String(100), nullable=False)
    tanggal_mulai        = db.Column(db.DateTime, default=datetime.utcnow)
    tanggal_selesai      = db.Column(db.DateTime, nullable=True)
    waktu                = db.Column(db.String(50), nullable=True)  # misalnya, waktu pelaksanaan pembelajaran
    penampilan           = db.Column(db.Float, nullable=True)  # Penilaian instruktur (0-10)
    pengenalan           = db.Column(db.Float, nullable=True)  # Penilaian instruktur (0-10)
    membangun_suasana    = db.Column(db.Float, nullable=True)  # Penilaian instruktur (0-10)
    penguasaan_materi    = db.Column(db.Float, nullable=True)  # Penilaian instruktur (0-10)
    penyampaian_materi   = db.Column(db.Float, nullable=True)  # Penilaian instruktur (0-10)
    rata_rata_per_instruktur = db.Column(db.Float, nullable=True)  # Rata-rata penilaian instruktur

    def __init__(self, kode_pembelajaran, judul_pembelajaran, periode, nama_instruktur, tanggal_mulai, tanggal_selesai=None):
        self.kode_pembelajaran = kode_pembelajaran
        self.judul_pembelajaran = judul_pembelajaran
        self.periode = periode
        self.nama_instruktur = nama_instruktur
        self.tanggal_mulai = tanggal_mulai
        self.tanggal_selesai = tanggal_selesai

    def __repr__(self):
        return f'<Pembelajaran {self.kode_pembelajaran} - {self.judul_pembelajaran}>'

    def hitung_rata_rata(self):
        penilaian = [self.penampilan, self.pengenalan, self.membangun_suasana, self.penguasaan_materi, self.penyampaian_materi]
        valid_penilaian = [p for p in penilaian if p is not None]
        if valid_penilaian:
            self.rata_rata_per_instruktur = sum(valid_penilaian) / len(valid_penilaian)
            db.session.commit()


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)
