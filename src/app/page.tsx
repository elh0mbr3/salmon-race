"use client";

import Image from "next/image";
import styles from "./page.module.css";
import Buttons from "./components/buttons";
import { useState, useEffect } from "react";

import salmon1 from "./assets/pictures of salmon/1.png";
import salmon2 from "./assets/pictures of salmon/2.png";
import salmon3 from "./assets/pictures of salmon/3.png";
import salmon4 from "./assets/pictures of salmon/4.png";
import salmon5 from "./assets/pictures of salmon/5.png";

const spriteMap: { [key: number]: typeof salmon1 } = {
  1: salmon1,
  2: salmon2,
  3: salmon3,
  4: salmon4,
  5: salmon5,
};

type FishData = { name: string; odds: number; sprite: number };

function parseCSV(csv: string): FishData[] {
  const lines = csv.trim().split("\n");
  // skipping header row
  return lines.slice(1).map((line) => {
    const [name, odds, sprite] = line.split(",");
    return {
      name: name.trim(),
      odds: parseFloat(odds),
      sprite: parseInt(sprite, 10),
    };
  });
}

// Fisher-Yates shuffle algorithm
function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

export default function Home() {
  const [selectedFish, setSelectedFish] = useState<FishData[]>([]);
  const [raceStarted, setRaceStarted] = useState(false);

  useEffect(() => {
    fetch("/fish.csv")
      .then((response) => response.text())
      .then((csv) => {
        const fishData = parseCSV(csv);
        const shuffled = shuffleArray(fishData);
        const selected = shuffled.slice(0, 10);
        setSelectedFish(selected);
      });
  }, []);

  const handleStartRace = () => {
    setRaceStarted(true);
  };

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <Image
          className={styles.projectLogo}
          src="/logo.png"
          alt="Salmon Race Logo"
          width={227}
          height={157}
          priority
        />
        <div className={styles.riverContainer}>
          <div className={styles.lanes}>
            {selectedFish.map((fish, index) => (
              <div key={index} className={styles.lane}>
                <div
                  className={`${styles.fishInfo} ${raceStarted ? styles.fishInfoHidden : ""}`}
                >
                  <span className={styles.fishName}>{fish.name}</span>
                  <span className={styles.fishOdds}>
                    {(fish.odds * 100).toFixed(0)}%
                  </span>
                </div>
                <Image
                  className={styles.fishSprite}
                  src={spriteMap[fish.sprite]}
                  alt={fish.name}
                  width={80}
                  height={40}
                />
              </div>
            ))}
          </div>
        </div>
        <div>
          <Buttons onStartRace={handleStartRace} raceStarted={raceStarted} />
        </div>
      </main>
    </div>
  );
}
