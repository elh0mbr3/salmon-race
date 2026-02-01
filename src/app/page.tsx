"use client";

import Image from "next/image";
import styles from "./page.module.css";
import Buttons from "./components/buttons";
import { useState, useEffect, useRef } from "react";
import confetti from "canvas-confetti";

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
type RaceSnapshot = { positions: { [fishName: string]: number }; tick: number };
type RaceResult = {
  winner: string;
  total_ticks: number;
  history: RaceSnapshot[];
};

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
  const [fishPositions, setFishPositions] = useState<{
    [name: string]: number;
  }>({});
  const [winner, setWinner] = useState<string | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [username, setUsername] = useState<string | null>(null);
  const [balance, setBalance] = useState<number | null>(null);
  const [balanceBeforeRace, setBalanceBeforeRace] = useState<number | null>(
    null,
  );
  const [profitLoss, setProfitLoss] = useState<number | null>(null);
  const animationRef = useRef<number | null>(null);
  const balanceBeforeRaceRef = useRef<number | null>(null);

  // function to fetch user balance
  const fetchBalance = async (user: string) => {
    try {
      const response = await fetch(
        `/api/getBalance?username=${encodeURIComponent(user)}`,
      );
      if (response.ok) {
        const data = await response.json();
        setBalance(data.balance);
      }
    } catch (error) {
      console.error("Failed to fetch balance:", error);
    }
  };

  // initialising username on mount
  useEffect(() => {
    const storedUsername = localStorage.getItem("salmonRaceUsername");
    if (storedUsername) {
      setUsername(storedUsername);
      fetchBalance(storedUsername);
    } else {
      const newUsername = prompt(
        "Welcome to Salmon Race! Enter your username:",
      );
      if (newUsername) {
        localStorage.setItem("salmonRaceUsername", newUsername);
        setUsername(newUsername);
        // registering with backend
        fetch(`/api/sendUname?username=${encodeURIComponent(newUsername)}`)
          .then(() => fetchBalance(newUsername))
          .catch(console.error);
      }
    }
  }, []);

  useEffect(() => {
    // fetching from backend API first, fallback to CSV
    fetch("/api/getFishNames")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Backend not available");
        }
        return response.json();
      })
      .then((data) => {
        // backend returns just names, we need to get full data from CSV
        // fetch CSV to get odds and sprites for the selected fish names
        return fetch("/fish.csv")
          .then((res) => res.text())
          .then((csv) => {
            const allFish = parseCSV(csv);
            const selectedNames: string[] = data.fish_names;
            // filtering to only fish selected by backend
            const selected = selectedNames
              .map((name: string) => allFish.find((f) => f.name === name))
              .filter((f): f is FishData => f !== undefined);
            setSelectedFish(selected);
            // initialising positions
            const initialPositions: { [name: string]: number } = {};
            selected.forEach((fish) => {
              initialPositions[fish.name] = 0;
            });
            setFishPositions(initialPositions);
          });
      })
      .catch(() => {
        // fallback to CSV only
        console.log("Backend not available, using CSV fallback");
        fetch("/fish.csv")
          .then((response) => response.text())
          .then((csv) => {
            const fishData = parseCSV(csv);
            const shuffled = shuffleArray(fishData);
            const selected = shuffled.slice(0, 10);
            setSelectedFish(selected);
            // initialising positions
            const initialPositions: { [name: string]: number } = {};
            selected.forEach((fish) => {
              initialPositions[fish.name] = 0;
            });
            setFishPositions(initialPositions);
          });
      });
  }, []);

  const animateRace = (history: RaceSnapshot[]) => {
    setIsAnimating(true);
    let currentTick = 0;

    const playNextTick = () => {
      if (currentTick >= history.length) {
        setIsAnimating(false);
        return;
      }

      const snapshot = history[currentTick];
      setFishPositions(snapshot.positions);
      currentTick++;

      // adjusting speed - 50ms per tick
      animationRef.current = window.setTimeout(playNextTick, 50);
    };

    playNextTick();
  };

  const handleStartRace = async () => {
    setRaceStarted(true);
    setWinner(null);
    setProfitLoss(null);
    // Store current balance before race starts using ref to avoid closure issues
    balanceBeforeRaceRef.current = balance;

    try {
      const response = await fetch("/api/startRace");
      if (!response.ok) {
        throw new Error("Failed to start race");
      }
      const result: RaceResult = await response.json();

      // animating the race using the history
      animateRace(result.history);

      // setting winner after animation completes
      const animationDuration = result.history.length * 50;
      setTimeout(async () => {
        setWinner(result.winner);
        // Trigger confetti celebration!
        confetti({
          particleCount: 150,
          spread: 100,
          origin: { y: 0.6 },
        });
        // refresh balance after race and calculate profit/loss
        if (username) {
          try {
            const response = await fetch(
              `/api/getBalance?username=${encodeURIComponent(username)}`,
            );
            if (response.ok) {
              const data = await response.json();
              setBalance(data.balance);
              // calculating profit/loss using ref
              if (balanceBeforeRaceRef.current !== null) {
                setProfitLoss(data.balance - balanceBeforeRaceRef.current);
              }
            }
          } catch (error) {
            console.error("Failed to fetch balance:", error);
          }
        }
      }, animationDuration);
    } catch (error) {
      console.error("Error starting race:", error);
      // fallback to simple animation if backend fails
      setIsAnimating(false);
    }
  };

  // cleanup animation on unmount
  useEffect(() => {
    return () => {
      if (animationRef.current) {
        clearTimeout(animationRef.current);
      }
    };
  }, []);

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <div className={styles.balanceDisplay}>
          <span className={styles.balanceLabel}>Balance:</span>
          <span className={styles.balanceAmount}>
            ${balance !== null ? balance.toLocaleString() : "..."}
          </span>
        </div>
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
                  style={{
                    left: `calc((100% - 80px) * ${(fishPositions[fish.name] || 0) / 100})`,
                    transition: isAnimating ? "left 50ms linear" : "none",
                  }}
                />
              </div>
            ))}
          </div>
        </div>
        {winner && (
          <div className={styles.winnerBanner}>
            🏆 Winner: {winner}!
            {profitLoss !== null && (
              <span
                className={
                  profitLoss >= 0 ? styles.profitText : styles.lossText
                }
              >
                {profitLoss >= 0
                  ? ` (+$${profitLoss.toLocaleString()})`
                  : ` (-$${Math.abs(profitLoss).toLocaleString()})`}
              </span>
            )}
            {profitLoss === null && " 🏆"}
          </div>
        )}
        <div>
          <Buttons
            onStartRace={handleStartRace}
            raceStarted={raceStarted}
            fishNames={selectedFish.map((f) => f.name)}
            username={username || undefined}
          />
        </div>
      </main>
    </div>
  );
}
