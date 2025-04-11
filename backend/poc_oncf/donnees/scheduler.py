import schedule  
import time  
import logging  
import requests  

# Configurez le logger  
logging.basicConfig(level=logging.INFO)  

def sync_data():  
    url = "http://127.0.0.1:8000/api/auto-sync/"  # L'URL que vous souhaitez appeler  
    try:  
        response = requests.get(url)  
        response.raise_for_status()  # Vérifie les erreurs HTTP  
        logging.info(f"Synchronisation réussie : {response.json()}")  
    except requests.exceptions.RequestException as e:  
        logging.error(f"Erreur lors de la synchronisation des données : {str(e)}")  

# Planifiez la tâche pour qu'elle s'exécute chaque minute  
schedule.every(1).minutes.do(sync_data)  

# Boucle principale qui exécute les tâches planifiées  
if __name__ == "__main__":  
    logging.info("Démarrage du planificateur de tâches...")  
    while True:  
        schedule.run_pending()  # Exécute les tâches planifiées qui sont prêtes à l'exécution  
        time.sleep(1)  # Attendre une seconde avant de vérifier à nouveau  