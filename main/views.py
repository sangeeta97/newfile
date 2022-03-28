from flask import render_template, request, Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_wtf.file import FileAllowed, FileRequired
from flask import Flask, send_from_directory, render_template, request, redirect, url_for, g, flash, send_file
from wtforms.widgets import Input
from werkzeug.utils import secure_filename, escape, unescape
from markupsafe import Markup
import os
from collections import defaultdict
import shutil
from flask_bootstrap import Bootstrap


main = Blueprint('main', __name__)

from ionos import basedir


@main.route("/")
def home():
    return render_template('main_base.html')


@main.route("/home/")
def home1():
    return redirect('/')


@main.route("/dna", methods=['GET', 'POST'])
def dna():
    uploads = os.path.join(basedir, "static", "images", "DNAconvert.png")
    return send_file(uploads)


@main.route("/spartmapper/", methods=['GET', 'POST'])
def spartmapper():
    uploads = os.path.join(basedir, "static", "images", "Spartmapper.png")
    return send_file(uploads)
