import os
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)

from werkzeug.exceptions import abort

from mygdr.db import get_db

bp = Blueprint('gdr', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            db.execute(
                "INSERT INTO user (username) VALUES (?)",
                (username,),
            )
            db.commit()
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

        if error is not None:
            flash(error)
        else:
            session.clear()
            session['user_id'] = user['id']

            print(g.user)
            return redirect(url_for('gdr.index'))
        
    return render_template('gdr/index.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
	).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('gdr.index'))
        
# @bp.route('/genus')
# def index_genus():
#     species = get_species_with_filter()
#     genera = get_genera_with_filter()
#     families = get_families_with_filter()
#     orders = get_orders_with_filter()
#     figpaths = get_figpaths_by_species(genera, "g_id")

#     return render_template('gdr/genus/index.html', genera=genera, figpaths=figpaths,
#                            nsp=len(species), nfa=len(families), nor=len(orders))

# @bp.route('/family')
# def index_family():
#     species = get_species_with_filter()
#     genera = get_genera_with_filter()
#     families = get_families_with_filter()
#     orders = get_orders_with_filter()
#     figpaths = get_figpaths_by_species(families, "f_id")

#     return render_template('gdr/family/index.html', families=families, figpaths=figpaths,
#                            nsp=len(species), nge=len(genera), nor=len(orders))

# @bp.route('/order')
# def index_order():
#     species = get_species_with_filter()
#     genera = get_genera_with_filter()
#     families = get_families_with_filter()
#     orders = get_orders_with_filter()
#     figpaths = get_figpaths_by_species(orders, "o_id")

#     return render_template('gdr/order/index.html', orders=orders, figpaths=figpaths,
#                            nsp=len(species), nge=len(genera), nfa=len(families))


# from urllib.parse import unquote

# @bp.route('/<string:title>/', methods=(['GET']))
# def view(title):
#     title = unquote(title)
#     spec = get_one_spec_with_filter('s.title', title)
#     previous_to_next = get_previous_to_next('species', 'title', title, 'modified DESC, id DESC')

#     error = None
#     if not spec or previous_to_next is None:
#         error = 'Cannot find species: %s' % title
#     if error is not None:
#         flash(error)

#     figs = get_figures_with_filter('s.title', title)

#     return render_template('gdr/view.html', spec=spec, figs=figs,
#                            title_previous=previous_to_next[0]["title"], title_next=previous_to_next[2]["title"])

# @bp.route('/genus/<string:title>/', methods=(['GET']))
# def view_genus(title):
#     genus = get_one_genus_with_filter('g.title', title)
#     previous_to_next = get_previous_to_next('genera', 'title', title, 'title ASC')
#     species = get_species_with_filter('g.title', title)
#     figpaths = get_figpaths_by_species(species, "s_id")

#     return render_template('gdr/genus/view.html', species=species, figpaths=figpaths, genus=genus,
#                            title_previous=previous_to_next[0]["title"], title_next=previous_to_next[2]["title"])

# @bp.route('/family/<string:title>/', methods=(['GET']))
# def view_family(title):
#     family = get_one_family_with_filter('f.title', title)
#     previous_to_next = get_previous_to_next('families', 'title', title, 'title ASC')
#     genera = get_genera_with_filter('f.title', title)
#     species = get_species_with_filter('f.title', title)
#     figpaths = get_figpaths_by_species(genera, "g_id")

#     return render_template('gdr/family/view.html', species=species, figpaths=figpaths, genera=genera, family=family,
#                            title_previous=previous_to_next[0]["title"], title_next=previous_to_next[2]["title"])

# @bp.route('/order/<string:title>/', methods=(['GET']))
# def view_order(title):
#     order = get_one_order_with_filter('o.title', title)
#     previous_to_next = get_previous_to_next('orders', 'title', title, 'title ASC')
#     families = get_families_with_filter('o.title', title)
#     genera = get_genera_with_filter('o.title', title)
#     species = get_species_with_filter('o.title', title)
#     figpaths = get_figpaths_by_species(families, "f_id")

#     return render_template('gdr/order/view.html', species=species, figpaths=figpaths, genera=genera, families=families, order=order,
#                            title_previous=previous_to_next[0]["title"], title_next=previous_to_next[2]["title"])

# @bp.route('/clade/<string:title>/', methods=(['GET']))
# def view_clade(title):
#     clade = get_one_clade_with_filter('c.title', title)
#     orders = get_orders_with_filter('c.title', title)
#     families = get_families_with_filter('c.title', title)
#     genera = get_genera_with_filter('c.title', title)
#     species = get_species_with_filter('c.title', title)
#     figpaths = get_figpaths_by_species(orders, "o_id")

#     return render_template('gdr/clade/view.html', species=species, figpaths=figpaths, genera=genera, families=families, orders=orders, clade=clade)


