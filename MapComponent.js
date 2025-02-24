import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const MapComponent = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchAlerts = async () => {
      const response = await fetch("http://localhost:5001/alerts");
      const data = await response.json();
      setAlerts(data);
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <MapContainer center={[34.02, -6.84]} zoom={10} style={{ height: "500px" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {alerts.map((alert, index) => (
        <CircleMarker
          key={index}
          center={[alert.latitude, alert.longitude]}
          radius={10}
          color={alert.temperature > 40 || alert.smoke > 700 ? "red" : "orange"}
          fillOpacity={0.8}
        >
          <Popup>
            <b>🔥 Alerte Incendie !</b><br />
            🌡️ Température: {alert.temperature}°C<br />
            💨 Fumée: {alert.smoke}
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
};

export default MapComponent;
