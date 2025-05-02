import os
import json
import pandas as pd

def create_csv_from_json():

    # Chemin vers le dossier racine 7272660
    ROOT_DIR = os.getcwd() + '/dataset/7272660'

    # Liste pour stocker les données
    images_data = []
    segmentations_data = []

    # ID incrémentaux simulés
    current_image_id = 1
    current_segmentation_id = 1

    # Les catégories et leurs sous-dossiers
    CATEGORIES = {
        'Benign': 'Benign',
        'Malignant': 'Malignant',
        'Mormal': 'Normal'
    }

    # Parcours des catégories
    for category_key, category_folder in CATEGORIES.items():
        category_path = os.path.join(ROOT_DIR, category_folder, category_folder)

        images_path = os.path.join(category_path, 'image')
        segmentation_path = os.path.join(category_path, 'segmentation')

        # Vérifier que le dossier existe
        if not os.path.exists(images_path):
            print(f"Dossier {images_path} manquant.")
            continue

        for file_name in os.listdir(images_path):
            if file_name.lower().endswith('.jpg'):
                # Préparer les infos pour la table image
                image_record = {
                    'id_image': current_image_id,
                    'file_name': file_name,
                    'file_path': os.path.relpath(os.path.join(images_path, file_name), ROOT_DIR).replace("\\", "/"),
                    'category': category_key
                }
                images_data.append(image_record)

                base_name = os.path.splitext(file_name)[0]

                # Pour chaque type de segmentation
                for seg_type in ['liver', 'mass', 'outline']:
                    seg_folder = os.path.join(segmentation_path, seg_type)
                    seg_file_path = os.path.join(seg_folder, base_name + '.json')

                    if os.path.exists(seg_file_path):
                        # Lecture du contenu JSON
                        with open(seg_file_path, 'r', encoding='utf-8') as f:
                            annotation_content = json.load(f)

                        segmentation_record = {
                            'id_segmentation': current_segmentation_id,
                            'segmentation_type': seg_type.capitalize(),  # Liver, Mass, Outline
                            'annotation': json.dumps(annotation_content),  # pour l'insérer en base
                            'fk_id_image': current_image_id
                        }
                        segmentations_data.append(segmentation_record)
                        current_segmentation_id += 1
                    else:
                        # Pas d'erreur si mass manque pour normal par exemple
                        if seg_type == 'mass' and category_key == 'normal':
                            continue
                        else:
                            print(f"Annotation {seg_type} manquante pour {file_name}")

                # Incrémenter l'image id
                current_image_id += 1

    # Création des DataFrames
    df_images = pd.DataFrame(images_data)
    df_segmentations = pd.DataFrame(segmentations_data)

    # Sauvegarde en CSV
    os.makedirs(os.path.join(os.getcwd(), 'output_data'), exist_ok=True)
    output_images_csv = os.path.join(os.getcwd() + '/output_data/images.csv')
    output_segmentations_csv = os.path.join(os.getcwd() + '/output_data/segmentations.csv')

    df_images.to_csv(output_images_csv, index=False, encoding='utf-8')
    df_segmentations.to_csv(output_segmentations_csv, index=False, encoding='utf-8')

    print(f"CSV Images généré : {output_images_csv}")
    print(f"CSV Segmentations généré : {output_segmentations_csv}")
    
    return output_images_csv, output_segmentations_csv

create_csv_from_json()