# def create_template(table, table_parent, default_redirect, update_html):
#     parents = get_all_nojoin(table_parent)
#     if request.method == 'POST':
#         title = request.form['title']
#         title_cn = None if request.form['title_cn'].strip()=="" else request.form['title_cn']
#         title_en = None if request.form['title_en'].strip()=="" else request.form['title_en']
#         link = "https://en.wikipedia.org/wiki/%s" % title.strip().replace(" ", "_")
#         body = request.form['body']
#         parent_id = request.form['parent_id']
#         if table == "species":
#             native_to = request.form['native_to']

#         error = None
        
#         if not title:
#             error = 'Binomial nomenclature is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO '+table+' (title, title_cn, title_en, link, body, parent_id)'
#                 ' VALUES (?, ?, ?, ?, ?, ?)',
#                 (title, title_cn, title_en, link, body, parent_id)
#             )
#             if table == "species":
#                 db.execute('UPDATE '+table+' SET native_to = ? WHERE title = ?', (native_to, title))
#             db.commit()
            
#             url_redirect = url_for(default_redirect, title=title)
#             if request.args.get('redirect'):
#                 url_redirect = request.args.get('redirect')
#             return redirect(url_redirect)

#     return render_template(update_html, parents=parents)


# @bp.route('/create', methods=(['GET', 'POST']))
# @admin_required
# def create():
#     return create_template('species', 'genera', 'gdr.view', 'gdr/create.html')

# @bp.route('/genus/create', methods=(['GET', 'POST']))
# @admin_required
# def create_genus():
#     return create_template('genera', 'families', 'gdr.view_genus', 'gdr/genus/create.html')

# @bp.route('/family/create', methods=(['GET', 'POST']))
# @admin_required
# def create_family():
#     return create_template('families', 'orders', 'gdr.view_family', 'gdr/family/create.html')

# @bp.route('/order/create', methods=(['GET', 'POST']))
# @admin_required
# def create_order():
#     return create_template('orders', 'clades', 'gdr.view_order', 'gdr/order/create.html')


# def update_template(id, table, table_parent, default_redirect, update_html):
#     item = get_one_nojoin(table, 'id', id)
#     parents = get_all_nojoin(table_parent)
    
#     if request.method == 'POST':
#         title = item["title"]
#         link = item["link"]
#         parent_id = item["parent_id"]
#         body = item["body"]
#         if g.user["permission"] > 10:
#             title = request.form['title'].strip()
#             link = "https://en.wikipedia.org/wiki/%s" % title.strip().replace(" ", "_")
#             parent_id = request.form['parent_id']
#             body = request.form['body']
#         title_cn = None if request.form['title_cn'].strip()=="" else request.form['title_cn']
#         title_en = None if request.form['title_en'].strip()=="" else request.form['title_en']
#         if table == "species":
#             native_to = request.form['native_to']

#         error = None
    
#         if not title or title == "":
#             error = 'Title is required.'
        
#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE '+table+' SET title = ?, title_cn = ?, title_en = ?, parent_id = ?, link = ?, body = ?, modified = ?'
#                 ' WHERE id = ?',
#                 (title, title_cn, title_en, parent_id, link, body, datetime.now(), id)
#             )
#             if table == "species":
#                 db.execute('UPDATE '+table+' SET native_to = ? WHERE id = ?', (native_to, id))
#             db.commit()
            
#             url_redirect = url_for(default_redirect, title=title)
#             if request.args.get('redirect'):
#                 url_redirect = request.args.get('redirect')
#             return redirect(url_redirect)

#     return render_template(update_html, item=item, parents=parents)


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @editor_required
# def update(id):
#     return update_template(id, 'species', 'genera', 'gdr.view', 'gdr/update.html')

# @bp.route('/genus/<int:id>/update', methods=('GET', 'POST'))
# @editor_required
# def update_genus(id):
#     return update_template(id, 'genera', 'families', 'gdr.view_genus', 'gdr/genus/update.html')

# @bp.route('/family/<int:id>/update', methods=('GET', 'POST'))
# @editor_required
# def update_family(id):
#     return update_template(id, 'families', 'orders', 'gdr.view_family', 'gdr/family/update.html')

# @bp.route('/order/<int:id>/update', methods=('GET', 'POST'))
# @editor_required
# def update_order(id):
#     return update_template(id, 'orders', 'clades', 'gdr.view_order', 'gdr/order/update.html')


# def destroy_photo(id):
#     filename = get_one_nojoin('figures', 'id', id)["path_to"]
#     if filename:
#         filename = re.sub(r'.*/', "", filename)
#         fullname = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
#         if os.path.exists(fullname):
#             os.remove(fullname)

#     db = get_db()
#     db.execute('DELETE FROM figures WHERE id = ?', (id,))
#     db.commit()

    
# def delete_template(id, table, default_redirect, default_redirect_error):
#     children = get_direct_children(id, table)

#     error = None
    
#     if table == "species":
#         for fig in children:
#             destroy_photo(fig["i_id"])
#     else:
#         if len(children) > 0:
#             error = 'Cannot delete this record, because there are children records linked to it.'

