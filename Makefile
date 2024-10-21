# Nom de l'image Docker
IMAGE_NAME=pdf-diff-tool

# Chemin du répertoire courant
CURRENT_DIR=$(shell pwd)

# Dossier local où les PDF seront stockés avant d'être montés en tant que volume
VOLUME_DIR=$(CURRENT_DIR)/pdf-copies
BACKUP_DIR=$(CURRENT_DIR)/pdf-backups

# Commande pour démarrer l'ensemble des conteneurs
up: build run 
# Commande pour construire l'image Docker
build:
	@echo "==> Construction de l'image Docker..."
	docker build -t $(IMAGE_NAME) .

# Commande pour copier tous les PDF locaux dans le dossier du volume
copy-pdfs-to-volume:
	@echo "==> Copie des fichiers PDF locaux dans le dossier volume..."
	# Crée le dossier pdf-copies si nécessaire
	[ -d $(VOLUME_DIR) ] || mkdir -p $(VOLUME_DIR)
	[ -d $(BACKUP_DIR) ] || mkdir -p $(BACKUP_DIR)
	# Copie tous les fichiers PDF locaux dans ce dossier
	find $(CURRENT_DIR) -name '*.pdf' -not -path "$(VOLUME_DIR)/*" -not -path "$(BACKUP_DIR)/*" -exec cp -f {} $(VOLUME_DIR) \;

# Commande pour exécuter le conteneur avec le dossier pdf-copies monté en tant que volume
run: copy-pdfs-to-volume
	@echo "==> Lancement de la comparaison des PDF en arrière-plan..."
	docker-compose up -d
	@echo "==> Attente de la fin de la comparaison..."
	docker-compose logs --tail 50 -f pdf-diff
	@echo "==> Changement de propriétaire des fichiers générés..."
	sudo chown -R $(USER):$(USER) $(VOLUME_DIR)
	sudo chown -R $(USER):$(USER) $(BACKUP_DIR)
	@echo "==> Comparaison terminée. Les fichiers sont accessibles."


accessdb:
	docker-compose exec postgres psql -U pdf_user -d pdf_db
#\dt;
#SELECT * FROM pdf_metadata;



# Commande pour supprimer l'image Docker
clean:
	@echo "==> Suppression de l'image Docker"
	docker-compose down
	
# Commande pour supprimer le volume
fclean: clean
	rm -rf $(VOLUME_DIR)

# Commande pour afficher les logs
log:
	@echo "==> Arrêt et suppression des conteneurs et réseaux..."
	docker-compose logs

re : clean up

resup : fclean up

ls:
	docker ps -a
	docker images -a
	docker volume ls

adios:
	@if [ -n "$$(docker ps -aq)" ]; then docker rm -f $$(docker ps -aq); fi
	@if [ -n "$$(docker images -aq)" ]; then docker rmi -f $$(docker images -aq); fi
	@if [ -n "$$(docker volume ls -q)" ]; then docker volume rm $$(docker volume ls -q) || echo "Some volumes are still in use."; fi



