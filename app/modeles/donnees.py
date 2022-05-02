# coding: utf-8
import datetime
from flask import url_for
from app.app import db


class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_cardinal_id = db.Column(db.Integer, db.ForeignKey('cardinal.cardinal_id'))
    authorship_formation_id = db.Column(db.Integer, db.ForeignKey('formation.formation_id'))
    authorship_pays_id = db.Column(db.Integer, db.ForeignKey('pays.pays_id'))
    authorship_ville_id = db.Column(db.Integer, db.ForeignKey('ville.ville_id'))
    authorship_etudes_id = db.Column(db.Integer, db.ForeignKey('etudes.etudes_id'))
    authorship_mission_id = db.Column(db.Integer, db.ForeignKey('mission.mission_id'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    cardinal = db.relationship("Cardinal", back_populates="authorships")
    formation = db.relationship("Formation", back_populates="authorships")
    pays = db.relationship("Pays", back_populates="authorships")
    ville = db.relationship("Ville", back_populates="authorships")
    etudes = db.relationship("Etudes", back_populates="authorships")
    mission = db.relationship("Mission", back_populates="authorships")
    user = db.relationship("User", back_populates="authorships")

    def author_to_json(self):
        return {
            "author": self.user.to_jsonapi_dict(),
            "on": self.authorship_date
        }


# On crée notre modèle
class Cardinal(db.Model):
    #__table_args__ = {'extend_existing': True}
    __tablename__ = "cardinal"
    cardinal_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    cardinal_nom = db.Column(db.Text, nullable=False)
    cardinal_prenom = db.Column(db.Text)
    cardinal_date_naissance = db.Column(db.Text)
    cardinal_date_deces = db.Column(db.Text)
    cardinal_pays_naissance = db.Column(db.Text)
    cardinal_ville_naissance = db.Column(db.Text)
    etudes = db.relationship("Etudes", back_populates="cardinal")
    mission = db.relationship("Mission", back_populates="cardinal")
    authorships = db.relationship("Authorship", back_populates="cardinal")

    #Cette méthode permet de pouvoir ajouter un cardinal à la base de données.
    @staticmethod
    def cardinal_add(cardinal_add_nom, cardinal_add_prenom, cardinal_add_date_naissance,cardinal_add_pays_naissance, cardinal_add_ville_naissance, cardinal_add_date_deces):
        erreurs = []
        if not cardinal_add_nom:
            erreurs.append("Merci d'indiquer le nom du cardinal")
        if not cardinal_add_prenom:
            erreurs.append( "Merci d'indiquer le prénom du cardinal")
        if not cardinal_add_date_naissance:
            erreurs.append("Merci d'indiquer la date de naissance du cardinal")
        if not cardinal_add_pays_naissance:
            erreurs.append("Merci d'indiquer l'État de naissance du cardinal")
        if not cardinal_add_ville_naissance:
            erreurs.append("Merci d'indiquer la ville de naissance du cardinal")
        if not cardinal_add_date_deces:
           erreurs.append("Merci d'indiquer la date de décès du cardinal")


        # Afficher un message d'erreur si au moins une erreur survient.
        if len(erreurs) > 0:
            return False, erreurs

        # Dans le cas où il n'y a aucune erreur, ajouter des nouvelles données dans la table Cardinal.
        new_cardinal = Cardinal(cardinal_nom=cardinal_add_nom,
                                cardinal_date_naissance=cardinal_add_date_naissance,
                                cardinal_pays_naissance=cardinal_add_pays_naissance,
                                cardinal_ville_naissance=cardinal_add_ville_naissance,
                                cardinal_date_deces=cardinal_add_date_deces,)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(new_cardinal)
            db.session.commit()
            return True, new_cardinal

        except Exception as erreur:
            return False, [str(erreur)]

    # Cette méthode permet de pouvoir mettre à jour les informations liées à un cardinal dans la base de données.
    @staticmethod
    def cardinal_update(cardinal_nom, cardinal_prenom, cardinal_date_naissance, cardinal_pays_naissance, cardinal_ville_naissance,cardinal_date_deces):
        erreurs = []
        if not cardinal_nom:
            erreurs.append("Veuillez renseigner le nom du cardinal")
        if not cardinal_prenom:
            erreurs.append("Veuillez renseigner le prénom du cardinal")
        if not cardinal_date_naissance:
            erreurs.append("Veuillez renseigner la date de naissance du cardinal")
        if not cardinal_pays_naissance:
            erreurs.append("Veuillez renseigner l'État dans lequel le cardinal est né")
        if not cardinal_ville_naissance:
            erreurs.append("Veuillez renseigner la ville dans laquelle le cardinal est né")
        if not cardinal_date_deces:
            erreurs.append("Veuillez renseigner la date de décès du cardinal")

        # S'il y a au moins une erreur.
        if len(erreurs) > 0:
            return False, erreurs

        # Récupération d'un cardinal dans la base.
        update_cardinal = Cardinal.query.get(cardinal_id)

        #Vérification de la modification d'au moins un élément.
        if update_cardinal.cardinal_nom == cardinal_nom \
                and update_cardinal.cardinal_prenom == cardinal_prenom \
                and update_cardinal.cardinal_date_naissance == cardinal_date_naissance \
                and update_cardinal.cardinal_pays_naissance == cardinal_pays_naissance \
                and update_cardinal.cardinal_ville_naissance == cardinal_ville_naissance \
                and update_cardinal.cardinal_date_deces == cardinal_date_deces:
            erreurs.append("No edit was submitted")

        if len(erreurs) > 0:
            return False, erreurs

        else:
            # Mise à jour des informations
            update_cardinal.cardinal_prenom = cardinal_prenom
            update_cardinal.cardinal_date_naissance = cardinal_date_naissance
            update_cardinal.cardinal_pays_naissance = cardinal_pays_naissance
            update_cardinal.cardinal_ville_naissance = cardinal_ville_naissance
            update_cardinal.cardinal_date_deces = cardinal_date_deces

        try:
            # On l'ajoute au transport vers la base de données.
            db.session.add(update_cardinal)
            # On envoie le paquet.
            db.session.commit()

            # On renvoie les informations du site.
            return True, update_cardinal
        except Exception as erreur:
            return False, [str(erreur)]


#Cette méthode permet de supprimer un cardinal de la base de données.
    @staticmethod
    def cardinal_delete(cardinal_id):

        del_cardinal = Cardinal.query.get(cardinal_id)

        try:
            db.session.delete(del_cardinal)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]

    def cardinal_to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type":"cardinal",
            "id": self.cardinal_id,
            "attributes": {
                "name": self.cardinal_nom,
                "fistname": self.cardinal_prenom,
                "datenaissance": self.cardinal_date_naissance,
                "datedeces": self.cardinal_date_deces
            },
            "links": {
                "self": url_for("cardinal", cardinal_id=self.cardinal_id, _external=True),
                "json": url_for("api_cardinal_single", cardinal_id=self.cardinal_id, _external=True)
            },
            "relationships": {
                "editions": [
                    author.author_to_json()
                    for author in self.authorships
                ]
            }
        }

