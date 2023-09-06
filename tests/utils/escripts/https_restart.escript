#!/usr/bin/env escript
%%! -name https_restart@test_env

-export([main/1]).

-define(NODE, list_to_atom("op_worker@dev-oneprovider-krakow-0.dev-oneprovider-krakow.default.svc.cluster.local")).

main([Duration]) ->
    compile:file(filename:dirname(escript:script_name()) ++ "/escript_utils.erl"),
    escript_utils:connect(?NODE),
    escript_utils:safe_call(?NODE, https_listener, stop, []),
    DurationInt = list_to_integer(Duration),
    timer:sleep(timer:seconds(DurationInt)),
    escript_utils:safe_call(?NODE, https_listener, start, []).
