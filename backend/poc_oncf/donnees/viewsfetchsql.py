from rest_framework import viewsets  
from rest_framework import status  
from .models import CriticiteNC  
from .serializers import CriticiteNCSerializer 
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
    SiteSQL,  
    Batiment,  
    Niveau,  
    TypeEspace,  
    EspaceSQL,  
    Prestataire,  
    CriticiteEquipement,  
    NbrSite,  
    EquipementSQL,  # Updated to 'Equipement SQL'  
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
    Marche  ,
    StatutAction,
    Action
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
    MarcheSerializer  ,
    ActionSerializer,
    StatutActionSerializer
)  
from django.db import connections  
from rest_framework.response import Response  
from rest_framework.views import APIView  


class PaysView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM PAYS")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                Pays.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'designation': item['DESIGNATION'],
                    }
                )

            queryset = Pays.objects.using('postgresql').all()
            serializer = PaysSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 2. Region
class RegionView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM REGION")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                Region.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'designation': item['DESIGNATION'],
                        'id_pays': Pays.objects.using('postgresql').get(id=item['IDT_PAYS']),
                    }
                )

            queryset = Region.objects.using('postgresql').all()
            serializer = RegionSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 3. Ville
class VilleView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM VILLE")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                Ville.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'designation': item['DESIGNATION'],
                        'display_name': item['DISPLAYNAME'],
                        'id_region': Region.objects.using('postgresql').get(id=item['IDT_REGION']),
                    }
                )

            queryset = Ville.objects.using('postgresql').all()
            serializer = VilleSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 4. ImportanceGeo
class ImportanceGeoView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM IMPORTANCE_GEO")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                ImportanceGeo.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'designation': item['DESIGNATION'],
                        'ordre': item['ORDRE'],
                    }
                )

            queryset = ImportanceGeo.objects.using('postgresql').all()
            serializer = ImportanceGeoSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 5. TypeSite
class TypeSiteView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM TYPE_SITE")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                TypeSite.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'designation': item['DESIGNATION'],
                    }
                )

            queryset = TypeSite.objects.using('postgresql').all()
            serializer = TypeSiteSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 6. LotTechnique
class LotTechniqueView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM LOT_TECHNIQUE")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                LotTechnique.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'code_lot': item['CODE_LOT'],
                        'designation': item['DESIGNATION'],
                        'module': item['MODULE'],
                    }
                )

            queryset = LotTechnique.objects.using('postgresql').all()
            serializer = LotTechniqueSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 7. FamilleEquipement
class FamilleEquipementView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM FAMILLE_EQUIPEMENT")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                FamilleEquipement.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'code_famille': item['CODE_FAMILLE'],
                        'designation': item['DESIGNATION'],
                        'module': item['MODULE'],
                        'id_lot': LotTechnique.objects.using('postgresql').get(id=item['IDT_LOT']),
                    }
                )

            queryset = FamilleEquipement.objects.using('postgresql').all()
            serializer = FamilleEquipementSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 8. GroupeEquipement
class GroupeEquipementView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM GROUPE_EQUIPEMENT")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                GroupeEquipement.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'designation': item['DESIGNATION'],
                        'id_famille_equipement': FamilleEquipement.objects.using('postgresql').get(id=item['IDT_FAMILLE_EQUIPEMENT']),
                    }
                )

            queryset = GroupeEquipement.objects.using('postgresql').all()
            serializer = GroupeEquipementSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 9. Batiment
class BatimentView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM BATIMENT")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                Batiment.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'code_batiment': item['CODE_BATIMENT'],
                        'intitule': item['INTITULE'],
                        'type_batiment': item['TYPE_BATIMENT'],
                        'id_importance': ImportanceGeo.objects.using('postgresql').get(id=item['IDT_IMPORTANCE']),
                        'id_site': SiteSQL.objects.using('postgresql').get(id=item['IDT_SITE']),
                        'idt_type_affectation': item['IDT_TYPE_AFFECTATION'],
                    }
                )

            queryset = Batiment.objects.using('postgresql').all()
            serializer = BatimentSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 10. Niveau
