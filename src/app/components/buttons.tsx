"use client";

import React from "react";
import styles from "../page.module.css";

interface ButtonsProps {
  onStartRace: () => void;
  raceStarted: boolean;
}

export default function Buttons({ onStartRace, raceStarted }: ButtonsProps) {
  var thingymajiggywhatchamacallit;
  return (
    <div>
      <select id="bet_type">
        <option value="win">Win</option>
        <option value="place">Place</option>
        <option value="each_way">Each Way</option>
      </select>
      <button
        className={styles.actionButton}
        onClick={() => {
          thingymajiggywhatchamacallit = prompt(
            "Select a salmon to bet on (1-10).",
          );
          if (thingymajiggywhatchamacallit != null) {
            thingymajiggywhatchamacallit = parseInt(
              thingymajiggywhatchamacallit
            );
            if (
              !isNaN(thingymajiggywhatchamacallit) &&
              0 < thingymajiggywhatchamacallit &&
              thingymajiggywhatchamacallit < 11
            ) {
              console.log(thingymajiggywhatchamacallit - 1);
              {/* @ts-ignore */}
              console.log(document.getElementById("bet_type").value);
            }
          }
        }}
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
