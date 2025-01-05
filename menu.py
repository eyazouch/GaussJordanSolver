from streamlit_option_menu import option_menu
from Opérations import Aide as A
from Opérations import Calcul_inverse as C
import streamlit as st
import numpy as np
import FLASK as f
import pandas as pd
from Fonctions import Calcul_résultat as cr
from Fonctions import Type_matrice as tm
from Fonctions import Fraction as FR 


def Résolution_des_systéme_linéaire():

    st.header(" Résolution de systéme : Ax=b")
    selected_option = st.radio("Sélectionnez une méthode", ["Manuel" ,"Aléatoire", "Importation fichier (.CSV)" ])

    if selected_option=="Manuel":
        matrice_html=f.matriceA_html()
        vecteur_html=f.vecteur_html()
        col1, col2 = st.columns(2)
        with col1:
            st.components.v1.html(matrice_html,width=300, height=300,scrolling=True)
        with col2:
            st.components.v1.html(vecteur_html,width=300, height=300,scrolling=True)
        afficher_details = st.checkbox("Afficher détails")
        if st.button("Résoudre"):
            try:
                A=np.array(f.get_matrix_values_A(),dtype=float)
                size=A.shape[0]
                b=np.array(f.get_vector_values(),dtype=float)

                matrix_type_A = tm.determine_matrix_type(A)
                st.success(tm.message_info(matrix_type_A))

                if size!=np.size(b):
                    st.warning("Le nombre de lignes de la matrice A doit correspondre à la taille du vecteur b ")
                    exit(0)
                if np.linalg.det(A) == 0:
                    st.warning("La matrice A n'est pas inversible")
                    if np.linalg.matrix_rank(A) < size:
                        augmented_matrix = np.column_stack((A, b))
                        if np.linalg.matrix_rank(A) != np.linalg.matrix_rank(augmented_matrix):
                            st.warning("Le système n'a pas de solution")
                        else:
                            st.warning("Le système possède une infinité de solutions")
                    else:
                        st.warning("Le système n'a pas de solution")
                    exit(0)
                
                b = b[:, np.newaxis]

                if matrix_type_A=="Dense": 
                    x, iterations = cr.gauss_jordan_dense(A, b, size, afficher_details)
                elif matrix_type_A=="d'identité":
                    x = b
                elif "Symétrique" in matrix_type_A or "Symétrique définie positive" in matrix_type_A or "Diagonale dominante par ligne" in matrix_type_A or "Diagonale dominante par colonne" in matrix_type_A or "Diagonale dominante" in matrix_type_A :
                    x, iterations=cr.gauss_jordan_sans_pivotage(A, b, size, afficher_details)
                elif matrix_type_A == "Diagonale":
                    x, iterations = cr.gauss_jordan_diagonale(A, b, size, afficher_details)
                elif "Demi-bande inférieure" in matrix_type_A:
                    x, iterations = cr.gauss_jordan_demi_bande_inf(A, b, size, matrix_type_A[1], afficher_details)
                elif "Demi-bande supérieure" in matrix_type_A:
                    x, iterations = cr.gauss_jordan_demi_bande_sup(A, b, size,matrix_type_A[1], afficher_details)
                elif "Bande" in matrix_type_A : 
                    x, iterations = cr.gauss_jordan_bande(A, b, size, matrix_type_A[1], afficher_details)
                elif "Bande symétrique définie positive" in matrix_type_A or "Matrice bande symétrique" in matrix_type_A:
                    x, iterations = cr.gauss_jordan_bande_symétrique_definie_positive(A, b, size, matrix_type_A[1], afficher_details)
                elif matrix_type_A == "Triangulaire supérieure":
                    x, iterations = cr.gauss_jordan_triangulaire_sup(A, b, size, afficher_details)
                elif matrix_type_A == "Triangulaire inférieure":
                    x, iterations = cr.gauss_jordan_triangulaire_inf(A, b, size, afficher_details)

                if afficher_details and matrix_type_A!="d'identité":
                    for idx, iteration in enumerate(iterations):
                        st.write(f"Étape {idx + 1} :")
                        st.dataframe(FR.matrix_to_fraction(iteration))

                # Afficher la solution finale
                if x is not None:
                    st.subheader("Solution x :")
                    st.dataframe(FR.matrix_to_fraction(x))

                    if matrix_type_A[0] in ["Bande", "Bande symétrique définie positive"]:
                        rapport = f"""
====================================================
                     RAPPORT
====================================================

Type de matrice : {matrix_type_A[0]} de largeur de bande m={matrix_type_A[1]}
Taille de la matrice : {size}

----------------------------------------------------
MATRICE A :
{str(FR.matrix_to_fraction(A))}

----------------------------------------------------
VECTEUR b :
{str(FR.matrix_to_fraction(b))}
"""

                        if afficher_details and iterations:
                            rapport += "\n----------------------------------------------------\nDÉTAILS DES ÉTAPES\n"
                            for idx, iteration in enumerate(iterations):
                                rapport += f"Étape {idx + 1} :\n"
                                rapport += str(FR.matrix_to_fraction(iteration)) + "\n\n"
                        rapport += f"----------------------------------------------------\nSOLUTION x :\n{FR.matrix_to_fraction(x)}\n\n===================================================="


                    elif matrix_type_A[0] in ["Demi-bande inférieure", "Demi-bande supérieure"]:
                        rapport = f"""
====================================================
                     RAPPORT
====================================================

Type de matrice : {matrix_type_A[0]} de largeur de demi bande m= {matrix_type_A[1]}
Taille de la matrice : {size}

----------------------------------------------------
MATRICE A :
{str(FR.matrix_to_fraction(A))}

----------------------------------------------------
VECTEUR b :
{str(FR.matrix_to_fraction(b))}
"""
                        if afficher_details and iterations:
                            rapport += "\n----------------------------------------------------\nDÉTAILS DES ÉTAPES\n"
                            for idx, iteration in enumerate(iterations):
                                rapport += f"Étape {idx + 1} :\n"
                                rapport += str(FR.matrix_to_fraction(iteration)) + "\n\n"
                        rapport += f"----------------------------------------------------\nSOLUTION x :\n{FR.matrix_to_fraction(x)}\n\n===================================================="


                    else:
                        rapport = f"""
====================================================
                     RAPPORT
====================================================

Type de matrice : {matrix_type_A}
Taille de la matrice : {size}

----------------------------------------------------
MATRICE A :
{str(FR.matrix_to_fraction(A))}

----------------------------------------------------
VECTEUR b :
{str(FR.matrix_to_fraction(b))}
"""
                        if afficher_details and matrix_type_A!="d'identité":
                            rapport += "\n----------------------------------------------------\nDÉTAILS DES ÉTAPES\n"
                            for idx, iteration in enumerate(iterations):
                                rapport += f"Étape {idx + 1} :\n"
                                rapport += str(FR.matrix_to_fraction(iteration)) + "\n\n"
                        rapport += f"----------------------------------------------------\nSOLUTION x :\n{FR.matrix_to_fraction(x)}\n\n===================================================="

                    # Télécharger le fichier bilan
                    st.download_button(
                        label="Télécharger le rapport en .txt",
                        data=rapport.encode('utf-8'),
                        file_name="rapport.txt",
                        mime="text/plain"
                    )
            except ValueError as e:
                     st.error(f"Une erreur est survenue lors de la conversion des données de la matrice A ou du vecteur b : {str(e)}")
            except Exception as ex:
                     st.error(f"Une erreur imprévue est survenue lors de la résolution du système : {str(ex)}")
                     


    elif selected_option == "Aléatoire":
        # Titre de la section
        st.subheader("Générer une matrice aléatoire")

        # Choix du type de matrice
        matrix_type = st.selectbox(
            "Sélectionnez le type de matrice",
            [
                "Dense", "Symétrique", "Symétrique définie positive", "Diagonale", "Diagonale dominante",
                "Triangulaire supérieure", "Triangulaire inférieure",
                "Bande", "Bande symétrique définie positive", "Demi-bande inférieure", "Demi-bande supérieure" 
            ]
        )

        # Créer des colonnes pour aligner les champs
        col1, col2 = st.columns(2)

        # Taille de la matrice dans la première colonne
        with col1:
            size = st.number_input(
                "Entrez la taille de la matrice (n x n)", 
                min_value=2, max_value=10, step=1, value=3
            )

        # Largeur de la bande ou demi-bande dans la deuxième colonne
        with col2:
            if matrix_type in ["Bande", "Bande symétrique définie positive"]:
                bande_width = st.number_input(
                    "Largeur de la bande (m)", 
                    min_value=1, max_value=size - 1, step=1, value=1
                )
                demi_bande_width = None
            elif matrix_type in ["Demi-bande inférieure", "Demi-bande supérieure"]:
                demi_bande_width = st.number_input(
                    "Largeur de la demi-bande (m)", 
                    min_value=1, max_value=size - 1, step=1, value=1
                )
                bande_width = None
            else:
                bande_width = None
                demi_bande_width = None


        st.write("Définir les limites des valeurs de la matrice")
        # Entrées pour la valeur minimale et maximale
        col1, col2, a, aa = st.columns(4)
        with col1:
            min = st.number_input("Valeur minimale", min_value=1, max_value=99999, step=1, value=1)
        with col2:
            max = st.number_input("Valeur maximale", min_value=2, max_value=100000, step=1, value=10)

        # Vérification de la validité des valeurs
        if min > max:
            st.warning(f"La valeur minimale ne peut pas dépasser la valeur maximale. Les deux valeurs ont été automatiquement échangées.")
            min, max = max, min
        elif min == max:
            st.warning(f"La matrice sera remplie avec la même valeur pour tous ses éléments.")
        else:
            st.success(f"Les valeurs seront générées entre {min} et {max}.")
        

        afficher_details = st.checkbox("Afficher détails")

        if st.button("Générer et résoudre"):
            try:
                A=tm.generate_specific_matrix(min, max, matrix_type, size, bande_width, demi_bande_width)

                # Générer un vecteur b
                b = np.random.randint(min, max, size=(size, 1))

                # Vérifier le type de matrice générée : matrix_type_A = dt.determine_matrix_type(A)

                # Afficher la matrice et le vecteur
                st.subheader("Matrice A :")
                st.dataframe(FR.matrix_to_fraction(A))
                st.subheader("Vecteur b :")
                st.dataframe(FR.matrix_to_fraction(b))

                if size!=np.size(b):
                    st.warning("Le nombre de lignes de la matrice A doit correspondre à la taille du vecteur b ")
                    exit(0)
                if np.linalg.det(A) == 0:
                    st.warning("La matrice A n'est pas inversible")
                    if np.linalg.matrix_rank(A) < size:
                        augmented_matrix = np.column_stack((A, b))
                        if np.linalg.matrix_rank(A) != np.linalg.matrix_rank(augmented_matrix):
                            st.warning("Le système n'a pas de solution")
                        else:
                            st.warning("Le système possède une infinité de solutions")
                    else:
                        st.warning("Le système n'a pas de solution")
                    exit(0)


                # Sélectionner et appliquer la méthode de résolution adaptée s'il n'y a aucune contrainte
                if matrix_type == "Dense":
                    x, iterations = cr.gauss_jordan_dense(A, b, size, afficher_details)
                elif matrix_type in ["Diagonale dominante","Symétrique", "Symétrique définie positive"]:
                    x, iterations = cr.gauss_jordan_sans_pivotage(A, b, size, afficher_details)
                elif matrix_type == "Diagonale":
                    x, iterations = cr.gauss_jordan_diagonale(A, b, size, afficher_details)
                elif matrix_type == "Demi-bande inférieure":
                    x, iterations = cr.gauss_jordan_demi_bande_inf(A, b, size,  demi_bande_width, afficher_details)
                elif matrix_type == "Demi-bande supérieure":
                    x, iterations = cr.gauss_jordan_demi_bande_sup(A, b, size,  demi_bande_width, afficher_details)
                elif matrix_type == "Bande":
                    x, iterations = cr.gauss_jordan_bande(A, b, size, bande_width, afficher_details)
                elif matrix_type == "Bande symétrique définie positive":
                    x, iterations = cr.gauss_jordan_bande_symétrique_definie_positive(A, b, size, bande_width, afficher_details)
                elif matrix_type == "Triangulaire supérieure":
                    x, iterations = cr.gauss_jordan_triangulaire_sup(A, b, size, afficher_details)
                elif matrix_type == "Triangulaire inférieure":
                    x, iterations = cr.gauss_jordan_triangulaire_inf(A, b, size, afficher_details)
                else:
                    st.error("Le type de matrice spécifié n'est pas pris en charge ou est mal défini.")
                    x, iterations = None, []

                # Afficher les détails si demandés
                if afficher_details and iterations:
                    for idx, iteration in enumerate(iterations):
                        st.write(f"Étape {idx + 1} :")
                        st.dataframe(FR.matrix_to_fraction(iteration))

                # Afficher la solution finale
                if x is not None:
                    st.subheader("Solution x :")
                    st.dataframe(FR.matrix_to_fraction(x))

                    if matrix_type in ["Bande", "Bande symétrique définie positive"]:
                        rapport = f"""
====================================================
                     RAPPORT
====================================================

Type de matrice : {matrix_type} de largeur de bande m={bande_width}
Taille de la matrice : {size}

----------------------------------------------------
MATRICE A :
{str(FR.matrix_to_fraction(A))}

----------------------------------------------------
VECTEUR b :
{str(FR.matrix_to_fraction(b))}
"""

                        if afficher_details and iterations:
                            rapport += "\n----------------------------------------------------\nDÉTAILS DES ÉTAPES\n"
                            for idx, iteration in enumerate(iterations):
                                rapport += f"Étape {idx + 1} :\n"
                                rapport += str(FR.matrix_to_fraction(iteration)) + "\n\n"
                        rapport += f"----------------------------------------------------\nSOLUTION x :\n{FR.matrix_to_fraction(x)}\n\n===================================================="


                    elif matrix_type in ["Demi-bande inférieure", "Demi-bande supérieure"]:
                        rapport = f"""
====================================================
                     RAPPORT
====================================================

Type de matrice : {matrix_type} de largeur de demi bande m= {demi_bande_width}
Taille de la matrice : {size}

----------------------------------------------------
MATRICE A :
{str(FR.matrix_to_fraction(A))}

----------------------------------------------------
VECTEUR b :
{str(FR.matrix_to_fraction(b))}
"""
                        if afficher_details and iterations:
                            rapport += "\n----------------------------------------------------\nDÉTAILS DES ÉTAPES\n"
                            for idx, iteration in enumerate(iterations):
                                rapport += f"Étape {idx + 1} :\n"
                                rapport += str(FR.matrix_to_fraction(iteration)) + "\n\n"
                        rapport += f"----------------------------------------------------\nSOLUTION x :\n{FR.matrix_to_fraction(x)}\n\n===================================================="


                    else:
                        rapport = f"""
====================================================
                     RAPPORT
====================================================

Type de matrice : {matrix_type}
Taille de la matrice : {size}

----------------------------------------------------
MATRICE A :
{str(FR.matrix_to_fraction(A))}

----------------------------------------------------
VECTEUR b :
{str(FR.matrix_to_fraction(b))}
"""
                        if afficher_details and iterations:
                            rapport += "\n----------------------------------------------------\nDÉTAILS DES ÉTAPES\n"
                            for idx, iteration in enumerate(iterations):
                                rapport += f"Étape {idx + 1} :\n"
                                rapport += str(FR.matrix_to_fraction(iteration)) + "\n\n"
                        rapport += f"----------------------------------------------------\nSOLUTION x :\n{FR.matrix_to_fraction(x)}\n\n===================================================="

                    # Télécharger le fichier bilan
                    st.download_button(
                        label="Télécharger le rapport en .txt",
                        data=rapport.encode('utf-8'),
                        file_name="rapport.txt",
                        mime="text/plain"
                    )
            except Exception as ex:
                st.error(f"Une erreur s'est produite lors de la génération de la matrice ou de la résolution du système : {str(ex)}")



    elif selected_option == "Importation fichier (.CSV)":
        st.subheader("Importer un fichier CSV contenant la matrice augmentée (A|b)")
        uploaded_file = st.file_uploader("Téléchargez votre fichier .CSV", type=["csv"])

        if uploaded_file:
            try:
                # Lire la première ligne pour les métadonnées
                first_line = uploaded_file.readline().decode('utf-8').strip()  # Assurez-vous que vous lisez la ligne correctement
                matrix_type, size = first_line.split(',')
                size = int(size)

                # Lire le reste du fichier
                df = pd.read_csv(uploaded_file, header=None)

                # Extraire la matrice augmentée (A|b)
                augmented_matrix = df.values
                A = augmented_matrix[:, :-1]  # Matrice A (toutes les colonnes sauf la dernière)
                b = augmented_matrix[:, -1].reshape(-1, 1)  # Vecteur b (dernière colonne)

                # Afficher la matrice A séparément
                if size <= 10:
                    st.subheader("Matrice A :")
                    st.dataframe(A)

                # Afficher le vecteur b séparément
                if size <= 10:
                    st.subheader("Vecteur b :")
                    st.dataframe(b)

                # Vérifier les dimensions
                if A.shape[0] != b.shape[0] or A.shape[0] != size:
                    st.error("Le nombre de lignes de la matrice A doit correspondre à la taille du vecteur b ainsi qu'à la taille indiquée dans le fichier")
                    return

                # Déterminer le type de matrice
                matrix_type = matrix_type.strip().replace('\ufeff', '')
                matrix_type_A = tm.determine_matrix_type(A)

                if matrix_type in ["B", "BSDP"]: #and matrix_type_A in ["Bande", "Bande symétrique définie positive"]:
                    bande_width = matrix_type_A[1]
                elif matrix_type in ["DBI", "DBS"]: #matrix_type in ["DBI", "DBS"] and matrix_type_A in ["Demi-bande inférieure", "Demi-bande supérieure"]
                    demi_bande_width = matrix_type_A[1]
                else:
                    bande_width = None
                    demi_bande_width = None
                

                st.success(tm.message_info(matrix_type_A))
                # Résoudre le système selon le type de matrice
                
                if size!=np.size(b):
                    st.warning("Le nombre de lignes de la matrice A doit correspondre à la taille du vecteur b ")
                    exit(0)
                if np.linalg.det(A) == 0:
                    st.warning("La matrice A n'est pas inversible")
                    if np.linalg.matrix_rank(A) < size:
                        augmented_matrix = np.column_stack((A, b))
                        if np.linalg.matrix_rank(A) != np.linalg.matrix_rank(augmented_matrix):
                            st.warning("Le système n'a pas de solution")
                        else:
                            st.warning("Le système possède une infinité de solutions")
                    else:
                        st.warning("Le système n'a pas de solution")
                    exit(0)
                

                if matrix_type in ["DE"]: #matrix_type_A == "Dense"
                    x = cr.gauss_jordan_dense(A, b, size)[0]
                elif matrix_type in ["S", "SDP", "DDL", "DDC", "DD"]:#matrix_type_A in ["Diagonale dominante par ligne", "Diagonale dominante par colonne", "Diagonale dominante",Symétrique"]:
                    x = cr.gauss_jordan_sans_pivotage(A, b, size)[0]
                elif matrix_type == "DI": #and matrix_type_A == "Diagonale":
                    x = cr.gauss_jordan_diagonale(A, b, size)[0]
                elif matrix_type == "TS": #and (matrix_type_A == "Triangulaire supérieure"):
                    x = cr.gauss_jordan_triangulaire_sup(A, b, size)[0]
                elif matrix_type == "TI": #and (matrix_type_A == "Triangulaire inférieure"):
                    x = cr.gauss_jordan_triangulaire_inf(A, b, size)[0]
                elif matrix_type == "DBI": #and ("Demi-bande inférieure" in matrix_type_A):
                    x = cr.gauss_jordan_demi_bande_inf(A, b, size, demi_bande_width)[0]
                elif matrix_type == "DBS": #and ("Demi-bande supérieure" in matrix_type_A):
                    x = cr.gauss_jordan_demi_bande_sup(A, b, size, demi_bande_width)[0]
                elif matrix_type == "B": #and (matrix_type_A == "Bande"):
                    x = cr.gauss_jordan_bande(A, b, size, bande_width)[0]
                elif matrix_type == "BSDP": #and ("Bande symétrique définie positive" in matrix_type_A):
                    x = cr.gauss_jordan_bande_symétrique_definie_positive(A, b, size, bande_width)[0]
                else:
                    st.error("Le type de matrice spécifié n'est pas pris en charge ou est mal défini")
                    return
                    


                # Afficher la solution sous forme de fraction
                st.subheader("Solution x :")
                st.dataframe(FR.matrix_to_fraction(x))

                if matrix_type in ["B", "BSDP"]:
                    rapport = f"""
====================================================
                     RAPPORT
====================================================

Type de matrice : {matrix_type_A[0]} de largeur de bande m= {bande_width}
Taille de la matrice : {size}

----------------------------------------------------
MATRICE A :
{str(FR.matrix_to_fraction(A))}

----------------------------------------------------
VECTEUR b :
{str(FR.matrix_to_fraction(b))}

----------------------------------------------------
SOLUTION x :
{FR.matrix_to_fraction(x)}

====================================================
"""
                elif matrix_type in ["DBI", "DBS"]:
                    rapport = f"""
====================================================
                     RAPPORT
====================================================

Type de matrice : {matrix_type_A[0]} de largeur de demi bande m= {demi_bande_width}
Taille de la matrice : {size}

----------------------------------------------------
MATRICE A :
{str(FR.matrix_to_fraction(A))}

----------------------------------------------------
VECTEUR b :
{str(FR.matrix_to_fraction(b))}

----------------------------------------------------
SOLUTION x :
{FR.matrix_to_fraction(x)}

====================================================
"""
                    
                else:
                    rapport = f"""
====================================================
                     RAPPORT
====================================================

Type de matrice : {matrix_type_A}
Taille de la matrice : {size}

----------------------------------------------------
MATRICE A :
{str(FR.matrix_to_fraction(A))}

----------------------------------------------------
VECTEUR b :
{str(FR.matrix_to_fraction(b))}

----------------------------------------------------
SOLUTION x :
{FR.matrix_to_fraction(x)}

====================================================
"""
                # Télécharger le fichier bilan
                st.download_button(
                    label="Télécharger le rapport en .txt",
                    data=rapport.encode('utf-8'),
                    file_name="rapport.txt",
                    mime="text/plain"
                )
            except Exception as ex:
                st.error(f"Une erreur s'est produite lors du traitement du fichier : {str(ex)}")















