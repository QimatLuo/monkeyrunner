"use strict";
var Client = require("battle/commander.js").Client;
var client = new Client();

function searchNextTarget() {
    var enemies = client.askMyRangeEnemyItems();
    if (enemies.length) {
        unitInFiringRange(enemies[0]);
    } else {
        client.whenEnemyInRange().then(unitInFiringRange);
    }
}

function unitInFiringRange(data) {
    client.doAttack(data.id);
    client.whenIdle().then(searchNextTarget);
}

searchNextTarget();
