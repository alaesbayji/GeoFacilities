from rest_framework import viewsets
from .models import (  
    Pays,  
    Region,  
    Ville,  
    ImportanceGeo,  
    TypeSite,  
    LotTechnique,  
    FamilleEquipement,  
    GroupeEquipement,  
    Batiment,  
    Niveau,  
    TypeEspace,  
    EspaceSQL,  
    SiteSQL,  
    Prestataire,  
    CriticiteEquipement,  
    NbrSite,  
    EquipementSQL,  
    StatutNC,  
    HistoriqueNC,  
    NonConformite,  
    Ronde,  
    RondeCommentaires,  
    RondeEvent,  
    RondeParametre,  
    RondeReleve,  
    TypeRealisation,  
    UniteMesure,  
    DonneeMesure,  
    Intervention,  
    InterventionAttachement,  
    InterventionIntervenants,  
    InterventionPrestataire,  
    Planification,  
    DetailPlanification,  
    Frequence,  
    DetailPlanificationIntervention,  
    User,  
    UserAffec,  
    Marche  
)    
from .serializers import (  
    SiteSQLSerializer,  
    EquipementSQLSerializer,  
    EspaceSQLSerializer,  
    TypeSiteSerializer,  
    VilleSerializer,  
    ImportanceGeoSerializer,  
    NiveauSerializer,  
    TypeEspaceSerializer,  
    CriticiteEquipementSerializer,  
    FamilleEquipementSerializer,  
    GroupeEquipementSerializer,  
    PrestataireSerializer,  
    NbrSiteSerializer,  
    LotTechniqueSerializer,  
    BatimentSerializer,  
    PaysSerializer,  
    RegionSerializer,  
    StatutNCSerializer,  
    HistoriqueNCSerializer,  
    NonConformiteSerializer,  
    RondeSerializer,  
    RondeCommentairesSerializer,  
    RondeEventSerializer,  
    RondeParametreSerializer,  
    RondeReleveSerializer,  
    TypeRealisationSerializer,  
    UniteMesureSerializer,  
    DonneeMesureSerializer,  
    InterventionSerializer,  
    InterventionAttachementSerializer,  
    InterventionIntervenantsSerializer,  
    InterventionPrestataireSerializer,  
    PlanificationSerializer,  
    DetailPlanificationSerializer,  
    FrequenceSerializer,  
    DetailPlanificationInterventionSerializer,  
    UserSerializer,  
    UserAffecSerializer,  
    MarcheSerializer  
)  
from django.db import connections
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from django.contrib.gis.geos import Polygon, Point
from random import uniform

