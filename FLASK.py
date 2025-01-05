# Script Streamlit (streamlit_app.py)
import streamlit as st                                                                                   
import requests
def get_matrix_values_A():
    try:
        # Effectuer une requête GET pour récupérer les valeurs de la matrice
        response = requests.get("https://webapp-esz7.onrender.com/get_matrix_values_A")
        # Vérifier si la requête a réussi (code de statut 200)
        if response.status_code == 200:
            matrix_valuesA = response.json()
            return matrix_valuesA
        else:
            st.error(f"Échec de la requête GET avec le code de statut {response.status_code}")
            st.error(response.text)
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la requête GET : {str(e)}")
        return None

def get_vector_values():
    try:
        # Effectuer une requête GET pour récupérer les valeurs du vecteur
        response = requests.get("https://webapp-esz7.onrender.com/get_vector_values")
        # Vérifier si la requête a réussi (code de statut 200)
        if response.status_code == 200:
            vector_values = response.json()
            return vector_values
        else:
            st.error(f"Échec de la requête GET avec le code de statut {response.status_code}")
            st.error(response.text)
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la requête GET : {str(e)}")
        return None



def matriceA_html():

    html_code = """
   <!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matrice Dynamique</title>
    <style>
    .matrix-container {
        display: flex;
        flex-direction: column;
        align-items: left;
        margin-top: 20px;
    }
    
    body {
        padding: 0px;
        margin: 0px;
        max-width: 1444px;
        min-width: min-content;
        margin-left: auto;
        margin-right: auto;
    }
    
    .matrix {
        margin: 5px;
        display: flex;
        flex-direction: column;
    }
    
    .matrix-row {
        display: flex;
    }
    
    /* Nouveau style pour les cases de la matrice */
    .matrix-cell {
        width: 45px;
        height: 45px;
        margin: 3px;
        position: relative;
        background: white;
        border: none;
        border-radius: 4px;
        box-shadow: 0 0 0 1.5px #2285b2;
        transition: all 0.2s ease;
        overflow: hidden;
    }

    .matrix-cell:hover {
        box-shadow: 0 0 0 2px #2285b2;
    }

    .matrix-input {
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
        text-align: center;
        font-size: 16px;
        color: #333;
        transition: all 0.3s ease;
        padding: 0;
    }

    .matrix-input:focus {
        outline: none;
        background-color: rgba(34, 133, 178, 0.1);
    }

    .matrix-cell-filled {
        background-color: rgba(34, 133, 178, 0.15);
    }

    .matrix-input:not(:placeholder-shown) {
        font-weight: 500;
    }

    .matrix-input[type="number"] {
        -moz-appearance: textfield;
    }

    .matrix-input::-webkit-outer-spin-button,
    .matrix-input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    
    input {
        width: 100%;
        height: 100%;
        border: none;
        box-sizing: border-box;
        text-align: center;
    }
    
    html {
        scroll-behavior: smooth;
        color: #242424;
        color: var(--color-text);
        padding: 12px;
        padding-top: 0px;
        padding-bottom: 0px;
        /*overflow-y: scroll;*/
        overflow-y: auto; 
        background-color: white;
        background-color: var(--color-background);
        background-size: 60px 40px;
        background-position: -1px -1px;
        font-size: 17px;
        line-height: 1.5;
    }
    
    .button-container {
        margin-top: 10px;
    }

    .add-button {
        display: inline-block;
        padding: 2px 8px;
        margin: 0px;
        line-height: 1;
        color: #ffffff;
        text-align: center;
        text-decoration: none;
        cursor: pointer;
        border: 1px solid;
        border-radius: 4px;
        transition: background-color 0.3s, color 0.3s;
    }

    .add-button.blue-theme {
        background-color: #3498db;
        border-color: #87CEEB;
    }

    .add-button.dark-theme {
        background-color: #242424;
        border-color: #242424;
    }

    .add-button.light-theme {
        background-color: #a7acac;
        border-color: #ffffff;
        color: #242424;
    }

    .add-button:hover {
        background-color: #4682b4;
        color: #ffffff;
    }

    



    /* Style de base pour le slider */
    #matrix-size-slider {
        -webkit-appearance: none;  /* Pour le rendre compatible avec les navigateurs Webkit (comme Chrome/Safari) */
        width: 100%;  /* Vous pouvez ajuster la largeur selon vos besoins */
        height: 10px;  /* Hauteur du curseur */
        background: #ddd;  /* Couleur de fond par défaut */
        border-radius: 5px;
        outline: none;  /* Supprime l'effet de focus par défaut */
    }

    /* Style de la "piste" (track) */
    #matrix-size-slider::-webkit-slider-runnable-track {
        height: 10px;
        background: #ddd;  /* Couleur de la piste */
        border-radius: 5px;
    }

    /* Style de la boule (thumb) */
    #matrix-size-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        height: 16px;  /* Taille de la boule légèrement réduite */
        width: 16px;   /* Taille de la boule légèrement réduite */
        border-radius: 50%;
        background: #2285b2;  /* Couleur de la boule */
        cursor: pointer;
        margin-top: -3px;  /* Centrer la boule par rapport à la piste */
    }

    /* Pour Firefox */
    #matrix-size-slider::-moz-range-track {
        height: 10px;
        background: #ddd;
        border-radius: 5px;
    }

    #matrix-size-slider::-moz-range-thumb {
        height: 16px;  /* Taille de la boule légèrement réduite */
        width: 16px;   /* Taille de la boule légèrement réduite */
        border-radius: 50%;
        background: #2285b2;
        cursor: pointer;
    }

    /* Pour les autres navigateurs */
    #matrix-size-slider::-ms-track {
        height: 10px;
        background: #ddd;
        border-radius: 5px;
        border-color: transparent;
        color: transparent;
    }

    #matrix-size-slider::-ms-thumb {
        height: 16px;  /* Taille de la boule légèrement réduite */
        width: 16px;   /* Taille de la boule légèrement réduite */
        border-radius: 50%;
        background: #2285b2;
        cursor: pointer;
    }





</style>
</head>

<body>
    <legend align="left">La matrice A :</legend>

    <div class="matrix-container" id="matrix-container">
        <!-- La matrice sera générée dynamiquement ici -->
    </div>

    <div class="button-container">
        <label for="matrix-size-slider">Taille de la matrice :</label>
        <span id="slider-value">2</span>
        <input 
            type="range" 
            id="matrix-size-slider" 
            min="2" 
            max="10" 
            value="2" 
            oninput="updateMatrixSize(this.value)">
        
        <button class="add-button light-theme" onclick="effacer()">Effacer</button>
        <button class="add-button light-theme" onclick="remplirCasesVides()">Remplir par 0</button>
    </div>

    <script>
        var matrixValues = [];
        var numRows = 2;
        var numCols = 2;

        function effacer() {
            // Réinitialiser les dimensions de la matrice
            numCols = 2;
            numRows = 2;
            matrixValues = [];
            
            // Réinitialiser le slider à sa valeur initiale
            let slider = document.getElementById("matrix-size-slider");
            slider.value = 2;

            // Mettre à jour l'affichage de la valeur du slider
            let sliderValue = document.getElementById("slider-value");
            sliderValue.textContent = 2;

            // Recréer la matrice avec les dimensions initiales
            createMatrix();
        }
        
        function remplirCasesVides() {
        var inputs = document.getElementsByClassName("matrix-input");

        for (var i = 0; i < inputs.length; i++) {
            if (inputs[i].value === "") {
                inputs[i].value = 0;
            }
        }
        getMatrixValuesFromPython()
        }

        function createMatrix() {
            var oldMatrix = document.getElementById("matrix");
            if (oldMatrix) {
                oldMatrix.remove();
            }


            var matrixContainer = document.getElementById("matrix-container");
            var matrix = document.createElement("div");
            matrix.id = "matrix";
            matrix.classList.add("matrix");

            for (var i = 0; i < numRows; i++) {
                var row = document.createElement("div");
                row.classList.add("matrix-row");

                for (var j = 0; j < numCols; j++) {
                    var cell = document.createElement("div");
                    cell.classList.add("matrix-cell");

                    var input = document.createElement("input");
                    input.type = "number";
                    input.classList.add("matrix-input");
                    input.id = "cell_" + i + "_" + j;
                    

                    cell.appendChild(input);
                    row.appendChild(cell);
                }

                matrix.appendChild(row);
            }

            matrixContainer.appendChild(matrix);
            restoreMatrixValues();
        }

        function getMatrixValues() {
            matrixValues = [];
            var inputs = document.getElementsByClassName("matrix-input");
            for (var i = 0; i < inputs.length; i++) {
                matrixValues.push(inputs[i].value);
            }
            console.log("Matrix Values:", matrixValues);
        }

        function restoreMatrixValues() {
                var inputs = document.getElementsByClassName("matrix-input");

                for (var i = 0; i < numRows; i++) {
                    for (var j = 0; j < numCols; j++) {
                        var value = matrixValues[i] && matrixValues[i][j] !== undefined ? matrixValues[i][j] : '';
                        inputs[i * numCols + j].value = value;

                        if (value !== '') {
                            inputs[i * numCols + j].classList.add('matrix-cell-filled');
                        } else {
                            inputs[i * numCols + j].classList.remove('matrix-cell-filled');
                        }
                    }
                }
                attachEventListeners();
            }


            function saveMatrixValues() {
                var inputs = document.getElementsByClassName("matrix-input");
                matrixValues = [];

                for (var i = 0; i < numRows; i++) {
                    var rowValues = [];
                    for (var j = 0; j < numCols; j++) {
                        var inputValue = inputs[i * numCols + j].value;
                        rowValues.push(inputValue);

                        if (inputValue !== '') {
                            inputs[i * numCols + j].classList.add('matrix-cell-filled');
                        } else {
                            inputs[i * numCols + j].classList.remove('matrix-cell-filled');
                        }
                    }
                    matrixValues.push(rowValues);
                }
                attachEventListeners();
            }

        function updateMatrixSize(value) {
            // Mettre à jour l'affichage de la taille actuelle dans le slider
            document.getElementById("slider-value").textContent = value;

            // Convertir la valeur du slider en un entier
            var newSize = parseInt(value);

            // Sauvegarder les valeurs actuelles de la matrice avant de modifier sa taille
            saveMatrixValues();

            // Ajuster le nombre de lignes et de colonnes
            if (newSize > numRows) {
                // Ajouter des lignes et colonnes si la nouvelle taille est plus grande
                while (numRows < newSize) {
                    // Ajouter une colonne vide à chaque ligne existante
                    for (var i = 0; i < numRows; i++) {
                        matrixValues[i].push(''); // Ajoute une nouvelle cellule vide
                    }

                    // Ajouter une nouvelle ligne remplie de cellules vides
                    var newRow = Array(numCols + 1).fill('');
                    matrixValues.push(newRow);

                    numRows++;
                    numCols++;
                }
            } else if (newSize < numRows) {
                // Retirer des lignes et colonnes si la nouvelle taille est plus petite
                while (numRows > newSize) {
                    // Retirer la dernière colonne de chaque ligne
                    for (var i = 0; i < numRows; i++) {
                        matrixValues[i].pop(); // Supprime la dernière cellule
                    }

                    // Supprimer la dernière ligne
                    matrixValues.pop();

                    numRows--;
                    numCols--;
                }
            }

            // Recréer la matrice avec les nouvelles dimensions
            createMatrix();
        }

        function getMatrixValuesFromPython() {
           
            fetch('https://webapp-esz7.onrender.com/get_matrix_values_A')
                updateMatrixValuesInPython()
                .then(response => response.json())
                .then(data => {
                    matrixValuesA = data;
                    restoreMatrixValues();
                })
                .catch(error => console.error('Error:', error));
        }

        function updateMatrixValuesInPython() {
            saveMatrixValues();
            fetch('https://webapp-esz7.onrender.com/update_matrix_values_A', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        matrixValuesA: matrixValues
                    }),
                })
                .then(response => response.json())
                .then(data => console.log('Success:', data))
                .catch(error => console.error('Error:', error));
        }
        function attachEventListeners() {
            var inputs = document.getElementsByClassName("matrix-input");

            for (var i = 0; i < inputs.length; i++) {
               
                inputs[i].addEventListener('blur', getMatrixValuesFromPython);

            
                inputs[i].addEventListener('keydown', function (event) {
                    if (event.key === 'Enter') {
                        getMatrixValuesFromPython();
                    }
                });
            }
        
        }
        function initializeMatrix() {
            createMatrix();
            attachEventListeners();
        }
           
        initializeMatrix();


        
    </script>
</body>

</html>
    """
    return html_code

