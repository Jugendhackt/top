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
const fs = require('fs')

module.exports = function(dir) {

  const mimeTypes = {
    'html': 'text/html',
    'js': 'text/javascript',
    'css': 'text/css',
    'json': 'application/json',
    'png': 'image/png',
    'jpg': 'image/jpg',
    'gif': 'image/gif',
    'wav': 'audio/wav',
    'mp4': 'video/mp4',
    'woff': 'application/font-woff',
    'ttf': 'application/font-ttf',
    'eot': 'application/vnd.ms-fontobject',
    'otf': 'application/font-otf',
    'svg': 'application/image/svg+xml',
    'woff2': 'font/woff2'
  }

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
      let filePath = dir + requestUrl.pathname

      fs.stat(filePath, function(err, stats) {
        if (!err && stats.isDirectory()) {
          if (requestUrl.pathname.slice(-1) === '/') {
            filePath += 'index.html'
          } else {
            res.writeHead(301, { 'Location': requestUrl.pathname + '/' })
            res.end()
            return
          }
        }

        let extname = filePath.split('.').pop().toLowerCase()
        let contentType = mimeTypes[extname] || 'text/html'

        fs.readFile(filePath, function(error, content) {
          if (error) {
            res.writeHead(404, { 'Content-Type': 'text/plain' })
            res.end('404')
          } else {
            res.writeHead(200, { 'Content-Type': contentType })
            res.end(content, 'utf-8')
          }
        })
      })

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
