'use strict';

var Client = require('battle/commander.js').Client;
var ROLE = require("battle/terms.js").ROLE;
var client = new Client();
var _ = {}

function whenIdle() {
	if (isReady()) {
		if (me().level >= 2) {
			timeout(1).then(whenReady) // to avoid the latest idle case
		} else {
			whenReady()
		}
	} else {
		client.whenIdle().then(whenIdle)
	}
}

function isReady() {
	if (client.askCurTime() < 10) return // avoid init only 1 client then ready

	/* not use === 'idle' is because lastest one just idle, but other bot alreay moved
	 * then idle bot will wait unitl other bot attacking, state will change to others
	 * so this idle bot can go next step
	 */
	return team()
		.every( item => item.state.action !== 'move') 
}

function timeout(sec) {
	if (me().level < 2) {
		var pos = me().coordinates
		var x = pos[0]
		var y = pos[1]
		var r = sec * me().speed / 2

		if (x < 30 && y > 20) {
			y -= r
		} else if (x > 30 && y > 20) {
			x -= r
		} else if (x > 30 && y < 20) {
			x -= r
		} else if (x < 30 && y < 20) {
			y += r
		}

		client.doMoves([
			[x,y],
			pos,
		])
		return client.whenIdle()
	} else {
		return client.whenTime(client.askCurTime() + sec)
	}
}

function targetPosition(from, to, r) {
	if (!from) {
		from = me().coordinates
	}
	if (!to) {
		to = client.askNearestEnemy(_.enemies).coordinates
	}
	if (!r) {
		r = me().firing_range
	}

	var x = from[0] - to[0]
	var y = from[1] - to[1]
	var z = pythagorean(x, y)
	var fireDistance = z - r
	var scale = z / fireDistance

	return {
		fireCoordinates: [
			from[0] - x / scale,
			from[1] - y / scale,
		],
		distance: z,
		fireDistance: fireDistance,
	}
}

function pythagorean(x, y) {
	return Math.pow(
		x*x + y*y,
		0.5
	)
}

function whenReady() {
	if (!_[me().type]) return

	switch (me().type) {
		case 'infantryBot':
			attack()
			break
		case 'rocketBot':
			var infantryLen = targetPosition(null,null,4).fireDistance
			var myLen = targetPosition().fireDistance
			var wait = infantryLen / 2 - myLen / me().speed
		  timeout(wait).then(attack)
			break
	}

	console.log(
		'EST',
		targetPosition().distance - targetPosition().fireDistance
	);
}

function me() {
	return client.askMyInfo()
}

function team() {
	return client.askMyItems()
}

function info(id) {
	return client.askItemInfo(id)
}

function position() {
	var x = {
		min: 20.25,
		max: 39.9,
	}
	var y = {
		min: 0,
		max: 39.75,
	}

	if (_.target === undefined) {
		str = me().coordinates[1] > y.max / 2 ? 'LT' : 'RT'
	}

	switch (_.target) {
		case 'LT':
			return [
				[x.max,y.max],
				[x.min,y.max],
			]
		case 'L':
			return [
				[x.max,y.max],
			]
		case 'RT':
			return [
				[x.max,y.min],
				[x.min,y.min],
			]
		case 'R':
			return [
				[x.max,y.min],
			]
		default:
			return _.target
	}
}

function attack() {
	var target = client.askNearestEnemy(_.enemies)
	if (me().level >= 4) {
		// rocket able to atk center, other can stop
	}
	if (target.type === 'machineGun') {
		if (me().type === 'infantryBot') {
			return client.whenItemDestroyed(target.id).then(whenReady)
		}
	}

//	client.doMove(targetPosition().fireCoordinates)

	client.doAttack(target.id)

	if (!_.once || me().type === 'rocketBot') {
		client.whenItemDestroyed(target.id).then(whenReady)
	}

	client.whenEnemyInRange().then( r => { 
		var target = client.askItemInfo(r.id)
		console.log(
			'act',
			targetPosition(null,target.coordinates).distance
		);
	})
}


_.target = 'LT'
_.once = !false
_.enemies = [
	ROLE.CENTER,
	ROLE.TOWER,
	//ROLE.UNIT,
	//ROLE.BUILDING,
	//ROLE.OBSTACLE,
	//ROLE.ALL,
]
_.infantryBot = true
_.rocketBot = true

client.doMoves(position())
client.whenIdle().then(whenIdle)

/* dead code
client.whenItemInArea(client.askCenter().coordinates, me.firing_range).then(
	(a,b,c) => {
		console.log('=====');
		console.log('inArea',a,b,c);
		console.log('-----');
	}
)
*/
