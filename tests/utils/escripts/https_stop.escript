#!/usr/bin/env escript
%%! -name https_stopt@test_env

-export([main/1]).

-define(NODE, list_to_atom("op_worker@dev-oneprovider-krakow-0.dev-oneprovider-krakow.default.svc.cluster.local")).

main([]) ->
    compile:file(filename:dirname(escript:script_name()) ++ "/escript_utils.erl"),
    escript_utils:connect(?NODE),
    escript_utils:safe_call(?NODE, https_listener, stop, []).
