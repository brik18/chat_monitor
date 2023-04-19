import { useState } from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "react-chartjs-2";
ChartJS.register(ArcElement, Tooltip, Legend);
export default function FormMonitor(styles: any) {
  const [url, setUrl] = useState("");
  const [chatAnalized, setChatAnalized] = useState({
    rawData: {
      bad: 0,
      neutral: 0,
      good: 0,
    },
    chartData: {
      labels: ["Bad", "Neutral", "Good"],
      datasets: [
        {
          label: "% Interactions",
          data: [0, 0, 0],
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
          ],
        },
      ],
    },
  });
  const startMonitor = (e: any) => {
    e.preventDefault();
    console.log("test");
    setChatAnalized({
      rawData: {
        bad: 10,
        neutral: 50,
        good: 40,
      },
      chartData: {
        labels: ["Bad", "Neutral", "Good"],
        datasets: [
          {
            label: "% Interactions",
            data: [10, 50, 40],
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
            ],
          },
        ],
      },
    });
  };
  return (
    <div>
      <form>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="YouTube Live URL"
        ></input>
        <button onClick={startMonitor}>Start</button>
      </form>
      <div className={styles.grid}>
        <div className={styles.card}>
          <h2>Chart</h2>
          <Pie data={chatAnalized.chartData} />
        </div>
        <div className={styles.card}>
          <h2>Bad &rarr; {chatAnalized.rawData.bad}%</h2>
        </div>

        <div className={styles.card}>
          <h2>Neutral &rarr; {chatAnalized.rawData.neutral}%</h2>
        </div>

        <div className={styles.card}>
          <h2>Good &rarr; {chatAnalized.rawData.good}%</h2>
        </div>
      </div>
    </div>
  );
}
