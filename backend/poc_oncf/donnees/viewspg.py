from rest_framework import viewsets
from .models import CriticiteNC  
from .serializers import CriticiteNCSerializer 
from django_filters import rest_framework as filters
from rest_framework.views import APIView  
from rest_framework.response import Response  
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

# Vue pour Pays
class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer

# Vue pour Region
class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

# Vue pour Ville
class VilleViewSet(viewsets.ModelViewSet):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer

# Vue pour ImportanceGeo
class ImportanceGeoViewSet(viewsets.ModelViewSet):
    queryset = ImportanceGeo.objects.all()
    serializer_class = ImportanceGeoSerializer

# Vue pour TypeSite
class TypeSiteViewSet(viewsets.ModelViewSet):
    queryset = TypeSite.objects.all()
    serializer_class = TypeSiteSerializer

# Vue pour LotTechnique
class LotTechniqueViewSet(viewsets.ModelViewSet):
    queryset = LotTechnique.objects.all()
    serializer_class = LotTechniqueSerializer

# Vue pour FamilleEquipement
class FamilleEquipementViewSet(viewsets.ModelViewSet):
    queryset = FamilleEquipement.objects.all()
    serializer_class = FamilleEquipementSerializer

# Vue pour GroupeEquipement
class GroupeEquipementViewSet(viewsets.ModelViewSet):
    queryset = GroupeEquipement.objects.all()
    serializer_class = GroupeEquipementSerializer
# Vue pour récupérer les familles d'équipement par lot technique
class FamillesParLotView(APIView):
    def get(self, request, lot_id):
        familles = FamilleEquipement.objects.filter(id_lot=lot_id)
        serializer = FamilleEquipementSerializer(familles, many=True)
        return Response(serializer.data)

# Vue pour récupérer les groupes d'équipement par famille
class GroupesParFamilleView(APIView):
    def get(self, request, famille_id):
        groupes = GroupeEquipement.objects.filter(id_famille_equipement=famille_id)
        serializer = GroupeEquipementSerializer(groupes, many=True)
        return Response(serializer.data)
# Vue pour Batiment
class BatimentViewSet(viewsets.ModelViewSet):
    queryset = Batiment.objects.all()
    serializer_class = BatimentSerializer
class BatimentParSiteView(APIView):
    def get(self, request, site_id):
        batiments = Batiment.objects.filter(id_site=site_id)
        serializer = BatimentSerializer(batiments, many=True)
        return Response(serializer.data)

class NiveauParBatimentView(APIView):
    def get(self, request, batiment_id):
        niveaux = Niveau.objects.filter(id_batiment=batiment_id)
        serializer = NiveauSerializer(niveaux, many=True)
        return Response(serializer.data)

class EspaceParNiveauView(APIView):
    def get(self, request, niveau_id):
        espaces = EspaceSQL.objects.filter(id_niveau=niveau_id)
        serializer = EspaceSQLSerializer(espaces, many=True)
        return Response(serializer.data)
# Vue pour Niveau
class NiveauViewSet(viewsets.ModelViewSet):
    queryset = Niveau.objects.all()
    serializer_class = NiveauSerializer

# Vue pour TypeEspace
class TypeEspaceViewSet(viewsets.ModelViewSet):
    queryset = TypeEspace.objects.all()
    serializer_class = TypeEspaceSerializer

# Vue pour EspaceSQL
class EspaceSQLViewSet(viewsets.ModelViewSet):
    queryset = EspaceSQL.objects.all()
    serializer_class = EspaceSQLSerializer

# Vue pour SiteSQL
class SiteSQLViewSet(viewsets.ModelViewSet):
    queryset = SiteSQL.objects.all()
    serializer_class = SiteSQLSerializer

# Vue pour Prestataire
class PrestataireViewSet(viewsets.ModelViewSet):
    queryset = Prestataire.objects.all()
    serializer_class = PrestataireSerializer

# Vue pour CriticiteEquipement
class CriticiteEquipementViewSet(viewsets.ModelViewSet):
    queryset = CriticiteEquipement.objects.all()
    serializer_class = CriticiteEquipementSerializer

# Vue pour NbrSite
class NbrSiteViewSet(viewsets.ModelViewSet):
    queryset = NbrSite.objects.all()
    serializer_class = NbrSiteSerializer
