from rest_framework import viewsets
from django.utils import timezone  
from datetime import datetime 
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
CriticiteNC,    StatutNC,  
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
    Marche  ,
    StatutAction,Action
)    
from .serializers import (  
    StatutActionSerializer,
    ActionSerializer,
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
    MarcheSerializer  ,
    CriticiteNCSerializer
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
        'fields': ['id', 'actif','designation','ordre'],  
        'dependencies': []  
    },  
        'CRICITICITE_NC': {  
        'model': CriticiteNC,  
        'serializer': CriticiteNCSerializer,  
        'fields': ['id', 'actif','designation','ordre'],  
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
        'dependencies': ['NON_COMFORMITE', 'STATUT_NC']
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
            'BATIMENT', 'CRICITICITE_NC', 'EQUIPEMENT', 'ESPACE', 'FAMILLE_EQUIPEMENT', 'IMPORTANCE_GEO',
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
        'fields': [ 'intervention_id', 'photo'],
        'dependencies': ['INTERVENTION']
    },
    'INTERVENTION_INTERVENANTS': {
        'model': InterventionIntervenants,
        'serializer': InterventionIntervenantsSerializer,
        'fields': ['intervention_id', 'intervenant'],
        'dependencies': ['INTERVENTION']
    },
    'INTERVENTION_PRESTATAIRE': {
        'model': InterventionPrestataire,
        'serializer': InterventionPrestataireSerializer,
        'fields': ['intervention_id', 'prestataire_id'],
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
        'fields': ['detail_planification_id', 'intervention_id'],
        'dependencies': ['DETAIL_PLANIFICATION', 'INTERVENTION']
    },
    'users': {
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
    },'STATUT_ACTION': {  
    'model': StatutAction,  
    'serializer': StatutActionSerializer,  
    'fields': ['id', 'actif', 'designation', 'ordre'],  
    'dependencies': []  
},  'ACTION': {  
    'model': Action,  
    'serializer': ActionSerializer,  
    'fields': [  
        'id', 'budget_action', 'commentaire', 'content_type',   
        'date_debut', 'date_fin_p', 'date_fin', 'date_suspens',   
        'date_validation', 'demande', 'detail_action', 'need_val',   
        'nom_fichier', 'num_save', 'numero_action', 'pdr_conso',   
        'responsable', 'taux_avancement', 'technicien', 'uid',   
        'valid', 'valider_par', 'idt_nc_id', 'pst_action_id',   
        'statut_action_id_id'  
    ],  
    'dependencies': ['STATUT_ACTION', 'NON_COMFORMITE'],  # Assuming NON_CONFORMITE is defined similarly  
},  
}  

class DonneeViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        all_data = {}
        tables_order = [
            'PAYS', 'REGION', 'VILLE', 'IMPORTANCE_GEO', 'TYPE_SITE', 'TYPE_ESPACE',
            'LOT_TECHNIQUE', 'FAMILLE_EQUIPEMENT', 'GROUPE_EQUIPEMENT', 'SITE', 'BATIMENT',
            'NIVEAU', 'ESPACE', 'CRICITICITE_EQUIPEMENT', 'NBR_SITE', 'EQUIPEMENT',
            'PRESTATAIRE', 'CRICITICITE_NC', 'STATUT_NC', 'STATUT_ACTION', 'NON_COMFORMITE',
            'HISTORIQUE_NC', 'TYPE_REALISATION', 'RONDE',
            'RONDE_COMMENTAIRES', 'RONDE_EVENT', 'DONNEE_MESURE', 'UNITE_MESURE',
            'RONDE_PARAMETRE', 'RONDE_RELEVE', 'FREQUENCE', 'MARCHE', 'PLANIFICATION',
            'DETAIL_PLANIFICATION', 'INTERVENTION',
            'INTERVENTION_ATTACHEMENT', 'INTERVENTION_INTERVENANTS', 'INTERVENTION_PRESTATAIRE',
            'DETAIL_PLANIFICATION_INTERVENTION', 'users', 'USER_AFFEC', 'ACTION'
        ]

        for table_name in tables_order:
            if table_name == 'NON_COMFORMITE':
                # Traitement spécial pour NON_COMFORMITE
                try:
                    with connections['default'].cursor() as cursor:
                        cursor.execute("SELECT * FROM NON_COMFORMITE")
                        columns = [col[0] for col in cursor.description]
                        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

                    for item in data:
                        # Mapping des champs comme dans NonConformiteView
                        item_mapped = {
                            'id': item.get('ID'),
                            'equipement_dispo': item.get('EquipementDispo'),
                            'astreinte': item.get('astreinte'),
                            'code_signalement': item.get('codeSignalement'),
                            'constate_par': item.get('constatepar'),
                            'contact_prestataire': item.get('contactPrestataire'),
                            'date': item.get('date'),
                            'date_debut_indisp': item.get('DATE_DEBUT_INDISP'),
                            'date_fpm': item.get('dateFPM'),
                            'date_paliatif': item.get('datePaliatif'),
                            'date_planification': item.get('datePlanification'),
                            'date_previsionnelle': item.get('DATE_PREVESIONNELLE'),
                            'date_retablissement': item.get('dateRetablissement'),
                            'date_retablissement_final': item.get('dateRetablissementFinal'),
                            'delai_intervention': item.get('delaiIntervention'),
                            'descriptif': item.get('descriptif'),
                            'descriptif_fpm': item.get('descriptifFPM'),
                            'diagnostic': item.get('diagnostic'),
                            'email': item.get('email'),
                            'equipement_saisie': item.get('equipementSaisie'),
                            'espace_saisie': item.get('espaceSaisie'),
                            'exterieur': item.get('exterieur'),
                            'fait_marquant': item.get('faitMarquant'),
                            'foc': item.get('foc'),
                            'date_annulation': item.get('DATE_ANNULATION'),
                            'date_pencharge': item.get('DATE_PENCHARGE'),
                            'lot_saisie': item.get('lotSaisie'),
                            'mobile': item.get('mobile'),
                            'motif_annulation': item.get('motifannulation'),
                            'n_fnc': item.get('nFNC'),
                            'nc_retablie': item.get('ncRetablie'),
                            'nom_fichier': item.get('NOM_FICHIER'),
                            'partial': item.get('partial'),
                            'photo_first': item.get('photoFirst'),
                            'signale_par': item.get('signalepar'),
                            'st_prestataire': item.get('stPrestataire'),
                            't_orp': item.get('tOrp'),
                            'tel': item.get('tel'),
                            'titre': item.get('titre'),
                            'titre_prestataire': item.get('titrePrestataire'),
                            'uid': item.get('uid'),
                            'valeur1': item.get('valeur1'),
                            'valeur2': item.get('valeur2'),
                            'valeur3': item.get('valeur3'),
                            'valeur4': item.get('valeur4'),
                            'batiment_id': item.get('batiment_ID'),
                            'criticite_non_conformite_id': item.get('criticiteNonConformite_ID'),
                            'equipement_id': item.get('equipement_ID'),
                            'espace_id': item.get('IDT_ESPACE'),
                            'famille_equipement_id': item.get('familleEquipement_ID'),
                            'importance_geographique_id': item.get('importanceGeographique_ID'),
                            'lot_technique_id': item.get('lotTechnique_ID'),
                            'marche_id': item.get('marche_ID'),
                            'niveau_id': item.get('niveau_ID'),
                            'prestataire_id': item.get('prestataire_ID'),
                            'prestataire_fpm_id': item.get('prestataireFPM_ID'),
                            'prestataire_st_id': item.get('prestataireST_ID'),
                            'prestation_service': item.get('prestationService_ID'),
                            'site_id': item.get('site_ID'),
                            'statut_nc_id': item.get('statutNC_ID'),
                        }

                        # Gestion des clés étrangères
                        foreign_keys = [
                            'batiment_id', 'criticite_non_conformite_id', 'equipement_id',
                            'espace_id', 'famille_equipement_id', 'importance_geographique_id',
                            'lot_technique_id', 'marche_id', 'niveau_id', 'prestataire_id',
                            'prestataire_fpm_id', 'prestataire_st_id', 'site_id', 'statut_nc_id'
                        ]

                        for fk in foreign_keys:
                            if item_mapped.get(fk) is None:
                                item_mapped[fk] = None

                        # Créer ou mettre à jour l'instance
                        NonConformite.objects.using('postgresql').update_or_create(
                            id=item_mapped['id'],
                            defaults=item_mapped
                        )

                    # Récupérer les données pour la réponse
                    queryset = NonConformite.objects.using('postgresql').all()
                    serializer = NonConformiteSerializer(queryset, many=True)
                    all_data[table_name] = serializer.data

                except Exception as e:
                    print(f"Error processing NON_COMFORMITE: {e}")
                    continue
            elif table_name == 'HISTORIQUE_NC':
                try:  
                    # Connect to SQL Server and fetch data  
                    with connections['default'].cursor() as cursor:  
                        cursor.execute("SELECT * FROM  HISTORIQUE_NC")  
                        columns = [col[0] for col in cursor.description]  
                        criticite_data = [dict(zip(columns, row)) for row in cursor.fetchall()]  

                    # Log fetched data for debugging  
                    print("Fetched Data: ", criticite_data)  

                    # Store or update data in PostgreSQL  
                    for item in criticite_data:  
                        if 'ID' not in item or item['ID'] is None:  
                            print(f"Skipping item due to missing id: {item}")  
                            continue  # Skip if ID is missing  

                        # Prepare item for integration  
                        criticite_nc, created = HistoriqueNC.objects.using('postgresql').update_or_create(  
                            id=item['ID'],  # Use ID for primary key  
                            defaults={  
                                'date': item['date'],  
                                'mobile': item['mobile'],  
                                'utilisateur': item['utilisateur']  ,
                                'non_conformite_id': item['nonConformite_ID']  ,
                                'statut_nc_id': item['statutNC_ID']  ,
                            }  
                        )  

                    # Retrieve updated data to return  
                    queryset = HistoriqueNC.objects.using('postgresql').all()  
                    serializer = HistoriqueNCSerializer(queryset, many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)  

                except Exception as e:  
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
            else:
                # Traitement normal pour les autres tables
                config = TABLES_CONFIG.get(table_name)
                if not config:
                    print(f"Skipping {table_name} - not in TABLES_CONFIG")
                    continue
                
                model = config['model']
                serializer_class = config['serializer']
                fields = config['fields']

                # Fetch data from SQL Server
                with connections['default'].cursor() as cursor:
                    try:
                        cursor.execute(f"SELECT * FROM {table_name}")
                        donnees_sql = cursor.fetchall()
                    except Exception as e:
                        print(f"Error fetching data from {table_name}: {e}")
                        continue

                for donnee in donnees_sql:
                    try:
                        data_dict = dict(zip(fields, donnee))
                        if 'id' not in data_dict or not data_dict['id']:
                            continue

                        # Handling ForeignKey fields
                        if 'dependencies' in config and config['dependencies']:
                            for dependency in config['dependencies']:
                                dependency_id = data_dict.get(f'id_{dependency.lower()}') or data_dict.get(f'{dependency.lower()}_id')
                                if dependency_id:
                                    dependency_model = TABLES_CONFIG[dependency]['model']
                                    instance = dependency_model.objects.using('postgresql').filter(id=dependency_id).first()
                                    if instance:
                                        data_dict[f'id_{dependency.lower()}'] = instance
                                        data_dict[f'{dependency.lower()}_id'] = instance.id
                                    else:
                                        continue

                        # Create or update the object
                        try:
                            model.objects.using('postgresql').update_or_create(
                                id=data_dict['id'],
                                defaults=data_dict
                            )
                        except Exception as e:
                            print(f"Error updating or creating {table_name} with id {data_dict['id']}: {e}")
                            continue

                    except Exception as e:
                        print(f"Error processing record from {table_name}: {e}")
                        continue

                # Retrieve data from PostgreSQL for response
                queryset = model.objects.using('postgresql').all()
                serializer = serializer_class(queryset, many=True)
                all_data[table_name] = serializer.data

        return Response(all_data)