# On crée notre modèle
class Formation(db.Model):
    # __table_args__ = {'extend_existing': True}
    __tablename__ = "formation"
    formation_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    formation_cursus = db.Column(db.Text)
    etudes = db.relationship("Etudes", back_populates="formation")
    authorships = db.relationship("Authorship", back_populates="formation")

    # Cette méthode permet de pouvoir ajouter une formation à la base de données.
    @staticmethod
    def formation_add(formation_add_cursus):
        erreurs = []
        if not formation_add_cursus:
            erreurs.append("Merci d'indiquer le nom de la formation")

        # Afficher un message d'erreur si au moins une erreur survient.
        if len(erreurs) > 0:
            return False, erreurs

        # Dans le cas où il n'y a aucune erreur, ajouter des nouvelles données dans la table Formation.
        new_formation = Formation(formation_cursus=formation_add_cursus)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(new_formation)
            db.session.commit()
            return True, new_formation

        except Exception as erreur:
            return False, [str(erreur)]

    # Cette méthode permet de pouvoir mettre à jour les informations liées à une formation dans la base de données.
    @staticmethod
    def formation_update(formation_cursus):
        erreurs = []
        if not formation_cursus:
            erreurs.append("Veuillez renseigner un cursus universitaire")


        # S'il y a au moins une erreur.
        if len(erreurs) > 0:
            return False, erreurs

        # Récupération d'une formation dans la base.
        update_formation = Formation.query.get(formation_id)

        # Vérification de la modification d'au moins un élément.
        if update_formation.formation_cursus == formation_cursus:

            erreurs.append("No edit was submitted")

        if len(erreurs) > 0:
            return False, erreurs

        else:
            # Mise à jour des informations
            update_formation.formation_cursus = formation_cursus

        try:
            # On l'ajoute au transport vers la base de données.
            db.session.add(update_formation)
            # On envoie le paquet.
            db.session.commit()

            # On renvoie les informations du site.
            return True, update_formation
        except Exception as erreur:
            return False, [str(erreur)]

    # Cette méthode permet de supprimer une formation de la base de données.
    @staticmethod
    def formation_delete(formation_id):

        del_formation = Formation.query.get(formation_id)

        try:
            db.session.delete(del_formation)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]

    def formation_to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "formation",
            "id": self.formation_id,
            "attributes": {
                "cursus": self.formation_formation,
            },
            "links": {
                "self": url_for("formation", formation_id=self.formation_id, _external=True),
                "json": url_for("api_formation_single", formation_id=self.formation_id, _external=True)
            },
            "relationships": {
                "editions": [
                    author.author_to_json()
                    for author in self.authorships
                ]
            }
        }