class EquipementParEspaceView(APIView):
    def get(self, request, espace_id):
        equipements = EquipementSQL.objects.filter(id_espace=espace_id)
        serializer = EquipementSQLSerializer(equipements, many=True)
        return Response(serializer.data)
# Vue pour EquipementSQL
class EquipementSQLFilter(filters.FilterSet):  
    id_famille_equipement = filters.BaseInFilter(field_name='id_famille_equipement__id')  # Adapte pour plusieurs valeurs  
    id_groupe_equipement = filters.BaseInFilter(field_name='id_groupe_equipement__id')  # Idem  
    id_espace = filters.BaseInFilter(field_name='id_espace__id')  # Idem  
    id_criticite = filters.BaseInFilter(field_name='id_criticite_equipement__id')  # Idem  
    id_site = filters.BaseInFilter(field_name='id_espace__id_niveau__id_batiment__id_site__id')  # Filtre par Site  
    id_niveau = filters.BaseInFilter(field_name='id_espace__id_niveau__id')  # Filtre par Niveau  
    id_lot_technique = filters.BaseInFilter(field_name='id_famille_equipement__id_lot__id')  # Nouveau filtre par LotTechnique  
    id_equipement = filters.BaseInFilter(field_name='id')  # Ajoutez ceci

    class Meta:  
        model = EquipementSQL  
        fields = [  
            'id_famille_equipement',  
            'id_groupe_equipement',  
            'id_espace',  
            'id_criticite',  
            'id_site',  
            'id_niveau',  
            'id_lot_technique'  ,
            'id_equipement'
        ]  
        
class EquipementSQLViewSet(viewsets.ModelViewSet):  
    # Optimiser avec select_related et prefetch_related  
    queryset = EquipementSQL.objects.filter(geom__isnull=False).select_related(  
        'id_famille_equipement',  
        'id_groupe_equipement',  
        'id_espace',  
        'id_criticite_equipement'  
    ).prefetch_related(  
        'prestataire_id',  
        'id_nbr_site'  
    )  
    serializer_class = EquipementSQLSerializer  
    filter_backends = (filters.DjangoFilterBackend,)  
    filterset_class = EquipementSQLFilter  
class EquipementParSiteNiveauView(APIView):
    def get(self, request, site_id):
        equipements = EquipementSQL.objects.filter(
            id_espace__id_niveau__id_batiment__id_site=site_id,
                        geom__isnull=False  # <-- Filtre pour géométrie non nulle

        )
        serializer = EquipementSQLSerializer(equipements, many=True)
        return Response(serializer.data)
# Vue pour StatutNC
class StatutNCViewSet(viewsets.ModelViewSet):
    queryset = StatutNC.objects.all()
    serializer_class = StatutNCSerializer

# Vue pour HistoriqueNC
class HistoriqueNCViewSet(viewsets.ModelViewSet):
    queryset = HistoriqueNC.objects.all()
    serializer_class = HistoriqueNCSerializer

from django_filters import rest_framework as filters
from rest_framework import viewsets
from .models import NonConformite
from .serializers import NonConformiteSerializer

# Filtre personnalisé pour les non-conformités
class NonConformiteFilter(filters.FilterSet):  
    criticite_nc = filters.NumberFilter(field_name="criticite_non_conformite__id")  
    statut_nc = filters.NumberFilter(field_name="statut_nc__id")  
    batiment_id = filters.NumberFilter(field_name="batiment__id")  
    equipement_id = filters.NumberFilter(field_name="equipement__id")  
    espace_id = filters.NumberFilter(field_name="espace__id")  
    famille_equipement_id = filters.NumberFilter(field_name="famille_equipement__id")  
    importance_geographique_id = filters.NumberFilter(field_name="importance_geographique__id")  
    lot_technique_id = filters.NumberFilter(field_name="lot_technique__id")  
    marche_id = filters.NumberFilter(field_name="marche__id")  
    niveau_id = filters.NumberFilter(field_name="niveau__id")  
    prestataire_id = filters.NumberFilter(field_name="prestataire__id")  
    site_id = filters.NumberFilter(field_name="site__id")
    
    # Filtres de date améliorés
    date_debut = filters.DateFilter(
        field_name="date", 
        lookup_expr='gte',
        help_text="Format: YYYY-MM-DD. Filtre les NC après cette date."
    )
    date_fin = filters.DateFilter(
        field_name="date", 
        lookup_expr='lte',
        help_text="Format: YYYY-MM-DD. Filtre les NC avant cette date."
    )
    date = filters.DateFilter(
        field_name="date", 
        lookup_expr='exact',
        help_text="Format: YYYY-MM-DD. Filtre les NC à cette date exacte."
    )

    class Meta:  
        model = NonConformite  
        fields = [  
            'criticite_nc',  
            'statut_nc',  
            'batiment_id',  
            'equipement_id',  
            'espace_id',  
            'famille_equipement_id',  
            'importance_geographique_id',  
            'lot_technique_id',  
            'marche_id',  
            'niveau_id',  
            'prestataire_id',  
            'site_id',
            'date',
            'date_debut',
            'date_fin'
        ]

