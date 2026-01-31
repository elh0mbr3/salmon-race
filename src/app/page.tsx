"use client";

import Image from "next/image";
import styles from "./page.module.css";
import Buttons from "./components/buttons";
import { useState, useEffect } from "react";

import salmon1 from "./assets/pictures of salmon/1.png";
import salmon2 from "./assets/pictures of salmon/2.png";
import salmon3 from "./assets/pictures of salmon/3.png";
import salmon4 from "./assets/pictures of salmon/4.png";

const spriteMap: { [key: number]: typeof salmon1 } = {
  1: salmon1,
  2: salmon2,
  3: salmon3,
  4: salmon4,
};

// fish data from CSV (excluding header)
const fishData = [
  { name: "Holy Carp", odds: 0.04, sprite: 1 },
  { name: "Gar Licbread", odds: 0.2, sprite: 2 },
  { name: "Eel Pie", odds: 0.4, sprite: 3 },
  { name: "Ray Parker Jr.", odds: 0.33, sprite: 1 },
  { name: "Jack Dempsey", odds: 0.17, sprite: 3 },
  { name: "Red Herring", odds: 0.5, sprite: 4 },
  { name: "Holy Mackarel", odds: 0.07, sprite: 2 },
  { name: "Marlin Brando", odds: 0.43, sprite: 3 },
  { name: "Jackson Pollock", odds: 0.25, sprite: 2 },
  { name: "Scatman John", odds: 0.1, sprite: 4 },
  { name: "That's a moray", odds: 0.5, sprite: 4 },
  { name: "The old billfish", odds: 0.32, sprite: 1 },
];

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
  const [selectedFish, setSelectedFish] = useState<typeof fishData>([]);
  const [raceStarted, setRaceStarted] = useState(false);

  useEffect(() => {
    const shuffled = shuffleArray(fishData);
    const selected = shuffled.slice(0, 10);
    setSelectedFish(selected);
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