st.set_page_config(
    page_title="Calcul Matriciel",
    page_icon="Gausss.png",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Styles CSS personnalisés
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stButton button {
        background-color: #2285b2;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stTitle {
        color: #1f4287;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .footer {
        width: 100%;
        background-color: #ffffff;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
        margin-bottom: 0;
    }
    </style>
""", unsafe_allow_html=True)

def header():
    """Affiche l'en-tête de l'application"""
    st.markdown('<p class="stTitle">Calcul Matriciel Par La Méthode De Gauss Jordan</p>', unsafe_allow_html=True)

def sidebar_menu():
    """Configuration du menu latéral"""
    
    with st.sidebar:
        st.image("Gausss.png", width=100)
        selected = option_menu(
            menu_title="Menu",
            options=[
                "Résolution de Systèmes",
                "Calcul de l'inverse",
                "Aide"
            ],
            icons=["calculator", "arrow-repeat", "question-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "1rem", "background-color": "#ffffff"},
                "icon": {"color": "#2285b2", "font-size": "1.2rem"},
                "nav-link": {
                    "font-size": "1rem",
                    "text-align": "left",
                    "margin": "0.5rem",
                    "--hover-color": "#eee"
                },
                "nav-link-selected": {"background-color": "#2285b2"}
            }
        )
    return selected

def footer():
    """Affiche le pied de page"""
    st.markdown(
        """
        <style>
            .footer {
                width: 100%;
                background-color: #ffffff;
                padding: 1rem;
                border-top: 1px solid #e0e0e0;
                display: flex;
                justify-content: space-between; /* Pour aligner les éléments de chaque côté */
                align-items: center; /* Pour aligner verticalement */
            }
            .footer div {
                display: flex;
                align-items: center; /* Pour aligner les éléments à l'intérieur de chaque div */
            }
            .footer p {
                margin: 0;
                font-size: 14px;  /* Taille de police ajustable */
            }
            .footer img {
                width: 80px;
            }
        </style>

        <div class="footer">
            <div>
                <p>Superviseur: Dr. Sirine MARRAKCHI<br>
                Matière: Algorithmes Numériques</p>
            </div>
            <div>
                <p>Filière: Cycle d'ingénieur<br>
                Établissement: Faculté des Sciences de Sfax</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    """Fonction principale de l'application"""
    header()
    selected = sidebar_menu()
    
    # Container principal pour le contenu
    with st.container():
        st.markdown("<br>", unsafe_allow_html=True)
        
        if selected == "Résolution de Systèmes":
            Résolution_des_systéme_linéaire()
        elif selected == "Calcul de l'inverse":
            C.main()
        elif selected == "Aide":
            A.main()
    
    footer()

if __name__ == "__main__":
    main()