class NonConformiteViewSet(viewsets.ModelViewSet):
    queryset = NonConformite.objects.all().order_by('-date')
    serializer_class = NonConformiteSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = NonConformiteFilter
# Vue pour Ronde
class RondeViewSet(viewsets.ModelViewSet):
    queryset = Ronde.objects.all()
    serializer_class = RondeSerializer

# Vue pour RondeCommentaires
class RondeCommentairesViewSet(viewsets.ModelViewSet):
    queryset = RondeCommentaires.objects.all()
    serializer_class = RondeCommentairesSerializer

# Vue pour RondeEvent
class RondeEventViewSet(viewsets.ModelViewSet):
    queryset = RondeEvent.objects.all()
    serializer_class = RondeEventSerializer

# Vue pour RondeParametre
class RondeParametreViewSet(viewsets.ModelViewSet):
    queryset = RondeParametre.objects.all()
    serializer_class = RondeParametreSerializer

# Vue pour RondeReleve
class RondeReleveViewSet(viewsets.ModelViewSet):
    queryset = RondeReleve.objects.all()
    serializer_class = RondeReleveSerializer

# Vue pour TypeRealisation
class TypeRealisationViewSet(viewsets.ModelViewSet):
    queryset = TypeRealisation.objects.all()
    serializer_class = TypeRealisationSerializer

# Vue pour UniteMesure
class UniteMesureViewSet(viewsets.ModelViewSet):
    queryset = UniteMesure.objects.all()
    serializer_class = UniteMesureSerializer

# Vue pour DonneeMesure
class DonneeMesureViewSet(viewsets.ModelViewSet):
    queryset = DonneeMesure.objects.all()
    serializer_class = DonneeMesureSerializer


# Vue pour InterventionAttachement
class InterventionAttachementViewSet(viewsets.ModelViewSet):
    queryset = InterventionAttachement.objects.all()
    serializer_class = InterventionAttachementSerializer

# Vue pour InterventionIntervenants
class InterventionIntervenantsViewSet(viewsets.ModelViewSet):
    queryset = InterventionIntervenants.objects.all()
    serializer_class = InterventionIntervenantsSerializer

# Vue pour InterventionPrestataire
class InterventionPrestataireViewSet(viewsets.ModelViewSet):
    queryset = InterventionPrestataire.objects.all()
    serializer_class = InterventionPrestataireSerializer

# Vue pour Planification
class PlanificationViewSet(viewsets.ModelViewSet):
    queryset = Planification.objects.all()
    serializer_class = PlanificationSerializer

# Vue pour DetailPlanification
class DetailPlanificationViewSet(viewsets.ModelViewSet):
    queryset = DetailPlanification.objects.all()
    serializer_class = DetailPlanificationSerializer

# Vue pour Frequence
class FrequenceViewSet(viewsets.ModelViewSet):
    queryset = Frequence.objects.all()
    serializer_class = FrequenceSerializer

# Vue pour DetailPlanificationIntervention
class DetailPlanificationInterventionViewSet(viewsets.ModelViewSet):
    queryset = DetailPlanificationIntervention.objects.all()
    serializer_class = DetailPlanificationInterventionSerializer

# Vue pour User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Vue pour UserAffec
class UserAffecViewSet(viewsets.ModelViewSet):
    queryset = UserAffec.objects.all()
    serializer_class = UserAffecSerializer

# Vue pour Marche
class MarcheViewSet(viewsets.ModelViewSet):
    queryset = Marche.objects.all()
    serializer_class = MarcheSerializer
