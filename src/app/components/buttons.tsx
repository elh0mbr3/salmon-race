"use client";

import React, { useState, useRef } from "react";
import styles from "../page.module.css";

interface ButtonsProps {
  onStartRace: () => void;
  raceStarted: boolean;
  fishNames?: string[];
  username?: string;
  balance?: number | null;
}

export default function Buttons({
  onStartRace,
  raceStarted,
  fishNames = [],
  username,
  balance,
}: ButtonsProps) {
  const [selectedFish, setSelectedFish] = useState<string | null>(null);
  const [betAmount, setBetAmount] = useState<number>(10);
  const betTypeRef = useRef<HTMLSelectElement>(null);

  // helper function to get valid bet amount
  const getValidBetAmount = (fishName: string): number | null => {
    let stake: number | null = null;

    while (stake === null) {
      const stakeInput = prompt(
        `How much would you like to bet on ${fishName}?`,
        "10",
      );

      if (stakeInput === null) {
        // user cancelled
        return null;
      }

      const parsedStake = parseFloat(stakeInput);

      if (isNaN(parsedStake) || parsedStake <= 0) {
        alert("Please enter a valid positive amount.");
        continue;
      }

      if (balance !== null && balance !== undefined && parsedStake > balance) {
        alert(
          `You don't have enough balance! Your current balance is $${balance.toLocaleString()}. Please enter a smaller amount.`,
        );
        continue;
      }

      // checking if betting entire balance
      if (
        balance !== null &&
        balance !== undefined &&
        parsedStake === balance
      ) {
        alert("LET'S GO GAMBLING!!!!!!!!!!");
      }

      stake = parsedStake;
    }

    return stake;
  };

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

        const stake = getValidBetAmount(fishName);
        if (stake !== null) {
          setBetAmount(stake);

          try {
            const betType = betTypeRef.current?.value || "win";
            const response = await fetch(
              `/api/sendBet?username=${encodeURIComponent(username)}&stake=${stake}&on_fish=${encodeURIComponent(fishName)}&bet_type=${encodeURIComponent(betType)}`,
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
  };

  return (
    <div>
      <select id="bet_type" ref={betTypeRef}>
        <option value="win">Win</option>
        <option value="place">Place</option>
        <option value="each_way">Each Way</option>
      </select>
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
