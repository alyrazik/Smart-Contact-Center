from flask import Flask, render_template, flash, redirect, request, url_for, session
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html',
                           companies=[{'name': 'Vodafone'}, {'name': 'Etisalat'}, {'name': 'WE'}, {'name': 'Orange'}])


@app.route("/test", methods=['GET', 'POST'])
def chooseCompany():
    df = pd.read_csv('./final.csv', encoding='utf-8-sig')
    select = request.form.get('comp_select')
    if (select == 'Vodafone'):
        df = df.query('named_entities.str.contains("vodafone")', engine='python')
    elif (select == 'Etisalat'):
        df = df.query('named_entities.str.contains("etisalat")', engine='python')
    elif (select == 'Orange'):
        df = df.query('named_entities.str.contains("orange")', engine='python')
    elif (select == 'WE'):
        df = df.query('named_entities.str.contains("we")', engine='python')

    return render_template('simple.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


if __name__ == "__main__":
    app.run(debug=True)