# On crée notre modèle
class Pays(db.Model):
    # __table_args__ = {'extend_existing': True}
    __tablename__ = "pays"
    pays_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    pays_nom = db.Column(db.Text)
    mission = db.relationship("Mission", back_populates="pays")
    authorships = db.relationship("Authorship", back_populates="pays")

    # Cette méthode permet de pouvoir ajouter un pays à la base de données.
    @staticmethod
    def pays_add(pays_add_nom):
            erreurs = []
            if not pays_add_nom:
                erreurs.append("Merci d'indiquer le nom du pays")

            # Afficher un message d'erreur si au moins une erreur survient.
            if len(erreurs) > 0:
                return False, erreurs

            # Dans le cas où il n'y a aucune erreur, ajouter des nouvelles données dans la table Pays.
            new_pays = Pays(pays_nom=pays_add_nom)

            # Tentative d'ajout qui sera stoppée si une erreur apparaît.
            try:
                db.session.add(new_pays)
                db.session.commit()
                return True, new_pays

            except Exception as erreur:
                return False, [str(erreur)]

    # Cette méthode permet de pouvoir mettre à jour les informations liées à un État dans la base de données.
    @staticmethod
    def pays_update(pays_nom):
        erreurs = []
        if not pays_nom:
            erreurs.append("Veuillez renseigner le nom d'un État")


        # S'il y a au moins une erreur.
        if len(erreurs) > 0:
            return False, erreurs

        # Récupération d'un État dans la base.
        update_pays = Pays.query.get(pays_id)

        # Vérification de la modification d'au moins un élément.
        if update_pays.pays_nom == pays_nom:

            erreurs.append("No edit was submitted")

        if len(erreurs) > 0:
            return False, erreurs

        else:
            # Mise à jour des informations
            update_pays.pays_nom = pays_nom

        try:
            # On l'ajoute au transport vers la base de données.
            db.session.add(update_pays)
            # On envoie le paquet.
            db.session.commit()

            # On renvoie les informations du site.
            return True, update_pays
        except Exception as erreur:
            return False, [str(erreur)]

    # Cette méthode permet de supprimer un pays de la base de données.
    @staticmethod
    def pays_delete(pays_id):

        del_pays = Pays.query.get(pays_id)

        try:
            db.session.delete(del_pays)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]

    def pays_to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "pays",
             "id": self.pays_id,
             "attributes": {
                 "name": self.pays_nom
            },
            "links": {
                "self": url_for("pays", pays_id=self.pays_id, _external=True),
                "json": url_for("api_pays_single", pays_id=self.pays_id, _external=True)
            },
            "relationships": {
                "editions": [
                    author.author_to_json()
                    for author in self.authorships
                ]
            }
        }

