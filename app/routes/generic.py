# coding: utf-8
from flask import render_template, request, flash, redirect, url_for

from ..app import app, login, db
from ..modeles.donnees import Authorship, Cardinal, Formation, Pays, Ville, Etudes, Mission
from ..modeles.utilisateurs import User
from ..constantes import RESULTATS_PAR_PAGE
from flask_login import login_user, current_user, logout_user, login_required
# On importe or_ pour pouvoir filtrer des résultats sur de multiples éléments
from sqlalchemy import or_


@app.route("/")
def accueil():
    return render_template("pages/accueil.html")
""" Route permettant l'affichage d'une page accueil
    """
#Page redirigeant vers les ajouts de pages
@app.route("/add")
def add():
    return render_template("pages/add.html")

#Routes vers les principaux éléments de la base de données

#Les cardinaux
@app.route("/cardinal/<int:cardinal_id>")
#:param cardinal_id: Identifiant numérique du cardinal
def cardinal(cardinal_id):
    cardinal = Cardinal.query.filter(Cardinal.cardinal_id == cardinal_id).first_or_404()
    return render_template("pages/cardinal.html", cardinal=cardinal)

#Les états
@app.route("/pays/<int:pays_id>")
#:param pays_id: Identifiant numérique du pays
def pays(pays_id):
    pays = Pays.query.filter(Pays.pays_id == pays_id).first_or_404()
    return render_template("pages/pays.html", pays=pays)

#Les villes
@app.route("/ville/<int:ville_id>")
#:param pays_id: Identifiant numérique de la ville
def ville(ville_id):
    ville = Ville.query.filter(Ville.ville_id == ville_id).first_or_404()
    return render_template("pages/ville.html", ville=ville)

#Les formations
@app.route("/formation/<int:formation_id>")
#:param pays_id: Identifiant numérique de la formations
def formation(formation_id):
    formation = Formation.query.filter(Formation.formation_id == formation_id).first_or_404()
    return render_template("pages/formation.html", formation=formation)

#Les pages d'index

#L'index des cardinaux
@app.route("/index_cardinaux")
def index_cardinaux():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Cardinal.query.order_by(Cardinal.cardinal_nom).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_cardinaux.html", resultats=resultats, cardinal=cardinal)

#L'index des cardinaux romains
@app.route("/index_cardinaux_romains")
def index_cardinaux_romains():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Cardinal.query.filter(Cardinal.cardinal_ville_naissance =="Rome").paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_cardinaux_romains.html", resultats=resultats, cardinal=cardinal)

#L'index des cardinaux florentins
@app.route("/index_cardinaux_florentins")
def index_cardinaux_florentins():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Cardinal.query.filter(Cardinal.cardinal_ville_naissance =="Florence").paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_cardinaux_florentins.html", resultats=resultats, cardinal=cardinal)

#L'index des autres cardinaux
@app.route("/index_autres_cardinaux")
def index_autres_cardinaux():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = Cardinal.query.filter(or_(
        Cardinal.cardinal_ville_naissance !="Florence"),
        Cardinal.cardinal_ville_naissance !="Rome").paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_autres_cardinaux.html", resultats=resultats, cardinal=cardinal)

#L'index des États
@app.route("/index_pays")
def index_pays():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Pays.query.order_by(Pays.pays_nom).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_pays.html", resultats=resultats, pays=pays)

#L'index des villes
@app.route("/index_villes")
def index_villes():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Ville.query.order_by(Ville.ville_nom).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_villes.html", resultats=resultats, ville=ville)

#L'index des formations
@app.route("/index_formations")
def index_formations():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Formation.query.order_by(Formation.formation_cursus).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_formations.html", resultats=resultats, formation=formation)

@app.route("/recherche")
def recherche():
    #Route permettant la recherche plein-texte

    '''On préfèrera l'utilisation de .get() ici
    qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])'''
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    '''On crée une liste vide de résultat (qui restera vide par défaut
    si on n'a pas de mot clé)'''
    resultats = []

    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Cardinal.query.filter(or_(
            Cardinal.cardinal_nom.like("%{}%".format(motclef)),
            Cardinal.cardinal_prenom.like("%{}%".format(motclef)),
            Cardinal.cardinal_date_naissance.like("%{}%".format(motclef)),
            Cardinal.cardinal_date_deces.like("%{}%".format(motclef)),
            Cardinal.cardinal_pays_naissance.like("%{}%".format(motclef)),
            Cardinal.cardinal_ville_naissance.like("%{}%".format(motclef)))).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
        titre = "Résultat pour la recherche `" + motclef + "`"

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )

#Gestion des inscriptions
@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")

#Gestion de la connexion
@app.route("/connexion", methods=["POST", "GET"])
def connexion():

    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")

    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion réussie", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Identifiant ou mot de passe incorrect.", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'

