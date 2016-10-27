'use strict';

var Client = require('battle/commander.js').Client;
var ROLE = require("battle/terms.js").ROLE;
var client = new Client();
var _ = {
	askMyInfo: client.askMyInfo(),
}

function whenIdle() {
	if (isReady()) {
		if (me('level') >= 2) {
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
		.every( item => item.state.action !== 'move' )
}

function timeout(sec) {
	if (me('level') < 2) {
		var pos = me('coordinates')
		var x = pos[0]
		var y = pos[1]
		var r = sec * me('speed') / 2

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

function go(path) {
	client.doMoves(path)
}

function targetPosition(from, to, r) {
	if (!from) {
		from = me('coordinates')
	}
	if (!to) {
		to = client.askNearestEnemy(_.enemies).coordinates
	}
	if (!r) {
		r = me('firing_range')
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
	var target = findTarget()
	if (target.type === 'rocketGun') {
		var goDie = team().sort(
			(a, b) => {
				return b.hit_points - a.hit_points
			}
		)[0]

		if (me('id') === goDie.id) {
			attack(target)
		} else {
			client.whenTime(client.askCurTime() + 1).then(
				() => {
					attack(target)
				}
			)
		}
	} else {
		attack(target)
	}
	client.whenItemDestroyed(target.id).then(whenReady)
}

function me(attr) {
	if (attr === 'coordinates') {
		_.askMyInfo = client.askMyInfo()
	}
	return _.askMyInfo[attr]
}

function team(type) {
	if (type) {
		var output
		client.askMyItems().some(
			item => {
				if (item.type === type) {
					output = item
					return true
				}
			}
		)
		return output
	} else {
		return client.askMyItems()
	}
}

function info(id) {
	return client.askItemInfo(id)
}

function position(path) {
	var x = {
		min: 20,
		max: 40,
	}
	var y = {
		min: 0,
		max: 40,
	}

	if (path === 'LR') {
		path = me('coordinates')[1] > y.max / 2 ? 'LT' : 'RT'
	}

	switch (path) {
		case 'C':
			path = [
				[x.max,y.max/2],
			]
			break
		case 'CC':
			path = [
				[x.max,y.max/2],
				[(x.min + x.max)/2,y.max/2],
			]
			break
		case 'CT':
			path = [
				[x.max,y.max/2],
				[x.min,y.max/2],
			]
			break
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
		path = [me('coordinates')]
	}

	return path
}

function findTarget() {
	var target = client.askTowers().filter(
		item => {
			return item.type === 'rocketGun'
		}
	)[0]

	target = target || client.askNearestEnemy( _.enemies)
	if (target.type !== 'commandCenter') return target

	var rocketRange = 8
	var me2target = targetPosition(null, null, rocketRange)
	var unSafe = client.askTowers().some(
		tower => {
			var pos2tower = targetPosition(me2target.fireCoordinates, tower.coordinates)
			return pos2tower.distance <= tower.firing_range
		}
	)
	if (unSafe) {
		target = client.askNearestEnemy([ROLE.TOWER])
	}
	return target
}

function attack(target) {
	if (info(target.id).is_dead) {
		client.whenIdle().then(whenReady)
	} else {
		client.doAttack(target.id)
	}
}


_.enemies = [
	ROLE.CENTER,
	ROLE.TOWER,
]
go(position('C')) // this will effect isReady(), don't put in cmds
client.whenIdle().then(whenIdle)
