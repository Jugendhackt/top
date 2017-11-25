/*  Copyright (C) 2017 Milan Pässler
    Copyright (C) 2016 HopGlass Server contributors

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

const http = require('http')
const url = require('url')

module.exports = function() {

  const index = {}

  const server = http.createServer(function(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*')

    let requestUrl = url.parse(req.url, true) // true to get query as object
    let success = false

    let path = req.method + ' ' + requestUrl.pathname
    if (path in index) {
      if (req.method === 'POST') {
        let data = ''
        req.on('data', function (chunk) {
          data += chunk;
        })
        req.on('end', function () {
          index[path](req, res, data, requestUrl.query)
        })
      } else {
        index[path](req, res, requestUrl.query)
      }
    } else {
      res.writeHead(404, { 'Content-Type': 'text/plain' })
      res.end('404')
    }
  })

  return {
    listen: function listen(ip, port) {
      server.listen(port, ip, function() {
        console.log('webserver listening on port ' + port)
      })
    },
    route: function route(path, func) {
      index[path] = func
    }
  }
}
