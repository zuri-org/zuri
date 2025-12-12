import { useState } from "react";
import ConsultaForm from "./ConsultaForm.jsx";
import Resultado from "./Resultado.jsx";

function App() {
  const [data, setData] = useState(null);

  return (
    <div className="app">
      <h1>Consulta de delitos – datos INE 2023</h1>
      <ConsultaForm onResult={setData} />
      <Resultado data={data} />
    </div>
  );
}

export default App;
