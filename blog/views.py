from flask import render_template, redirect, url_for, flash, request
from flask_wtf.file import FileAllowed, FileRequired
from flask import Flask, send_from_directory, render_template, request, redirect, url_for, g, flash, send_file
from wtforms.widgets import Input
from werkzeug.utils import secure_filename, escape, unescape
from markupsafe import Markup
import os
from collections import defaultdict
import shutil
import csv, io
import re
import sys, os
import pandas as pd
import re
from pykml.factory import KML_ElementMaker as KML
from datetime import datetime
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
import folium
import folium.plugins
from folium.plugins import MarkerCluster
import numpy as np
import io
import chardet
from collections import defaultdict
from ionos.blog.mapper_model import *
from flask_bootstrap import Bootstrap
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)


blog = Blueprint('blog', __name__)

from ionos import basedir

context= {'status': False, 'name': False, 'extra': False, 'starting': True}
options= defaultdict(lambda: None)

outputfile = defaultdict(lambda: None)
folder = defaultdict(lambda: None)
launcher= Mapper_Model()



def run_analysis():
    if context['name']:
        launcher= Mapper_Model()
        launcher.filepath(folder['tab_file'], folder['spart_file'])
        launcher.tab_file_data()
        launcher.tab_kml()
        launcher.tab_html()
        yy= os.path.join(basedir, 'static', 'analysis.html')

        print(launcher.result_files.keys())
        launcher.result_files['html_file'].save(yy)
        yl = os.path.join(basedir, 'static', 'analysis.kml')
        f = open(yl, 'w+')
        f.write(etree.tostring(launcher.result_files['kml_file']).decode('utf-8'))
        f.close()
        outputfile['html']= yy
        outputfile['kml']= yl
    if context['status']:
        print('yes')
        launcher= Mapper_Model()
        launcher.user_input_data(folder['input_data'])
        launcher.user_input_html()
        launcher.user_input_kml()
        yy= os.path.join(basedir, 'static', 'analysis.html')
        launcher.result_files['html_file'].save(yy)
        yl = os.path.join(basedir, 'static', 'analysis.kml')
        f = open(yl, 'w+')
        f.write(etree.tostring(launcher.result_files['kml_file']).decode('utf-8'))
        f.close()
        outputfile['html']= yy
        outputfile['kml']= yl
    context['extra']= True



@blog.route("/spart/home", methods=['GET', 'POST'])
def check():
    try:
        clear()
        context['name'] = False
        context['status'] = False
        context['extra'] = False
        if request.method == "POST":
                display_type = request.form.get("customRadio", None)
                print(display_type)
                if display_type== "paste":
                    context['status']= True
                if display_type=="upload":
                    context['name']= True
                return render_template("spart_First.html", context= context, name= context['name'], status= context['status'])
        return render_template("spart_First.html", context= context, name= context['name'], status= context['status'])
    except Exception as e:
        clear()
        context['name'] = False
        context['status'] = False
        context['extra'] = False
        flash(f'The process failed beacause {e}')

        return render_template('spart_error.html', context= context, names= context['names'], name= context['name'], status= context['status'], extra= context['extra'])



@blog.route("/spart/upload", methods=['GET', 'POST'])
def upload():
    try:
        if request.method == 'POST':
            if 'files[]' not in request.files:
                flash('No file part')
                return redirect("spart_First.html", context, names= context['names'])
            files = request.files.getlist('files[]')
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                if filename.endswith(".spart"):
                    folder['spart_file'] = file.read().decode('UTF-8')
                if filename.endswith((".txt", ".tab")):
                    folder['tab_file']= file.read().decode('UTF-8')
        context['name'] = True
        context['status'] = False
        context['extra'] = False
        run_analysis()
        template_name = 'spart_last.html'
        html= outputfile['html']
        up2= '/static/analysis.html'
        filen2= 'analysis.html'
        up1= '/static/analysis.kml'
        filen1= 'analysis.kml'
        return render_template(template_name, up2= up2, filen2= filen2, up1= up1, filen1= filen1, name= context['name'], status= context['status'], extra= context['extra'])
    except Exception as e:
        clear()
        context['name'] = False
        context['status'] = False
        context['extra'] = False
        flash(f'The process failed beacause {e}')

        return render_template('spart_error.html', context= context, names= context['names'], name= context['name'], status= context['status'], extra= context['extra'])





@blog.route("/spart/paste", methods=['GET', 'POST'])
def paste():
    try:
        if request.method == "POST":
            content = request.form['content']
            folder['input_data']= content
            context['name'] = False
            context['extra'] = False
            context['status']= True
            template_name= "dna_last.html"
            run_analysis()
        context['name'] = False
        context['extra'] = True
        context['status']= True
        template_name= "dna_last.html"
        html= outputfile['html']
        up2= '/static/analysis.html'
        filen2= 'analysis.html'
        up1= '/static/analysis.kml'
        filen1= 'analysis.kml'
        return render_template("spart_last.html", up1= up1, up2= up2, filen1= filen1, filen2= filen2, extra= context['extra'], name= context['name'], status= context['status'])
    except Exception as e:
        clear()
        context['name'] = False
        context['status'] = False
        context['extra'] = False
        flash(f'The process failed beacause {e}')

        return render_template('spart_error.html', context= context, names= context['names'], name= context['name'], status= context['status'], extra= context['extra'])



def clear():
    outputfile= {}
    context= {'name': False, 'status': False, 'extra': False}