# Fonctions pour ArcGIS Online
import requests


def fetch_features_from_arcgis(layer_id=1, token=None):
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

    count_null_attributes = 0  # Initialize a counter for features with NULL attributes  

    for polygon_feature in polygons:  
        attributes = polygon_feature['attributes']  
        espace_code = attributes.get('Espace')  
        batiment_code = attributes.get('Bâtiment')  
        niveau_code = attributes.get('Niveau')  
        geometry = polygon_feature.get('geometry')  

        # Log and skip features with NULL attributes  
        if espace_code is None and batiment_code is None and niveau_code is None:  
            count_null_attributes += 1  # Increment counter  
            print("Feature with NULL attributes found. Skipping...")  
            continue  

        # Check if any of the essential attributes are NULL  
        if not all([espace_code, batiment_code, niveau_code]):  
            print(f"Feature incomplete - Espace: {espace_code}, Bâtiment: {batiment_code}, Niveau: {niveau_code}")  
            continue  

        if geometry is None:  
            print("La géométrie n'existe pas pour cette feature.")  
            continue  # Skip this feature since it has no geometry.  

        # Proceed with your existing processing logic...  
        spatial_reference = geometry.get('spatialReference', {}).get('wkid', 3857)  

        try:  
            django_polygon = convert_arcgis_geometry_to_django(geometry)  

            if spatial_reference == 3857:  
                django_polygon = convert_projection(django_polygon, from_epsg=3857, to_epsg=4326)  

            # Perform the database lookup and update operations as before.  
            espace = EspaceSQL.objects.filter(  
                intitule__exact=espace_code,  
                id_niveau__intitule__exact=niveau_code,  
                id_niveau__id_batiment__intitule__exact=batiment_code  
            ).select_related('id_niveau', 'id_niveau__id_batiment').first()  

            if espace:  
                espace.geom = django_polygon  
                espaces_to_update.append(espace)  
                print(f"Correspondance exacte trouvée - Mise à jour géométrie pour {espace_code} (Bâtiment: {batiment_code}, Niveau: {niveau_code})")  
            else:  
                print(f"Aucun espace trouvé avec la combinaison exacte: {espace_code}|{batiment_code}|{niveau_code}")  

        except ValueError as e:  
            print(f"Erreur de conversion pour {espace_code}: {str(e)}")  
        except Exception as e:  
            print(f"Erreur inattendue pour {espace_code}: {str(e)}")  

    # Log number of skipped polygons with NULL attributes  
    print(f"Nombre de polygones ignorés avec attributs NULL: {count_null_attributes}")  

    if espaces_to_update:  
        EspaceSQL.objects.bulk_update(espaces_to_update, ['geom'])  
        print(f"{len(espaces_to_update)} géométries mises à jour avec succès")  
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
            # Dictionnaire pour suivre les URLs déjà traitées
            processed_urls = set()

            # Récupérer tous les niveaux avec des URLs de webservice uniques
            niveaux = Niveau.objects.exclude(url_web_service__isnull=True).exclude(url_web_service__exact='')

            for niveau in niveaux:
                if niveau.url_web_service in processed_urls:
                    print(f"URL déjà traitée: {niveau.url_web_service} - Skipping...")
                    continue
                
                processed_urls.add(niveau.url_web_service)
                print(f"Traitement de l'URL: {niveau.url_web_service}")

                try:
                    # Extraire le layer_id de l'URL si nécessaire
                    layer_id = 0  # Valeur par défaut
                    if '/FeatureServer/' in niveau.url_web_service:
                        parts = niveau.url_web_service.split('/FeatureServer/')
                        if len(parts) > 1:
                            layer_id = int(parts[1].split('/')[0])

                    # Mettre à jour les géométries pour ce webservice
                    self.update_geometries_for_webservice(niveau.url_web_service, layer_id)
                    
                except Exception as e:
                    print(f"Erreur lors du traitement de l'URL {niveau.url_web_service}: {str(e)}")
                    continue

            return Response({"status": "Geometries updated successfully", "processed_urls": list(processed_urls)})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def update_geometries_for_webservice(self, webservice_url, layer_id=0):
        """
        Met à jour les géométries pour un webservice spécifique
        """
        def fetch_features_from_url(url, layer_id):
            """Version modifiée de fetch_features_from_arcgis pour utiliser l'URL spécifique"""
            url = f"{url}/query" if not url.endswith('/query') else url
            params = {
                "where": "1=1",
                "outFields": "*",
                "f": "json",
            }
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                return data.get('features', [])
            except requests.RequestException as e:
                raise Exception(f"Erreur lors de l'appel à l'API: {str(e)}")

        # Récupérer les features depuis le webservice
        features = fetch_features_from_url(webservice_url, layer_id)
        espaces_to_update = []
        count_null_attributes = 0

        for feature in features:
            attributes = feature['attributes']
            espace_code = attributes.get('Espace')
            batiment_code = attributes.get('Bâtiment')
            niveau_code = attributes.get('Niveau')
            geometry = feature.get('geometry')

            if espace_code is None and batiment_code is None and niveau_code is None:
                count_null_attributes += 1
                continue

            if not all([espace_code, batiment_code, niveau_code]):
                continue

            if geometry is None:
                continue

            spatial_reference = geometry.get('spatialReference', {}).get('wkid', 3857)

            try:
                django_polygon = convert_arcgis_geometry_to_django(geometry)

                if spatial_reference == 3857:
                    django_polygon = convert_projection(django_polygon, from_epsg=3857, to_epsg=4326)

                espace = EspaceSQL.objects.filter(
                    intitule__exact=espace_code,
                    id_niveau__intitule__exact=niveau_code,
                    id_niveau__id_batiment__intitule__exact=batiment_code
                ).select_related('id_niveau', 'id_niveau__id_batiment').first()

                if espace:
                    espace.geom = django_polygon
                    espaces_to_update.append(espace)
                    print(f"Mise à jour géométrie pour {espace_code}")

            except ValueError as e:
                print(f"Erreur de conversion pour {espace_code}: {str(e)}")
            except Exception as e:
                print(f"Erreur inattendue pour {espace_code}: {str(e)}")

        if espaces_to_update:
            EspaceSQL.objects.bulk_update(espaces_to_update, ['geom'])
            print(f"{len(espaces_to_update)} géométries mises à jour pour le webservice {webservice_url}")

        # Mise à jour des équipements après les espaces
        self.update_equipement_geometries()

    def update_equipement_geometries(self):
        """Version optimisée de update_equipement_geometries"""
        equipements_to_update = []
        
        # Récupérer seulement les équipements dans des espaces avec géométrie
        equipements = EquipementSQL.objects.filter(
            id_espace__geom__isnull=False
        ).select_related('id_espace')

        for equipement in equipements:
            polygon = equipement.id_espace.geom
            min_x, min_y, max_x, max_y = polygon.extent

            # Essayer 10 fois max pour trouver un point aléatoire dans le polygone
            for _ in range(10):
                random_point = Point(uniform(min_x, max_x), uniform(min_y, max_y))
                if polygon.contains(random_point):
                    equipement.geom = random_point
                    equipements_to_update.append(equipement)
                    break

        if equipements_to_update:
            EquipementSQL.objects.bulk_update(equipements_to_update, ['geom'])
            print(f"{len(equipements_to_update)} positions d'équipements mises à jour")