# On crée notre modèle
class Ville(db.Model):
    # __table_args__ = {'extend_existing': True}
    __tablename__ = "ville"
    ville_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    ville_nom = db.Column(db.Text)
    ville_latitude = db.Column(db.Integer)
    ville_longitude = db.Column(db.Integer)
    etudes = db.relationship("Etudes", back_populates="ville")
    mission = db.relationship("Mission", back_populates="ville")
    authorships = db.relationship("Authorship", back_populates="ville")

    # Cette méthode permet de pouvoir ajouter une ville à la base de données.
    @staticmethod
    def ville_add(ville_add_nom, ville_add_latitude, ville_add_longitude):
        erreurs = []
        if not ville_add_nom:
            erreurs.append("Merci d'indiquer le nom de la ville")
        if not ville_add_latitude:
            erreurs.append("Merci d'indiquer la latitude correspondant à la ville")
        if not ville_add_longitude:
            erreurs.append("Merci d'indiquer la longitude correspondant à la ville")

        # Afficher un message d'erreur si au moins une erreur survient.
        if len(erreurs) > 0:
            return False, erreurs

        # Dans le cas où il n'y a aucune erreur, ajouter des nouvelles données dans la table Ville.
        new_ville = Ville(ville_nom=ville_add_nom,ville_latitude=ville_add_latitude, ville_longitude=ville_add_longitude)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(new_ville)
            db.session.commit()
            return True, new_ville

        except Exception as erreur:
            return False, [str(erreur)]

    # Cette méthode permet de pouvoir mettre à jour les informations liées à une ville dans la base de données.
    @staticmethod
    def ville_update(ville_nom, ville_latitude, ville_longitude):
        erreurs = []
        if not ville_nom:
            erreurs.append("Veuillez renseigner le nom d'une ville")
        if not ville_latitude:
            erreurs.append("Veuillez renseigner la latitude d'une ville")
        if not ville_longitude:
            erreurs.append("Veuillez renseigner la longitude d'une ville")

        # S'il y a au moins une erreur.
        if len(erreurs) > 0:
            return False, erreurs

        # Récupération d'une ville dans la base.
        update_ville = Ville.query.get(ville_id)

        # Vérification de la modification d'au moins un élément.
        if update_ville.ville_nom == ville_nom \
            and update_ville.ville_latitude == ville_latitude \
            and update_ville.ville_longitude == ville_longitude:
            erreurs.append("No edit was submitted")

        if len(erreurs) > 0:
            return False, erreurs

        else:
            # Mise à jour des informations
            update_ville.ville_nom = ville_nom
            update_ville.ville_latitude = ville_latitude
            update_ville.ville_longitude = ville_longitude
        try:
            # On l'ajoute au transport vers la base de données.
            db.session.add(update_ville)
            # On envoie le paquet.
            db.session.commit()

            # On renvoie les informations du site.
            return True, update_ville
        except Exception as erreur:
            return False, [str(erreur)]

    # Cette méthode permet de supprimer une ville de la base de données.
    @staticmethod
    def ville_delete(ville_id):

        del_ville = Ville.query.get(ville_id)

        try:
            db.session.delete(del_ville)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]

    def ville_to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "ville",
            "id": self.ville_id,
            "attributes": {
                "name": self.ville_nom,
                "latitude": self.ville_latitude,
                "longitude": self.ville_longitude
            },
            "links": {
                "self": url_for("ville", ville_id=self.ville_id, _external=True),
                "json": url_for("api_ville_single", ville_id=self.ville_id, _external=True)
            },
            "relationships": {
                "editions": [
                    author.author_to_json()
                    for author in self.authorships
                ]
            }
        }

