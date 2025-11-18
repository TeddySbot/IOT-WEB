// Connexion au broker EMQX via WebSocket
const client = mqtt.connect('wss://broker.emqx.io:8084/mqtt');

client.on('connect', () => {
  console.log('✅ Connecté au broker MQTT');
  client.subscribe('VHT/Température/Salon', err => {
    if (!err) console.log('Abonné au topic VHT/Température/Salon');
  });
});

// Quand un message arrive
client.on('message', (topic, message) => {
  const msg = message.toString();

  try {
    const data = JSON.parse(msg);

    document.getElementById('temp').innerText = data.Celsius;
    document.getElementById('hum').innerText = data.Humidité;
  } catch (e) {
    console.error('Erreur parsing JSON:', e, 'Message reçu:', msg);
  }
});