#Gestion de la déconnexion
@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")

# Gérer les pages d'erreurs
#Erreur 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('erreurs/erreur404.html'), 404

#Erreur 500
@app.errorhandler(500)
def internal_error(error):
    return render_template('erreurs/erreur500.html'), 500

#Ajouter, modifier ou supprimer une page

#Ajouter une page

#Ajouter une page cardinal
@app.route("/cardinal/add", methods=["GET", "POST"])
@login_required
def cardinal_add():

    if request.method == "POST":
        statut, informations = Cardinal.cardinal_add(
            cardinal_add_nom = request.form.get("cardinal_add_nom", None),
            cardinal_add_prenom = request.form.get("cardinal_add_prenom", None),
            cardinal_add_date_naissance = request.form.get("cardinal_add_date_naissance", None),
            cardinal_add_pays_naissance = request.form.get("cardinal_add_pays_naissance", None),
            cardinal_add_ville_naissance = request.form.get("cardinal_add_ville_naissance", None),
            cardinal_add_date_deces = request.form.get("cardinal_add_date_deces", None),
        )

        if statut is True:
            flash("Cardinal supplémentaire ajouté à la base", "success")
            return redirect("/")
        else:
            flash("Echec : " + ", ".join(informations), "danger")
            return render_template("pages/cardinal_add.html")
    else:
        return render_template("pages/cardinal_add.html")

#Ajouter une page État
@app.route("/pays/add", methods=["GET", "POST"])
@login_required
def pays_add():

    if request.method == "POST":
        statut, informations = Pays.pays_add(
            pays_add_nom = request.form.get("pays_add_nom", None),
        )

        if statut is True:
            flash("État supplémentaire ajouté à la base", "success")
            return redirect("/")
        else:
            flash("Echec : " + ", ".join(informations), "danger")
            return render_template("pages/pays_add.html")
    else:
        return render_template("pages/pays_add.html")

#Ajouter une page ville
@app.route("/ville/add", methods=["GET", "POST"])
@login_required
def ville_add():

    if request.method == "POST":
        statut, informations = Ville.ville_add(
            ville_add_nom = request.form.get("ville_add_nom", None),
            ville_add_latitude = request.form.get("ville_add_latitude", None),
            ville_add_longitude=request.form.get("ville_add_longitude", None)
        )

        if statut is True:
            flash("Ville supplémentaire ajoutée à la base", "success")
            return redirect("/")
        else:
            flash("Echec : " + ", ".join(informations), "danger")
            return render_template("pages/ville_add.html")
    else:
        return render_template("pages/ville_add.html")

#Ajouter une page formation
@app.route("/formation/add", methods=["GET", "POST"])
@login_required
def formation_add():

    if request.method == "POST":
        statut, informations = Formation.formation_add(
            formation_add_cursus = request.form.get("formation_add_cursus", None),
        )

        if statut is True:
            flash("Formation supplémentaire ajoutée à la base", "success")
            return redirect("/")
        else:
            flash("Echec : " + ", ".join(informations), "danger")
            return render_template("pages/formation_add.html")
    else:
        return render_template("pages/formation_add.html")

#Ajouter des etudes
@app.route("/etudes/add", methods=["GET", "POST"])
@login_required
def etudes_add():

    if request.method == "POST":
        statut, informations = Etudes.pays_add(
            etudes_add_id_cardinal = request.form.get("etudes_add_id_cardinal", None),
            etudes_add_id_ville=request.form.get("etudes_add_id_ville", None),
            etudes_add_id_formation=request.form.get("etudes_add_id_formation", None),
        )

        if statut is True:
            flash("Etude supplémentaire ajoutée à la base", "success")
            return redirect("/")
        else:
            flash("Echec : " + ", ".join(informations), "danger")
            return render_template("pages/etudes.html")
    else:
        return render_template("pages/etudes.html")

#Ajouter une mission
@app.route("/mission/add", methods=["GET", "POST"])
@login_required
def mission_add():

    if request.method == "POST":
        statut, informations = Mission.pays_add(
            mission_add_id_cardinal = request.form.get("mission_add_id_cardinal", None),
            mission_add_id_pays=request.form.get("mission_add_id_pays", None),
            mission_add_id_ville=request.form.get("mission_add_id_ville", None),
            mission_add_date=request.form.get("mission_add_date", None),
        )

        if statut is True:
            flash("Mission supplémentaire ajoutée à la base", "success")
            return redirect("/")
        else:
            flash("Echec : " + ", ".join(informations), "danger")
            return render_template("pages/mission.html")
    else:
        return render_template("pages/mission.html")

#Modifier une page

