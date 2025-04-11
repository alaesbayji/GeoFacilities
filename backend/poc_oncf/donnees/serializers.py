from rest_framework import serializers  

# Importation des modèles  
from .models import (  
    Action,
    StatutAction,
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
    CriticiteNC,
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
    Marche  ,
CriticiteNC 
)  

# Sérialiseur pour Pays  
class PaysSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Pays  
        fields = '__all__'  

# Sérialiseur pour Region  
class RegionSerializer(serializers.ModelSerializer):  
    id_pays = serializers.PrimaryKeyRelatedField(queryset=Pays.objects.all())  

    class Meta:  
        model = Region  
        fields = '__all__'  

# Sérialiseur pour Ville  
class VilleSerializer(serializers.ModelSerializer):  
    id_region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())  

    class Meta:  
        model = Ville  
        fields = '__all__'  

# Sérialiseur pour ImportanceGeo  
class ImportanceGeoSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = ImportanceGeo  
        fields = '__all__'  

# Sérialiseur pour TypeSite  
class TypeSiteSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = TypeSite  
        fields = '__all__'  

# Sérialiseur pour LotTechnique  
class LotTechniqueSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = LotTechnique  
        fields = '__all__'  

# Sérialiseur pour FamilleEquipement  
class FamilleEquipementSerializer(serializers.ModelSerializer):  
    id_lot =  LotTechniqueSerializer(read_only=True)  

    class Meta:  
        model = FamilleEquipement  
        fields = '__all__'  

# Sérialiseur pour GroupeEquipement  
class GroupeEquipementSerializer(serializers.ModelSerializer):  
    id_famille_equipement = serializers.PrimaryKeyRelatedField(queryset=FamilleEquipement.objects.all())  

    class Meta:  
        model = GroupeEquipement  
        fields = '__all__'  

# Sérialiseur pour Prestataire  
class PrestataireSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Prestataire  
        fields = '__all__'  

# Sérialiseur pour NbrSite  
class NbrSiteSerializer(serializers.ModelSerializer):  
    id_famille = serializers.PrimaryKeyRelatedField(queryset=FamilleEquipement.objects.all())  
    id_niveau = serializers.PrimaryKeyRelatedField(queryset=Niveau.objects.all())  
    id_site = serializers.PrimaryKeyRelatedField(queryset=SiteSQL.objects.all())  

    class Meta:  
        model = NbrSite  
        fields = '__all__'  

# Sérialiseur pour Batiment  




# Sérialiseur pour TypeEspace  
class TypeEspaceSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = TypeEspace  
        fields = '__all__'  



# Sérialiseur pour SiteSQL  
class SiteSQLSerializer(serializers.ModelSerializer):  
    id_type_site = serializers.PrimaryKeyRelatedField(queryset=TypeSite.objects.all())  
    id_ville = serializers.PrimaryKeyRelatedField(queryset=Ville.objects.all())  

    class Meta:  
        model = SiteSQL  
        fields = '__all__'  
class BatimentSerializer(serializers.ModelSerializer):  
    id_importance = serializers.PrimaryKeyRelatedField(queryset=ImportanceGeo.objects.all())  
    id_site = SiteSQLSerializer(read_only=True)  

    class Meta:  
        model = Batiment  
        fields = '__all__'  
# Sérialiseur pour Niveau  
class NiveauSerializer(serializers.ModelSerializer):  
    id_batiment = BatimentSerializer(read_only=True)  
    id_importance = serializers.PrimaryKeyRelatedField(queryset=ImportanceGeo.objects.all())  

    class Meta:  
        model = Niveau  
        fields = '__all__'  
# Sérialiseur pour EspaceSQL  
class EspaceSQLSerializer(serializers.ModelSerializer):  
    id_importance = serializers.PrimaryKeyRelatedField(queryset=ImportanceGeo.objects.all())  
    id_niveau = NiveauSerializer(read_only=True) 
    id_type_espace = serializers.PrimaryKeyRelatedField(queryset=TypeEspace.objects.all())  

    class Meta:  
        model = EspaceSQL  
        fields = '__all__'  
# Sérialiseur pour CriticiteEquipement  
class CriticiteEquipementSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = CriticiteEquipement  
        fields = '__all__'  
class CriticiteNCSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = CriticiteNC  
        fields = '__all__'  
