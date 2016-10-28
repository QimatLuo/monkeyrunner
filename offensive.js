'use strict';

var Client = require('battle/commander.js').Client;
var ROLE = require("battle/terms.js").ROLE;
var client = new Client();
var _ = {
	askMyInfo: client.askMyInfo(),
	logs: [],
	pathHistory: [],
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
		.every( item => item.state.action !== 'move') 
}

function printLogs() {
	if (_.logs.length) {
		console.log.apply(null, _.logs.splice(0))
	}
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

function back() {
	var rocket = team('rocketBot')

	if (rocket) {
		client.doMove(rocket.coordinates)
		_.logs.push('back to rockets')
	} else {
		var last2me = p2p(_.pathHistory.pop(), me('coordinates'))
		_.logs.push('back to last pos')
		client.doMove(last2me.fireCoordinates)
	}

	printLogs()
}

function go(path) {
	_.pathHistory = _.pathHistory.concat(path)
	client.doMoves(path)
}

function p2p(from, to, r) {
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
	_.logs.push('I am ' +  me('type'))
	var cmds = _[me('type')]
	if (!cmds.length) return

	var cmd = cmds.shift()
	_.logs.push('CMD: ' + cmd)

	if (Array.isArray(cmd)) {
		go(cmd)
		client.whenIdle().then(whenReady)
	} else {
		if (cmd === 'auto') {
			cmds.push(cmd)
		}

		var target = findTarget()
		switch (me('type')) {
			case 'heavyBot':
				attack(target)
				break
			case 'infantryBot':
				waitThenAttack(target)
				break
			case 'rocketBot':
				if (
					target.type === 'commandCenter' ||
					target.type === 'machineGun'
				) {
					attack(target)
				} else {
					waitThenAttack(target)
				}
				break
		}
		client.whenItemDestroyed(target.id).then(whenReady)
	}
}

function waitThenAttack(target) {
	var heavy = team('heavyBot')
	if (!heavy) {
		return attack(target)
	}

	var heavy2target = p2p(heavy.coordinates,target.coordinates)
	var hurtLen = heavy2target.distance - target.firing_range / 2
	var myLen = p2p(null, target.coordinates).fireDistance
	var wait = hurtLen / heavy.speed - myLen / me('speed')
	_.logs.push('wait ' + wait + 's')
	printLogs()

	if (wait < 0) {
		attack(target)
	} else {
		timeout(wait).then(
			() => {
				attack(target)
			}
		)
	}
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
				[1, 0.5],
			]
			break
		case 'CC':
			path = [
				[1, 0.5],
				[0.5, 0.5],
			]
			break
		case 'CT':
			path = [
				[1, 0.5],
				[0, 0.5],
			]
			break
		case 'L':
			path = [
				[1, 1],
			]
			break
		case 'LC':
			path = [
				[1, 1],
				[0.5, 1],
			]
			break
		case 'LT':
			path = [
				[1, 1],
				[0, 1],
			]
			break
		case 'R':
			path = [
				[1, 0],
			]
			break
		case 'RC':
			path = [
				[1, 0],
				[0.5, 0],
			]
			break
		case 'RT':
			path = [
				[1, 0],
				[0, 0],
			]
			break
	}

	if (Array.isArray(path)) {
		path = path.map(
			pos => {
				return [
					x.min + (x.max - x.min) * pos[0],
					y.min + (y.max - y.min) * pos[1],
				]
			}
		)
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
	var me2target = p2p(null, null, rocketRange)
	var unSafe = client.askTowers().some(
		tower => {
			var pos2tower = p2p(me2target.fireCoordinates, tower.coordinates)
			return pos2tower.distance <= tower.firing_range
		}
	)
	if (unSafe) {
		target = client.askNearestEnemy([ROLE.TOWER])
	}
	return target
}

function attack(target) {
	switch (me('type')) {
		case 'rocketBot':
			switch (target.type) {
				case 'commandCenter':
					_.logs.push('lv4 doMessage("rocket able to atk center, other can stop")')
					break
			}
			break
	}

	client.whenEnemyInRange().then( r => {
	})

	if (info(target.id).is_dead) {
		_.logs.push(target.type + target.id + ' is dead')
		printLogs()
		client.whenIdle().then(whenReady)
	} else {
		printLogs()
		client.doAttack(target.id)
	}
}


_.enemies = [
	ROLE.CENTER,
	ROLE.TOWER,
	//ROLE.UNIT,
	//ROLE.BUILDING,
	//ROLE.OBSTACLE,
	//ROLE.ALL,
]
_.heavyBot = [
	'auto',
]
_.infantryBot = [
	'auto',
]
_.rocketBot = [
	'auto',
]
go(position('C')) // this will effect isReady(), don't put in cmds
client.whenIdle().then(whenIdle)
