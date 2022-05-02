# coding: utf-8
'''from flask import render_template, request, url_for, jsonify
#from urllib.parse import urlencode
#from urlparse import urlparse

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

from app.app import app
from app.constantes import RESULTATS_PAR_PAGE, API_ROUTE
from app.modeles.donnees import Cardinal, Pays, Ville, Formation, Etudes, Mission


def Json_404():
    response = jsonify({"erreur": "Unable to perform the query"})
    response.status_code = 404
    return response


@app.route(API_ROUTE+"/cardinal/<cardinal_id>")
def api_cardinal_single(cardinal_id):
    try:
        query = Cardinal.query.get(cardinal_id)
        return jsonify(query.to_jsonapi_dict())
    except:
        return Json_404()


@app.route(API_ROUTE+"/cardinal")
def api_cardinal_browse():
    """ Route permettant la recherche plein-texte

    On s'inspirera de http://jsonapi.org/ faute de pouvoir trouver temps d'y coller à 100%
    """
    # q est très souvent utilisé pour indiquer une capacité de recherche
    motclef = request.args.get("q", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if motclef:
        query = Cardinal.query.filter(
            Cardinal.cardinal_nom.like("%{}%".format(motclef))
        )
    else:
        query = Cardinal.query

    try:
        resultats = query.paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    except Exception:
        return Json_404()

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            cardinal.to_jsonapi_dict()
            for cardinal in resultats.items
        ]
    }

    if resultats.has_next:
        arguments = {
            "page": resultats.next_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["next"] = url_for("api_cardinal_browse", _external=True)+"?"+urlparse(arguments)

    if resultats.has_prev:
        arguments = {
            "page": resultats.prev_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["prev"] = url_for("api_cardinal_browse", _external=True)+"?"+urlparse(arguments)

    response = jsonify(dict_resultats)
    return response'''