# On crée notre modèle
class Etudes(db.Model):
    # __table_args__ = {'extend_existing': True}
    __tablename__ = "etudes"
    etudes_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    etudes_id_cardinal = db.Column(db.Integer, db.ForeignKey('cardinal.cardinal_id'))
    etudes_id_formation = db.Column(db.Integer, db.ForeignKey('formation.formation_id'))
    etudes_id_ville = db.Column(db.Integer, db.ForeignKey('ville.ville_id'))
    cardinal = db.relationship("Cardinal", back_populates="etudes")
    formation = db.relationship("Formation", back_populates="etudes")
    ville = db.relationship("Ville", back_populates="etudes")
    authorships = db.relationship("Authorship", back_populates="etudes")

    # Cette méthode permet de pouvoir ajouter des études à la base de données.
    @staticmethod
    def etudes_add(etudes_add_id_cardinal, etudes_add_id_formation, etudes_add_id_ville):
        erreurs = []
        if not etudes_add_id_cardinal:
            erreurs.append("Merci d'indiquer l'identifiant du cardinal")
        if not etudes_add_id_formation:
            erreurs.append("Merci d'indiquer l'identifiant de la formation")
        if not etudes_add_id_ville:
            erreurs.append("Merci d'indiquer l'identifiant de la ville")

        # Afficher un message d'erreur si au moins une erreur survient.
        if len(erreurs) > 0:
            return False, erreurs

        # Dans le cas où il n'y a aucune erreur, ajouter des nouvelles données dans la table Etudes.
        new_etudes = Etudes(etudes_id_cardinal=etudes_add_id_cardinal, etudes_id_formation=etudes_add_id_formation, etudes_id_ville=etudes_add_id_ville)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(new_etudes)
            db.session.commit()
            return True, new_etudes

        except Exception as erreur:
            return False, [str(erreur)]

    # Cette méthode permet de pouvoir mettre à jour les informations liées aux études d'un cardinal dans la base de données.
    @staticmethod
    def etudes_update(etudes_id_cardinal, etudes_id_formation, etudes_id_ville):
        erreurs = []
        if not etudes_id_cardinal:
            erreurs.append("Veuillez renseigner l'identifiant d'un cardinal'")
        if not etudes_id_formation:
            erreurs.append("Veuillez renseigner l'identifiant d'une formation'")
        if not etudes_id_ville:
            erreurs.append("Veuillez renseigner l'identifiant d'une ville")

        # S'il y a au moins une erreur.
        if len(erreurs) > 0:
            return False, erreurs

        # Récupération des études dans la base.
        update_etudes = Etudes.query.get(etudes_id)

        # Vérification de la modification d'au moins un élément.
        if update_etudes.etudes_id_cardinal == etudes_id_cardinal \
            and update_etudes.etudes_id_formation == etudes_id_formation \
            and update_etudes.etudes_id_ville == etudes_id_ville:
            erreurs.append("No edit was submitted")

        if len(erreurs) > 0:
            return False, erreurs

        else:
            # Mise à jour des informations
            update_etudes.etudes_id_cardinal = etudes_id_cardinal
            update_etudes.etudes_id_formation = etudes_id_formation
            update_etudes.etudes_id_ville = etudes_id_ville
        try:
            # On l'ajoute au transport vers la base de données.
            db.session.add(update_etudes)
            # On envoie le paquet.
            db.session.commit()

            # On renvoie les informations du site.
            return True, update_etudes
        except Exception as erreur:
            return False, [str(erreur)]

    # Cette méthode permet de supprimer des études de la base de données.
    @staticmethod
    def etudes_delete(etudes_id):

        del_etudes = Etudes.query.get(etudes_id)

        try:
            db.session.delete(del_etudes)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]

    def etudes_to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "etudes",
            "id": self.etudes_id,
            "attributes": {
                "id_cardinal": self.etudes_id_cardinal,
                "id_formation": self.etudes_id_formation,
                "id_ville": self.etudes_id_ville
            },
            "links": {
                "self": url_for("etudes", etudes_id=self.etudes_id, _external=True),
                "json": url_for("api_etudes_single", etudes_id=self.etudes_id, _external=True)
            },
            "relationships": {
                "editions": [
                    author.author_to_json()
                    for author in self.authorships
                ]
            }
        }