# Dictionnaire pour lier chaque table avec son modèle et son sérialiseur
TABLES_CONFIG = {  
    'ESPACE': {  
        'model': EspaceSQL,  
        'serializer': EspaceSQLSerializer,  
        'fields': ['id', 'actif', 'code_espace', 'intitule', 'id_importance_id', 'id_niveau_id', 'id_type_espace_id'],  
        'dependencies': []  # Aucune dépendance  
    },  
    'SITE': {  
        'model': SiteSQL,  
        'serializer': SiteSQLSerializer,  
        'fields': [  
            'id', 'adresse', 'code_agence', 'code_site', 'intitule', 'nombre_occupant',  
            'peut_cloturer', 'peut_valider', 'photo_path', 'photo_source', 'statut',  
            'superficie', 'id_type_site_id', 'id_ville_id'  
        ],  
        'dependencies': []  # Aucune dépendance  
    },  
    'EQUIPEMENT': {  
        'model': EquipementSQL,  
        'serializer': EquipementSQLSerializer,  
        'fields': [  
            'id', 'actif', 'code_barre', 'code_equipement', 'code_equipement_prestataire',  
            'condition_equipement', 'date_desactivation', 'date_fin_garantie',  
            'date_installation', 'date_reception', 'etat', 'frn_installeur', 'lisible',  
            'nevragique', 'numero_marche', 'proprietaire_id', 'receptionne',  
            'id_criticite_equipement_id', 'id_espace_id', 'id_espace_desservi',   
            'id_famille_equipement_id', 'id_groupe_equipement_id', 'prestataire_id_id',   
            'id_nbr_site_id'  
        ],  
        'dependencies': ['ESPACE']  # Dépend de ESPACE  
    },  
    'TYPE_SITE': {  
        'model': TypeSite,  
        'serializer': TypeSiteSerializer,  
        'fields': ['id', 'designation'],  
        'dependencies': []  
    },  
    'IMPORTANCE_GEO': {  
        'model': ImportanceGeo,  
        'serializer': ImportanceGeoSerializer,  
        'fields': ['id', 'actif','designation', 'ordre'],  
        'dependencies': []  
    },  
    'NIVEAU': {  
        'model': Niveau,  
        'serializer': NiveauSerializer,  
        'fields': ['id', 'actif', 'code_niveau', 'intitule', 'id_batiment_id', 'id_importance_id'],  
        'dependencies': ['BATIMENT']  
    },  
    'TYPE_ESPACE': {  
        'model': TypeEspace,  
        'serializer': TypeEspaceSerializer,  
        'fields': ['id', 'actif', 'designation'],  
        'dependencies': []  
    },  
    'CRICITICITE_EQUIPEMENT': {  
        'model': CriticiteEquipement,  
        'serializer': CriticiteEquipementSerializer,  
        'fields': ['id', 'designation'],  
        'dependencies': []  
    },  
    'FAMILLE_EQUIPEMENT': {  
        'model': FamilleEquipement,  
        'serializer': FamilleEquipementSerializer,  
        'fields': ['id', 'actif', 'code_famille', 'designation', 'module', 'id_lot_id'],  
        'dependencies': ['LOT_TECHNIQUE']  
    },  
    'GROUPE_EQUIPEMENT': {  
        'model': GroupeEquipement,  
        'serializer': GroupeEquipementSerializer,  
        'fields': ['id', 'actif', 'designation', 'id_famille_equipement'],  
        'dependencies': ['FAMILLE_EQUIPEMENT']  
    },  
    'PRESTATAIRE': {  
        'model': Prestataire,  
        'serializer': PrestataireSerializer,  
        'fields': [  
            'id', 'adresse', 'cnss', 'code_prestataire', 'email',   
            'identifiant_fiscal', 'logo_path', 'logo_source',   
            'raison_sociale', 'registre_commerce', 'site_web',   
            'taxe_prof', 'id_forme_juridique', 'id_ranking_prestataire',   
            'id_societe_mere', 'id_ville_param'  
        ],  
        'dependencies': []  
    },  
    'NBR_SITE': {  
        'model': NbrSite,  
        'serializer': NbrSiteSerializer,  
        'fields': ['id', 'nbr', 'id_famille_id', 'id_niveau_id', 'id_site_id'],  
        'dependencies': ['ESPACE', 'NIVEAU', 'SITE']  
    },  
    'LOT_TECHNIQUE': {  
        'model': LotTechnique,  
        'serializer': LotTechniqueSerializer,  
        'fields': ['id', 'actif', 'code_lot', 'designation', 'module'],  
        'dependencies': []  
    },  
    'BATIMENT': {  
        'model': Batiment,  
        'serializer': BatimentSerializer,  
        'fields': ['id', 'actif', 'code_batiment', 'intitule', 'type_batiment', 'id_importance_id', 'id_site_id', 'idt_type_affectation'],  
        'dependencies': []  
    },  
    'PAYS': {  
        'model': Pays,  
        'serializer': PaysSerializer,  
        'fields': ['id', 'actif', 'designation'],  
        'dependencies': []  
    },  
    'REGION': {  
        'model': Region,  
        'serializer': RegionSerializer,  
        'fields': ['id', 'actif', 'designation', 'id_pays'],  
        'dependencies': ['PAYS']  
    },  
    'VILLE': {  
        'model': Ville,  
        'serializer': VilleSerializer,  
        'fields': ['id', 'actif', 'designation', 'display_name', 'id_region'],  
        'dependencies': ['REGION']  
    }  ,    'STATUT_NC': {
        'model': StatutNC,
        'serializer': StatutNCSerializer,
        'fields': ['id', 'actif', 'designation', 'ordre'],
        'dependencies': []
    },
    'HISTORIQUE_NC': {
        'model': HistoriqueNC,
        'serializer': HistoriqueNCSerializer,
        'fields': ['id', 'date', 'mobile', 'utilisateur', 'non_conformite_id', 'statut_nc_id'],
        'dependencies': ['NON_CONFORMITE', 'STATUT_NC']
    },
    'NON_COMFORMITE': {
        'model': NonConformite,
        'serializer': NonConformiteSerializer,
        'fields': [
            'id', 'equipement_dispo', 'astreinte', 'code_signalement', 'constate_par', 'contact_prestataire',
            'date', 'date_debut_indisp', 'date_fpm', 'date_paliatif', 'date_planification', 'date_previsionnelle',
            'date_retablissement', 'date_retablissement_final', 'delai_intervention', 'descriptif', 'descriptif_fpm',
            'diagnostic', 'email', 'equipement_saisie', 'espace_saisie', 'exterieur', 'fait_marquant', 'foc',
            'date_annulation', 'date_pencharge', 'lot_saisie', 'mobile', 'motif_annulation', 'n_fnc', 'nc_retablie',
            'nom_fichier', 'partial', 'photo_first', 'signale_par', 'st_prestataire', 't_orp', 'tel', 'titre',
            'titre_prestataire', 'uid', 'valeur1', 'valeur2', 'valeur3', 'valeur4', 'batiment_id', 'criticite_non_conformite_id',
            'equipement_id', 'espace_id', 'famille_equipement_id', 'importance_geographique_id', 'lot_technique_id',
            'marche_id', 'niveau_id', 'prestataire_id', 'prestataire_fpm_id', 'prestataire_st_id', 'prestation_service',
            'site_id', 'statut_nc_id'
        ],
        'dependencies': [
            'BATIMENT', 'CRICITICITE_EQUIPEMENT', 'EQUIPEMENT', 'ESPACE', 'FAMILLE_EQUIPEMENT', 'IMPORTANCE_GEO',
            'LOT_TECHNIQUE', 'MARCHE', 'NIVEAU', 'PRESTATAIRE', 'SITE', 'STATUT_NC'
        ]
    },
    'RONDE': {
        'model': Ronde,
        'serializer': RondeSerializer,
        'fields': [
            'id', 'date_debut', 'actif', 'date_desactivation', 'description', 'frequence', 'profiles', 'titre',
            't_orp', 'type_ronde', 'batiment_id', 'cmsite_id', 'equipement_id', 'espace_id', 'niveau_id',
            'prestataire_id', 'prestation', 'type_realisation_id'
        ],
        'dependencies': ['BATIMENT', 'SITE', 'EQUIPEMENT', 'ESPACE', 'NIVEAU', 'PRESTATAIRE', 'TYPE_REALISATION']
    },
    'RONDE_COMMENTAIRES': {
        'model': RondeCommentaires,
        'serializer': RondeCommentairesSerializer,
        'fields': ['id', 'month', 'text', 'ronde_id'],
        'dependencies': ['RONDE']
    },
    'RONDE_EVENT': {
        'model': RondeEvent,
        'serializer': RondeEventSerializer,
        'fields': ['id', 'heure', 'jour', 'ronde_id'],
        'dependencies': ['RONDE']
    },
    'RONDE_PARAMETRE': {
        'model': RondeParametre,
        'serializer': RondeParametreSerializer,
        'fields': ['id', 'anotifier', 'graphe', 'is_max', 'seuil', 'donnee_mesure_id', 'ronde_id', 'unite_de_mesure_id'],
        'dependencies': ['DONNEE_MESURE', 'RONDE', 'UNITE_MESURE']
    },
    'RONDE_RELEVE': {
        'model': RondeReleve,
        'serializer': RondeReleveSerializer,
        'fields': ['id', 'comment', 'date', 'date_saisie', 'disponible', 'from_mobile', 'rondier', 'valeur', 'ronde_event_id', 'ronde_parametre_id'],
        'dependencies': ['RONDE_EVENT', 'RONDE_PARAMETRE']
    },
    'TYPE_REALISATION': {
        'model': TypeRealisation,
        'serializer': TypeRealisationSerializer,
        'fields': ['id', 'actif', 'designation', 'ordre'],
        'dependencies': []
    },
    'UNITE_MESURE': {
        'model': UniteMesure,
        'serializer': UniteMesureSerializer,
        'fields': ['id', 'is_active', 'unite_de_mesure', 'donnee_mesure_id'],
        'dependencies': ['DONNEE_MESURE']
    },
    'DONNEE_MESURE': {
        'model': DonneeMesure,
        'serializer': DonneeMesureSerializer,
        'fields': ['id', 'column_label', 'is_active', 'donne_mesuree'],
        'dependencies': []
    },
    'INTERVENTION': {
        'model': Intervention,
        'serializer': InterventionSerializer,
        'fields': [
            'id', 'cloture', 'commentaire', 'content_type_one', 'content_type_two', 'date', 'date_cloture',
            'date_debut', 'date_depart_previsionnel', 'date_fin', 'date_fin_prev', 'index_intervention',
            'nom_fichier_1', 'nom_fichier_2', 'ordre', 'prestatire_sous_traitant', 'statut', 'taille',
            'taux_avancement', 'uid_one', 'uid_two', 'cloturer_par_id', 'contrat', 'detail_planification_id', 'fournisseur'
        ],
        'dependencies': ['DETAIL_PLANIFICATION']
    },
    'INTERVENTION_ATTACHEMENT': {
        'model': InterventionAttachement,
        'serializer': InterventionAttachementSerializer,
        'fields': ['id', 'intervention_id', 'photo'],
        'dependencies': ['INTERVENTION']
    },
    'INTERVENTION_INTERVENANTS': {
        'model': InterventionIntervenants,
        'serializer': InterventionIntervenantsSerializer,
        'fields': ['id', 'intervention_id', 'intervenant'],
        'dependencies': ['INTERVENTION']
    },
    'INTERVENTION_PRESTATAIRE': {
        'model': InterventionPrestataire,
        'serializer': InterventionPrestataireSerializer,
        'fields': ['id', 'intervention_id', 'prestataire_id'],
        'dependencies': ['INTERVENTION', 'PRESTATAIRE']
    },
    'PLANIFICATION': {
        'model': Planification,
        'serializer': PlanificationSerializer,
        'fields': ['id', 'date_debut', 'date_fin', 'intitule', 't_orp', 'marche_id', 'prestataire_id', 'prestation', 'site_id'],
        'dependencies': ['MARCHE', 'PRESTATAIRE', 'SITE']
    },
    'DETAIL_PLANIFICATION': {
        'model': DetailPlanification,
        'serializer': DetailPlanificationSerializer,
        'fields': [
            'id', 'charge', 'content_type', 'lieu', 'nom_fichier', 'nombre', 'ordre_fam', 'ordre_lot', 'semaine',
            'size', 'tache', 'task', 'uid', 'criticite_equipement_id', 'equipement_id', 'famille_equipement_id',
            'frequence_id', 'groupe_equipement_id', 'lot_technique_id', 'planification_id', 'type_realisation_id'
        ],
        'dependencies': [
            'CRICITICITE_EQUIPEMENT', 'EQUIPEMENT', 'FAMILLE_EQUIPEMENT', 'FREQUENCE', 'GROUPE_EQUIPEMENT',
            'LOT_TECHNIQUE', 'PLANIFICATION', 'TYPE_REALISATION'
        ]
    },
    'FREQUENCE': {
        'model': Frequence,
        'serializer': FrequenceSerializer,
        'fields': ['id', 'actif', 'couleur', 'designation', 'ordre', 'valeur', 'value'],
        'dependencies': []
    },
    'DETAIL_PLANIFICATION_INTERVENTION': {
        'model': DetailPlanificationIntervention,
        'serializer': DetailPlanificationInterventionSerializer,
        'fields': ['id', 'detail_planification_id', 'intervention_id'],
        'dependencies': ['DETAIL_PLANIFICATION', 'INTERVENTION']
    },
    'USER': {
        'model': User,
        'serializer': UserSerializer,
        'fields': [
            'id', 'actif', 'attempts', 'departement', 'device', 'directeur_agence', 'email', 'enabled', 'foc',
            'fonction', 'gcmid', 'iam', 'last_login', 'loked_date', 'nom', 'notifiable', 'password', 'prenom',
            'rest_tocken', 'role', 'tel', 'username', 'contact', 'fournisseur', 'password_changed_time'
        ],
        'dependencies': []
    },
    'USER_AFFEC': {
        'model': UserAffec,
        'serializer': UserAffecSerializer,
        'fields': ['id', 'peux_cloturer', 'peux_valider', 'marche_id', 'prestataire_id', 'site_id', 'user_id'],
        'dependencies': ['MARCHE', 'PRESTATAIRE', 'SITE', 'USER']
    },
    'MARCHE': {
        'model': Marche,
        'serializer': MarcheSerializer,
        'fields': [
            'id', 'actif', 'alloti', 'code_marche', 'condition_pfpm', 'condition_pprestataire', 'date_approbation',
            'date_attribution', 'date_fin', 'date_ordre_service', 'date_effective', 'designation', 'duree_initiale',
            'duree_preavis_fpm', 'duree_preavis_prestataire', 'duree_renouvellement', 'nombre_lots', 'nombre_renouvellement',
            'nombre_sites', 'numero_marche', 'renouvellement', 'technique', 'prestataire_id', 'rankin_marche', 'type_prestation',
            'support_contractuel'
        ],
        'dependencies': ['PRESTATAIRE']
    }
}  

