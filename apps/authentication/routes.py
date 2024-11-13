# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for
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
    return redirect(url_for('home_blueprint.index'))


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
