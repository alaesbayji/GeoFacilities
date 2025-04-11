from django.contrib.gis.db import models  # Import modifié pour utiliser les modèles géographiques  
from django.contrib.gis.geos import Point  # Import de Point pour la valeur par défaut  
from django.utils import timezone  
from datetime import datetime 
import logging

logger = logging.getLogger(__name__) 
# 1. Pays  
class Pays(models.Model):  
    id = models.AutoField(primary_key=True)  # INT11 ID  
    actif = models.BooleanField(default=True)  # BIT1 ACTIF  
    designation = models.CharField(max_length=255)  # VARCHAR255 DESIGNATION  

    def __str__(self):  
        return self.designation  

# 2. Region (dépend de Pays)  
class Region(models.Model):  
    id = models.AutoField(primary_key=True)  # INT11 ID  
    actif = models.BooleanField(default=True)  # BIT1 ACTIF  
    designation = models.CharField(max_length=255)  # VARCHAR255 DESIGNATION  
    id_pays = models.ForeignKey('Pays', on_delete=models.CASCADE, related_name='regions')  # INT11 IDT_PAYS  

    def __str__(self):  
        return self.designation  

# 3. Ville (dépend de Region)  
class Ville(models.Model):  
    id = models.AutoField(primary_key=True)  # INT11 ID  
    actif = models.BooleanField(default=True)  # BIT1 ACTIF  
    designation = models.CharField(max_length=255)  # VARCHAR255 DESIGNATION  
    display_name = models.CharField(max_length=255)  # DISPLAYNAME  
    id_region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='villes')  # INT11 IDT_REGION  

    def __str__(self):  
        return self.designation  

# 4. ImportanceGeo  
class ImportanceGeo(models.Model):  
    id = models.AutoField(primary_key=True)
    actif = models.BooleanField(default=True)  
    designation = models.CharField(max_length=255)  
    ordre = models.IntegerField()  

    def __str__(self):  
        return self.designation  

# 5. TypeSite  
class TypeSite(models.Model):  
    id = models.AutoField(primary_key=True)  
    designation = models.CharField(max_length=255)  

    def __str__(self):  
        return self.designation  

# 6. LotTechnique  
class LotTechnique(models.Model):  
    id = models.AutoField(primary_key=True)  
    actif = models.BooleanField(default=True)  
    code_lot = models.CharField(max_length=255)  
    designation = models.CharField(max_length=255)  
    module = models.CharField(max_length=255, null=True, blank=True)  