#Modifier une page cardinal
@app.route("/cardinal/<int:cardinal_id>/update", methods=["GET", "POST"])
@login_required
def cardinal_update(cardinal_id):
    new_cardinal = Cardinal.query.get_or_404(cardinal_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        if not request.form.get("cardinal_nom", "").strip():
            erreurs.append("Insérez le nom d'un cardinal")
        if not request.form.get("cardinal_prenom", "").strip():
            erreurs.append("Insérez le prénom d'un cardinal")
        if not request.form.get("cardinal_date_naissance", "").strip():
            erreurs.append("Insérez la date de naissance d'un cardinal")
        if not request.form.get("cardinal_pays_naissance", "").strip():
            erreurs.append("Insérez l'État dans lequel le cardinal est né")
        if not request.form.get("cardinal_ville_naissance", "").strip():
            erreurs.append("Insérez la ville dans laquelle le cardinal est né")
        if not request.form.get("cardinal_date_deces", "").strip():
            erreurs.append("Insérez la date de décès d'un cardinal")

        if not erreurs:
            print("Faire ma modification")
            new_cardinal.cardinal_nom = request.form["cardinal_nom"]
            new_cardinal.cardinal_prenom = request.form["cardinal_prenom"]
            new_cardinal.cardinal_date_naissance = request.form["cardinal_date_naissance"]
            new_cardinal.cardinal_pays_naissance = request.form["cardinal_pays_naissance"]
            new_cardinal.cardinal_ville_naissance = request.form["cardinal_ville_naissance"]
            new_cardinal.cardinal_date_deces = request.form["cardinal_date_deces"]


            db.session.add(new_cardinal)
            db.session.add(Authorship(cardinal=new_cardinal, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/cardinal_update.html",
        cardinal=new_cardinal,
        erreurs=erreurs,
        updated=updated
    )

#Modifier une page pays
@app.route("/pays/<int:pays_id>/update", methods=["GET", "POST"])
@login_required
def pays_update(pays_id):
    new_pays = Pays.query.get_or_404(pays_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        if not request.form.get("pays_nom", "").strip():
            erreurs.append("Insérez le nom d'un État")

        if not erreurs:
            print("Faire ma modification")
            new_pays.pays_nom = request.form["pays_nom"]

            db.session.add(new_pays)
            db.session.add(Authorship(pays=new_pays, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/pays_update.html",
        pays=new_pays,
        erreurs=erreurs,
        updated=updated
    )

#Modifier une page ville
@app.route("/ville/<int:ville_id>/update", methods=["GET", "POST"])
@login_required
def ville_update(ville_id):
    new_ville = Ville.query.get_or_404(ville_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        if not request.form.get("ville_nom", "").strip():
            erreurs.append("Insérez le nom d'une ville")
        if not request.form.get("ville_latitude", "").strip():
            erreurs.append("Insérez la latitude d'une ville")
        if not request.form.get("ville_longitude", "").strip():
            erreurs.append("Insérez la longitude d'une ville")

        if not erreurs:
            print("Faire ma modification")
            new_ville.ville_nom = request.form["ville_nom"]
            new_ville.ville_latitude = request.form["ville_latitude"]
            new_ville.ville_longitude = request.form["ville_longitude"]

            db.session.add(new_ville)
            db.session.add(Authorship(ville=new_ville, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/ville_update.html",
        ville=new_ville,
        erreurs=erreurs,
        updated=updated
    )

#Modifier une page formation
@app.route("/formation/<int:formation_id>/update", methods=["GET", "POST"])
@login_required
def formation_update(formation_id):
    new_formation = Formation.query.get_or_404(formation_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        if not request.form.get("formation_cursus", "").strip():
            erreurs.append("Insérez le nom d'un cursus universitaire")

        if not erreurs:
            print("Faire ma modification")
            new_formation.formation_cursus = request.form["formation_cursus"]

            db.session.add(new_formation)
            db.session.add(Authorship(formation=new_formation, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/formation_update.html",
        formation=new_formation,
        erreurs=erreurs,
        updated=updated
    )

#Modifier des etudes
@app.route("/etudes/<int:etudes_id>/update", methods=["GET", "POST"])
@login_required
def etudes_update(etudes_id):
    new_etudes = Etudes.query.get_or_404(etudes_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        if not request.form.get("etudes_id_cardinal", "").strip():
            erreurs.append("Insérez un identifiant de cardinal")
        if not request.form.get("etudes_id_ville", "").strip():
            erreurs.append("Insérez un identifiant de ville")
        if not request.form.get("etudes_id_formation", "").strip():
            erreurs.append("Insérez un identifiant de formation")

        if not erreurs:
            print("Faire ma modification")
            new_etudes.etudes_id_cardinal = request.form["etudes_id_cardinal"]
            new_etudes.etudes_id_ville = request.form["etudes_id_ville"]
            new_etudes.etudes_id_formation = request.form["etudes_id_fomration"]

            db.session.add(new_etudes)
            db.session.add(Etudes(etudes=new_etudes, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/etudes.html",
        etudes=new_etudes,
        erreurs=erreurs,
        updated=updated
    )

#Modifier une mission
@app.route("/mission/<int:mission_id>/update", methods=["GET", "POST"])
@login_required
def mission_update(mission_id):
    new_mission = Mission.query.get_or_404(mission_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        if not request.form.get("mission_id_cardinal", "").strip():
            erreurs.append("Insérez un identifiant de cardinal")
        if not request.form.get("mission_id_pays", "").strip():
            erreurs.append("Insérez un identifiant d'un État")
        if not request.form.get("mission_id_ville", "").strip():
            erreurs.append("Insérez un identifiant de ville")
        if not request.form.get("mission_date", "").strip():
            erreurs.append("Insérez la date de la mission")


        if not erreurs:
            print("Faire ma modification")
            new_mission.mission_id_cardinal = request.form["mission_id_cardinal"]
            new_mission.mission_id_pays = request.form["mission_id_pays"]
            new_mission.mission_id_ville = request.form["mission_id_ville"]
            new_mission.mission_date = request.form["mission_date"]

            db.session.add(new_mission)
            db.session.add(Mission(etudes=new_mission, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/mission.html",
        mission=new_mission,
        erreurs=erreurs,
        updated=updated
    )

#Supprimer une page

#Supprimer une page cardinal
@app.route("/cardinal/<int:cardinal_id>/delete", methods=["POST", "GET"])
@login_required
def cardinal_delete(cardinal_id):

    del_cardinal = Cardinal.query.get(cardinal_id)

    if request.method == "POST":
        statut = Cardinal.cardinal_delete(
            cardinal_id=cardinal_id
        )

        if statut is True:
            flash("Le cardinal a été supprimé de la base", "success")
            return redirect("/")
        else:
            flash("Echec", "error")
            return redirect("/")
    else:
        return render_template("pages/cardinal_delete.html", del_cardinal=del_cardinal)


#Supprimer une page pays
@app.route("/pays/<int:pays_id>/delete", methods=["POST", "GET"])
@login_required
def pays_delete(pays_id):

    del_pays = Pays.query.get(pays_id)

    if request.method == "POST":
        statut = Pays.pays_delete(
            pays_id=pays_id
        )

        if statut is True:
            flash("L'État a été supprimé de la base", "success")
            return redirect("/")
        else:
            flash("Echec", "error")
            return redirect("/")
    else:
        return render_template("pages/pays_delete.html", del_pays=del_pays)

#Supprimer une page ville
@app.route("/ville/<int:ville_id>/delete", methods=["POST", "GET"])
@login_required
def ville_delete(ville_id):

    del_ville = Ville.query.get(ville_id)

    if request.method == "POST":
        statut = Ville.ville_delete(
            ville_id=ville_id
        )

        if statut is True:
            flash("La ville a été supprimée de la base", "success")
            return redirect("/")
        else:
            flash("Echec", "error")
            return redirect("/")
    else:
        return render_template("pages/ville_delete.html", del_ville=del_ville)

#Supprimer une page formation
@app.route("/formation/<int:formation_id>/delete", methods=["POST", "GET"])
@login_required
def formation_delete(formation_id):

    del_formation = Formation.query.get(formation_id)

    if request.method == "POST":
        statut = Formation.formation_delete(
            formation_id=formation_id
        )

        if statut is True:
            flash("La formation a été supprimée de la base", "success")
            return redirect("/")
        else:
            flash("Echec", "error")
            return redirect("/")
    else:
        return render_template("pages/formation_delete.html", del_formation=del_formation)

#Supprimer des etudes
@app.route("/etudes/<int:etudes_id>/delete", methods=["POST", "GET"])
@login_required
def etudes_delete(etudes_id):

    del_etudes = Etudes.query.get(etudes_id)

    if request.method == "POST":
        statut = Etudes.etudes_delete(
            etudes_id=etudes_id
        )

        if statut is True:
            flash("Les études ont été supprimées de la base", "success")
            return redirect("/")
        else:
            flash("Echec", "error")
            return redirect("/")
    else:
        return render_template("pages/etudes.html", del_etudes=del_etudes)

#Supprimer une mission
@app.route("/mission/<int:mission_id>/delete", methods=["POST", "GET"])
@login_required
def mission_delete(mission_id):

    del_mission = Mission.query.get(mission_id)

    if request.method == "POST":
        statut = Mission.mission_delete(
            mission_id=mission_id
        )

        if statut is True:
            flash("La mission a été supprimée de la base", "success")
            return redirect("/")
        else:
            flash("Echec", "error")
            return redirect("/")
    else:
        return render_template("pages/mission.html", del_mission=del_mission)