# Sérialiseur pour EquipementSQL  
class EquipementSQLSerializer(serializers.ModelSerializer):  
    id_criticite_equipement = CriticiteEquipementSerializer(read_only=True)  
    id_espace = EspaceSQLSerializer(read_only=True)
    id_famille_equipement = FamilleEquipementSerializer(read_only=True)  
    id_groupe_equipement = GroupeEquipementSerializer(read_only=True)    
    prestataire_id = serializers.PrimaryKeyRelatedField(queryset=Prestataire.objects.all())  
    id_nbr_site = serializers.PrimaryKeyRelatedField(queryset=NbrSite.objects.all())  

    class Meta:  
        model = EquipementSQL  
        fields = '__all__'  

# Sérialiseur pour StatutNC  
class StatutNCSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = StatutNC  
        fields = '__all__'  

# Sérialiseur pour HistoriqueNC  
class HistoriqueNCSerializer(serializers.ModelSerializer):  
    non_conformite = serializers.PrimaryKeyRelatedField(queryset=NonConformite.objects.all())  
    statut_nc = serializers.PrimaryKeyRelatedField(queryset=StatutNC.objects.all())  

    class Meta:  
        model = HistoriqueNC  
        fields = '__all__'  

# Sérialiseur pour NonConformite  
class MarcheSerializer(serializers.ModelSerializer):  
    prestataire = serializers.PrimaryKeyRelatedField(queryset=Prestataire.objects.all())  

    class Meta:  
        model = Marche  
        fields = '__all__'
class NonConformiteSerializer(serializers.ModelSerializer):  
    batiment = BatimentSerializer()  
    statut_nc = StatutNCSerializer()
    criticite_non_conformite = CriticiteNCSerializer()  
    equipement = EquipementSQLSerializer()  
    espace = EspaceSQLSerializer()  
    famille_equipement = FamilleEquipementSerializer()  
    importance_geographique = ImportanceGeoSerializer()  
    lot_technique = LotTechniqueSerializer()  
    marche = MarcheSerializer()  
    niveau = NiveauSerializer()  
    prestataire = PrestataireSerializer()  
    prestataire_fpm = PrestataireSerializer(many=False, allow_null=True)  
    prestataire_st = PrestataireSerializer(many=False, allow_null=True)  
    
    class Meta:  
        model = NonConformite  
        fields = '__all__'  
        extra_kwargs = {  
            'date_debut_indisp': {'allow_null': True},  
            'date_fpm': {'allow_null': True},  
            'date_paliatif': {'allow_null': True},  
            'date_planification': {'allow_null': True},  
            'date_previsionnelle': {'allow_null': True},  
            'date_retablissement': {'allow_null': True},  
            'date_retablissement_final': {'allow_null': True},  
        }  
# Sérialiseur pour Ronde  
class RondeSerializer(serializers.ModelSerializer):  
    batiment = serializers.PrimaryKeyRelatedField(queryset=Batiment.objects.all())  
    cmsite = serializers.PrimaryKeyRelatedField(queryset=SiteSQL.objects.all())  
    equipement = serializers.PrimaryKeyRelatedField(queryset=EquipementSQL.objects.all())  
    espace = serializers.PrimaryKeyRelatedField(queryset=EspaceSQL.objects.all())  
    niveau = serializers.PrimaryKeyRelatedField(queryset=Niveau.objects.all())  
    prestataire = serializers.PrimaryKeyRelatedField(queryset=Prestataire.objects.all())  

    class Meta:  
        model = Ronde  
        fields = '__all__'  

# Sérialiseur pour RondeCommentaires  
class RondeCommentairesSerializer(serializers.ModelSerializer):  
    ronde = serializers.PrimaryKeyRelatedField(queryset=Ronde.objects.all())  

    class Meta:  
        model = RondeCommentaires  
        fields = '__all__'  

# Sérialiseur pour RondeEvent  
class RondeEventSerializer(serializers.ModelSerializer):  
    ronde = serializers.PrimaryKeyRelatedField(queryset=Ronde.objects.all())  

    class Meta:  
        model = RondeEvent  
        fields = '__all__'  

# Sérialiseur pour RondeParametre  
class RondeParametreSerializer(serializers.ModelSerializer):  
    donnee_mesure = serializers.PrimaryKeyRelatedField(queryset=DonneeMesure.objects.all())  
    ronde = serializers.PrimaryKeyRelatedField(queryset=Ronde.objects.all())  
    unite_de_mesure = serializers.PrimaryKeyRelatedField(queryset=UniteMesure.objects.all())  

    class Meta:  
        model = RondeParametre  
        fields = '__all__'  

# Sérialiseur pour RondeReleve  
class RondeReleveSerializer(serializers.ModelSerializer):  
    ronde_event = serializers.PrimaryKeyRelatedField(queryset=RondeEvent.objects.all())  
    ronde_parametre = serializers.PrimaryKeyRelatedField(queryset=RondeParametre.objects.all())  

    class Meta:  
        model = RondeReleve  
        fields = '__all__'  

