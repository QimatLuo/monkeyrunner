'use strict';

var Client = require('battle/commander.js').Client;
var ROLE = require("battle/terms.js").ROLE;
var client = new Client();
var _ = {}

function whenIdle() {
	if (isReady()) {
		if (me().level >= 2) {
			time(1).then(whenTogether)
		} else {
			whenTogether()
		}
	} else {
		client.whenIdle().then(whenIdle)
	}
}

function isReady() {
	if (client.askCurTime() < 10) return

	return team()
		.every( item => item.state.action !== 'move')
}

function time(sec) {
	return client.whenTime(client.askCurTime() + sec)
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

function attackNearest() {
	let enemies = client.askTowers()
	enemies.push(client.askCenter())
	enemies.sort(
		(a, b) => {
			return distance(a) - distance(b)
		}
	)
	let target = enemies[0]

	client.doAttack(target.id)
	client.whenItemDestroyed(target.id).then(attackNearest)
}

function distance(item) {
	let x = Math.abs(item.coordinates[0] - me().coordinates[0])
	let y = Math.abs(item.coordinates[1] - me().coordinates[1])

	return Math.pow((x*x + y*y), 0.5)
}

function attackCenter() {
	let target = client.askCenter()
	client.doAttack(target.id)

	let targetPos = targetPosition(
		me().coordinates,
		target.coordinates
	)
	console.log(targetPos)

	let tower = client.askNearestEnemy([ROLE.TOWER])
	let towerPos = tower.coordinates
	let x =	targetPos[0] - towerPos[0]
	let y =	targetPos[1] - towerPos[1]
	let z = Math.pow(x*x + y*y, 0.5)
	if (z > tower.firing_range) {
		console.log('safe')
	} else {
		console.log('unsafe')
	}
	client.whenEnemyInRange(target.id).then(
		(r) => {
			console.log(r)
			console.log(me().coordinates)
		}
	)
}

function fakeTimeout(sec) {
	let pos = me().coordinates
	let x = pos[0]
	let y = pos[1]

	if (x < 30 && y > 20) {
		y -= sec
	} else if (x > 30 && y > 20) {
		x -= sec
	} else if (x > 30 && y < 20) {
		x -= sec
	} else if (x < 30 && y < 20) {
		y += sec
	}

	client.doMoves([
		[x,y],
		pos,
	])
}

function attack() {
	if (_.center) {
		attackCenter()
	} else {
		attackNearest()
	}
}

function position(str) {
	let x = {
		min: 20.25,
		max: 39.9,
	}
	let y = {
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

function targetPosition(from, to) {
	console.log(from, to)
	let x = from[0] - to[0]
	let y = from[1] - to[1]
	let z = pythagorean(x, y)
	let scale = z / (z - me().firing_range)
	return [
		from[0] - x / scale,
		from[1] - y / scale,
	]
}

function pythagorean(x, y) {
	return Math.pow(
		x*x + y*y,
		0.5
	)
}

function whenTogether() {
	if (!_[me().type]) return

	switch (me().type) {
		case 'infantryBot':
			attack()
			break
		case 'rocketBot':
			if (me().level >= 2) {
				time(1).then(attack)
			} else {
				fakeTimeout(5)
				client.whenIdle().then(attack)
			}
			break
	}
}

_.target = 'LT'
_.center = true
_.infantryBot = true
_.rocketBot = true

client.doMoves(position())
client.whenIdle().then(whenIdle)
	console.log(me().speed)
