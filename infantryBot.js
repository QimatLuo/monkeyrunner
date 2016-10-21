'use strict';

var Client = require('battle/commander.js').Client;
var ROLE = require("battle/terms.js").ROLE;
var client = new Client();
var _ = {
	askMyInfo: client.askMyInfo(),
	message: 0,
}

function whenMessage(r) {
	if (!isReady()) {
		client.whenMessage().then(whenMessage)
	}
}

function isReady() {
	_.message++
	if (_.message !== team().length) return

	whenReady()
	return true
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
go(position('RT')) // this will effect isReady(), don't put in cmds
client.whenIdle().then(() => {
	client.doMessageToTeam(_.message)
	isReady()
})
client.whenMessage().then(whenMessage)
