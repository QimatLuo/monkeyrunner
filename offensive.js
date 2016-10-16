'use strict';

var Client = require('battle/commander.js').Client;
var ROLE = require("battle/terms.js").ROLE;
var client = new Client();
var _ = {
	pathHistory: [],
}

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

		client.doMoves([ [x,y], pos ]) // don't use go(), this is fake move
		return client.whenIdle()
	} else {
		return client.whenTime(client.askCurTime() + sec)
	}
}

function back(n) {
	n = n || 1
	var path = _.pathHistory.splice(_.pathHistory.length - n)
	client.doMoves(path.reverse())
}

function go(path) {
	_.pathHistory = _.pathHistory.concat(path)
	client.doMoves(path)
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
	console.log('I am %s', me().type);
	var cmds = _[me().type]
	if (!cmds.length) return

	var cmd = cmds.shift()
	console.log('CMD:', cmd);

	if (Array.isArray(cmd)) {
		go(cmd)
		client.whenIdle().then(whenReady)
	} else {
		if (cmd === 'auto') {
			cmds.push(cmd)
		}
		switch (me().type) {
			case 'infantryBot':
				attack(cmd)
				break
			case 'rocketBot':
				var infantryLen = targetPosition(null,null,4).fireDistance
				var myLen = targetPosition().fireDistance
				var wait = infantryLen / 2 - myLen / me().speed
				console.log('wait %ds', wait);
				timeout(wait).then(
					() => {
						attack(cmd)
					}
				)
				break
		}
	}
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

function position(path) {
	var x = {
		min: 20.25,
		max: 39.9,
	}
	var y = {
		min: 0,
		max: 39.75,
	}

	if (path === 'LR') {
		path = me().coordinates[1] > y.max / 2 ? 'LT' : 'RT'
	}

	switch (path) {
		case 'LT':
			path = [
				[x.max,y.max],
				[x.min,y.max],
			]
			break
		case 'L':
			path = [
				[x.max,y.max],
			]
			break
		case 'RT':
			path = [
				[x.max,y.min],
				[x.min,y.min],
			]
			break
		case 'R':
			path = [
				[x.max,y.min],
			]
			break
	}

	if (!path) {
		path = [me().coordinates]
	}

	return path
}

function attack(role) {
	var target = client.askNearestEnemy(role === 'auto' ? _.enemies : [role])
	if (me().type === 'infantryBot') {
		switch (target.type) {
			case 'commandCenter':
				back(9)
				return
			case 'machineGun':
				return client.whenItemDestroyed(target.id).then(whenReady)
		}
	}

	console.log('Target is %s%d', target.type, target.id);
	console.log(
		'Est fire distance:',
		targetPosition().distance - targetPosition().fireDistance
	);

	if (me().type === 'rocketBot' && target.type === 'commandCenter') {
		console.log('lv4 doMessage("rocket able to atk center, other can stop")');
	}

	client.doAttack(target.id)

	client.whenItemDestroyed(target.id).then(whenReady)

	client.whenEnemyInRange().then( r => {
		var target = client.askItemInfo(r.id)
		console.log(
			'Enemy %d in range: %d',
			target.id,
			targetPosition(null,target.coordinates).distance
		);
	})
}


_.enemies = [
	ROLE.CENTER,
	ROLE.TOWER,
	//ROLE.UNIT,
	//ROLE.BUILDING,
	//ROLE.OBSTACLE,
	//ROLE.ALL,
]
_.infantryBot = [
	'auto',
]
_.rocketBot = [
	'auto',
]
go(position('RT')) // this will effect isReady(), don't put in cmds
client.whenIdle().then(whenIdle)
