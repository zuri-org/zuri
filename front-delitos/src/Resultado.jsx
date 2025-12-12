export default function Resultado({ data }) {
  if (!data) return null;

  const { frase, respuesta_gpt, resultado, resultado_total_general } = data;

  return (
    <div className="resultado">
      <h3>Frase consultada</h3>
      <p className="frase">{frase}</p>

      <h3>Respuesta (IA + datos INE 2023)</h3>
      <p className="gpt">{respuesta_gpt}</p>

      <h3>Datos por procedencia</h3>
      <table>
        <thead>
          <tr>
            <th>Procedencia</th>
            <th>TipoDelito</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {resultado.map((r, i) => (
            <tr key={i}>
              <td>{r.Procedencia}</td>
              <td>{r.TipoDelito}</td>
              <td>{r.Total}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <details>
        <summary>Datos totales (todas procedencias)</summary>
        <table>
          <thead>
            <tr>
              <th>TipoDelito</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            {resultado_total_general.map((r, i) => (
              <tr key={i}>
                <td>{r.TipoDelito}</td>
                <td>{r.Total}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </details>
    </div>
  );
}
