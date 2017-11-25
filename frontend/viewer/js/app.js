"use strict"

var data, dsb

var date = new Date()
date.setHours(date.getHours() + 8)
if (date.getDay() === 6) date.setHours(date.getHours() + 24)
if (date.getDay() === 0) date.setHours(date.getHours() + 24)

var onejan = new Date(date.getFullYear(), 0, 1)
var week = Math.ceil((((date - onejan) / 86400000) + onejan.getDay() + 1) / 7)

var tabsInitialized = false

function setData(data, update) {
	var headers = ["Mo", "Di", "Mi", "Do", "Fr"]

	setWeekData(data[0], headers, date.getDay() - 1, true)

	$('#content').show()
	$('#fail').hide()

	if ($(window).width() <= 700 && !tabsInitialized) {
		tabsInitialized = true
		$('#tabs-0').tabs({swipeable: true})
		$('#tabs-1').tabs({swipeable: true})
		$('#tabs-0').tabs('select_tab', 'day-' + (date.getDay() - 1))
	}
}
$(window).resize(function() {
	if ($(window).width() <= 700 && !tabsInitialized) {
		tabsInitialized = true
		$('#tabs-0').tabs({swipeable: true})
		$('#tabs-1').tabs({swipeable: true})
		$('#tabs-0').tabs('select_tab', 'day-' + (date.getDay() - 1))
	}
})

function setWeekData(data, headers, day, thisweek) {
	var table = $('#table')
	table.empty()

	var max = 0
	for (var key1 in data) {
		var row = data[key1]
		for (var key2 in row) {
			if (row[key2] !== "" && key1 > max) max = key1
		}
	}

	var headersObj = $('<tr>').appendTo(table)
	for (var key in headers) {
		var item = headers[key]
		var obj = $('<th>').html(item)
		if (key == day && thisweek) obj.attr('class', 'today')
		headersObj.append(obj)
	}

	for (var i = 0; i < 5; i++) {
		$('#day-' + i).empty()
	}

	for (var key1 = 0; key1 <= max; key1++) {
		var row = data[key1]
		var rowObj = $('<tr>').appendTo(table)
		for (var key2 = 0; key2 < 5; key2++) {
			var item = row[key2]
			var obj = $('<td>').html(item)
			if (key2 == day && thisweek) obj.attr('class', 'today')
			rowObj.append(obj)
			$('#day-' + key2).append($('<div>').html(item))
		}
	}
}

$('input#search').on('focus', function(evt) {
	$('#content').hide()
})
$('input#search').on('blur', function(evt) {
	if ($('#fail').css('display') == "none") {
		setTimeout(function() {
		$('#content').show()
		}, 200)
	}
})
$('.input-field .close').click(function(evt) {
	$(evt.target).prev().val('')
	$('input#search').focus()
})

var selected = localStorage.getItem('selected')
if (!selected) {
	$('#fail').show()
	$('input#search').focus()
}

function updateData(update) {
	var index = Object.keys(data).reduce(function(acc, cur, i) {
		acc[cur] = null
		return acc
	}, {})

	if (selected && selected in data) {
		$('input#search').val(selected)
		setData(data[selected], update)
	} else {
		$('#fail').show()
		$('input#search').focus()
	}

	$('input#search').autocomplete({
		data: index,
		limit: 30,
		minLength: 1,
		onAutocomplete: function(val) {
			setData(data[val], false)
			localStorage.setItem('selected', val)
		}
	})
}

$.getJSON("http://127.0.0.1:4000/stdplan.json").done(function(res) {
	data = res
	updateData(false)
})

/*if ('serviceWorker' in navigator) {
	navigator.serviceWorker.register('sw.js', {
		scope: './'
	})

	navigator.serviceWorker.onmessage = function(evt) {
		var msg = JSON.parse(evt.data)
		if (msg.type === 'planinfo') {
			data = JSON.parse(msg.data)
			updateData(true)
		} else if (msg.type === 'dsb') {
			data = JSON.parse(msg.data)
			updateData(true)
		}
	}
}*/