def vecteur_html():
    html_code= """
    <!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vecteur Dynamique</title>
    <style>
    .vector-container {
        display: flex;
        flex-direction: column;
        align-items: left;
        margin-top: 20px;
    }

    body {
        padding: 0px;
        margin: 0px;
        max-width: 1444px;
        min-width: min-content;
        margin-left: auto;
        margin-right: auto;
    }

    /* Nouveau style pour les cases du vecteur */
    .vector-cell {
    width: 45px;
    height: 45px;
    margin: 5px;  /* Augmenté de 3px à 5px pour plus d'espace */
    position: relative;
    background: white;
    border: none;
    border-radius: 4px;
    box-shadow: 0 0 0 1.5px #2285b2;
    transition: all 0.2s ease;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

    .vector-cell:hover {
        box-shadow: 0 0 0 2px #2285b2;
    }

    input {
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
        text-align: center;
        font-size: 16px;
        color: #333;
        transition: all 0.3s ease;
        padding: 0;
    }

    input:focus {
        outline: none;
        background-color: rgba(34, 133, 178, 0.1);
    }

    .vector-cell-filled {
        background-color: rgba(34, 133, 178, 0.15);
    }

    input:not(:placeholder-shown) {
        font-weight: 500;
    }

    input[type="number"] {
        -moz-appearance: textfield;
    }

    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    html {
        scroll-behavior: smooth;
        padding: 12px;
        padding-top: 0px;
        padding-bottom: 0px;
        /*overflow-y: scroll;*/
        overflow-y: auto; 
        background-size: 60px 40px;
        background-position: -1px -1px;
        font-size: 17px;
        line-height: 1.5;
    }

    .button-container {
        margin-top: 10px;
    }

    .add-button {
        display: inline-block;
        padding: 2px 8px;
        margin: 0px;
        line-height: 1;
        color: #ffffff;
        text-align: center;
        text-decoration: none;
        cursor: pointer;
        border: 1px solid;
        border-radius: 4px;
        transition: background-color 0.3s, color 0.3s;
    }

    .add-button.blue-theme {
        background-color: #3498db;
        border-color: #87CEEB;
    }

    .add-button.dark-theme {
        background-color: #242424;
        border-color: #242424;
    }

    .add-button.light-theme {
        background-color: #a7acac;
        border-color: #ffffff;
        color: #242424;
    }

    .add-button:hover {
        background-color: #4682b4;
        color: #ffffff;
    }


    /* Style de base pour le slider */
    #vector-size-slider {
        -webkit-appearance: none;  /* Pour le rendre compatible avec les navigateurs Webkit (comme Chrome/Safari) */
        width: 100%;  /* Vous pouvez ajuster la largeur selon vos besoins */
        height: 10px;  /* Hauteur du curseur */
        background: #ddd;  /* Couleur de fond par défaut */
        border-radius: 5px;
        outline: none;  /* Supprime l'effet de focus par défaut */
    }

    /* Style de la "piste" (track) */
    #vector-size-slider::-webkit-slider-runnable-track {
        height: 10px;
        background: #ddd;  /* Couleur de la piste */
        border-radius: 5px;
    }

    /* Style de la boule (thumb) */
    #vector-size-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        height: 16px;  /* Taille de la boule légèrement réduite */
        width: 16px;   /* Taille de la boule légèrement réduite */
        border-radius: 50%;
        background: #2285b2;  /* Couleur de la boule */
        cursor: pointer;
        margin-top: -3px;  /* Centrer la boule par rapport à la piste */
    }

    /* Pour Firefox */
    #vector-size-slider::-moz-range-track {
        height: 10px;
        background: #ddd;
        border-radius: 5px;
    }

    #vector-size-slider::-moz-range-thumb {
        height: 16px;  /* Taille de la boule légèrement réduite */
        width: 16px;   /* Taille de la boule légèrement réduite */
        border-radius: 50%;
        background: #2285b2;
        cursor: pointer;
    }

    /* Pour les autres navigateurs */
    #vector-size-slider::-ms-track {
        height: 10px;
        background: #ddd;
        border-radius: 5px;
        border-color: transparent;
        color: transparent;
    }

    #vector-size-slider::-ms-thumb {
        height: 16px;  /* Taille de la boule légèrement réduite */
        width: 16px;   /* Taille de la boule légèrement réduite */
        border-radius: 50%;
        background: #2285b2;
        cursor: pointer;
    }


</style>
</head>

<body>
    <legend align="left">Le vecteur b:</legend>

    <div class="vector-container" id="vector-container">
        <!-- Le vecteur sera généré dynamiquement ici -->
    </div>

    <div class="button-container">
        <label for="vector-size-slider">Taille du vecteur :</label>
        <span id="slider-value">2</span>
        <input 
            type="range" 
            id="vector-size-slider" 
            min="2" 
            max="10" 
            value="2" 
            oninput="updateVectorSize(this.value)">
        
        <button class="add-button light-theme" onclick="effacer()">effacer</button>
        <button class="add-button light-theme" onclick="remplirCasesVides()">Remplir par 0</button>
    </div>


    <script>
        var vectorValues = [];
        var numElements = 2;

        function createVector() {
            var oldVector = document.getElementById("vector");
            if (oldVector) {
                oldVector.remove();
            }

            var vectorContainer = document.getElementById("vector-container");
            var vector = document.createElement("div");
            vector.id = "vector";
            vector.classList.add("vector");

            for (var i = 0; i < numElements; i++) {
                var cell = document.createElement("div");
                cell.classList.add("vector-cell");

                var input = document.createElement("input");
                input.type = "number";
                input.classList.add("vector-input");
                input.id = "element_" + i;

                cell.appendChild(input);
                vector.appendChild(cell);
            }

            vectorContainer.appendChild(vector);
            restoreVectorValues();
        }
                function remplirCasesVides() {
            var inputs = document.getElementsByClassName("vector-input");

            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].value === "") {
                    inputs[i].value = 0;
                }

            }
            getVectorValuesFromPython();
           
        }

        function getVectorValues() {
            vectorValues = [];
            var inputs = document.getElementsByClassName("vector-input");
            for (var i = 0; i < inputs.length; i++) {
                vectorValues.push(inputs[i].value);
            }
            console.log("Vector Values:", vectorValues);
        }

        function restoreVectorValues() {
            var inputs = document.getElementsByClassName("vector-input");

            for (var i = 0; i < numElements; i++) {
                var value = vectorValues[i] !== undefined ? vectorValues[i] : '';
                inputs[i].value = value;
            
            if (value !== '') {
                    inputs[i].classList.add('vector-cell-filled');
                }
              attachEventListeners();
            }
        }

        function saveVectorValues() {
            var inputs = document.getElementsByClassName("vector-input");
            vectorValues = [];

            for (var i = 0; i < numElements; i++) {
                var inputValue = inputs[i].value;
                vectorValues.push(inputValue);
                  if (inputValue !== '') {
                    inputs[i].classList.add('vector-cell-filled');
                } else {
                    inputs[i].classList.remove('vector-cell-filled');
                }
            }
               attachEventListeners();
        }

        function updateVectorSize(value) {
            // Mettre à jour l'affichage de la taille actuelle dans le slider
            document.getElementById("slider-value").textContent = value;

            // Convertir la valeur du slider en un entier
            var newSize = parseInt(value);

            // Sauvegarder les valeurs actuelles du vecteur avant de modifier sa taille
            saveVectorValues();

            // Ajuster la taille du vecteur
            if (newSize > numElements) {
                // Ajouter des éléments si la nouvelle taille est plus grande
                while (numElements < newSize) {
                    vectorValues.push(''); // Ajouter un nouvel élément vide
                    numElements++;
                }
            } else if (newSize < numElements) {
                // Retirer des éléments si la nouvelle taille est plus petite
                while (numElements > newSize) {
                    vectorValues.pop(); // Supprimer le dernier élément
                    numElements--;
                }
            }

            // Recréer le vecteur avec les nouvelles dimensions
            createVector();
        }


        function effacer() {
            // Réinitialiser le nombre d'éléments du vecteur
            numElements = 2;
            vectorValues = [];
            
            // Réinitialiser le slider à sa valeur initiale
            let slider = document.getElementById("vector-size-slider");
            slider.value = 2;

            // Mettre à jour l'affichage de la valeur du slider
            let sliderValue = document.getElementById("slider-value");
            sliderValue.textContent = 2;

            // Recréer le vecteur avec les dimensions initiales
            createVector();
        }

        function getVectorValuesFromPython() {
            fetch('https://webapp-esz7.onrender.com/get_vector_values')
            updateVectorValuesInPython()
                .then(response => response.json())
                .then(data => {
                    vectorValues = data;
                    restoreVectorValues();
                })
                .catch(error => console.error('Error:', error));
        }

        function updateVectorValuesInPython() {
            saveVectorValues();
            fetch('https://webapp-esz7.onrender.com/update_vector_values', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        vectorValues: vectorValues
                    }),
                })
                .then(response => response.json())
                .then(data => console.log('Success:', data))
                .catch(error => console.error('Error:', error));
        }

        function attachEventListeners() {
            var inputs = document.getElementsByClassName("vector-input");

            for (var i = 0; i < inputs.length; i++) {
               
                inputs[i].addEventListener('blur',  getVectorValuesFromPython);

            
                inputs[i].addEventListener('keydown', function (event) {
                    if (event.key === 'Enter') {
                         getVectorValuesFromPython();
                    }
                });
            }
        }
        function initializevect() {
              createVector();
            attachEventListeners();
        }
        initializevect();
      
    </script>
</body>

</html>
    
    """
    return html_code