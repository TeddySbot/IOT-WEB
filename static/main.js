// static/main.js

// Connexion au broker via WebSocket
const client = mqtt.connect('wss://broker.emqx.io:8084/mqtt');

client.on('connect', () => {
    console.log('✅ Connecté au broker MQTT');

    const base = 'Ynov/VHT';

    // on ne s'abonne qu'aux topics de l'utilisateur connecté
    const topic = `${base}/${USER_ID}/+`;
    console.log('Abonnement au topic :', topic);

    client.subscribe(topic, err => {
        if (err) {
            console.error('❌ Erreur abonnement :', err);
        } else {
            console.log('📡 Abonné au topic :', topic);
        }
    });
});

client.on('message', (topic, message) => {
    const msg = message.toString();
    console.log('📥 Message reçu sur', topic, ':', msg);

    try {
        const data = JSON.parse(msg);

        // Ynov/VHT/userId/potId  → ["Ynov","VHT","1","1"]
        const parts = topic.split('/');
        const userIdFromTopic = parts[2];
        const potId = parts[3];

        console.log('Découpé :', parts, 'userId=', userIdFromTopic, 'potId=', potId);

        const tempEl = document.getElementById(`temp_${potId}`);
        const humEl  = document.getElementById(`hum_${potId}`);

        if (!tempEl || !humEl) {
            console.warn('⚠️ Pas d’éléments HTML pour ce pot', potId);
            return;
        }

        tempEl.innerText = data.Celsius ?? '--';
        humEl.innerText  = data.Humidité ?? '--';
    } catch (e) {
        console.error('💥 Erreur parsing JSON :', e, 'Message brut:', msg);
    }
});
