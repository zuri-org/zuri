import { useState } from "react";

export default function ConsultaForm({ onResult }) {
  const [frase, setFrase] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!frase.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://217.160.4.170:8005/responder", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ frase }),
      });
      if (!res.ok) throw new Error("Error en la API");
      const data = await res.json();
      onResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="consulta-form">
      <textarea
        value={frase}
        onChange={(e) => setFrase(e.target.value)}
        placeholder="Ej: ¿Cuántos hurtos cometieron los europeos?"
        rows={3}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Consultando…" : "Consultar"}
      </button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}
