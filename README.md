# openIMIS Backend Product reference module
This repository holds the files of the openIMIS Backend Product reference module. It is dedicated to be deployed as a module of [openimis-be_py](https://github.com/openimis/openimis-be_py).

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## Code climat (develop branch)

[![Maintainability](https://img.shields.io/codeclimate/maintainability/openimis/openimis-be-policy_py.svg)](https://codeclimate.com/github/openimis/openimis-be-policy_py/maintainability)
[![Test Coverage](https://img.shields.io/codeclimate/coverage/openimis/openimis-be-policy_py.svg)](https://codeclimate.com/github/openimis/openimis-be-policy_py)

## ORM mapping:
* tblProduct > Product (partial mapping)
* tblProductItems > ProductItem
* tblProductServices > ProductService

## Listened Django Signals
None

## Services
None

## Reports (template can be overloaded via report.ReportDefinition)
None

## GraphQL Queries
* products
* products_str: full text search on product code and name

## GraphQL Mutations - each mutation emits default signals and return standard error lists (cfr. openimis-be-core_py)
None

## Configuration options (can be changed via core.ModuleConfiguration)
* gql_query_products_perms: required rights to call products and products_str gql(Default: [])

## openIMIS Modules Dependencies
None
