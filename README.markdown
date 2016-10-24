# papi

## Low-Boilerplate RESTful APIs

## Introduction

papi is a library that allows you to build powerful RESTful web services on top
of plain WSGI by writing backends as simple and semantic classes, and then
feeding them to its equally simple WSGI wrapper function.

## Features

- Proper RESTful semantics over HTTP(S): GET, PUT, POST, DELETE map to
  retrieve / list resources, create, update, delete
- Automatic routing
- Automatic HATEOAS decoration (adds links to parent, self, and children, on
  every JSON response)
- Semi-automatic content type negotiation: JSON is handled transparently, other
  content types are easy to support in your backend code
- Automatic translations of failures to HTTP error responses; uses the 4xx
  range of status codes correctly
- Runs on any compliant WSGI host, making it suitable for deployment under a
  wide range of web servers and protocols
