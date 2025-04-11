from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewspg import (update_equipement_geom,
    PaysViewSet, RegionViewSet, VilleViewSet, ImportanceGeoViewSet, TypeSiteViewSet,
    LotTechniqueViewSet, FamilleEquipementViewSet, GroupeEquipementViewSet, BatimentViewSet,
    NiveauViewSet, TypeEspaceViewSet, EspaceSQLViewSet, SiteSQLViewSet, PrestataireViewSet,
    CriticiteEquipementViewSet, NbrSiteViewSet, EquipementSQLViewSet, StatutNCViewSet,
    HistoriqueNCViewSet, NonConformiteViewSet, RondeViewSet, RondeCommentairesViewSet,
    RondeEventViewSet, RondeParametreViewSet, RondeReleveViewSet, TypeRealisationViewSet,
    UniteMesureViewSet, DonneeMesureViewSet, InterventionViewSet, InterventionAttachementViewSet,FamillesParMultiLotView,GroupesParMultiFamilleView,
    InterventionIntervenantsViewSet, InterventionPrestataireViewSet, PlanificationViewSet,EquipementParSiteNiveauView,
    DetailPlanificationViewSet, FrequenceViewSet, DetailPlanificationInterventionViewSet,EquipementParEspaceView,FamillesParLotView, GroupesParFamilleView,
    UserViewSet, UserAffecViewSet, MarcheViewSet,ActionViewSet,StatutActionViewSet,BatimentParSiteView, NiveauParBatimentView, EspaceParNiveauView,
MultiFilterViewSet,BatimentParMultiSitesView,NiveauParMultiBatimentsView,EspaceParMultiNiveauxView,ldap_login,logout_view,UserProfileViewSet
)

router = DefaultRouter()

# Enregistrement des vues
router.register(r'pays', PaysViewSet)
router.register(r'region', RegionViewSet)
router.register(r'ville', VilleViewSet)
router.register(r'importance-geo', ImportanceGeoViewSet)
router.register(r'type-site', TypeSiteViewSet)
router.register(r'lot-technique', LotTechniqueViewSet)
router.register(r'famille-equipement', FamilleEquipementViewSet)
router.register(r'groupe-equipement', GroupeEquipementViewSet)
router.register(r'batiment', BatimentViewSet)
router.register(r'niveau', NiveauViewSet)
router.register(r'type-espace', TypeEspaceViewSet)
router.register(r'espace-sql', EspaceSQLViewSet)
router.register(r'site-sql', SiteSQLViewSet)
router.register(r'prestataire', PrestataireViewSet)
router.register(r'criticite-equipement', CriticiteEquipementViewSet)
router.register(r'nbr-site', NbrSiteViewSet)
router.register(r'equipement-sql', EquipementSQLViewSet)
router.register(r'statut-nc', StatutNCViewSet)
router.register(r'historique-nc', HistoriqueNCViewSet)
router.register(r'non-conformite', NonConformiteViewSet)
router.register(r'ronde', RondeViewSet)
router.register(r'ronde-commentaires', RondeCommentairesViewSet)
router.register(r'ronde-event', RondeEventViewSet)
router.register(r'ronde-parametre', RondeParametreViewSet)
router.register(r'ronde-releve', RondeReleveViewSet)
router.register(r'type-realisation', TypeRealisationViewSet)
router.register(r'unite-mesure', UniteMesureViewSet)
router.register(r'donnee-mesure', DonneeMesureViewSet)
router.register(r'intervention', InterventionViewSet)
router.register(r'intervention-attachement', InterventionAttachementViewSet)
router.register(r'intervention-intervenants', InterventionIntervenantsViewSet)
router.register(r'intervention-prestataire', InterventionPrestataireViewSet)
router.register(r'planification', PlanificationViewSet)
router.register(r'detail-planification', DetailPlanificationViewSet)
router.register(r'frequence', FrequenceViewSet)
router.register(r'detail-planification-intervention', DetailPlanificationInterventionViewSet)
router.register(r'user', UserViewSet)
router.register(r'user-affec', UserAffecViewSet)
router.register(r'marche', MarcheViewSet)
router.register(r'action', ActionViewSet)
router.register(r'statut-action', StatutActionViewSet)
router.register(r'user-profiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
    path('batiments-par-site/<int:site_id>/', BatimentParSiteView.as_view(), name='batiments-par-site'),
    path('niveaux-par-batiment/<int:batiment_id>/', NiveauParBatimentView.as_view(), name='niveaux-par-batiment'),
    path('espaces-par-niveau/<int:niveau_id>/', EspaceParNiveauView.as_view(), name='espaces-par-niveau'),
    path('equipements-par-espace/<int:espace_id>/', EquipementParEspaceView.as_view(), name='equipements-par-espace'),
    path('familles-par-lot/<int:lot_id>/', FamillesParLotView.as_view(), name='familles-par-lot'),
    path('groupes-par-famille/<int:famille_id>/', GroupesParFamilleView.as_view(), name='groupes-par-famille'),
    path('equipements-par-site-niveau/<int:site_id>/', EquipementParSiteNiveauView.as_view(), name='equipements-par-site-niveau'),
    path('batiments-par-multi-sites/', BatimentParMultiSitesView.as_view(), name='batiments-par-multi-sites'),
    path('niveaux-par-multi-batiments/', NiveauParMultiBatimentsView.as_view(), name='niveaux-par-multi-batiments'),
    path('espaces-par-multi-niveaux/', EspaceParMultiNiveauxView.as_view(), name='espaces-par-multi-niveaux'),
    path('familles-par-multi-lots/', FamillesParMultiLotView.as_view(), name='familles-par-multi-lots'),
    path('groupes-par-multi-familles/', GroupesParMultiFamilleView.as_view(), name='groupes-par-multi-familles'),
    path('non-conformite/multi-filter/', NonConformiteViewSet.as_view({'get': 'multi_filter'}), name='non-conformite-multi-filter'),
    path('login/', ldap_login, name='ldap_login'),
    path('logout/', logout_view, name='logout'),
    path('update-equipement-geom/', update_equipement_geom, name='update_equipement_geom'),

]