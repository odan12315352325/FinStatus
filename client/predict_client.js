

async function runPredict() {
  const payload = {
    inn: "1234567890",
    company_name: "ООО Пример",
    year: 2024,
    quarter: 4,
    features: Array.from({ length: 35 }, (_, i) => 0.1 * (i + 1))
  };

  const r = await fetch("http://localhost:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await r.json();
  console.log("Prediction:", data);
}

runPredict().catch(console.error);
