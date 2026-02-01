"use client";

import React, { useState } from "react";
import styles from "../page.module.css";

interface ButtonsProps {
  onStartRace: () => void;
  raceStarted: boolean;
  fishNames?: string[];
  username?: string;
}

export default function Buttons({
  onStartRace,
  raceStarted,
  fishNames = [],
  username,
}: ButtonsProps) {
  const [selectedFish, setSelectedFish] = useState<string | null>(null);
  const [betAmount, setBetAmount] = useState<number>(10);

  const handlePlaceBet = async () => {
    if (!username) {
      alert("Please enter a username first!");
      const newUsername = prompt("Enter your username:");
      if (newUsername) {
        try {
          await fetch(
            `/api/sendUname?username=${encodeURIComponent(newUsername)}`,
          );
        } catch (error) {
          console.error("Error creating user:", error);
        }
      }
      return;
    }

    if (fishNames.length === 0) {
      // fallback to number prompt if no fish names provided
      const selection = prompt("Select a salmon to bet on (1-10).");
      if (selection != null) {
        const fishIndex = parseInt(selection);
        if (!isNaN(fishIndex) && fishIndex > 0 && fishIndex < 11) {
          console.log("Selected fish index:", fishIndex - 1);
        }
      }
      return;
    }

    // showing fish selection dialog
    const fishList = fishNames.map((name, i) => `${i + 1}. ${name}`).join("\n");
    const selection = prompt(
      `Select a salmon to bet on:\n${fishList}\n\nEnter number (1-${fishNames.length}):`,
    );

    if (selection != null) {
      const fishIndex = parseInt(selection);
      if (!isNaN(fishIndex) && fishIndex > 0 && fishIndex <= fishNames.length) {
        const fishName = fishNames[fishIndex - 1];
        setSelectedFish(fishName);

        const stakeInput = prompt(
          `How much would you like to bet on ${fishName}?`,
          "10",
        );
        if (stakeInput) {
          const stake = parseFloat(stakeInput);
          if (!isNaN(stake) && stake > 0) {
            setBetAmount(stake);

            try {
              const response = await fetch(
                `/api/sendBet?username=${encodeURIComponent(username)}&stake=${stake}&on_fish=${encodeURIComponent(fishName)}&bet_type=WIN`,
              );
              if (response.ok) {
                alert(`Bet placed! $${stake} on ${fishName}`);
              } else {
                alert("Failed to place bet. Please try again.");
              }
            } catch (error) {
              console.error("Error placing bet:", error);
              alert("Error connecting to server.");
            }
          }
        }
      }
    }
  };

  return (
    <div>
      <button
        className={styles.actionButton}
        onClick={handlePlaceBet}
        disabled={raceStarted}
      >
        Place a bet
      </button>
      <button
        className={styles.actionButton}
        onClick={() => {
          onStartRace();
          console.log("Go");
        }}
        disabled={raceStarted}
      >
        Start the race
      </button>
    </div>
  );
}
