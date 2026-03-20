import json

import graphene
from graphql import graphql
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import Route

GRAPHIQL_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>D&D API — GraphiQL</title>
  <style>
    html, body { height: 100%%; margin: 0; overflow: hidden; }
    #graphiql { height: 100vh; }
  </style>
  <link rel="stylesheet"
        href="https://unpkg.com/graphiql@3/graphiql.min.css" />
</head>
<body>
  <div id="graphiql"></div>

  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/graphiql@3/graphiql.min.js"></script>

  <script>
    const fetcher = GraphiQL.createFetcher({ url: '%s' });
    const root = ReactDOM.createRoot(document.getElementById('graphiql'));
    root.render(React.createElement(GraphiQL, { fetcher: fetcher }));
  </script>
</body>
</html>
"""


def make_edition_graphql_app(gql_schema: graphene.Schema, edition: str) -> Starlette:
    """Starlette sub-app that serves GraphQL (POST) and GraphiQL (GET)."""

    async def _graphql_post(request: Request) -> Response:
        content_type = request.headers.get("content-type", "")

        if "application/json" in content_type:
            body = await request.json()
        else:
            raw = (await request.body()).decode()
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                body = {"query": raw}

        query = body.get("query", "")
        variables = body.get("variables")
        operation_name = body.get("operationName")

        result = await graphql(
            gql_schema.graphql_schema,
            source=query,
            variable_values=variables,
            operation_name=operation_name,
            context_value={"request": request, "edition": edition},
        )

        response_data: dict = {}
        if result.data is not None:
            response_data["data"] = result.data
        if result.errors:
            response_data["errors"] = [
                {"message": str(e), "locations": e.locations, "path": e.path}
                for e in result.errors
            ]

        return JSONResponse(response_data)

    async def _graphiql_get(request: Request) -> Response:
        graphql_url = str(request.url).split("?")[0]
        if not graphql_url.endswith("/"):
            graphql_url += "/"
        return HTMLResponse(GRAPHIQL_HTML % graphql_url)

    async def _root(request: Request) -> Response:
        if request.method == "POST":
            return await _graphql_post(request)
        return await _graphiql_get(request)

    return Starlette(
        routes=[
            Route("/", _root, methods=["GET", "POST"]),
            Route("/{path:path}", _root, methods=["GET", "POST"]),
        ],
    )