class EquipementSQLViewSet(viewsets.ModelViewSet):
    queryset = EquipementSQL.objects.all()
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
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import connections
from datetime import datetime
from django.utils import timezone
from django.contrib.gis.geos import Point
import logging

logger = logging.getLogger(__name__)

class AutoSyncView(viewsets.ViewSet):
    """
    Vue avec correspondance correcte entre tables SQL Server et modèles Django
    """
    # Mapping entre noms de tables SQL Server et noms de modèles Django
    TABLE_MODEL_MAPPING = {
        #'STATUT_NC': 'StatutNC',
        #'CRICITICITE_NC': 'CriticiteNC',
        #'STATUT_ACTION': 'StatutAction',
        #'SITE': 'SiteSQL',
        #'BATIMENT': 'Batiment',
        #'NIVEAU': 'Niveau',
        #'ESPACE': 'EspaceSQL',
        'EQUIPEMENT': 'EquipementSQL',
        #'PRESTATAIRE': 'Prestataire',
        #'users': 'User',
        'NON_COMFORMITE': 'NonConformite',
        #'HISTORIQUE_NC': 'HistoriqueNC',
        #'PLANIFICATION': 'Planification',
        #'FREQUENCE': 'Frequence',
        #'DETAIL_PLANIFICATION': 'DetailPlanification',
        'INTERVENTION': 'Intervention',
        #'INTERVENTION_ATTACHEMENT': 'InterventionAttachement',
        #'INTERVENTION_INTERVENANTS': 'InterventionIntervenants',
        #'INTERVENTION_PRESTATAIRE': 'InterventionPrestataire',
        #'DETAIL_PLANIFICATION_INTERVENTION': 'DetailPlanificationIntervention',
        #'RONDE': 'Ronde',
        #'RONDE_COMMENTAIRES': 'RondeCommentaires',
        #'RONDE_EVENT': 'RondeEvent',
        #'RONDE_PARAMETRE': 'RondeParametre',
        #'RONDE_RELEVE': 'RondeReleve',
        #'ACTION': 'Action'
    }

    def list(self, request):
        """Endpoint principal avec gestion des correspondances"""
        try:
            sync_report = {}
            
            for sql_table, django_model in self.TABLE_MODEL_MAPPING.items():
                try:
                    logger.info(f"Début synchronisation table: {sql_table} -> {django_model}")
                    table_result = self._sync_table(sql_table, django_model)
                    sync_report[sql_table] = table_result
                    logger.info(f"Table {sql_table} synchronisée: {table_result['count']} enregistrements")
                except Exception as e:
                    logger.error(f"Erreur avec la table {sql_table}: {str(e)}")
                    sync_report[sql_table] = {
                        'count': 0,
                        'errors': [str(e)],
                        'last_id': None
                    }

            return Response({
                'status': 'success',
                'sync_report': sync_report,
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Erreur globale de synchronisation: {str(e)}", exc_info=True)
            return Response({
                'status': 'error',
                'message': str(e),
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _sync_table(self, sql_table, django_model):
        """Méthode avec correspondance des noms de tables"""
        try:
            model = globals().get(django_model)
            if not model:
                raise ValueError(f"Modèle Django {django_model} introuvable")

            with connections['default'].cursor() as cursor:
                cursor.execute(f"SELECT * FROM {sql_table} WITH (NOLOCK)")
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            success_count = 0
            errors = []
            last_id = None

            for row in rows:
                try:
                    row_data = dict(zip(columns, row))
                    
                    # Nettoyage spécifique pour chaque table
                    if sql_table == 'NON_COMFORMITE':
                        cleaned_data = self._clean_nc_data(row_data)
                    else:
                        cleaned_data = self._clean_generic_data(row_data)
                    
                    # Gestion des relations
                    cleaned_data = self._handle_relations(sql_table, cleaned_data)
                    
                    # Conversion des dates
                    cleaned_data = self._convert_dates(cleaned_data)
                    
                    # Insertion/Mise à jour
                    obj, created = model.objects.using('postgresql').update_or_create(
                        id=cleaned_data['id'],
                        defaults=cleaned_data
                    )
                    success_count += 1
                    last_id = obj.id
                    
                except Exception as e:
                    errors.append(f"ID {row_data.get('ID')}: {str(e)}")
                    continue

            return {
                'count': success_count,
                'errors': errors,
                'last_id': last_id
            }

        except DatabaseError as e:
            logger.error(f"Erreur DB avec {sql_table}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Erreur avec {sql_table}: {str(e)}")
            raise

    def _clean_nc_data(self, row_data):
        """Nettoyage spécifique pour NON_COMFORMITE"""
        return {
            'id': row_data['ID'],
            'equipement_dispo': bool(row_data.get('EquipementDispo', True)),
            'astreinte': bool(row_data.get('astreinte', False)),
            'code_signalement': row_data.get('codeSignalement', ''),
            'constate_par': row_data.get('constatepar'),
            'contact_prestataire': row_data.get('contactPrestataire'),
            'date': row_data.get('date'),
            'date_debut_indisp': row_data.get('DATE_DEBUT_INDISP'),
            'date_fpm': row_data.get('dateFPM'),
            'date_paliatif': row_data.get('datePaliatif'),
            'date_planification': row_data.get('datePlanification'),
            'date_previsionnelle': row_data.get('DATE_PREVESIONNELLE'),
            'date_retablissement': row_data.get('dateRetablissement'),
            'date_retablissement_final': row_data.get('dateRetablissementFinal'),
            'delai_intervention': row_data.get('delaiIntervention'),
            'descriptif': row_data.get('descriptif', ''),
            'descriptif_fpm': row_data.get('descriptifFPM'),
            'diagnostic': row_data.get('diagnostic'),
            'email': row_data.get('email'),
            'equipement_saisie': row_data.get('equipementSaisie'),
            'espace_saisie': row_data.get('espaceSaisie'),
            'exterieur': bool(row_data.get('exterieur', False)),
            'fait_marquant': bool(row_data.get('faitMarquant', False)),
            'foc': row_data.get('foc'),
            'date_annulation': row_data.get('DATE_ANNULATION'),
            'date_pencharge': row_data.get('DATE_PENCHARGE'),
            'lot_saisie': row_data.get('lotSaisie'),
            'mobile': bool(row_data.get('mobile', False)),
            'motif_annulation': row_data.get('motifannulation'),
            'n_fnc': row_data.get('nFNC'),
            'nc_retablie': bool(row_data.get('ncRetablie', False)),
            'nom_fichier': row_data.get('NOM_FICHIER'),
            'partial': bool(row_data.get('partial', False)),
            'photo_first': row_data.get('photoFirst'),
            'signale_par': row_data.get('signalepar'),
            'st_prestataire': row_data.get('stPrestataire'),
            't_orp': bool(row_data.get('tOrp', False)),
            'tel': row_data.get('tel'),
            'titre': row_data.get('titre', ''),
            'titre_prestataire': row_data.get('titrePrestataire'),
            'uid': row_data.get('uid'),
            'valeur1': bool(row_data.get('valeur1', False)),
            'valeur2': bool(row_data.get('valeur2', False)),
            'valeur3': bool(row_data.get('valeur3', False)),
            'valeur4': bool(row_data.get('valeur4', False)),
            'batiment_id': row_data.get('batiment_ID'),
            'criticite_non_conformite_id': row_data.get('criticiteNonConformite_ID'),
            'equipement_id': row_data.get('equipement_ID'),
            'espace_id': row_data.get('IDT_ESPACE'),
            'famille_equipement_id': row_data.get('familleEquipement_ID'),
            'importance_geographique_id': row_data.get('importanceGeographique_ID'),
            'lot_technique_id': row_data.get('lotTechnique_ID'),
            'marche_id': row_data.get('marche_ID'),
            'niveau_id': row_data.get('niveau_ID'),
            'prestataire_id': row_data.get('prestataire_ID'),
            'prestataire_fpm_id': row_data.get('prestataireFPM_ID'),
            'prestataire_st_id': row_data.get('prestataireST_ID'),
            'prestation_service_id': row_data.get('prestationService_ID'),
            'site_id': row_data.get('site_ID'),
            'statut_nc_id': row_data.get('statutNC_ID')
        }

    def _clean_generic_data(self, row_data):
        """Nettoyage générique des données"""
        return {k.lower(): v for k, v in row_data.items()}

    def _handle_relations(self, sql_table, data):
        """Gestion des relations avec mapping correct"""
        relation_config = {
            'NON_COMFORMITE': {
                'statut_nc_id': ('StatutNC', 'id'),
                'criticite_non_conformite_id': ('CriticiteNC', 'id'),
                'equipement_id': ('EquipementSQL', 'id'),
                'site_id': ('SiteSQL', 'id'),
                'batiment_id': ('Batiment', 'id'),
                'espace_id': ('EspaceSQL', 'id'),
                'famille_equipement_id': ('FamilleEquipement', 'id'),
                'importance_geographique_id': ('ImportanceGeo', 'id'),
                'lot_technique_id': ('LotTechnique', 'id'),
                'marche_id': ('Marche', 'id'),
                'niveau_id': ('Niveau', 'id'),
                'prestataire_id': ('Prestataire', 'id'),
                'prestataire_fpm_id': ('Prestataire', 'id'),
                'prestataire_st_id': ('Prestataire', 'id')
            },
            'HISTORIQUE_NC': {
                'non_conformite_id': ('NonConformite', 'id'),
                'statut_nc_id': ('StatutNC', 'id')
            },
            'ACTION': {
                'idt_nc_id': ('NonConformite', 'id'),
                'statut_action_id': ('StatutAction', 'id')
            }
        }

        if sql_table in relation_config:
            for field, (model_name, field_name) in relation_config[sql_table].items():
                if field in data and data[field]:
                    try:
                        related_model = globals().get(model_name)
                        if related_model:
                            instance = related_model.objects.using('postgresql').filter(**{field_name: data[field]}).first()
                            data[field] = instance.id if instance else None
                    except Exception as e:
                        logger.warning(f"Erreur relation {field}: {str(e)}")
                        data[field] = None

        return data

    def _convert_dates(self, data):
        """Conversion robuste des dates"""
        date_fields = [k for k in data.keys() if k.startswith('date') or '_date' in k or k.endswith('_at')]
        
        for field in date_fields:
            if data.get(field) and isinstance(data[field], datetime):
                try:
                    data[field] = timezone.make_aware(data[field])
                except Exception as e:
                    logger.warning(f"Erreur conversion date {field}: {str(e)}")
                    data[field] = None
        
        return data