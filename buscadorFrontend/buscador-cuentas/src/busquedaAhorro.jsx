import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { FiDollarSign } from "react-icons/fi";
import { FaPiggyBank } from "react-icons/fa";

export default function BusquedaAhorro() {
  const [query, setQuery] = useState("");
  const [resultados, setResultados] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleBuscar = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/busquedaVectorialSBS/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setResultados(data.results || []);
    } catch (error) {
      console.error("Error en búsqueda:", error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-2xl mx-auto text-center">
        <div className="flex items-center justify-center gap-3 mb-4">
        <FaPiggyBank className="text-pink-600 text-8xl" />
        <h1 className="text-3xl font-bold">
            Encuentra la cuenta de ahorro ideal
        </h1>
        <FaPiggyBank className="text-pink-600 text-8xl" />
        </div>
        <p className="text-gray-600 mb-6">
          Escribe en lenguaje natural lo que estás buscando.
        </p>
        <div className="flex gap-2 mb-4">
          <Input
            placeholder="Ej: cuenta de ahorros a tu medida"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-grow"
          />
          <Button onClick={handleBuscar} disabled={loading}>
            {loading ? "Buscando..." : "Buscar"}
          </Button>
        </div>
      </div>

      <ScrollArea className="max-w-4xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {resultados.map((item) => (
            <Card key={item.id} className="bg-white shadow-md">
              <CardContent className="p-4">
                <h2 className="text-lg font-semibold mb-1">
                  {item.entidad} - {item.tipo_cuenta}
                </h2>
                    <p className="flex items-center gap-1 text-sm text-gray-700 mb-1 justify-center">
                    <FiDollarSign className="text-green-500" />
                    <strong>Tasa:</strong> {item.tasa} | <strong>Moneda:</strong> {item.moneda}
                    </p>
                <p className="text-sm text-gray-700 mb-1">
                  <strong>Ubicación:</strong> {item.ubicacion}
                </p>
                <p className="text-sm text-gray-600">{item.condiciones}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}