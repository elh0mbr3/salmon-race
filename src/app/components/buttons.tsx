"use client";

import React from "react";
import styles from "../page.module.css";

export default function Buttons() {
  var thingymajiggywhatchamacallit;
  return (
    <div>
      <button
        className={styles.actionButton}
        onClick={() => {
          thingymajiggywhatchamacallit = prompt(
            "Select a salmon to bet on (1-10).",
          );
          if (thingymajiggywhatchamacallit != null) {
            thingymajiggywhatchamacallit = parseInt(
              thingymajiggywhatchamacallit,
            );
            if (
              !isNaN(thingymajiggywhatchamacallit) &&
              0 < thingymajiggywhatchamacallit &&
              thingymajiggywhatchamacallit < 11
            ) {
              console.log(thingymajiggywhatchamacallit - 1);
            }
          }
        }}
      >
        Place a bet
      </button>
      <button
        className={styles.actionButton}
        onClick={() => {
          console.log("Go");
        }}
      >
        Start the race
      </button>
    </div>
  );
}
