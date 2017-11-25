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

module.exports = function() {

  const index = {}

  const server = http.createServer(function(req, stream) {
    stream.setHeader('Access-Control-Allow-Origin', '*')

    let url = require('url').parse(req.url, true) // true to get query as object
    let success = false

    if (url.pathname in index) {
      index[url.pathname](stream, url.query)
    } else {
      stream.writeHead(404, { 'Content-Type': 'text/plain' })
      stream.end('404')
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
