from dna import app
from flask import render_template, redirect, url_for, flash, request
from flask_wtf.file import FileAllowed, FileRequired
from flask import Flask, send_from_directory, render_template, request, redirect, url_for, g, flash, send_file
from wtforms.widgets import Input
from werkzeug.utils import secure_filename, escape, unescape
from markupsafe import Markup
import os
from collections import defaultdict
import shutil
from dna.DNAconvert import *


basedir = os.path.abspath(os.path.dirname(__file__))

context= {'status': False, 'name': False, 'extra': False, 'starting': True}
options= defaultdict(lambda: None)

@app.route('/download', methods=['GET', 'POST'])
def download():
    if context['status']:
        file = os.path.join(app.config['output'], 'result.txt')
        return send_file(file, as_attachment=True)
    if context['name']:
        file = os.path.join(basedir, 'output.zip')
        return send_file(file, as_attachment=True)


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def check():
    try:
        clear()
        display_type= None
        context['name'] = False
        context['status'] = False
        context['extra'] = False
        context['names']= ['tab', 'fasta', 'tab_noheaders', 'relaxed_phylip', 'phylip', 'fastq', 'nexus', 'genbank', 'fasta_gbexport', 'moid_fas']
        context['outputs']= ['tab', 'fasta', 'tab_noheaders', 'relaxed_phylip', 'phylip', 'fastq', 'nexus', 'fasta_gbexport', 'moid_fas']
        if request.method == "POST":
            display_type = request.form.get("customRadio", None)
            print(display_type)
            if display_type== "paste":
                context['status']= True
            if display_type=="upload":
                context['name']= True
            return render_template("First.html", context= context, names= context['names'], outputs= context['outputs'], name= context['name'], status= context['status'])
                # return render(request, "profile_upload1.html", {"formset": formset})
        return render_template("First.html", context= context, names= context['names'], outputs= context['outputs'], name= context['name'], status= context['status'])

    except Exception as e:
        clear()
        template_name = 'error.html'
        flash(f'The process failed beacause {e}')
        return render(request, template_name, context)


def paste_convert(inputdata, outfile_path, informat_name= None, outformat_name= None, disable_automatic_renaming= False, allow_empty_sequences= False):
    informat = parse_format(informat_name, ext_pair= ("", ""))
    outformat = parse_format(outformat_name, ext_pair= ("", ""))
    infile = inputdata
    with infile, open(outfile_path, mode="w") as outfile:
        convertDNA(infile, outfile, informat=informat, outformat=outformat, allow_empty_sequences= allow_empty_sequences, disable_automatic_renaming= disable_automatic_renaming)



@app.route('/')
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        if os.path.exists(os.path.join(app.config['output'], 'result.txt')):
            os.remove(os.path.join(app.config['output'], 'result.txt'))
        if os.path.exists(os.path.join(basedir, 'output.zip')):
            os.remove(os.path.join(basedir, 'output.zip'))

        input= os.path.join(app.config['uploads'], 'input')
        if os.path.isdir(input):
            shutil.rmtree(input, ignore_errors=True)
        os.mkdir(input)
        result= os.path.join(app.config['output'], 'result')
        if os.path.isdir(result):
            shutil.rmtree(result, ignore_errors=True)
        os.mkdir(result)
        options['allow_empty_sequences'] = False
        options['disable_automatic_renaming'] = False

        if request.method == 'POST':
            input_format= request.form['u1']
            output_format= request.form['u2']
            if request.form.get('u3'):
                options['allow_empty_sequences'] = True
            if request.form.get('u4'):
                options['disable_automatic_renaming'] = True

            if 'files[]' not in request.files:
                flash('No file part')
            # check if the post request has the file part

                return redirect("First.html", context, names= context['names'])
            files = request.files.getlist('files[]')

        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(input, filename))

        from dna.DNAconvert import convert_wrapper
        convert_wrapper(
            input,
            result,
            input_format,
            output_format,
            allow_empty_sequences= options['allow_empty_sequences'],
            disable_automatic_renaming= options['disable_automatic_renaming'],
        )
        context['name'] = True
        context['status'] = False
        context['extra'] = True

        template_name = 'last.html'
        dir_name = os.path.join(app.config['output'], 'result')
        shutil.make_archive(app.config['output'], 'zip', dir_name)


        return render_template(template_name, context= context, names= context['names'], name= context['name'], status= context['status'], extra= context['extra'])

    except Exception as e:
        clear()
        context['status'] = False
        flash(f'The process failed beacause {e}')
        return render_template('error.html')



@app.route('/')
@app.route('/paste', methods=['GET', 'POST'])
def paste():
    try:
        if os.path.exists(os.path.join(app.config['output'], 'result.txt')):
            os.remove(os.path.join(app.config['output'], 'result.txt'))
        if os.path.exists(os.path.join(basedir, 'output.zip')):
            os.remove(os.path.join(basedir, 'output.zip'))
        options['allow_empty_sequences'] = False
        options['disable_automatic_renaming'] = False
        outfile_path = os.path.join(app.config['output'], 'result.txt')
        if request.method == "POST":
            content = request.form['content']
            content= io.StringIO(content)
            input_format= request.form['p1']
            output_format= request.form['p2']
            if request.form.get('p3'):
                options['allow_empty_sequences'] = True
            if request.form.get('p4'):
                options['disable_automatic_renaming'] = True
            paste_convert(content, outfile_path, informat_name= input_format, outformat_name= output_format, allow_empty_sequences= options['allow_empty_sequences'], disable_automatic_renaming= options['disable_automatic_renaming'])
        context['name'] = False
        context['extra'] = True
        context['status']= True
        template_name= "last.html"
        return render_template("last.html", context= context, names= context['names'], extra= context['extra'], name= context['name'], status= context['status'])

    except Exception as e:
        clear()
        context['status'] = False
        flash(f'The process failed beacause {e}')
        return render_template('error.html')



def clear():
    outputfile= {}
    context= {'name': False, 'status': False, 'extra': False}
