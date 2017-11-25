#!/usr/bin/node

/*  Copyright (C) 2017 Milan Pässler

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. */

'use strict'

const Djv = require('djv')
const inputSchema = require('./res/input-schema.json')
const outputSchema = require('./res/output-schema.json')
const exec = require('child_process').execSync
const WebServer = require('./modules/webserver')
const fs = require('fs')

const djv = new Djv({
  version: 'draft-06'
})

let solverRunning = false
let problem = {"teachers": [], "students": [], "subjects": [], "roomTypes": []}
let courses = []
let stdplanData = {}

function convertFormat(input) {
  return {
    students: input.students.map(function(s) {
      let ns = Object.assign({}, s)
      delete ns.firstName
      delete ns.lastName
      return ns
    }),
    teachers: input.teachers.map(function(t) {
      let nt = Object.assign({}, t)
      delete nt.firstName
      delete nt.lastName
      return nt
    }),
    roomTypes: input.roomTypes.map(function(r) {
      let nr = Object.assign({}, r)
      delete nr.name
      return nr
    }),
    subjects: input.subjects.map(function(s) {
      let ns = Object.assign({}, s)
      delete s.name
      return ns
    })
  }
}

function stdplan() {
  stdplanData = {}
  let emptyRow = ['', '', '', '', '']
  let emptyWeek = []
  for (let i = 0; i < 10; i++) {
    emptyWeek.push(emptyRow)
  }
  let studentsDict = {}
  let subjectsDict = {}
  problem.students.forEach(function(s) {
    let fullName = s.firstName + ' ' + s.lastName
    if (stdplanData[fullName]) {
      fullName += ' (' + s.id + ')'
    }
    stdplanData[fullName] = [emptyWeek]
    studentsDict[s.id] = fullName
  })
  problem.subjects.forEach(function(s) {
    subjectsDict[s.id] = s
  })
  courses.forEach(function(c) {
    c.students.forEach(function (s) {
      c.hours.forEach(function(h) {
        stdplanData[studentsDict[s.id]][h[1]][h[0]] = subjectsDict[s.id].name
      })
    })
  })
}

function saveToDisk() {
  fs.writeFileSync('./data.json', JSON.stringify({
    stdplan: stdplanData,
    problem: problem,
    courses: courses
  }))
}

function loadFromDisk() {
  let data
  try {
    data = JSON.parse(fs.readFileSync('./data.json'))
  } catch(err) {
    return
  }
  stdplanData = data.stdplan
  problem = data.problem
  courses = data.courses
}

djv.addSchema('input', inputSchema)
djv.addSchema('output', outputSchema)

loadFromDisk()

const server = new WebServer()

server.listen('::', 4000)

server.route('GET /', function(req, res) {
  res.writeHead(200, { 'Content-Type': 'text/plain' })
  res.end('Hello user!')
})

server.route('GET /problem.json', function(req, res) {
  res.writeHead(200, { 'Content-Type': 'application/json' })
  res.end(JSON.stringify(problem))
})

server.route('GET /output.json', function(req, res) {
  res.writeHead(200, { 'Content-Type': 'application/json' })
  res.end(JSON.stringify(courses))
})

server.route('GET /stdplan.json', function(req, res) {
  res.writeHead(200, { 'Content-Type': 'application/json' })
  res.end(JSON.stringify(stdplanData))
})

server.route('GET /status', function(req, res) {
  res.writeHead(200, { 'Content-Type': 'text/plain' })
  res.end(solverRunning ? 'running' : 'waiting')
})

server.route('POST /problem.json', function(req, res, data) {
  console.log('foo');

  if (solverRunning) {
    res.writeHead(500, { 'Content-Type': 'text/plain' })
    res.end('Error: Solver still running')
  }

  // parse input
  let parsedInput
  try {
    parsedInput = JSON.parse(data)
  } catch(err) {
    res.writeHead(400, { 'Content-Type': 'text/plain' })
    res.end('Error: Invalid JSON')
    return
  }

  // validate input
  let inputValidationError = djv.validate('input', parsedInput)
  if (inputValidationError) {
    res.writeHead(400, { 'Content-Type': 'text/plain' })
    res.end('Error: Invalid JSON data:\n' + inputValidationError)
    return
  }

  problem = parsedInput

  solverRunning = true

  // run solver
  let output = exec('./dummy-solver', {
    input: JSON.stringify(convertFormat(parsedInput)) + '\n'
  })

  solverRunning = false

  // parse solver output
  let parsedOutput
  try {
    parsedOutput = JSON.parse(output)
  } catch(err) {
    res.writeHead(400, { 'Content-Type': 'text/plain' })
    res.end('Error: Error while processing data:\n' + output)
    return 
  }

  // validate solver output
  let outputValidationError = djv.validate('output', parsedOutput)
  if (outputValidationError) {
    res.writeHead(400, { 'Content-Type': 'text/plain' })
    res.end('Error: Invalid JSON data foo:\n' + outputValidationError)
    return
  }

  courses = parsedOutput

  res.writeHead(200, { 'Content-Type': 'text/plain' })
  res.end('OK')

  stdplan()
  saveToDisk()
})