# On crée notre modèle
class Mission(db.Model):
    # __table_args__ = {'extend_existing': True}
    __tablename__ = "mission"
    mission_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    mission_id_cardinal = db.Column(db.Integer, db.ForeignKey('cardinal.cardinal_id'))
    mission_id_pays = db.Column(db.Integer, db.ForeignKey('pays.pays_id'))
    mission_id_ville = db.Column(db.Integer, db.ForeignKey('ville.ville_id'))
    mission_date = db.Column(db.Text)
    cardinal = db.relationship("Cardinal", back_populates="mission")
    pays = db.relationship("Pays", back_populates="mission")
    ville = db.relationship("Ville", back_populates="mission")
    authorships = db.relationship("Authorship", back_populates="mission")


    # Cette méthode permet de pouvoir ajouter une mission diplomatique à la base de données.
    @staticmethod
    def mission_add(mission_add_id_cardinal, mission_add_id_pays, mission_add_id_ville, mission_add_date):
        erreurs = []
        if not mission_add_id_cardinal:
            erreurs.append("Merci d'indiquer l'identifiant du cardinal")
        if not mission_add_id_pays:
            erreurs.append("Merci d'indiquer l'identifiant du pays'")
        if not mission_add_id_ville:
            erreurs.append("Merci d'indiquer l'identifiant de la ville")
        if not mission_add_date:
            erreurs.append("Merci d'indiquer la date de la mission")

        # Afficher un message d'erreur si au moins une erreur survient.
        if len(erreurs) > 0:
            return False, erreurs

        # Dans le cas où il n'y a aucune erreur, ajouter des nouvelles données dans la table Mission.
        new_mission = Mission(mission_id_cardinal=mission_add_id_cardinal, mission_id_pays=mission_add_id_pays, mission_id_ville=mission_add_id_ville, mission_date=mission_add_date)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(new_mission)
            db.session.commit()
            return True, new_mission

        except Exception as erreur:
            return False, [str(erreur)]

    # Cette méthode permet de pouvoir mettre à jour les informations liées aux missions diplomatiques d'un cardinal dans la base de données.
    @staticmethod
    def mission_update(mission_id_cardinal, mission_id_pays, mission_id_ville, mission_date):
        erreurs = []
        if not mission_id_cardinal:
            erreurs.append("Veuillez renseigner l'identifiant d'un cardinal'")
        if not mission_id_pays:
            erreurs.append("Veuillez renseigner l'identifiant d'un État'")
        if not mission_id_ville:
            erreurs.append("Veuillez renseigner l'identifiant d'une ville")
        if not mission_date:
            erreurs.append("Veuillez renseigner la date de la mission")

        # S'il y a au moins une erreur.
        if len(erreurs) > 0:
            return False, erreurs

        # Récupération d'une mission dans la base.
        update_mission = Mission.query.get(mission_id)

        # Vérification de la modification d'au moins un élément.
        if update_mission.mission_id_cardinal == mission_id_cardinal \
            and update_mission.mission_id_pays == mission_id_pays \
            and update_mission.mission_id_ville == mission_id_ville \
            and update_mission.mission_date == mission_date:
            erreurs.append("No edit was submitted")

        if len(erreurs) > 0:
            return False, erreurs

        else:
            # Mise à jour des informations
            update_mission.mission_id_cardinal = mission_id_cardinal
            update_mission.mission_id_pays = mission_id_pays
            update_mission.mission_id_ville = mission_id_ville
            update_mission.mission_date = mission_date
        try:
            # On l'ajoute au transport vers la base de données.
            db.session.add(update_mission)
            # On envoie le paquet.
            db.session.commit()

            # On renvoie les informations du site.
            return True, update_mission
        except Exception as erreur:
            return False, [str(erreur)]

    # Cette méthode permet de supprimer une mission de la base de données.
    @staticmethod
    def mission_delete(mission_id):

        del_mission = Mission.query.get(mission_id)

        try:
            db.session.delete(del_mission)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]

    def mission_to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "mission",
            "id": self.mission_id,
            "attributes": {
                "id_cardinal": self.mission_id_cardinal,
                "id_pays": self.mission_id_pays,
                "id_ville": self.mission_id_ville
            },
            "links": {
                "self": url_for("mission", mission_id=self.mission_id, _external=True),
                "json": url_for("api_mission_single", mission_id=self.mission_id, _external=True)
            },
            "relationships": {
                "editions": [
                    author.author_to_json()
                    for author in self.authorships
                ]
            }
        }