class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer 
class StatutActionViewSet(viewsets.ModelViewSet):
    queryset = StatutAction.objects.all()
    serializer_class = StatutActionSerializer
# Dans views.py

from rest_framework.decorators import action
from django.db.models import Q

class MultiFilterViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'])
    def multi_filter(self, request):
        # Récupérer les paramètres de requête
        params = request.query_params
        
        # Construire le filtre Q
        q_filters = Q()
        
        # Site
        if 'sites' in params:
            site_ids = [int(id) for id in params['sites'].split(',')]
            q_filters &= Q(site__id__in=site_ids)
            
        # Bâtiment
        if 'batiments' in params:
            batiment_ids = [int(id) for id in params['batiments'].split(',')]
            q_filters &= Q(batiment__id__in=batiment_ids)
            
        # Niveau
        if 'niveaux' in params:
            niveau_ids = [int(id) for id in params['niveaux'].split(',')]
            q_filters &= Q(niveau__id__in=niveau_ids)
            
        # Espace
        if 'espaces' in params:
            espace_ids = [int(id) for id in params['espaces'].split(',')]
            q_filters &= Q(espace__id__in=espace_ids)
            
        # Lot technique
        if 'lots_techniques' in params:
            lot_ids = [int(id) for id in params['lots_techniques'].split(',')]
            q_filters &= Q(lot_technique__id__in=lot_ids)
            
        # Criticité
        if 'criticites' in params:
            criticite_ids = [int(id) for id in params['criticites'].split(',')]
            q_filters &= Q(criticite_non_conformite__id__in=criticite_ids)
            
        # Statut
        if 'statuts' in params:
            statut_ids = [int(id) for id in params['statuts'].split(',')]
            q_filters &= Q(statut_nc__id__in=statut_ids)
            
        # Appliquer le filtre
        queryset = self.get_queryset().filter(q_filters)
        
        # Pagination si nécessaire
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Mettre à jour NonConformiteViewSet pour hériter de MultiFilterViewSet
class NonConformiteViewSet(MultiFilterViewSet):
    queryset = NonConformite.objects.all()
    serializer_class = NonConformiteSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = NonConformiteFilter
# Nouvelles vues pour les sélections multiples
class BatimentParMultiSitesView(APIView):
    def get(self, request):
        site_ids = request.query_params.get('sites', '').split(',')
        if site_ids and site_ids[0]:
            batiments = Batiment.objects.filter(id_site__in=site_ids)
            serializer = BatimentSerializer(batiments, many=True)
            return Response(serializer.data)
        return Response([])

class NiveauParMultiBatimentsView(APIView):
    def get(self, request):
        batiment_ids = request.query_params.get('batiments', '').split(',')
        if batiment_ids and batiment_ids[0]:
            niveaux = Niveau.objects.filter(id_batiment__in=batiment_ids)
            serializer = NiveauSerializer(niveaux, many=True)
            return Response(serializer.data)
        return Response([])

class EspaceParMultiNiveauxView(APIView):
    def get(self, request):
        niveau_ids = request.query_params.get('niveaux', '').split(',')
        if niveau_ids and niveau_ids[0]:
            espaces = EspaceSQL.objects.filter(id_niveau__in=niveau_ids)
            serializer = EspaceSQLSerializer(espaces, many=True)
            return Response(serializer.data)
        return Response([])
class FamillesParMultiLotView(APIView):  
    def get(self, request):  
        lot_ids = request.query_params.get('lots', '').split(',')  
        if lot_ids and lot_ids[0]:  
            familles = FamilleEquipement.objects.filter(id_lot__in=lot_ids)  # Filtrer par plusieurs lots  
            serializer = FamilleEquipementSerializer(familles, many=True)  
            return Response(serializer.data)  
        return Response([])  
class GroupesParMultiFamilleView(APIView):  
    def get(self, request):  
        famille_ids = request.query_params.get('familles', '').split(',')  
        if famille_ids and famille_ids[0]:  
            # Utiliser filter avec un OR sur les familles pour récupérer tous les groupes d'équipement correspondants  
            groupes = GroupeEquipement.objects.filter(id_famille_equipement__in=famille_ids)  
            serializer = GroupeEquipementSerializer(groupes, many=True)  
            return Response(serializer.data)  
        return Response([])  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import json