class DonneeViewSet(viewsets.ViewSet):  
    def list(self, request, *args, **kwargs):  
        all_data = {}  
        # Ordre d'intégration des tables en fonction des Foreign Keys  
        tables_order = [
    'PAYS', 'REGION', 'VILLE', 'IMPORTANCE_GEO', 'TYPE_SITE', 'TYPE_ESPACE',
    'LOT_TECHNIQUE', 'FAMILLE_EQUIPEMENT', 'GROUPE_EQUIPEMENT', 'SITE', 'BATIMENT',
    'NIVEAU', 'ESPACE', 'CRICITICITE_EQUIPEMENT', 'NBR_SITE', 'EQUIPEMENT',
    'PRESTATAIRE', 'STATUT_NC', 'NON_COMFORMITE', 'HISTORIQUE_NC', 'RONDE',
    'RONDE_COMMENTAIRES', 'RONDE_EVENT', 'RONDE_PARAMETRE', 'RONDE_RELEVE',
    'TYPE_REALISATION', 'UNITE_MESURE', 'DONNEE_MESURE', 'INTERVENTION',
    'INTERVENTION_ATTACHEMENT', 'INTERVENTION_INTERVENANTS', 'INTERVENTION_PRESTATAIRE',
    'PLANIFICATION', 'DETAIL_PLANIFICATION', 'FREQUENCE', 'DETAIL_PLANIFICATION_INTERVENTION',
    'USER', 'USER_AFFEC', 'MARCHE'
]

        for table_name in tables_order:  
            config = TABLES_CONFIG[table_name]  
            model = config['model']  
            serializer_class = config['serializer']  
            fields = config['fields']  

            # Récupérer les données depuis SQL Server  
            with connections['default'].cursor() as cursor:  
                cursor.execute(f"SELECT * FROM {table_name}")  
                donnees_sql = cursor.fetchall()  

            # Insérer les données dans PostgreSQL  
            for donnee in donnees_sql:  
                data_dict = dict(zip(fields, donnee))  

                # Gérer les ForeignKey pour chaque table  
                if table_name == 'EQUIPEMENT':  
                    id_espace = data_dict.get('id_espace')  
                    if id_espace:  
                        espace_instance = EspaceSQL.objects.using('postgresql').filter(id=id_espace).first()  
                        if espace_instance:  
                            data_dict['id_espace'] = espace_instance  
                        else:  
                            continue  

                if 'dependencies' in config and config['dependencies']:  
                    for dependency in config['dependencies']:  
                        dependency_id = data_dict.get(f'id_{dependency.lower()}')  
                        if dependency_id:  
                            dependency_model = TABLES_CONFIG[dependency]['model']  
                            instance = dependency_model.objects.using('postgresql').filter(id=dependency_id).first()  
                            if instance:  
                                data_dict[f'id_{dependency.lower()}'] = instance  
                            else:  
                                continue  

                # Créer ou mettre à jour l'objet  
                model.objects.using('postgresql').update_or_create(  
                    id=data_dict['id'], defaults=data_dict  
                )  

            # Récupérer les données mises à jour depuis PostgreSQL  
            queryset = model.objects.using('postgresql').all()  
            serializer = serializer_class(queryset, many=True)  
            all_data[table_name] = serializer.data  

        return Response(all_data)  

