#!/usr/bin/env escript
%%! -name oc_test@test_env

-export([main/1]).

-define(NODE, list_to_atom("op_worker@dev-oneprovider-krakow-0.dev-oneprovider-krakow.default.svc.cluster.local")).

main([Duration]) ->
    escript_utils:connect(?NODE),
    erlang:set_cookie(?NODE, cluster_node),
    escript_utils:safe_call(?NODE, https_listener, stop, []),
    DurationInt = list_to_integer(Duration),
    timer:sleep(timer:seconds(DurationInt)),
    escript_utils:safe_call(?NODE, https_listener, start, []).