from django.views.decorators.http import require_POST
import logging  
logger = logging.getLogger(__name__)  
@csrf_exempt  
def ldap_login(request):  
    if request.method == 'POST':  
        try:  
            # Charger les données envoyées dans la requête  
            data = json.loads(request.body)  
            username = data.get('username')  
            password = data.get('password')  
            
            # Vérifiez que le nom d'utilisateur et le mot de passe sont fournis  
            if not username or not password:  
                return JsonResponse(  
                    {'status': 'error', 'message': 'Username et password sont requis'},  
                    status=400  
                )  
            
            # Vérifiez si l'utilisateur existe d'abord dans UserProfile  
            try:  
                profile = UserProfile.objects.get(ldap_cn=username)  
                if not profile.is_active:  # Refuse l'accès si le compte est désactivé  
                    return JsonResponse({  
                        'status': 'error',  
                        'message': 'Compte désactivé'  
                    }, status=403)  
            except UserProfile.DoesNotExist:  
                # Si aucun profil n'est trouvé, retourner une erreur  
                return JsonResponse({  
                    'status': 'error',  
                    'message': 'Profil utilisateur introuvable. Contactez un administrateur.'  
                }, status=403)  

            # Authentification via le backend LDAP  
            user = authenticate(request, username=username, password=password)  
            if user is not None:  
                # Si l'utilisateur est authentifié avec succès via LDAP, connectez-le  
                login(request, user)  
                return JsonResponse({  
                    'status': 'success',  
                    'message': 'Authentification réussie',  
                    'user': {  
                        'username': user.username,  
                        'first_name': user.first_name,  
                        'last_name': user.last_name,  
                        'email': user.email,  
                        'role': profile.role  # Ajout du rôle du profil  
                    }  
                })  
            else:  
                # Échec d'authentification via LDAP  
                return JsonResponse({  
                    'status': 'error',  
                    'message': 'Identifiants incorrects ou problème d\'authentification LDAP'  
                }, status=401)  
        
        except Exception as e:  
            # Gestion globale des erreurs  
            return JsonResponse({  
                'status': 'error',  
                'message': f'Erreur serveur: {str(e)}'  
            }, status=500)  
    
    # Si ce n'est pas une méthode POST, retourner une erreur  
    return JsonResponse({  
        'status': 'error',  
        'message': 'Méthode non autorisée'  
    }, status=405)  
@csrf_exempt
@require_POST
def logout_view(request):
    logout(request)
    response = JsonResponse({'status': 'success'})
    response.delete_cookie('sessionid')  # Si vous utilisez des sessions
    return response
from rest_framework import viewsets, status  
from rest_framework.response import Response  
from rest_framework.decorators import action  
import ldap  
from django.conf import settings   
from .models import UserProfile  
from .serializers import UserProfileSerializer  
import logging  

logger = logging.getLogger(__name__)  

