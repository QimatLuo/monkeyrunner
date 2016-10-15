"use strict";
var Client = require("battle/commander.js").Client;
var client = new Client();

var lastTarget
var priority = [
	'rocketBot',
	'infantryBot',
]
client.whenEnemyInRange().then(whenEnemyInRange);

function whenEnemyInRange() {
    var enemies = client.askMyRangeEnemyItems();
		enemies.sort(
			(a, b) => {
				return priority.indexOf(a.type) - priority.indexOf(b.type)
			}
		)

		var target = enemies[0]
		if (target.id === lastTarget.id) {
			client.whenEnemyInRange().then(whenEnemyInRange);
		} else {
			unitInFiringRange();
		}
}

function unitInFiringRange(data) {
		console.log('Attack %s%d', data.type, data.id);
		lastTarget = data
    client.doAttack(data.id);
		client.whenEnemyInRange().then(whenEnemyInRange);
		client.whenItemDestroyed(data.id).then(
			r => {
				console.log('%d destoryed', data.id);
			}
		)
}