#     if error is not None:
#         flash(error)
#     else:
#         db = get_db()
#         db.execute('DELETE FROM '+table+' WHERE id = ?', (id,))
#         db.commit()
#         return redirect(default_redirect)

#     return redirect(default_redirect_error)


# @bp.route('/<int:id>/delete', methods=('POST',))
# @admin_required
# def delete(id):
#     title = get_one_nojoin('species', 'id', id)["title"]
#     return delete_template(id, "species", url_for('gdr.index'), url_for('gdr.view', title=title))

# @bp.route('/genus/<int:id>/delete', methods=('POST',))
# @admin_required
# def delete_genus(id):
#     title = get_one_nojoin('genera', 'id', id)["title"]
#     return delete_template(id, "genera", url_for('gdr.index_genus'), url_for('gdr.view_genus', title=title))

# @bp.route('/family/<int:id>/delete', methods=('POST',))
# @admin_required
# def delete_family(id):
#     title = get_one_nojoin('families', 'id', id)["title"]
#     return delete_template(id, "families", url_for('gdr.index_family'), url_for('gdr.view_family', title=title))

# @bp.route('/order/<int:id>/delete', methods=('POST',))
# @admin_required
# def delete_order(id):
#     title = get_one_nojoin('orders', 'id', id)["title"]
#     return delete_template(id, "orders", url_for('gdr.index_order'), url_for('gdr.view_order', title=title))


# @bp.route('/<string:title>/add_photo', methods=(['GET', 'POST']))
# @admin_required
# def add_photo(title):
#     title = unquote(title)
#     spec = get_one_nojoin('species', 'title', title)
#     title_cn = spec["title_cn"]
#     if request.method == 'POST':
#         taken_on = request.form['taken_on']
#         taken_at = request.form['taken_at']
#         parent_id = spec["id"]
#         path_to = None

#         error = None

#         if 'file' not in request.files:
#             error = 'File is required.'
#         else:
#             ifile = request.files['file']
#             filename = secure_filename(ifile.filename)
#             fullname = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
#             if not allowed_file(filename):
#                 error = 'Extensions allowed: %s' % str(ALLOWED_EXTENSIONS)
#             elif os.path.exists(fullname):
#                 error = '%s already exists. Change the file name.' % filename

#             ifile.save(fullname)
#             path_to = fullname.replace(current_app.config['FROM_STATIC'], "")
            
#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO figures (path_to, taken_on, taken_at, parent_id)'
#                 ' VALUES (?, ?, ?, ?)',
#                 (path_to, taken_on, taken_at, parent_id)
#             )
#             db.execute(
#                 'UPDATE species SET modified = ? WHERE id = ?',
#                 (datetime.now(), parent_id)
#             )
#             db.commit()

#             # return redirect(url_for('gdr.view', title=title))
#             url_redirect = url_for('gdr.view', title=title)
#             if request.args.get('redirect'):
#                 url_redirect = request.args.get('redirect')
#             return redirect(url_redirect)
        
#     return render_template('gdr/add_photo.html', s_title=title, s_title_cn=title_cn)


# @bp.route('/<string:title>/photo/<int:id>/update', methods=('GET', 'POST'))
# @admin_required
# def update_photo(id, title):
#     title = unquote(title)
#     fig = get_one_nojoin('figures', 'id', id)    
#     if request.method == 'POST':
#         taken_on = request.form['taken_on']
#         taken_at = request.form['taken_at']
#         body = request.form['body']
        
#         error = None
#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE figures SET taken_on = ?, taken_at = ?, body = ? WHERE id = ?',
#                 (taken_on, taken_at, body, id)
#             )
#             db.commit()
#             # return redirect(url_for('gdr.view', title=title))
#             url_redirect = url_for('gdr.view', title=title)
#             if request.args.get('redirect'):
#                 url_redirect = request.args.get('redirect')
#             return redirect(url_redirect)
        
#     return render_template('gdr/update_photo.html', fig=fig, s_title=title)


# @bp.route('/<string:title>/photo/<int:id>/delete', methods=('POST',))
# @admin_required
# def delete_photo(id, title):
#     title = unquote(title)
#     destroy_photo(id)

#     return redirect(url_for('gdr.view', title=title))


# @bp.route('/search')
# def search():
#     skey = unquote(request.args.get('skey'))
#     species = get_db().execute(
#         'SELECT s.id AS s_id, s.title AS s_title, s.title_cn AS s_title_cn, s.title_en AS s_title_en'
#         ' FROM species s'
#         ' WHERE instr(lower(s.title), lower(?)) > 0 OR instr(lower(s.title_cn), lower(?)) > 0 OR instr(lower(s.title_en), lower(?)) > 0',
#         (skey, skey, skey)
#     ).fetchall()
#     figpaths = get_figpaths_by_species(species, "s_id")

#     return render_template('gdr/search.html', species=species, figpaths=figpaths, skey=skey)