# Fonctions pour ArcGIS Online
import requests


def fetch_features_from_arcgis(layer_id=0, token=None):
    """
    Récupère les entités d'une couche spécifique dans un service ArcGIS Online.
    
    :param layer_id: ID de la couche à interroger (par défaut : 0).
    :param token: Token d'accès ArcGIS Online.
    :return: Liste des entités avec leurs attributs et géométries.
    """
    url = f"https://services2.arcgis.com/uaR6EOboD6BtHr7b/arcgis/rest/services/Map_WFS_TEST/FeatureServer/{layer_id}/query"
    params = {
        "where": "1=1",  # Filtre pour récupérer toutes les entités
        "outFields": "*",  # Récupérer tous les champs
        "f": "json",  # Format de réponse
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('features', [])
    except requests.RequestException as e:
        raise Exception(f"Erreur lors de l'appel à l'API ArcGIS Online: {str(e)}")

# Exemple d'utilisation
features = fetch_features_from_arcgis(layer_id=0)
for feature in features:
    print(feature)
def convert_arcgis_geometry_to_django(geometry):
    if geometry.get('rings'):
        coordinates = geometry['rings'][0]
        return Polygon(coordinates)
    elif geometry.get('x') and geometry.get('y'):
        return Point(geometry['x'], geometry['y'])
    else:
        raise ValueError("Format de géométrie non supporté")
from pyproj import Transformer

def convert_projection(geometry, from_epsg, to_epsg):
    """
    Convertit une géométrie d'un système de coordonnées à un autre.
    
    :param geometry: Géométrie Django GEOS.
    :param from_epsg: Code EPSG source (par exemple, 3857 pour Web Mercator).
    :param to_epsg: Code EPSG cible (par exemple, 4326 pour WGS84).
    :return: Géométrie convertie.
    """
    transformer = Transformer.from_crs(f"EPSG:{from_epsg}", f"EPSG:{to_epsg}", always_xy=True)
    
    if isinstance(geometry, Point):
        x, y = transformer.transform(geometry.x, geometry.y)
        return Point(x, y)
    elif isinstance(geometry, Polygon):
        new_coords = [transformer.transform(x, y) for x, y in geometry.coords[0]]
        return Polygon(new_coords)
    elif isinstance(geometry, MultiPolygon):
        new_polygons = []
        for polygon in geometry:
            new_coords = [transformer.transform(x, y) for x, y in polygon.coords[0]]
            new_polygons.append(Polygon(new_coords))
        return MultiPolygon(new_polygons)
    else:
        raise ValueError(f"Type de géométrie non supporté pour la conversion: {type(geometry)}")
# Fonctions de mise à jour
def update_espace_geometries():
    polygons = fetch_features_from_arcgis()
    espaces_to_update = []

    for polygon_feature in polygons:
        espace_code = polygon_feature['attributes'].get('Espace')
        geometry = polygon_feature['geometry']
        spatial_reference = geometry.get('spatialReference', {}).get('wkid', 3857)  # Par défaut Web Mercator

        print(f"Espace: {espace_code}, Projection: EPSG:{spatial_reference}")

        try:
            django_polygon = convert_arcgis_geometry_to_django(geometry)
            
            # Convertir la projection de Web Mercator (3857) à WGS84 (4326)
            if spatial_reference == 3857:  # Vérifiez que la projection est bien Web Mercator
                django_polygon = convert_projection(django_polygon, from_epsg=3857, to_epsg=4326)
            
            espace = EspaceSQL.objects.filter(intitule=espace_code).first()
            if espace:
                espace.geom = django_polygon
                espaces_to_update.append(espace)
                print(f"Géométrie mise à jour pour l'espace {espace_code}")
        except ValueError as e:
            print(f"Erreur de conversion de géométrie pour l'espace {espace_code}: {str(e)}")

    if espaces_to_update:
        EspaceSQL.objects.bulk_update(espaces_to_update, ['geom'])
def update_equipement_geometries():
    equipements_to_update = []

    for equipement in EquipementSQL.objects.select_related('id_espace').all():
        if equipement.id_espace and equipement.id_espace.geom:
            polygon = equipement.id_espace.geom
            min_x, min_y, max_x, max_y = polygon.extent

            while True:
                random_point = Point(uniform(min_x, max_x), uniform(min_y, max_y))
                if polygon.contains(random_point):
                    equipement.geom = random_point
                    equipements_to_update.append(equipement)
                    break

    if equipements_to_update:
        EquipementSQL.objects.bulk_update(equipements_to_update, ['geom'])

# Vue pour mettre à jour les géométries
class UpdateGeometriesView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            update_espace_geometries()
            update_equipement_geometries()
            return Response({"status": "Geometries updated successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
class EquipementSQLViewSet(viewsets.ModelViewSet):
    queryset = EquipementSQL.objects.all()[8000:]
    serializer_class = EquipementSQLSerializer
class ArcGISLayerAPI(APIView):
    def get(self, request, *args, **kwargs):
        """
        Récupère les données de la couche ArcGIS et les renvoie au format JSON.
        """
        try:
            # URL de la couche ArcGIS
            layer_url = "https://services2.arcgis.com/uaR6EOboD6BtHr7b/arcgis/rest/services/Map_WFS_TEST/FeatureServer/0/query"
            params = {
                "where": "1=1",  # Récupérer toutes les entités
                "outFields": "*",  # Récupérer tous les champs
                "f": "json",  # Format de réponse
            }

            # Faire la requête à l'API ArcGIS
            response = requests.get(layer_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Renvoyer les données au client
            return Response(data.get('features', []))
        except requests.RequestException as e:
            return Response({"error": f"Erreur lors de la récupération des données ArcGIS : {str(e)}"}, status=500)