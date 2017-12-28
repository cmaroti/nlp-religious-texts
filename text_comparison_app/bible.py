
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField
import pickle
import pandas as pd


# read in pickled data
sims = pickle.load(open('final_sims.pkl', 'rb'))
book_indices = pickle.load(open('book_indices.pkl', 'rb'))
df = pd.read_pickle('full_df.pkl')

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176b'

class ReusableForm(Form):
    name = TextField('Enter chapter to compare:', validators=[validators.required()])
    # book = TextField('Choose book to compare above chapter to:', validators=[validators.required()])
    book = SelectField('Choose book:', choices=[('old testament', 'Old Testament'),
        ('new testament', 'New Testament'), ('quran', 'Quran'), ('rigveda', 'Rigveda'),
        ('bhagavad gita', 'Bhagavad Gita'), ('shri guru granth', 'Guru Granth Sahib'),
        ('dhammapada', 'Dhammapada'), ('tao te ching', 'Tao Te Ching'),
        ('confucian analects', 'Analects of Confucius'), ('book of mormon', 'Book of Mormon')])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    def get_similar_chapters(chapter_index, book):
        book_ind = book_indices[book]
        ind = list(sims[chapter_index][book_ind[0]:(book_ind[0]+book_ind[1]-1)]).index(max(sims[chapter_index][book_ind[0]:(book_ind[0]+book_ind[1]-1)]))
        return sims[chapter_index][book_ind[0]+ind], df.loc()[book_ind[0]+ind].book, df.loc()[book_ind[0]+ind].chapter, df.loc()[book_ind[0]+ind].text


    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        book = request.form['book']

        if name == "":
            flash('Please enter a chapter', 'o-text')
        elif book == "":
            chap_ind = df[df.chapter == name].index[0]
            flash(str(df.loc()[chap_ind].book), 'o-book')
            flash(str(df.loc()[chap_ind].chapter), 'o-chap')
            flash(str(df.loc()[chap_ind].text), 'o-text')
            flash('Please enter a book', 'n-text')

        else:
            chap_ind = df[df.chapter == name].index[0]
            if form.validate():
                # Save the comment here.
                flash(str(df.loc()[chap_ind].book).upper(), 'o-book')
                flash(str(df.loc()[chap_ind].chapter), 'o-chap')
                flash(str(df.loc()[chap_ind].text), 'o-text')
                flash(str(get_similar_chapters(chap_ind, book)[1]).upper(), 'n-book')
                flash(str(get_similar_chapters(chap_ind, book)[2]), 'n-chap')
                flash(str(get_similar_chapters(chap_ind, book)[3]), 'n-text')


    return render_template('textapp.html', form=form)

if __name__ == "__main__":
    app.run()
