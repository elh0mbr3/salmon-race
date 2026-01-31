'use client';

import React from "react";


export default function Buttons(){
    var thingymajiggywhatchamacallit;
    return (<div>
                <button onClick={() => {
                    thingymajiggywhatchamacallit = prompt("Select a salmon to bet on.");
                    if(thingymajiggywhatchamacallit!=null){
                        thingymajiggywhatchamacallit=parseInt(thingymajiggywhatchamacallit)
                        if(!isNaN(thingymajiggywhatchamacallit)&&0<thingymajiggywhatchamacallit&&thingymajiggywhatchamacallit<11){
                            console.log(thingymajiggywhatchamacallit-1);
                        }
                    }
                }}>
                    Place a bet
                </button>
                <button onClick={() => {
                    console.log('Go')
                }}>
                    Start the race
                </button>
            </div>)
}