class NiveauView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM NIVEAU")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                Niveau.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'code_niveau': item['CODE_NIVEAU'],
                        'intitule': item['INTITULE'],
                        'id_batiment': Batiment.objects.using('postgresql').get(id=item['IDT_BATIMENT']),
                        'id_importance': ImportanceGeo.objects.using('postgresql').get(id=item['IDT_IMPORTANCE']),
                    }
                )

            queryset = Niveau.objects.using('postgresql').all()
            serializer = NiveauSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 11. TypeEspace
class TypeEspaceView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM TYPE_ESPACE")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                TypeEspace.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'designation': item['DESIGNATION'],
                    }
                )

            queryset = TypeEspace.objects.using('postgresql').all()
            serializer = TypeEspaceSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 12. EspaceSQL
class EspaceSQLView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM ESPACE")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                EspaceSQL.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'actif': item['ACTIF'],
                        'code_espace': item['CODE_ESPACE'],
                        'intitule': item['INTITULE'],
                        'id_importance': ImportanceGeo.objects.using('postgresql').get(id=item['IDT_IMPORTANCE']),
                        'id_niveau': Niveau.objects.using('postgresql').get(id=item['IDT_NIVEAU']),
                        'id_type_espace': TypeEspace.objects.using('postgresql').get(id=item['IDT_TYPE_ESPACE']),
                        'geom': item['GEOM'],
                    }
                )

            queryset = EspaceSQL.objects.using('postgresql').all()
            serializer = EspaceSQLSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 13. SiteSQL
class SiteSQLView(APIView):
    def get(self, request):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT * FROM SITE")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for item in data:
                SiteSQL.objects.using('postgresql').update_or_create(
                    id=item['ID'],
                    defaults={
                        'adresse': item['ADRESSE'],
                        'code_agence': item['CODE_AGENCE'],
                        'code_site': item['CODE_SITE'],
                        'intitule': item['INTITULE'],
                        'nombre_occupant': item['NOMBRE_OCCUPANT'],
                        'peut_cloturer': item['PEUT_CLOTURER'],
                        'peut_valider': item['PEUT_VALIDER'],
                        'photo_path': item['PHOTO_PATH'],
                        'photo_source': item['PHOTO_SOURCE'],
                        'statut': item['STATUT'],
                        'superficie': item['SUPERFICIE'],
                        'id_type_site': TypeSite.objects.using('postgresql').get(id=item['IDT_TYPE_SITE']),
                        'id_ville': Ville.objects.using('postgresql').get(id=item['IDT_VILLE']),
                    }
                )

            queryset = SiteSQL.objects.using('postgresql').all()
            serializer = SiteSQLSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EquipementSQLView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM EQUIPEMENT")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class PrestataireView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM PRESTATAIRE")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class CriticiteEquipementView(APIView):  
     def get(self, request):  
        try:  
            # Fetch data from SQL Server CRICITICITE_EQUIPEMENT table  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT TOP (1000) [ID], [ACTIF], [DESIGNATION], [ORDRE] FROM [PRDGESTINIUM].[dbo].[CRICITICITE_EQUIPEMENT]")  
                columns = [col[0] for col in cursor.description]  
                equipement_data = [dict(zip(columns, row)) for row in cursor.fetchall()]  

            # Log fetched CRICITICITE_EQUIPEMENT data for debugging  
            print("Fetched Criticite Equipement Data: ", equipement_data)  

            # Store or update data in PostgreSQL for CRICITICITE_EQUIPEMENT  
            for item in equipement_data:  
                if 'ID' not in item or item['ID'] is None:  
                    print(f"Skipping item due to missing id: {item}")  
                    continue  # Skip if ID is missing  

                CriticiteEquipement.objects.using('postgresql').update_or_create(  
                    id=item['ID'],  # Use ID for primary key  
                    defaults={  
                        'actif': item['ACTIF'],  
                        'designation': item['DESIGNATION'],  
                        'ordre': item['ORDRE'],  
                    }  
                )  

            # Retrieve updated CRICITICITE_EQUIPEMENT data to return  
            queryset = CriticiteEquipement.objects.using('postgresql').all()  
            serializer = CriticiteEquipementSerializer(queryset, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)  

        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class NbrSiteView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM NBR_SITE")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class StatutNCView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM STATUT_NC")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  