# 7. FamilleEquipement (dépend de LotTechnique)  
class FamilleEquipement(models.Model):  
    id = models.AutoField(primary_key=True)  
    actif = models.BooleanField(default=True)  
    code_famille = models.CharField(max_length=255)  
    designation = models.CharField(max_length=255)  
    module = models.CharField(max_length=255,null=True, blank=True)  
    id_lot = models.ForeignKey('LotTechnique', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  

    def __str__(self):  
        return self.designation  

# 8. GroupeEquipement (dépend de FamilleEquipement)  
class GroupeEquipement(models.Model):  
    id = models.AutoField(primary_key=True)  
    actif = models.BooleanField(default=True)  
    designation = models.CharField(max_length=255)  
    id_famille_equipement = models.ForeignKey('FamilleEquipement', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  

    def __str__(self):  
        return self.designation  

# 9. Batiment (dépend de SiteSQL et ImportanceGeo)  
class Batiment(models.Model):  
    id = models.AutoField(primary_key=True)  # INT11 ID  
    actif = models.BooleanField(default=True)  # BIT1 ACTIF  
    code_batiment = models.CharField(max_length=255)  # VARCHAR255 CODE_BATIMENT  
    intitule = models.CharField(max_length=255)  # VARCHAR255 INTITULE  
    type_batiment = models.CharField(max_length=255)  # VARCHAR255 TYPE_BATIMENT  
    id_importance = models.ForeignKey('ImportanceGeo', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_site = models.ForeignKey('SiteSQL', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    idt_type_affectation = models.IntegerField()  # INT11 IDT_TYPE_AFFECTATION  

    def __str__(self):  
        return self.intitule  

# 10. Niveau (dépend de Batiment et ImportanceGeo)  
class Niveau(models.Model):  
    id = models.AutoField(primary_key=True)  
    actif = models.BooleanField(default=True)  
    code_niveau = models.CharField(max_length=255)  
    intitule = models.CharField(max_length=255)  
    id_batiment = models.ForeignKey('Batiment', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_importance = models.ForeignKey('ImportanceGeo', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    url_web_service = models.URLField(max_length=255, default='https://services2.arcgis.com/uaR6EOboD6BtHr7b/arcgis/rest/services/Map_WFS_TEST/FeatureServer/0', blank=True, null=True)  # Champ pour l'URL du service web  

    def __str__(self):  
        return self.intitule  
class TypeEspace(models.Model):
    id = models.AutoField(primary_key=True)
    actif = models.BooleanField(default=True)
    designation = models.CharField(max_length=255)

    def __str__(self):
        return self.designation
# 11. EspaceSQL (dépend de Niveau et ImportanceGeo)  
class EspaceSQL(models.Model):  
    id = models.AutoField(primary_key=True)  
    actif = models.BooleanField(default=True)  
    code_espace = models.CharField(max_length=255)  
    intitule = models.CharField(max_length=255)  
    id_importance = models.ForeignKey('ImportanceGeo', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_niveau = models.ForeignKey('Niveau', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_type_espace = models.ForeignKey('TypeEspace', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    geom = models.PolygonField(null=True, blank=True)  # Valeur par défaut  

    def __str__(self):  
        return self.intitule  

# 12. SiteSQL (dépend de Ville et TypeSite)  
class SiteSQL(models.Model):  
    id = models.AutoField(primary_key=True)  
    adresse = models.CharField(max_length=255)  
    code_agence = models.CharField(max_length=255)  
    code_site = models.CharField(max_length=255)  
    intitule = models.CharField(max_length=255)  
    nombre_occupant = models.IntegerField()  
    peut_cloturer = models.BooleanField(default=False)  
    peut_valider = models.BooleanField(default=False)  
    photo_path = models.CharField(max_length=255, null=True, blank=True)  
    photo_source = models.CharField(max_length=255, null=True, blank=True)  
    statut = models.IntegerField()  
    superficie = models.IntegerField()  
    id_type_site = models.ForeignKey('TypeSite', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_ville = models.ForeignKey('Ville', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  

    def __str__(self):  
        return self.intitule  

# 13. Prestataire  
class Prestataire(models.Model):  
    id = models.AutoField(primary_key=True)  
    adresse = models.CharField(max_length=255)  
    cnss = models.CharField(max_length=255)  
    code_prestataire = models.CharField(max_length=255)  
    email = models.CharField(max_length=255)  
    identifiant_fiscal = models.CharField(max_length=255)  
    logo_path = models.CharField(max_length=255, null=True, blank=True)  
    logo_source = models.CharField(max_length=255, null=True, blank=True)  
    raison_sociale = models.CharField(max_length=255)  
    registre_commerce = models.CharField(max_length=255)  
    site_web = models.CharField(max_length=255)  
    taxe_prof = models.CharField(max_length=255)  
    id_forme_juridique = models.IntegerField()  # Clé étrangère  
    id_ranking_prestataire = models.IntegerField()  # Clé étrangère  
    id_societe_mere = models.IntegerField()  
    id_ville_param = models.IntegerField()  

    def __str__(self):  
        return self.raison_sociale  

# 14. CriticiteEquipement
class CriticiteEquipement(models.Model):  
    id = models.AutoField(primary_key=True)  
    actif = models.BooleanField(null=True, blank=True)  
    designation = models.CharField(max_length=255)  
    ordre = models.IntegerField(default=0,null=True, blank=True)  # Valeur par défaut pour ordre  

    def __str__(self):  
        return self.designation  

# 15. NbrSite (dépend de SiteSQL et Niveau)  
class NbrSite(models.Model):  
    id = models.AutoField(primary_key=True)  
    nbr = models.IntegerField(null=True, blank=True)  
    id_famille = models.ForeignKey('FamilleEquipement', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_niveau = models.ForeignKey('Niveau', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_site = models.ForeignKey('SiteSQL', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  

    def __str__(self):  
        return f"NbrSite {self.id}"  

# 16. EquipementSQL (dépend de EspaceSQL, CriticiteEquipement, FamilleEquipement)  
class EquipementSQL(models.Model):  
    id = models.AutoField(primary_key=True)  
    actif = models.BooleanField(default=True)  
    code_barre = models.CharField(max_length=255, null=True, blank=True)  
    code_equipement = models.CharField(max_length=255, null=True, blank=True)  
    code_equipement_prestataire = models.CharField(max_length=255, null=True, blank=True)  
    condition_equipement = models.BooleanField(default=False)  
    date_desactivation = models.DateTimeField(null=True, blank=True)  
    date_fin_garantie = models.DateTimeField(null=True, blank=True)  
    date_installation = models.DateTimeField(null=True, blank=True)  
    date_reception = models.DateTimeField(null=True, blank=True)  
    etat = models.BooleanField(default=False, null=True, blank=True)  
    frn_installeur = models.CharField(max_length=255, null=True, blank=True)  
    lisible = models.BooleanField(default=False, null=True, blank=True)  
    nevragique = models.BooleanField(default=False, null=True, blank=True)  
    numero_marche = models.CharField(max_length=255, null=True, blank=True)  
    proprietaire_id = models.IntegerField(null=True, blank=True)  # Clé étrangère  
    receptionne = models.BooleanField(default=False, null=True, blank=True)  
    id_criticite_equipement = models.ForeignKey('CriticiteEquipement', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_espace = models.ForeignKey('EspaceSQL', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_espace_desservi =models.CharField(max_length=255, null=True, blank=True)
    id_famille_equipement = models.ForeignKey('FamilleEquipement', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_groupe_equipement = models.ForeignKey('GroupeEquipement', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    prestataire_id = models.ForeignKey('Prestataire', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    id_nbr_site = models.ForeignKey('NbrSite', on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère  
    geom = models.PointField(null=True, blank=True)  # Sans valeur par défaut  

    def __str__(self):  
        return self.code_equipement or str(self.id)  
class StatutNC(models.Model):  
    id = models.AutoField(primary_key=True)  
    actif = models.BooleanField()  
    designation = models.CharField(max_length=255)  
    ordre = models.PositiveIntegerField()  
class HistoriqueNC(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    mobile = models.BooleanField(default=False)
    utilisateur = models.CharField(max_length=255)
    non_conformite = models.ForeignKey('NonConformite', on_delete=models.CASCADE)
    statut_nc = models.ForeignKey('StatutNC', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"HistoriqueNC {self.id}"
class NonConformite(models.Model):
    id = models.AutoField(primary_key=True)
    equipement_dispo = models.BooleanField(default=True)
    astreinte = models.BooleanField(default=False,null=True, blank=True)
    code_signalement = models.CharField(max_length=255)
    constate_par = models.IntegerField()
    contact_prestataire = models.BinaryField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    date_debut_indisp = models.DateTimeField(null=True, blank=True)
    date_fpm = models.DateTimeField(null=True, blank=True)
    date_paliatif = models.DateTimeField(null=True, blank=True)
    date_planification =models.DateTimeField(null=True, blank=True)
    date_previsionnelle =models.DateTimeField(null=True, blank=True)
    date_retablissement = models.DateTimeField(null=True, blank=True)
    date_retablissement_final =models.DateTimeField(null=True, blank=True)
    delai_intervention = models.TextField(null=True, blank=True)
    descriptif = models.TextField(null=True, blank=True)
    descriptif_fpm = models.TextField(null=True, blank=True)
    diagnostic = models.TextField(null=True, blank=True)
    email = models.CharField(max_length=255,null=True, blank=True)
    equipement_saisie = models.CharField(max_length=255,null=True, blank=True)
    espace_saisie = models.CharField(max_length=255,null=True, blank=True)
    exterieur = models.BooleanField(default=False,null=True, blank=True)
    fait_marquant = models.BooleanField(default=False,null=True, blank=True)
    foc = models.IntegerField(null=True, blank=True)
    date_annulation = models.DateTimeField(null=True, blank=True)
    date_pencharge = models.DateTimeField(null=True, blank=True)
    lot_saisie = models.CharField(max_length=255,null=True, blank=True)
    mobile = models.BooleanField(default=False,null=True, blank=True)
    motif_annulation = models.CharField(max_length=255,null=True, blank=True)
    n_fnc = models.CharField(max_length=255,null=True, blank=True)
    nc_retablie = models.BooleanField(default=False)
    nom_fichier = models.CharField(max_length=255,null=True, blank=True)
    partial = models.BooleanField(default=False)
    photo_first = models.CharField(max_length=255,null=True, blank=True)
    signale_par = models.CharField(max_length=255,null=True, blank=True)
    st_prestataire = models.CharField(max_length=255,null=True, blank=True)
    t_orp = models.BooleanField(default=False)
    tel = models.CharField(max_length=255,null=True, blank=True)
    titre = models.CharField(max_length=255,null=True, blank=True)
    titre_prestataire = models.CharField(max_length=255,null=True, blank=True)
    uid = models.CharField(max_length=255,null=True, blank=True)
    valeur1 = models.BooleanField(default=False)
    valeur2 = models.BooleanField(default=False)
    valeur3 = models.BooleanField(default=False)
    valeur4 = models.BooleanField(default=False)
    batiment = models.ForeignKey('Batiment', on_delete=models.SET_NULL, null=True, blank=True)
    criticite_non_conformite = models.ForeignKey('CriticiteNC', on_delete=models.SET_NULL, null=True, blank=True)
    equipement = models.ForeignKey('EquipementSQL', on_delete=models.SET_NULL, null=True, blank=True)
    espace = models.ForeignKey('EspaceSQL', on_delete=models.SET_NULL, null=True, blank=True)
    famille_equipement = models.ForeignKey('FamilleEquipement', on_delete=models.SET_NULL, null=True, blank=True)
    importance_geographique = models.ForeignKey('ImportanceGeo', on_delete=models.SET_NULL, null=True, blank=True)
    lot_technique = models.ForeignKey('LotTechnique', on_delete=models.SET_NULL, null=True, blank=True)
    marche = models.ForeignKey('Marche', on_delete=models.SET_NULL, null=True, blank=True)
    niveau = models.ForeignKey('Niveau', on_delete=models.SET_NULL, null=True, blank=True)
    prestataire = models.ForeignKey('Prestataire', on_delete=models.SET_NULL, null=True, blank=True)
    prestataire_fpm = models.ForeignKey('Prestataire', related_name='prestataire_fpm', on_delete=models.SET_NULL, null=True, blank=True)
    prestataire_st = models.ForeignKey('Prestataire', related_name='prestataire_st', on_delete=models.SET_NULL, null=True, blank=True)
    prestation_service = models.CharField(max_length=255,null=True, blank=True)
    site = models.ForeignKey('SiteSQL', on_delete=models.SET_NULL, null=True, blank=True)
    statut_nc = models.ForeignKey('StatutNC', on_delete=models.SET_NULL, null=True, blank=True)
class Ronde(models.Model):
    id = models.AutoField(primary_key=True)
    date_debut = models.DateTimeField()
    actif = models.BooleanField(default=True)
    date_desactivation = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    frequence = models.IntegerField(null=True, blank=True)
    profiles = models.CharField(max_length=255)
    titre = models.CharField(max_length=255)
    t_orp = models.BooleanField(default=False)
    type_ronde = models.IntegerField(null=True, blank=True)
    batiment = models.ForeignKey('Batiment', on_delete=models.SET_NULL, null=True, blank=True)
    cmsite = models.ForeignKey('SiteSQL', on_delete=models.SET_NULL, null=True, blank=True)
    equipement = models.ForeignKey('EquipementSQL', on_delete=models.SET_NULL, null=True, blank=True)
    espace = models.ForeignKey('EspaceSQL', on_delete=models.SET_NULL, null=True, blank=True)
    niveau = models.ForeignKey('Niveau', on_delete=models.SET_NULL, null=True, blank=True)
    prestataire = models.ForeignKey('Prestataire', on_delete=models.SET_NULL, null=True, blank=True)
    prestation = models.CharField(max_length=255 ,null=True, blank=True)
    type_realisation = models.ForeignKey('TypeRealisation', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titre
class RondeCommentaires(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.CharField(max_length=255,null=True, blank=True)
    text = models.CharField(max_length=255,null=True, blank=True)
    ronde = models.ForeignKey('Ronde', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"RondeCommentaires {self.id}"
class RondeEvent(models.Model):
    id = models.AutoField(primary_key=True)
    heure = models.IntegerField(null=True, blank=True)
    jour = models.IntegerField(null=True, blank=True)
    ronde = models.ForeignKey('Ronde', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"RondeEvent {self.id}"
class RondeParametre(models.Model):
    id = models.AutoField(primary_key=True)
    anotifier = models.BooleanField(default=False,null=True, blank=True)
    graphe = models.BooleanField(default=False,null=True, blank=True)
    is_max = models.BooleanField(default=False,null=True, blank=True)
    seuil = models.FloatField(null=True, blank=True)
    donnee_mesure = models.ForeignKey('DonneeMesure', on_delete=models.SET_NULL, null=True, blank=True)
    ronde = models.ForeignKey('Ronde', on_delete=models.CASCADE,null=True, blank=True)
    unite_de_mesure = models.ForeignKey('UniteMesure', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"RondeParametre {self.id}"
class RondeReleve(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255,null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    date_saisie = models.DateTimeField(null=True, blank=True)
    disponible = models.BooleanField(default=False,null=True, blank=True)
    from_mobile = models.BooleanField(default=False,null=True, blank=True)
    rondier = models.CharField(max_length=255,null=True, blank=True)
    valeur = models.FloatField(null=True, blank=True)
    ronde_event = models.ForeignKey('RondeEvent', on_delete=models.CASCADE,null=True, blank=True)
    ronde_parametre = models.ForeignKey('RondeParametre', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"RondeReleve {self.id}"
class TypeRealisation(models.Model):
    id = models.AutoField(primary_key=True)
    actif = models.BooleanField(default=True,null=True, blank=True)
    designation = models.CharField(max_length=255,null=True, blank=True)
    ordre = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.designation
class UniteMesure(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True,null=True, blank=True)
    unite_de_mesure = models.CharField(max_length=255,null=True, blank=True)
    donnee_mesure = models.ForeignKey('DonneeMesure', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.unite_de_mesure
class DonneeMesure(models.Model):  
    id = models.AutoField(primary_key=True)  
    column_label = models.CharField(max_length=255,null=True, blank=True)  # Assurez-vous d'ajuster la longueur si nécessaire  
    is_active = models.BooleanField(null=True, blank=True)  # Renommer pour respecter les conventions Python  
    donne_mesuree = models.CharField(max_length=255,null=True, blank=True)# Assurez-vous d'utiliser le bon type  
class Intervention(models.Model):
    id = models.AutoField(primary_key=True)
    cloture = models.BooleanField(default=False,null=True, blank=True)
    commentaire = models.CharField(max_length=255,null=True, blank=True)
    content_type_one = models.CharField(max_length=255,null=True, blank=True)
    content_type_two = models.CharField(max_length=255,null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    date_cloture = models.DateTimeField(null=True, blank=True)
    date_debut = models.DateTimeField(null=True, blank=True)
    date_depart_previsionnel = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    date_fin_prev = models.DateTimeField(null=True, blank=True)
    index_intervention = models.IntegerField(null=True, blank=True)
    nom_fichier_1 = models.CharField(max_length=255,null=True, blank=True)
    nom_fichier_2 = models.CharField(max_length=255,null=True, blank=True)
    ordre = models.IntegerField(null=True, blank=True)
    prestatire_sous_traitant = models.CharField(max_length=255,null=True, blank=True)
    statut = models.IntegerField(null=True, blank=True)
    taille = models.IntegerField(null=True, blank=True)
    taux_avancement = models.IntegerField(null=True, blank=True)
    uid_one = models.CharField(max_length=255,null=True, blank=True)
    uid_two = models.CharField(max_length=255,null=True, blank=True)
    cloturer_par = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    contrat = models.CharField(max_length=255,null=True, blank=True)
    detail_planification = models.ForeignKey('DetailPlanification', on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return f"Intervention {self.id}"
class InterventionAttachement(models.Model):
    intervention = models.ForeignKey('Intervention', on_delete=models.CASCADE, primary_key=True)
    photo = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['intervention', 'photo'],
                name='unique_intervention_photo'
            )
        ]
        managed = True
        db_table = 'intervention_attachement'

    def __str__(self):
        return f"Intervention {self.intervention_id} - Photo {self.photo}"

class InterventionIntervenants(models.Model):
    intervention = models.ForeignKey('Intervention', on_delete=models.CASCADE, primary_key=True)
    intervenant = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['intervention', 'intervenant'], 
                name='unique_intervention_intervenant'
            )
        ]
        managed = True
        db_table = 'intervention_intervenants'



class InterventionPrestataire(models.Model):
    intervention = models.ForeignKey('Intervention', on_delete=models.CASCADE, primary_key=True)
    prestataire = models.ForeignKey('Prestataire', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['intervention', 'prestataire'], 
                name='unique_intervention_prestataire'
            )
        ]
        managed = True
        db_table = 'intervention_prestataire'

    def __str__(self):
        return f"Intervention {self.intervention_id} - Prestataire {self.prestataire_id}"

class Planification(models.Model):
    id = models.AutoField(primary_key=True)
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    intitule = models.CharField(max_length=255,null=True, blank=True)
    t_orp = models.BooleanField(default=False,null=True, blank=True)
    marche = models.ForeignKey('Marche', on_delete=models.SET_NULL, null=True, blank=True)
    prestataire = models.ForeignKey('Prestataire', on_delete=models.SET_NULL, null=True, blank=True)
    prestation = models.CharField(max_length=255,null=True, blank=True)
    site = models.ForeignKey('SiteSQL', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.intitule
class DetailPlanification(models.Model):
    id = models.AutoField(primary_key=True)
    charge = models.IntegerField(null=True, blank=True)
    content_type = models.CharField(max_length=255,null=True, blank=True)
    lieu = models.CharField(max_length=255,null=True, blank=True)
    nom_fichier = models.CharField(max_length=255,null=True, blank=True)
    nombre = models.IntegerField(null=True, blank=True)
    ordre_fam = models.IntegerField(null=True, blank=True)
    ordre_lot = models.IntegerField(null=True, blank=True)
    semaine = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    tache = models.CharField(max_length=255,null=True, blank=True)
    task = models.BooleanField(default=False,null=True, blank=True)
    uid = models.CharField(max_length=255,null=True, blank=True)
    criticite_equipement = models.ForeignKey('CriticiteEquipement', on_delete=models.SET_NULL, null=True, blank=True)
    equipement = models.ForeignKey('EquipementSQL', on_delete=models.SET_NULL, null=True, blank=True)
    famille_equipement = models.ForeignKey('FamilleEquipement', on_delete=models.SET_NULL, null=True, blank=True)
    frequence = models.ForeignKey('Frequence', on_delete=models.SET_NULL, null=True, blank=True)
    groupe_equipement = models.ForeignKey('GroupeEquipement', on_delete=models.SET_NULL, null=True, blank=True)
    lot_technique = models.ForeignKey('LotTechnique', on_delete=models.SET_NULL, null=True, blank=True)
    planification = models.ForeignKey('Planification', on_delete=models.CASCADE,null=True, blank=True)
    type_realisation = models.ForeignKey('TypeRealisation', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"DetailPlanification {self.id}"
class Frequence(models.Model):  
    id = models.AutoField(primary_key=True)  
    actif = models.BooleanField(null=True, blank=True)  
    couleur = models.CharField(max_length=100,null=True, blank=True)  # Ajustez la longueur selon vos besoins  
    designation = models.CharField(max_length=255,null=True, blank=True)  # Ajustez la longueur selon vos besoins  
    ordre = models.PositiveIntegerField(null=True, blank=True)  
    valeur = models.FloatField(null=True, blank=True)  # Utilisez le type approprié pour la colonne VALEUR  
    value = models.FloatField(null=True, blank=True)   # Utilisez un autre nom ou ajustez en fonction de votre base de données  
class DetailPlanificationIntervention(models.Model):
    detail_planification = models.ForeignKey('DetailPlanification', on_delete=models.CASCADE, primary_key=True)
    intervention = models.ForeignKey('Intervention', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['detail_planification', 'intervention'],
                name='unique_detail_planification_intervention'
            )
        ]
        managed = True
        db_table = 'detail_planification_intervention'

    def __str__(self):
        return f"DetailPlanification {self.detail_planification_id} - Intervention {self.intervention_id}"

class User(models.Model):
    id = models.AutoField(primary_key=True)
    actif = models.BooleanField(default=True)
    attempts = models.IntegerField(null=True, blank=True)
    departement = models.CharField(max_length=255,null=True, blank=True)
    device = models.CharField(max_length=255,null=True, blank=True)
    directeur_agence = models.BooleanField(default=False,null=True, blank=True)
    email = models.CharField(max_length=255,null=True, blank=True)
    enabled = models.BooleanField(default=True,null=True, blank=True)
    foc = models.IntegerField(null=True, blank=True)
    fonction = models.CharField(max_length=255,null=True, blank=True)
    gcmid = models.CharField(max_length=255,null=True, blank=True)
    iam = models.CharField(max_length=255,null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    loked_date = models.DateTimeField(null=True, blank=True)
    nom = models.CharField(max_length=255,null=True, blank=True)
    notifiable = models.BooleanField(default=False,null=True, blank=True)
    password = models.CharField(max_length=255,null=True, blank=True)
    prenom = models.CharField(max_length=255,null=True, blank=True)
    rest_tocken = models.CharField(max_length=255,null=True, blank=True)
    role = models.CharField(max_length=255,null=True, blank=True)
    tel = models.CharField(max_length=255,null=True, blank=True)
    username = models.CharField(max_length=255,null=True, blank=True)
    contact =models.CharField(max_length=255,null=True, blank=True)
    fournisseur = models.CharField(max_length=255,null=True, blank=True)
    password_changed_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username
class UserAffec(models.Model):
    id = models.AutoField(primary_key=True)
    peux_cloturer = models.BooleanField(default=False)
    peux_valider = models.BooleanField(default=False)
    marche = models.ForeignKey('Marche', on_delete=models.SET_NULL, null=True, blank=True)
    prestataire = models.ForeignKey('Prestataire', on_delete=models.SET_NULL, null=True, blank=True)
    site = models.ForeignKey('SiteSQL', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"UserAffec {self.id}"
class Marche(models.Model):
    id = models.AutoField(primary_key=True)
    actif = models.BooleanField(default=True,null=True, blank=True)
    alloti = models.BooleanField(default=False,null=True, blank=True)
    code_marche = models.CharField(max_length=255,null=True, blank=True)
    condition_pfpm = models.CharField(max_length=255,null=True, blank=True)
    condition_pprestataire = models.CharField(max_length=255,null=True, blank=True)
    date_approbation = models.DateTimeField(null=True, blank=True)
    date_attribution = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    date_ordre_service = models.DateTimeField(null=True, blank=True)
    date_effective = models.DateTimeField(null=True, blank=True)
    designation = models.CharField(max_length=255,null=True, blank=True)
    duree_initiale = models.IntegerField(null=True, blank=True)
    duree_preavis_fpm = models.IntegerField(null=True, blank=True)
    duree_preavis_prestataire = models.IntegerField(null=True, blank=True)
    duree_renouvellement = models.IntegerField(null=True, blank=True)
    nombre_lots = models.IntegerField(null=True, blank=True)
    nombre_renouvellement = models.IntegerField(null=True, blank=True)
    nombre_sites = models.IntegerField(null=True, blank=True)
    numero_marche = models.CharField(max_length=255,null=True, blank=True)
    renouvellement = models.BooleanField(default=False,null=True, blank=True)
    technique = models.BooleanField(default=False,null=True, blank=True)
    prestataire = models.ForeignKey('Prestataire', on_delete=models.SET_NULL, null=True, blank=True)
    rankin_marche = models.CharField(max_length=255,null=True, blank=True)
    type_prestation = models.CharField(max_length=255, null=True, blank=True)
    support_contractuel = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.designation
class CriticiteNC(models.Model):  
    id = models.AutoField(primary_key=True)  # Assuming ID is an AutoIncrement field  
    actif = models.BooleanField(default=True)  # Assuming ACTIF is a boolean field  
    designation = models.CharField(max_length=255)  # Assuming DESIGNATION is a string  
    ordre = models.IntegerField()  # Assuming ORDRE is an integer  
class Action(models.Model):  
    id = models.AutoField(primary_key=True)  
    budget_action = models.CharField(max_length=255,null=True, blank=True)  
    commentaire = models.TextField(null=True, blank=True)  
    content_type = models.CharField(max_length=100,null=True, blank=True)  
    date_debut = models.DateTimeField(null=True, blank=True)  
    date_fin_p = models.DateTimeField(null=True, blank=True)  
    date_fin = models.DateTimeField(null=True, blank=True)  
    date_suspens = models.DateTimeField(null=True, blank=True)  
    date_validation = models.DateTimeField(null=True, blank=True)  
    demande = models.CharField(max_length=255,null=True, blank=True)  
    detail_action = models.TextField(null=True, blank=True)  
    need_val = models.BooleanField()  
    nom_fichier = models.CharField(max_length=255,null=True, blank=True)  
    num_save = models.IntegerField(null=True, blank=True)  
    numero_action = models.CharField(max_length=100,null=True, blank=True)  
    pdr_conso = models.CharField(max_length=100,null=True, blank=True)  
    responsable = models.CharField(max_length=255,null=True, blank=True)  
    taux_avancement = models.CharField(max_length=100,null=True, blank=True)  
    technicien = models.CharField(max_length=255,null=True, blank=True)  
    uid = models.CharField(max_length=255,null=True, blank=True)  
    valid = models.BooleanField(null=True, blank=True)  
    valider_par = models.CharField(max_length=255,null=True, blank=True)  
    idt_nc = models.ForeignKey('NonConformite', on_delete=models.CASCADE)
    pst_action_id = models.IntegerField(null=True, blank=True)  
    statut_action_id = models.ForeignKey('StatutAction', on_delete=models.SET_NULL, null=True, blank=True) 



class StatutAction(models.Model):  
    id = models.AutoField(primary_key=True)  
    actif = models.BooleanField()  
    designation = models.CharField(max_length=255)  
    ordre = models.IntegerField()
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models  
from django.contrib.auth.models import AbstractUser  

class UserProfile(models.Model):  
    ROLE_CHOICES = (  
        ('admin_technique', 'Administrateur Technique'),  
        ('admin_fonctionnel', 'Administrateur Fonctionnel'),  
        ('responsable_site', 'Responsable Site'),  
        ('technicien_terrain', 'Technicien Terrain'),  
    )  
    
    ldap_cn = models.CharField(max_length=100, unique=True)  # CN de LDAP  
    ldap_sn = models.CharField(max_length=100)  # SN de LDAP  
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)  
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    # Sites assigned to the user  
    sites = models.ManyToManyField('SiteSQL', related_name='user_profiles', blank=True)  
    all_sites = models.BooleanField(default=False)  # Field to indicate if the user has access to all sites  

    def __str__(self):  
        return f"{self.ldap_cn} ({self.get_role_display()})"  