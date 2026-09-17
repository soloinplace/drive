console.log("APP.JS CHARGÉ");

const user = document.getElementById("user");
const connections = document.getElementById("connections");
const downloads = document.getElementById("downloads");
const denials = document.getElementById("denials");
const cleanStatus = document.getElementById("clean-status");

const popup = document.getElementById("alert-popup");
const alertRule = document.getElementById("alert-rule");
const alertMessage = document.getElementById("alert-message");
const closeButton = document.getElementById("close-alert");

const jsonFile = document.getElementById("json-file");


let alertQueue = [];
let alertShowing = false;



function showAlerts(alerts) {

    console.log("SHOW ALERTS :", alerts);

    alertQueue.push(...alerts);

    if (!alertShowing) {
        showNextAlert();
    }
}


function showNextAlert() {

    if (alertQueue.length === 0) {
        alertShowing = false;
        return;
    }

    alertShowing = true;

    const alert = alertQueue.shift();

    alertRule.textContent = `Rule : ${alert.rule}`;
    alertMessage.textContent = alert.message;

    popup.classList.remove("hidden");
}


async function checkLog(log) {

    console.log("CHECK LOG :", log);

    user.textContent = log.user;
    connections.textContent = log.connections ?? 0;
    downloads.textContent = log.downloads ?? 0;
    denials.textContent = log.denials ?? 0;

    const response = await fetch("http://localhost:8080/check", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(log)
    });

    const data = await response.json();

    console.log("RÉPONSE SERVEUR :", data);

    if (data.status === "ALERT") {

        console.log("ALERTES :", data.alerts);

        cleanStatus.classList.add("hidden");

        showAlerts(data.alerts);

    } else {

        console.log("AUCUNE ALERTE");

        cleanStatus.classList.remove("hidden");
    }
}


// Lecture du fichier JSON
jsonFile.addEventListener("change", () => {

    const file = jsonFile.files[0];

    if (!file) {
        return;
    }

    const reader = new FileReader();

    reader.onload = () => {

        try {
            const log = JSON.parse(reader.result);

            console.log("JSON chargé :", log);

            checkLog(log);

        } catch (error) {
            console.error("JSON invalide :", error);
        }
    };

    reader.readAsText(file);
});


closeButton.addEventListener("click", () => {

    popup.classList.add("hidden");

    showNextAlert();
});


closeSuccess.addEventListener("click", () => {

    successPopup.classList.add("hidden");

});