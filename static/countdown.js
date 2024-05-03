
    // Appel à l'API Ergast pour obtenir les détails de la prochaine course
    fetch('https://ergast.com/api/f1/2024.json')
    .then(response => response.json())
    .then(data => {
        // Extraire la date et l'heure de la prochaine course
        const nextRaceDate = new Date(data.MRData.RaceTable.Races[0].date + 'T' + data.MRData.RaceTable.Races[0].time);

        // Mettre à jour le compte à rebours chaque seconde
        const x = setInterval(function() {
            // Obtenir la date et l'heure actuelles
            const now = new Date().getTime();

            // Calculer la différence entre la date de la prochaine course et la date actuelle
            const distance = nextRaceDate - now;

            // Calculer les jours, heures, minutes et secondes restants
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Afficher le compte à rebours dans l'élément avec l'ID "countdown"
            document.getElementById("countdown").innerHTML = "Prochaine course : " + data.MRData.RaceTable.Races[0].raceName + " dans " + days + "j " + hours + "h " + minutes + "m " + seconds + "s ";

            // Si le compte à rebours est terminé, afficher un message
            if (distance < 0) {
                clearInterval(x);
                document.getElementById("countdown").innerHTML = "La course est en cours !";
            }
        }, 1000);
    })
    .catch(error => console.error('Une erreur s\'est produite lors de la récupération des données de l\'API Ergast :', error));