# Dictionnaire pour lier chaque table avec son modèle et son sérialiseur (assurez-vous que c'est défini ici)  
TABLES_CONFIG = {  
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
    }  
}  
class HistoriqueNCView(APIView):  
    def get(self, request):  
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
class CriticiteNCView(APIView):  
    def get(self, request):  
        try:  
            # Connect to SQL Server and fetch data  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM  CRICITICITE_NC")  
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
                criticite_nc, created = CriticiteNC.objects.using('postgresql').update_or_create(  
                    id=item['ID'],  # Use ID for primary key  
                    defaults={  
                        'actif': item['ACTIF'],  
                        'designation': item['DESIGNATION'],  
                        'ordre': item['ORDRE']  
                    }  
                )  

            # Retrieve updated data to return  
            queryset = CriticiteNC.objects.using('postgresql').all()  
            serializer = CriticiteNCSerializer(queryset, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)  

        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
class NonConformiteView(APIView):  
    def get(self, request):  
        try:  
            # Récupérer les données depuis SQL Server  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM NON_COMFORMITE")  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  

            # Log fetched data for troubleshooting  
            print("Fetched Data: ", data)  

            # Function to remap keys to match Django model fields  
            def remap_non_conformite(item):  
                return {  
                    'id': item.get('ID'),  # Map 'ID' from SQL Server to 'id'  
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
                    'batiment_id': item.get('batiment_ID'),  # Remap foreign keys  
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

            # Stocker les données dans PostgreSQL  
            for item in data:  
                # Remap keys correctly to match model fields  
                item_mapped = remap_non_conformite(item)  
                
                if not item_mapped['id']:  # Validate if the id exists  
                    print(f"Skipping item due to missing id: {item_mapped}")  
                    continue  
                
                # Create or update the 'NonConformite' instance  
                Non_Conformite, created = TABLES_CONFIG['NON_COMFORMITE']['model'].objects.using('postgresql').update_or_create(  
                    id=item_mapped['id'],  # Use the primary key for identification  
                    defaults=item_mapped  # Use mapped fields  
                )  

            # Récupérer les données depuis PostgreSQL pour la réponse  
            queryset = TABLES_CONFIG['NON_COMFORMITE']['model'].objects.using('postgresql').all()  
            serializer = TABLES_CONFIG['NON_COMFORMITE']['serializer'](queryset,many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)  

        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
class RondeView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM RONDE")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class RondeCommentairesView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM RONDE_COMMENTAIRES")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class RondeEventView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM RONDE_EVENT")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class RondeParametreView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM RONDE_PARAMETRE")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class RondeReleveView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM RONDE_RELEVE")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class TypeRealisationView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM TYPE_REALISATION")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class UniteMesureView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM UNITE_MESURE")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class DonneeMesureView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM DONNEE_MESURE")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class InterventionView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM INTERVENTION")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class InterventionAttachementView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM INTERVENTION_ATTACHEMENT")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class InterventionIntervenantsView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM INTERVENTION_INTERVENANTS")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class InterventionPrestataireView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM INTERVENTION_PRESTATAIRE")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class PlanificationView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM PLANIFICATION")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class DetailPlanificationView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM DETAIL_PLANIFICATION")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class FrequenceView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM FREQUENCE")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class DetailPlanificationInterventionView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM DETAIL_PLANIFICATION_INTERVENTION")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class UserView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM users")  # This remains the same as it matches your initial table name  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class UserAffecView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM USER_AFFEC")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class MarcheView(APIView):  
    def get(self, request):  
        try:  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM MARCHE")  # Updated  
                columns = [col[0] for col in cursor.description]  
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
class ActionIntegrationView(APIView):  
    def get(self, request):  
        try:  
            # Fetch data from SQL Server ACTION table  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM [PRDGESTINIUM].[dbo].[ACTION]")  
                columns = [col[0] for col in cursor.description]  
                action_data = [dict(zip(columns, row)) for row in cursor.fetchall()]  

            # Log fetched ACTION data for debugging  
            print("Fetched Action Data: ", action_data)  

            # Store or update data in PostgreSQL for ACTION  
            for item in action_data:  
                if 'ID' not in item or item['ID'] is None:  
                    print(f"Skipping item due to missing id: {item}")  
                    continue  # Skip if ID is missing  

                Action.objects.using('postgresql').update_or_create(  
                    id=item['ID'],  # Use ID for primary key  
                    defaults={  
                        'budget_action': item['BUDGET_ACTION'],  
                        'commentaire': item['commentaire'],  
                        'content_type': item['contentType'],  
                        'date_debut': item['DATE_DEBUT'],  
                        'date_fin_p': item['DATE_FIN_P'],  
                        'date_fin': item['DATE_FIN'],  
                        'date_suspens': item['DATE_SUSPENS'],  
                        'date_validation': item['dateValidation'],  
                        'demande': item['demande'],  
                        'detail_action': item['DETAIL_ACTION'],  
                        'need_val': item['needVal'],  
                        'nom_fichier': item['NOM_FICHIER'],  
                        'num_save': item['numSave'],  
                        'numero_action': item['NUMERO_ACTION'],  
                        'pdr_conso': item['PDR_CONSO'],  
                        'responsable': item['responsable'],  
                        'taux_avancement': item['TAUX_AVANCEMENT'],  
                        'technicien': item['technicien'],  
                        'uid': item['uid'],  
                        'valid': item['valid'],  
                        'valider_par': item['validerPar'],  
                        'idt_nc_id': item['IDT_NC'],  
                        'pst_action_id': item['pstAction_ID'],  
                        'statut_action_id_id': item['statutAction_ID'],  
                    }  
                )  

            # Retrieve updated ACTION data to return  
            queryset = Action.objects.using('postgresql').all()  
            serializer = ActionSerializer(queryset, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)  

        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class StatutActionIntegrationView(APIView):  
    def get(self, request):  
        try:  
            # Fetch data from SQL Server STATUT_ACTION table  
            with connections['default'].cursor() as cursor:  
                cursor.execute("SELECT * FROM [PRDGESTINIUM].[dbo].[STATUT_ACTION]")  
                columns = [col[0] for col in cursor.description]  
                statut_action_data = [dict(zip(columns, row)) for row in cursor.fetchall()]  

            # Log fetched STATUT_ACTION data for debugging  
            print("Fetched Statut Action Data: ", statut_action_data)  

            # Store or update data in PostgreSQL for STATUT_ACTION  
            for item in statut_action_data:  
                if 'ID' not in item or item['ID'] is None:  
                    print(f"Skipping item due to missing id: {item}")  
                    continue  # Skip if ID is missing  

                StatutAction.objects.using('postgresql').update_or_create(  
                    id=item['ID'],  # Use ID for primary key  
                    defaults={  
                        'actif': item['ACTIF'],  
                        'designation': item['DESIGNATION'],  
                        'ordre': item['ORDRE'],  
                    }  
                )  

            # Retrieve updated STATUT_ACTION data to return  
            queryset = StatutAction.objects.using('postgresql').all()  
            serializer = StatutActionSerializer(queryset, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)  

        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  