class UserProfileViewSet(viewsets.ModelViewSet):  
    queryset = UserProfile.objects.all()  
    serializer_class = UserProfileSerializer  

    @action(detail=False, methods=['get'])  
    def ldap_users(self, request):  
        """Liste des utilisateurs LDAP non encore activés"""  
        try:  
            existing_users = set(UserProfile.objects.values_list('ldap_cn', flat=True))  
            conn = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)  
            conn.simple_bind_s(settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD)  

            users = []  
            results = conn.search_s(  
                'ou=users,ou=system',  
                ldap.SCOPE_SUBTREE,  
                '(objectClass=inetOrgPerson)',  
                ['cn', 'sn', 'uid']  
            )  

            for dn, entry in results:  
                try:  
                    cn = entry['cn'][0].decode('utf-8')  
                    if cn not in existing_users:  
                        users.append({  
                            'cn': cn,  
                            'sn': entry.get('sn', [b''])[0].decode('utf-8'),  
                            'dn': dn  
                        })  
                except (KeyError, IndexError, UnicodeDecodeError) as e:  
                    logger.warning(f"Error processing LDAP entry {dn}: {str(e)}")  

            return Response(users)  

        except ldap.LDAPError as e:  
            logger.error(f"LDAP Error: {str(e)}")  
            return Response(  
                {'error': 'LDAP connection failed', 'details': str(e)},  
                status=status.HTTP_503_SERVICE_UNAVAILABLE  
            )  
        finally:  
            try:  
                conn.unbind()  
            except:  
                pass  

    @action(detail=True, methods=['patch'])
    def update_user(self, request, pk=None):
        """Mise à jour d'un utilisateur (désactivation ou changement de rôle)"""
        try:
            user_profile = self.get_object()
            data = request.data

            # Update available fields
            if 'is_active' in data:
                user_profile.is_active = data['is_active']
            
            if 'role' in data:
                old_role = user_profile.role
                new_role = data['role']
                user_profile.role = new_role
                
                # Handle role changes
                if new_role in ['admin_technique', 'admin_fonctionnel']:
                    user_profile.all_sites = True
                    user_profile.sites.clear()  # Clear specific site assignments
                else:
                    # If changing from admin to non-admin role
                    if old_role in ['admin_technique', 'admin_fonctionnel']:
                        user_profile.all_sites = False
                        # Don't clear sites here - let frontend prompt for site selection
        
            # Only update sites if not an admin role and all_sites is False
            if not user_profile.all_sites and 'sites' in data:
                user_profile.sites.set(data['sites'])

            user_profile.save()

            return Response({
                "status": "success",
                "message": "Utilisateur mis à jour avec succès"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Une erreur est survenue : {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework import viewsets, filters  
from django_filters.rest_framework import DjangoFilterBackend  
from rest_framework.decorators import action  
from rest_framework.response import Response  
from django.db.models import Q  
from datetime import datetime  
from django.utils import timezone  
from datetime import timedelta  
import logging  

logger = logging.getLogger(__name__)  

class InterventionViewSet(viewsets.ModelViewSet):  
    queryset = Intervention.objects.all()  
    serializer_class = InterventionSerializer  
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  

    def get_queryset(self):  
        queryset = super().get_queryset()  
        params = self.request.query_params  

        # Récupération des paramètres  
        site_ids = params.getlist('site_id', [])
        batiment_ids = params.getlist('batiment_id', [])
        niveau_ids = params.getlist('niveau_id', [])
        frequence_ids = params.getlist('frequence_id', [])
        jours_restants = params.get('jours_restants')

        # Filtre par localisation  
        if site_ids:  
            queryset = queryset.filter(  
                Q(detail_planification__planification__site_id__in=site_ids)  
            ).distinct()  

        if batiment_ids:  
            queryset = queryset.filter(  
                Q(detail_planification__equipement__id_espace__id_niveau__id_batiment__in=batiment_ids) |  
                Q(detail_planification__famille_equipement__equipementsql__id_espace__id_niveau__id_batiment__in=batiment_ids)  
            ).distinct()  

        if niveau_ids:  
            queryset = queryset.filter(  
                Q(detail_planification__equipement__id_espace__id_niveau__in=niveau_ids) |  
                Q(detail_planification__famille_equipement__equipementsql__id_espace__id_niveau__in=niveau_ids)  
            ).distinct()  

        # Filtre par fréquence  
        if frequence_ids:  
            queryset = queryset.filter(detail_planification__frequence__id__in=frequence_ids)  

        # Filtre par jours restants  
        if jours_restants:  
            try:  
                jours = int(jours_restants)  
                today = timezone.now().date()  
                threshold_date = today + timedelta(days=jours)  # Date limite dans le futur  
                
                # Récupérer les interventions dont date_fin_prev est entre aujourd'hui et la date limite  
                queryset = queryset.filter(date_fin_prev__date__gte=today, date_fin_prev__date__lte=threshold_date)  
            except ValueError:  
                logger.warning("Jours restants invalide pour le filtre.")    

        # Filtre par date_depart_prevesionnel  
        date_depart_de = self.request.query_params.get('date_depart_de')  
        date_depart_jusqua = self.request.query_params.get('date_depart_jusqua')  

        if date_depart_de:  
            try:  
                date_de = datetime.strptime(date_depart_de, '%Y-%m-%d').date()  
                queryset = queryset.filter(date_depart_previsionnel__date__gte=date_de)  
            except ValueError:  
                logger.warning("Date de départ invalide pour le filtre.")  

        if date_depart_jusqua:  
            try:  
                date_jusqua = datetime.strptime(date_depart_jusqua, '%Y-%m-%d').date()  
                queryset = queryset.filter(date_depart_previsionnel__date__lte=date_jusqua)  
            except ValueError:  
                logger.warning("Date jusqu'à invalide pour le filtre.")  

        # Optimisation des requêtes  
        queryset = queryset.select_related(  
            'detail_planification',  
            'detail_planification__equipement',  
            'detail_planification__famille_equipement',  
            'detail_planification__frequence',  
            'detail_planification__planification'  
        ).prefetch_related(  
            'interventionintervenants_set',  
            'interventionprestataire_set'  
        )  

        return queryset  

    @action(detail=False, methods=['get'])  
    def geojson(self, request):  
        queryset = self.filter_queryset(self.get_queryset())  
        features = []  
        
        for intervention in queryset:  
            detail = intervention.detail_planification  
            if not detail:  
                continue  
                
            properties = InterventionSerializer(intervention).data  
            
            # Cas 1: Intervention liée à un équipement spécifique  
            if detail.equipement and detail.equipement.geom:  
                self._add_equipment_feature(features, detail.equipement, properties)  
            
            # Cas 2: Intervention liée à une famille d'équipements (si pas d'équipement spécifique)  
            elif detail.famille_equipement:  
                self._add_family_equipment_features(request, features, detail, properties)  
        
        return Response({  
            "type": "FeatureCollection",  
            "features": features  
        })  

    def _add_equipment_feature(self, features, equipment, properties):  
        """Ajoute une feature pour un équipement spécifique"""  
        try:  
            if hasattr(equipment.geom, 'x') and hasattr(equipment.geom, 'y'):  
                longitude, latitude = equipment.geom.x, equipment.geom.y  
            else:  
                coords = equipment.geom.split(';')[1].replace('POINT (', '').replace(')', '').split()  
                longitude, latitude = map(float, coords)  
            
            feature = {  
                "type": "Feature",  
                "geometry": {  
                    "type": "Point",  
                    "coordinates": [longitude, latitude]  
                },  
                "properties": {  
                    **properties,  
                    "source": "equipement",  
                    "equipement": {  
                        "id": equipment.id,  
                        "code_equipement": equipment.code_equipement,  
                        "famille": equipment.id_famille_equipement.designation if equipment.id_famille_equipement else None  
                    }  
                }  
            }  
            features.append(feature)  
        except Exception as e:  
            logger.warning(f"Failed to process equipment {equipment.id}: {str(e)}")  

    def _add_family_equipment_features(self, request, features, detail, properties):
        """Ajoute des features pour tous les équipements d'une famille"""
        equipements = EquipementSQL.objects.filter(
            id_famille_equipement=detail.famille_equipement,
            geom__isnull=False
        )
        
        # Récupérer tous les paramètres avec getlist()
        site_ids = request.query_params.getlist('site_id', [])
        batiment_ids = request.query_params.getlist('batiment_id', [])
        niveau_ids = request.query_params.getlist('niveau_id', [])
        
        # Appliquer les filtres seulement si des valeurs sont fournies
        if site_ids:
            equipements = equipements.filter(id_espace__id_niveau__id_batiment__id_site__in=site_ids)
        
        if batiment_ids:
            equipements = equipements.filter(id_espace__id_niveau__id_batiment__in=batiment_ids)
        
        if niveau_ids:
            equipements = equipements.filter(id_espace__id_niveau__in=niveau_ids)
        
        for equipement in equipements:
            try:
                if hasattr(equipement.geom, 'x') and hasattr(equipement.geom, 'y'):
                    longitude, latitude = equipement.geom.x, equipement.geom.y
                else:
                    coords = equipement.geom.split(';')[1].replace('POINT (', '').replace(')', '').split()
                    longitude, latitude = map(float, coords)
                
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [longitude, latitude]
                    },
                    "properties": {
                        **properties,
                        "source": "famille_equipement",
                        "equipement": {
                            "id": equipement.id,
                            "code_equipement": equipement.code_equipement,
                            "famille": equipement.id_famille_equipement.designation if equipement.id_famille_equipement else None
                        }
                    }
                }
                features.append(feature)
            except Exception as e:
                logger.warning(f"Failed to process family equipment {equipement.id}: {str(e)}")
from rest_framework.decorators import api_view

@api_view(['PATCH'])
def update_equipement_geom(request):
    updates = request.data.get('updates', [])
    
    try:
        for update in updates:
            equipement = EquipementSQL.objects.get(id=update['id'])
            equipement.geom = update['geom']
            equipement.save()
            
        return Response({'success': True, 'message': 'Geometries updated successfully'})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=400)