# Sérialiseur pour TypeRealisation  
class TypeRealisationSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = TypeRealisation  
        fields = '__all__'  

# Sérialiseur pour UniteMesure  
class UniteMesureSerializer(serializers.ModelSerializer):  
    donnee_mesure = serializers.PrimaryKeyRelatedField(queryset=DonneeMesure.objects.all())  

    class Meta:  
        model = UniteMesure  
        fields = '__all__'  

# Sérialiseur pour DonneeMesure  
class FrequenceSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Frequence  
        fields = '__all__'  
class DonneeMesureSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = DonneeMesure  
        fields = '__all__'  
class PlanificationSerializer(serializers.ModelSerializer):  
    marche = serializers.PrimaryKeyRelatedField(queryset=Marche.objects.all())  
    prestataire = serializers.PrimaryKeyRelatedField(queryset=Prestataire.objects.all())  

    class Meta:  
        model = Planification  
        fields = '__all__'  

class DetailPlanificationSerializer(serializers.ModelSerializer):  
    planification = PlanificationSerializer()  
    criticite_equipement = serializers.PrimaryKeyRelatedField(queryset=CriticiteEquipement.objects.all())  
    equipement = EquipementSQLSerializer()
    famille_equipement = FamilleEquipementSerializer()  
    frequence = FrequenceSerializer() 
    groupe_equipement = serializers.PrimaryKeyRelatedField(queryset=GroupeEquipement.objects.all())  
    lot_technique = LotTechniqueSerializer() 

    class Meta:  
        model = DetailPlanification  
        fields = '__all__'  
# Sérialiseur pour Intervention  
class InterventionSerializer(serializers.ModelSerializer):  
    cloturer_par = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  
    detail_planification = DetailPlanificationSerializer()  

    class Meta:  
        model = Intervention  
        fields = '__all__'  

# Sérialiseur pour InterventionAttachement  
class InterventionAttachementSerializer(serializers.ModelSerializer):  
    intervention = serializers.PrimaryKeyRelatedField(queryset=Intervention.objects.all())  

    class Meta:  
        model = InterventionAttachement  
        fields = '__all__'  

# Sérialiseur pour InterventionIntervenants  
class InterventionIntervenantsSerializer(serializers.ModelSerializer):  
    intervention = serializers.PrimaryKeyRelatedField(queryset=Intervention.objects.all())  

    class Meta:  
        model = InterventionIntervenants  
        fields = '__all__'  

# Sérialiseur pour InterventionPrestataire  
class InterventionPrestataireSerializer(serializers.ModelSerializer):  
    intervention = serializers.PrimaryKeyRelatedField(queryset=Intervention.objects.all())  
    prestataire = serializers.PrimaryKeyRelatedField(queryset=Prestataire.objects.all())  

    class Meta:  
        model = InterventionPrestataire  
        fields = '__all__'  

# Sérialiseur pour Planification  

# Sérialiseur pour DetailPlanification  


# Sérialiseur pour Frequence  


# Sérialiseur pour DetailPlanificationIntervention  
class DetailPlanificationInterventionSerializer(serializers.ModelSerializer):  
    detail_planification = serializers.PrimaryKeyRelatedField(queryset=DetailPlanification.objects.all())  
    intervention = serializers.PrimaryKeyRelatedField(queryset=Intervention.objects.all())  

    class Meta:  
        model = DetailPlanificationIntervention  
        fields = '__all__'  

# Sérialiseur pour User  
class UserSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = User  
        fields = '__all__'  

# Sérialiseur pour UserAffec  
class UserAffecSerializer(serializers.ModelSerializer):  
    marche = serializers.PrimaryKeyRelatedField(queryset=Marche.objects.all())  
    prestataire = serializers.PrimaryKeyRelatedField(queryset=Prestataire.objects.all())  
    site = serializers.PrimaryKeyRelatedField(queryset=SiteSQL.objects.all())  
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  

    class Meta:  
        model = UserAffec  
        fields = '__all__'  

# Sérialiseur pour Marche  
  
class CriticiteNCSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = CriticiteNC  
        fields = ['id', 'actif', 'designation', 'ordre']  
class ActionSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Action  
        fields = '__all__'  # Vous pouvez lister les champs individuellement si nécessaire  


class StatutActionSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = StatutAction  
        fields = '__all__'  # Vous pouvez lister les champs individuellement si nécessaire  
from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

class LDAPUserSerializer(serializers.Serializer):
    cn = serializers.CharField()
    sn = serializers.CharField()