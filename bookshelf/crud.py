# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for


crud = Blueprint('crud', __name__)


# [START list]
@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list]

@crud.route('/search')
def search():
    title = request.args.get('title', None)
    year = request.args.get('year', None)
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().search_list(title=title, year=year, cursor=token)

    return render_template(
        "search_list.html", 
        title = title, 
        year = year, 
        books=books, 
        next_page_token=next_page_token)

@crud.route('/hsearch')
def hsearch():
    hashtag = request.args.get('hashtag', None)
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().search_hash(hashtag=hashtag, cursor=token)
    return render_template(
        "search_hash.html",
        hashtag = hashtag,
        books = books,
        next_page_token = next_page_token)

@crud.route('/<id>')
def view(id):
    book = get_model().read_book(id)

    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    reviews, next_page_token = get_model().list_review(cursor=token, book_id=id)
    avg_rate, count = get_model().book_rate(id)
    hashtag = get_model().hashtag(id)
    return render_template(
        "view.html", 
        book=book, 
        reviews=reviews, 
        avg_rate=avg_rate[0],
        count=count[0],
        next_page_token=next_page_token,
        tags=hashtag)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().create_book(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read_book(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("edit_form.html", action="Edit", book=book)

@crud.route('/<id>/edit-verify', methods=['GET', 'POST'])
def edit_verify(id):
    book = get_model().read_book(id)
    verify_id = ""
    verify_pw = ""

    if request.method == 'POST':
        verify_id = request.form.get('verify_id')
        verify_pw = request.form.get('verify_pw')

        if (verify_id == book['createdBy'] and verify_pw == book['createdPW']):
            return redirect(url_for('.edit', id=book['id']))
        else:
            return redirect(url_for('.failed', id=book['id']))

    return render_template("verify.html", book=book, verify_id= verify_id, verify_pw= verify_pw)

@crud.route('/<id>/delete-verify', methods=['GET', 'POST'])
def delete_verify(id):
    book = get_model().read_book(id)
    verify_id = ""
    verify_pw = ""

    if request.method == 'POST':
        verify_id = request.form.get('verify_id')
        verify_pw = request.form.get('verify_pw')

        if (verify_id == book['createdBy'] and verify_pw == book['createdPW']):
            return redirect(url_for('.delete', id=book['id']))
        else:
            return redirect(url_for('.failed', id=book['id']))

    return render_template("verify.html", book=book, verify_id= verify_id, verify_pw= verify_pw)


@crud.route('/<id>/loginfailed')
def failed(id):
    return render_template("failed.html", book_id=id)

@crud.route('/<id>/review', methods=['GET', 'POST'])
def review(id):

    book = get_model().read_book(id)

    if request.method == 'POST':

        data = request.form.to_dict(flat=True)

        review = get_model().create_review(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("review.html", review={}, book_id = id)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
